"""
Caching utilities for performance optimization.
Uses Streamlit's caching mechanisms to speed up data processing.
"""

import streamlit as st
import pandas as pd
import hashlib
from functools import wraps


def generate_data_hash(df: pd.DataFrame) -> str:
    """
    Generate a hash for a dataframe for caching purposes.
    
    Args:
        df: DataFrame to hash
        
    Returns:
        Hash string
    """
    # Create hash from dataframe shape and first few rows
    data_str = f"{df.shape}_{df.head().to_json()}"
    return hashlib.md5(data_str.encode()).hexdigest()


@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_correlation_matrix(df_hash: str, df: pd.DataFrame, method: str = 'pearson'):
    """
    Calculate correlation matrix with caching.
    
    Args:
        df_hash: Hash of the dataframe for cache invalidation
        df: DataFrame
        method: Correlation method
        
    Returns:
        Correlation matrix
    """
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) < 2:
        return None
    return df[numeric_cols].corr(method=method)


@st.cache_data(ttl=3600)
def cached_statistics(df_hash: str, df: pd.DataFrame):
    """
    Calculate statistics with caching.
    
    Args:
        df_hash: Hash of the dataframe for cache invalidation
        df: DataFrame
        
    Returns:
        Statistics dataframe
    """
    return df.describe()


@st.cache_data(ttl=3600)
def cached_value_counts(df_hash: str, series: pd.Series, top_n: int = 10):
    """
    Calculate value counts with caching.
    
    Args:
        df_hash: Hash for cache invalidation
        series: Series to count
        top_n: Number of top values to return
        
    Returns:
        Value counts
    """
    return series.value_counts().head(top_n)


def cache_info():
    """Display cache information."""
    try:
        cache_stats = st.cache_data.get_stats()
        return cache_stats
    except:
        return "Cache statistics not available"


def clear_all_caches():
    """Clear all Streamlit caches."""
    st.cache_data.clear()
    st.cache_resource.clear()
