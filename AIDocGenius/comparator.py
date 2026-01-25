#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文档比较模块
"""
from typing import Dict, List, Any
from difflib import SequenceMatcher, unified_diff


class DocumentComparator:
    """文档比较器"""
    
    def __init__(self):
        """初始化比较器"""
        pass
    
    def compare(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        比较两个文档的相似度和差异
        
        Args:
            text1: 第一个文档的文本
            text2: 第二个文档的文本
            
        Returns:
            包含相似度和差异信息的字典
        """
        # 计算相似度
        similarity = self._calculate_similarity(text1, text2)
        
        # 获取差异
        differences = self._get_differences(text1, text2)
        
        # 统计信息
        stats = self._get_statistics(text1, text2)
        
        return {
            'similarity': similarity,
            'differences': differences,
            'statistics': stats
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            相似度分数 (0-1)
        """
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
        
        matcher = SequenceMatcher(None, text1, text2)
        return matcher.ratio()
    
    def _get_differences(self, text1: str, text2: str) -> List[str]:
        """
        获取两个文本的差异
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            差异列表
        """
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        
        diff = list(unified_diff(
            lines1, lines2,
            fromfile='文档1',
            tofile='文档2',
            lineterm=''
        ))
        
        return diff[:100]  # 限制返回前100个差异
    
    def _get_statistics(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        获取统计信息
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            统计信息字典
        """
        return {
            'length1': len(text1),
            'length2': len(text2),
            'length_diff': abs(len(text1) - len(text2)),
            'words1': len(text1.split()),
            'words2': len(text2.split()),
            'lines1': len(text1.splitlines()),
            'lines2': len(text2.splitlines())
        }
    
    def find_common_phrases(self, text1: str, text2: str, min_length: int = 10) -> List[str]:
        """
        查找两个文档中的共同短语
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            min_length: 最小短语长度
            
        Returns:
            共同短语列表
        """
        matcher = SequenceMatcher(None, text1, text2)
        common_phrases = []
        
        for match in matcher.get_matching_blocks():
            if match.size >= min_length:
                phrase = text1[match.a:match.a + match.size]
                common_phrases.append(phrase)
        
        return common_phrases
