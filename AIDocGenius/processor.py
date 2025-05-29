"""
文档处理器基类
"""
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from .exceptions import DocumentProcessError
from .translator import Translator
from .summarizer import Summarizer
from .converter import Converter
from .analyzer import Analyzer
from .utils import load_document, save_document

class DocProcessor:
    """文档处理器基类，提供基础的文档处理功能"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._supported_formats = {
            'pdf': ['.pdf'],
            'word': ['.doc', '.docx'],
            'text': ['.txt', '.md', '.rst'],
            'image': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        }
        self.translator = Translator()
        self.summarizer = Summarizer(model_name="bert-base-chinese", device="cuda" if torch.cuda.is_available() else "cpu")
        self.converter = Converter()
        self.analyzer = Analyzer()

    def process_document(
        self, 
        input_path: Union[str, Path], 
        output_path: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        处理文档的主要方法
        
        Args:
            input_path: 输入文档路径
            output_path: 输出路径（可选）
            **kwargs: 额外的处理参数
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise DocumentProcessError(f"文件不存在: {input_path}")
            
        file_format = self._get_file_format(input_path)
        if not file_format:
            raise DocumentProcessError(f"不支持的文件格式: {input_path.suffix}")
            
        try:
            result = self._process_by_format(input_path, file_format, **kwargs)
            if output_path:
                self._save_result(result, output_path)
            return result
        except Exception as e:
            raise DocumentProcessError(f"处理文档时出错: {str(e)}")
    
    def _get_file_format(self, file_path: Path) -> Optional[str]:
        """获取文件格式"""
        suffix = file_path.suffix.lower()
        for format_type, extensions in self._supported_formats.items():
            if suffix in extensions:
                return format_type
        return None
    
    def _process_by_format(
        self, 
        file_path: Path, 
        file_format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """根据文件格式调用相应的处理方法"""
        method_name = f"_process_{file_format}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(file_path, **kwargs)
        raise NotImplementedError(f"未实现的文件格式处理方法: {file_format}")
    
    def _save_result(self, result: Dict[str, Any], output_path: Union[str, Path]):
        """保存处理结果"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 根据输出路径的后缀决定保存格式
        if output_path.suffix == '.json':
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        elif output_path.suffix == '.txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(result))
        else:
            raise DocumentProcessError(f"不支持的输出格式: {output_path.suffix}")
            
    def validate_file(self, file_path: Union[str, Path]) -> bool:
        """验证文件是否可处理"""
        file_path = Path(file_path)
        return (
            file_path.exists() and 
            file_path.is_file() and 
            self._get_file_format(file_path) is not None
        )

    def generate_summary(self, 
                        document_path: Union[str, Path],
                        max_length: Optional[int] = None,
                        min_length: Optional[int] = None) -> str:
        """
        生成文档摘要
        
        Args:
            document_path: 文档路径
            max_length: 摘要最大长度
            min_length: 摘要最小长度
            
        Returns:
            str: 生成的摘要文本
        """
        content = load_document(document_path)
        return self.summarizer.generate(content, max_length, min_length)

    def translate(self,
                 document_path: Union[str, Path],
                 target_language: str,
                 source_language: Optional[str] = None) -> str:
        """
        翻译文档
        
        Args:
            document_path: 文档路径
            target_language: 目标语言代码
            source_language: 源语言代码（可选）
            
        Returns:
            str: 翻译后的文本
        """
        content = load_document(document_path)
        return self.translator.translate(content, target_language, source_language)

    def convert(self,
                input_path: Union[str, Path],
                output_path: Union[str, Path],
                format_options: Optional[dict] = None) -> None:
        """
        转换文档格式
        
        Args:
            input_path: 输入文档路径
            output_path: 输出文档路径
            format_options: 格式选项
        """
        self.converter.convert(input_path, output_path, format_options)

    def analyze(self,
                document_path: Union[str, Path],
                criteria: Optional[List[str]] = None) -> dict:
        """
        分析文档质量
        
        Args:
            document_path: 文档路径
            criteria: 分析标准列表
            
        Returns:
            dict: 分析结果报告
        """
        content = load_document(document_path)
        return self.analyzer.analyze(content, criteria)

    def batch_process(self,
                     input_dir: Union[str, Path],
                     output_dir: Union[str, Path],
                     operations: List[str],
                     **kwargs) -> dict:
        """
        批量处理文档
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            operations: 要执行的操作列表
            **kwargs: 其他参数
            
        Returns:
            dict: 处理结果报告
        """
        results = {}
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for file in input_path.glob("**/*"):
            if file.is_file():
                results[str(file)] = {}
                for operation in operations:
                    try:
                        if operation == "summarize":
                            results[str(file)]["summary"] = self.generate_summary(file, **kwargs)
                        elif operation == "translate":
                            results[str(file)]["translation"] = self.translate(file, **kwargs)
                        elif operation == "analyze":
                            results[str(file)]["analysis"] = self.analyze(file, **kwargs)
                    except Exception as e:
                        results[str(file)][operation] = f"Error: {str(e)}"
                        
        return results 