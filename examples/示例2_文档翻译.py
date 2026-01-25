#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例2：文档翻译
演示如何使用 AIDocGenius 翻译文档
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from AIDocGenius import DocProcessor

def main():
    """文档翻译示例"""
    print("=" * 60)
    print("示例2：文档翻译")
    print("=" * 60)
    
    # 创建处理器实例
    processor = DocProcessor()
    
    # 创建中文示例文档
    chinese_text = """
    人工智能技术正在快速发展，已经广泛应用于各个领域。
    机器学习和深度学习是人工智能的核心技术。
    未来，人工智能将继续改变我们的生活方式。
    """
    
    chinese_file = Path("chinese_doc.txt")
    with open(chinese_file, "w", encoding="utf-8") as f:
        f.write(chinese_text)
    
    print(f"\n原文（中文）:")
    print("-" * 60)
    print(chinese_text.strip())
    
    # 中译英
    print("\n翻译成英文:")
    print("-" * 60)
    try:
        english_translation = processor.translate(
            chinese_file,
            target_language="en",
            source_language="zh"
        )
        print(english_translation)
    except Exception as e:
        print(f"翻译失败: {str(e)}")
        print("提示: 翻译功能需要网络连接")
    
    # 创建英文示例文档
    english_text = """
    Artificial intelligence is revolutionizing the way we work and live.
    Machine learning algorithms can now process vast amounts of data.
    The future of AI holds endless possibilities.
    """
    
    english_file = Path("english_doc.txt")
    with open(english_file, "w", encoding="utf-8") as f:
        f.write(english_text)
    
    print(f"\n\n原文（英文）:")
    print("-" * 60)
    print(english_text.strip())
    
    # 英译中
    print("\n翻译成中文:")
    print("-" * 60)
    try:
        chinese_translation = processor.translate(
            english_file,
            target_language="zh",
            source_language="en"
        )
        print(chinese_translation)
    except Exception as e:
        print(f"翻译失败: {str(e)}")
        print("提示: 翻译功能需要网络连接")
    
    # 清理
    chinese_file.unlink()
    english_file.unlink()
    
    print("\n" + "=" * 60)
    print("✓ 示例完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
