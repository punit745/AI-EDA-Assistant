# 📊 AI-EDA Assistant

An intelligent, AI-driven Python application for automated Exploratory Data Analysis (EDA) and data preprocessing. This tool provides an intuitive interface for data scientists and analysts to perform comprehensive data analysis, visualization, and preprocessing tasks with minimal effort.

## 🌟 Features

### 1. **Multi-Format Data Support**
- Upload and parse multiple file formats: `.csv`, `.xlsx`, `.json`, `.txt`
- Automatic DataFrame conversion for standardized operations
- Smart delimiter detection for text files

### 2. **Interactive Web Interface**
- Built with Streamlit for an intuitive user experience
- Responsive design with organized navigation
- Real-time feedback and progress indicators

### 3. **Automated Exploratory Data Analysis**
- **Dataset Overview**: Size, columns, data types, missing values
- **Statistical Summaries**: Mean, median, std dev, skewness, kurtosis
- **Visualizations**: 
  - Histograms for distribution analysis
  - Box plots for outlier detection
  - Correlation heatmaps
  - Scatter matrices for feature relationships
  - Missing value visualizations

### 4. **Data Preprocessing**
- **Missing Value Handling**:
  - Fill with mean, median, or mode
  - Remove rows or columns with missing data
- **Outlier Detection & Handling**:
  - Z-score method
  - IQR (Interquartile Range) method
  - Options: remove, cap, or replace with median
- **Data Normalization**:
  - StandardScaler (mean=0, std=1)
  - MinMaxScaler (range 0-1)
  - RobustScaler (using median and IQR)

### 5. **Data Integrity Checks**
- Duplicate row detection and removal
- Data type consistency validation
- Date format validation
- Numerical data validation (infinites, negatives, zeros)
- Categorical data consistency checks

### 6. **Machine Learning Models**
- **Regression Models**:
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor
- **Performance Metrics**:
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - R² Score
  - Feature importance visualization

### 7. **Export & Reporting**
- **Download Processed Data**: CSV, Excel, JSON formats
- **Python Code Generation**: Reproducible scripts for all operations
- **PDF Reports**: Comprehensive analysis reports with:
  - Executive summary
  - Dataset information
  - Statistical summaries
  - Operations log

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

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

## 💻 Usage

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

1. **📊 Dataset Overview**: 
   - View basic statistics and data preview
   - Understand column types and missing values

2. **🔍 Automated EDA**:
   - Generate statistical summaries
   - Create interactive visualizations
   - Analyze distributions and correlations

3. **🧹 Preprocessing**:
   - Handle missing values
   - Detect and manage outliers
   - Normalize or scale features

4. **✅ Data Integrity**:
   - Check for duplicates
   - Validate data types
   - Ensure data consistency

5. **🤖 Model Training**:
   - Select features and target variable
   - Train regression models
   - Evaluate performance metrics

6. **💾 Export & Reports**:
   - Download processed datasets
   - Generate Python scripts
   - Create PDF reports

## 📦 Project Structure

```
AI-EDA-Assistant/
├── app.py                  # Main Streamlit application
├── data_handler.py         # File upload and parsing module
├── eda.py                  # EDA functionality and visualizations
├── preprocessing.py        # Data preprocessing operations
├── data_integrity.py       # Data validation and integrity checks
├── model_training.py       # Machine learning model training
├── code_generator.py       # Python code generation
├── report_generator.py     # PDF report generation
├── requirements.txt        # Project dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## 🛠️ Technology Stack

- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Machine Learning**: Scikit-learn, SciPy
- **Web Framework**: Streamlit
- **Report Generation**: FPDF2
- **File Handling**: openpyxl, xlrd

## 📊 Example Use Cases

1. **Data Quality Assessment**: Upload a dataset to quickly identify missing values, duplicates, and data type issues

2. **Feature Engineering**: Normalize features, handle outliers, and prepare data for machine learning

3. **Quick Model Prototyping**: Train and evaluate basic models without writing code

4. **Report Generation**: Create professional PDF reports for stakeholders

5. **Code Reproducibility**: Export Python scripts to reproduce analysis in production environments

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

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data visualization powered by [Plotly](https://plotly.com/)
- Machine learning with [Scikit-learn](https://scikit-learn.org/)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Happy Data Analyzing! 📊✨**
