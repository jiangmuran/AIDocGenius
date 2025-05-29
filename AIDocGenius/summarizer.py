from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqGeneration
import numpy as np
from .utils import logger

class Summarizer:
    """
    文档摘要生成器
    """
    
    def __init__(self,
                 model_name: str = "bert-base-chinese",
                 device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        初始化摘要生成器
        
        Args:
            model_name: 使用的模型名称
            device: 运行设备
        """
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqGeneration.from_pretrained(model_name).to(device)
        logger.info(f"Initialized summarizer with model {model_name} on {device}")
        
    def generate(self,
                content: str,
                max_length: Optional[int] = None,
                min_length: Optional[int] = None) -> str:
        """
        生成文档摘要
        
        Args:
            content: 文档内容
            max_length: 摘要最大长度
            min_length: 摘要最小长度
            
        Returns:
            str: 生成的摘要
        """
        # 设置默认长度
        if max_length is None:
            max_length = min(len(content.split()) // 3, 150)
        if min_length is None:
            min_length = max(len(content.split()) // 10, 30)
            
        try:
            # 对长文本进行分段处理
            segments = self._split_into_segments(content)
            summaries = []
            
            for segment in segments:
                inputs = self.tokenizer(segment, return_tensors="pt", truncation=True, max_length=1024)
                inputs = inputs.to(self.device)
                
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=4,
                    length_penalty=2.0,
                    early_stopping=True
                )
                
                summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(summary)
            
            # 合并所有摘要
            final_summary = self._merge_summaries(summaries)
            logger.info(f"Generated summary of length {len(final_summary.split())}")
            return final_summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
            
    def _split_into_segments(self, content: str, max_segment_length: int = 1000) -> list:
        """
        将长文本分割成小段
        
        Args:
            content: 文档内容
            max_segment_length: 每段最大长度
            
        Returns:
            list: 文本段落列表
        """
        words = content.split()
        segments = []
        current_segment = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) > max_segment_length:
                segments.append(" ".join(current_segment))
                current_segment = [word]
                current_length = len(word)
            else:
                current_segment.append(word)
                current_length += len(word) + 1  # +1 for space
                
        if current_segment:
            segments.append(" ".join(current_segment))
            
        return segments
        
    def _merge_summaries(self, summaries: list) -> str:
        """
        合并多个摘要
        
        Args:
            summaries: 摘要列表
            
        Returns:
            str: 合并后的摘要
        """
        if len(summaries) == 1:
            return summaries[0]
            
        # 使用简单的连接策略，可以根据需要改进
        merged = " ".join(summaries)
        
        # 去除重复的句子
        sentences = merged.split("。")
        unique_sentences = list(dict.fromkeys(sentences))
        
        return "。".join(unique_sentences) 