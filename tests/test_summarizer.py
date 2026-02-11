#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试摘要生成功能
"""
import unittest
import tempfile
from pathlib import Path
from AIDocGenius.summarizer import Summarizer


class TestSummarizer(unittest.TestCase):
    """测试摘要生成器"""
    
    def setUp(self):
        """测试前准备"""
        self.summarizer = Summarizer(use_simple=True)
        self.test_text = """
        人工智能是计算机科学的一个分支。它试图理解智能的实质。
        该领域包括机器人、语言识别、图像识别等。人工智能从诞生以来发展迅速。
        未来人工智能将带来更多科技产品。人工智能可以模拟人的思维过程。
        """
    
    def test_summarize_short_text(self):
        """测试短文本摘要"""
        summary = self.summarizer.generate_summary(self.test_text, max_length=50)
        self.assertIsInstance(summary, str)
        self.assertLess(len(summary), len(self.test_text))
        self.assertGreater(len(summary), 0)
    
    def test_summarize_medium_text(self):
        """测试中等长度文本摘要"""
        summary = self.summarizer.generate_summary(self.test_text, max_length=100)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 20)
    
    def test_summarize_with_ratio(self):
        """测试使用比例参数"""
        summary = self.summarizer.generate_summary(self.test_text, ratio=0.3)
        self.assertIsInstance(summary, str)
        self.assertLess(len(summary), len(self.test_text))
    
    def test_empty_text(self):
        """测试空文本"""
        summary = self.summarizer.generate_summary("", max_length=100)
        self.assertEqual(summary, "")
    
    def test_very_short_text(self):
        """测试极短文本"""
        short_text = "这是一个测试。"
        summary = self.summarizer.generate_summary(short_text, max_length=100)
        self.assertEqual(summary.strip(), short_text.strip())

    def test_cache_dir_env(self):
        """测试缓存目录环境变量读取"""
        import os

        os.environ["MODEL_CACHE_DIR"] = "/tmp/aidocgenius_cache"
        summarizer = Summarizer(use_simple=True)
        self.assertEqual(summarizer.cache_dir, "/tmp/aidocgenius_cache")
        os.environ.pop("MODEL_CACHE_DIR", None)


class TestSummarizerEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.summarizer = Summarizer(use_simple=True)
    
    def test_single_sentence(self):
        """测试单句文本"""
        text = "这是唯一的一句话。"
        summary = self.summarizer.generate_summary(text, max_length=50)
        self.assertIn("这是", summary)
    
    def test_multiple_paragraphs(self):
        """测试多段落文本"""
        text = """
        第一段内容。这是第一段的第二句。
        
        第二段内容。这是第二段的第二句。
        
        第三段内容。这是第三段的第二句。
        """
        summary = self.summarizer.generate_summary(text, max_length=100)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
    
    def test_chinese_and_english_mixed(self):
        """测试中英文混合文本"""
        text = "AI人工智能 is changing the world. 它正在改变世界。"
        summary = self.summarizer.generate_summary(text, max_length=50)
        self.assertIsInstance(summary, str)


if __name__ == '__main__':
    unittest.main()
