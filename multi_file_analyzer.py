"""
Multi-File Analysis Module
Provides functionality to analyze and compare multiple datasets.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Optional, Union


class MultiFileAnalyzer:
    """Analyze and compare multiple datasets."""
    
    def __init__(self):
        self.datasets = {}
    
    def add_dataset(self, name: str, df: pd.DataFrame):
        """
        Add a dataset to the analyzer.
        
        Args:
            name: Name identifier for the dataset
            df: DataFrame to add
        """
        self.datasets[name] = df
    
    def get_dataset_names(self) -> List[str]:
        """Get list of dataset names."""
        return list(self.datasets.keys())
    
    def compare_schemas(self) -> pd.DataFrame:
        """
        Compare schemas of all datasets.
        
        Returns:
            DataFrame with schema comparison
        """
        if len(self.datasets) < 2:
            return pd.DataFrame()
        
        comparison = {}
        
        for name, df in self.datasets.items():
            comparison[name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': ', '.join(df.columns.tolist()[:5]) + ('...' if len(df.columns) > 5 else ''),
                'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
                'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns),
                'memory_mb': df.memory_usage(deep=True).sum() / (1024**2)
            }
        
        return pd.DataFrame(comparison).T
    
    def find_common_columns(self) -> Dict[str, List[str]]:
        """
        Find common columns across datasets.
        
        Returns:
            Dict with common columns information
        """
        if len(self.datasets) < 2:
            return {}
        
        # Get all column sets
        column_sets = {name: set(df.columns) for name, df in self.datasets.items()}
        
        # Find intersection
        common_columns = set.intersection(*column_sets.values())
        
        # Find unique columns for each dataset
        unique_columns = {}
        for name, cols in column_sets.items():
            unique = cols - common_columns
            unique_columns[name] = list(unique)
        
        return {
            'common': list(common_columns),
            'unique': unique_columns
        }
    
    def merge_datasets(self, dataset1: str, dataset2: str, 
                      join_column: str, how: str = 'inner') -> pd.DataFrame:
        """
        Merge two datasets on a common column.
        
        Args:
            dataset1: Name of first dataset
            dataset2: Name of second dataset
            join_column: Column to join on
            how: Type of join ('inner', 'outer', 'left', 'right')
            
        Returns:
            Merged DataFrame
        """
        if dataset1 not in self.datasets:
            raise ValueError(f"Dataset '{dataset1}' not found")
        if dataset2 not in self.datasets:
            raise ValueError(f"Dataset '{dataset2}' not found")
        
        df1 = self.datasets[dataset1]
        df2 = self.datasets[dataset2]
        
        if join_column not in df1.columns or join_column not in df2.columns:
            raise ValueError(f"Column '{join_column}' not found in both datasets")
        
        merged = pd.merge(df1, df2, on=join_column, how=how, suffixes=('_1', '_2'))
        
        return merged
    
    def compare_statistics(self, column: str) -> pd.DataFrame:
        """
        Compare statistics for a specific column across datasets.
        
        Args:
            column: Column name to compare
            
        Returns:
            DataFrame with comparative statistics
        """
        stats = {}
        
        for name, df in self.datasets.items():
            if column in df.columns:
                col_data = df[column]
                
                if pd.api.types.is_numeric_dtype(col_data):
                    stats[name] = {
                        'mean': col_data.mean(),
                        'median': col_data.median(),
                        'std': col_data.std(),
                        'min': col_data.min(),
                        'max': col_data.max(),
                        'missing': col_data.isnull().sum(),
                        'unique': col_data.nunique()
                    }
                else:
                    mode_values = col_data.mode()
                    value_counts = col_data.value_counts()
                    
                    stats[name] = {
                        'unique': col_data.nunique(),
                        'missing': col_data.isnull().sum(),
                        'mode': mode_values[0] if len(mode_values) > 0 else None,
                        'top_value': value_counts.index[0] if len(value_counts) > 0 else None
                    }
        
        return pd.DataFrame(stats).T
    
    def create_comparison_chart(self, column: str, chart_type: str = 'box') -> go.Figure:
        """
        Create comparison chart for a column across datasets.
        
        Args:
            column: Column name to visualize
            chart_type: Type of chart ('box', 'violin', 'histogram')
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for name, df in self.datasets.items():
            if column in df.columns and pd.api.types.is_numeric_dtype(df[column]):
                if chart_type == 'box':
                    fig.add_trace(go.Box(
                        y=df[column].dropna(),
                        name=name,
                        boxmean='sd'
                    ))
                elif chart_type == 'violin':
                    fig.add_trace(go.Violin(
                        y=df[column].dropna(),
                        name=name,
                        box_visible=True,
                        meanline_visible=True
                    ))
                elif chart_type == 'histogram':
                    fig.add_trace(go.Histogram(
                        x=df[column].dropna(),
                        name=name,
                        opacity=0.7
                    ))
        
        fig.update_layout(
            title=f"Comparison of '{column}' across datasets",
            xaxis_title="Dataset" if chart_type in ['box', 'violin'] else column,
            yaxis_title=column if chart_type in ['box', 'violin'] else "Count",
            height=500
        )
        
        return fig
    
    def aggregate_analysis(self, group_column: str, value_column: str,
                          agg_func: str = 'mean') -> pd.DataFrame:
        """
        Perform aggregated analysis across datasets.
        
        Args:
            group_column: Column to group by
            value_column: Column to aggregate
            agg_func: Aggregation function ('mean', 'sum', 'count', 'median')
            
        Returns:
            DataFrame with aggregated results
        """
        results = {}
        
        for name, df in self.datasets.items():
            if group_column in df.columns and value_column in df.columns:
                if agg_func == 'mean':
                    result = df.groupby(group_column)[value_column].mean()
                elif agg_func == 'sum':
                    result = df.groupby(group_column)[value_column].sum()
                elif agg_func == 'count':
                    result = df.groupby(group_column)[value_column].count()
                elif agg_func == 'median':
                    result = df.groupby(group_column)[value_column].median()
                else:
                    continue
                
                results[name] = result
        
        if results:
            return pd.DataFrame(results)
        else:
            return pd.DataFrame()
    
    def detect_relationships(self) -> List[Dict]:
        """
        Detect potential relationships between datasets.
        
        Returns:
            List of potential relationship suggestions
        """
        if len(self.datasets) < 2:
            return []
        
        relationships = []
        dataset_names = list(self.datasets.keys())
        
        # Check for common columns that could be join keys
        for i in range(len(dataset_names)):
            for j in range(i + 1, len(dataset_names)):
                name1 = dataset_names[i]
                name2 = dataset_names[j]
                
                df1 = self.datasets[name1]
                df2 = self.datasets[name2]
                
                common_cols = set(df1.columns) & set(df2.columns)
                
                for col in common_cols:
                    # Check if column could be a join key
                    unique1 = df1[col].nunique()
                    unique2 = df2[col].nunique()
                    
                    overlap = len(set(df1[col].unique()) & set(df2[col].unique()))
                    
                    if overlap > 0:
                        max_unique = max(unique1, unique2)
                        if max_unique > 0:
                            overlap_pct = (overlap / max_unique) * 100
                            
                            relationships.append({
                                'dataset1': name1,
                                'dataset2': name2,
                                'join_column': col,
                                'overlap_percentage': round(overlap_pct, 2),
                                'common_values': overlap,
                                'recommendation': 'Strong join candidate' if overlap_pct > 50 else 'Possible join'
                            })
        
        return sorted(relationships, key=lambda x: x['overlap_percentage'], reverse=True)
    
    def get_summary(self) -> Dict:
        """
        Get summary of all datasets.
        
        Returns:
            Dict with summary information
        """
        return {
            'total_datasets': len(self.datasets),
            'dataset_names': list(self.datasets.keys()),
            'total_rows': sum(len(df) for df in self.datasets.values()),
            'total_columns': sum(len(df.columns) for df in self.datasets.values()),
            'common_columns': self.find_common_columns()
        }
