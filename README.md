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
- 网络连接（用于翻译功能）

### 快速安装（3 步）

#### Windows 用户

1. **安装依赖**
   ```
   双击运行 "安装依赖.bat"
   ```

2. **启动服务**
   ```
   双击运行 "启动服务.bat"
   ```

3. **访问界面**
   ```
   浏览器打开 http://localhost:8000
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

### 三种使用方式

#### 方式一：Web 界面（最简单）

```bash
# Windows: 双击 "启动服务.bat"
# 其他系统:
python app.py
```

访问 http://localhost:8000，即可使用图形界面！

#### 方式二：Python API（最灵活）

```python
from AIDocGenius import DocProcessor

processor = DocProcessor()

# 生成摘要
summary = processor.generate_summary("document.txt", max_length=200)

# 翻译文档
translation = processor.translate("doc.txt", target_language="en")

# 分析文档
analysis = processor.analyze("doc.txt")

# 格式转换
processor.convert("input.md", "output.html")
```

#### 方式三：运行示例（学习推荐）

```bash
# 运行综合演示
python demo.py

# 运行具体示例
python examples/示例1_文档摘要.py
python examples/示例2_文档翻译.py
python examples/示例3_文档分析.py
```

## 📖 详细文档

- [使用说明](docs/usage.md)
- [开发文档](docs/development.md)
- [部署指南](docs/deployment.md)

## 🐳 Docker 部署

使用 Docker 运行：

```bash
docker-compose up -d
```

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=jiangmuran/AIDocGenius&type=Date)](https://star-history.com/#jiangmuran/AIDocGenius&Date)

## 👥 贡献者

感谢所有为这个项目做出贡献的开发者！

<a href="https://github.com/jiangmuran/AIDocGenius/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=jiangmuran/AIDocGenius" />
</a>

### 主要贡献者

- [@jiangmuran](https://github.com/jiangmuran) - 项目创建者和维护者
- 期待您的贡献！

## 🏆 贡献排行榜

| 贡献者 | 提交次数 | 贡献类型 |
|--------|----------|----------|
| [@jiangmuran](https://github.com/jiangmuran) | - | 核心功能开发 |

## 🤝 贡献指南

我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告问题和建议
- 📝 改进文档
- ✨ 添加新功能
- 🔨 修复 bug
- 💡 提供想法和建议

如何贡献：

1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📫 联系方式

- 邮箱：jmr@jiangmuran.com
- GitHub：[@jiangmuran](https://github.com/jiangmuran)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 