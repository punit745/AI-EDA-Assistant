# 📊 AI-EDA Assistant

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent, AI-driven Python application for automated Exploratory Data Analysis (EDA) and data preprocessing with AI-powered insights, theme customization, and multi-file analysis capabilities.

---

## 🚀 Quick Links

- [Installation](#-installation)
- [Usage](#-usage)
- [Features](#-features)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Features

### 🎨 **NEW: Theme Customization**
- **Dark/Light Mode Toggle**: Switch between professional dark and light themes
- **Minimalist Design**: Clean, elegant interface following modern design principles
- **Responsive Layout**: Works seamlessly across desktop, tablet, and mobile devices

### 🤖 **NEW: AI-Powered Insights**
- **Data Health Scoring**: Comprehensive data quality assessment with grading system
- **Smart Recommendations**: Automated suggestions for data preprocessing
- **Correlation Insights**: Intelligent analysis of feature relationships
- **Feature Importance Hints**: Automatic detection of high-value features
- **Chart Recommendations**: AI-suggested visualizations based on data types
- **Automated Insights**: Context-aware explanations for all visualizations

### 📂 **NEW: Multi-File Analysis**
- **Upload Multiple Datasets**: Compare and analyze multiple files simultaneously
- **Schema Comparison**: Side-by-side comparison of dataset structures
- **Relationship Detection**: Automatic identification of join opportunities
- **Merge & Join**: Intelligent data merging with visual guidance
- **Aggregation Analysis**: Cross-dataset aggregation and analysis
- **Comparative Visualizations**: Compare metrics across multiple datasets

### 1. **Multi-Format Data Support**
- Upload and parse multiple file formats: `.csv`, `.xlsx`, `.json`, `.txt`
- Automatic DataFrame conversion for standardized operations
- Smart delimiter detection for text files
- Support for single or multiple file uploads

### 2. **Interactive Web Interface**
- Built with Streamlit for an intuitive user experience
- Responsive design with organized navigation
- Real-time feedback and progress indicators
- Smooth animations and transitions

### 3. **Automated Exploratory Data Analysis**
- **Dataset Overview**: Size, columns, data types, missing values
- **Statistical Summaries**: Mean, median, std dev, skewness, kurtosis
- **Interactive Visualizations**: 
  - Histograms for distribution analysis
  - Box plots for outlier detection
  - Correlation heatmaps with insights
  - Scatter matrices for feature relationships
  - Missing value visualizations
- **Automated Insights**: AI-generated explanations for visualizations

### 4. **Advanced Statistical Analysis Suite**
- **Descriptive Statistics**: 
  - Comprehensive metrics: mean, median, mode, min, max, std, variance
  - Skewness, kurtosis, quantiles, IQR, coefficient of variation
  - Multi-column selection and export
- **Inferential Statistics**:
  - Independent and one-sample t-tests
  - ANOVA (Analysis of Variance)
  - Chi-square test of independence
  - Confidence interval calculations
- **Correlation & Causality Analysis**:
  - Pearson, Spearman, and Kendall correlations
  - Interactive correlation heatmaps
  - Pairwise correlation matrices
  - Granger causality test for time series
- **Time Series Analysis**:
  - Seasonal decomposition (additive/multiplicative)
  - Stationarity testing (Augmented Dickey-Fuller)
  - Autocorrelation (ACF) and Partial Autocorrelation (PACF)
  - Trend and seasonal component identification
- **Probability Analysis**:
  - Distribution fitting (Normal, Exponential, Gamma, Log-Normal)
  - Goodness-of-fit testing (Kolmogorov-Smirnov)
  - Probability density function visualization
  - Expected values and probability statistics

### 5. **Data Preprocessing**
- **Missing Value Handling**:
  - Fill with mean, median, or mode
  - Remove rows or columns with missing data
  - AI-recommended strategies
- **Outlier Detection & Handling**:
  - Z-score method
  - IQR (Interquartile Range) method
  - Options: remove, cap, or replace with median
- **Data Normalization**:
  - StandardScaler (mean=0, std=1)
  - MinMaxScaler (range 0-1)
  - RobustScaler (using median and IQR)

### 6. **Data Integrity Checks**
- Duplicate row detection and removal
- Data type consistency validation
- Date format validation
- Numerical data validation (infinites, negatives, zeros)
- Categorical data consistency checks

### 7. **Expanded Machine Learning Models**
- **Regression Models**:
  - Linear Regression
  - Ridge Regression (L2 regularization)
  - Lasso Regression (L1 regularization)
  - Support Vector Regression (SVR)
  - K-Nearest Neighbors (KNN) Regressor
  - Decision Tree Regressor
  - Random Forest Regressor
- **Classification Models**:
  - Logistic Regression
  - Support Vector Classification (SVC)
  - K-Nearest Neighbors (KNN) Classifier
  - Decision Tree Classifier
  - Random Forest Classifier
- **Gradient Boosting Models**:
  - XGBoost (eXtreme Gradient Boosting)
  - LightGBM (Light Gradient Boosting Machine)
  - CatBoost (Categorical Boosting)
- **Time Series Models**:
  - ARIMA (AutoRegressive Integrated Moving Average)
  - Facebook Prophet
- **Advanced Features**:
  - Multi-model training and comparison
  - Hyperparameter tuning controls
  - Model performance comparison
  - Feature importance visualization
- **Performance Metrics**:
  - Regression: RMSE, MAE, R² Score
  - Classification: Accuracy, Precision, Recall, F1-Score

### 8. **Export & Reporting**
- **Download Processed Data**: CSV, Excel, JSON formats
- **Python Code Generation**: Reproducible scripts for all operations including:
  - Statistical analysis code
  - Model training code (including gradient boosting)
  - Data preprocessing operations
- **PDF Reports**: Comprehensive analysis reports with:
  - Executive summary
  - Dataset information
  - Statistical summaries
  - Operations log

### 9. **Performance Optimization**
- **Caching**: Intelligent caching for faster repeated operations
- **Lazy Loading**: Efficient memory management for large datasets
- **Optimized Computations**: Fast algorithms for statistical operations
- **Configurable Limits**: Adjustable upload size (up to 200MB)

---

## 🎯 What's New in This Version

### Major Enhancements:

1. **🎨 Theme Toggle**: Switch between dark and light professional themes
2. **🤖 AI Insights**: Automated data health scoring and smart recommendations
3. **📂 Multi-File Analysis**: Compare and merge multiple datasets
4. **💡 Smart Recommendations**: AI-powered preprocessing suggestions
5. **📊 Enhanced Visualizations**: Interactive Plotly charts with automated insights
6. **⚡ Performance**: Caching and optimization for faster operations

---

> **📖 For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone the repository**:
```bash
git clone https://github.com/punit745/AI-EDA-Assistant.git
cd AI-EDA-Assistant
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
streamlit run app.py
```

5. **Open browser** and navigate to `http://localhost:8501`

## 💻 Usage

### Using the Demo Dataset

A demo customer dataset (`demo_customer_data.csv`) is included with:
- 205 rows of realistic customer data
- Missing values, outliers, and duplicates for testing
- 11 columns (numeric and categorical)

**See [DEMO_DATA_README.md](DEMO_DATA_README.md) for dataset details.**

### Running the Application

1. **Start the Streamlit app**:
```bash
streamlit run app.py
```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Upload your dataset** using the file uploader in the sidebar

4. **Explore features**:
   - Navigate between different tasks using the sidebar menu
   - Follow the intuitive workflow from data overview to export

### Workflow

1. **🏠 Home**: 
   - Learn about the application features
   - Understand the workflow

2. **📊 Dataset Overview**: 
   - View basic statistics and data preview
   - Understand column types and missing values

3. **🤖 AI Insights** ⭐ NEW:
   - Get data health score and recommendations
   - View correlation insights
   - Receive smart preprocessing suggestions
   - Get chart recommendations

4. **🔍 Automated EDA**:
   - Generate statistical summaries
   - Create interactive visualizations with insights
   - Analyze distributions and correlations

5. **📈 Statistical Analysis**:
   - Perform descriptive statistics
   - Run inferential tests (t-tests, ANOVA, chi-square)
   - Analyze correlations and causality
   - Conduct time series analysis
   - Fit probability distributions

6. **🧹 Preprocessing**:
   - Handle missing values
   - Detect and manage outliers
   - Normalize or scale features

7. **✅ Data Integrity**:
   - Check for duplicates
   - Validate data types
   - Ensure data consistency

8. **🎯 Model Training**:
   - Select multiple models for comparison
   - Train regression, classification, gradient boosting, or time series models
   - Fine-tune hyperparameters
   - Compare model performance
   - Visualize feature importance

9. **📂 Multi-File Analysis** ⭐ NEW:
   - Upload multiple datasets
   - Compare schemas and statistics
   - Detect potential relationships
   - Merge and join datasets
   - Perform aggregation analysis

10. **💾 Export & Reports**:
    - Download processed datasets
    - Generate Python scripts (including new models)
    - Create PDF reports

## 📦 Project Structure

```
AI-EDA-Assistant/
├── app.py                      # Main Streamlit application
├── data_handler.py             # File upload and parsing module
├── eda.py                      # EDA functionality and visualizations
├── statistical_analysis.py     # Advanced statistical analysis
├── ai_insights.py              # AI-powered insights and recommendations ⭐ NEW
├── multi_file_analyzer.py      # Multi-file analysis module ⭐ NEW
├── preprocessing.py            # Data preprocessing operations
├── data_integrity.py           # Data validation and integrity checks
├── model_training.py           # ML model training (expanded)
├── code_generator.py           # Python code generation
├── report_generator.py         # PDF report generation
├── cache_utils.py              # Caching utilities for performance ⭐ NEW
├── utils.py                    # Utility functions
├── style.css                   # Dark theme CSS
├── style_light.css             # Light theme CSS ⭐ NEW
├── requirements.txt            # Project dependencies (updated)
├── .streamlit/
│   └── config.toml            # Streamlit configuration (enhanced)
├── .gitignore                 # Git ignore file
└── README.md                  # Project documentation
```

## 🛠️ Technology Stack

- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Machine Learning**: Scikit-learn, SciPy
- **Gradient Boosting**: XGBoost, LightGBM, CatBoost ⭐ NEW
- **Statistical Analysis**: Statsmodels ⭐ NEW
- **Time Series**: ARIMA, Facebook Prophet ⭐ NEW
- **Web Framework**: Streamlit
- **Report Generation**: FPDF2
- **File Handling**: openpyxl, xlrd

## 📊 Example Use Cases

1. **Data Quality Assessment**: Upload datasets to get AI-powered health scores and recommendations

2. **Multi-Dataset Comparison**: Compare sales data across regions or time periods

3. **Feature Engineering**: Get smart preprocessing suggestions and implement them with one click

4. **Quick Model Prototyping**: Train and compare multiple models simultaneously

5. **Report Generation**: Create professional PDF reports with automated insights for stakeholders

6. **Code Reproducibility**: Export Python scripts to reproduce analysis in production environments

7. **Data Merging**: Intelligently merge customer and transaction data with relationship detection

## 🌐 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Heroku

1. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```

2. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t ai-eda-assistant .
docker run -p 8501:8501 ai-eda-assistant
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 📚 Documentation

- **[User Guide](USER_GUIDE.md)**: Comprehensive guide on using all features
- **[Quick Start](QUICKSTART.md)**: Quick reference for common tasks
- **[Examples](EXAMPLES.md)**: Sample datasets and workflows
- **[Project Summary](PROJECT_SUMMARY.md)**: Complete implementation overview

## 🎯 Project Status

- **Version**: 1.0.0
- **Status**: ✅ Production Ready
- **Features**: 11/11 Core Features Implemented
- **Security**: ✅ No Vulnerabilities
- **Test Status**: ✅ All Tests Passing

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data visualization powered by [Plotly](https://plotly.com/)
- Machine learning with [Scikit-learn](https://scikit-learn.org/)
- PDF generation with [FPDF2](https://github.com/py-pdf/fpdf2)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

**Happy Data Analyzing! 📊✨**
