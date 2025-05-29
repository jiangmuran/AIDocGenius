# AIDocGenius 开发文档

## 项目架构

### 核心模块

```
aidocgenius/
├── __init__.py
├── processor.py      # 主处理器
├── translator.py     # 翻译模块
├── summarizer.py     # 摘要生成器
├── converter.py      # 格式转换器
├── analyzer.py       # 文档分析器
├── utils.py         # 工具函数
├── api.py           # Web API
└── cli.py           # 命令行接口
```

### 前端结构

```
aidocgenius/static/
├── index.html       # 主页面
├── css/            # 样式文件
└── js/
    └── main.js     # 前端逻辑
```

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装开发依赖：
```bash
pip install -e ".[dev]"
```

## 代码规范

### Python代码规范

- 使用 Python 类型注解
- 遵循 PEP 8 规范
- 使用 black 进行代码格式化
- 使用 isort 管理导入顺序
- 使用 flake8 进行代码检查

### 文档规范

- 所有公共函数和类必须有文档字符串
- 使用中文编写用户文档
- 使用英文编写代码注释
- 保持文档的及时更新

## API文档

### 核心类

#### DocProcessor

主要处理器类，整合所有文档处理功能。

```python
class DocProcessor:
    def __init__(self, model_name: str = "bert-base-chinese", device: str = "cuda"):
        """初始化文档处理器"""
        
    def generate_summary(self, document_path: str, max_length: int = None) -> str:
        """生成文档摘要"""
        
    def translate(self, document_path: str, target_language: str) -> str:
        """翻译文档"""
        
    def analyze(self, document_path: str) -> dict:
        """分析文档"""
        
    def convert(self, input_path: str, output_path: str) -> None:
        """转换文档格式"""
```

### REST API

#### 文档摘要

```http
POST /summarize
Content-Type: multipart/form-data

file: <文件>
max_length: <最大长度>
min_length: <最小长度>
```

响应：
```json
{
    "summary": "生成的摘要内容"
}
```

#### 文档翻译

```http
POST /translate
Content-Type: multipart/form-data

file: <文件>
target_language: "en"
source_language: "zh"
```

响应：
```json
{
    "translation": "翻译后的内容"
}
```

#### 文档分析

```http
POST /analyze
Content-Type: multipart/form-data

file: <文件>
```

响应：
```json
{
    "readability": {
        "score": 85.5,
        "suggestion": "文档可读性很好"
    },
    "structure": {
        "paragraph_count": 10,
        "sentence_count": 45
    },
    "keywords": [
        {"word": "人工智能", "frequency": 5},
        {"word": "机器学习", "frequency": 3}
    ]
}
```

#### 格式转换

```http
POST /convert
Content-Type: multipart/form-data

file: <文件>
output_format: "pdf"
```

响应：
```json
{
    "converted_content": "转换后的内容"
}
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_processor.py

# 生成覆盖率报告
pytest --cov=aidocgenius
```

### 编写测试

- 使用 pytest 框架
- 每个模块都应有对应的测试文件
- 使用 fixtures 共享测试资源
- 保持测试简单、独立

## 发布流程

1. 更新版本号：
   - 在 `setup.py` 中更新版本号
   - 遵循语义化版本规范

2. 更新更新日志：
   - 在 `CHANGELOG.md` 中添加新版本信息
   - 记录所有重要更改

3. 创建发布分支：
```bash
git checkout -b release/v0.1.x
```

4. 运行测试：
```bash
pytest
```

5. 构建分发包：
```bash
python setup.py sdist bdist_wheel
```

6. 上传到PyPI：
```bash
twine upload dist/*
```

## 故障排除

### 常见问题

1. 模型加载失败
```python
# 检查CUDA是否可用
import torch
print(torch.cuda.is_available())

# 检查模型文件是否存在
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
```

2. 内存不足
```python
# 使用生成器处理大文件
def process_large_file(file_path):
    with open(file_path) as f:
        for chunk in f:
            yield process_chunk(chunk)
```

### 性能优化

1. 批处理
```python
# 使用批处理提高性能
def batch_process(items, batch_size=32):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        process_batch(batch)
```

2. 缓存
```python
# 使用缓存避免重复计算
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(input_data):
    return process(input_data)
```

## 安全考虑

1. 文件上传
- 限制文件大小
- 验证文件类型
- 使用安全的临时文件处理

2. API访问
- 实施速率限制
- 添加认证机制
- 验证输入数据

3. 错误处理
- 不暴露敏感信息
- 记录错误日志
- 优雅降级

## 部署

### Docker部署

1. 构建镜像：
```bash
docker build -t aidocgenius .
```

2. 运行容器：
```bash
docker run -p 8000:8000 aidocgenius
```

### 服务器部署

1. 使用Gunicorn：
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker aidocgenius.api:app
```

2. 使用Nginx配置：
```nginx
server {
    listen 80;
    server_name aidocgenius.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 维护和监控

1. 日志管理
- 使用结构化日志
- 实施日志轮转
- 监控错误率

2. 性能监控
- 监控API响应时间
- 跟踪资源使用
- 设置告警阈值

3. 备份策略
- 定期备份数据
- 测试恢复流程
- 维护版本历史 