"""
Statistical Analysis Module
Provides advanced statistical analysis capabilities including descriptive, inferential,
correlation, time series, and probability analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import (
    ttest_ind, ttest_1samp, f_oneway, chi2_contingency,
    pearsonr, spearmanr, kendalltau, shapiro, normaltest,
    kstest, anderson
)
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf, grangercausalitytests
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class StatisticalAnalysis:
    """Perform advanced statistical analysis on DataFrame."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    # ========== DESCRIPTIVE STATISTICS ==========
    
    def get_descriptive_statistics(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calculate comprehensive descriptive statistics.
        
        Args:
            columns: List of columns to analyze. If None, use all numerical columns.
            
        Returns:
            pd.DataFrame: Descriptive statistics including mean, median, mode, std, variance,
                         skewness, kurtosis, min, max, and quantiles.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not columns:
            return pd.DataFrame()
        
        stats_dict = {}
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            data = self.df[col].dropna()
            
            if len(data) == 0:
                continue
            
            stats_dict[col] = {
                'count': len(data),
                'mean': data.mean(),
                'median': data.median(),
                'mode': data.mode()[0] if not data.mode().empty else np.nan,
                'std': data.std(),
                'variance': data.var(),
                'min': data.min(),
                'max': data.max(),
                'range': data.max() - data.min(),
                'q1': data.quantile(0.25),
                'q2': data.quantile(0.50),
                'q3': data.quantile(0.75),
                'iqr': data.quantile(0.75) - data.quantile(0.25),
                'skewness': data.skew(),
                'kurtosis': data.kurtosis(),
                'cv': (data.std() / data.mean() * 100) if data.mean() != 0 else np.nan  # coefficient of variation
            }
        
        return pd.DataFrame(stats_dict).T
    
    # ========== INFERENTIAL STATISTICS ==========
    
    def perform_ttest_ind(self, col1: str, col2: str) -> Dict:
        """
        Perform independent samples t-test.
        
        Args:
            col1: First column name
            col2: Second column name
            
        Returns:
            Dict: Test results including t-statistic, p-value, and interpretation
        """
        data1 = self.df[col1].dropna()
        data2 = self.df[col2].dropna()
        
        statistic, pvalue = ttest_ind(data1, data2)
        
        return {
            'test': 'Independent T-Test',
            'columns': [col1, col2],
            't_statistic': statistic,
            'p_value': pvalue,
            'significant': pvalue < 0.05,
            'interpretation': f"{'Reject' if pvalue < 0.05 else 'Fail to reject'} null hypothesis (α=0.05)"
        }
    
    def perform_ttest_1samp(self, column: str, population_mean: float) -> Dict:
        """
        Perform one-sample t-test.
        
        Args:
            column: Column name
            population_mean: Hypothesized population mean
            
        Returns:
            Dict: Test results
        """
        data = self.df[column].dropna()
        statistic, pvalue = ttest_1samp(data, population_mean)
        
        return {
            'test': 'One-Sample T-Test',
            'column': column,
            'population_mean': population_mean,
            'sample_mean': data.mean(),
            't_statistic': statistic,
            'p_value': pvalue,
            'significant': pvalue < 0.05,
            'interpretation': f"{'Reject' if pvalue < 0.05 else 'Fail to reject'} null hypothesis (α=0.05)"
        }
    
    def perform_anova(self, columns: List[str]) -> Dict:
        """
        Perform one-way ANOVA test.
        
        Args:
            columns: List of columns to compare
            
        Returns:
            Dict: ANOVA results
        """
        groups = [self.df[col].dropna() for col in columns]
        statistic, pvalue = f_oneway(*groups)
        
        return {
            'test': 'One-Way ANOVA',
            'columns': columns,
            'f_statistic': statistic,
            'p_value': pvalue,
            'significant': pvalue < 0.05,
            'interpretation': f"{'Reject' if pvalue < 0.05 else 'Fail to reject'} null hypothesis (α=0.05)"
        }
    
    def perform_chi_square(self, col1: str, col2: str) -> Dict:
        """
        Perform chi-square test of independence for categorical variables.
        
        Args:
            col1: First categorical column
            col2: Second categorical column
            
        Returns:
            Dict: Chi-square test results
        """
        contingency_table = pd.crosstab(self.df[col1], self.df[col2])
        chi2, pvalue, dof, expected = chi2_contingency(contingency_table)
        
        return {
            'test': 'Chi-Square Test of Independence',
            'columns': [col1, col2],
            'chi2_statistic': chi2,
            'p_value': pvalue,
            'degrees_of_freedom': dof,
            'significant': pvalue < 0.05,
            'interpretation': f"Variables are {'dependent' if pvalue < 0.05 else 'independent'} (α=0.05)"
        }
    
    def calculate_confidence_interval(self, column: str, confidence: float = 0.95) -> Dict:
        """
        Calculate confidence interval for a column.
        
        Args:
            column: Column name
            confidence: Confidence level (default 0.95 for 95%)
            
        Returns:
            Dict: Confidence interval bounds and related statistics
        """
        data = self.df[column].dropna()
        mean = data.mean()
        sem = stats.sem(data)
        interval = stats.t.interval(confidence, len(data)-1, loc=mean, scale=sem)
        
        return {
            'column': column,
            'mean': mean,
            'confidence_level': confidence,
            'lower_bound': interval[0],
            'upper_bound': interval[1],
            'margin_of_error': interval[1] - mean,
            'sample_size': len(data)
        }
    
    # ========== CORRELATION AND CAUSALITY ==========
    
    def calculate_correlations(self, columns: Optional[List[str]] = None, 
                              method: str = 'pearson') -> pd.DataFrame:
        """
        Calculate correlation matrix using specified method.
        
        Args:
            columns: List of columns. If None, use all numerical columns.
            method: Correlation method ('pearson', 'spearman', 'kendall')
            
        Returns:
            pd.DataFrame: Correlation matrix
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not columns:
            return pd.DataFrame()
        
        return self.df[columns].corr(method=method)
    
    def get_pairwise_correlations(self, columns: Optional[List[str]] = None) -> Dict:
        """
        Calculate pairwise correlations using all three methods.
        
        Args:
            columns: List of columns. If None, use all numerical columns.
            
        Returns:
            Dict: Dictionary with Pearson, Spearman, and Kendall correlations
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        return {
            'pearson': self.calculate_correlations(columns, 'pearson'),
            'spearman': self.calculate_correlations(columns, 'spearman'),
            'kendall': self.calculate_correlations(columns, 'kendall')
        }
    
    def create_correlation_heatmap(self, columns: Optional[List[str]] = None,
                                   method: str = 'pearson') -> go.Figure:
        """
        Create interactive correlation heatmap.
        
        Args:
            columns: List of columns to include
            method: Correlation method ('pearson', 'spearman', 'kendall')
            
        Returns:
            go.Figure: Plotly heatmap figure
        """
        corr_matrix = self.calculate_correlations(columns, method)
        
        if corr_matrix.empty:
            return None
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.3f}',
            textfont={"size": 10},
            colorbar=dict(title=f"{method.capitalize()} Correlation")
        ))
        
        fig.update_layout(
            title=f"{method.capitalize()} Correlation Heatmap",
            xaxis_title="Features",
            yaxis_title="Features",
            height=600,
            width=700
        )
        
        return fig
    
    def perform_granger_causality(self, col1: str, col2: str, max_lag: int = 5) -> Dict:
        """
        Perform Granger causality test for time series.
        
        Args:
            col1: First time series column (cause)
            col2: Second time series column (effect)
            max_lag: Maximum lag to test
            
        Returns:
            Dict: Granger causality test results
        """
        try:
            data = self.df[[col1, col2]].dropna()
            
            if len(data) < max_lag + 1:
                return {
                    'error': 'Insufficient data for Granger causality test',
                    'min_required': max_lag + 1,
                    'available': len(data)
                }
            
            # Perform Granger causality test
            result = grangercausalitytests(data[[col2, col1]], maxlag=max_lag, verbose=False)
            
            # Extract p-values for each lag
            p_values = {}
            for lag in range(1, max_lag + 1):
                p_values[f'lag_{lag}'] = result[lag][0]['ssr_ftest'][1]
            
            # Check if any lag is significant
            min_p_value = min(p_values.values())
            
            return {
                'test': 'Granger Causality Test',
                'cause': col1,
                'effect': col2,
                'max_lag': max_lag,
                'p_values': p_values,
                'min_p_value': min_p_value,
                'significant': min_p_value < 0.05,
                'interpretation': f"{col1} {'does' if min_p_value < 0.05 else 'does not'} Granger-cause {col2} (α=0.05)"
            }
        except Exception as e:
            return {
                'error': str(e),
                'test': 'Granger Causality Test',
                'cause': col1,
                'effect': col2
            }
    
    # ========== TIME SERIES ANALYSIS ==========
    
    def decompose_time_series(self, column: str, period: int = 12, 
                             model: str = 'additive') -> Dict:
        """
        Decompose time series into trend, seasonal, and residual components.
        
        Args:
            column: Time series column name
            period: Period for seasonal decomposition
            model: 'additive' or 'multiplicative'
            
        Returns:
            Dict: Decomposed components
        """
        try:
            data = self.df[column].dropna()
            
            if len(data) < 2 * period:
                return {
                    'error': f'Insufficient data. Need at least {2 * period} points, got {len(data)}'
                }
            
            decomposition = seasonal_decompose(data, model=model, period=period, extrapolate_trend='freq')
            
            return {
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid,
                'original': data
            }
        except Exception as e:
            return {'error': str(e)}
    
    def create_decomposition_plot(self, column: str, period: int = 12,
                                 model: str = 'additive') -> go.Figure:
        """
        Create plot showing time series decomposition.
        
        Args:
            column: Time series column name
            period: Period for seasonal decomposition
            model: 'additive' or 'multiplicative'
            
        Returns:
            go.Figure: Plotly figure with decomposition plots
        """
        decomp = self.decompose_time_series(column, period, model)
        
        if 'error' in decomp:
            return None
        
        fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=['Original', 'Trend', 'Seasonal', 'Residual'],
            vertical_spacing=0.08
        )
        
        # Original
        fig.add_trace(
            go.Scatter(y=decomp['original'], mode='lines', name='Original'),
            row=1, col=1
        )
        
        # Trend
        fig.add_trace(
            go.Scatter(y=decomp['trend'], mode='lines', name='Trend'),
            row=2, col=1
        )
        
        # Seasonal
        fig.add_trace(
            go.Scatter(y=decomp['seasonal'], mode='lines', name='Seasonal'),
            row=3, col=1
        )
        
        # Residual
        fig.add_trace(
            go.Scatter(y=decomp['residual'], mode='lines', name='Residual'),
            row=4, col=1
        )
        
        fig.update_layout(
            title=f"Time Series Decomposition - {column}",
            height=800,
            showlegend=False
        )
        
        return fig
    
    def test_stationarity(self, column: str) -> Dict:
        """
        Test stationarity using Augmented Dickey-Fuller test.
        
        Args:
            column: Time series column name
            
        Returns:
            Dict: Stationarity test results
        """
        data = self.df[column].dropna()
        
        result = adfuller(data, autolag='AIC')
        
        return {
            'test': 'Augmented Dickey-Fuller Test',
            'column': column,
            'adf_statistic': result[0],
            'p_value': result[1],
            'n_lags': result[2],
            'n_observations': result[3],
            'critical_values': result[4],
            'stationary': result[1] < 0.05,
            'interpretation': f"Series is {'stationary' if result[1] < 0.05 else 'non-stationary'} (α=0.05)"
        }
    
    def calculate_autocorrelation(self, column: str, nlags: int = 40) -> Dict:
        """
        Calculate autocorrelation and partial autocorrelation.
        
        Args:
            column: Time series column name
            nlags: Number of lags
            
        Returns:
            Dict: ACF and PACF values
        """
        data = self.df[column].dropna()
        
        acf_values = acf(data, nlags=nlags, fft=False)
        pacf_values = pacf(data, nlags=nlags, method='ywm')
        
        return {
            'acf': acf_values,
            'pacf': pacf_values,
            'lags': list(range(len(acf_values)))
        }
    
    def create_acf_pacf_plot(self, column: str, nlags: int = 40) -> go.Figure:
        """
        Create ACF and PACF plots.
        
        Args:
            column: Time series column name
            nlags: Number of lags
            
        Returns:
            go.Figure: Plotly figure with ACF and PACF plots
        """
        autocorr = self.calculate_autocorrelation(column, nlags)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Autocorrelation (ACF)', 'Partial Autocorrelation (PACF)']
        )
        
        # ACF
        fig.add_trace(
            go.Bar(x=autocorr['lags'], y=autocorr['acf'], name='ACF'),
            row=1, col=1
        )
        
        # PACF
        fig.add_trace(
            go.Bar(x=autocorr['lags'], y=autocorr['pacf'], name='PACF'),
            row=1, col=2
        )
        
        # Add confidence intervals
        conf_interval = 1.96 / np.sqrt(len(self.df[column].dropna()))
        fig.add_hline(y=conf_interval, line_dash="dash", line_color="red", row=1, col=1)
        fig.add_hline(y=-conf_interval, line_dash="dash", line_color="red", row=1, col=1)
        fig.add_hline(y=conf_interval, line_dash="dash", line_color="red", row=1, col=2)
        fig.add_hline(y=-conf_interval, line_dash="dash", line_color="red", row=1, col=2)
        
        fig.update_layout(
            title=f"ACF and PACF - {column}",
            height=400,
            showlegend=False
        )
        
        return fig
    
    # ========== PROBABILITY ANALYSIS ==========
    
    def fit_distribution(self, column: str, distribution: str = 'norm') -> Dict:
        """
        Fit a statistical distribution to the data.
        
        Args:
            column: Column name
            distribution: Distribution type ('norm', 'expon', 'gamma', 'beta', 'lognorm', 'poisson')
            
        Returns:
            Dict: Distribution parameters and goodness of fit
        """
        data = self.df[column].dropna()
        
        try:
            if distribution == 'norm':
                params = stats.norm.fit(data)
                ks_stat, p_value = kstest(data, 'norm', args=params)
                
                return {
                    'distribution': 'Normal',
                    'parameters': {'mean': params[0], 'std': params[1]},
                    'ks_statistic': ks_stat,
                    'p_value': p_value,
                    'fit_quality': 'good' if p_value > 0.05 else 'poor'
                }
            
            elif distribution == 'expon':
                params = stats.expon.fit(data)
                ks_stat, p_value = kstest(data, 'expon', args=params)
                
                return {
                    'distribution': 'Exponential',
                    'parameters': {'loc': params[0], 'scale': params[1]},
                    'ks_statistic': ks_stat,
                    'p_value': p_value,
                    'fit_quality': 'good' if p_value > 0.05 else 'poor'
                }
            
            elif distribution == 'gamma':
                params = stats.gamma.fit(data)
                ks_stat, p_value = kstest(data, 'gamma', args=params)
                
                return {
                    'distribution': 'Gamma',
                    'parameters': {'a': params[0], 'loc': params[1], 'scale': params[2]},
                    'ks_statistic': ks_stat,
                    'p_value': p_value,
                    'fit_quality': 'good' if p_value > 0.05 else 'poor'
                }
            
            elif distribution == 'lognorm':
                params = stats.lognorm.fit(data)
                ks_stat, p_value = kstest(data, 'lognorm', args=params)
                
                return {
                    'distribution': 'Log-Normal',
                    'parameters': {'s': params[0], 'loc': params[1], 'scale': params[2]},
                    'ks_statistic': ks_stat,
                    'p_value': p_value,
                    'fit_quality': 'good' if p_value > 0.05 else 'poor'
                }
            
            else:
                return {'error': f'Unsupported distribution: {distribution}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def create_distribution_plot(self, column: str, distribution: str = 'norm') -> go.Figure:
        """
        Create histogram with fitted distribution overlay.
        
        Args:
            column: Column name
            distribution: Distribution type
            
        Returns:
            go.Figure: Plotly figure with histogram and PDF
        """
        data = self.df[column].dropna()
        fit_result = self.fit_distribution(column, distribution)
        
        if 'error' in fit_result:
            return None
        
        fig = go.Figure()
        
        # Histogram
        fig.add_trace(go.Histogram(
            x=data,
            name='Data',
            nbinsx=30,
            histnorm='probability density',
            opacity=0.7
        ))
        
        # Fitted distribution
        x_range = np.linspace(data.min(), data.max(), 100)
        
        if distribution == 'norm':
            params = fit_result['parameters']
            y_fitted = stats.norm.pdf(x_range, params['mean'], params['std'])
        elif distribution == 'expon':
            params = fit_result['parameters']
            y_fitted = stats.expon.pdf(x_range, params['loc'], params['scale'])
        elif distribution == 'gamma':
            params = fit_result['parameters']
            y_fitted = stats.gamma.pdf(x_range, params['a'], params['loc'], params['scale'])
        elif distribution == 'lognorm':
            params = fit_result['parameters']
            y_fitted = stats.lognorm.pdf(x_range, params['s'], params['loc'], params['scale'])
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_fitted,
            mode='lines',
            name=f'Fitted {fit_result["distribution"]}',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title=f'{fit_result["distribution"]} Distribution Fit - {column}',
            xaxis_title=column,
            yaxis_title='Probability Density',
            height=500
        )
        
        return fig
    
    def calculate_probabilities(self, column: str) -> Dict:
        """
        Calculate various probabilities and expected values.
        
        Args:
            column: Column name
            
        Returns:
            Dict: Probability statistics
        """
        data = self.df[column].dropna()
        
        return {
            'expected_value': data.mean(),
            'variance': data.var(),
            'std': data.std(),
            'median': data.median(),
            'mode': data.mode()[0] if not data.mode().empty else np.nan,
            'range': (data.min(), data.max()),
            'iqr': data.quantile(0.75) - data.quantile(0.25),
            'coefficient_of_variation': (data.std() / data.mean() * 100) if data.mean() != 0 else np.nan
        }
