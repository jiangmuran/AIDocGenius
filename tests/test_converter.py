#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试格式转换功能
"""
import unittest
import tempfile
from pathlib import Path
from AIDocGenius.converter import Converter


class TestConverter(unittest.TestCase):
    """测试格式转换器"""
    
    def setUp(self):
        """测试前准备"""
        self.converter = Converter()
        self.test_text = "# 标题\n\n这是测试内容。\n\n## 子标题\n\n更多内容。"
        
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)
    
    def test_markdown_to_html(self):
        """测试 Markdown 转 HTML"""
        input_file = self.temp_path / "test.md"
        output_file = self.temp_path / "test.html"
        
        input_file.write_text(self.test_text, encoding='utf-8')
        
        self.converter.convert(str(input_file), str(output_file))
        
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('<h1>', content)
    
    def test_text_to_markdown(self):
        """测试文本转 Markdown"""
        input_file = self.temp_path / "test.txt"
        output_file = self.temp_path / "test.md"
        
        input_file.write_text("测试内容\n第二行", encoding='utf-8')
        
        self.converter.convert(str(input_file), str(output_file))
        
        self.assertTrue(output_file.exists())
    
    def test_markdown_to_json(self):
        """测试 Markdown 转 JSON"""
        input_file = self.temp_path / "test.md"
        output_file = self.temp_path / "test.json"
        
        input_file.write_text(self.test_text, encoding='utf-8')
        
        self.converter.convert(str(input_file), str(output_file))
        
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('{', content)
        self.assertIn('}', content)
    
    def test_unsupported_format(self):
        """测试不支持的格式"""
        input_file = self.temp_path / "test.md"
        output_file = self.temp_path / "test.xyz"
        
        input_file.write_text(self.test_text, encoding='utf-8')
        
        with self.assertRaises(Exception):
            self.converter.convert(str(input_file), str(output_file))
    
    def test_empty_file(self):
        """测试空文件转换"""
        input_file = self.temp_path / "empty.txt"
        output_file = self.temp_path / "empty.md"
        
        input_file.write_text("", encoding='utf-8')
        
        self.converter.convert(str(input_file), str(output_file))
        
        self.assertTrue(output_file.exists())


class TestConverterFormats(unittest.TestCase):
    """测试各种格式转换"""
    
    def setUp(self):
        self.converter = Converter()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)
    
    def test_detect_format(self):
        """测试格式检测"""
        from pathlib import Path
        
        test_cases = [
            ("test.txt", ".txt"),
            ("test.md", ".md"),
            ("test.html", ".html"),
            ("test.json", ".json"),
        ]
        
        for filename, expected in test_cases:
            suffix = Path(filename).suffix
            self.assertEqual(suffix, expected)


if __name__ == '__main__':
    unittest.main()
