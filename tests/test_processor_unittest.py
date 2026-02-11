#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 DocProcessor 类
"""
import unittest
import tempfile
from pathlib import Path
from AIDocGenius import DocProcessor


class TestDocProcessor(unittest.TestCase):
    """测试文档处理器"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = DocProcessor()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # 创建测试文档
        self.test_text = """
        人工智能技术正在快速发展。机器学习是人工智能的核心技术之一。
        深度学习在图像识别和自然语言处理领域取得了突破性进展。
        未来，人工智能将在更多领域发挥重要作用。
        """
        
        self.test_file = self.temp_path / "test_doc.txt"
        self.test_file.write_text(self.test_text, encoding='utf-8')
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)
    
    def test_initialization(self):
        """测试初始化"""
        processor = DocProcessor()
        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.translator)
        self.assertIsNotNone(processor.converter)
        self.assertIsNotNone(processor.analyzer)
        self.assertIsNotNone(processor.comparator)
        self.assertIsNotNone(processor.merger)
    
    def test_generate_summary(self):
        """测试摘要生成"""
        summary = self.processor.generate_summary(self.test_file, max_length=100)
        
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        self.assertLess(len(summary), len(self.test_text))
    
    def test_analyze(self):
        """测试文档分析"""
        result = self.processor.analyze(self.test_file)
        
        self.assertIn('readability', result)
        self.assertIn('statistics', result)
        self.assertIn('keywords', result)
    
    def test_convert(self):
        """测试格式转换"""
        output_file = self.temp_path / "output.md"
        
        self.processor.convert(self.test_file, output_file)
        
        self.assertTrue(output_file.exists())

    def test_process_document_text(self):
        """测试 process_document 文本"""
        result = self.processor.process_document(self.test_file)
        self.assertEqual(result.get("format"), "text")
        self.assertIn("content", result)
        self.assertIn("info", result)

    def test_process_document_structured(self):
        """测试 process_document 结构化文件"""
        data_file = self.temp_path / "data.json"
        data_file.write_text('{"a": 1, "b": 2}', encoding='utf-8')
        result = self.processor.process_document(data_file)
        self.assertEqual(result.get("format"), "structured")
        self.assertIsInstance(result.get("content"), dict)
    
    def test_compare_documents(self):
        """测试文档比较"""
        # 创建第二个测试文档
        test_file2 = self.temp_path / "test_doc2.txt"
        test_file2.write_text("这是另一个测试文档。内容不太相同。", encoding='utf-8')
        
        result = self.processor.compare_documents(self.test_file, test_file2)
        
        self.assertIn('similarity', result)
        self.assertIn('differences', result)
        self.assertIn('statistics', result)
        self.assertIsInstance(result['similarity'], float)
    
    def test_merge_documents(self):
        """测试文档合并"""
        # 创建多个测试文档
        doc1 = self.temp_path / "doc1.txt"
        doc2 = self.temp_path / "doc2.txt"
        
        doc1.write_text("文档1的内容", encoding='utf-8')
        doc2.write_text("文档2的内容", encoding='utf-8')
        
        output_file = self.temp_path / "merged.txt"
        
        self.processor.merge_documents([doc1, doc2], output_file)
        
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn("文档1的内容", content)
        self.assertIn("文档2的内容", content)

    def test_batch_process_outputs(self):
        """测试批量处理输出文件"""
        output_dir = self.temp_path / "outputs"
        results = self.processor.batch_process(
            input_dir=str(self.temp_path),
            output_dir=str(output_dir),
            operations=["summarize", "analyze", "convert"],
            max_length=50,
            output_format="md"
        )

        self.assertIsInstance(results, dict)
        file_results = results.get(str(self.test_file), {})
        summary_out = Path(file_results.get("summary_output", ""))
        analysis_out = Path(file_results.get("analysis_output", ""))
        convert_out = Path(file_results.get("converted_output", ""))
        self.assertTrue(summary_out.exists())
        self.assertTrue(analysis_out.exists())
        self.assertTrue(convert_out.exists())
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = {'test_key': 'test_value'}
        processor = DocProcessor(config=config)
        
        self.assertEqual(processor.config['test_key'], 'test_value')


if __name__ == '__main__':
    unittest.main()
