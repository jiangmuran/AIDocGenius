from typing import Dict, List, Tuple
import difflib
from .analyzer import DocumentAnalyzer

class DocumentComparator:
    """文档比较器"""

    def __init__(self):
        self.analyzer = DocumentAnalyzer()

    def compare_documents(self, file_path1: str, file_path2: str) -> Dict[str, any]:
        """
        比较两个文档
        
        Args:
            file_path1: 第一个文档的路径
            file_path2: 第二个文档的路径
            
        Returns:
            包含比较结果的字典
        """
        # 提取文本
        text1 = self.analyzer._extract_text(file_path1)
        text2 = self.analyzer._extract_text(file_path2)
        
        if not text1 or not text2:
            return {
                'error': 'Failed to extract text from one or both documents',
                'comparison': None
            }
            
        return {
            'error': None,
            'comparison': self.compare_texts(text1, text2)
        }

    def compare_texts(self, text1: str, text2: str) -> Dict[str, any]:
        """
        比较两段文本
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            包含比较结果的字典
        """
        # 分析两段文本
        analysis1 = self.analyzer.analyze_text(text1)
        analysis2 = self.analyzer.analyze_text(text2)
        
        # 计算文本相似度
        similarity = self._calculate_similarity(text1, text2)
        
        # 找出共同的关键词
        common_words = set(analysis1['top_words'].keys()) & set(analysis2['top_words'].keys())
        
        # 生成差异报告
        diff_report = self._generate_diff_report(text1, text2)
        
        return {
            'similarity_score': similarity,
            'common_keywords': list(common_words),
            'text1_analysis': analysis1,
            'text2_analysis': analysis2,
            'differences': diff_report
        }

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算两段文本的相似度"""
        seq = difflib.SequenceMatcher(None, text1, text2)
        return round(seq.ratio() * 100, 2)

    def _generate_diff_report(self, text1: str, text2: str) -> Dict[str, any]:
        """生成详细的差异报告"""
        # 将文本分割成行
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        # 计算差异
        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))
        
        # 统计变更
        additions = len([line for line in diff if line.startswith('+ ')])
        deletions = len([line for line in diff if line.startswith('- ')])
        changes = len([line for line in diff if line.startswith('? ')])
        
        return {
            'additions': additions,
            'deletions': deletions,
            'changes': changes,
            'diff_details': self._format_diff_details(diff)
        }

    def _format_diff_details(self, diff: List[str]) -> List[Dict[str, str]]:
        """格式化差异详情"""
        formatted_diff = []
        for line in diff:
            if line.startswith('  '):  # 未改变的行
                formatted_diff.append({
                    'type': 'unchanged',
                    'content': line[2:]
                })
            elif line.startswith('+ '):  # 添加的行
                formatted_diff.append({
                    'type': 'addition',
                    'content': line[2:]
                })
            elif line.startswith('- '):  # 删除的行
                formatted_diff.append({
                    'type': 'deletion',
                    'content': line[2:]
                })
            # 忽略以 '?' 开头的行，因为它们只是用来标记具体的更改位置
        
        return formatted_diff 