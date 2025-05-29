from typing import Optional, Union, List
from pathlib import Path

from .translator import Translator
from .summarizer import Summarizer
from .converter import Converter
from .analyzer import Analyzer
from .utils import load_document, save_document

class DocProcessor:
    """
    文档处理器主类，整合所有文档处理功能
    """
    
    def __init__(self, 
                 model_name: str = "bert-base-chinese",
                 device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        初始化文档处理器
        
        Args:
            model_name: 使用的基础模型名称
            device: 运行设备 ('cuda' 或 'cpu')
        """
        self.translator = Translator()
        self.summarizer = Summarizer(model_name=model_name, device=device)
        self.converter = Converter()
        self.analyzer = Analyzer()

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