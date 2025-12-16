"""
Exploratory Data Analysis (EDA) Module
Provides automated EDA functionality including statistical summaries and visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
import io


class EDA:
    """Perform exploratory data analysis on DataFrame."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_dataset_overview(self) -> Dict:
        """
        Get comprehensive overview of the dataset.
        
        Returns:
            Dict: Overview information including size, columns, types, and missing values
        """
        overview = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'missing_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / (1024 * 1024),
            'duplicate_rows': self.df.duplicated().sum()
        }
        return overview
    
    def get_statistical_summary(self) -> pd.DataFrame:
        """
        Get statistical summary of numerical columns.
        
        Returns:
            pd.DataFrame: Statistical summary including mean, median, std, etc.
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return pd.DataFrame()
        
        summary = self.df[numeric_cols].describe()
        
        # Add additional statistics
        summary.loc['median'] = self.df[numeric_cols].median()
        summary.loc['variance'] = self.df[numeric_cols].var()
        summary.loc['skewness'] = self.df[numeric_cols].skew()
        summary.loc['kurtosis'] = self.df[numeric_cols].kurtosis()
        
        return summary
    
    def get_categorical_summary(self) -> Dict:
        """
        Get summary of categorical columns.
        
        Returns:
            Dict: Summary of categorical columns including unique values and counts
        """
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        summary = {}
        
        for col in categorical_cols:
            summary[col] = {
                'unique_values': self.df[col].nunique(),
                'top_values': self.df[col].value_counts().head(10).to_dict(),
                'missing': self.df[col].isnull().sum()
            }
        
        return summary
    
    def create_histograms(self) -> go.Figure:
        """
        Create histograms for numerical columns.
        
        Returns:
            go.Figure: Plotly figure with histograms
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            return None
        
        # Limit to first 10 columns for performance
        numeric_cols = numeric_cols[:10]
        
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig = make_subplots(
            rows=n_rows, cols=n_cols,
            subplot_titles=numeric_cols,
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        for idx, col in enumerate(numeric_cols):
            row = idx // n_cols + 1
            col_num = idx % n_cols + 1
            
            fig.add_trace(
                go.Histogram(x=self.df[col], name=col, showlegend=False),
                row=row, col=col_num
            )
        
        fig.update_layout(
            title_text="Distribution of Numerical Features",
            height=300 * n_rows,
            showlegend=False
        )
        
        return fig
    
    def create_box_plots(self) -> go.Figure:
        """
        Create box plots for numerical columns.
        
        Returns:
            go.Figure: Plotly figure with box plots
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            return None
        
        # Limit to first 10 columns
        numeric_cols = numeric_cols[:10]
        
        fig = go.Figure()
        
        for col in numeric_cols:
            fig.add_trace(go.Box(y=self.df[col], name=col))
        
        fig.update_layout(
            title="Box Plots for Numerical Features",
            yaxis_title="Value",
            showlegend=True,
            height=500
        )
        
        return fig
    
    def create_correlation_heatmap(self) -> go.Figure:
        """
        Create correlation heatmap for numerical columns.
        
        Returns:
            go.Figure: Plotly figure with correlation heatmap
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return None
        
        # Limit to first 15 columns for readability
        numeric_cols = numeric_cols[:15]
        correlation_matrix = self.df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Correlation Heatmap",
            xaxis_title="Features",
            yaxis_title="Features",
            height=600,
            width=700
        )
        
        return fig
    
    def create_pair_plot_data(self, max_cols: int = 4) -> List[Tuple[str, str]]:
        """
        Generate data for pair plots (scatter matrix).
        
        Args:
            max_cols: Maximum number of columns to include
            
        Returns:
            List of column pairs for scatter plots
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return []
        
        # Limit columns
        numeric_cols = numeric_cols[:max_cols]
        
        pairs = []
        for i in range(len(numeric_cols)):
            for j in range(i, len(numeric_cols)):
                pairs.append((numeric_cols[i], numeric_cols[j]))
        
        return pairs
    
    def create_scatter_matrix(self) -> go.Figure:
        """
        Create scatter matrix for numerical columns.
        
        Returns:
            go.Figure: Plotly figure with scatter matrix
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return None
        
        # Limit to 5 columns for performance
        numeric_cols = numeric_cols[:5]
        
        fig = px.scatter_matrix(
            self.df[numeric_cols],
            dimensions=numeric_cols,
            title="Scatter Matrix of Numerical Features"
        )
        
        fig.update_layout(
            height=800,
            width=800
        )
        
        return fig
    
    def get_missing_value_plot(self) -> go.Figure:
        """
        Create visualization of missing values.
        
        Returns:
            go.Figure: Plotly figure showing missing values
        """
        missing_data = self.df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) == 0:
            return None
        
        fig = go.Figure(data=[
            go.Bar(
                x=missing_data.values,
                y=missing_data.index,
                orientation='h',
                marker=dict(color='red')
            )
        ])
        
        fig.update_layout(
            title="Missing Values by Column",
            xaxis_title="Number of Missing Values",
            yaxis_title="Column",
            height=max(400, len(missing_data) * 30)
        )
        
        return fig
