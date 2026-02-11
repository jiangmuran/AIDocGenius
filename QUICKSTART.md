# AIDocGenius 快速上手指南

欢迎使用 AIDocGenius！这份指南将帮助你在 5 分钟内开始使用。

## 系统要求

- Python 3.8 或更高版本
- Windows / macOS / Linux 操作系统
- 网络连接（用于翻译功能与可选模型下载）

## 可选依赖

- `transformers` + `torch`: 小模型摘要（首次使用会自动下载模型）
- `PyPDF2`: PDF 文本提取
- `pyyaml`: YAML 读写
- `markdown`: 更高质量的 Markdown → HTML

## 快速安装

### 一行命令开箱即用

```bash
pip install -r requirements.txt && python app.py
```

访问 http://localhost:8000

### 方法一：使用安装脚本（推荐 - Windows）

双击运行 `安装依赖.bat`，脚本会自动安装所有依赖包。

### 方法二：手动安装

```bash
# 1. 进入项目目录
cd AIDocGenius

# 2. 安装依赖包
pip install -r requirements.txt
```

## 立即开始

### 方式一：运行示例程序

我们提供了 5 个实用示例，帮助你快速了解功能：

```bash
# 文档摘要生成
python examples/示例1_文档摘要.py

# 文档翻译
python examples/示例2_文档翻译.py

# 文档分析
python examples/示例3_文档分析.py

# 格式转换
python examples/示例4_格式转换.py

# 批量处理
python examples/示例5_批量处理.py
```

### 方式二：启动 Web 界面

**Windows 用户：** 双击 `启动服务.bat`

**其他系统：**
```bash
python app.py
```

然后在浏览器访问：http://localhost:8000

### 方式三：Python 代码调用

```python
from AIDocGenius import DocProcessor

# 创建处理器
processor = DocProcessor()

# 生成文档摘要
summary = processor.generate_summary("your_document.txt", max_length=200)
print(summary)

# 翻译文档
translation = processor.translate(
    "your_document.txt",
    target_language="en",
    source_language="zh"
)
print(translation)

# 分析文档
analysis = processor.analyze("your_document.txt")
print(analysis)

# 格式转换
processor.convert("input.txt", "output.docx")
```

### 方式四：CLI（脚本友好）

```bash
# 生成摘要
python -m AIDocGenius.cli summary "your_document.txt" --max-length 200

# 分析文档
python -m AIDocGenius.cli analyze "your_document.txt" --output analysis.json

# 格式转换
python -m AIDocGenius.cli convert "README.md" "README.html"

# 预热小模型
python -m AIDocGenius.cli model warmup --model-name "google/flan-t5-small"

# 仅输出报告
python -m AIDocGenius.cli batch "input" "output" --operations summarize,analyze --report --report-only
```

### 方式五：REST API

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

JSON 端点统一返回 `status/data/error/request_id` 结构。

`/batch` 配合 `zip_output=false` 会直接返回报告结构。

使用 `report_prefix` 可以避免覆盖已有报告文件。

`/batch` 支持 `zip_output=true` 下载压缩包，`report=true` 生成报告文件。

## 主要功能

### 1. 智能摘要生成

自动提取文档核心内容，生成简洁摘要：

```python
processor = DocProcessor()
summary = processor.generate_summary(
    "long_article.txt",
    max_length=150  # 控制摘要长度
)
```

小模型摘要（可选，需要安装 `transformers` 与 `torch`）：

```python
processor = DocProcessor(config={
    "summarizer": {
        "use_small_model": True,
        "model_name": "google/flan-t5-small"
    }
})
summary = processor.generate_summary("long_article.txt", max_length=150)
```

### 2. 多语言翻译

支持中英日韩等多种语言互译：

```python
# 中译英
translation = processor.translate(
    "chinese_doc.txt",
    target_language="en",
    source_language="zh"
)

# 英译中
translation = processor.translate(
    "english_doc.txt",
    target_language="zh",
    source_language="en"
)
```

