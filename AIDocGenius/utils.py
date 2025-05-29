import os
from pathlib import Path
from typing import Union, Any
import json
import yaml
from docx import Document
import PyPDF2
import markdown
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_document(file_path: Union[str, Path]) -> str:
    """
    加载文档内容，支持多种格式
    
    Args:
        file_path: 文档路径
        
    Returns:
        str: 文档内容
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        elif suffix == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        elif suffix == '.docx':
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
        elif suffix == '.pdf':
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                return '\n'.join([page.extract_text() for page in pdf_reader.pages])
                
        elif suffix in ['.json', '.yaml', '.yml']:
            with open(file_path, 'r', encoding='utf-8') as f:
                if suffix == '.json':
                    return json.load(f)
                else:
                    return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
            
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        raise

def save_document(content: Any, file_path: Union[str, Path], format_options: dict = None) -> None:
    """
    保存文档内容
    
    Args:
        content: 要保存的内容
        file_path: 保存路径
        format_options: 格式选项
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == '.txt':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(content))
                
        elif suffix == '.md':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        elif suffix == '.docx':
            doc = Document()
            doc.add_paragraph(content)
            doc.save(file_path)
            
        elif suffix == '.pdf':
            # PDF generation requires additional libraries
            raise NotImplementedError("PDF generation not implemented yet")
            
        elif suffix in ['.json', '.yaml', '.yml']:
            with open(file_path, 'w', encoding='utf-8') as f:
                if suffix == '.json':
                    json.dump(content, f, ensure_ascii=False, indent=2)
                else:
                    yaml.safe_dump(content, f, allow_unicode=True)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
            
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {str(e)}")
        raise

def get_file_info(file_path: Union[str, Path]) -> dict:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        dict: 文件信息
    """
    file_path = Path(file_path)
    
    return {
        'name': file_path.name,
        'extension': file_path.suffix,
        'size': os.path.getsize(file_path),
        'created_time': os.path.getctime(file_path),
        'modified_time': os.path.getmtime(file_path),
        'is_binary': is_binary_file(file_path)
    }

def is_binary_file(file_path: Union[str, Path]) -> bool:
    """
    检查文件是否为二进制文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 是否为二进制文件
    """
    try:
        with open(file_path, 'tr') as f:
            f.read(1024)
            return False
    except:
        return True

def create_directory_if_not_exists(directory: Union[str, Path]) -> None:
    """
    如果目录不存在则创建
    
    Args:
        directory: 目录路径
    """
    Path(directory).mkdir(parents=True, exist_ok=True) 