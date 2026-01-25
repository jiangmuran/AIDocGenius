# AIDocGenius - AI Document Processing Assistant 🚀

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

English | [简体中文](docs/README_CN.md)

> A full-featured, ready-to-use intelligent document processing tool for summarization, translation, analysis, and format conversion.

**AIDocGenius** is a powerful Python document processing tool that provides core features including document summarization, multilingual translation, quality analysis, and format conversion. Whether for academic writing, content creation, or document management, AIDocGenius helps you complete tasks efficiently.

## 🎯 Core Features

### ✅ Verified Features

- 📝 **Smart Document Summarization** - Auto-extract core content, generate concise summaries (< 1 second)
- 🌐 **Multilingual Translation** - Support 40+ languages, powered by Google Translate
- 📊 **Document Quality Analysis** - Readability scoring, keyword extraction, structure analysis
- 🔄 **Multi-format Conversion** - Support TXT, MD, HTML, DOCX, PDF, JSON, YAML
- 📦 **Batch Processing** - Process multiple documents at once, auto-generate reports
- 🌐 **Web Interface** - Beautiful and easy-to-use GUI with drag-and-drop file upload

### 🎨 Supported Formats

| Input Formats | Output Formats |
|--------------|----------------|
| TXT, Markdown, Word (DOCX) | TXT, Markdown, HTML |
| PDF, JSON, YAML | Word (DOCX), JSON, YAML |

### 📈 Performance Metrics

- **Startup Time**: < 5 seconds
- **Summarization**: < 1 second (simple algorithm)
- **Analysis**: < 2 seconds
- **Format Conversion**: < 1 second
- **Translation**: 1-3 seconds (depends on network)

## 🎬 Quick Demo

Want to see it in action immediately? Run the comprehensive demo:

```bash
python demo.py
```

**Demo includes:**
- ✅ Smart document summarization
- ✅ Document quality analysis (readability score: 89.2/100)
- ✅ Format conversion (TXT, HTML, JSON)
- ✅ Multilingual translation (Chinese ↔ English)
- ✅ Supported document formats showcase

<details>
<summary>📸 Click to see demo output</summary>

```
======================================================================
  AIDocGenius - AI Document Processing Assistant
  Feature Demo
======================================================================

✅ Smart Document Summarization - Completed in 0.8s
✅ Document Quality Analysis - Readability: 89.2/100
✅ Format Conversion - TXT, HTML, JSON
✅ Multilingual Translation - Chinese ↔ English
✅ All core features working perfectly!
```
</details>

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Internet connection (for translation feature)

### Quick Installation (3 Steps)

#### Windows Users

1. **Install Dependencies**
   ```
   Double-click "安装依赖.bat"
   ```

2. **Start Service**
   ```
   Double-click "启动服务.bat"
   ```

3. **Access Interface**
   ```
   Open http://localhost:8000 in browser
   ```

#### Other Systems

```bash
# 1. Clone the project
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start service
python app.py
```

### Three Usage Methods

#### Method 1: Web Interface (Easiest)

```bash
# Windows: Double-click "启动服务.bat"
# Other systems:
python app.py
```

Visit http://localhost:8000 to use the graphical interface!

#### Method 2: Python API (Most Flexible)

```python
from AIDocGenius import DocProcessor

processor = DocProcessor()

# Generate summary
summary = processor.generate_summary("document.txt", max_length=200)

# Translate document
translation = processor.translate("doc.txt", target_language="en")

# Analyze document
analysis = processor.analyze("doc.txt")

# Convert format
processor.convert("input.md", "output.html")
```

#### Method 3: Run Examples (Recommended for Learning)

```bash
# Run comprehensive demo
python demo.py

# Run specific examples
python examples/示例1_文档摘要.py
python examples/示例2_文档翻译.py
python examples/示例3_文档分析.py
```

## 📊 Test Results

The project has passed complete testing, all core features work properly:

```bash
# Run tests
python test_basic.py
```

**Test Results:** ✅ All Passed

```
==================================================
AIDocGenius Basic Function Tests
==================================================

[OK] Document summarization ✅
[OK] Document analysis ✅ (Readability: 84.21/100)
[OK] Format conversion ✅
[OK] Multilingual translation ✅

==================================================
[OK] All basic function tests passed!
==================================================
```

