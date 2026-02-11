"""
文档处理器基类
"""
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

try:
    import torch
except ImportError:
    torch = None

from .exceptions import DocumentProcessError
from .translator import Translator
from .summarizer import Summarizer
from .converter import Converter
from .analyzer import Analyzer
from .comparator import DocumentComparator
from .merger import DocumentMerger
from .utils import load_document, save_document, ensure_text, get_file_info

class DocProcessor:
    """文档处理器基类，提供基础的文档处理功能"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._supported_formats = {
            'pdf': ['.pdf'],
            'word': ['.docx'],
            'text': ['.txt', '.md', '.rst'],
            'structured': ['.json', '.yaml', '.yml']
        }
        # 默认使用 Google Translate（更轻量级）
        self.translator = Translator(use_google=True)
        # 延迟初始化 summarizer，避免在导入时就加载模型
        self._summarizer = None
        self.converter = Converter()
        self.analyzer = Analyzer()
        self.comparator = DocumentComparator()
        self.merger = DocumentMerger()
    
    @property
    def summarizer(self):
        """延迟加载 summarizer"""
        if self._summarizer is None:
            summarizer_config = self.config.get("summarizer", {})
            if not isinstance(summarizer_config, dict):
                summarizer_config = {}
            # 默认使用简单摘要算法（无需下载模型）
            self._summarizer = Summarizer(
                use_simple=summarizer_config.get("use_simple", True),
                use_small_model=summarizer_config.get("use_small_model", False),
                model_name=summarizer_config.get("model_name"),
                max_length=summarizer_config.get("max_length", 1024),
                min_length=summarizer_config.get("min_length", 50),
                max_input_length=summarizer_config.get("max_input_length"),
                cache_dir=summarizer_config.get("cache_dir")
            )
        return self._summarizer

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

    def _process_text(self, file_path: Path, **kwargs) -> Dict[str, Any]:
        content = load_document(file_path)
        return {
            "format": "text",
            "content": content,
            "info": get_file_info(file_path)
        }

    def _process_pdf(self, file_path: Path, **kwargs) -> Dict[str, Any]:
        content = load_document(file_path)
        return {
            "format": "pdf",
            "content": content,
            "info": get_file_info(file_path)
        }

    def _process_word(self, file_path: Path, **kwargs) -> Dict[str, Any]:
        content = load_document(file_path)
        return {
            "format": "word",
            "content": content,
            "info": get_file_info(file_path)
        }

    def _process_structured(self, file_path: Path, **kwargs) -> Dict[str, Any]:
        content = load_document(file_path)
        return {
            "format": "structured",
            "content": content,
            "info": get_file_info(file_path)
        }
    
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
                        min_length: Optional[int] = None,
                        ratio: Optional[float] = None) -> str:
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
        return self.summarizer.generate_summary(
            ensure_text(content),
            max_length=max_length,
            min_length=min_length,
            ratio=ratio
        )

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
        # translator.translate 的参数顺序是 (text, source_lang, target_lang)
        # 语言代码映射
        lang_map = {
            "en": "en", "english": "en", "英文": "en",
            "zh": "zh", "chinese": "zh", "中文": "zh",
            "ja": "ja", "japanese": "ja", "日语": "ja",
            "ko": "ko", "korean": "ko", "韩语": "ko"
        }
        
        target_lang = lang_map.get(target_language.lower(), target_language.lower())
        if source_language is None:
            source_lang = "auto"
        elif source_language.lower() == "auto":
            source_lang = "auto"
        else:
            source_lang = lang_map.get(source_language.lower(), source_language.lower())
        
        # 直接调用 translator，它会自动处理语言对和回退（包括 Google Translate）
        try:
            return self.translator.translate(ensure_text(content), source_lang, target_lang)
        except Exception as e:
            raise DocumentProcessError(f"翻译失败: {str(e)}")

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
        return self.analyzer.analyze(ensure_text(content), criteria)

    def batch_process(self,
                     input_dir: Union[str, Path],
                     output_dir: Union[str, Path],
                     operations: List[str],
                     report: bool = False,
                     report_formats: Optional[List[str]] = None,
                     report_only: bool = False,
                     report_prefix: Optional[str] = None,
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

        output_path_resolved = output_path.resolve()
        
        import time

        total_files = 0
        processed_files = 0
        error_count = 0
        batch_start = time.time()
        report_files = []

        for file in input_path.glob("**/*"):
            if not file.is_file():
                continue
            try:
                if output_path_resolved in file.resolve().parents:
                    continue
            except Exception:
                pass

            total_files += 1
            results[str(file)] = {}
            file_entry = {
                "path": str(file),
                "operations": {},
                "outputs": {},
                "errors": {},
                "seconds": 0.0
            }
            file_start = time.time()
            for operation in operations:
                op_start = time.time()
                try:
                    rel_path = file.relative_to(input_path)
                    target_dir = output_path / rel_path.parent
                    target_dir.mkdir(parents=True, exist_ok=True)

                    if operation == "summarize":
                        summary = self.generate_summary(file, **kwargs)
                        results[str(file)]["summary"] = summary
                        output_file = target_dir / f"{file.stem}.summary.txt"
                        save_document(summary, output_file)
                        results[str(file)]["summary_output"] = str(output_file)
                        file_entry["outputs"]["summarize"] = str(output_file)
                    elif operation == "translate":
                        translation = self.translate(file, **kwargs)
                        results[str(file)]["translation"] = translation
                        target_language = kwargs.get("target_language", "en")
                        output_file = target_dir / f"{file.stem}.translated.{target_language}.txt"
                        save_document(translation, output_file)
                        results[str(file)]["translation_output"] = str(output_file)
                        file_entry["outputs"]["translate"] = str(output_file)
                    elif operation == "analyze":
                        analysis = self.analyze(file, **kwargs)
                        results[str(file)]["analysis"] = analysis
                        output_file = target_dir / f"{file.stem}.analysis.json"
                        save_document(analysis, output_file)
                        results[str(file)]["analysis_output"] = str(output_file)
                        file_entry["outputs"]["analyze"] = str(output_file)
                    elif operation == "convert":
                        output_format = kwargs.get("output_format")
                        if not output_format:
                            raise DocumentProcessError("convert 操作需要提供 output_format")
                        output_file = target_dir / f"{file.stem}.{output_format.lstrip('.')}"
                        self.convert(file, output_file)
                        results[str(file)]["converted_output"] = str(output_file)
                        file_entry["outputs"]["convert"] = str(output_file)
                    else:
                        results[str(file)][operation] = "Error: Unsupported operation"
                        file_entry["errors"][operation] = "Unsupported operation"
                    file_entry["operations"][operation] = {
                        "status": "ok",
                        "seconds": round(time.time() - op_start, 4)
                    }
                except Exception as e:
                    results[str(file)][operation] = f"Error: {str(e)}"
                    file_entry["errors"][operation] = str(e)
                    file_entry["operations"][operation] = {
                        "status": "error",
                        "seconds": round(time.time() - op_start, 4)
                    }
                    error_count += 1

            processed_files += 1
            file_entry["seconds"] = round(time.time() - file_start, 4)
            report_files.append(file_entry)
                        
        report_payload = None
        if report:
            if report_formats is None:
                report_formats = ["json"]

            summary_report = {
                "input_dir": str(input_path),
                "output_dir": str(output_path),
                "operations": operations,
                "total_files": total_files,
                "processed_files": processed_files,
                "error_count": error_count,
                "seconds": round(time.time() - batch_start, 4),
                "files": report_files
            }

            report_payload = summary_report

            report_prefix = report_prefix or "batch_report"

            if "json" in report_formats:
                report_path = output_path / f"{report_prefix}.json"
                save_document(summary_report, report_path)

            if "md" in report_formats:
                report_lines = [
                    "# Batch Processing Report",
                    "",
                    f"- Input: {input_path}",
                    f"- Output: {output_path}",
                    f"- Operations: {', '.join(operations)}",
                    f"- Total files: {total_files}",
                    f"- Processed files: {processed_files}",
                    f"- Errors: {error_count}",
                    "",
                    "## Results",
                ]
                for file_path, result in results.items():
                    report_lines.append(f"- {file_path}")
                    for key, value in result.items():
                        if key.endswith("_output"):
                            report_lines.append(f"  - {key}: {value}")
                        elif isinstance(value, str) and value.startswith("Error:"):
                            report_lines.append(f"  - {key}: {value}")
                report_path = output_path / f"{report_prefix}.md"
                save_document("\n".join(report_lines), report_path)

            if "csv" in report_formats:
                import csv

                report_path = output_path / f"{report_prefix}.csv"
                with open(report_path, "w", newline="", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["file", "operation", "status", "output", "error", "seconds"])
                    for file_entry in report_files:
                        file_path = file_entry["path"]
                        for op_name, op_info in file_entry["operations"].items():
                            status = op_info.get("status")
                            seconds = op_info.get("seconds")
                            output = file_entry["outputs"].get(op_name, "")
                            error = file_entry["errors"].get(op_name, "")
                            writer.writerow([file_path, op_name, status, output, error, seconds])

        if report_payload is not None:
            if report_only:
                return report_payload
            return {
                "results": results,
                "report": report_payload
            }

        return results
    
    def compare_documents(
        self,
        document1_path: Union[str, Path],
        document2_path: Union[str, Path]
    ) -> Dict[str, Any]:
        """
        比较两个文档
        
        Args:
            document1_path: 第一个文档路径
            document2_path: 第二个文档路径
            
        Returns:
            dict: 比较结果（相似度、差异等）
        """
        content1 = ensure_text(load_document(document1_path))
        content2 = ensure_text(load_document(document2_path))
        
        return self.comparator.compare(content1, content2)
    
    def merge_documents(
        self,
        document_paths: List[Union[str, Path]],
        output_path: Union[str, Path],
        smart_merge: bool = False
    ) -> None:
        """
        合并多个文档
        
        Args:
            document_paths: 文档路径列表
            output_path: 输出文件路径
            smart_merge: 是否使用智能合并（移除重复等）
        """
        if smart_merge:
            # 智能合并
            documents = []
            for path in document_paths:
                content = ensure_text(load_document(path))
                documents.append(content)
            
            merged_content = self.merger.smart_merge(documents)
            save_document(merged_content, output_path)
        else:
            # 普通合并
            paths = [Path(p) for p in document_paths]
            self.merger.merge_files(paths, Path(output_path)) 
