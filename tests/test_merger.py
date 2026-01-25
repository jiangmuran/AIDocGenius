#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试文档合并功能
"""
import unittest
import tempfile
from pathlib import Path
from AIDocGenius.merger import DocumentMerger


class TestMerger(unittest.TestCase):
    """测试文档合并器"""
    
    def setUp(self):
        """测试前准备"""
        self.merger = DocumentMerger()
        self.doc1 = "第一个文档的内容。"
        self.doc2 = "第二个文档的内容。"
        self.doc3 = "第三个文档的内容。"
    
    def test_merge_basic(self):
        """测试基本合并"""
        documents = [self.doc1, self.doc2, self.doc3]
        result = self.merger.merge(documents)
        
        self.assertIn(self.doc1, result)
        self.assertIn(self.doc2, result)
        self.assertIn(self.doc3, result)
    
    def test_merge_empty_list(self):
        """测试空列表"""
        result = self.merger.merge([])
        self.assertEqual(result, "")
    
    def test_merge_with_empty_documents(self):
        """测试包含空文档"""
        documents = [self.doc1, "", self.doc2, "  ", self.doc3]
        result = self.merger.merge(documents)
        
        # 应该只包含非空文档
        self.assertIn(self.doc1, result)
        self.assertIn(self.doc2, result)
        self.assertIn(self.doc3, result)
    
    def test_merge_custom_separator(self):
        """测试自定义分隔符"""
        documents = [self.doc1, self.doc2]
        separator = "\n\n***\n\n"
        result = self.merger.merge(documents, separator=separator)
        
        self.assertIn(separator, result)
    
    def test_smart_merge_remove_duplicates(self):
        """测试智能合并 - 移除重复"""
        documents = [self.doc1, self.doc2, self.doc1]  # doc1 重复
        result = self.merger.smart_merge(documents, remove_duplicates=True)
        
        # 统计 doc1 出现次数
        count = result.count(self.doc1.strip())
        self.assertEqual(count, 1)
    
    def test_smart_merge_sort_by_length(self):
        """测试智能合并 - 按长度排序"""
        short = "短"
        medium = "中等长度的文档"
        long = "这是一个很长很长的文档内容"
        
        documents = [medium, short, long]
        result = self.merger.smart_merge(documents, sort_by_length=True)
        
        # 最长的应该在前面
        self.assertTrue(result.index(long) < result.index(medium))
        self.assertTrue(result.index(medium) < result.index(short))


class TestMergerFiles(unittest.TestCase):
    """测试文件合并"""
    
    def setUp(self):
        self.merger = DocumentMerger()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)
    
    def test_merge_files(self):
        """测试合并文件"""
        # 创建测试文件
        file1 = self.temp_path / "doc1.txt"
        file2 = self.temp_path / "doc2.txt"
        
        file1.write_text("内容1", encoding='utf-8')
        file2.write_text("内容2", encoding='utf-8')
        
        # 合并
        output = self.temp_path / "merged.txt"
        self.merger.merge_files([file1, file2], output)
        
        self.assertTrue(output.exists())
        content = output.read_text(encoding='utf-8')
        self.assertIn("内容1", content)
        self.assertIn("内容2", content)
    
    def test_merge_files_with_titles(self):
        """测试合并文件并添加标题"""
        file1 = self.temp_path / "文档1.txt"
        file1.write_text("内容", encoding='utf-8')
        
        output = self.temp_path / "merged.txt"
        self.merger.merge_files([file1], output, add_titles=True)
        
        content = output.read_text(encoding='utf-8')
        self.assertIn("# 文档1", content)


if __name__ == '__main__':
    unittest.main()
