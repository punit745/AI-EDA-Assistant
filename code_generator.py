"""
Code Generator Module
Generates Python scripts based on performed operations for reproducibility.
"""

from typing import List, Dict
from datetime import datetime


class CodeGenerator:
    """Generate Python code for performed operations."""
    
    def __init__(self):
        self.operations = []
        self.imports = set()
    
    def add_operation(self, operation: str, code: str, imports: List[str] = None):
        """
        Add an operation to the code generation log.
        
        Args:
            operation: Description of the operation
            code: Python code for the operation
            imports: List of required imports for this operation
        """
        self.operations.append({
            'operation': operation,
            'code': code
        })
        
        if imports:
            self.imports.update(imports)
    
    def generate_script(self, filename: str = 'data_analysis.py') -> str:
        """
        Generate a complete Python script from logged operations.
        
        Args:
            filename: Name for the generated script (for documentation)
            
        Returns:
            str: Complete Python script as string
        """
        script_lines = [
            '"""',
            f'Auto-generated Data Analysis Script',
            f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '"""',
            '',
            '# Import required libraries'
        ]
        
        # Add imports
        default_imports = [
            'import pandas as pd',
            'import numpy as np',
            'import matplotlib.pyplot as plt',
            'import seaborn as sns'
        ]
        
        script_lines.extend(default_imports)
        script_lines.extend(sorted(self.imports))
        script_lines.append('')
        script_lines.append('# Load data')
        script_lines.append('# df = pd.read_csv("your_data.csv")  # Replace with your data file')
        script_lines.append('')
        
        # Add operations
        for idx, op in enumerate(self.operations, 1):
            script_lines.append(f'# Step {idx}: {op["operation"]}')
            script_lines.append(op['code'])
            script_lines.append('')
        
        script_lines.append('# Display results')
        script_lines.append('print(df.head())')
        script_lines.append('print("\\nDataFrame shape:", df.shape)')
        
        return '\n'.join(script_lines)
    
    def add_data_loading(self, file_type: str, filename: str):
        """Add data loading code."""
        if file_type == 'csv':
            code = f'df = pd.read_csv("{filename}")'
        elif file_type in ['xlsx', 'xls']:
            code = f'df = pd.read_excel("{filename}")'
            self.imports.add('from openpyxl import load_workbook')
        elif file_type == 'json':
            code = f'df = pd.read_json("{filename}")'
        else:
            code = f'# Load data from {filename}'
        
        self.add_operation('Load data', code)
    
    def add_missing_value_handling(self, strategy: str, columns: List[str]):
        """Add missing value handling code."""
        if strategy == 'drop_rows':
            code = f'df = df.dropna(subset={columns})'
        elif strategy == 'drop_columns':
            code = f'df = df.drop(columns={columns})'
        elif strategy in ['mean', 'median']:
            code = f'df[{columns}] = df[{columns}].fillna(df[{columns}].{strategy}())'
        elif strategy == 'mode':
            code = f'df[{columns}] = df[{columns}].fillna(df[{columns}].mode().iloc[0])'
        else:
            code = f'# Handle missing values with {strategy}'
        
        self.add_operation(f'Handle missing values ({strategy})', code)
    
    def add_outlier_handling(self, method: str, strategy: str, columns: List[str]):
        """Add outlier handling code."""
        if method == 'iqr' and strategy == 'remove':
            code = f'''# Remove outliers using IQR method
for col in {columns}:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]'''
        else:
            code = f'# Handle outliers: method={method}, strategy={strategy}'
        
        self.add_operation(f'Handle outliers ({method}, {strategy})', code, 
                          imports=['from scipy import stats'])
    
    def add_normalization(self, method: str, columns: List[str]):
        """Add normalization code."""
        if method == 'standard':
            code = f'''from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[{columns}] = scaler.fit_transform(df[{columns}])'''
        elif method == 'minmax':
            code = f'''from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df[{columns}] = scaler.fit_transform(df[{columns}])'''
        elif method == 'robust':
            code = f'''from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
df[{columns}] = scaler.fit_transform(df[{columns}])'''
        else:
            code = f'# Normalize data using {method}'
        
        self.add_operation(f'Normalize data ({method})', code)
    
    def add_visualization(self, plot_type: str, columns: List[str] = None):
        """Add visualization code."""
        if plot_type == 'histogram':
            code = f'''df[{columns}].hist(figsize=(12, 8))
plt.tight_layout()
plt.show()'''
        elif plot_type == 'correlation':
            code = '''plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()'''
        elif plot_type == 'boxplot':
            code = f'''df[{columns}].boxplot(figsize=(12, 6))
plt.xticks(rotation=45)
plt.show()'''
        else:
            code = f'# Create {plot_type} visualization'
        
        self.add_operation(f'Create {plot_type}', code)
    
    def add_model_training(self, model_type: str, target: str, features: List[str]):
        """Add model training code."""
        code = f'''from sklearn.model_selection import train_test_split
from sklearn.{model_type.lower()} import {model_type}

X = df[{features}]
y = df['{target}']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = {model_type}()
model.fit(X_train, y_train)
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f'Train Score: {{train_score:.4f}}')
print(f'Test Score: {{test_score:.4f}}')'''
        
        self.add_operation(f'Train {model_type} model', code)
    
    def clear(self):
        """Clear all logged operations."""
        self.operations = []
        self.imports = set()
