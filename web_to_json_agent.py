import argparse
import json
import time
import requests
from bs4 import BeautifulSoup
import trafilatura
import google.generativeai as genai
from urllib.parse import urljoin, urlparse, ParseResult
import robotexclusionrulesparser
import os # Added for environment variable access

# --- Configuration ---
# Gemini API Key (Configure this securely, e.g., via environment variable)
# GENAI_API_KEY = "YOUR_GEMINI_API_KEY"
# genai.configure(api_key=GENAI_API_KEY)

# Default number of pages to crawl
DEFAULT_MAX_PAGES = 10

# Request headers
HEADERS = {
    "User-Agent": "WebToJsonAgent/1.0 (Python; +http://example.com/botinfo)" # Replace with your bot info URL
}

# Delay between requests (in seconds)
REQUEST_DELAY = 2

# --- Global variable for Gemini model ---
# This allows us to configure it once with the API key
gemini_model = None

def ensure_scheme(url_string):
    """Adds https:// to a URL if no scheme is present."""
    parsed = urlparse(url_string)
    if not parsed.scheme:
        # Try to guess if it's a local file path or a web URL missing a scheme
        if not parsed.netloc and parsed.path == url_string: # Likely a path, check if it could be a domain
            if '.' in url_string.split('/')[-1]: # Simple check for a dot, might be domain
                return f"https://{url_string}"
            else: # Treat as a file path, no change for now, or handle as error later
                return url_string
        return f"https://{url_string}"
    # Check if the scheme is one of the web schemes
    if parsed.scheme not in ["http", "https"]:
        # If it has a different scheme (e.g. ftp, file) and it's what we got, we might want to error or handle it.
        # For now, if it has *a* scheme, assume it's intentional if not http/https.
        # However, for web crawling, we really only want http/https. If it's a file scheme, we might want to treat it differently.
        # This part might need refinement based on how strictly we want to enforce http/https
        if parsed.scheme == 'file':
            return url_string # Allow file URIs if explicitly given
        # If it's some other scheme, it's probably an error for web crawling context
        # Forcing it to https might be wrong. Let's assume if a scheme is there, it was intended.
        # OR, more strictly: if scheme is not http/https, prepend https if netloc looks like a domain.
        if parsed.netloc: # If there's a domain part, it's likely a web URL with a wrong scheme
            return ParseResult(scheme='https', netloc=parsed.netloc, path=parsed.path, params=parsed.params, query=parsed.query, fragment=parsed.fragment).geturl()
    return url_string

def configure_gemini(api_key, model_name='gemini-1.5-flash-latest'):
    global gemini_model
    if not api_key:
        print("Warning: No Gemini API key provided. Q&A generation will be skipped.")
        gemini_model = None
        return False
    try:
        genai.configure(api_key=api_key)
        print(f"Attempting to configure Gemini with model: {model_name}...")
        gemini_model = genai.GenerativeModel(model_name) 
        print(f"Gemini API configured successfully with {model_name}.")
        return True
    except Exception as e:
        print(f"Error configuring Gemini API with {model_name}: {e}")
        gemini_model = None
        # Fallback can be removed if model is selectable, or kept as a simpler internal fallback
        # For now, let's remove the explicit fallback here, as the GUI will offer choices.
        return False

# --- Helper Functions ---

