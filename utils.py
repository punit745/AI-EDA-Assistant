"""
Utility functions for the AI-EDA Assistant.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
import io


def convert_df_to_csv(df: pd.DataFrame) -> str:
    """Convert DataFrame to CSV string."""
    return df.to_csv(index=False)


def convert_df_to_excel(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to Excel bytes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Get list of numeric column names."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Get list of categorical column names."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def format_bytes(bytes_size: int) -> str:
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def get_column_stats(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Get detailed statistics for a specific column."""
    stats = {}
    
    if column not in df.columns:
        return stats
    
    col_data = df[column]
    
    stats['name'] = column
    stats['dtype'] = str(col_data.dtype)
    stats['count'] = col_data.count()
    stats['null_count'] = col_data.isnull().sum()
    stats['null_percentage'] = (col_data.isnull().sum() / len(df)) * 100
    stats['unique_count'] = col_data.nunique()
    
    if col_data.dtype in ['int64', 'float64']:
        stats['min'] = col_data.min()
        stats['max'] = col_data.max()
        stats['mean'] = col_data.mean()
        stats['median'] = col_data.median()
        stats['std'] = col_data.std()
    
    return stats


def detect_column_type(df: pd.DataFrame, column: str) -> str:
    """
    Detect the semantic type of a column.
    
    Returns: 'numeric', 'categorical', 'datetime', 'text', or 'unknown'
    """
    if column not in df.columns:
        return 'unknown'
    
    col = df[column]
    
    # Check if numeric
    if col.dtype in ['int64', 'float64']:
        return 'numeric'
    
    # Check if datetime
    if col.dtype == 'datetime64[ns]':
        return 'datetime'
    
    # Try to detect if it's a date string
    if col.dtype == 'object':
        try:
            pd.to_datetime(col.dropna().head(10))
            return 'datetime'
        except:
            pass
    
    # Check if categorical
    if col.dtype == 'category' or col.nunique() / len(col) < 0.05:
        return 'categorical'
    
    # Check if text
    if col.dtype == 'object':
        avg_length = col.astype(str).str.len().mean()
        if avg_length > 50:
            return 'text'
        else:
            return 'categorical'
    
    return 'unknown'


def sample_dataframe(df: pd.DataFrame, n: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """Sample a DataFrame for large datasets."""
    if len(df) <= n:
        return df
    return df.sample(n=n, random_state=random_state)


def validate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate DataFrame and return validation results.
    
    Returns:
        Dict with validation results
    """
    validation = {
        'is_valid': True,
        'issues': [],
        'warnings': []
    }
    
    # Check if empty
    if len(df) == 0:
        validation['is_valid'] = False
        validation['issues'].append('DataFrame is empty')
        return validation
    
    # Check for duplicate columns
    if len(df.columns) != len(set(df.columns)):
        validation['warnings'].append('Duplicate column names detected')
    
    # Check for all-null columns
    all_null_cols = df.columns[df.isnull().all()].tolist()
    if all_null_cols:
        validation['warnings'].append(f'Columns with all null values: {all_null_cols}')
    
    # Check for single-value columns
    single_value_cols = [col for col in df.columns if df[col].nunique() == 1]
    if single_value_cols:
        validation['warnings'].append(f'Columns with single unique value: {single_value_cols}')
    
    return validation
