#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例5：批量文档处理
演示如何使用 AIDocGenius 批量处理多个文档
"""
import sys
from pathlib import Path
import json
sys.path.insert(0, str(Path(__file__).parent.parent))

from AIDocGenius import DocProcessor

def main():
    """批量文档处理示例"""
    print("=" * 60)
    print("示例5：批量文档处理")
    print("=" * 60)
    
    # 创建处理器实例
    processor = DocProcessor()
    
    # 创建测试目录
    test_dir = Path("test_batch_docs")
    test_dir.mkdir(exist_ok=True)
    output_dir = Path("test_batch_output")
    output_dir.mkdir(exist_ok=True)
    
    # 创建多个测试文档
    documents = {
        "文档1_技术文章.txt": """
        云计算是一种基于互联网的计算方式。
        用户可以通过网络访问共享的计算资源。
        云计算提供了灵活性和可扩展性。
        """,
        "文档2_产品介绍.txt": """
        我们的产品采用最新的人工智能技术。
        提供智能推荐和自动化处理功能。
        帮助用户提高工作效率。
        """,
        "文档3_用户手册.txt": """
        本手册介绍软件的基本使用方法。
        第一步：安装软件并创建账户。
        第二步：配置基本设置和偏好。
        第三步：开始使用各项功能。
        """
    }
    
    print(f"\n✓ 创建测试目录: {test_dir}")
    print(f"✓ 创建 {len(documents)} 个测试文档")
    
    # 保存测试文档
    for filename, content in documents.items():
        file_path = test_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"  - {filename}")
    
    # 批量处理：生成摘要和分析
    print("\n" + "-" * 60)
    print("开始批量处理...")
    print("-" * 60)
    
    operations = ["summarize", "analyze"]
    
    try:
        results = processor.batch_process(
            input_dir=test_dir,
            output_dir=output_dir,
            operations=operations,
            max_length=100  # 摘要参数
        )
        
        # 显示处理结果
        print("\n批量处理完成！结果如下：\n")
        
        for file_path, result in results.items():
            filename = Path(file_path).name
            print(f"【{filename}】")
            
            # 显示摘要
            if "summary" in result:
                if isinstance(result["summary"], str) and not result["summary"].startswith("Error"):
                    print(f"  摘要: {result['summary'][:80]}...")
                else:
                    print(f"  摘要: {result['summary']}")
            
            # 显示分析统计
            if "analysis" in result and isinstance(result["analysis"], dict):
                stats = result["analysis"].get("statistics", {})
                if stats:
                    print(f"  字数: {stats.get('word_count', 'N/A')}")
                    print(f"  句数: {stats.get('sentence_count', 'N/A')}")
                    readability = result["analysis"].get("readability", {})
                    if readability:
                        print(f"  可读性评分: {readability.get('score', 'N/A')}/100")
            
            print()
        
        # 保存完整结果
        result_file = output_dir / "batch_results.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 完整结果已保存到: {result_file}")
        
    except Exception as e:
        print(f"✗ 批量处理失败: {str(e)}")
    
    # 清理测试文件
    print("\n" + "-" * 60)
    print("清理测试文件...")
    for file in test_dir.glob("*"):
        file.unlink()
    test_dir.rmdir()
    
    for file in output_dir.glob("*"):
        file.unlink()
    output_dir.rmdir()
    
    print("\n" + "=" * 60)
    print("✓ 示例完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
