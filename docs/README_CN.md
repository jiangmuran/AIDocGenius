# AIDocGenius - 智能文档处理助手

[English](../README.md) | 简体中文

> 一个功能完整、开箱即用的智能文档处理工具

**AIDocGenius** 是一个 Python 文档处理工具，提供摘要、翻译、分析与格式转换能力，适用于学术写作、内容生产和文档管理场景。

## 核心功能

### 已验证功能

- 文档摘要（默认轻量摘要，可选小模型摘要）
- 多语言翻译（优先 Google Translate，部分语言对模型回退）
- 文档质量分析（可读性、关键词、结构分析）
- 多格式转换（TXT、MD、HTML、DOCX、JSON、YAML）
- 批量处理与报告输出
- Web 界面（拖拽上传）

### 新增功能（v1.1.0）

- 文档对比（相似度与差异）
- 文档合并（支持去重）
- 完整测试套件（50+ 单测）

### 支持格式

| 输入格式 | 输出格式 |
|--------------|----------------|
| TXT、Markdown、Word (DOCX) | TXT、Markdown、HTML |
| PDF、JSON、YAML | Word (DOCX)、JSON、YAML |

### 性能说明

- 启动时间取决于环境与依赖
- 轻量摘要速度快，模型摘要取决于硬件
- 分析与转换随文本长度变化
- 翻译依赖网络与引擎可用性

## 快速演示

运行示例：

```bash
python demo.py
```

演示包含摘要、分析、格式转换、翻译与格式检查。

## 快速开始

### 系统要求

- Python 3.8+
- 网络连接（翻译与可选模型下载）

### 可选依赖

- `transformers` + `torch`: 小模型摘要（首次使用自动下载）
- `PyPDF2`: PDF 文本提取
- `pyyaml`: YAML 读写
- `markdown`: 更高质量 Markdown → HTML

### 一行命令开箱即用

```bash
pip install -r requirements.txt && python app.py
```

访问 http://localhost:8000

### 快速安装（3 步）

#### Windows 用户

1. 安装依赖
   ```
   双击 "安装依赖.bat"
   ```
2. 启动服务
   ```
   双击 "启动服务.bat"
   ```
3. 访问界面
   ```
   打开 http://localhost:8000
   ```

#### 其他系统

```bash
# 1. 克隆项目
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python app.py
```

### 使用方式

#### 方式一：Web 界面

```bash
# Windows: 双击 "启动服务.bat"
# 其他系统:
python app.py
```

浏览器访问 http://localhost:8000

#### 方式二：Python API

```python
from AIDocGenius import DocProcessor

processor = DocProcessor()

# 摘要
summary = processor.generate_summary("document.txt", max_length=200)

# 翻译
translation = processor.translate("doc.txt", target_language="en")

# 分析
analysis = processor.analyze("doc.txt")

# 转换
processor.convert("input.md", "output.html")
```

#### 方式三：运行示例

```bash
python demo.py
python examples/示例1_文档摘要.py
python examples/示例2_文档翻译.py
python examples/示例3_文档分析.py
```

#### 方式四：CLI

```bash
python -m AIDocGenius.cli summary "document.txt" --max-length 200
python -m AIDocGenius.cli analyze "document.txt" --output analysis.json
python -m AIDocGenius.cli convert "README.md" "README.html"
```

#### 方式五：REST API

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

## 测试

```bash
python test_basic.py
```

## 使用示例

### 1. 文档摘要

```python
from AIDocGenius import DocProcessor

processor = DocProcessor()

short = processor.generate_summary("article.txt", max_length=100)
print(short)

detailed = processor.generate_summary("article.txt", max_length=500)
print(detailed)
```

小模型摘要（可选，需安装 `transformers` 与 `torch`）：

```python
processor = DocProcessor(config={
    "summarizer": {
        "use_small_model": True,
        "model_name": "google/flan-t5-small"
    }
})

summary = processor.generate_summary("article.txt", max_length=200)
```

### 2. 文档翻译

