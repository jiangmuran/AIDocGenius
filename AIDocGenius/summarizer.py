"""
摘要生成器模块
"""
from typing import List, Optional, Union
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqGeneration
from .exceptions import SummarizationError

class Summarizer:
    """文档摘要生成器"""
    
    def __init__(
        self,
        model_name: str = "IDEA-CCNL/Randeng-Pegasus-238M-Summary-Chinese",
        device: Optional[str] = None,
        max_length: int = 1024,
        min_length: int = 50
    ):
        """
        初始化摘要生成器
        
        Args:
            model_name: 预训练模型名称
            device: 运行设备
            max_length: 最大输出长度
            min_length: 最小输出长度
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = max_length
        self.min_length = min_length
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqGeneration.from_pretrained(model_name).to(self.device)
        except Exception as e:
            raise SummarizationError(f"加载摘要模型失败: {str(e)}")
    
    def generate_summary(
        self,
        text: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
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
            num_beams: beam search的beam数量
            length_penalty: 长度惩罚系数
            no_repeat_ngram_size: 避免重复的n-gram大小
            
        Returns:
            str: 生成的摘要
        """
        try:
            # 编码输入
            inputs = self.tokenizer(
                text,
                max_length=self.max_length,
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
            raise SummarizationError(f"生成摘要失败: {str(e)}")
    
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