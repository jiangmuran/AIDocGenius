"""
命令行接口模块
"""
import argparse
import sys
from typing import Optional, List

from . import __version__
from .processor import DocProcessor
from .exceptions import AIDocGeniusError
from .utils import load_config, save_document


def _parse_list(value: Optional[str]) -> Optional[List[str]]:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _load_processor(config_path: Optional[str]) -> DocProcessor:
    config = load_config(config_path)
    return DocProcessor(config=config)


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

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--config", "-c", help="配置文件路径 (json/yaml)")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 处理文档命令
    process_parser = subparsers.add_parser("process", help="处理文档", parents=[common_parser])
    process_parser.add_argument("input", help="输入文件路径")
    process_parser.add_argument("--output", "-o", help="输出文件路径")

    # 翻译命令
    translate_parser = subparsers.add_parser("translate", help="翻译文档", parents=[common_parser])
    translate_parser.add_argument("input", help="输入文件路径")
    translate_parser.add_argument("--output", "-o", help="输出文件路径")
    translate_parser.add_argument("--source", "-s", help="源语言代码", default="auto")
    translate_parser.add_argument("--target", "-t", help="目标语言代码", required=True)

    # 摘要命令
    summary_parser = subparsers.add_parser("summary", help="生成文档摘要", parents=[common_parser])
    summary_parser.add_argument("input", help="输入文件路径")
    summary_parser.add_argument("--output", "-o", help="输出文件路径")
    summary_parser.add_argument("--max-length", type=int, help="最大摘要长度")
    summary_parser.add_argument("--min-length", type=int, help="最小摘要长度")
    summary_parser.add_argument("--ratio", type=float, help="摘要比例 (0-1)")

    # 分析命令
    analyze_parser = subparsers.add_parser("analyze", help="分析文档", parents=[common_parser])
    analyze_parser.add_argument("input", help="输入文件路径")
    analyze_parser.add_argument("--output", "-o", help="输出文件路径")
    analyze_parser.add_argument("--criteria", help="分析维度，逗号分隔")

    # 转换命令
    convert_parser = subparsers.add_parser("convert", help="转换文档格式", parents=[common_parser])
    convert_parser.add_argument("input", help="输入文件路径")
    convert_parser.add_argument("output", help="输出文件路径")
    convert_parser.add_argument("--from-markdown", dest="from_markdown", action="store_true", default=True)
    convert_parser.add_argument("--no-from-markdown", dest="from_markdown", action="store_false")

    # 比较命令
    compare_parser = subparsers.add_parser("compare", help="比较文档", parents=[common_parser])
    compare_parser.add_argument("input1", help="第一个文档路径")
    compare_parser.add_argument("input2", help="第二个文档路径")
    compare_parser.add_argument("--output", "-o", help="输出文件路径")

    # 合并命令
    merge_parser = subparsers.add_parser("merge", help="合并文档", parents=[common_parser])
    merge_parser.add_argument("inputs", nargs='+', help="输入文件路径列表")
    merge_parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    merge_parser.add_argument("--smart", action="store_true", help="智能合并（去重）")

    # 批处理命令
    batch_parser = subparsers.add_parser("batch", help="批量处理", parents=[common_parser])
    batch_parser.add_argument("input_dir", help="输入目录")
    batch_parser.add_argument("output_dir", help="输出目录")
    batch_parser.add_argument("--operations", required=True, help="操作列表，逗号分隔")
    batch_parser.add_argument("--max-length", type=int, help="摘要最大长度")
    batch_parser.add_argument("--min-length", type=int, help="摘要最小长度")
    batch_parser.add_argument("--target-language", help="目标语言")
    batch_parser.add_argument("--source-language", help="源语言")
    batch_parser.add_argument("--output-format", help="转换输出格式")

    return parser


def process_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    result = processor.process_document(args.input, args.output)
    if not args.output:
        return str(result)
    return None


def translate_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    result = processor.translate(args.input, args.target, args.source)
    if args.output:
        save_document(result, args.output)
        return None
    return result


def summary_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    result = processor.generate_summary(
        args.input,
        max_length=args.max_length,
        min_length=args.min_length,
        ratio=args.ratio
    )
    if args.output:
        save_document(result, args.output)
        return None
    return result


def analyze_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    criteria = _parse_list(args.criteria)
    result = processor.analyze(args.input, criteria)
    if args.output:
        save_document(result, args.output)
        return None
    return str(result)


def convert_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    processor.convert(
        args.input,
        args.output,
        format_options={"from_markdown": args.from_markdown}
    )
    return None


def compare_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    result = processor.compare_documents(args.input1, args.input2)
    if args.output:
        save_document(result, args.output)
        return None
    return str(result)


def merge_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    processor.merge_documents(args.inputs, args.output, smart_merge=args.smart)
    return None


def batch_command(args: argparse.Namespace) -> Optional[str]:
    processor = _load_processor(args.config)
    operations = _parse_list(args.operations) or []
    result = processor.batch_process(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        operations=operations,
        max_length=args.max_length,
        min_length=args.min_length,
        target_language=args.target_language,
        source_language=args.source_language,
        output_format=args.output_format
    )
    return str(result)


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "process": process_command,
        "translate": translate_command,
        "summary": summary_command,
        "analyze": analyze_command,
        "convert": convert_command,
        "compare": compare_command,
        "merge": merge_command,
        "batch": batch_command
    }

    try:
        result = commands[args.command](args)
        if result:
            print(result)
    except AIDocGeniusError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