def get_base_url(url):
    # Ensure scheme before parsing for base URL
    url_with_scheme = ensure_scheme(url)
    parsed_url = urlparse(url_with_scheme)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def fetch_page(url, progress_callback=None):
    log_func = progress_callback or print
    processed_url = ensure_scheme(url)
    log_func(f"Fetching {processed_url}...")
    try:
        response = requests.get(processed_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text, response.url
    except requests.exceptions.RequestException as e:
        log_func(f"Error fetching {processed_url}: {e}")
        return None, None

def process_with_gemini(text_content, source_url, progress_callback=None, max_chars=28000):
    global gemini_model
    log_func = progress_callback or print

    if not text_content:
        return None

    if not gemini_model:
        log_func("Warning: Gemini model not configured. Skipping Q&A generation.")
        return None
    
    truncated_text_content = text_content[:max_chars]

    if not truncated_text_content.strip():
        log_func(f"Warning: Extracted text for {source_url} is empty or only whitespace. Skipping Gemini.")
        return None

    prompt = f"""
Read the following text carefully. It was extracted from the webpage {source_url}

BEGIN TEXT CONTENT:
{truncated_text_content}
END TEXT CONTENT.

Based *only* on the information present in the TEXT CONTENT provided above, generate a relevant question about its main topic and provide a concise answer.
Your output MUST be a single, valid JSON object with exactly two keys: "question" and "answer".
Do not include any explanations, introductory text, or any characters outside of this single JSON object.

Example of the required JSON Output format:
```json
{{
  "question": "What is the main theme of the provided text?",
  "answer": "The main theme is X, Y, and Z based on the text."
}}
```

JSON Output:
"""
    max_retries = 3
    raw_response_text = "" 
    qa_pair = {} 

    for attempt in range(max_retries):
        try:
            log_func(f"Sending content from {source_url} to Gemini (attempt {attempt + 1})...")
            response = gemini_model.generate_content(prompt)
            raw_response_text = response.text
            
            json_start_index = raw_response_text.find('{')
            json_end_index = raw_response_text.rfind('}') + 1
            
            if json_start_index != -1 and json_end_index != -1 and json_start_index < json_end_index:
                json_string = raw_response_text[json_start_index:json_end_index]
                qa_pair = json.loads(json_string)
                if isinstance(qa_pair, dict) and 'question' in qa_pair and 'answer' in qa_pair:
                    return {"context": truncated_text_content, "question": qa_pair["question"], "answer": qa_pair["answer"]}
                else:
                    log_func(f"Error: Gemini response for {source_url} did not contain valid Q&A keys. Response: {json_string}")
            else:
                log_func(f"Error: Could not extract JSON from Gemini response for {source_url}. Response: {raw_response_text}")

        except json.JSONDecodeError as e:
            log_func(f"Error decoding JSON from Gemini for {source_url} (attempt {attempt + 1}): {e}. Response: {raw_response_text}")
        except Exception as e:
            log_func(f"Error interacting with Gemini API for {source_url} (attempt {attempt + 1}): {e}")
        
        # Using the parameter request_delay_seconds for retries as well, if available, or a default
        # This requires request_delay_seconds to be passed down or accessed globally/defaulted here
        # For simplicity, let's keep REQUEST_DELAY for retries for now, or it needs more wiring.
        current_request_delay = REQUEST_DELAY # Defaulting, this could be a parameter too.
        if attempt < max_retries - 1:
            time.sleep(current_request_delay * (attempt + 1))
        else:
            log_func(f"Failed to process content from {source_url} with Gemini after {max_retries} attempts.")
            return None 
    return None 

def run_web_to_json_conversion(start_url_from_user, num_pages, output_file, api_key_to_use, progress_callback,
                               model_name_to_use='gemini-1.5-flash-latest', 
                               request_delay_seconds=2, 
                               max_chars_for_gemini=28000):
    log_func = progress_callback or print
    
    start_url = ensure_scheme(start_url_from_user)
    if urlparse(start_url).scheme not in ["http", "https"]:
        log_func(f"Invalid starting URL scheme for {start_url_from_user}. Must be http or https. Aborting.")
        return [] 

    if not configure_gemini(api_key_to_use, model_name_to_use):
        log_func("Gemini API key not configured or invalid. Proceeding without Q&A generation.")

    log_func(f"Starting crawl from: {start_url}")
    log_func(f"Max pages to retrieve: {num_pages}")
    log_func(f"Using Gemini model: {model_name_to_use}")
    log_func(f"Request delay: {request_delay_seconds}s")
    log_func(f"Max chars for Gemini: {max_chars_for_gemini}")

    base_url = get_base_url(start_url)

    pages_to_visit = [start_url]
    visited_urls = set()
    collected_data = []

    while pages_to_visit and len(collected_data) < num_pages:
        current_url_from_queue = pages_to_visit.pop(0)
        current_url = ensure_scheme(current_url_from_queue)

        if current_url in visited_urls:
            continue

        html_content, final_url_after_redirect = fetch_page(current_url, log_func)
        actual_url_processed = ensure_scheme(final_url_after_redirect or current_url) 
        
        visited_urls.add(current_url) 
        if final_url_after_redirect and final_url_after_redirect != current_url:
            visited_urls.add(actual_url_processed) 

        if not html_content:
            time.sleep(request_delay_seconds) # Use configured delay
            continue

        extracted_text = trafilatura.extract(html_content)

        if extracted_text:
            log_func(f"Successfully extracted content from {actual_url_processed}")
            gemini_output = process_with_gemini(extracted_text, actual_url_processed, log_func, max_chars_for_gemini)
            if gemini_output:
                collected_data.append(gemini_output)
            else:
                collected_data.append({
                    "context": extracted_text[:max_chars_for_gemini],
                    "question": "N/A (Gemini processing failed or skipped)", 
                    "answer": "N/A (Gemini processing failed or skipped)"
                })
        else:
            log_func(f"Could not extract main content from {actual_url_processed}")

        if len(collected_data) >= num_pages:
            break

        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            page_base_url_for_links = actual_url_processed 
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_link_unprocessed = urljoin(page_base_url_for_links, href)
                absolute_link = ensure_scheme(absolute_link_unprocessed)
                parsed_link = urlparse(absolute_link)
                
                if parsed_link.scheme in ['http', 'https'] and \
                   get_base_url(absolute_link) == base_url and \
                   parsed_link.path and not parsed_link.path.endswith(('.pdf', '.jpg', '.png', '.css', '.js')) and \
                   '#' not in absolute_link: 
                    if absolute_link not in visited_urls and absolute_link not in pages_to_visit:
                        pages_to_visit.append(absolute_link)
        
        log_func(f"Collected {len(collected_data)}/{num_pages} pages. URLs in queue: {len(pages_to_visit)}")
        time.sleep(request_delay_seconds) # Use configured delay

    # Save the data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(collected_data, f, indent=4, ensure_ascii=False)
        log_func(f"Successfully saved data to {output_file}")
    except IOError as e:
        log_func(f"Error saving data to {output_file}: {e}")

    # TODO: Implement the rest of the agent logic
    # 1. Link Discovery & Selection (Loop) - Partially done
    # 2. Web Page Fetching & Content Extraction (Inside Loop) - Partially done
    # 3. JSON Transformation (using Gemini or other methods) (Inside Loop) - Placeholder added
    # 4. Save Output - Done

    return collected_data # Return the data for potential use in GUI (e.g. display summary)

# --- Main Agent Logic (for command-line usage) ---
def main_cli():
    parser = argparse.ArgumentParser(description="Web Content to LLM Fine-tuning JSON Agent - CLI")
    parser.add_argument("start_url", help="The starting URL to crawl.")
    parser.add_argument("-n", "--num_pages", type=int, default=DEFAULT_MAX_PAGES, 
                        help=f"Maximum number of pages to crawl (default: {DEFAULT_MAX_PAGES}).")
    parser.add_argument("-o", "--output_file", default="fine_tuning_data.json", 
                        help="Path to save the output JSON file (default: fine_tuning_data.json).")
    parser.add_argument("--api_key", help="Gemini API Key. If not provided, will try to use GENAI_API_KEY environment variable.", default=None)
    
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GENAI_API_KEY")

    def cli_progress_callback(message):
        print(message)

    run_web_to_json_conversion(args.start_url, args.num_pages, args.output_file, api_key, cli_progress_callback)

if __name__ == "__main__":
    main_cli() 