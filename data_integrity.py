"""
Data Integrity Module
Performs data validation and integrity checks.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import re
from datetime import datetime


class DataIntegrity:
    """Perform data integrity checks on DataFrame."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def check_duplicates(self) -> Dict:
        """
        Identify duplicate rows in the DataFrame.
        
        Returns:
            Dict: Information about duplicates
        """
        duplicate_count = self.df.duplicated().sum()
        duplicate_rows = self.df[self.df.duplicated(keep=False)]
        
        return {
            'total_duplicates': duplicate_count,
            'percentage': (duplicate_count / len(self.df) * 100) if len(self.df) > 0 else 0,
            'duplicate_indices': duplicate_rows.index.tolist()[:100]  # Limit to first 100
        }
    
    def remove_duplicates(self, keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate rows from DataFrame.
        
        Args:
            keep: Which duplicates to keep ('first', 'last', or False to remove all)
            
        Returns:
            pd.DataFrame: DataFrame with duplicates removed
        """
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates(keep=keep)
        removed_count = initial_count - len(self.df)
        
        return self.df
    
    def check_data_types(self) -> Dict:
        """
        Check and report data types for each column.
        
        Returns:
            Dict: Information about data types and potential inconsistencies
        """
        type_info = {}
        
        for col in self.df.columns:
            col_type = str(self.df[col].dtype)
            unique_types = set()
            
            # Check for mixed types in object columns
            if col_type == 'object':
                for val in self.df[col].dropna().head(100):  # Sample first 100
                    unique_types.add(type(val).__name__)
            
            type_info[col] = {
                'dtype': col_type,
                'unique_types': list(unique_types) if unique_types else [col_type],
                'is_consistent': len(unique_types) <= 1
            }
        
        return type_info
    
    def validate_date_formats(self, date_columns: List[str] = None) -> Dict:
        """
        Validate date formats in specified columns.
        
        Args:
            date_columns: List of columns to check for date formats
            
        Returns:
            Dict: Validation results for date columns
        """
        if date_columns is None:
            # Try to identify potential date columns
            date_columns = []
            for col in self.df.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_columns.append(col)
        
        results = {}
        
        for col in date_columns:
            if col not in self.df.columns:
                continue
            
            valid_dates = 0
            invalid_dates = 0
            date_formats = set()
            
            for val in self.df[col].dropna().head(100):  # Sample
                try:
                    parsed = pd.to_datetime(val)
                    valid_dates += 1
                    # Try to detect format
                    if isinstance(val, str):
                        if re.match(r'\d{4}-\d{2}-\d{2}', val):
                            date_formats.add('YYYY-MM-DD')
                        elif re.match(r'\d{2}/\d{2}/\d{4}', val):
                            date_formats.add('MM/DD/YYYY')
                        elif re.match(r'\d{2}-\d{2}-\d{4}', val):
                            date_formats.add('DD-MM-YYYY')
                except:
                    invalid_dates += 1
            
            results[col] = {
                'valid_dates': valid_dates,
                'invalid_dates': invalid_dates,
                'detected_formats': list(date_formats),
                'is_valid': invalid_dates == 0
            }
        
        return results
    
    def validate_numerical_entries(self, columns: List[str] = None) -> Dict:
        """
        Validate numerical entries for consistency.
        
        Args:
            columns: List of columns to validate. If None, check all numerical columns.
            
        Returns:
            Dict: Validation results including range, negative values, zeros, etc.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        results = {}
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            col_data = self.df[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            results[col] = {
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'range': float(col_data.max() - col_data.min()),
                'negative_count': int((col_data < 0).sum()),
                'zero_count': int((col_data == 0).sum()),
                'positive_count': int((col_data > 0).sum()),
                'infinite_count': int(np.isinf(col_data).sum()),
                'has_issues': np.isinf(col_data).any()
            }
        
        return results
    
    def check_categorical_consistency(self, columns: List[str] = None) -> Dict:
        """
        Check consistency of categorical columns.
        
        Args:
            columns: List of categorical columns to check
            
        Returns:
            Dict: Information about categorical consistency
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        results = {}
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            unique_values = self.df[col].nunique()
            total_values = len(self.df[col].dropna())
            
            # Check for case inconsistencies (e.g., "Yes" vs "yes")
            if self.df[col].dtype == 'object':
                values = self.df[col].dropna().astype(str)
                lower_values = values.str.lower()
                case_inconsistencies = len(values.unique()) - len(lower_values.unique())
            else:
                case_inconsistencies = 0
            
            results[col] = {
                'unique_values': unique_values,
                'total_values': total_values,
                'cardinality_ratio': unique_values / total_values if total_values > 0 else 0,
                'case_inconsistencies': case_inconsistencies,
                'top_values': self.df[col].value_counts().head(5).to_dict()
            }
        
        return results
    
    def get_integrity_report(self) -> Dict:
        """
        Generate a comprehensive integrity report.
        
        Returns:
            Dict: Complete integrity report
        """
        report = {
            'duplicates': self.check_duplicates(),
            'data_types': self.check_data_types(),
            'date_validation': self.validate_date_formats(),
            'numerical_validation': self.validate_numerical_entries(),
            'categorical_consistency': self.check_categorical_consistency()
        }
        
        return report
