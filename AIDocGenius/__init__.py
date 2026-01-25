"""
AIDocGenius - 智能文档处理助手
"""

__version__ = "0.1.0"

from .processor import DocProcessor
from .translator import Translator
from .summarizer import Summarizer
from .analyzer import Analyzer
from .converter import Converter

__all__ = [
    "DocProcessor",
    "Translator",
    "Summarizer",
    "Analyzer",
    "Converter",
] 