```python
translation = processor.translate(
    "chinese_doc.txt",
    target_language="en",
    source_language="zh"
)
print(translation)
```

### 3. 文档分析

```python
analysis = processor.analyze("document.txt")

print(f"可读性: {analysis['readability']['score']}/100")
print(f"字数: {analysis['statistics']['word_count']}")
print(f"关键词: {analysis['keywords'][:5]}")
```

### 4. 格式转换

```python
processor.convert("README.md", "README.html")
processor.convert("article.txt", "article.docx")
```

### 5. 批量处理

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

批量输出文件：

- `*.summary.txt`
- `*.translated.<lang>.txt`
- `*.analysis.json`
- `*.<output_format>`（convert）
- `batch_report.json`、`batch_report.md`

### 6. 文档对比

```python
comparison = processor.compare_documents("doc1.txt", "doc2.txt")

print(f"相似度: {comparison['similarity']:.2%}")
print(f"字数差异: {comparison['statistics']['length_diff']}")
print(f"差异数量: {len(comparison['differences'])}")
```

### 7. 文档合并

```python
processor.merge_documents(
    ["intro.md", "chapter1.md", "chapter2.md"],
    "book.md"
)

processor.merge_documents(
    ["doc1.txt", "doc2.txt", "doc3.txt"],
    "merged.txt",
    smart_merge=True
)
```

## 技术栈

### 后端

- Python 3.8+
- FastAPI
- Uvicorn
- python-docx
- PyPDF2
- NLTK
- googletrans

### 前端

- HTML5 + CSS3
- JavaScript (ES6+)
- Bootstrap 5

## 文档

- [快速上手指南](../QUICKSTART.md)
- [完整使用说明](../使用说明.md)
- [贡献指南](../CONTRIBUTING.md)
- [示例代码](../examples/)
- [更新日志](../CHANGELOG.md)

### API 参考

<details>
<summary>核心 API 方法</summary>

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

## 适用场景

### 学术写作

- 快速生成摘要
- 可读性分析
- 外文资料翻译

### 内容生产

- 长文重点提取
- 多语言内容发布
- 批量格式转换

### 文档管理

- 批量文档处理
- 关键信息提取
- 质量评估

### 学习与研究

- NLP 技术学习
- Python 项目实践
- 文档处理学习

## 迭代计划

### v1.0.0（已发布）

- 核心文档处理功能
- Web 界面
- REST API
- 批量处理
- 文档完善

### v1.1.0（当前）

- 文档对比
- 文档合并（去重）
- 完整测试套件
- 错误处理优化

### v1.2.0（计划）

- API 返回结构与错误码统一
- 批处理报告增强（json/csv/md）与 zip 输出
- 模型缓存目录与预热命令
- CLI 批处理/报告/导出增强
- API 与 CLI 测试补充

### v2.0.0（未来）

- AI 内容生成
- 多文档分析
- 可视化增强
- 插件系统

## 常见问题

Q: 翻译无法使用？

A: 翻译需要网络连接，请确认网络正常且 Google Translate 可访问。

Q: 如何提升摘要质量？

A: 调整 `max_length`，保持文档结构清晰，或使用小模型摘要。

Q: 是否支持 PDF？

A: 支持。直接传入 PDF 路径即可。

Q: 是否支持离线？

A: 摘要/分析/转换支持离线，翻译需要网络。

Q: 是否可用于商用？

A: 可以。项目采用 MIT License。

## Docker 部署

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 配置说明

创建 `config.yaml`：

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

## 相关链接

- [完整文档](../QUICKSTART.md)
- [示例代码](../examples/)
- [问题反馈](https://github.com/jiangmuran/AIDocGenius/issues)
- [功能建议](https://github.com/jiangmuran/AIDocGenius/discussions)

## 联系方式

- 邮箱: jmr@jiangmuran.com
- GitHub: [@jiangmuran](https://github.com/jiangmuran)

## 致谢

- FastAPI
- NLTK
- Google Translate
- Bootstrap

## 许可证

项目采用 MIT License，详情见 [LICENSE](../LICENSE)。
