# AI Agent - Web Content to LLM JSON Converter

An intelligent web crawling and content extraction tool that transforms web content into structured JSON data suitable for fine-tuning Large Language Models (LLMs). This project combines web scraping capabilities with Google's Gemini AI to automatically generate question-answer pairs from crawled content.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 🚀 Features

- **Intelligent Web Crawling**: Automatically discovers and crawls web pages from a starting URL
- **Content Extraction**: Uses advanced content extraction techniques to get clean, readable text
- **AI-Powered Q&A Generation**: Leverages Google Gemini AI to create contextual question-answer pairs
- **Modern GUI Interface**: User-friendly tkinter-based graphical interface
- **CLI Support**: Command-line interface for automation and scripting
- **Configurable Settings**: Customizable crawling parameters, delays, and AI model selection
- **JSON Output**: Generates structured JSON data perfect for LLM fine-tuning
- **Robots.txt Compliance**: Respects website crawling policies
- **Real-time Progress Tracking**: Monitor crawling progress with detailed logs

## 📋 Requirements

- Python 3.7 or higher
- Google Gemini API key
- Internet connection for web crawling and AI processing

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/razee4315/AI-agent.git
   cd AI-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API Key:**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - You can either:
     - Set it as an environment variable: `export GENAI_API_KEY="your_api_key_here"`
     - Enter it directly in the GUI
     - Pass it as a command-line argument

## 🖥️ Usage

### GUI Application (Recommended)

Run the modern graphical interface:

```bash
python gui_agent.py
```

**GUI Features:**
- **Step 1**: Enter and verify your Gemini API key
- **Step 2**: Configure crawling settings (start URL, number of pages)
- **Advanced Settings**: Customize AI model, request delays, and character limits
- **Real-time Progress**: Monitor crawling and processing in the log area
- **Save Results**: Export generated data to JSON files

### Command Line Interface

For automation and scripting:

```bash
python web_to_json_agent.py "https://example.com" -n 5 -o output.json --api_key "your_api_key"
```

**CLI Parameters:**
- `start_url`: The starting URL to crawl (required)
- `-n, --num_pages`: Maximum number of pages to crawl (default: 10)
- `-o, --output_file`: Output JSON file path (default: fine_tuning_data.json)
- `--api_key`: Gemini API key (optional if set as environment variable)

## 📊 Output Format

The tool generates JSON data in the following format:

```json
[
  {
    "context": "Extracted content from the webpage...",
    "question": "What is the main topic discussed in this content?",
    "answer": "The main topic is about..."
  },
  {
    "context": "Another piece of extracted content...",
    "question": "How does this relate to the previous topic?",
    "answer": "This relates to the previous topic by..."
  }
]
```

## ⚙️ Configuration Options

### Advanced Settings

- **Gemini Model**: Choose from available models (gemini-1.5-flash-latest, gemini-1.5-pro-latest, etc.)
- **Request Delay**: Configure delay between requests (0.5-60 seconds)
- **Max Characters**: Set character limit for AI processing (1000-100000)
- **Number of Pages**: Control crawling depth (1-1000 pages)

### Custom Headers

The tool uses respectful crawling practices with appropriate user agents and follows robots.txt guidelines.

## 🧠 AI Integration

This project utilizes Google's Gemini AI for intelligent content processing:

- **Context Understanding**: AI analyzes extracted content to understand main themes
- **Question Generation**: Creates relevant, contextual questions about the content
- **Answer Synthesis**: Provides concise, accurate answers based on the source material
- **JSON Formatting**: Ensures output is properly structured for LLM training

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your Gemini API key is valid and has appropriate permissions
2. **Network Issues**: Check internet connection and firewall settings
3. **Content Extraction Failures**: Some websites may block crawling or have complex structures
4. **Memory Issues**: For large crawls, consider processing in smaller batches

### Debug Tips

- Check the progress log for detailed error messages
- Verify the starting URL is accessible
- Ensure sufficient disk space for output files
- Monitor rate limits with request delays

## 🎯 Use Cases

- **LLM Fine-tuning**: Generate training data for language models
- **Content Analysis**: Extract and analyze website content at scale
- **Knowledge Base Creation**: Build Q&A datasets from web sources
- **Research Automation**: Automate content gathering for research projects
- **Educational Resources**: Create study materials from educational websites

## 🤝 Contributors

### Development Team

**Developer:** Saqlain Abbas  
- GitHub: [@razee4315](https://github.com/razee4315)  
- Email: saqlainrazee@gmail.com

**Developer:** AleenaTahir1  
- GitHub: [@AleenaTahir1](https://github.com/AleenaTahir1)  
- Email: aleenatahirf23@nutech.edu.pk

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google for providing the Gemini AI API
- The open-source community for the excellent libraries used in this project

---

**Happy Crawling! 🕷️🤖** 
