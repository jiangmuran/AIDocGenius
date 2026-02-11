from typing import Optional, List, Dict
import re
try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    nltk = None
    NLTK_AVAILABLE = False
from collections import Counter
from .utils import logger

class Analyzer:
    """
    文档分析器
    """
    
    def __init__(self):
        """
        初始化分析器
        """
        # 下载所需的 NLTK 资源
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt_tab')
            except LookupError:
                try:
                    nltk.download('punkt_tab', quiet=True)
                except Exception:
                    # 如果 punkt_tab 不可用，尝试 punkt
                    try:
                        nltk.data.find('tokenizers/punkt')
                    except LookupError:
                        nltk.download('punkt', quiet=True)

            try:
                nltk.data.find('taggers/averaged_perceptron_tagger_eng')
            except LookupError:
                try:
                    nltk.download('averaged_perceptron_tagger_eng', quiet=True)
                except Exception:
                    # 回退到旧版本资源名
                    try:
                        nltk.data.find('taggers/averaged_perceptron_tagger')
                    except LookupError:
                        nltk.download('averaged_perceptron_tagger', quiet=True)

        logger.info("Initialized analyzer")
        
    def analyze(self, content: str, criteria: Optional[List[str]] = None) -> Dict:
        """
        分析文档
        
        Args:
            content: 文档内容
            criteria: 分析标准列表
            
        Returns:
            Dict: 分析结果
        """
        if criteria is None:
            criteria = ['readability', 'structure', 'keywords', 'statistics']
            
        results = {}
        
        try:
            for criterion in criteria:
                if criterion == 'readability':
                    results['readability'] = self._analyze_readability(content)
                elif criterion == 'structure':
                    results['structure'] = self._analyze_structure(content)
                elif criterion == 'keywords':
                    results['keywords'] = self._extract_keywords(content)
                elif criterion == 'statistics':
                    results['statistics'] = self._get_statistics(content)
                    
            logger.info("Completed document analysis")
            return results
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
            
    def _analyze_readability(self, content: str) -> Dict:
        """
        分析文档可读性
        """
        sentences = self._sentence_tokenize(content)
        words = self._word_tokenize(content)
        
        # 计算平均句子长度
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # 计算平均词长
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # 简单的可读性评分
        readability_score = 100 - (avg_sentence_length * 0.5 + avg_word_length * 0.5)
        
        return {
            'score': round(readability_score, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'avg_word_length': round(avg_word_length, 2),
            'suggestion': self._get_readability_suggestion(readability_score)
        }
        
    def _analyze_structure(self, content: str) -> Dict:
        """
        分析文档结构
        """
        paragraphs = content.split('\n\n')
        sentences = self._sentence_tokenize(content)
        
        # 分析段落结构
        paragraph_lengths = [len(p.split()) for p in paragraphs if p.strip()]
        avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
        
        # 分析标题和小标题
        headers = re.findall(r'^#+\s+.+$', content, re.MULTILINE)
        
        return {
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': round(avg_paragraph_length, 2),
            'sentence_count': len(sentences),
            'header_count': len(headers),
            'structure_score': self._calculate_structure_score(paragraphs, headers)
        }
        
    def _extract_keywords(self, content: str, top_n: int = 10) -> List[Dict]:
        """
        提取关键词
        """
        tokens = self._word_tokenize(content.lower())

        if NLTK_AVAILABLE:
            tagged = nltk.pos_tag(tokens)
            keywords = [word for word, pos in tagged if pos.startswith(('NN', 'JJ'))]
        else:
            keywords = [word for word in tokens if len(word) > 1]

        keyword_freq = Counter(keywords)

        return [
            {'word': word, 'frequency': freq}
            for word, freq in keyword_freq.most_common(top_n)
        ]
        
    def _get_statistics(self, content: str) -> Dict:
        """
        获取文档统计信息
        """
        # 基本统计
        char_count = len(content)
        word_count = len(self._word_tokenize(content))
        sentence_count = len(self._sentence_tokenize(content))
        paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        
        # 特殊字符统计
        numbers = len(re.findall(r'\d+', content))
        special_chars = len(re.findall(r'[^\w\s]', content))
        
        return {
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'numbers_count': numbers,
            'special_chars_count': special_chars,
            'avg_word_per_sentence': round(word_count / sentence_count if sentence_count else 0, 2)
        }

    def _sentence_tokenize(self, content: str) -> List[str]:
        if NLTK_AVAILABLE:
            return nltk.sent_tokenize(content)
        sentences = re.split(r'[。！？.!?]+', content)
        return [s.strip() for s in sentences if s.strip()]

    def _word_tokenize(self, content: str) -> List[str]:
        if NLTK_AVAILABLE:
            return nltk.word_tokenize(content)
        return re.findall(r'[\u4e00-\u9fff]+|[A-Za-z0-9]+', content)
        
    def _get_readability_suggestion(self, score: float) -> str:
        """
        根据可读性评分生成建议
        """
        if score >= 80:
            return "文档可读性很好，适合大多数读者。"
        elif score >= 60:
            return "文档可读性一般，建议简化一些长句。"
        else:
            return "文档可读性较差，建议重写部分内容，使用更简单的句子结构。"
            
    def _calculate_structure_score(self, paragraphs: List[str], headers: List[str]) -> float:
        """
        计算文档结构评分
        """
        score = 100.0
        
        # 检查段落长度分布
        paragraph_lengths = [len(p.split()) for p in paragraphs if p.strip()]
        if paragraph_lengths:
            avg_length = sum(paragraph_lengths) / len(paragraph_lengths)
            if avg_length > 150:
                score -= 20
            elif avg_length < 30:
                score -= 10
                
        # 检查标题使用
        if not headers:
            score -= 30
        elif len(headers) < 3:
            score -= 10
            
        # 检查段落数量
        if len(paragraphs) < 3:
            score -= 20
            
        return round(max(0, score), 2) 
