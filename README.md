# AIDocGenius - AI Document Processing Assistant

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

English | [简体中文](docs/README_CN.md)

> A full-featured, ready-to-use intelligent document processing tool for summarization, translation, analysis, and format conversion.

**AIDocGenius** is a Python document processing tool that provides summarization, multilingual translation, quality analysis, and format conversion. It targets academic writing, content creation, and document management workflows.

## Core Features

### Verified Features

- Smart document summarization (simple mode by default, optional small-model summaries)
- Multilingual translation (Google Translate when available, model fallback for limited pairs)
- Document quality analysis (readability scoring, keyword extraction, structure analysis)
- Multi-format conversion (TXT, MD, HTML, DOCX, JSON, YAML)
- Batch processing with report output
- Web interface with drag-and-drop upload

### New Features (v1.1.0)

- Document comparison (similarity and differences)
- Document merging with smart duplicate removal
- Complete test suite (50+ unit tests)

### Supported Formats

| Input Formats | Output Formats |
|--------------|----------------|
| TXT, Markdown, Word (DOCX) | TXT, Markdown, HTML |
| PDF, JSON, YAML | Word (DOCX), JSON, YAML |

### Performance Notes

- Startup time depends on environment and dependencies
- Summarization is fast in simple mode; model mode depends on hardware
- Analysis depends on document length and language
- Format conversion is fast for text-based formats
- Translation depends on network and engine availability

## Quick Demo

Run the demo:

```bash
python demo.py
```

Demo includes summarization, analysis, conversion, translation, and format checks.

## Quick Start

### Requirements

- Python 3.8+
- Internet connection (for translation feature and optional model download)

### Optional Dependencies

- `transformers` + `torch`: small-model summarization (downloads on first use)
- `PyPDF2`: PDF text extraction
- `pyyaml`: YAML read/write
- `markdown`: higher-quality Markdown → HTML (fallback renderer available)

### One-liner (pip + app.py)

```bash
pip install -r requirements.txt && python app.py
```

Visit http://localhost:8000

### Quick Installation (3 Steps)

#### Windows Users

1. Install Dependencies
   ```
   Double-click "安装依赖.bat"
   ```
2. Start Service
   ```
   Double-click "启动服务.bat"
   ```
3. Access Interface
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

### Usage Methods

#### Method 1: Web Interface

```bash
# Windows: Double-click "启动服务.bat"
# Other systems:
python app.py
```

Visit http://localhost:8000 to use the graphical interface.

#### Method 2: Python API

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

#### Method 3: Run Examples

```bash
# Run comprehensive demo
python demo.py

# Run specific examples
python examples/示例1_文档摘要.py
python examples/示例2_文档翻译.py
python examples/示例3_文档分析.py
```

#### Method 4: CLI

```bash
# Summarize
python -m AIDocGenius.cli summary "document.txt" --max-length 200

# Analyze
python -m AIDocGenius.cli analyze "document.txt" --output analysis.json

# Convert
python -m AIDocGenius.cli convert "README.md" "README.html"

# Warm up small model
python -m AIDocGenius.cli model warmup --model-name "google/flan-t5-small"
```

#### Method 5: REST API

```
POST /summarize
POST /translate
POST /analyze
POST /convert
POST /compare
POST /merge
POST /batch
GET  /health
```

### API Response Schema

All JSON endpoints return:

```json
{
  "status": "ok",
  "data": {},
  "error": null,
  "request_id": "uuid"
}
```

## Test Results

```bash
python test_basic.py
```

## Usage Examples

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

Small downloadable model (optional, requires `transformers` and `torch`):

```python
from AIDocGenius import DocProcessor

processor = DocProcessor(config={
    "summarizer": {
        "use_small_model": True,
        "model_name": "google/flan-t5-small"
    }
})

summary = processor.generate_summary("article.txt", max_length=200)
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
results = processor.batch_process(
    input_dir="documents/",
    output_dir="results/",
    operations=["summarize", "analyze"],
    max_length=200,
    report=True,
    report_formats=["json", "md"]
)
```

