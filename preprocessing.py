"""
Data Preprocessing Module
Handles missing values, outliers, normalization, and scaling.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from scipy import stats
from typing import List, Optional, Dict


class Preprocessor:
    """Handle various data preprocessing tasks."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.operations_log = []
    
    def handle_missing_values(self, strategy: str = 'mean', columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            strategy: Strategy to handle missing values ('mean', 'median', 'mode', 'drop_rows', 'drop_columns')
            columns: List of columns to apply the strategy to. If None, apply to all columns.
            
        Returns:
            pd.DataFrame: DataFrame with missing values handled
        """
        if columns is None:
            columns = self.df.columns.tolist()
        
        if strategy == 'drop_rows':
            initial_rows = len(self.df)
            self.df = self.df.dropna(subset=columns)
            self.operations_log.append(f"Dropped {initial_rows - len(self.df)} rows with missing values")
        
        elif strategy == 'drop_columns':
            cols_to_drop = [col for col in columns if self.df[col].isnull().any()]
            self.df = self.df.drop(columns=cols_to_drop)
            self.operations_log.append(f"Dropped columns with missing values: {cols_to_drop}")
        
        elif strategy in ['mean', 'median', 'mode']:
            for col in columns:
                if col not in self.df.columns:
                    continue
                
                if self.df[col].isnull().any():
                    if self.df[col].dtype in ['float64', 'int64']:
                        if strategy == 'mean':
                            fill_value = self.df[col].mean()
                        elif strategy == 'median':
                            fill_value = self.df[col].median()
                        else:  # mode
                            fill_value = self.df[col].mode()[0] if not self.df[col].mode().empty else 0
                        
                        self.df[col].fillna(fill_value, inplace=True)
                        self.operations_log.append(f"Filled missing values in '{col}' with {strategy}: {fill_value:.2f}")
                    else:
                        # For non-numeric columns, use mode
                        mode_value = self.df[col].mode()[0] if not self.df[col].mode().empty else 'Unknown'
                        self.df[col].fillna(mode_value, inplace=True)
                        self.operations_log.append(f"Filled missing values in '{col}' with mode: {mode_value}")
        
        return self.df
    
    def detect_outliers_zscore(self, columns: Optional[List[str]] = None, threshold: float = 3.0) -> Dict[str, pd.Series]:
        """
        Detect outliers using Z-score method.
        
        Args:
            columns: List of numerical columns to check. If None, check all numerical columns.
            threshold: Z-score threshold (default: 3.0)
            
        Returns:
            Dict: Dictionary with column names as keys and boolean series indicating outliers
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers = {}
        for col in columns:
            if col in self.df.columns and self.df[col].dtype in ['float64', 'int64']:
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                outliers[col] = pd.Series(False, index=self.df.index)
                outliers[col].loc[self.df[col].notna()] = z_scores > threshold
        
        return outliers
    
    def detect_outliers_iqr(self, columns: Optional[List[str]] = None) -> Dict[str, pd.Series]:
        """
        Detect outliers using IQR (Interquartile Range) method.
        
        Args:
            columns: List of numerical columns to check. If None, check all numerical columns.
            
        Returns:
            Dict: Dictionary with column names as keys and boolean series indicating outliers
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers = {}
        for col in columns:
            if col in self.df.columns and self.df[col].dtype in ['float64', 'int64']:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers[col] = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
        
        return outliers
    
    def handle_outliers(self, method: str = 'iqr', strategy: str = 'remove', columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Handle outliers in the DataFrame.
        
        Args:
            method: Method to detect outliers ('zscore' or 'iqr')
            strategy: Strategy to handle outliers ('remove', 'cap', or 'median')
            columns: List of columns to process. If None, process all numerical columns.
            
        Returns:
            pd.DataFrame: DataFrame with outliers handled
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == 'zscore':
            outliers_dict = self.detect_outliers_zscore(columns)
        else:  # iqr
            outliers_dict = self.detect_outliers_iqr(columns)
        
        for col, outliers in outliers_dict.items():
            outlier_count = outliers.sum()
            
            if outlier_count == 0:
                continue
            
            if strategy == 'remove':
                self.df = self.df[~outliers]
                self.operations_log.append(f"Removed {outlier_count} outliers from '{col}'")
            
            elif strategy == 'cap':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                self.df.loc[outliers, col] = self.df.loc[outliers, col].clip(lower_bound, upper_bound)
                self.operations_log.append(f"Capped {outlier_count} outliers in '{col}'")
            
            elif strategy == 'median':
                median_value = self.df.loc[~outliers, col].median()
                self.df.loc[outliers, col] = median_value
                self.operations_log.append(f"Replaced {outlier_count} outliers in '{col}' with median: {median_value:.2f}")
        
        return self.df
    
    def normalize_data(self, method: str = 'standard', columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Normalize or scale numerical features.
        
        Args:
            method: Normalization method ('standard', 'minmax', or 'robust')
            columns: List of columns to normalize. If None, normalize all numerical columns.
            
        Returns:
            pd.DataFrame: DataFrame with normalized features
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filter out columns that don't exist
        columns = [col for col in columns if col in self.df.columns]
        
        if len(columns) == 0:
            return self.df
        
        if method == 'standard':
            scaler = StandardScaler()
            scaler_name = "StandardScaler (mean=0, std=1)"
        elif method == 'minmax':
            scaler = MinMaxScaler()
            scaler_name = "MinMaxScaler (range 0-1)"
        elif method == 'robust':
            scaler = RobustScaler()
            scaler_name = "RobustScaler (using median and IQR)"
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        self.df[columns] = scaler.fit_transform(self.df[columns])
        self.operations_log.append(f"Normalized columns {columns} using {scaler_name}")
        
        return self.df
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return the processed DataFrame."""
        return self.df
    
    def get_operations_log(self) -> List[str]:
        """Return the log of operations performed."""
        return self.operations_log
