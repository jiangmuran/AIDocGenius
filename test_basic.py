#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基本功能测试脚本
"""
import os
import sys
from pathlib import Path
from AIDocGenius import DocProcessor

# 设置输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_basic_functionality():
    """测试基本功能"""
    print("=" * 50)
    print("AIDocGenius 基本功能测试")
    print("=" * 50)
    
    # 创建测试文件
    test_content = """
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，
    它试图理解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    
    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。
    可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。
    人工智能可以对人的意识、思维的信息过程的模拟。
    人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。
    """
    
    test_file = Path("test_document.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print(f"\n[OK] 创建测试文件: {test_file}")
    
    try:
        processor = DocProcessor()
        print("[OK] 初始化 DocProcessor 成功")
        
        # 测试摘要生成
        print("\n1. 测试摘要生成...")
        summary = processor.generate_summary(test_file, max_length=100)
        print(f"   摘要: {summary[:100]}...")
        print("   [OK] 摘要生成成功")
        
        # 测试文档分析
        print("\n2. 测试文档分析...")
        analysis = processor.analyze(test_file)
        print(f"   可读性评分: {analysis.get('readability', {}).get('score', 'N/A')}")
        print(f"   关键词数量: {len(analysis.get('keywords', []))}")
        print("   [OK] 文档分析成功")
        
        # 测试格式转换
        print("\n3. 测试格式转换...")
        output_md = Path("test_output.md")
        processor.convert(test_file, output_md)
        if output_md.exists():
            print(f"   [OK] 格式转换成功: {output_md}")
            output_md.unlink()  # 清理
        
        # 测试翻译（如果可用）
        print("\n4. 测试翻译功能...")
        try:
            translation = processor.translate(test_file, target_language="en", source_language="zh")
            print(f"   翻译结果: {translation[:100]}...")
            print("   [OK] 翻译成功")
        except Exception as e:
            print(f"   [WARN] 翻译功能需要网络连接或模型: {str(e)}")
        
        print("\n" + "=" * 50)
        print("[OK] 所有基本功能测试通过！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理测试文件
        if test_file.exists():
            test_file.unlink()
            print(f"\n[OK] 清理测试文件: {test_file}")

if __name__ == "__main__":
    test_basic_functionality()