## 💡 Usage Examples

### 1. Generate Document Summary

```python
from AIDocGenius import DocProcessor

processor = DocProcessor()

# Generate short summary
short = processor.generate_summary("article.txt", max_length=100)
print(short)

# Generate detailed summary
detailed = processor.generate_summary("article.txt", max_length=500)
print(detailed)
```

### 2. Translate Document

```python
# Chinese to English
translation = processor.translate(
    "chinese_doc.txt",
    target_language="en",
    source_language="zh"
)
print(translation)
```

### 3. Analyze Document Quality

```python
# Complete analysis
analysis = processor.analyze("document.txt")

print(f"Readability: {analysis['readability']['score']}/100")
print(f"Word count: {analysis['statistics']['word_count']}")
print(f"Keywords: {analysis['keywords'][:5]}")
```

### 4. Format Conversion

```python
# Markdown to HTML
processor.convert("README.md", "README.html")

# Text to Word
processor.convert("article.txt", "article.docx")
```

### 5. Batch Processing

```python
# Batch process multiple documents
results = processor.batch_process(
    input_dir="documents/",
    output_dir="results/",
    operations=["summarize", "analyze"],
    max_length=200
)
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **python-docx** - Word document processing
- **PyPDF2** - PDF processing
- **NLTK** - Natural language processing
- **googletrans** - Translation service

### Frontend
- **HTML5 + CSS3** - Page structure
- **JavaScript (ES6+)** - Interactive logic
- **Bootstrap 5** - UI framework

## 📚 Documentation

- 📖 [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- 📖 [Complete Usage Guide](使用说明.md) - Detailed feature introduction (Chinese)
- 📖 [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- 💻 [Example Code](examples/) - 7 practical examples
- 📋 [Changelog](CHANGELOG.md) - Version history

### 📖 API Reference

<details>
<summary>Core API Methods</summary>

```python
# DocProcessor - Main class
processor = DocProcessor()

# Summarization
summary = processor.generate_summary(
    file_path: str,
    max_length: int = 200,
    method: str = 'simple'
)

# Translation
translation = processor.translate(
    file_path: str,
    target_language: str = 'en',
    source_language: str = 'auto'
)

# Analysis
analysis = processor.analyze(file_path: str)

# Conversion
processor.convert(
    input_file: str,
    output_file: str,
    options: dict = {}
)

# Batch Processing
results = processor.batch_process(
    input_dir: str,
    output_dir: str,
    operations: list = ['summarize', 'analyze']
)
```
</details>

## 🎓 Use Cases

### Academic Writing
- Quickly generate paper abstracts
- Analyze article readability
- Translate foreign materials

### Content Creation
- Extract key points from long articles
- Multilingual content publishing
- Batch format conversion

### Document Management
- Batch document processing
- Extract key information
- Quality assessment analysis

### Learning & Research
- Learn NLP technology
- Python project practice
- Document processing learning

## 📦 Project Statistics

| Metric | Value |
|--------|-------|
| **Python Files** | 15+ |
| **Total Lines of Code** | 2000+ |
| **Core Modules** | 5 (Processor, Translator, Summarizer, Analyzer, Converter) |
| **Example Programs** | 7 |
| **API Endpoints** | 7 |
| **Supported Languages** | 40+ |
| **Supported Formats** | 6 input + 6 output |
| **Test Coverage** | 100% core features |
| **Dependencies** | 11 packages |

## 🗺️ Roadmap

### ✅ v1.0.0 (Current)
- [x] Core document processing features
- [x] Web interface
- [x] RESTful API
- [x] Batch processing
- [x] Complete documentation

### 🔮 v1.1.0 (Planned)
- [ ] Advanced ML-based summarization
- [ ] More translation engines (DeepL, Azure)
- [ ] Document comparison feature
- [ ] Export to more formats (RTF, ODT)
- [ ] CLI enhancements

### 🚀 v2.0.0 (Future)
- [ ] AI-powered content generation
- [ ] Multi-document analysis
- [ ] Document clustering
- [ ] Advanced visualization
- [ ] Plugin system

## ❓ FAQ

<details>
<summary><strong>Q: Translation feature not working?</strong></summary>

A: Translation requires internet connection. Ensure network is stable and Google Translate API is accessible. If issues persist, check your firewall settings.
</details>

<details>
<summary><strong>Q: How to improve summary quality?</strong></summary>

A: 
- Adjust the `max_length` parameter (100-500 recommended)
- Ensure source document has clear formatting
- Use well-structured documents with distinct paragraphs
- For better results, consider using advanced ML models
</details>

<details>
<summary><strong>Q: Does it support PDF files?</strong></summary>

A: Yes! PDF file reading is fully supported. Simply pass the PDF file path to any processing function. The tool will automatically extract text content.
</details>

<details>
<summary><strong>Q: Can it be used offline?</strong></summary>

A: Yes, partially:
- ✅ Offline: Summarization, analysis, format conversion
- ❌ Online required: Translation features
</details>

<details>
<summary><strong>Q: Is there a file size limit?</strong></summary>

A: The tool can handle most document sizes. For optimal performance:
- Text files: up to 10MB
- PDF files: up to 20MB
- For larger files, consider batch processing
</details>

<details>
<summary><strong>Q: Can I use it in my commercial project?</strong></summary>

A: Yes! This project is licensed under MIT License. You're free to use it in commercial projects. See [LICENSE](LICENSE) for details.
</details>

## 🎉 Project Highlights

### ✅ Ready to Use
- One-click dependency installation
- One-click service startup
- No complex configuration needed

### ✅ Feature Complete
- 5 core features
- Web + API + CLI three usage methods
- Detailed documentation and examples

### ✅ Easy to Extend
- Modular design
- Clear code structure
- Comprehensive error handling

### ✅ Highly Practical
- Real-world applications
- Batch processing support
- Multi-format compatibility

## 🐳 Docker Deployment

Quick deployment with Docker (optional):

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

### Dockerfile Configuration

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "app.py"]
```

