#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
集成测试 - 测试完整的工作流程
"""
import unittest
import tempfile
from pathlib import Path
from AIDocGenius import DocProcessor


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = DocProcessor()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # 创建测试文档
        self.test_content = """
        人工智能技术正在快速发展。机器学习是人工智能的核心技术之一。
        深度学习在图像识别和自然语言处理领域取得了突破性进展。
        未来，人工智能将在更多领域发挥重要作用。
        """
        
        self.test_file = self.temp_path / "test_document.txt"
        self.test_file.write_text(self.test_content, encoding='utf-8')
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)
    
    def test_full_workflow_summarize_and_convert(self):
        """测试完整工作流：摘要 + 转换"""
        # 1. 生成摘要
        summary = self.processor.generate_summary(
            self.test_file,
            max_length=100
        )
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        
        # 2. 转换格式
        output_md = self.temp_path / "output.md"
        self.processor.convert(self.test_file, output_md)
        self.assertTrue(output_md.exists())
        
        # 3. 转换为 HTML
        output_html = self.temp_path / "output.html"
        self.processor.convert(output_md, output_html)
        self.assertTrue(output_html.exists())
    
    def test_full_workflow_analyze_and_summarize(self):
        """测试完整工作流：分析 + 摘要"""
        # 1. 分析文档
        analysis = self.processor.analyze(self.test_file)
        self.assertIn('readability', analysis)
        self.assertIn('statistics', analysis)
        
        # 2. 生成摘要
        summary = self.processor.generate_summary(
            self.test_file,
            max_length=50
        )
        self.assertIsInstance(summary, str)
    
    def test_batch_process_multiple_files(self):
        """测试批量处理多个文件"""
        # 创建多个测试文件
        for i in range(3):
            file = self.temp_path / f"doc{i}.txt"
            file.write_text(f"文档{i}的内容。" * 10, encoding='utf-8')
        
        # 批量处理
        output_dir = self.temp_path / "output"
        output_dir.mkdir(exist_ok=True)
        
        results = self.processor.batch_process(
            input_dir=str(self.temp_path),
            output_dir=str(output_dir),
            operations=['summarize'],
            max_length=50
        )
        
        self.assertIsInstance(results, dict)
    
    def test_error_handling_invalid_file(self):
        """测试错误处理：无效文件"""
        invalid_file = self.temp_path / "nonexistent.txt"
        
        with self.assertRaises(Exception):
            self.processor.generate_summary(invalid_file)
    
    def test_error_handling_empty_file(self):
        """测试错误处理：空文件"""
        empty_file = self.temp_path / "empty.txt"
        empty_file.write_text("", encoding='utf-8')
        
        summary = self.processor.generate_summary(empty_file, max_length=100)
        self.assertEqual(summary, "")


class TestProcessorConfiguration(unittest.TestCase):
    """测试处理器配置"""
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = {
            'max_summary_length': 200,
            'default_language': 'zh'
        }
        processor = DocProcessor(config=config)
        self.assertEqual(processor.config['max_summary_length'], 200)
    
    def test_default_config(self):
        """测试默认配置"""
        processor = DocProcessor()
        self.assertIsInstance(processor.config, dict)


if __name__ == '__main__':
    unittest.main()
