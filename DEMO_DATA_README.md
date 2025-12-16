# Demo Customer Data - Dataset Information

## Overview
This is a synthetic customer dataset created for demonstrating the AI-EDA Assistant features.

## Dataset Details

- **File Name**: `demo_customer_data.csv`
- **Size**: ~12 KB
- **Rows**: 205 (200 unique + 5 duplicates)
- **Columns**: 11

## Column Descriptions

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `customer_id` | Integer | Unique customer identifier | 1, 2, 3... |
| `age` | Integer | Customer age (18-75) | 25, 42, 58 |
| `annual_income` | Float | Annual income in dollars | 55000.50, 42000.00 |
| `credit_score` | Integer | Credit score (300-850) | 720, 650, 580 |
| `purchase_amount` | Float | Total purchase amount | 125.50, 450.00 |
| `months_as_customer` | Integer | Duration as customer (1-120 months) | 24, 36, 48 |
| `num_purchases` | Integer | Number of purchases made (1-50) | 5, 12, 25 |
| `satisfaction_rating` | Float | Satisfaction rating (1.0-5.0) | 3.5, 4.2, 2.8 |
| `region` | String | Geographic region | North, South, East, West, Central |
| `membership_tier` | String | Membership level | Bronze, Silver, Gold, Platinum |
| `product_category` | String | Product category | Electronics, Clothing, Home & Garden, Sports, Books |

## Data Characteristics

### ✅ Realistic Features
- **Normal Distribution**: Income follows normal distribution (~$55k mean)
- **Log-Normal**: Purchase amounts follow log-normal distribution
- **Categorical Balance**: Regions and tiers have realistic proportions

### 🔍 Intentional Issues (for Testing)
1. **Missing Values**: 25 missing values across 2 columns
   - `annual_income`: 15 missing (7.3%)
   - `satisfaction_rating`: 10 missing (4.9%)

2. **Outliers**: 8 extreme values in `purchase_amount`
   - Can be detected using IQR or Z-score methods
   - Represent 3x normal purchase amounts

3. **Duplicates**: 5 exact duplicate rows
   - Can be found using duplicate detection
   - Represent data entry errors

## Suggested Analysis Tasks

### 1. Exploratory Data Analysis
- Generate statistical summary of numerical columns
- Create histograms for age, income, and purchase amount distributions
- Visualize correlation between income, credit score, and purchase amount
- Analyze missing value patterns

### 2. Data Cleaning
- Handle missing values using mean/median imputation
- Detect and handle outliers in purchase_amount
- Remove duplicate entries

### 3. Feature Engineering
- Normalize numerical features for modeling
- Calculate customer lifetime value
- Create age groups or income brackets

### 4. Predictive Modeling
- **Regression Task**: Predict `purchase_amount`
  - Features: age, annual_income, credit_score, months_as_customer, num_purchases
  - Models: Linear Regression, Random Forest Regressor
  
- **Classification Task**: Predict `membership_tier`
  - Features: annual_income, credit_score, num_purchases, satisfaction_rating
  - Models: Decision Tree, Random Forest Classifier

## Expected Analysis Results

### Statistical Summary
- **Age**: Mean ~46, Std ~16
- **Income**: Mean ~$55k, Std ~$20k
- **Purchase Amount**: Median ~$90, with outliers up to ~$900
- **Satisfaction**: Mean ~3.0, Range 1.0-5.0

### Correlations
- **Strong**: credit_score ↔ annual_income (positive)
- **Moderate**: months_as_customer ↔ num_purchases (positive)
- **Weak**: age ↔ satisfaction_rating

### Data Quality Issues
- Missing: 12.2% of annual_income values
- Missing: 4.9% of satisfaction_rating values
- Duplicates: 2.4% of rows
- Outliers: 3.9% of purchase amounts

## Sample Queries & Insights

### Business Questions to Explore:

1. **Customer Segmentation**
   - Which regions have the highest average purchase amounts?
   - How does membership tier correlate with satisfaction?

2. **Revenue Analysis**
   - What's the relationship between customer tenure and purchase behavior?
   - Which product categories are most popular by region?

3. **Risk Assessment**
   - Does credit score predict purchase amount?
   - Are there patterns in missing satisfaction ratings?

## Usage Example

```python
import pandas as pd

# Load the data
df = pd.read_csv('demo_customer_data.csv')

# Basic exploration
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Analyze by region
print(df.groupby('region')['purchase_amount'].mean())
```

## Best Practices for This Dataset

1. **Start with Overview**: Check shape, columns, and basic statistics
2. **Handle Missing Values**: Consider mean imputation for income
3. **Address Outliers**: Use IQR method for purchase amounts
4. **Remove Duplicates**: Before any analysis or modeling
5. **Normalize Features**: Before training ML models
6. **Validate Results**: Check if insights make business sense

## Data Generation

This dataset was generated using Python with:
- `numpy.random` for numerical distributions
- Realistic parameters for each field
- Intentional data quality issues for testing

**Created**: December 2024  
**Purpose**: Demonstration and testing of AI-EDA Assistant  
**License**: Public domain - free to use for any purpose

---

**Ready to analyze?** Upload this file to the AI-EDA Assistant and start exploring! 🚀
