# AI-EDA Assistant - Example Notebook

## Creating Sample Data for Testing

This notebook demonstrates how to create sample datasets for testing the AI-EDA Assistant.

### Import Required Libraries

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
```

### Example 1: Customer Purchase Data

```python
np.random.seed(42)
n_samples = 1000

# Generate customer data
data = {
    'customer_id': range(1, n_samples + 1),
    'age': np.random.randint(18, 80, n_samples),
    'income': np.random.normal(55000, 25000, n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'purchase_amount': np.random.lognormal(5, 1.5, n_samples),
    'num_purchases': np.random.randint(1, 50, n_samples),
    'satisfaction_score': np.random.uniform(1, 10, n_samples),
    'loyalty_years': np.random.randint(0, 20, n_samples),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
    'product_category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n_samples),
    'subscription': np.random.choice(['Free', 'Basic', 'Premium'], n_samples, p=[0.5, 0.3, 0.2])
}

df = pd.DataFrame(data)

# Add some missing values (realistic scenario)
missing_indices = np.random.choice(df.index, size=100, replace=False)
df.loc[missing_indices, 'income'] = np.nan

missing_indices = np.random.choice(df.index, size=50, replace=False)
df.loc[missing_indices, 'satisfaction_score'] = np.nan

# Add some outliers
outlier_indices = np.random.choice(df.index, size=20, replace=False)
df.loc[outlier_indices, 'purchase_amount'] *= 10

# Add some duplicates
duplicate_rows = df.sample(n=15, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# Save to CSV
df.to_csv('sample_customer_data.csv', index=False)
print(f"Created dataset with {len(df)} rows and {len(df.columns)} columns")
```

### Example 2: Sales Data

```python
np.random.seed(123)
n_records = 500

# Generate sales data
sales_data = {
    'transaction_id': range(1, n_records + 1),
    'date': [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(n_records)],
    'product_name': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], n_records),
    'quantity': np.random.randint(1, 100, n_records),
    'unit_price': np.random.uniform(10, 500, n_records),
    'discount_pct': np.random.choice([0, 5, 10, 15, 20], n_records),
    'sales_rep': np.random.choice(['John', 'Mary', 'Bob', 'Alice', 'Charlie'], n_records),
    'store_location': np.random.choice(['Store 1', 'Store 2', 'Store 3'], n_records)
}

df_sales = pd.DataFrame(sales_data)
df_sales['total_amount'] = df_sales['quantity'] * df_sales['unit_price'] * (1 - df_sales['discount_pct']/100)

df_sales.to_csv('sample_sales_data.csv', index=False)
print(f"Created sales dataset with {len(df_sales)} rows")
```

### Example 3: Employee Data

```python
np.random.seed(456)
n_employees = 300

# Generate employee data
employee_data = {
    'employee_id': range(1, n_employees + 1),
    'department': np.random.choice(['IT', 'HR', 'Sales', 'Marketing', 'Finance'], n_employees),
    'position': np.random.choice(['Junior', 'Mid-Level', 'Senior', 'Manager'], n_employees),
    'salary': np.random.normal(60000, 20000, n_employees),
    'years_experience': np.random.randint(0, 25, n_employees),
    'performance_rating': np.random.uniform(1, 5, n_employees),
    'training_hours': np.random.randint(0, 100, n_employees),
    'projects_completed': np.random.randint(0, 50, n_employees),
    'remote_work': np.random.choice(['Yes', 'No', 'Hybrid'], n_employees)
}

df_employees = pd.DataFrame(employee_data)

# Add missing values
missing_indices = np.random.choice(df_employees.index, size=20, replace=False)
df_employees.loc[missing_indices, 'performance_rating'] = np.nan

df_employees.to_csv('sample_employee_data.csv', index=False)
print(f"Created employee dataset with {len(df_employees)} rows")
```

## Using the AI-EDA Assistant

### Step 1: Upload Data
1. Run the Streamlit app: `streamlit run app.py`
2. Click on "Browse files" in the sidebar
3. Upload one of the sample CSV files created above

### Step 2: Explore Dataset Overview
- View basic statistics
- Check for missing values
- Identify data types
- Preview the data

### Step 3: Run Automated EDA
- Generate statistical summaries
- Create visualizations:
  - Histograms for distributions
  - Box plots for outliers
  - Correlation heatmap
  - Scatter matrix

### Step 4: Preprocess Data

**Handle Missing Values:**
- Strategy: Mean (for income, performance_rating)
- Columns: Select specific columns with missing data

**Handle Outliers:**
- Method: IQR
- Strategy: Cap (to preserve data)
- Columns: Select numerical columns

**Normalize Data:**
- Method: StandardScaler
- Columns: age, income, salary (depending on dataset)

### Step 5: Check Data Integrity
- Remove duplicates
- Validate data types
- Check for inconsistencies

### Step 6: Train Models (Optional)

**For Customer Data:**
- Target: purchase_amount
- Features: age, income, credit_score, loyalty_years
- Model: Random Forest Regressor

**For Employee Data:**
- Target: salary
- Features: years_experience, performance_rating, training_hours
- Model: Linear Regression

### Step 7: Export Results
- Download processed CSV
- Generate Python script
- Create PDF report

## Advanced Tips

### 1. Feature Engineering

Create new features before training models:
```python
# In your preprocessing pipeline
df['income_per_age'] = df['income'] / df['age']
df['purchase_frequency'] = df['num_purchases'] / df['loyalty_years']
```

### 2. Handling Categorical Variables

For model training, encode categorical variables:
```python
df_encoded = pd.get_dummies(df, columns=['region', 'product_category'])
```

### 3. Time Series Features

If working with date columns:
```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
```

### 4. Cross-Validation

Use multiple train-test splits to validate model performance:
- Try different test sizes (20%, 25%, 30%)
- Compare results across splits

### 5. Feature Selection

Before training:
- Remove highly correlated features (correlation > 0.95)
- Use feature importance from initial models
- Focus on features with business relevance

## Common Analysis Patterns

### Pattern 1: Customer Segmentation
1. Load customer data
2. Normalize features (age, income, purchases)
3. Create correlation heatmap
4. Identify customer segments

### Pattern 2: Sales Forecasting
1. Load sales data
2. Handle missing values
3. Create time-based features
4. Train regression model

### Pattern 3: Performance Analysis
1. Load employee data
2. Check for outliers in ratings
3. Analyze feature relationships
4. Train prediction model

## Troubleshooting

### Issue: Model performance is poor
**Solution:**
- Check for missing values
- Remove or cap outliers
- Normalize/scale features
- Try different models
- Add more relevant features

### Issue: Visualizations not showing
**Solution:**
- Ensure numerical columns exist
- Check for at least 2 columns for correlation
- Verify data is loaded correctly

### Issue: Export fails
**Solution:**
- Check file permissions
- Ensure output directory exists
- Verify data is not too large

## Next Steps

1. Experiment with different datasets
2. Try various preprocessing combinations
3. Compare model performances
4. Generate reports for stakeholders
5. Export code for production use

---

**Remember**: The AI-EDA Assistant is designed to speed up your workflow, 
not replace your domain expertise. Always validate results and apply your 
knowledge to interpret findings.
