#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试文档分析功能
"""
import unittest
from AIDocGenius.analyzer import Analyzer


class TestAnalyzer(unittest.TestCase):
    """测试文档分析器"""
    
    def setUp(self):
        """测试前准备"""
        self.analyzer = Analyzer()
        self.test_text = """
        人工智能是计算机科学的一个重要分支。它包括机器学习、深度学习等技术。
        这些技术正在改变我们的生活。从智能手机到自动驾驶，AI无处不在。
        """
    
    def test_analyze_basic(self):
        """测试基本分析"""
        result = self.analyzer.analyze(self.test_text)
        
        self.assertIn('readability', result)
        self.assertIn('statistics', result)
        self.assertIn('keywords', result)
    
    def test_readability_score(self):
        """测试可读性评分"""
        result = self.analyzer.analyze(self.test_text)
        score = result['readability']['score']
        
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_statistics(self):
        """测试统计信息"""
        result = self.analyzer.analyze(self.test_text)
        stats = result['statistics']
        
        self.assertIn('word_count', stats)
        self.assertIn('sentence_count', stats)
        self.assertIn('paragraph_count', stats)
        
        self.assertGreater(stats['word_count'], 0)
        self.assertGreater(stats['sentence_count'], 0)
    
    def test_keywords_extraction(self):
        """测试关键词提取"""
        result = self.analyzer.analyze(self.test_text)
        keywords = result['keywords']
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
    
    def test_empty_text(self):
        """测试空文本"""
        result = self.analyzer.analyze("")
        
        self.assertEqual(result['statistics']['word_count'], 0)
        self.assertEqual(result['statistics']['sentence_count'], 0)
    
    def test_chinese_text(self):
        """测试中文文本"""
        chinese_text = "这是一个测试。包含多个句子。用于测试分析功能。"
        result = self.analyzer.analyze(chinese_text)
        
        self.assertGreater(result['statistics']['word_count'], 0)
        self.assertGreater(result['statistics']['sentence_count'], 0)
    
    def test_english_text(self):
        """测试英文文本"""
        english_text = "This is a test. It contains multiple sentences. For testing analysis."
        result = self.analyzer.analyze(english_text)
        
        self.assertGreater(result['statistics']['word_count'], 0)
        self.assertGreater(result['statistics']['sentence_count'], 0)


class TestAnalyzerEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.analyzer = Analyzer()
    
    def test_single_word(self):
        """测试单个词"""
        result = self.analyzer.analyze("测试")
        self.assertEqual(result['statistics']['word_count'], 1)
    
    def test_special_characters(self):
        """测试特殊字符"""
        text = "Hello! 你好？ Test... 测试——"
        result = self.analyzer.analyze(text)
        self.assertGreater(result['statistics']['word_count'], 0)
    
    def test_numbers_and_symbols(self):
        """测试数字和符号"""
        text = "2024年，AI技术发展迅速。增长率达到50%以上。"
        result = self.analyzer.analyze(text)
        self.assertGreater(result['statistics']['word_count'], 0)


if __name__ == '__main__':
    unittest.main()
