# AIDocGenius (智能文档助手)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

AIDocGenius 是一个强大的智能文档处理助手，它能够帮助用户高效地处理、分析和转换各种文档。

## ✨ 主要功能

- 📝 智能文档摘要生成
- 🌐 多语言文档翻译
- 📊 文档内容分析
- 🔄 多格式文档转换
- 📋 文本提取与处理
- 🎯 关键信息识别

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Docker (可选，用于容器化部署)

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 使用方式

#### 1. Python API

```python
from aidocgenius import DocProcessor

processor = DocProcessor()
result = processor.process_document("path/to/your/document")
```

#### 2. 命令行工具

```bash
python -m aidocgenius process --input document.pdf --output summary.txt
```

#### 3. Web API

启动 Web 服务：
```bash
python app.py
```

访问 http://localhost:5000 使用 Web 界面。

## 📖 详细文档

- [使用说明](docs/usage.md)
- [开发文档](docs/development.md)
- [部署指南](docs/deployment.md)

## 🐳 Docker 部署

使用 Docker 运行：

```bash
docker-compose up -d
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📫 联系方式

- 邮箱：jmr@jiangmuran.com
- GitHub：[@jiangmuran](https://github.com/jiangmuran)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 