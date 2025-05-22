# Contributing to AI Agent - Web Content to LLM JSON Converter

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Google Gemini API key for testing
- Basic understanding of web scraping and AI concepts

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/razee4315/AI-agent.git
   cd AI-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export GENAI_API_KEY="your_gemini_api_key_here"
   ```

## 🔄 Development Workflow

### Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Test the GUI application
   python gui_agent.py
   
   # Test the CLI
   python web_to_json_agent.py "https://example.com" -n 2
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

## 📝 Code Style Guidelines

### Python Conventions

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example Code Structure

```python
def extract_content(url: str, timeout: int = 10) -> tuple[str, str]:
    """
    Extract content from a given URL.
    
    Args:
        url: The URL to extract content from
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (extracted_text, final_url)
        
    Raises:
        requests.RequestException: If the request fails
    """
    # Implementation here
    pass
```

### GUI Development

- Use consistent padding and spacing
- Follow the existing theme and style
- Add progress indicators for long operations
- Handle errors gracefully with user-friendly messages

## 🐛 Bug Reports

Create an issue with:

- **Clear title**: Brief description of the bug
- **Environment**: OS, Python version, dependencies
- **Steps to reproduce**: Detailed steps to trigger the bug
- **Expected behavior**: What should have happened
- **Actual behavior**: What actually happened
- **Logs/Screenshots**: Any relevant error messages or screenshots

### Bug Report Template

```markdown
**Environment:**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- Package Versions: [run `pip freeze`]

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior:**
A clear description of what you expected to happen.

**Actual Behavior:**
A clear description of what actually happened.

**Additional Context:**
Add any other context about the problem here.
```

## 💡 Feature Requests

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Provide context** about why this feature would be useful
3. **Describe the solution** you'd like to see
4. **Consider alternatives** you've thought about

## 🔧 Technical Contributions

### Areas for Contribution

- **Core Functionality**
  - Improve content extraction accuracy
  - Add support for more AI models
  - Enhance crawling efficiency

- **User Interface**
  - Improve GUI design and usability
  - Add new configuration options
  - Create web-based interface

- **Documentation**
  - Improve code documentation
  - Add usage examples
  - Create video tutorials

- **Testing**
  - Add unit tests
  - Create integration tests
  - Improve error handling

### Code Review Process

1. All submissions require review from project maintainers
2. We may suggest changes, improvements, or alternatives
3. Once approved, maintainers will merge the PR
4. Changes should not break existing functionality

## 📚 Documentation

When contributing, please:

- Update README.md if you change functionality
- Add docstrings to new functions
- Update inline comments for complex logic
- Create examples for new features

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## 👥 Community

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a positive environment

### Getting Help

- Create an issue for bugs or feature requests
- Email the maintainers for private concerns
- Join discussions in existing issues

## 🎯 Priority Areas

We're currently looking for help with:

1. **Testing**: More comprehensive test coverage
2. **Performance**: Optimizing large-scale crawling
3. **UI/UX**: Improving the user interface
4. **Documentation**: Better examples and tutorials
5. **Multi-language**: Supporting non-English content

## 📞 Contact

**Maintainers:**
- Saqlain Abbas ([@razee4315](https://github.com/razee4315)) - saqlainrazee@gmail.com
- AleenaTahir1 ([@AleenaTahir1](https://github.com/AleenaTahir1)) - aleenatahirf23@nutech.edu.pk

---

**Thank you for contributing! 🙏** 