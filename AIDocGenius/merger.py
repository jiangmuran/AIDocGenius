#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文档合并模块
"""
from typing import List, Dict, Any, Optional
from pathlib import Path


class DocumentMerger:
    """文档合并器"""
    
    def __init__(self):
        """初始化合并器"""
        pass
    
    def merge(self, documents: List[str], separator: str = "\n\n---\n\n") -> str:
        """
        合并多个文档
        
        Args:
            documents: 文档内容列表
            separator: 文档之间的分隔符
            
        Returns:
            合并后的文档内容
        """
        if not documents:
            return ""
        
        # 过滤空文档
        non_empty_docs = [doc for doc in documents if doc.strip()]
        
        if not non_empty_docs:
            return ""
        
        return separator.join(non_empty_docs)
    
    def merge_files(
        self,
        file_paths: List[Path],
        output_path: Path,
        add_titles: bool = True,
        separator: str = "\n\n---\n\n"
    ) -> None:
        """
        合并多个文件
        
        Args:
            file_paths: 文件路径列表
            output_path: 输出文件路径
            add_titles: 是否添加文件名作为标题
            separator: 文档之间的分隔符
        """
        documents = []
        
        for path in file_paths:
            if not path.exists():
                continue
            
            try:
                content = path.read_text(encoding='utf-8')
                
                if add_titles:
                    title = f"# {path.stem}\n\n"
                    content = title + content
                
                documents.append(content)
            except Exception as e:
                print(f"Warning: Failed to read {path}: {e}")
                continue
        
        merged_content = self.merge(documents, separator)
        
        if merged_content:
            output_path.write_text(merged_content, encoding='utf-8')
    
    def smart_merge(
        self,
        documents: List[str],
        remove_duplicates: bool = True,
        sort_by_length: bool = False
    ) -> str:
        """
        智能合并文档
        
        Args:
            documents: 文档内容列表
            remove_duplicates: 是否移除重复内容
            sort_by_length: 是否按长度排序
            
        Returns:
            合并后的文档内容
        """
        if not documents:
            return ""
        
        # 移除重复
        if remove_duplicates:
            seen = set()
            unique_docs = []
            for doc in documents:
                doc_normalized = doc.strip()
                if doc_normalized and doc_normalized not in seen:
                    seen.add(doc_normalized)
                    unique_docs.append(doc)
            documents = unique_docs
        
        # 排序
        if sort_by_length:
            documents = sorted(documents, key=len, reverse=True)
        
        return self.merge(documents)
