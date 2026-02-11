# AIDocGenius - 智能文档处理助手 🚀

[English](../README.md) | 简体中文

> 一个功能完整、开箱即用的智能文档处理工具

## 📖 中文文档

### 快速开始
- [快速上手指南](../QUICKSTART.md) - 5分钟快速开始
- [完整使用说明](../使用说明.md) - 详细功能介绍

### 项目文档
- [项目改进说明](../项目改进说明.md) - 改进记录
- [完成清单](../完成清单.md) - 功能验证清单

### 示例代码
查看 [examples](../examples/) 目录获取 7 个实用示例：
1. 示例1_文档摘要.py - 文档摘要生成
2. 示例2_文档翻译.py - 多语言翻译
3. 示例3_文档分析.py - 文档质量分析
4. 示例4_格式转换.py - 格式转换
5. 示例5_批量处理.py - 批量处理

## 🎯 核心功能

- 📝 智能文档摘要 - 默认使用轻量摘要算法
- 🌐 多语言翻译 - 支持 40+ 种语言
- 📊 文档质量分析 - 可读性评分、关键词提取
- 🔄 多格式转换 - TXT, MD, HTML, DOCX, JSON, YAML
- 📦 批量处理 - 自动生成报告

## 🚀 快速开始

### Windows 用户

1. 双击运行 `安装依赖.bat`
2. 双击运行 `启动服务.bat`
3. 浏览器打开 http://localhost:8000

### 其他系统

```bash
pip install -r requirements.txt
python app.py
```

### 使用小模型摘要（可选，需要安装 transformers 和 torch）

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

## 📞 联系方式

- 邮箱：jmr@jiangmuran.com
- GitHub：[@jiangmuran](https://github.com/jiangmuran)
