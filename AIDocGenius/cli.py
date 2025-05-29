"""
命令行接口模块
"""
import argparse
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .processor import DocProcessor
from .translator import Translator
from .summarizer import Summarizer
from .exceptions import AIDocGeniusError

def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="AIDocGenius - 智能文档处理助手",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"AIDocGenius v{__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 处理文档命令
    process_parser = subparsers.add_parser("process", help="处理文档")
    process_parser.add_argument("input", help="输入文件路径")
    process_parser.add_argument("--output", "-o", help="输出文件路径")
    process_parser.add_argument("--config", "-c", help="配置文件路径")
    
    # 翻译命令
    translate_parser = subparsers.add_parser("translate", help="翻译文档")
    translate_parser.add_argument("input", help="输入文件路径")
    translate_parser.add_argument("--output", "-o", help="输出文件路径")
    translate_parser.add_argument("--source", "-s", help="源语言代码", default="auto")
    translate_parser.add_argument("--target", "-t", help="目标语言代码", required=True)
    
    # 摘要命令
    summary_parser = subparsers.add_parser("summary", help="生成文档摘要")
    summary_parser.add_argument("input", help="输入文件路径")
    summary_parser.add_argument("--output", "-o", help="输出文件路径")
    summary_parser.add_argument("--max-length", type=int, help="最大摘要长度")
    summary_parser.add_argument("--min-length", type=int, help="最小摘要长度")
    
    return parser

def process_command(args: argparse.Namespace) -> Optional[str]:
    """处理文档命令"""
    processor = DocProcessor()
    try:
        result = processor.process_document(args.input, args.output)
        if not args.output:
            return str(result)
    except AIDocGeniusError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

def translate_command(args: argparse.Namespace) -> Optional[str]:
    """翻译命令"""
    translator = Translator()
    try:
        if args.output:
            translator.translate_file(args.input, args.output, args.source, args.target)
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
            return translator.translate(content, args.source, args.target)
    except AIDocGeniusError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

def summary_command(args: argparse.Namespace) -> Optional[str]:
    """摘要命令"""
    summarizer = Summarizer()
    try:
        return summarizer.generate_file_summary(
            args.input,
            args.output,
            max_length=args.max_length,
            min_length=args.min_length
        )
    except AIDocGeniusError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 命令映射
    commands = {
        "process": process_command,
        "translate": translate_command,
        "summary": summary_command
    }
    
    # 执行命令
    result = commands[args.command](args)
    if result:
        print(result)

if __name__ == "__main__":
    main() 