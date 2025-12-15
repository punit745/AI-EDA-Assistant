# 🚀 Quick Setup Guide - AI-EDA Assistant

## Running the Project Locally

Follow these simple steps to run the AI-EDA Assistant on your local system:

### Step 1: Prerequisites

Make sure you have the following installed:
- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning the repository)

To check your Python version:
```bash
python --version
# or
python3 --version
```

### Step 2: Get the Project

**Option A: Clone from GitHub**
```bash
git clone https://github.com/punit745/AI-EDA-Assistant.git
cd AI-EDA-Assistant
```

**Option B: Download ZIP**
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in the extracted folder

### Step 3: Create Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages (~50MB download). It may take 1-2 minutes.

### Step 5: Run the Application

```bash
streamlit run app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Step 6: Open in Browser

The application should automatically open in your default browser. If not, manually open:
- **http://localhost:8501**

---

## 📁 Using the Demo Dataset

A demo dataset (`demo_customer_data.csv`) is included in the project with:
- **205 rows** of customer data
- **11 columns** (numeric and categorical)
- **25 missing values** for testing preprocessing
- **5 duplicate rows** for testing data integrity
- **8 outliers** for testing outlier detection

### How to Use the Demo File:

1. **Start the application** (Step 5 above)
2. In the sidebar, click **"Browse files"**
3. Navigate to the project folder
4. Select **`demo_customer_data.csv`**
5. Click **"Open"**

The data will load automatically!

### Demo Workflow:

1. **📊 Dataset Overview**: Check basic statistics
2. **🔍 Automated EDA**: 
   - View statistical summaries
   - Create histograms for age, income, purchase_amount
   - Generate correlation heatmap
   - Check missing values plot
3. **🧹 Preprocessing**:
   - Handle missing values (try "mean" for numeric columns)
   - Detect outliers (use IQR method)
   - Normalize data (StandardScaler)
4. **✅ Data Integrity**:
   - Remove the 5 duplicate rows
   - Check data type consistency
5. **🤖 Model Training** (optional):
   - Target: `purchase_amount`
   - Features: `age`, `annual_income`, `credit_score`, `months_as_customer`
   - Model: Random Forest
6. **💾 Export**:
   - Download cleaned CSV
   - Generate Python script
   - Create PDF report

---

## 🎯 Quick Test Commands

### Test 1: Verify Installation
```bash
# In the project directory
python -c "import streamlit, pandas, plotly, sklearn; print('✓ All dependencies installed!')"
```

### Test 2: Check Application Modules
```bash
python -c "from data_handler import DataHandler; from eda import EDA; print('✓ Modules working!')"
```

### Test 3: Verify Demo File
```bash
python -c "import pandas as pd; df = pd.read_csv('demo_customer_data.csv'); print(f'✓ Demo file loaded: {df.shape}')"
```

---

## 🐛 Troubleshooting

### Issue: "streamlit: command not found"
**Solution:**
```bash
pip install --upgrade streamlit
# or
python -m streamlit run app.py
```

### Issue: "ModuleNotFoundError: No module named 'XXX'"
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: Application won't start
**Solution:**
1. Make sure you're in the correct directory
2. Check Python version (must be 3.8+)
3. Ensure virtual environment is activated
4. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

---

## 📱 Alternative: Using Docker

If you have Docker installed:

```bash
# Build the image
docker-compose up

# Or using Docker directly
docker build -t ai-eda-assistant .
docker run -p 8501:8501 ai-eda-assistant
```

Then open **http://localhost:8501**

---

## 💡 Tips for First-Time Users

1. **Start Small**: Use the demo file first to understand the workflow
2. **Explore Features**: Navigate through all 6 main sections
3. **Try Operations**: Handle missing values, detect outliers, normalize data
4. **Reset Often**: Use the "Reset to Original Data" button to experiment
5. **Export Results**: Download your cleaned data and generated code

---

## 📚 Additional Resources

- **User Guide**: See `USER_GUIDE.md` for detailed feature explanations
- **Quick Reference**: See `QUICKSTART.md` for command reference
- **Examples**: See `EXAMPLES.md` for more sample workflows

---

## 🆘 Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review the error message in the terminal
3. Open an issue on GitHub with:
   - Your Python version
   - Operating system
   - Error message/screenshot
   - Steps to reproduce

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application starts without errors
- [ ] Demo file loads successfully
- [ ] Can navigate between different sections
- [ ] Visualizations appear correctly

---

**You're all set!** 🎉 Start exploring your data with the AI-EDA Assistant!
