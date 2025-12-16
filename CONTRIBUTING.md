# Contributing to AI-EDA Assistant

First off, thank you for considering contributing to AI-EDA Assistant! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to fostering an open and welcoming environment. Be respectful, professional, and considerate of others.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (sample data, screenshots)
- **Describe the behavior you observed and what you expected**
- **Include details about your environment** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions you've considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, commented code
3. **Follow the existing code style** (PEP 8 for Python)
4. **Add tests** if applicable
5. **Update documentation** as needed
6. **Write a clear commit message**

#### Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Write descriptive commit messages
- Update the README.md if needed
- Add yourself to the contributors list

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI-EDA-Assistant.git
cd AI-EDA-Assistant

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

## Code Style

### Python Style Guide

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Maximum line length: 100 characters

### Example

```python
def calculate_statistics(df: pd.DataFrame, columns: List[str]) -> Dict:
    """
    Calculate statistical measures for specified columns.
    
    Args:
        df: Input DataFrame
        columns: List of column names to analyze
        
    Returns:
        Dict: Statistical measures for each column
    """
    stats = {}
    for col in columns:
        stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median()
        }
    return stats
```

### Code Formatting

Use Black for code formatting:
```bash
black .
```

Use flake8 for linting:
```bash
flake8 .
```

## Testing

### Running Tests

```bash
pytest tests/
```

### Writing Tests

- Write tests for new features
- Ensure tests are independent
- Use descriptive test names
- Cover edge cases

Example:
```python
def test_handle_missing_values_with_mean():
    """Test missing value handling with mean strategy."""
    df = pd.DataFrame({'col1': [1, 2, None, 4]})
    preprocessor = Preprocessor(df)
    result = preprocessor.handle_missing_values(strategy='mean')
    assert result['col1'].isnull().sum() == 0
```

## Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Update USER_GUIDE.md for new features
- Include inline comments for complex logic

## Project Structure

```
AI-EDA-Assistant/
├── app.py                  # Main Streamlit app
├── data_handler.py         # Data loading
├── eda.py                  # EDA functionality
├── preprocessing.py        # Preprocessing operations
├── data_integrity.py       # Data validation
├── model_training.py       # ML model training
├── code_generator.py       # Code export
├── report_generator.py     # PDF reports
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
└── tests/                 # Test files
```

## Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples
```
feat(eda): add scatter matrix visualization

Add scatter matrix plot for analyzing pairwise relationships
between numerical features. Limited to 5 columns for performance.

Closes #123
```

```
fix(preprocessing): handle edge case in outlier detection

Fix issue where IQR calculation failed on columns with
single unique value.

Fixes #456
```

## Review Process

1. **Automated checks** must pass (linting, tests)
2. **Code review** by maintainers
3. **Documentation review** if applicable
4. **Merge** when approved

## Feature Requests

We track feature requests as GitHub issues. To request a feature:

1. Check if the feature already exists
2. Open a new issue with the "enhancement" label
3. Describe the feature clearly
4. Explain the use case
5. Be patient - we'll review all requests

## Questions?

Feel free to ask questions by:
- Opening a GitHub issue
- Starting a discussion
- Contacting the maintainers

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
