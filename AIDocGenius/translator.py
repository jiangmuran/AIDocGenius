"""
翻译器模块
"""
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

try:
    import torch
    from transformers import MarianMTModel, MarianTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None
    MarianMTModel = None
    MarianTokenizer = None

try:
    from googletrans import Translator as GoogleTranslator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    GoogleTranslator = None

from .exceptions import TranslationError

class Translator:
    """多语言翻译器"""
    
    def __init__(self, device: Optional[str] = None, use_google: bool = True):
        """
        初始化翻译器
        
        Args:
            device: 设备（cuda/cpu），仅在 transformers 可用时有效
            use_google: 是否优先使用 Google Translate（更轻量级）
        """
        self.use_google = use_google and GOOGLETRANS_AVAILABLE
        self.device = device or ("cuda" if torch and torch.cuda.is_available() else "cpu")
        self._models: Dict[str, Any] = {}
        self._tokenizers: Dict[str, Any] = {}
        self._language_pairs = {
            'en2zh': 'Helsinki-NLP/opus-mt-en-zh',
            'zh2en': 'Helsinki-NLP/opus-mt-zh-en',
            'en2ja': 'Helsinki-NLP/opus-mt-en-jap',
            'ja2en': 'Helsinki-NLP/opus-mt-jap-en',
            'en2ko': 'Helsinki-NLP/opus-mt-en-ko',
            'ko2en': 'Helsinki-NLP/opus-mt-ko-en',
        }
        
        # Google Translate 语言代码映射
        self._google_lang_map = {
            'en': 'en', 'zh': 'zh-cn', 'ja': 'ja', 'ko': 'ko'
        }
        
        if self.use_google:
            try:
                self._google_translator = GoogleTranslator()
            except Exception:
                self.use_google = False
    
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
            batch_size: 批处理大小（仅用于 transformers）
            
        Returns:
            翻译后的文本或文本列表
        """
        # 优先使用 Google Translate（更轻量级，无需下载模型）
        if self.use_google:
            try:
                return self._translate_with_google(text, source_lang, target_lang)
            except Exception as e:
                # 如果 Google Translate 失败，回退到 transformers
                if not TRANSFORMERS_AVAILABLE:
                    raise TranslationError(f"翻译失败: {str(e)}")

        if source_lang == "auto":
            raise TranslationError("当前翻译引擎不支持自动检测语言，请显式指定 source_language")
        
        # 使用 transformers 模型
        if not TRANSFORMERS_AVAILABLE:
            raise TranslationError("没有可用的翻译引擎。请安装 transformers 或 googletrans")
            
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
    
    def _translate_with_google(
        self,
        text: Union[str, List[str]],
        source_lang: str,
        target_lang: str
    ) -> Union[str, List[str]]:
        """使用 Google Translate API 翻译"""
        # 转换语言代码
        src = self._google_lang_map.get(source_lang, source_lang)
        dst = self._google_lang_map.get(target_lang, target_lang)
        
        try:
            if isinstance(text, str):
                result = self._google_translator.translate(text, src=src, dest=dst)
                # 处理异步或同步结果
                if hasattr(result, 'text'):
                    return result.text
                elif hasattr(result, '__await__'):
                    # 如果是协程，需要同步执行（不推荐，但作为回退）
                    import asyncio
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # 如果事件循环正在运行，创建新任务
                            import concurrent.futures
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(asyncio.run, self._google_translator.translate(text, src=src, dest=dst))
                                result = future.result()
                        else:
                            result = loop.run_until_complete(self._google_translator.translate(text, src=src, dest=dst))
                    except RuntimeError:
                        result = asyncio.run(self._google_translator.translate(text, src=src, dest=dst))
                    return result.text if hasattr(result, 'text') else str(result)
                else:
                    return str(result)
            else:
                results = []
                for t in text:
                    result = self._google_translator.translate(t, src=src, dest=dst)
                    if hasattr(result, 'text'):
                        results.append(result.text)
                    elif hasattr(result, '__await__'):
                        import asyncio
                        try:
                            result = asyncio.run(result)
                            results.append(result.text if hasattr(result, 'text') else str(result))
                        except RuntimeError:
                            results.append(str(result))
                    else:
                        results.append(str(result))
                return results
        except Exception as e:
            raise TranslationError(f"Google Translate 翻译失败: {str(e)}")
    
    def _get_model_and_tokenizer(self, pair_key: str):
        """获取或加载模型和分词器"""
        if not TRANSFORMERS_AVAILABLE:
            raise TranslationError("transformers 库未安装，无法使用模型翻译")
            
        if pair_key not in self._models:
            model_name = self._language_pairs[pair_key]
            try:
                # 动态导入，避免在模块级别导入失败
                from transformers import MarianMTModel, MarianTokenizer
                self._models[pair_key] = MarianMTModel.from_pretrained(model_name).to(self.device)
                self._tokenizers[pair_key] = MarianTokenizer.from_pretrained(model_name)
            except Exception as e:
                raise TranslationError(f"加载翻译模型失败: {str(e)}")
                
        return self._models[pair_key], self._tokenizers[pair_key]
    
    def _translate_batch(
        self,
        texts: List[str],
        model: Any,
        tokenizer: Any
    ) -> List[str]:
        """批量翻译文本"""
        if not TRANSFORMERS_AVAILABLE:
            raise TranslationError("transformers 库未安装")
            
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
        if self.use_google:
            # Google Translate 支持更多语言
            return ['en', 'zh', 'ja', 'ko', 'fr', 'de', 'es', 'ru', 'ar', 'pt', 'it', 'vi', 'th', 'id', 'hi']
        else:
            languages = set()
            for pair in self._language_pairs.keys():
                source, target = pair.split('2')
                languages.add(source)
                languages.add(target)
            return sorted(list(languages)) 
