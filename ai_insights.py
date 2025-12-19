"""
AI-Powered Insights Module
Provides intelligent data analysis and automated insights generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


class AIInsights:
    """Generate AI-powered insights for data analysis."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_data_health_score(self) -> Dict:
        """
        Calculate comprehensive data health score.
        
        Returns:
            Dict: Health metrics and scores
        """
        total_cells = self.df.shape[0] * self.df.shape[1]
        
        # Missing values score
        missing_cells = self.df.isnull().sum().sum()
        missing_score = max(0, 100 - (missing_cells / total_cells * 100))
        
        # Duplicate rows score
        duplicate_rows = self.df.duplicated().sum()
        duplicate_score = max(0, 100 - (duplicate_rows / len(self.df) * 100))
        
        # Data type consistency score
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        type_consistency_issues = 0
        for col in self.df.columns:
            if col in numeric_cols:
                # Check for mixed types in numeric columns
                try:
                    non_numeric = pd.to_numeric(self.df[col], errors='coerce').isna().sum() - self.df[col].isna().sum()
                    type_consistency_issues += non_numeric
                except (ValueError, TypeError):
                    pass
        
        type_consistency_score = max(0, 100 - (type_consistency_issues / total_cells * 100))
        
        # Outlier score (for numeric columns)
        outlier_count = 0
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            outlier_count += outliers
        
        outlier_score = max(0, 100 - (outlier_count / len(self.df) * 20)) if len(numeric_cols) > 0 else 100
        
        # Overall health score
        overall_score = (missing_score * 0.3 + duplicate_score * 0.2 + 
                        type_consistency_score * 0.3 + outlier_score * 0.2)
        
        return {
            'overall_score': round(overall_score, 2),
            'missing_score': round(missing_score, 2),
            'duplicate_score': round(duplicate_score, 2),
            'type_consistency_score': round(type_consistency_score, 2),
            'outlier_score': round(outlier_score, 2),
            'health_grade': self._get_health_grade(overall_score),
            'recommendations': self._get_health_recommendations(
                missing_score, duplicate_score, type_consistency_score, outlier_score
            )
        }
    
    def _get_health_grade(self, score: float) -> str:
        """Get letter grade for health score."""
        if score >= 90:
            return "A - Excellent"
        elif score >= 80:
            return "B - Good"
        elif score >= 70:
            return "C - Fair"
        elif score >= 60:
            return "D - Poor"
        else:
            return "F - Critical"
    
    def _get_health_recommendations(self, missing: float, duplicate: float, 
                                   consistency: float, outlier: float) -> List[str]:
        """Generate recommendations based on health scores."""
        recommendations = []
        
        if missing < 90:
            recommendations.append("⚠️ Handle missing values using imputation or removal")
        if duplicate < 90:
            recommendations.append("⚠️ Remove duplicate rows to improve data quality")
        if consistency < 90:
            recommendations.append("⚠️ Check data type consistency across columns")
        if outlier < 80:
            recommendations.append("⚠️ Investigate and handle outliers appropriately")
        
        if not recommendations:
            recommendations.append("✅ Data is in excellent condition!")
        
        return recommendations
    
    def generate_correlation_insights(self, threshold: float = 0.7) -> List[str]:
        """
        Generate insights about correlations in the data.
        
        Args:
            threshold: Correlation threshold for strong relationships
            
        Returns:
            List of correlation insights
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return ["Not enough numerical columns for correlation analysis."]
        
        corr_matrix = self.df[numeric_cols].corr()
        insights = []
        
        # Find strong correlations
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                
                if abs(corr_value) >= threshold:
                    if corr_value > 0:
                        insights.append(
                            f"📈 Strong positive correlation ({corr_value:.2f}) between "
                            f"'{col1}' and '{col2}'"
                        )
                    else:
                        insights.append(
                            f"📉 Strong negative correlation ({corr_value:.2f}) between "
                            f"'{col1}' and '{col2}'"
                        )
        
        if not insights:
            insights.append(f"No strong correlations (>={threshold}) found in the data.")
        
        return insights
    
    def detect_feature_importance_hints(self) -> Dict:
        """
        Provide hints about potentially important features.
        
        Returns:
            Dict with feature importance hints
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        hints = {
            'high_variance_features': [],
            'low_cardinality_categories': [],
            'potential_target_variables': [],
            'timestamp_features': []
        }
        
        # High variance features
        for col in numeric_cols:
            cv = self.df[col].std() / self.df[col].mean() if self.df[col].mean() != 0 else 0
            if cv > 0.5:
                hints['high_variance_features'].append({
                    'column': col,
                    'coefficient_of_variation': round(cv, 2)
                })
        
        # Low cardinality categorical features (good for classification)
        for col in categorical_cols:
            unique_count = self.df[col].nunique()
            if 2 <= unique_count <= 10:
                hints['low_cardinality_categories'].append({
                    'column': col,
                    'unique_values': unique_count
                })
        
        # Potential target variables (binary or low cardinality numeric)
        for col in numeric_cols:
            unique_count = self.df[col].nunique()
            if unique_count <= 10:
                hints['potential_target_variables'].append({
                    'column': col,
                    'unique_values': unique_count,
                    'type': 'numeric'
                })
        
        # Detect potential timestamp columns
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp', 'year', 'month']):
                hints['timestamp_features'].append(col)
        
        return hints
    
    def suggest_preprocessing_steps(self) -> List[Dict]:
        """
        Suggest preprocessing steps based on data characteristics.
        
        Returns:
            List of suggested preprocessing steps
        """
        suggestions = []
        
        # Check for missing values
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            cols_with_missing = missing[missing > 0].index.tolist()
            suggestions.append({
                'step': 'Handle Missing Values',
                'priority': 'High',
                'reason': f'Found missing values in {len(cols_with_missing)} column(s)',
                'columns': cols_with_missing,
                'recommended_action': 'Use mean/median imputation for numeric, mode for categorical'
            })
        
        # Check for duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            suggestions.append({
                'step': 'Remove Duplicates',
                'priority': 'High',
                'reason': f'Found {duplicates} duplicate row(s)',
                'recommended_action': 'Remove duplicate rows to avoid bias'
            })
        
        # Check for outliers
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outlier_cols = []
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > len(self.df) * 0.05:  # More than 5% outliers
                outlier_cols.append(col)
        
        if outlier_cols:
            suggestions.append({
                'step': 'Handle Outliers',
                'priority': 'Medium',
                'reason': f'Significant outliers detected in {len(outlier_cols)} column(s)',
                'columns': outlier_cols,
                'recommended_action': 'Use IQR method to cap or remove outliers'
            })
        
        # Check if normalization is needed
        if len(numeric_cols) > 0:
            scales_vary = False
            means = self.df[numeric_cols].mean()
            stds = self.df[numeric_cols].std()
            
            if means.max() / (means.min() + 1e-10) > 10 or stds.max() / (stds.min() + 1e-10) > 10:
                scales_vary = True
            
            if scales_vary:
                suggestions.append({
                    'step': 'Normalize/Scale Features',
                    'priority': 'Medium',
                    'reason': 'Features have different scales',
                    'recommended_action': 'Use StandardScaler or MinMaxScaler for ML models'
                })
        
        return suggestions
    
    def generate_chart_insights(self, chart_type: str, data: pd.Series or pd.DataFrame) -> str:
        """
        Generate automatic insights for charts.
        
        Args:
            chart_type: Type of chart (histogram, boxplot, correlation, etc.)
            data: Data used in the chart
            
        Returns:
            Insight string
        """
        insights = []
        
        if chart_type == "histogram":
            if isinstance(data, pd.Series):
                mean_val = data.mean()
                median_val = data.median()
                skew = data.skew()
                
                insights.append(f"Mean: {mean_val:.2f}, Median: {median_val:.2f}")
                
                if abs(skew) < 0.5:
                    insights.append("Distribution appears to be approximately symmetric")
                elif skew > 0.5:
                    insights.append("Distribution is right-skewed (positive skew)")
                else:
                    insights.append("Distribution is left-skewed (negative skew)")
        
        elif chart_type == "correlation":
            if isinstance(data, pd.DataFrame):
                corr_matrix = data.corr()
                max_corr = corr_matrix.abs().unstack().sort_values(ascending=False)
                # Skip diagonal (self-correlations)
                max_corr = max_corr[max_corr < 1.0]
                
                if len(max_corr) > 0:
                    highest_pair = max_corr.index[0]
                    highest_value = max_corr.iloc[0]
                    insights.append(
                        f"Strongest correlation: {highest_pair[0]} ↔ {highest_pair[1]} (r={highest_value:.2f})"
                    )
        
        return " | ".join(insights) if insights else "No specific insights available"
    
    def auto_recommend_chart(self, column: str) -> List[str]:
        """
        Recommend appropriate chart types for a column.
        
        Args:
            column: Column name
            
        Returns:
            List of recommended chart types
        """
        recommendations = []
        
        if column not in self.df.columns:
            return ["Column not found"]
        
        col_data = self.df[column]
        dtype = col_data.dtype
        unique_count = col_data.nunique()
        
        # Numeric columns
        if pd.api.types.is_numeric_dtype(dtype):
            recommendations.append("Histogram - View distribution")
            recommendations.append("Box Plot - Identify outliers")
            
            if unique_count <= 20:
                recommendations.append("Bar Chart - Compare values")
            else:
                recommendations.append("Line Chart - Show trends (if ordered)")
        
        # Categorical columns
        elif pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
            if unique_count <= 20:
                recommendations.append("Bar Chart - Compare categories")
                recommendations.append("Pie Chart - Show proportions")
            else:
                recommendations.append("Bar Chart (top 10) - Show most common values")
        
        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            recommendations.append("Line Chart - Time series trend")
            recommendations.append("Area Chart - Cumulative trends")
        
        return recommendations if recommendations else ["No specific recommendations"]
