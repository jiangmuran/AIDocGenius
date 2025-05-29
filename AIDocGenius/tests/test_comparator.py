import pytest
from aidocgenius.comparator import DocumentComparator

def test_compare_texts():
    comparator = DocumentComparator()
    
    text1 = """
    This is the first document.
    It contains some text for comparison.
    We will compare this with another document.
    """
    
    text2 = """
    This is the second document.
    It contains some text for testing.
    We will compare this with the first document.
    """
    
    result = comparator.compare_texts(text1, text2)
    
    assert 'similarity_score' in result
    assert 0 <= result['similarity_score'] <= 100
    assert isinstance(result['common_keywords'], list)
    assert 'differences' in result
    assert 'additions' in result['differences']
    assert 'deletions' in result['differences']
    assert 'changes' in result['differences']

def test_identical_texts():
    comparator = DocumentComparator()
    
    text = "This is a test document."
    result = comparator.compare_texts(text, text)
    
    assert result['similarity_score'] == 100
    assert result['differences']['additions'] == 0
    assert result['differences']['deletions'] == 0
    assert result['differences']['changes'] == 0

def test_completely_different_texts():
    comparator = DocumentComparator()
    
    text1 = "This is the first document."
    text2 = "Something completely different."
    
    result = comparator.compare_texts(text1, text2)
    
    assert result['similarity_score'] < 50
    assert len(result['common_keywords']) == 0

def test_document_comparison():
    comparator = DocumentComparator()
    
    # 测试无效文件路径
    result = comparator.compare_documents(
        "nonexistent1.txt",
        "nonexistent2.txt"
    )
    
    assert result['error'] is not None
    assert result['comparison'] is None 