Batch processing writes outputs into `output_dir` with standardized filenames:

- `*.summary.txt`
- `*.translated.<lang>.txt`
- `*.analysis.json`
- `*.<output_format>` (for convert)
- `batch_report.json`, `batch_report.md`, `batch_report.csv`

### 6. Compare Documents

```python
comparison = processor.compare_documents("doc1.txt", "doc2.txt")

print(f"Similarity: {comparison['similarity']:.2%}")
print(f"Word count difference: {comparison['statistics']['length_diff']}")
print(f"Number of differences: {len(comparison['differences'])}")
```

### 7. Merge Documents

```python
# Standard merge
processor.merge_documents(
    ["intro.md", "chapter1.md", "chapter2.md"],
    "book.md"
)

# Smart merge (remove duplicates)
processor.merge_documents(
    ["doc1.txt", "doc2.txt", "doc3.txt"],
    "merged.txt",
    smart_merge=True
)
```

## Tech Stack

### Backend

- Python 3.8+
- FastAPI
- Uvicorn
- python-docx
- PyPDF2
- NLTK
- googletrans

### Frontend

- HTML5 + CSS3
- JavaScript (ES6+)
- Bootstrap 5

## Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Complete Usage Guide](使用说明.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Example Code](examples/)
- [Changelog](CHANGELOG.md)

### API Reference

<details>
<summary>Core API Methods</summary>

```python
from AIDocGenius import DocProcessor

processor = DocProcessor()

summary = processor.generate_summary(
    document_path: str,
    max_length: int = 200,
    min_length: int = None,
    ratio: float = None
)

translation = processor.translate(
    document_path: str,
    target_language: str,
    source_language: str = None
)

analysis = processor.analyze(document_path: str)

processor.convert(
    input_path: str,
    output_path: str,
    format_options: dict = None
)

results = processor.batch_process(
    input_dir: str,
    output_dir: str,
    operations: list,
    report: bool = False,
    report_formats: list = None
)
```
</details>

## Use Cases

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

## Roadmap

### v1.0.0 (Released)

- Core document processing features
- Web interface
- REST API
- Batch processing
- Documentation

### v1.1.0 (Current)

- Document comparison
- Document merging with smart deduplication
- Comprehensive test suite
- Improved error handling

### v1.2.0 (Planned)

- Unified API response schema and error codes
- Batch report enhancements (json/csv/md) and zip outputs
- Model cache directory and warmup command
- CLI enhancements for batch/report/export
- Additional API and CLI tests

### v2.0.0 (Future)

- AI-powered content generation
- Multi-document analysis
- Advanced visualization
- Plugin system

## FAQ

Q: Translation feature not working?

A: Translation requires internet connection. Ensure network is stable and Google Translate API is accessible. If issues persist, check firewall settings.

Q: How to improve summary quality?

A: Adjust `max_length`, ensure clear formatting, and consider using small-model summaries.

Q: Does it support PDF files?

A: Yes. Pass the PDF file path to any processing function. The tool will extract text content.

Q: Can it be used offline?

A: Summarization, analysis, and conversion work offline. Translation requires network access.

Q: Can I use it in commercial projects?

A: Yes. This project is licensed under MIT License.

## Docker Deployment

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## Configuration

Create a `config.yaml` file for custom settings:

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false

processing:
  max_file_size: 10485760
  default_summary_length: 200
  default_language: "en"

translation:
  engine: "google"
  timeout: 30

analysis:
  enable_readability: true
  enable_keywords: true
  keyword_count: 10
```

Environment variables:

- `MODEL_CACHE_DIR`: HuggingFace model cache directory

## Links

- [Complete Documentation](QUICKSTART.md)
- [Example Code](examples/)
- [Issue Tracker](https://github.com/jiangmuran/AIDocGenius/issues)
- [Feature Requests](https://github.com/jiangmuran/AIDocGenius/discussions)

## Contact

- Email: jmr@jiangmuran.com
- GitHub: [@jiangmuran](https://github.com/jiangmuran)

## Acknowledgments

- FastAPI
- NLTK
- Google Translate
- Bootstrap

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
