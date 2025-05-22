#!/usr/bin/env python3
"""
Setup script for AI Agent - Web Content to LLM JSON Converter
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "AI Agent - Web Content to LLM JSON Converter"

# Read requirements from requirements.txt
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "requests",
            "beautifulsoup4", 
            "trafilatura",
            "google-generativeai",
            "robotexclusionrulesparser",
            "urllib3"
        ]

setup(
    name="ai-web-agent",
    version="2.0.0",
    author="Saqlain Abbas, AleenaTahir1",
    author_email="saqlainrazee@gmail.com",
    description="An intelligent web crawling and content extraction tool that transforms web content into structured JSON data suitable for fine-tuning Large Language Models (LLMs).",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/razee4315/AI-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov", 
            "black",
            "flake8",
            "mypy",
        ],
        "gui": [
            "tkinter",  # Usually comes with Python
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-web-agent=web_to_json_agent:main_cli",
            "ai-web-gui=gui_agent:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/razee4315/AI-agent/issues",
        "Source": "https://github.com/razee4315/AI-agent",
        "Documentation": "https://github.com/razee4315/AI-agent#readme",
    },
    keywords="ai, web-scraping, llm, fine-tuning, gemini, content-extraction, json, machine-learning",
    include_package_data=True,
    zip_safe=False,
) 