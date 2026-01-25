#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example 1: Document Summary Generation
Demonstrates how to use AIDocGenius to generate document summaries
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from AIDocGenius import DocProcessor

def main():
    """Document summary generation example"""
    print("=" * 60)
    print("Example 1: Document Summary Generation")
    print("=" * 60)
    
    # Create processor instance
    processor = DocProcessor()
    
    # Create sample document
    sample_text = """
    Deep learning is a branch of machine learning based on artificial neural 
    networks, particularly utilizing multi-layer neural networks for learning 
    and processing. The concept of deep learning stems from research on 
    artificial neural networks, and a multi-layer perceptron with multiple 
    layers is a type of deep learning structure.
    
    Deep learning has achieved major breakthroughs in image recognition, 
    speech recognition, and natural language processing. Convolutional Neural 
    Networks (CNN) excel in image processing, Recurrent Neural Networks (RNN) 
    have unique advantages in sequential data processing, while the Transformer 
    architecture has driven revolutionary progress in natural language processing.
    
    Modern deep learning frameworks like TensorFlow and PyTorch enable 
    researchers and engineers to more easily build and train complex neural 
    network models. These tools provide features like automatic differentiation 
    and GPU acceleration, greatly improving deep learning development efficiency 
    and model training speed.
    """
    
    # Save sample document
    sample_file = Path("sample_document.txt")
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print(f"\n✓ Created sample document: {sample_file}")
    print(f"✓ Document length: {len(sample_text)} characters")
    
    # Generate short summary
    print("\n" + "-" * 60)
    print("Generating short summary (max 100 characters):")
    print("-" * 60)
    short_summary = processor.generate_summary(
        sample_file,
        max_length=100
    )
    print(short_summary)
    
    # Generate medium length summary
    print("\n" + "-" * 60)
    print("Generating medium summary (max 200 characters):")
    print("-" * 60)
    medium_summary = processor.generate_summary(
        sample_file,
        max_length=200
    )
    print(medium_summary)
    
    # Cleanup
    sample_file.unlink()
    print("\n" + "=" * 60)
    print("✓ Example completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
