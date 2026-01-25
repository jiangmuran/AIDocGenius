#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例3：文档分析
演示如何使用 AIDocGenius 分析文档质量和结构
"""
import sys
from pathlib import Path
import json
sys.path.insert(0, str(Path(__file__).parent.parent))

from AIDocGenius import DocProcessor

def main():
    """文档分析示例"""
    print("=" * 60)
    print("示例3：文档分析")
    print("=" * 60)
    
    # 创建处理器实例
    processor = DocProcessor()
    
    # 创建示例文档
    sample_text = """
    # Python 编程最佳实践
    
    Python 是一种高级编程语言，以其简洁和可读性而闻名。
    本文档介绍一些 Python 编程的最佳实践。
    
    ## 代码风格
    
    遵循 PEP 8 风格指南是编写优质 Python 代码的基础。
    使用有意义的变量名和函数名可以提高代码可读性。
    适当的注释和文档字符串能帮助其他开发者理解你的代码。
    
    ## 性能优化
    
    使用内置函数和标准库通常比自己实现更高效。
    列表推导式比传统循环更简洁且性能更好。
    在处理大数据时，考虑使用生成器以节省内存。
    
    ## 错误处理
    
    使用异常处理机制来处理可能出现的错误。
    避免使用裸露的 except 子句，应该指定具体的异常类型。
    适当的日志记录有助于调试和监控应用程序。
    """
    
    sample_file = Path("sample_python_guide.md")
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print(f"\n✓ 创建示例文档: {sample_file}")
    
    # 执行文档分析
    print("\n" + "-" * 60)
    print("正在分析文档...")
    print("-" * 60)
    
    analysis = processor.analyze(sample_file)
    
    # 显示可读性分析
    if 'readability' in analysis:
        print("\n【可读性分析】")
        readability = analysis['readability']
        print(f"  可读性评分: {readability.get('score', 'N/A')}/100")
        print(f"  平均句子长度: {readability.get('avg_sentence_length', 'N/A')} 词")
        print(f"  平均词长: {readability.get('avg_word_length', 'N/A')} 字符")
        print(f"  建议: {readability.get('suggestion', 'N/A')}")
    
    # 显示结构分析
    if 'structure' in analysis:
        print("\n【结构分析】")
        structure = analysis['structure']
        print(f"  段落数量: {structure.get('paragraph_count', 'N/A')}")
        print(f"  句子数量: {structure.get('sentence_count', 'N/A')}")
        print(f"  标题数量: {structure.get('header_count', 'N/A')}")
        print(f"  平均段落长度: {structure.get('avg_paragraph_length', 'N/A')} 词")
        print(f"  结构评分: {structure.get('structure_score', 'N/A')}/100")
    
    # 显示关键词提取
    if 'keywords' in analysis:
        print("\n【关键词提取】")
        keywords = analysis['keywords']
        print("  前10个关键词:")
        for i, kw in enumerate(keywords[:10], 1):
            print(f"    {i}. {kw['word']} (出现 {kw['frequency']} 次)")
    
    # 显示统计信息
    if 'statistics' in analysis:
        print("\n【统计信息】")
        stats = analysis['statistics']
        print(f"  字符总数: {stats.get('char_count', 'N/A')}")
        print(f"  单词总数: {stats.get('word_count', 'N/A')}")
        print(f"  句子总数: {stats.get('sentence_count', 'N/A')}")
        print(f"  段落总数: {stats.get('paragraph_count', 'N/A')}")
        print(f"  数字出现次数: {stats.get('numbers_count', 'N/A')}")
        print(f"  特殊字符数: {stats.get('special_chars_count', 'N/A')}")
    
    # 保存分析结果
    output_file = Path("analysis_result.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 分析结果已保存到: {output_file}")
    
    # 清理
    sample_file.unlink()
    output_file.unlink()
    
    print("\n" + "=" * 60)
    print("✓ 示例完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
