"""
Data Handler Module
Handles file upload, parsing, and DataFrame conversion for multiple file formats.
"""

import pandas as pd
import json
from io import StringIO, BytesIO
from typing import Optional, Union


class DataHandler:
    """Handle data loading and parsing from various file formats."""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.file_name: Optional[str] = None
        self.file_type: Optional[str] = None
    
    def load_data(self, uploaded_file) -> pd.DataFrame:
        """
        Load data from uploaded file and convert to pandas DataFrame.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            pd.DataFrame: Parsed data as DataFrame
            
        Raises:
            ValueError: If file format is not supported
        """
        self.file_name = uploaded_file.name
        self.file_type = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if self.file_type == 'csv':
                self.df = pd.read_csv(uploaded_file)
            elif self.file_type in ['xlsx', 'xls']:
                self.df = pd.read_excel(uploaded_file)
            elif self.file_type == 'json':
                content = uploaded_file.read()
                json_data = json.loads(content)
                self.df = pd.json_normalize(json_data) if isinstance(json_data, list) else pd.DataFrame([json_data])
            elif self.file_type == 'txt':
                content = uploaded_file.read().decode('utf-8')
                # Try to parse as CSV with various delimiters
                for delimiter in [',', '\t', ';', '|']:
                    try:
                        self.df = pd.read_csv(StringIO(content), delimiter=delimiter)
                        if len(self.df.columns) > 1:
                            break
                    except:
                        continue
                if self.df is None or len(self.df.columns) == 1:
                    # If still not parsed, treat as single column
                    lines = content.strip().split('\n')
                    self.df = pd.DataFrame({'data': lines})
            else:
                raise ValueError(f"Unsupported file format: {self.file_type}")
            
            return self.df
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """Return the current DataFrame."""
        return self.df
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """Set the current DataFrame."""
        self.df = df
    
    def get_file_info(self) -> dict:
        """Get information about the loaded file."""
        if self.df is None:
            return {}
        
        return {
            'file_name': self.file_name,
            'file_type': self.file_type,
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'size_mb': self.df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
