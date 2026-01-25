#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例1：生成文档摘要
演示如何使用 AIDocGenius 生成文档摘要
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from AIDocGenius import DocProcessor

def main():
    """生成文档摘要示例"""
    print("=" * 60)
    print("示例1：文档摘要生成")
    print("=" * 60)
    
    # 创建处理器实例
    processor = DocProcessor()
    
    # 创建示例文档
    sample_text = """
    深度学习是机器学习的一个分支，它基于人工神经网络的研究，特别是利用多层
    神经网络来进行学习和处理。深度学习的概念源于对人工神经网络的研究，含多层的
    多层感知器就是一种深度学习结构。深度学习通过组合低层特征形成更加抽象的高层
    表示属性类别或特征，以发现数据的分布式特征表示。
    
    深度学习在图像识别、语音识别、自然语言处理等领域取得了重大突破。卷积神经
    网络（CNN）在图像处理方面表现出色，循环神经网络（RNN）在序列数据处理方面
    有独特优势，而变换器（Transformer）架构则推动了自然语言处理的革命性进展。
    
    现代深度学习框架如TensorFlow、PyTorch等，使得研究人员和工程师能够更容易地
    构建和训练复杂的神经网络模型。这些工具提供了自动微分、GPU加速等功能，
    大大提高了深度学习的开发效率和模型训练速度。
    """
    
    # 保存示例文档
    sample_file = Path("sample_document.txt")
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print(f"\n✓ 创建示例文档: {sample_file}")
    print(f"✓ 文档长度: {len(sample_text)} 字符")
    
    # 生成短摘要
    print("\n" + "-" * 60)
    print("生成短摘要（100字符以内）:")
    print("-" * 60)
    short_summary = processor.generate_summary(
        sample_file,
        max_length=100
    )
    print(short_summary)
    
    # 生成中等长度摘要
    print("\n" + "-" * 60)
    print("生成中等摘要（200字符以内）:")
    print("-" * 60)
    medium_summary = processor.generate_summary(
        sample_file,
        max_length=200
    )
    print(medium_summary)
    
    # 清理
    sample_file.unlink()
    print("\n" + "=" * 60)
    print("✓ 示例完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