支持的语言（Google Translate 可用时）：
- 中文 (zh)
- 英语 (en)
- 日语 (ja)
- 韩语 (ko)
- 法语 (fr)
- 德语 (de)
- 西班牙语 (es)
- 等 40+ 种语言

### 3. 文档分析

全面分析文档质量和结构：

```python
analysis = processor.analyze("document.txt")

# 查看可读性评分
print(f"可读性: {analysis['readability']['score']}/100")

# 查看文档统计
print(f"字数: {analysis['statistics']['word_count']}")

# 查看关键词
for keyword in analysis['keywords']:
    print(f"{keyword['word']}: {keyword['frequency']} 次")
```

### 4. 格式转换

轻松转换文档格式：

```python
# Markdown 转 Word
processor.convert("readme.md", "readme.docx")

# 文本转 HTML
processor.convert("article.txt", "article.html")

# Markdown 转 JSON
processor.convert("data.md", "data.json")
```

支持格式：TXT、Markdown、HTML、DOCX、JSON、YAML

### 5. 批量处理

一次处理多个文档：

```python
results = processor.batch_process(
    input_dir="documents/",
    output_dir="results/",
    operations=["summarize", "analyze"],
    max_length=200
)
```

## 支持的文档格式

### 输入格式
- 纯文本 (.txt)
- Markdown (.md)
- Word 文档 (.docx)
- PDF (.pdf)
- JSON (.json)
- YAML (.yaml, .yml)

提示：PDF/YAML 需要对应依赖可用（`PyPDF2`/`pyyaml`）。

### 输出格式
- TXT
- Markdown
- HTML
- Word (DOCX)
- JSON
- YAML

## 快速测试

运行内置测试验证安装：

**Windows：** 双击 `运行测试.bat`

**其他系统：**
```bash
python test_basic.py
```

测试通过会显示：
```
==================================================
[OK] 所有基本功能测试通过！
==================================================
```

## 实用技巧

### 处理长文档

对于长文档，可以控制摘要长度：

```python
# 短摘要（100字）
short = processor.generate_summary("long.txt", max_length=100)

# 中摘要（300字）
medium = processor.generate_summary("long.txt", max_length=300)

# 长摘要（500字）
long = processor.generate_summary("long.txt", max_length=500)
```

### 批量翻译文件

```python
import os
from pathlib import Path

processor = DocProcessor()
input_dir = Path("chinese_docs")
output_dir = Path("english_docs")
output_dir.mkdir(exist_ok=True)

for file in input_dir.glob("*.txt"):
    translation = processor.translate(
        file,
        target_language="en",
        source_language="zh"
    )
    output_file = output_dir / file.name
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(translation)
```

### 生成文档报告

```python
import json

# 分析文档
analysis = processor.analyze("report.txt")

# 保存为 JSON 报告
with open("analysis_report.json", "w", encoding="utf-8") as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)
```

## 常见问题

### Q: 翻译功能无法使用？

A: 翻译功能需要网络连接。请确保：
1. 网络连接正常
2. 防火墙未阻止 Python 访问网络
3. 如仍有问题，可能是 Google Translate API 访问受限

### Q: 如何提高摘要质量？

A: 可以尝试：
1. 调整 `max_length` 参数，使摘要长度适中
2. 确保原文档格式清晰，有明确的段落划分
3. 对于技术文档，保留关键术语的原文

### Q: 支持 PDF 文件吗？

A: 是的！AIDocGenius 支持读取 PDF 文件。使用方式与其他格式相同：

```python
processor.generate_summary("document.pdf")
```

## 相关资源

- 📖 [完整使用说明](使用说明.md)
- 💻 [GitHub 仓库](https://github.com/jiangmuran/AIDocGenius)
- 📧 [联系我们](mailto:jmr@jiangmuran.com)

## 下一步

1. ✅ 尝试运行示例程序
2. ✅ 使用你自己的文档进行测试
3. ✅ 访问 Web 界面体验可视化操作
4. ✅ 查看 `examples/` 目录了解更多用法

祝你使用愉快！如有问题，欢迎反馈。
