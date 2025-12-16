# AI-EDA Assistant - User Guide

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/punit745/AI-EDA-Assistant.git
cd AI-EDA-Assistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Features Overview

### File Upload
- **Supported Formats**: CSV, Excel (.xlsx, .xls), JSON, TXT
- **Max File Size**: Depends on your system memory
- **Smart Detection**: Automatically detects delimiters in text files

### Dataset Overview
View comprehensive information about your dataset:
- Number of rows and columns
- Memory usage
- Duplicate rows
- Column data types
- Missing value statistics
- Data preview with adjustable row count

### Automated EDA
Perform exploratory data analysis with one click:

#### Statistical Summary
- Descriptive statistics for numerical columns
- Mean, median, std, variance, skewness, kurtosis
- Additional metrics beyond standard describe()

#### Categorical Summary
- Unique value counts
- Top values for each category
- Missing value counts

#### Visualizations
1. **Histograms**: Distribution of numerical features
2. **Box Plots**: Detect outliers and understand spread
3. **Correlation Heatmap**: Identify relationships between features
4. **Scatter Matrix**: Pairwise relationships (limited to 5 columns for performance)
5. **Missing Values Plot**: Visualize missing data patterns

### Data Preprocessing

#### Handle Missing Values
Choose from multiple strategies:
- **Mean**: Fill with column mean (numerical only)
- **Median**: Fill with column median (numerical only)
- **Mode**: Fill with most frequent value
- **Drop Rows**: Remove rows with missing values
- **Drop Columns**: Remove columns with missing values

Select specific columns or apply to all columns with missing data.

#### Handle Outliers
**Detection Methods**:
- **IQR (Interquartile Range)**: Industry standard, robust to extreme outliers
- **Z-score**: Statistical method using standard deviations

**Handling Strategies**:
- **Remove**: Delete rows containing outliers
- **Cap**: Clip values to acceptable range
- **Median**: Replace outliers with column median

#### Normalize/Scale Data
Choose the appropriate scaler for your use case:
- **Standard Scaler**: Mean=0, Std=1 (use for normally distributed data)
- **MinMax Scaler**: Range 0-1 (use when you need bounded values)
- **Robust Scaler**: Uses median and IQR (use with outliers)

### Data Integrity Checks

#### Duplicate Detection
- Identify duplicate rows
- View percentage of duplicates
- Remove duplicates with one click

#### Data Type Consistency
- Check for mixed types in columns
- Identify inconsistent data

#### Date Format Validation
- Validate date columns
- Detect common date formats
- Identify invalid date entries

#### Numerical Validation
- Check for infinite values
- Count negative, zero, and positive values
- Validate numerical ranges

#### Categorical Consistency
- Analyze cardinality ratios
- Detect case inconsistencies
- View top values per category

### Model Training

Train basic machine learning models without writing code:

#### Supported Models
1. **Linear Regression**: Simple and interpretable
2. **Decision Tree**: Non-linear relationships
3. **Random Forest**: Ensemble method, robust

#### Configuration
- Select target column
- Choose feature columns
- Set test size (10-50%)
- Configure model parameters (depth, estimators)

#### Evaluation Metrics
**Regression**:
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score

**Classification**:
- Accuracy
- Precision, Recall, F1-Score
- Feature importance visualization

### Export & Reports

#### Download Processed Data
Save your cleaned and processed data in multiple formats:
- **CSV**: Universal format
- **Excel**: Business-friendly format with sheets
- **JSON**: API-ready format

#### Python Code Export
Generate reproducible Python scripts:
- All operations logged
- Complete with imports
- Ready to run independently
- Maintains operation order

#### PDF Reports
Create professional reports containing:
- Executive summary
- Dataset information
- Column statistics
- Missing value analysis
- Statistical summaries
- Operations log

## Best Practices

### 1. Data Loading
- Start with clean file names (no special characters)
- Ensure consistent column names
- Check encoding (UTF-8 recommended)

### 2. Exploratory Analysis
- Always start with Dataset Overview
- Review statistical summaries before preprocessing
- Check for missing values and outliers

### 3. Preprocessing Pipeline
Recommended order:
1. Handle duplicates
2. Handle missing values
3. Handle outliers
4. Normalize/scale data

### 4. Model Training
- Select relevant features (avoid highly correlated features)
- Start with simple models (Linear Regression)
- Use at least 100 samples for reliable results
- Check for overfitting (train vs test scores)

### 5. Export
- Download data after major preprocessing steps
- Generate Python code for reproducibility
- Create PDF reports for stakeholders

## Troubleshooting

### Common Issues

#### File Upload Errors
- **Solution**: Check file format and encoding
- Try saving as CSV with UTF-8 encoding
- Remove special characters from file name

#### Memory Errors
- **Solution**: Use smaller datasets or sample your data
- Close other applications
- Increase available RAM

#### Visualization Not Showing
- **Solution**: Ensure numerical columns exist
- Check for at least 2 columns for correlation plots
- Refresh the page if needed

#### Model Training Fails
- **Solution**: Ensure target column is numerical
- Remove rows with missing values in features/target
- Use at least 2 feature columns

## Tips for Best Results

1. **Start Small**: Test with a sample of your data first
2. **Save Often**: Download intermediate results
3. **Document**: Use the operations log to track changes
4. **Validate**: Check data after each preprocessing step
5. **Iterate**: Run multiple analyses with different parameters

## Example Workflow

### Complete Analysis Example

```
1. Upload Data
   └─ Load customer_data.csv

2. Dataset Overview
   └─ 1000 rows, 10 columns, 5% missing

3. Automated EDA
   ├─ Statistical summary: identify skewed features
   ├─ Correlation heatmap: find related features
   └─ Missing values plot: visualize patterns

4. Preprocessing
   ├─ Remove duplicates (10 found)
   ├─ Handle missing values (mean for numerical)
   ├─ Handle outliers (IQR method, cap strategy)
   └─ Normalize data (StandardScaler)

5. Model Training
   ├─ Target: purchase_amount
   ├─ Features: age, income, credit_score
   ├─ Model: Random Forest
   └─ R² Score: 0.85

6. Export
   ├─ Download processed CSV
   ├─ Generate Python script
   └─ Create PDF report
```

## Keyboard Shortcuts

- **Ctrl/Cmd + R**: Reload data
- **Ctrl/Cmd + S**: Download current data
- **Escape**: Close modals/popups

## Support and Feedback

For issues or questions:
- Open an issue on GitHub
- Check documentation
- Review example notebooks

## Version Information

- **Version**: 1.0.0
- **Last Updated**: December 2024
- **Python**: 3.8+
- **Streamlit**: 1.28+

---

**Happy Analyzing! 📊**
