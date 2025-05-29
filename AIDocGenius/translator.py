from typing import Optional
from googletrans import Translator as GoogleTranslator
from .utils import logger

class Translator:
    """
    文档翻译器
    """
    
    def __init__(self):
        """
        初始化翻译器
        """
        self.translator = GoogleTranslator()
        self.supported_languages = {
            'zh': 'chinese',
            'en': 'english',
            'ja': 'japanese',
            'ko': 'korean',
            'fr': 'french',
            'de': 'german',
            'es': 'spanish',
            'it': 'italian',
            'ru': 'russian',
            'ar': 'arabic'
        }
        logger.info("Initialized translator")
        
    def translate(self,
                content: str,
                target_language: str,
                source_language: Optional[str] = None) -> str:
        """
        翻译文本
        
        Args:
            content: 要翻译的文本
            target_language: 目标语言代码
            source_language: 源语言代码（可选）
            
        Returns:
            str: 翻译后的文本
        """
        try:
            # 验证语言代码
            if target_language not in self.supported_languages:
                raise ValueError(f"Unsupported target language: {target_language}")
            if source_language and source_language not in self.supported_languages:
                raise ValueError(f"Unsupported source language: {source_language}")
                
            # 分段翻译以处理长文本
            segments = self._split_into_segments(content)
            translated_segments = []
            
            for segment in segments:
                translation = self.translator.translate(
                    segment,
                    dest=target_language,
                    src=source_language if source_language else 'auto'
                )
                translated_segments.append(translation.text)
                
            # 合并翻译结果
            result = '\n'.join(translated_segments)
            logger.info(f"Translated text from {source_language or 'auto'} to {target_language}")
            return result
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise
            
    def _split_into_segments(self, content: str, max_length: int = 5000) -> list:
        """
        将长文本分割成小段
        
        Args:
            content: 要分割的文本
            max_length: 每段最大长度
            
        Returns:
            list: 文本段落列表
        """
        if len(content) <= max_length:
            return [content]
            
        segments = []
        current_segment = []
        current_length = 0
        
        # 按句子分割
        sentences = content.replace('。', '。\n').replace('！', '！\n').replace('？', '？\n').split('\n')
        
        for sentence in sentences:
            if current_length + len(sentence) > max_length:
                segments.append(''.join(current_segment))
                current_segment = [sentence]
                current_length = len(sentence)
            else:
                current_segment.append(sentence)
                current_length += len(sentence)
                
        if current_segment:
            segments.append(''.join(current_segment))
            
        return segments
        
    def get_supported_languages(self) -> dict:
        """
        获取支持的语言列表
        
        Returns:
            dict: 支持的语言代码和名称
        """
        return self.supported_languages.copy()
        
    def detect_language(self, text: str) -> str:
        """
        检测文本语言
        
        Args:
            text: 要检测的文本
            
        Returns:
            str: 检测到的语言代码
        """
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            raise 