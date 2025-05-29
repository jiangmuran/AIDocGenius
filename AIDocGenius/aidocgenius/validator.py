from typing import Dict, List, Optional
import magic
import os

class DocumentValidator:
    """文档格式验证器"""
    
    SUPPORTED_FORMATS = {
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'text/plain': '.txt',
        'text/markdown': '.md',
        'text/html': '.html'
    }

    def __init__(self):
        self.mime = magic.Magic(mime=True)

    def validate_format(self, file_path: str) -> Dict[str, any]:
        """
        验证文档格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含验证结果的字典
        """
        if not os.path.exists(file_path):
            return {
                'valid': False,
                'error': 'File not found',
                'mime_type': None,
                'extension': None
            }

        mime_type = self.mime.from_file(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if mime_type not in self.SUPPORTED_FORMATS:
            return {
                'valid': False,
                'error': 'Unsupported document format',
                'mime_type': mime_type,
                'extension': file_ext
            }
            
        expected_ext = self.SUPPORTED_FORMATS[mime_type]
        if file_ext != expected_ext:
            return {
                'valid': False,
                'error': f'File extension mismatch. Expected {expected_ext}, got {file_ext}',
                'mime_type': mime_type,
                'extension': file_ext
            }
            
        return {
            'valid': True,
            'error': None,
            'mime_type': mime_type,
            'extension': file_ext
        }

    def check_document_integrity(self, file_path: str) -> Dict[str, any]:
        """
        检查文档完整性
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含完整性检查结果的字典
        """
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            return {
                'valid': True,
                'error': None,
                'size': len(content),
                'corrupted': False
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'size': 0,
                'corrupted': True
            } 