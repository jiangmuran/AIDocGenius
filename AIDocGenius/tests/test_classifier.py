import pytest
from aidocgenius.classifier import DocumentClassifier

def test_classifier_initialization():
    classifier = DocumentClassifier()
    assert not classifier.is_trained
    assert len(classifier.CATEGORIES) > 0

def test_classifier_training():
    classifier = DocumentClassifier()
    
    training_data = [
        {
            'text': 'quarterly financial report revenue growth profit margin',
            'category': 'business'
        },
        {
            'text': 'python programming code development software engineering',
            'category': 'technical'
        },
        {
            'text': 'legal contract agreement terms conditions compliance',
            'category': 'legal'
        },
        {
            'text': 'research paper methodology analysis results conclusion',
            'category': 'academic'
        },
        {
            'text': 'family vacation photos personal diary notes',
            'category': 'personal'
        }
    ]
    
    classifier.train(training_data)
    assert classifier.is_trained

def test_text_classification():
    classifier = DocumentClassifier()
    
    # 训练数据
    training_data = [
        {
            'text': 'quarterly financial report revenue growth',
            'category': 'business'
        },
        {
            'text': 'python programming code development',
            'category': 'technical'
        }
    ]
    
    classifier.train(training_data)
    
    # 测试商业文本分类
    business_text = "annual revenue report and financial analysis"
    result = classifier.classify_text(business_text)
    
    assert result['error'] is None
    assert result['category'] in classifier.CATEGORIES
    assert isinstance(result['confidence'], float)
    assert 0 <= result['confidence'] <= 100

def test_untrained_classifier():
    classifier = DocumentClassifier()
    
    result = classifier.classify_text("some text")
    assert result['error'] == 'Classifier not trained'
    assert result['category'] is None
    assert result['confidence'] == 0.0

def test_category_keywords():
    classifier = DocumentClassifier()
    
    # 训练数据
    training_data = [
        {
            'text': 'quarterly financial report revenue growth profit',
            'category': 'business'
        },
        {
            'text': 'python programming code development software',
            'category': 'technical'
        }
    ]
    
    classifier.train(training_data)
    
    keywords = classifier.get_category_keywords()
    assert isinstance(keywords, dict)
    assert len(keywords) > 0
    
    # 检查每个类别是否有关键词
    for category in classifier.CATEGORIES:
        if category in ['business', 'technical']:
            assert category in keywords
            assert isinstance(keywords[category], list)
            assert len(keywords[category]) > 0

def test_category_suggestion():
    classifier = DocumentClassifier()
    
    # 训练数据
    training_data = [
        {
            'text': 'financial report revenue profit',
            'category': 'business'
        },
        {
            'text': 'code development software engineering',
            'category': 'technical'
        }
    ]
    
    classifier.train(training_data)
    
    # 测试关键词建议
    keywords = ['revenue', 'profit', 'quarterly']
    result = classifier.suggest_category(keywords)
    
    assert result['error'] is None
    assert 'suggestion' in result
    assert 'category' in result['suggestion']
    assert 'confidence' in result['suggestion']
    assert 'alternatives' in result['suggestion'] 