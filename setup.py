from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aidocgenius",
    version="0.1.0",
    author="jiangmuran",
    author_email="jmr@jiangmuran.com",
    description="一个强大的AI驱动的文档处理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiangmuran/AIDocGenius",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "python-docx>=0.8.11",
        "PyPDF2>=3.0.0",
        "markdown>=3.4.3",
        "googletrans>=3.1.0a0",
        "python-magic>=0.4.27",
        "nltk>=3.8.1",
        "spacy>=3.5.3",
        "fastapi>=0.95.2",
        "uvicorn>=0.22.0",
        "python-multipart>=0.0.6",
        "pydantic>=1.10.7",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "sphinx>=7.0.1",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
) 