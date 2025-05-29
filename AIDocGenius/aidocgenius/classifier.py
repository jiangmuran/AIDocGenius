from typing import Dict, List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from .analyzer import DocumentAnalyzer

class DocumentClassifier:
    """文档分类器"""

    CATEGORIES = [
        'business',
        'technical',
        'legal',
        'academic',
        'personal',
        'other'
    ]

    def __init__(self):
        self.analyzer = DocumentAnalyzer()
        self.classifier = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )),
            ('clf', MultinomialNB())
        ])
        self.is_trained = False

    def train(self, training_data: List[Dict[str, str]]) -> None:
        """
        训练分类器
        
        Args:
            training_data: 训练数据列表，每项包含 'text' 和 'category' 字段
        """
        texts = [item['text'] for item in training_data]
        categories = [item['category'] for item in training_data]
        
        self.classifier.fit(texts, categories)
        self.is_trained = True

    def classify_text(self, text: str) -> Dict[str, any]:
        """
        对文本进行分类
        
        Args:
            text: 要分类的文本
            
        Returns:
            包含分类结果的字典
        """
        if not self.is_trained:
            return {
                'error': 'Classifier not trained',
                'category': None,
                'confidence': 0.0
            }
            
        # 获取预测概率
        probabilities = self.classifier.predict_proba([text])[0]
        category_idx = np.argmax(probabilities)
        confidence = probabilities[category_idx]
        
        return {
            'error': None,
            'category': self.CATEGORIES[category_idx],
            'confidence': round(float(confidence) * 100, 2),
            'all_probabilities': {
                cat: round(float(prob) * 100, 2)
                for cat, prob in zip(self.CATEGORIES, probabilities)
            }
        }

    def classify_document(self, file_path: str) -> Dict[str, any]:
        """
        对文档进行分类
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            包含分类结果的字典
        """
        text = self.analyzer._extract_text(file_path)
        if not text:
            return {
                'error': 'Failed to extract text from document',
                'classification': None
            }
            
        classification = self.classify_text(text)
        if classification['error']:
            return {
                'error': classification['error'],
                'classification': None
            }
            
        # 添加文档分析结果
        analysis = self.analyzer.analyze_text(text)
        classification['document_analysis'] = analysis
        
        return {
            'error': None,
            'classification': classification
        }

    def get_category_keywords(self) -> Dict[str, List[str]]:
        """获取每个类别的关键词"""
        if not self.is_trained:
            return {}
            
        feature_names = self.classifier.named_steps['tfidf'].get_feature_names_out()
        coefficients = self.classifier.named_steps['clf'].feature_log_prob_
        
        keywords = {}
        for idx, category in enumerate(self.CATEGORIES):
            # 获取该类别最重要的10个特征词
            top_indices = np.argsort(coefficients[idx])[-10:]
            keywords[category] = [
                feature_names[i] for i in top_indices
            ]
            
        return keywords

    def suggest_category(self, keywords: List[str]) -> Dict[str, any]:
        """
        根据关键词建议文档类别
        
        Args:
            keywords: 关键词列表
            
        Returns:
            包含建议类别的字典
        """
        if not self.is_trained:
            return {
                'error': 'Classifier not trained',
                'suggestion': None
            }
            
        # 将关键词组合成文本
        text = ' '.join(keywords)
        classification = self.classify_text(text)
        
        return {
            'error': None,
            'suggestion': {
                'category': classification['category'],
                'confidence': classification['confidence'],
                'alternatives': [
                    {
                        'category': cat,
                        'probability': prob
                    }
                    for cat, prob in classification['all_probabilities'].items()
                    if prob > 20  # 只返回概率大于20%的类别
                ]
            }
        } 