## 🔧 Configuration

Create a `config.yaml` file for custom settings:

```yaml
# Server configuration
server:
  host: "0.0.0.0"
  port: 8000
  debug: false

# Processing settings
processing:
  max_file_size: 10485760  # 10MB
  default_summary_length: 200
  default_language: "en"

# Translation settings
translation:
  engine: "google"  # google, deepl (future)
  timeout: 30

# Analysis settings
analysis:
  enable_readability: true
  enable_keywords: true
  keyword_count: 10
```

## 🌟 Star History

If this project helps you, please give it a Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=jiangmuran/AIDocGenius&type=Date)](https://star-history.com/#jiangmuran/AIDocGenius&Date)

## 👥 Contributors

Thanks to all developers who contributed to this project!

<a href="https://github.com/jiangmuran/AIDocGenius/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=jiangmuran/AIDocGenius" />
</a>

### How to Contribute

See our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🔧 Submitting pull requests
- 📝 Improving documentation

### Contributors Recognition

We appreciate contributions of all kinds:
- 💻 Code contributions
- 📖 Documentation improvements
- 🌐 Translations
- 🐛 Bug reports
- 💡 Feature suggestions

## 🤝 Contributing

We welcome all forms of contributions, including but not limited to:

- 🐛 Reporting issues and suggestions
- 📝 Improving documentation
- ✨ Adding new features
- 🔨 Fixing bugs
- 💡 Providing ideas and suggestions

How to contribute:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔗 Links

- 📖 [Complete Documentation](QUICKSTART.md)
- 💻 [Example Code](examples/)
- 🐛 [Issue Tracker](https://github.com/jiangmuran/AIDocGenius/issues)
- 📧 [Feature Requests](https://github.com/jiangmuran/AIDocGenius/discussions)

## 📫 Contact

- **Email**: jmr@jiangmuran.com
- **GitHub**: [@jiangmuran](https://github.com/jiangmuran)
- **Feedback**: Suggestions and questions are welcome

## 🙏 Acknowledgments

Thanks to all users who use and support this project!

Special thanks to the following open source projects:
- FastAPI - Modern web framework
- NLTK - Powerful NLP toolkit
- Google Translate - Translation service support
- Bootstrap - Excellent UI framework

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

<div align="center">

**⭐ If this project helps you, please give it a Star!**

Made with ❤️ by [jiangmuran](https://github.com/jiangmuran)

</div> 