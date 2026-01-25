#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIDocGenius 功能演示
快速展示所有核心功能
"""
import sys
import io
from pathlib import Path

# Windows UTF-8 输出支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from AIDocGenius import DocProcessor

def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def demo_summary():
    """演示摘要功能"""
    print_section("1. 智能文档摘要")
    
    # 创建测试文档
    content = """
    人工智能（AI）正在改变我们的世界。从智能手机到自动驾驶汽车，
    AI技术已经渗透到日常生活的方方面面。机器学习算法可以识别图像、
    理解语音、翻译语言，甚至创作艺术作品。深度学习的突破使得计算机
    能够完成以前只有人类才能完成的复杂任务。随着技术的不断进步，
    AI将在医疗、教育、交通等领域发挥更大的作用。
    """
    
    test_file = Path("demo_doc.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    processor = DocProcessor()
    
    print("\n原文长度:", len(content), "字符")
    print("\n生成摘要（100字以内）:")
    print("-" * 70)
    summary = processor.generate_summary(test_file, max_length=100)
    print(summary)
    
    test_file.unlink()

def demo_analysis():
    """演示分析功能"""
    print_section("2. 文档质量分析")
    
    content = """
    Python 是一种高级编程语言。它易于学习和使用。
    
    Python 支持多种编程范式。包括面向对象、函数式和过程式编程。
    
    Python 有丰富的标准库。这使得开发效率大大提高。
    Python 社区非常活跃。有大量的第三方库可供使用。
    """
    
    test_file = Path("demo_doc.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    processor = DocProcessor()
    analysis = processor.analyze(test_file)
    
    print("\n可读性分析:")
    print(f"  评分: {analysis['readability']['score']:.1f}/100")
    print(f"  建议: {analysis['readability']['suggestion']}")
    
    print("\n文档统计:")
    stats = analysis['statistics']
    print(f"  字数: {stats['word_count']}")
    print(f"  句数: {stats['sentence_count']}")
    print(f"  段落: {stats['paragraph_count']}")
    
    print("\n关键词 (前5个):")
    for i, kw in enumerate(analysis['keywords'][:5], 1):
        print(f"  {i}. {kw['word']} ({kw['frequency']}次)")
    
    test_file.unlink()

def demo_conversion():
    """演示格式转换功能"""
    print_section("3. 文档格式转换")
    
    content = """# Python 编程指南

## 简介
Python 是一种易于学习的编程语言。

## 特点
- 简洁易读
- 功能强大
- 社区活跃
"""
    
    md_file = Path("demo.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    processor = DocProcessor()
    
    print("\n支持的转换格式:")
    formats = ["txt", "html", "docx", "json"]
    converted_files = []
    
    for fmt in formats:
        output = md_file.with_suffix(f".{fmt}")
        try:
            processor.convert(md_file, output)
            print(f"  ✓ Markdown → {fmt.upper():5} : {output.name}")
            converted_files.append(output)
        except Exception as e:
            print(f"  ✗ {fmt.upper():5} : {str(e)}")
    
    # 清理
    md_file.unlink()
    for f in converted_files:
        if f.exists():
            f.unlink()

def demo_translation():
    """演示翻译功能"""
    print_section("4. 多语言翻译")
    
    print("\n注意: 翻译功能需要网络连接")
    print("-" * 70)
    
    content = "人工智能正在改变世界。技术创新推动社会进步。"
    
    test_file = Path("demo_doc.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    processor = DocProcessor()
    
    print(f"\n原文（中文）: {content}")
    
    try:
        translation = processor.translate(
            test_file,
            target_language="en",
            source_language="zh"
        )
        print(f"翻译（英文）: {translation}")
        print("\n✓ 翻译成功!")
    except Exception as e:
        print(f"\n✗ 翻译失败: {str(e)}")
        print("  提示: 请检查网络连接")
    
    test_file.unlink()

def demo_supported_formats():
    """显示支持的格式"""
    print_section("支持的文档格式")
    
    print("\n输入格式:")
    print("  📄 TXT  - 纯文本")
    print("  📝 MD   - Markdown")
    print("  📑 DOCX - Microsoft Word")
    print("  📋 PDF  - PDF文档")
    print("  🔤 JSON - JSON数据")
    print("  📊 YAML - YAML配置")
    
    print("\n输出格式:")
    print("  📄 TXT  - 纯文本")
    print("  📝 MD   - Markdown")
    print("  🌐 HTML - 网页")
    print("  📑 DOCX - Microsoft Word")
    print("  🔤 JSON - JSON数据")
    print("  📊 YAML - YAML配置")

def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("  AIDocGenius - 智能文档处理助手")
    print("  功能演示")
    print("=" * 70)
    
    try:
        # 演示各个功能
        demo_summary()
        demo_analysis()
        demo_conversion()
        demo_translation()
        demo_supported_formats()
        
        # 总结
        print_section("演示完成")
        print("\n✓ 所有核心功能演示完成！")
        print("\n下一步:")
        print("  1. 运行 '启动服务.bat' 使用 Web 界面")
        print("  2. 查看 'examples/' 目录了解更多用法")
        print("  3. 阅读 'QUICKSTART.md' 快速上手指南")
        print("  4. 参考 '使用说明.md' 详细文档")
        
    except Exception as e:
        print(f"\n✗ 演示过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
