"""
异常处理模块
"""

class AIDocGeniusError(Exception):
    """基础异常类"""
    pass

class DocumentProcessError(AIDocGeniusError):
    """文档处理异常"""
    pass

class TranslationError(AIDocGeniusError):
    """翻译异常"""
    pass

class SummarizationError(AIDocGeniusError):
    """摘要生成异常"""
    pass

class AnalysisError(AIDocGeniusError):
    """内容分析异常"""
    pass

class ConversionError(AIDocGeniusError):
    """格式转换异常"""
    pass

class ExtractionError(AIDocGeniusError):
    """文本提取异常"""
    pass

class OCRError(AIDocGeniusError):
    """OCR处理异常"""
    pass

class ConfigurationError(AIDocGeniusError):
    """配置异常"""
    pass

class ValidationError(AIDocGeniusError):
    """验证异常"""
    pass 