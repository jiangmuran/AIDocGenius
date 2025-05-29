import argparse
import sys
from pathlib import Path
from .processor import DocProcessor
from .utils import logger

def main():
    parser = argparse.ArgumentParser(description="AIDocGenius - AI驱动的文档处理工具")
    parser.add_argument("command", choices=["summarize", "translate", "analyze", "convert"],
                      help="要执行的命令")
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--target-lang", "-t", help="目标语言代码")
    parser.add_argument("--source-lang", "-s", help="源语言代码")
    parser.add_argument("--max-length", type=int, help="摘要最大长度")
    parser.add_argument("--min-length", type=int, help="摘要最小长度")
    parser.add_argument("--format-options", help="格式选项（JSON字符串）")
    
    args = parser.parse_args()
    
    try:
        processor = DocProcessor()
        
        if args.command == "summarize":
            summary = processor.generate_summary(
                args.input,
                max_length=args.max_length,
                min_length=args.min_length
            )
            print(summary)
            
        elif args.command == "translate":
            if not args.target_lang:
                parser.error("翻译命令需要指定目标语言")
            translation = processor.translate(
                args.input,
                target_language=args.target_lang,
                source_language=args.source_lang
            )
            print(translation)
            
        elif args.command == "analyze":
            analysis = processor.analyze(args.input)
            print("\n=== 文档分析报告 ===")
            print(f"\n可读性分析:")
            print(f"评分: {analysis['readability']['score']}")
            print(f"建议: {analysis['readability']['suggestion']}")
            
            print(f"\n文档结构:")
            print(f"段落数: {analysis['structure']['paragraph_count']}")
            print(f"句子数: {analysis['structure']['sentence_count']}")
            print(f"结构评分: {analysis['structure']['structure_score']}")
            
            print(f"\n关键词:")
            for kw in analysis['keywords'][:5]:
                print(f"- {kw['word']}: {kw['frequency']}次")
                
            print(f"\n统计信息:")
            stats = analysis['statistics']
            print(f"字符数: {stats['char_count']}")
            print(f"词数: {stats['word_count']}")
            print(f"平均句长: {stats['avg_word_per_sentence']}词")
            
        elif args.command == "convert":
            if not args.output:
                parser.error("转换命令需要指定输出文件路径")
            processor.convert(args.input, args.output)
            print(f"已将文件转换并保存到: {args.output}")
            
    except Exception as e:
        logger.error(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 