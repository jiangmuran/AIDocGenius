from aidocgenius import DocProcessor

def main():
    # 初始化文档处理器
    processor = DocProcessor()
    
    # 示例文本
    sample_text = """
    北冥有鱼，其名为昆
    """
    
    # 保存示例文本
    with open("sample.md", "w", encoding="utf-8") as f:
        f.write(sample_text)
        
    print("1. 生成文档摘要")
    summary = processor.generate_summary("sample.md")
    print(f"摘要：\n{summary}\n")
    
    print("2. 翻译文档")
    translation = processor.translate("sample.md", target_language="en")
    print(f"英文翻译：\n{translation}\n")
    
    print("3. 分析文档")
    analysis = processor.analyze("sample.md")
    print("文档分析结果：")
    print(f"可读性评分：{analysis['readability']['score']}")
    print(f"建议：{analysis['readability']['suggestion']}")
    print(f"关键词：{', '.join(k['word'] for k in analysis['keywords'])}\n")
    
    print("4. 转换格式")
    # 转换为不同格式
    processor.convert("sample.md", "output.docx")
    processor.convert("sample.md", "output.html", {"from_markdown": True})
    
    print("文档处理完成！输出文件已保存。")

if __name__ == "__main__":
    main() 