from typing import Dict, List, Optional
import re
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import PyPDF2
from docx import Document
import markdown
from bs4 import BeautifulSoup

class DocumentAnalyzer:
    """文档分析器"""

    def __init__(self):
        # 下载必要的NLTK数据
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        分析文本内容
        
        Args:
            text: 要分析的文本
            
        Returns:
            包含分析结果的字典
        """
        # 分词和句子分割
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
        
        # 去除停用词
        stop_words = set(stopwords.words('english'))
        words_no_stop = [word for word in words if word.isalnum() and word not in stop_words]
        
        # 词频统计
        word_freq = Counter(words_no_stop)
        
        # 计算平均句子长度
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'unique_words': len(set(words_no_stop)),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'top_words': dict(word_freq.most_common(10)),
            'readability_score': self._calculate_readability(text)
        }

    def analyze_document(self, file_path: str) -> Dict[str, any]:
        """
        分析文档文件
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            包含分析结果的字典
        """
        text = self._extract_text(file_path)
        if not text:
            return {
                'error': 'Failed to extract text from document',
                'analysis': None
            }
            
        analysis = self.analyze_text(text)
        return {
            'error': None,
            'analysis': analysis
        }

    def _extract_text(self, file_path: str) -> Optional[str]:
        """从不同格式的文档中提取文本"""
        try:
            ext = file_path.lower().split('.')[-1]
            
            if ext == 'pdf':
                return self._extract_from_pdf(file_path)
            elif ext in ['doc', 'docx']:
                return self._extract_from_docx(file_path)
            elif ext == 'md':
                return self._extract_from_markdown(file_path)
            elif ext == 'txt':
                return self._extract_from_txt(file_path)
            else:
                return None
        except Exception:
            return None

    def _extract_from_pdf(self, file_path: str) -> str:
        """从PDF文件提取文本"""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """从Word文档提取文本"""
        doc = Document(file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])

    def _extract_from_markdown(self, file_path: str) -> str:
        """从Markdown文件提取文本"""
        with open(file_path, 'r', encoding='utf-8') as file:
            md_text = file.read()
            html = markdown.markdown(md_text)
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text()

    def _extract_from_txt(self, file_path: str) -> str:
        """从文本文件提取文本"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _calculate_readability(self, text: str) -> float:
        """计算文本可读性分数（使用简化的Flesch Reading Ease公式）"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        if not sentences or not words:
            return 0.0
            
        avg_sentence_length = len(words) / len(sentences)
        syllable_count = sum([self._count_syllables(word) for word in words])
        avg_syllables_per_word = syllable_count / len(words)
        
        # Flesch Reading Ease Score
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        return round(max(0, min(100, score)), 2)

    def _count_syllables(self, word: str) -> int:
        """计算单词的音节数"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count
