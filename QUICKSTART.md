# AI-EDA Assistant - Quick Reference

## Installation & Startup

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py
```

## File Formats Supported
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)
- Text (`.txt`)

## Main Features

### 1. Dataset Overview
- **Metrics**: Rows, columns, memory, duplicates
- **Data Preview**: Adjustable row count
- **Column Info**: Types, null counts, unique values

### 2. Automated EDA
- **Stats**: Mean, median, std, skewness, kurtosis
- **Visualizations**: Histograms, box plots, correlation heatmap, scatter matrix, missing values plot

### 3. Preprocessing
- **Missing Values**: mean | median | mode | drop_rows | drop_columns
- **Outliers**: 
  - Detection: IQR | Z-score
  - Handling: remove | cap | median
- **Normalization**: standard | minmax | robust

### 4. Data Integrity
- Duplicate detection & removal
- Data type consistency
- Date validation
- Numerical validation

### 5. Model Training
- **Models**: Linear Regression | Decision Tree | Random Forest
- **Metrics**: RMSE, MAE, R², Accuracy
- **Features**: Feature importance visualization

### 6. Export
- **Formats**: CSV | Excel | JSON
- **Code**: Python script generation
- **Reports**: PDF with visualizations

## Workflow

```
Upload → Overview → EDA → Preprocess → Integrity Check → Model Training → Export
```

## Keyboard Shortcuts
- `R`: Refresh page
- `Esc`: Close modal

## Quick Tips

1. **Always start with**: Dataset Overview
2. **Best preprocessing order**: Duplicates → Missing → Outliers → Normalize
3. **Before modeling**: Check for at least 2 numerical features
4. **Performance**: Limit visualizations to top 10 columns
5. **Export often**: Save intermediate results

## Common Commands

```bash
# Development
streamlit run app.py

# Docker
docker-compose up

# Deploy to Heroku
git push heroku main

# Run tests
python /tmp/test_modules.py
```

## Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Web interface |
| pandas | Data manipulation |
| plotly | Interactive visualizations |
| scikit-learn | Machine learning |
| fpdf2 | PDF reports |

## Project Structure

```
AI-EDA-Assistant/
├── app.py              # Main app
├── data_handler.py     # File I/O
├── eda.py             # Analysis
├── preprocessing.py   # Cleaning
├── model_training.py  # ML models
├── code_generator.py  # Export code
├── report_generator.py # PDF reports
└── utils.py           # Helpers
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| File won't upload | Check format & encoding (UTF-8) |
| No visualizations | Need 2+ numerical columns |
| Model fails | Check for missing values |
| Out of memory | Use smaller dataset or sample |

## API Quick Reference

### DataHandler
```python
handler = DataHandler()
df = handler.load_data(uploaded_file)
```

### EDA
```python
eda = EDA(df)
overview = eda.get_dataset_overview()
stats = eda.get_statistical_summary()
fig = eda.create_histograms()
```

### Preprocessor
```python
prep = Preprocessor(df)
df = prep.handle_missing_values(strategy='mean')
df = prep.handle_outliers(method='iqr', strategy='cap')
df = prep.normalize_data(method='standard')
```

### Model Training
```python
trainer = ModelTrainer(df)
trainer.prepare_data('target', ['feat1', 'feat2'])
results = trainer.train_random_forest()
```

## Support

- **GitHub**: https://github.com/punit745/AI-EDA-Assistant
- **Issues**: Open a GitHub issue
- **Docs**: README.md, USER_GUIDE.md

---

Version 1.0.0 | December 2024
