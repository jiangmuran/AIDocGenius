# 贡献指南

感谢您考虑为AIDocGenius项目做出贡献！我们欢迎任何形式的贡献，包括但不限于：

- 代码贡献
- 文档改进
- Bug报告
- 功能建议
- 测试用例

## 开发环境设置

1. Fork项目到您的GitHub账户

2. 克隆项目到本地：
```bash
git clone https://github.com/YOUR_USERNAME/AIDocGenius.git
cd AIDocGenius
```

3. 安装开发依赖：
```bash
pip install -e ".[dev]"
```

4. 创建新分支：
```bash
git checkout -b feature/your-feature-name
```

## 代码风格

我们使用以下工具来保持代码质量：

- black：代码格式化
- isort：导入语句排序
- flake8：代码风格检查

在提交代码之前，请运行：

```bash
black .
isort .
flake8
```

## 提交Pull Request

1. 确保您的代码符合我们的代码风格要求
2. 更新测试用例并确保所有测试通过
3. 更新相关文档
4. 提交代码时使用清晰的提交信息
5. 创建Pull Request并描述您的更改

## 提交Bug报告

如果您发现了bug，请创建一个Issue并包含以下信息：

- 问题的详细描述
- 复现步骤
- 期望的行为
- 实际的行为
- 环境信息（操作系统、Python版本等）
- 相关的日志输出

## 功能建议

如果您有新功能的建议，请创建一个Issue并：

- 清晰地描述新功能
- 解释为什么这个功能是有用的
- 提供可能的实现方案
- 考虑向后兼容性

## 文档贡献

文档改进对项目非常重要。如果您发现文档中的问题或想添加新内容：

1. 找到相关的文档文件
2. 进行必要的更改
3. 提交Pull Request

## 测试

- 添加新功能时，请包含相应的测试用例
- 确保所有测试都能通过：
```bash
pytest
```

## 发布流程

1. 更新版本号（遵循语义化版本）
2. 更新CHANGELOG.md
3. 创建新的发布标签
4. 发布到PyPI

## 行为准则

请保持专业和友善。我们希望维护一个开放和包容的社区。

## 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

## 联系方式

如果您有任何问题，请通过以下方式联系我们：

- GitHub Issues
- 电子邮件：[jmr@jiangmuran.com]

再次感谢您的贡献！ 