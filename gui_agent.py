import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import json
import google.generativeai as genai

# Import the refactored agent logic
from web_to_json_agent import run_web_to_json_conversion, configure_gemini, DEFAULT_MAX_PAGES, ensure_scheme

class ModernWebToJsonApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Web Content to LLM JSON v2.0")
        self.root.geometry("700x800") # Adjusted size

        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        # print(f"Available themes: {available_themes}")
        # Try common cross-platform themes first
        preferred_themes = ['clam', 'alt', 'default'] # 'vista' and 'xpnative' are Windows-specific
        for theme in preferred_themes:
            if theme in available_themes:
                try:
                    self.style.theme_use(theme)
                    # print(f"Using theme: {theme}")
                    break
                except tk.TclError:
                    continue

        # Global padding for frames and widgets for a more spaced-out look
        self.frame_padding = {"padx": 10, "pady": 10}
        self.widget_padding = {"padx": 7, "pady": 7}

        # --- API Key --- (StringVar)
        self.api_key_var = tk.StringVar()
        
        # --- Crawl Settings --- (StringVars and IntVars for easy get/set)
        self.start_url_var = tk.StringVar()
        self.num_pages_var = tk.IntVar(value=DEFAULT_MAX_PAGES)
        self.output_file_path = "" # Will be set by filedialog

        # --- Advanced Settings --- 
        self.gemini_model_var = tk.StringVar(value='gemini-1.5-flash-latest')
        self.request_delay_var = tk.DoubleVar(value=2.0) # Allow float for delay
        self.max_chars_var = tk.IntVar(value=28000)
        
        self.generated_data = None
        self.processing_thread = None

        self.setup_ui()

    def setup_ui(self):
        # Main container frame
        main_container = ttk.Frame(self.root, padding=(self.frame_padding["padx"], self.frame_padding["pady"]))
        main_container.pack(fill=tk.BOTH, expand=True)

        # --- Top section for API key and basic crawl config ---
        top_config_frame = ttk.Frame(main_container)
        top_config_frame.pack(fill=tk.X, expand=False, pady=(0,10))

        # API Key Frame (within top_config_frame)
        api_frame = ttk.LabelFrame(top_config_frame, text="Step 1: Gemini API Key", padding=(self.frame_padding["padx"], self.frame_padding["pady"]))
        api_frame.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0,5))
        
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky="w", **self.widget_padding)
        api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=40, show="*")
        api_key_entry.grid(row=0, column=1, sticky="ew", **self.widget_padding)
        
        self.set_api_key_button = ttk.Button(api_frame, text="Set/Verify API Key", command=self.handle_api_key_submission, style='Accent.TButton')
        self.set_api_key_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=self.widget_padding["padx"], pady=(5, self.widget_padding["pady"]))

        self.api_status_label = ttk.Label(api_frame, text="API Key Status: Not Set")
        self.api_status_label.grid(row=2, column=0, columnspan=2, sticky="w", **self.widget_padding)
        api_frame.columnconfigure(1, weight=1)

        # Basic Crawl Settings (within top_config_frame)
        basic_crawl_frame = ttk.LabelFrame(top_config_frame, text="Step 2: Basic Crawl Settings", padding=(self.frame_padding["padx"], self.frame_padding["pady"]))
        basic_crawl_frame.pack(fill=tk.X, expand=True, side=tk.LEFT)

        ttk.Label(basic_crawl_frame, text="Start URL:").grid(row=0, column=0, sticky="w", **self.widget_padding)
        url_entry = ttk.Entry(basic_crawl_frame, textvariable=self.start_url_var, width=40)
        url_entry.grid(row=0, column=1, sticky="ew", **self.widget_padding)
        ttk.Label(basic_crawl_frame, text="Num Pages:").grid(row=1, column=0, sticky="w", **self.widget_padding)
        num_pages_entry = ttk.Spinbox(basic_crawl_frame, from_=1, to=1000, textvariable=self.num_pages_var, width=7)
        num_pages_entry.grid(row=1, column=1, sticky="w", **self.widget_padding)
        basic_crawl_frame.columnconfigure(1, weight=1)

        # --- Advanced Settings Frame (collapsible or separate section) ---
        advanced_settings_frame = ttk.LabelFrame(main_container, text="Advanced Settings", padding=(self.frame_padding["padx"], self.frame_padding["pady"]))
        advanced_settings_frame.pack(fill=tk.X, expand=False, pady=(0,10))

        ttk.Label(advanced_settings_frame, text="Gemini Model:").grid(row=0, column=0, sticky="w", **self.widget_padding)
        # Common models, user can type in others if needed or we can fetch dynamically if API key is set
        model_options = ['gemini-1.5-flash-latest', 'gemini-1.5-pro-latest', 'gemini-1.0-pro', 'gemini-pro'] 
        model_dropdown = ttk.Combobox(advanced_settings_frame, textvariable=self.gemini_model_var, values=model_options, width=27)
        model_dropdown.grid(row=0, column=1, sticky="ew", **self.widget_padding)

        ttk.Label(advanced_settings_frame, text="Request Delay (s):").grid(row=0, column=2, sticky="w", **self.widget_padding)
        delay_spinbox = ttk.Spinbox(advanced_settings_frame, from_=0.5, to=60.0, increment=0.5, textvariable=self.request_delay_var, width=7)
        delay_spinbox.grid(row=0, column=3, sticky="w", **self.widget_padding)

        ttk.Label(advanced_settings_frame, text="Max Chars (Gemini):").grid(row=1, column=0, sticky="w", **self.widget_padding)
        max_chars_spinbox = ttk.Spinbox(advanced_settings_frame, from_=1000, to=100000, increment=1000, textvariable=self.max_chars_var, width=10)
        max_chars_spinbox.grid(row=1, column=1, sticky="ew", **self.widget_padding)
        
        advanced_settings_frame.columnconfigure(1, weight=1)
        advanced_settings_frame.columnconfigure(3, weight=1)

        # --- Action Buttons Frame ---
        action_frame = ttk.Frame(main_container, padding=(self.frame_padding["padx"], 10))
        action_frame.pack(fill=tk.X, expand=False)

        self.start_button = ttk.Button(action_frame, text="Start Processing", command=self.start_processing_thread, state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=(0,10))
        
        self.download_button = ttk.Button(action_frame, text="Save Result Again", command=self.save_json_file, state=tk.DISABLED)
        self.download_button.pack(side=tk.LEFT)

        # Themed button style (example)
        self.style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), padding=(self.widget_padding['padx'], self.widget_padding['pady']))

        # --- Log Area ---
        log_frame = ttk.LabelFrame(main_container, text="Progress Log", padding=(self.frame_padding["padx"], self.frame_padding["pady"]))
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10, relief=tk.SOLID, borderwidth=1)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.log_text.configure(state='disabled')

    def handle_api_key_submission(self):
        key = self.api_key_var.get()
        if not key:
            messagebox.showerror("API Key Error", "API Key cannot be empty.")
            self.api_status_label.config(text="API Key Status: EMPTY!", foreground="red")
            return
        
        self.log_message(f"Attempting to configure Gemini with API key and model: {self.gemini_model_var.get()}...")
        if configure_gemini(key, self.gemini_model_var.get()): # Pass selected model
            self.log_message("Gemini API Key configured successfully.")
            self.api_status_label.config(text=f"API Key Status: OK ({self.gemini_model_var.get()})", foreground="green")
            self.start_button.config(state=tk.NORMAL)
        else:
            self.log_message("Failed to configure Gemini. Check console for errors. Q&A generation will be skipped.")
            self.api_status_label.config(text=f"API Key Status: FAILED ({self.gemini_model_var.get()})", foreground="red")
            self.start_button.config(state=tk.NORMAL) # Allow processing even if Gemini fails, will skip Q&A

    def start_processing_thread(self):
        raw_start_url = self.start_url_var.get()
        if not raw_start_url:
            messagebox.showerror("Input Error", "Start URL cannot be empty.")
            return
        
        start_url_val = ensure_scheme(raw_start_url)
        num_pages_val = self.num_pages_var.get()
        model_to_use = self.gemini_model_var.get()
        delay_val = self.request_delay_var.get()
        max_chars_val = self.max_chars_var.get()

        if num_pages_val <= 0:
            messagebox.showerror("Input Error", "Number of pages must be a positive integer.")
            return

        self.output_file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Output JSON As"
        )
        if not self.output_file_path:
            self.log_message("Output file not selected. Aborting.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.set_api_key_button.config(state=tk.DISABLED)
        self.download_button.config(state=tk.DISABLED)
            
        self.log_message(f"Starting process for {start_url_val}, up to {num_pages_val} pages.")
        self.log_message(f"Output will be saved to: {self.output_file_path}")

        self.processing_thread = threading.Thread(target=self.run_agent_logic, 
                                            args=(start_url_val, num_pages_val, model_to_use, 
                                                  delay_val, max_chars_val))
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def run_agent_logic(self, start_url_val, num_pages_val, model_val, delay_val, max_chars_val):
        try:
            self.generated_data = run_web_to_json_conversion(
                start_url_from_user=start_url_val,
                num_pages=num_pages_val,
                output_file=self.output_file_path,
                api_key_to_use=self.api_key_var.get(),
                progress_callback=self.log_message,
                model_name_to_use=model_val,
                request_delay_seconds=delay_val,
                max_chars_for_gemini=max_chars_val
            )
            self.log_message("Processing finished.")
            if self.generated_data is not None: # Check if data is None (e.g. if run_web_to_json_conversion returns [] on error)
                 self.log_message(f"Successfully processed. Data saved to {self.output_file_path}")
                 if self.generated_data: # Only enable download if there's actual data
                    self.download_button.config(state=tk.NORMAL)
            else:
                self.log_message("Processing completed, but no data was generated or an error occurred. Check logs.")

        except Exception as e:
            self.log_message(f"An unexpected error occurred in GUI during processing: {e}")
            import traceback
            self.log_message(traceback.format_exc()) # Log full traceback to GUI log
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.set_api_key_button.config(state=tk.NORMAL)

    def log_message(self, message):
        if hasattr(self, 'log_text') and self.log_text.winfo_exists():
            self.log_text.configure(state='normal')
            self.log_text.insert(tk.END, str(message) + "\n") # Ensure message is string
            self.log_text.see(tk.END)
            self.log_text.configure(state='disabled')
            self.root.update_idletasks() 
        else:
            print(str(message)) 

    def save_json_file(self):
        if not self.generated_data:
            messagebox.showinfo("No Data", "No data has been generated yet to save.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=self.output_file_path if self.output_file_path else "fine_tuning_data.json",
            title="Save Output JSON As"
        )
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.generated_data, f, indent=4, ensure_ascii=False)
                self.log_message(f"Data successfully re-saved to {path}")
                self.output_file_path = path 
            except IOError as e:
                messagebox.showerror("Save Error", f"Error saving data to {path}: {e}")
        else:
            self.log_message("Save operation cancelled.")

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernWebToJsonApp(root)
    root.mainloop() 