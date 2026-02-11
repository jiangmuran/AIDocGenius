"""
摘要生成器模块
"""
import os
from typing import List, Optional, Union
from pathlib import Path

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqGeneration
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None

from .exceptions import SummarizationError

class Summarizer:
    """文档摘要生成器"""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None,
        max_length: int = 1024,
        min_length: int = 50,
        use_simple: bool = True,
        use_small_model: bool = False,
        max_input_length: Optional[int] = None,
        cache_dir: Optional[str] = None
    ):
        """
        初始化摘要生成器
        
        Args:
            model_name: 预训练模型名称（如果为 None 且 use_simple=True，则使用简单摘要）
            device: 运行设备
            max_length: 最大输出长度
            min_length: 最小输出长度
            use_simple: 是否使用简单摘要算法（无需模型）
        """
        if use_small_model:
            use_simple = False
            if not model_name:
                model_name = "google/flan-t5-small"

        self.use_simple = use_simple or not TRANSFORMERS_AVAILABLE
        self.device = device or ("cuda" if torch and torch.cuda.is_available() else "cpu")
        self.max_length = max_length
        self.min_length = min_length
        self.model_name = model_name or "IDEA-CCNL/Randeng-Pegasus-238M-Summary-Chinese"
        self.cache_dir = cache_dir or os.getenv("MODEL_CACHE_DIR")
        if max_input_length is None:
            if "t5" in self.model_name.lower():
                max_input_length = 512
            else:
                max_input_length = 1024
        self.max_input_length = max_input_length
        
        if not self.use_simple and TRANSFORMERS_AVAILABLE:
            try:
                self._load_model()
            except Exception as e:
                # 如果加载模型失败，回退到简单摘要
                self.use_simple = True
                print(f"警告: 加载摘要模型失败，将使用简单摘要算法: {str(e)}")

    def _load_model(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        self.model = AutoModelForSeq2SeqGeneration.from_pretrained(self.model_name, cache_dir=self.cache_dir).to(self.device)

    def warmup(self) -> None:
        """预热模型并验证可用性"""
        if self.use_simple:
            return
        if not TRANSFORMERS_AVAILABLE:
            raise SummarizationError("transformers is not available")
        if not hasattr(self, "tokenizer") or not hasattr(self, "model"):
            self._load_model()
    
    def generate_summary(
        self,
        text: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        ratio: Optional[float] = None,
        num_beams: int = 4,
        length_penalty: float = 2.0,
        no_repeat_ngram_size: int = 3
    ) -> str:
        """
        生成文本摘要
        
        Args:
            text: 输入文本
            max_length: 最大输出长度
            min_length: 最小输出长度
            num_beams: beam search的beam数量（仅用于模型）
            length_penalty: 长度惩罚系数（仅用于模型）
            no_repeat_ngram_size: 避免重复的n-gram大小（仅用于模型）
            
        Returns:
            str: 生成的摘要
        """
        if ratio is not None:
            ratio = max(0.0, min(1.0, ratio))
            ratio_length = int(len(text) * ratio)
            if max_length is None:
                max_length = ratio_length
            else:
                max_length = min(max_length, ratio_length)

        if self.use_simple:
            return self._generate_simple_summary(text, max_length, min_length)
        
        if not TRANSFORMERS_AVAILABLE:
            return self._generate_simple_summary(text, max_length, min_length)
            
        try:
            # 编码输入
            prompt = text
            if "t5" in self.model_name.lower():
                prompt = f"summarize: {text}"

            inputs = self.tokenizer(
                prompt,
                max_length=self.max_input_length,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)
            
            # 生成摘要
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length or self.max_length,
                    min_length=min_length or self.min_length,
                    num_beams=num_beams,
                    length_penalty=length_penalty,
                    no_repeat_ngram_size=no_repeat_ngram_size,
                    early_stopping=True
                )
                
            # 解码输出
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return summary
            
        except Exception as e:
            # 如果模型生成失败，回退到简单摘要
            return self._generate_simple_summary(text, max_length, min_length)
    
    def _generate_simple_summary(
        self,
        text: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None
    ) -> str:
        """使用简单算法生成摘要（提取前N个句子）"""
        import re

        cleaned = text.strip()
        if not cleaned:
            return ""

        # 分割句子并保留标点
        sentences = re.findall(r'[^。！？.!?]+[。！？.!?]?', cleaned)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) == 1:
            if max_length is None or len(cleaned) <= max_length:
                return cleaned

        if not sentences:
            return cleaned[:max_length or 200] if max_length else cleaned[:200]
        
        # 计算目标句子数
        target_length = max_length or 200
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
        target_sentences = max(1, int(target_length / (avg_sentence_length or 50)))
        target_sentences = min(target_sentences, len(sentences))
        
        # 选择前N个句子
        summary_sentences = sentences[:target_sentences]
        summary = ''.join(summary_sentences)
        
        # 确保满足长度要求
        if max_length and len(summary) > max_length:
            summary = summary[:max_length]
        if min_length and len(summary) < min_length and len(sentences) > target_sentences:
            # 如果太短，添加更多句子
            additional = min(3, len(sentences) - target_sentences)
            summary_sentences = sentences[:target_sentences + additional]
            summary = ''.join(summary_sentences)
            if max_length and len(summary) > max_length:
                summary = summary[:max_length]
        
        return summary
    
    def generate_file_summary(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> str:
        """
        为文件生成摘要
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径（可选）
            **kwargs: 传递给generate_summary的参数
            
        Returns:
            str: 生成的摘要
        """
        try:
            # 读取文件
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 生成摘要
            summary = self.generate_summary(content, **kwargs)
            
            # 保存结果
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                    
            return summary
            
        except Exception as e:
            raise SummarizationError(f"处理文件摘要失败: {str(e)}")
    
    def generate_batch_summaries(
        self,
        texts: List[str],
        **kwargs
    ) -> List[str]:
        """
        批量生成摘要
        
        Args:
            texts: 输入文本列表
            **kwargs: 传递给generate_summary的参数
            
        Returns:
            List[str]: 摘要列表
        """
        return [self.generate_summary(text, **kwargs) for text in texts] 
