# Contributing to AIDocGenius

Thank you for your interest in contributing to AIDocGenius! This document provides guidelines for contributing to the project.

[中文版本](docs/CONTRIBUTING_CN.md)

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Python version and OS
- Any relevant logs or screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- A clear and descriptive title
- Detailed description of the proposed feature
- Examples of how the feature would be used
- Any alternative solutions considered

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure tests pass: `python test_basic.py`
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Add docstrings for functions and classes
- Write clear commit messages
- Keep functions focused and modular
- Add comments for complex logic

### Testing

Before submitting a pull request, ensure:

- All existing tests pass
- New features have corresponding tests
- Code coverage is maintained or improved

Run tests with:
```bash
python test_basic.py
```

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update examples if changing API
- Keep documentation clear and concise

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python test_basic.py
```

4. Start development server:
```bash
python app.py
```

## Code Review Process

- All submissions require review
- Reviewers may request changes
- Once approved, maintainers will merge
- Keep PRs focused on a single feature/fix

## Community

- Be respectful and constructive
- Help others in discussions
- Share your use cases and examples
- Report security issues privately

## Questions?

Feel free to:
- Open an issue for questions
- Email: jmr@jiangmuran.com
- Check existing documentation

Thank you for contributing! 🎉
