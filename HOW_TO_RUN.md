# 🚀 How to Run AI-EDA Assistant - Simple Guide

## What You Need
- Computer with Python 3.8 or newer
- Internet connection (for downloading packages)
- 10 minutes of your time

## Step-by-Step Instructions

### 1️⃣ Download the Project

**Option A: Using Git**
```bash
git clone https://github.com/punit745/AI-EDA-Assistant.git
cd AI-EDA-Assistant
```

**Option B: Download ZIP**
- Go to GitHub repository
- Click green "Code" button → "Download ZIP"
- Extract ZIP file
- Open terminal in that folder

### 2️⃣ Install Python Packages

```bash
pip install -r requirements.txt
```

**This installs:**
- Streamlit (web interface)
- Pandas (data processing)
- Plotly (visualizations)
- Scikit-learn (machine learning)
- And 10 other packages

**Wait time:** 1-2 minutes

### 3️⃣ Run the App

```bash
streamlit run app.py
```

**You'll see:**
```
Local URL: http://localhost:8501
```

**Browser will open automatically!** 🎉

If not, manually open: http://localhost:8501

### 4️⃣ Load Demo Data

1. Look for **"Browse files"** button in sidebar
2. Click it
3. Navigate to project folder
4. Select **`demo_customer_data.csv`**
5. Click Open

**Data loads instantly!** ✅

### 5️⃣ Explore Features

**Try this 5-minute workflow:**

1. **📊 Dataset Overview** (current page)
   - See 205 rows, 11 columns
   - View data preview
   - Check column types

2. **🔍 Automated EDA** (sidebar menu)
   - Click "Histograms" → See age/income distributions
   - Click "Correlation Heatmap" → See relationships
   - Click "Missing Values" → See 25 missing values

3. **🧹 Preprocessing** (sidebar menu)
   - Select "Handle Missing Values"
   - Choose "mean" strategy
   - Click "Apply"
   - ✅ Missing values fixed!

4. **🤖 Model Training** (sidebar menu)
   - Target: `purchase_amount`
   - Features: `age`, `annual_income`, `credit_score`
   - Model: Random Forest
   - Click "Train Model"
   - See R² score and metrics!

5. **💾 Export** (sidebar menu)
   - Download cleaned CSV
   - Generate Python script
   - Create PDF report

## 🎥 What It Looks Like

```
┌─────────────────────────────────────────┐
│  📁 Upload File    [Browse files...]    │  ← Sidebar
│                                         │
│  🧭 Navigation                          │
│   📊 Dataset Overview                   │
│   🔍 Automated EDA                      │
│   🧹 Preprocessing                      │
│   ✅ Data Integrity                     │
│   🤖 Model Training                     │
│   💾 Export & Reports                   │
└─────────────────────────────────────────┘

        ┌──────────────────────────────┐
        │                              │
        │   Main Content Area          │  ← Charts, tables, forms
        │   • Statistics               │
        │   • Visualizations           │
        │   • Results                  │
        │                              │
        └──────────────────────────────┘
```

## 📱 Stop the App

Press `Ctrl + C` in terminal to stop the server.

## ✅ Checklist

Before you start:
- [ ] Python 3.8+ installed
- [ ] Terminal/Command Prompt open
- [ ] Inside project folder
- [ ] Internet connected

After setup:
- [ ] Dependencies installed (no errors)
- [ ] App starts successfully
- [ ] Browser opens to localhost:8501
- [ ] Demo file loads
- [ ] Can see visualizations

## ❓ Common Questions

**Q: Which Python version?**
A: 3.8, 3.9, 3.10, 3.11, or 3.12 (recommended: 3.11)

**Q: Do I need to install Python packages globally?**
A: No! Use virtual environment (see SETUP_GUIDE.md)

**Q: Can I use my own data?**
A: Yes! Upload any CSV, Excel, JSON, or TXT file

**Q: Is internet required after installation?**
A: No, works offline after packages are installed

**Q: How much disk space needed?**
A: ~200 MB (packages) + your data files

**Q: Can I run on Windows/Mac/Linux?**
A: Yes! Works on all platforms

## 🐛 Problems?

See **SETUP_GUIDE.md** for detailed troubleshooting:
- Port already in use
- Module not found errors
- Permission issues
- Installation failures

## 📚 Learn More

- **SETUP_GUIDE.md** - Full setup with troubleshooting
- **USER_GUIDE.md** - Feature documentation
- **DEMO_DATA_README.md** - About the demo dataset
- **QUICKSTART.md** - Command reference

## 🎯 Pro Tips

1. **Use virtual environment** to avoid package conflicts
2. **Check Python version** before installing packages
3. **Start with demo data** to learn the interface
4. **Read error messages** - they tell you what's wrong
5. **Keep terminal open** while using the app

---

**That's it!** You're ready to analyze data! 🎉

Need help? Open an issue on GitHub with your error message.
