"""
翻译器模块
"""
from typing import Dict, List, Optional, Union
from pathlib import Path

import torch
from transformers import MarianMTModel, MarianTokenizer
from .exceptions import TranslationError

class Translator:
    """多语言翻译器"""
    
    def __init__(self, device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._models: Dict[str, MarianMTModel] = {}
        self._tokenizers: Dict[str, MarianTokenizer] = {}
        self._language_pairs = {
            'en2zh': 'Helsinki-NLP/opus-mt-en-zh',
            'zh2en': 'Helsinki-NLP/opus-mt-zh-en',
            'en2ja': 'Helsinki-NLP/opus-mt-en-jap',
            'ja2en': 'Helsinki-NLP/opus-mt-jap-en',
            'en2ko': 'Helsinki-NLP/opus-mt-en-ko',
            'ko2en': 'Helsinki-NLP/opus-mt-ko-en',
        }
    
    def translate(
        self,
        text: Union[str, List[str]],
        source_lang: str,
        target_lang: str,
        batch_size: int = 8
    ) -> Union[str, List[str]]:
        """
        翻译文本
        
        Args:
            text: 待翻译文本或文本列表
            source_lang: 源语言代码
            target_lang: 目标语言代码
            batch_size: 批处理大小
            
        Returns:
            翻译后的文本或文本列表
        """
        pair_key = f"{source_lang}2{target_lang}"
        if pair_key not in self._language_pairs:
            raise TranslationError(f"不支持的语言对: {pair_key}")
            
        try:
            model, tokenizer = self._get_model_and_tokenizer(pair_key)
            
            # 处理输入
            if isinstance(text, str):
                text = [text]
                return_string = True
            else:
                return_string = False
                
            # 分批处理
            results = []
            for i in range(0, len(text), batch_size):
                batch = text[i:i + batch_size]
                translated = self._translate_batch(batch, model, tokenizer)
                results.extend(translated)
                
            return results[0] if return_string else results
            
        except Exception as e:
            raise TranslationError(f"翻译过程出错: {str(e)}")
    
    def _get_model_and_tokenizer(self, pair_key: str):
        """获取或加载模型和分词器"""
        if pair_key not in self._models:
            model_name = self._language_pairs[pair_key]
            try:
                self._models[pair_key] = MarianMTModel.from_pretrained(model_name).to(self.device)
                self._tokenizers[pair_key] = MarianTokenizer.from_pretrained(model_name)
            except Exception as e:
                raise TranslationError(f"加载翻译模型失败: {str(e)}")
                
        return self._models[pair_key], self._tokenizers[pair_key]
    
    def _translate_batch(
        self,
        texts: List[str],
        model: MarianMTModel,
        tokenizer: MarianTokenizer
    ) -> List[str]:
        """批量翻译文本"""
        try:
            # 编码
            encoded = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            encoded = {k: v.to(self.device) for k, v in encoded.items()}
            
            # 翻译
            with torch.no_grad():
                outputs = model.generate(**encoded)
                
            # 解码
            return tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
        except Exception as e:
            raise TranslationError(f"批量翻译失败: {str(e)}")
    
    def translate_file(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        source_lang: str,
        target_lang: str
    ):
        """
        翻译文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            source_lang: 源语言代码
            target_lang: 目标语言代码
        """
        try:
            # 读取文件
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 翻译
            translated = self.translate(content, source_lang, target_lang)
            
            # 保存结果
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated)
                
        except Exception as e:
            raise TranslationError(f"文件翻译失败: {str(e)}")
            
    def get_supported_languages(self) -> List[str]:
        """获取支持的语言列表"""
        languages = set()
        for pair in self._language_pairs.keys():
            source, target = pair.split('2')
            languages.add(source)
            languages.add(target)
        return sorted(list(languages)) 