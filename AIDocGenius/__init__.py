"""
AIDocGenius - 智能文档处理助手
"""

__version__ = "0.1.0"

from .processor import DocProcessor
from .translator import Translator
from .summarizer import Summarizer
from .analyzer import ContentAnalyzer
from .converter import FormatConverter
from .extractor import TextExtractor
from .ocr import OCRProcessor

__all__ = [
    "DocProcessor",
    "Translator",
    "Summarizer",
    "ContentAnalyzer",
    "FormatConverter",
    "TextExtractor",
    "OCRProcessor",
] 