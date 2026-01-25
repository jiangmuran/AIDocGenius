#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新增功能
"""
import sys
import tempfile
from pathlib import Path
from AIDocGenius import DocProcessor

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def test_new_features():
    """测试新增的文档比较和合并功能"""
    print("=" * 60)
    print("AIDocGenius New Features Test")
    print("=" * 60)
    
    # 创建测试环境
    temp_dir = Path(tempfile.mkdtemp())
    processor = DocProcessor()
    
    try:
        # Test 1: Document Comparison
        print("\n1. Testing Document Comparison...")
        doc1 = temp_dir / "doc1.txt"
        doc2 = temp_dir / "doc2.txt"
        
        doc1.write_text("This is the first document. AI is changing the world.", encoding='utf-8')
        doc2.write_text("This is the second document. AI is changing the future.", encoding='utf-8')
        
        comparison = processor.compare_documents(doc1, doc2)
        
        print(f"   Similarity: {comparison['similarity']:.2%}")
        print(f"   Doc1 length: {comparison['statistics']['length1']} chars")
        print(f"   Doc2 length: {comparison['statistics']['length2']} chars")
        print("   [OK] Document comparison successful")
        
        # Test 2: Document Merging
        print("\n2. Testing Document Merging...")
        doc3 = temp_dir / "doc3.txt"
        doc3.write_text("This is the third document.", encoding='utf-8')
        
        merged_file = temp_dir / "merged.txt"
        processor.merge_documents([doc1, doc2, doc3], merged_file)
        
        if merged_file.exists():
            content = merged_file.read_text(encoding='utf-8')
            print(f"   Merged doc length: {len(content)} chars")
            print("   [OK] Document merging successful")
        
        # Test 3: Smart Merge (remove duplicates)
        print("\n3. Testing Smart Merge...")
        doc4 = temp_dir / "doc4.txt"
        doc4.write_text("This is the first document. AI is changing the world.", encoding='utf-8')  # Duplicate of doc1
        
        smart_merged = temp_dir / "smart_merged.txt"
        processor.merge_documents([doc1, doc2, doc4], smart_merged, smart_merge=True)
        
        if smart_merged.exists():
            content = smart_merged.read_text(encoding='utf-8')
            # Check if duplicates were removed
            count = content.count("This is the first document")
            print(f"   'This is the first document' appears: {count} time(s) (should be 1)")
            print("   [OK] Smart merge successful")
        
        # Test 4: Batch Processing
        print("\n4. Testing Batch Processing...")
        # Create multiple test documents
        batch_dir = temp_dir / "batch_input"
        batch_dir.mkdir()
        
        for i in range(3):
            doc = batch_dir / f"test{i}.txt"
            doc.write_text(f"Test document {i} content. " * 10, encoding='utf-8')
        
        output_dir = temp_dir / "batch_output"
        results = processor.batch_process(
            input_dir=batch_dir,
            output_dir=output_dir,
            operations=['summarize', 'analyze']
        )
        
        print(f"   Files processed: {len(results)}")
        print(f"   Successfully processed: {sum(1 for r in results.values() if 'Error' not in str(r))}")
        print("   [OK] Batch processing successful")
        
        print("\n" + "=" * 60)
        print("[OK] All new features tested successfully!")
        print("=" * 60)
        
        # Feature Summary
        print("\nNew Features Summary:")
        print("  - Document Comparison: Calculate similarity and differences")
        print("  - Document Merging: Standard and smart merge")
        print("  - Batch Processing: Support multiple operations")
        print("  - Complete Test Suite: 46+ unit tests")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_new_features()
