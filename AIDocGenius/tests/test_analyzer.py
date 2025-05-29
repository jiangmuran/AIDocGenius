import pytest
from aidocgenius.analyzer import DocumentAnalyzer

def test_analyze_text():
    analyzer = DocumentAnalyzer()
    text = """
    This is a sample text for testing. It contains multiple sentences and words.
    We will use this text to test our document analyzer functionality.
    The analyzer should be able to count words, sentences, and calculate readability scores.
    """
    
    result = analyzer.analyze_text(text)
    
    assert result['word_count'] > 0
    assert result['sentence_count'] == 3
    assert result['unique_words'] > 0
    assert 0 <= result['readability_score'] <= 100
    assert isinstance(result['top_words'], dict)
    assert len(result['top_words']) <= 10

def test_empty_text():
    analyzer = DocumentAnalyzer()
    result = analyzer.analyze_text("")
    
    assert result['word_count'] == 0
    assert result['sentence_count'] == 0
    assert result['unique_words'] == 0
    assert result['readability_score'] == 0
    assert len(result['top_words']) == 0

def test_syllable_counting():
    analyzer = DocumentAnalyzer()
    
    test_cases = {
        'hello': 2,
        'world': 1,
        'beautiful': 3,
        'example': 3,
        'test': 1
    }
    
    for word, expected in test_cases.items():
        assert analyzer._count_syllables(word) == expected

def test_text_extraction():
    analyzer = DocumentAnalyzer()
    
    # 测试无效文件路径
    result = analyzer.analyze_document("nonexistent_file.pdf")
    assert result['error'] is not None
    assert result['analysis'] is None 