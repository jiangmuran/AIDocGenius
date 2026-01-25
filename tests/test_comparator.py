#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试文档比较功能
"""
import unittest
from AIDocGenius.comparator import DocumentComparator


class TestComparator(unittest.TestCase):
    """测试文档比较器"""
    
    def setUp(self):
        """测试前准备"""
        self.comparator = DocumentComparator()
        self.text1 = "这是第一个测试文档。它包含一些内容。"
        self.text2 = "这是第二个测试文档。它包含不同的内容。"
    
    def test_compare_identical_documents(self):
        """测试相同文档"""
        result = self.comparator.compare(self.text1, self.text1)
        
        self.assertEqual(result['similarity'], 1.0)
        self.assertIn('statistics', result)
        self.assertIn('differences', result)
    
    def test_compare_different_documents(self):
        """测试不同文档"""
        result = self.comparator.compare(self.text1, self.text2)
        
        self.assertLess(result['similarity'], 1.0)
        self.assertGreater(result['similarity'], 0.0)
    
    def test_compare_empty_documents(self):
        """测试空文档"""
        result = self.comparator.compare("", "")
        self.assertEqual(result['similarity'], 1.0)
    
    def test_compare_one_empty(self):
        """测试一个空文档"""
        result = self.comparator.compare(self.text1, "")
        self.assertEqual(result['similarity'], 0.0)
    
    def test_statistics(self):
        """测试统计信息"""
        result = self.comparator.compare(self.text1, self.text2)
        stats = result['statistics']
        
        self.assertIn('length1', stats)
        self.assertIn('length2', stats)
        self.assertIn('words1', stats)
        self.assertIn('words2', stats)
    
    def test_find_common_phrases(self):
        """测试查找共同短语"""
        text1 = "人工智能正在改变世界。技术发展迅速。"
        text2 = "人工智能正在改变未来。科技发展很快。"
        
        common = self.comparator.find_common_phrases(text1, text2, min_length=5)
        
        self.assertIsInstance(common, list)


if __name__ == '__main__':
    unittest.main()
