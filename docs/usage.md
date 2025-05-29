# AIDocGenius 使用指南

## 安装

### 使用pip安装

```bash
pip install aidocgenius
```

### 从源代码安装

```bash
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius
pip install -e .
```

## 使用方式

### 1. Web界面

AIDocGenius提供了一个直观的Web界面，是最简单的使用方式：

1. 启动Web服务器：
```bash
python -m aidocgenius.api
```

2. 打开浏览器访问：`http://localhost:8000`

3. 使用方法：
   - 拖放文件或点击上传区域选择文件
   - 选择要执行的操作（摘要、翻译、分析或转换）
   - 根据需要设置其他选项（如目标语言、输出格式）
   - 点击"处理文档"按钮
   - 查看处理结果

### 2. 命令行工具

如果您喜欢使用命令行，可以使用以下命令：

```bash
# 生成文档摘要
aidocgenius summarize input.md

# 翻译文档
aidocgenius translate input.md -t en

# 分析文档
aidocgenius analyze input.md

# 转换文档格式
aidocgenius convert input.md -o output.docx
```

### 3. Python API

对于开发者，我们提供了完整的Python API：

```python
from aidocgenius import DocProcessor

# 初始化处理器
processor = DocProcessor()

# 生成摘要
summary = processor.generate_summary("document.md")

# 翻译文档
translation = processor.translate("document.md", target_language="en")

# 分析文档
analysis = processor.analyze("document.md")

# 转换格式
processor.convert("document.md", "output.docx")
```

### 4. REST API

如果您需要在其他应用中集成AIDocGenius，可以使用REST API：

- 启动API服务器：
```bash
python -m aidocgenius.api
```

API端点：
- POST `/summarize`: 生成文档摘要
- POST `/translate`: 翻译文档
- POST `/analyze`: 分析文档
- POST `/convert`: 转换文档格式
- GET `/supported-formats`: 获取支持的格式
- GET `/supported-languages`: 获取支持的语言

API文档：访问 `http://localhost:8000/docs` 查看完整的API文档。

## 高级功能

### 1. 批量处理

```python
processor = DocProcessor()
results = processor.batch_process(
    input_dir="documents/",
    output_dir="processed/",
    operations=["summarize", "translate", "analyze"]
)
```

### 2. 自定义选项

```python
# 自定义摘要长度
summary = processor.generate_summary(
    "document.md",
    max_length=150,
    min_length=50
)

# 指定源语言和目标语言
translation = processor.translate(
    "document.md",
    target_language="en",
    source_language="zh"
)

# 自定义分析标准
analysis = processor.analyze(
    "document.md",
    criteria=["readability", "structure", "keywords"]
)
```

## 支持的格式

- Markdown (.md)
- 纯文本 (.txt)
- Word文档 (.docx)
- PDF文件 (.pdf)
- HTML (.html)
- JSON (.json)
- YAML (.yaml, .yml)

## 支持的语言

- 中文 (zh)
- 英语 (en)
- 日语 (ja)
- 韩语 (ko)
- 法语 (fr)
- 德语 (de)
- 西班牙语 (es)
- 意大利语 (it)
- 俄语 (ru)
- 阿拉伯语 (ar)

## 最佳实践

1. **文档预处理**
   - 确保文档编码为UTF-8
   - 移除不必要的格式和样式
   - 保持文档结构清晰

2. **性能优化**
   - 对大文件使用批处理
   - 适当设置摘要长度
   - 合理使用缓存

3. **错误处理**
   - 总是进行异常处理
   - 检查输入文件的有效性
   - 验证语言代码和格式支持

## 常见问题

1. **安装问题**
   Q: 安装时报错 `torch not found`
   A: 先安装PyTorch: `pip install torch`

2. **使用问题**
   Q: 如何处理大文件？
   A: 使用批处理功能，设置适当的块大小

3. **性能问题**
   Q: 处理速度慢？
   A: 考虑使用GPU加速，减小处理块大小

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](../LICENSE) 文件。 