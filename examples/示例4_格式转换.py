#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例4：文档格式转换
演示如何使用 AIDocGenius 进行文档格式转换
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from AIDocGenius import DocProcessor

def main():
    """文档格式转换示例"""
    print("=" * 60)
    print("示例4：文档格式转换")
    print("=" * 60)
    
    # 创建处理器实例
    processor = DocProcessor()
    
    # 创建 Markdown 示例文档
    markdown_content = """# Python 快速入门指南

## 简介

Python 是一种易于学习、功能强大的编程语言。

## 基础语法

### 变量和数据类型

Python 支持多种数据类型：
- 整数 (int)
- 浮点数 (float)
- 字符串 (str)
- 列表 (list)
- 字典 (dict)

### 控制流

使用 if、for、while 等关键字控制程序流程。

## 总结

Python 是初学者和专业开发者的理想选择。
"""
    
    # 保存 Markdown 文件
    md_file = Path("guide.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"\n✓ 创建 Markdown 文件: {md_file}")
    
    # 转换为不同格式
    conversions = [
        ("txt", "纯文本"),
        ("html", "HTML"),
        ("docx", "Word 文档"),
        ("json", "JSON")
    ]
    
    print("\n正在进行格式转换...")
    print("-" * 60)
    
    converted_files = []
    
    for ext, name in conversions:
        output_file = md_file.with_suffix(f".{ext}")
        try:
            processor.convert(md_file, output_file)
            print(f"✓ {name:12} → {output_file}")
            converted_files.append(output_file)
        except Exception as e:
            print(f"✗ {name:12} → 转换失败: {str(e)}")
    
    # 显示转换后的文件内容示例
    print("\n" + "-" * 60)
    print("查看转换结果示例 (TXT):")
    print("-" * 60)
    
    txt_file = md_file.with_suffix(".txt")
    if txt_file.exists():
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()
            print(content[:200] + "..." if len(content) > 200 else content)
    
    # 显示 HTML 示例
    print("\n" + "-" * 60)
    print("查看转换结果示例 (HTML 开头部分):")
    print("-" * 60)
    
    html_file = md_file.with_suffix(".html")
    if html_file.exists():
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
            print(content[:300] + "..." if len(content) > 300 else content)
    
    # 清理所有文件
    print("\n" + "-" * 60)
    print("清理生成的文件...")
    md_file.unlink()
    for file in converted_files:
        if file.exists():
            file.unlink()
    
    print("\n" + "=" * 60)
    print("✓ 示例完成！")
    print("支持的转换格式: TXT, Markdown, HTML, DOCX, JSON, YAML")
    print("=" * 60)

if __name__ == "__main__":
    main()
