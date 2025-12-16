"""
Report Generator Module
Generates PDF reports summarizing EDA and preprocessing steps.
"""

from fpdf import FPDF
import pandas as pd
from datetime import datetime
from typing import List, Dict
import io
import matplotlib.pyplot as plt
import base64


class ReportGenerator(FPDF):
    """Generate PDF reports for data analysis."""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """Add header to each page."""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Data Analysis Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title: str):
        """Add a chapter title."""
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)
    
    def chapter_body(self, body: str):
        """Add chapter body text."""
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()
    
    def add_table(self, data: pd.DataFrame, title: str = None):
        """
        Add a table to the report.
        
        Args:
            data: DataFrame to display as table
            title: Optional title for the table
        """
        if title:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1)
        
        # Limit rows and columns for PDF
        max_rows = 20
        max_cols = 8
        
        if len(data) > max_rows:
            data = data.head(max_rows)
        
        if len(data.columns) > max_cols:
            data = data.iloc[:, :max_cols]
        
        self.set_font('Arial', 'B', 9)
        
        # Calculate column widths
        col_width = (self.w - 20) / len(data.columns)
        row_height = 7
        
        # Header
        for col in data.columns:
            self.cell(col_width, row_height, str(col)[:20], 1, 0, 'C')
        self.ln()
        
        # Data rows
        self.set_font('Arial', '', 8)
        for idx, row in data.iterrows():
            for value in row:
                # Format value
                if isinstance(value, float):
                    display_value = f'{value:.2f}'
                else:
                    display_value = str(value)[:20]
                self.cell(col_width, row_height, display_value, 1, 0, 'C')
            self.ln()
        
        self.ln(5)
    
    def add_key_value_pairs(self, data: Dict, title: str = None):
        """
        Add key-value pairs to the report.
        
        Args:
            data: Dictionary of key-value pairs
            title: Optional title
        """
        if title:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1)
        
        self.set_font('Arial', '', 10)
        for key, value in data.items():
            if isinstance(value, float):
                display_value = f'{value:.4f}'
            elif isinstance(value, dict):
                display_value = str(value)[:50]
            else:
                display_value = str(value)
            
            self.cell(0, 6, f'{key}: {display_value}', 0, 1)
        
        self.ln(5)
    
    def generate_report(self, 
                       file_info: Dict,
                       overview: Dict,
                       statistical_summary: pd.DataFrame,
                       operations_log: List[str],
                       output_path: str = 'report.pdf'):
        """
        Generate a complete EDA report.
        
        Args:
            file_info: File information dictionary
            overview: Dataset overview dictionary
            statistical_summary: Statistical summary DataFrame
            operations_log: List of operations performed
            output_path: Path to save the PDF report
        """
        self.add_page()
        
        # Executive Summary
        self.chapter_title('1. Executive Summary')
        summary_text = f'''This report provides a comprehensive analysis of the dataset "{file_info.get('file_name', 'Unknown')}".
The dataset contains {overview.get('shape', (0, 0))[0]} rows and {overview.get('shape', (0, 0))[1]} columns.
Memory usage: {file_info.get('size_mb', 0):.2f} MB.'''
        self.chapter_body(summary_text)
        
        # Dataset Information
        self.chapter_title('2. Dataset Information')
        self.add_key_value_pairs({
            'Number of Rows': overview.get('shape', (0, 0))[0],
            'Number of Columns': overview.get('shape', (0, 0))[1],
            'Duplicate Rows': overview.get('duplicate_rows', 0),
            'Memory Usage (MB)': f"{overview.get('memory_usage_mb', 0):.2f}"
        })
        
        # Column Information
        self.chapter_title('3. Column Information')
        if 'columns' in overview:
            self.chapter_body(f"Columns: {', '.join(overview['columns'][:10])}")
            if len(overview['columns']) > 10:
                self.chapter_body(f"... and {len(overview['columns']) - 10} more columns")
        
        # Missing Values
        self.chapter_title('4. Missing Values Summary')
        missing_data = {k: v for k, v in overview.get('missing_values', {}).items() if v > 0}
        if missing_data:
            self.add_key_value_pairs(missing_data, 'Missing Values by Column')
        else:
            self.chapter_body('No missing values found in the dataset.')
        
        # Statistical Summary
        if not statistical_summary.empty:
            self.add_page()
            self.chapter_title('5. Statistical Summary')
            self.add_table(statistical_summary.T, 'Descriptive Statistics (Top 10 columns)')
        
        # Operations Log
        if operations_log:
            self.add_page()
            self.chapter_title('6. Operations Performed')
            for idx, operation in enumerate(operations_log, 1):
                self.chapter_body(f'{idx}. {operation}')
        
        # Save report
        self.output(output_path)
        
        return output_path


def create_simple_report(file_info: Dict, overview: Dict, stats: pd.DataFrame, 
                        operations: List[str], output_path: str = 'report.pdf') -> str:
    """
    Helper function to create a simple report.
    
    Args:
        file_info: File information
        overview: Dataset overview
        stats: Statistical summary
        operations: List of operations performed
        output_path: Output file path
        
    Returns:
        str: Path to generated report
    """
    report = ReportGenerator()
    return report.generate_report(file_info, overview, stats, operations, output_path)
