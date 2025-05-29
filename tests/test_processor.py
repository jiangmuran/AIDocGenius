import pytest
from pathlib import Path
import tempfile
from aidocgenius import DocProcessor

@pytest.fixture
def processor():
    return DocProcessor()

@pytest.fixture
def sample_text():
    return """
    # 测试文档

    这是一个用于测试的示例文档。它包含多个段落和一些基本的格式。

    ## 第一部分

    这是第一部分的内容。这里有一些文本用于测试文档处理功能。

    ## 第二部分

    这是第二部分的内容。我们将测试以下功能：
    1. 文档摘要
    2. 文档翻译
    3. 文档分析
    4. 格式转换
    """

@pytest.fixture
def temp_markdown_file(sample_text):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(sample_text)
        return Path(f.name)

def test_summary_generation(processor, temp_markdown_file):
    summary = processor.generate_summary(temp_markdown_file)
    assert summary
    assert isinstance(summary, str)
    assert len(summary) < len(open(temp_markdown_file, encoding='utf-8').read())

def test_translation(processor, temp_markdown_file):
    translation = processor.translate(temp_markdown_file, target_language='en')
    assert translation
    assert isinstance(translation, str)
    assert 'test' in translation.lower()  # 假设翻译后的文本包含"test"

def test_document_analysis(processor, temp_markdown_file):
    analysis = processor.analyze(temp_markdown_file)
    assert analysis
    assert isinstance(analysis, dict)
    assert 'readability' in analysis
    assert 'structure' in analysis
    assert 'keywords' in analysis
    assert 'statistics' in analysis

def test_format_conversion(processor, temp_markdown_file):
    output_file = Path(temp_markdown_file).with_suffix('.txt')
    processor.convert(temp_markdown_file, output_file)
    assert output_file.exists()
    content = output_file.read_text(encoding='utf-8')
    assert content
    output_file.unlink()

def test_batch_processing(processor, temp_markdown_file):
    operations = ['summarize', 'analyze']
    results = processor.batch_process(
        temp_markdown_file.parent,
        temp_markdown_file.parent,
        operations
    )
    assert results
    assert isinstance(results, dict)
    assert str(temp_markdown_file) in results

def test_invalid_file(processor):
    with pytest.raises(Exception):
        processor.generate_summary('nonexistent.txt')

def test_invalid_language(processor, temp_markdown_file):
    with pytest.raises(ValueError):
        processor.translate(temp_markdown_file, target_language='invalid') 