"""
AI-EDA Assistant - Main Streamlit Application
An AI-driven tool for automated exploratory data analysis and preprocessing.
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from datetime import datetime

# Import custom modules
from data_handler import DataHandler
from eda import EDA
from preprocessing import Preprocessor
from data_integrity import DataIntegrity
from model_training import ModelTrainer
from code_generator import CodeGenerator
from report_generator import create_simple_report

# Page configuration
st.set_page_config(
    page_title="AI-EDA Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler()
if 'operations_log' not in st.session_state:
    st.session_state.operations_log = []
if 'code_generator' not in st.session_state:
    st.session_state.code_generator = CodeGenerator()


def main():
    """Main application function."""
    
    # Title and description
    st.title("📊 AI-EDA Assistant")
    st.markdown("""
    An intelligent data analysis assistant that helps you perform exploratory data analysis (EDA) 
    and preprocessing tasks with ease.
    """)
    
    # Sidebar for file upload and navigation
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload your dataset",
            type=['csv', 'xlsx', 'xls', 'json', 'txt'],
            help="Supported formats: CSV, Excel, JSON, TXT"
        )
        
        if uploaded_file is not None:
            try:
                if st.session_state.df is None or st.button("Reload Data"):
                    df = st.session_state.data_handler.load_data(uploaded_file)
                    st.session_state.df = df.copy()
                    st.session_state.original_df = df.copy()
                    st.success(f"✅ Data loaded successfully!")
                    
                    file_info = st.session_state.data_handler.get_file_info()
                    st.info(f"📏 Shape: {file_info['rows']} rows × {file_info['columns']} columns")
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        st.markdown("---")
        
        # Navigation
        st.header("🧭 Navigation")
        page = st.radio(
            "Select Task",
            ["📊 Dataset Overview", 
             "🔍 Automated EDA", 
             "🧹 Preprocessing",
             "✅ Data Integrity",
             "🤖 Model Training",
             "💾 Export & Reports"]
        )
    
    # Main content area
    if st.session_state.df is None:
        st.info("👆 Please upload a dataset to get started.")
        
        # Example usage
        with st.expander("ℹ️ How to use this app"):
            st.markdown("""
            ### Steps to get started:
            
            1. **Upload Data**: Use the file uploader in the sidebar to upload your dataset
            2. **Explore Data**: View dataset overview and statistics
            3. **Run EDA**: Generate automated visualizations and insights
            4. **Preprocess**: Handle missing values, outliers, and normalize data
            5. **Check Integrity**: Validate data quality and consistency
            6. **Train Models**: Build basic machine learning models
            7. **Export**: Download processed data, reports, and Python code
            
            ### Supported File Formats:
            - CSV (.csv)
            - Excel (.xlsx, .xls)
            - JSON (.json)
            - Text (.txt)
            """)
        
        return
    
    # Route to selected page
    if page == "📊 Dataset Overview":
        show_dataset_overview()
    elif page == "🔍 Automated EDA":
        show_automated_eda()
    elif page == "🧹 Preprocessing":
        show_preprocessing()
    elif page == "✅ Data Integrity":
        show_data_integrity()
    elif page == "🤖 Model Training":
        show_model_training()
    elif page == "💾 Export & Reports":
        show_export_reports()


def show_dataset_overview():
    """Display dataset overview page."""
    st.header("📊 Dataset Overview")
    
    df = st.session_state.df
    
    # Basic information
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Memory (MB)", f"{df.memory_usage(deep=True).sum() / (1024**2):.2f}")
    with col4:
        st.metric("Duplicates", df.duplicated().sum())
    
    # Data preview
    st.subheader("Data Preview")
    n_rows = st.slider("Number of rows to display", 5, 100, 10)
    st.dataframe(df.head(n_rows), use_container_width=True)
    
    # Column information
    st.subheader("Column Information")
    col_info = pd.DataFrame({
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum(),
        'Null %': (df.isnull().sum() / len(df) * 100).round(2),
        'Unique Values': df.nunique()
    })
    st.dataframe(col_info, use_container_width=True)


def show_automated_eda():
    """Display automated EDA page."""
    st.header("🔍 Automated Exploratory Data Analysis")
    
    df = st.session_state.df
    eda = EDA(df)
    
    # Statistical Summary
    st.subheader("📈 Statistical Summary")
    stats = eda.get_statistical_summary()
    if not stats.empty:
        st.dataframe(stats, use_container_width=True)
    else:
        st.info("No numerical columns found for statistical summary.")
    
    # Categorical Summary
    st.subheader("📋 Categorical Summary")
    cat_summary = eda.get_categorical_summary()
    if cat_summary:
        for col, info in cat_summary.items():
            with st.expander(f"Column: {col}"):
                st.write(f"**Unique Values:** {info['unique_values']}")
                st.write(f"**Missing Values:** {info['missing']}")
                st.write("**Top Values:**")
                st.write(pd.Series(info['top_values']))
    else:
        st.info("No categorical columns found.")
    
    # Visualizations
    st.subheader("📊 Visualizations")
    
    viz_option = st.selectbox(
        "Select Visualization",
        ["Histograms", "Box Plots", "Correlation Heatmap", "Scatter Matrix", "Missing Values"]
    )
    
    if viz_option == "Histograms":
        fig = eda.create_histograms()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numerical columns available for histograms.")
    
    elif viz_option == "Box Plots":
        fig = eda.create_box_plots()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numerical columns available for box plots.")
    
    elif viz_option == "Correlation Heatmap":
        fig = eda.create_correlation_heatmap()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numerical columns for correlation heatmap.")
    
    elif viz_option == "Scatter Matrix":
        with st.spinner("Generating scatter matrix..."):
            fig = eda.create_scatter_matrix()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 numerical columns for scatter matrix.")
    
    elif viz_option == "Missing Values":
        fig = eda.get_missing_value_plot()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing values found in the dataset!")


def show_preprocessing():
    """Display preprocessing page."""
    st.header("🧹 Data Preprocessing")
    
    df = st.session_state.df
    
    # Task selection
    task = st.selectbox(
        "Select Preprocessing Task",
        ["Handle Missing Values", "Handle Outliers", "Normalize/Scale Data"]
    )
    
    if task == "Handle Missing Values":
        st.subheader("Handle Missing Values")
        
        # Show current missing values
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        
        if len(missing) == 0:
            st.success("✅ No missing values in the dataset!")
        else:
            st.warning(f"Found missing values in {len(missing)} columns:")
            st.write(missing)
            
            strategy = st.selectbox(
                "Select Strategy",
                ["mean", "median", "mode", "drop_rows", "drop_columns"]
            )
            
            columns = st.multiselect(
                "Select Columns (leave empty for all)",
                df.columns.tolist(),
                default=missing.index.tolist()
            )
            
            if st.button("Apply"):
                preprocessor = Preprocessor(df)
                df_processed = preprocessor.handle_missing_values(
                    strategy=strategy,
                    columns=columns if columns else None
                )
                st.session_state.df = df_processed
                st.session_state.operations_log.extend(preprocessor.get_operations_log())
                
                # Log for code generation
                st.session_state.code_generator.add_missing_value_handling(strategy, columns)
                
                st.success("✅ Missing values handled successfully!")
                st.experimental_rerun()
    
    elif task == "Handle Outliers":
        st.subheader("Handle Outliers")
        
        method = st.selectbox("Detection Method", ["iqr", "zscore"])
        strategy = st.selectbox("Handling Strategy", ["remove", "cap", "median"])
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        columns = st.multiselect(
            "Select Columns",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if columns and st.button("Apply"):
            preprocessor = Preprocessor(df)
            
            # Show outliers before handling
            if method == "iqr":
                outliers = preprocessor.detect_outliers_iqr(columns)
            else:
                outliers = preprocessor.detect_outliers_zscore(columns)
            
            total_outliers = sum(o.sum() for o in outliers.values())
            st.info(f"Detected {total_outliers} outliers across selected columns.")
            
            df_processed = preprocessor.handle_outliers(
                method=method,
                strategy=strategy,
                columns=columns
            )
            st.session_state.df = df_processed
            st.session_state.operations_log.extend(preprocessor.get_operations_log())
            
            # Log for code generation
            st.session_state.code_generator.add_outlier_handling(method, strategy, columns)
            
            st.success("✅ Outliers handled successfully!")
            st.experimental_rerun()
    
    elif task == "Normalize/Scale Data":
        st.subheader("Normalize/Scale Data")
        
        method = st.selectbox(
            "Normalization Method",
            ["standard", "minmax", "robust"],
            help="standard: StandardScaler, minmax: MinMaxScaler, robust: RobustScaler"
        )
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        columns = st.multiselect("Select Columns", numeric_cols, default=numeric_cols)
        
        if columns and st.button("Apply"):
            preprocessor = Preprocessor(df)
            df_processed = preprocessor.normalize_data(method=method, columns=columns)
            st.session_state.df = df_processed
            st.session_state.operations_log.extend(preprocessor.get_operations_log())
            
            # Log for code generation
            st.session_state.code_generator.add_normalization(method, columns)
            
            st.success("✅ Data normalized successfully!")
            st.experimental_rerun()
    
    # Show operations log
    if st.session_state.operations_log:
        with st.expander("📝 Operations Log"):
            for i, op in enumerate(st.session_state.operations_log, 1):
                st.write(f"{i}. {op}")
    
    # Reset option
    if st.button("🔄 Reset to Original Data"):
        st.session_state.df = st.session_state.original_df.copy()
        st.session_state.operations_log = []
        st.session_state.code_generator.clear()
        st.success("Data reset to original!")
        st.experimental_rerun()


def show_data_integrity():
    """Display data integrity page."""
    st.header("✅ Data Integrity Checks")
    
    df = st.session_state.df
    integrity = DataIntegrity(df)
    
    # Duplicates
    st.subheader("🔍 Duplicate Rows")
    dup_info = integrity.check_duplicates()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Duplicates", dup_info['total_duplicates'])
    with col2:
        st.metric("Percentage", f"{dup_info['percentage']:.2f}%")
    
    if dup_info['total_duplicates'] > 0:
        if st.button("Remove Duplicates"):
            df_clean = integrity.remove_duplicates()
            st.session_state.df = df_clean
            st.success(f"✅ Removed {dup_info['total_duplicates']} duplicate rows!")
            st.experimental_rerun()
    
    # Data Types
    st.subheader("📊 Data Type Consistency")
    type_info = integrity.check_data_types()
    
    inconsistent = {k: v for k, v in type_info.items() if not v['is_consistent']}
    if inconsistent:
        st.warning(f"Found {len(inconsistent)} columns with inconsistent types:")
        st.json(inconsistent)
    else:
        st.success("✅ All columns have consistent data types!")
    
    # Numerical Validation
    st.subheader("🔢 Numerical Data Validation")
    num_validation = integrity.validate_numerical_entries()
    
    if num_validation:
        issues = {k: v for k, v in num_validation.items() if v['has_issues']}
        if issues:
            st.warning(f"Found issues in {len(issues)} numerical columns:")
            for col, info in issues.items():
                st.write(f"**{col}**: {info['infinite_count']} infinite values")
        else:
            st.success("✅ No issues found in numerical columns!")
    
    # Categorical Consistency
    st.subheader("📋 Categorical Data Consistency")
    cat_consistency = integrity.check_categorical_consistency()
    
    if cat_consistency:
        for col, info in cat_consistency.items():
            with st.expander(f"Column: {col}"):
                st.write(f"**Unique Values:** {info['unique_values']}")
                st.write(f"**Cardinality Ratio:** {info['cardinality_ratio']:.4f}")
                if info['case_inconsistencies'] > 0:
                    st.warning(f"**Case Inconsistencies:** {info['case_inconsistencies']}")


def show_model_training():
    """Display model training page."""
    st.header("🤖 Model Training")
    
    df = st.session_state.df
    
    # Check if we have numerical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numerical columns for model training.")
        return
    
    st.info("💡 Select features and target for model training")
    
    # Model selection
    model_type = st.selectbox(
        "Select Model Type",
        ["Linear Regression", "Decision Tree", "Random Forest"]
    )
    
    task_type = st.selectbox("Task Type", ["regression", "classification"])
    
    # Feature and target selection
    target_col = st.selectbox("Select Target Column", numeric_cols)
    
    available_features = [col for col in numeric_cols if col != target_col]
    feature_cols = st.multiselect(
        "Select Feature Columns",
        available_features,
        default=available_features[:min(5, len(available_features))]
    )
    
    if not feature_cols:
        st.warning("Please select at least one feature column.")
        return
    
    # Training parameters
    col1, col2 = st.columns(2)
    with col1:
        test_size = st.slider("Test Size", 0.1, 0.5, 0.2, 0.05)
    with col2:
        if model_type in ["Decision Tree", "Random Forest"]:
            max_depth = st.slider("Max Depth", 2, 20, 5)
    
    # Train button
    if st.button("🚀 Train Model"):
        with st.spinner("Training model..."):
            try:
                trainer = ModelTrainer(df)
                trainer.prepare_data(target_col, feature_cols, test_size=test_size)
                
                if model_type == "Linear Regression":
                    results = trainer.train_linear_regression()
                elif model_type == "Decision Tree":
                    results = trainer.train_decision_tree(task_type=task_type, max_depth=max_depth)
                else:  # Random Forest
                    results = trainer.train_random_forest(task_type=task_type, max_depth=max_depth)
                
                # Display results
                st.success(f"✅ Model trained successfully!")
                
                st.subheader("📊 Model Performance")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Training Metrics:**")
                    st.json(results['train_metrics'])
                
                with col2:
                    st.write("**Testing Metrics:**")
                    st.json(results['test_metrics'])
                
                # Feature importance
                if 'feature_importance' in results:
                    st.subheader("📈 Feature Importance")
                    importance_df = pd.DataFrame({
                        'Feature': list(results['feature_importance'].keys()),
                        'Importance': list(results['feature_importance'].values())
                    }).sort_values('Importance', ascending=False)
                    
                    st.bar_chart(importance_df.set_index('Feature'))
                
                # Log operation
                operation_text = f"Trained {results['model_name']} - Test Score: {results['test_metrics']}"
                st.session_state.operations_log.append(operation_text)
                
                # Log for code generation
                st.session_state.code_generator.add_model_training(
                    model_type.replace(" ", ""),
                    target_col,
                    feature_cols
                )
                
            except Exception as e:
                st.error(f"❌ Error training model: {str(e)}")


def show_export_reports():
    """Display export and reports page."""
    st.header("💾 Export & Reports")
    
    df = st.session_state.df
    
    # Download processed data
    st.subheader("📥 Download Processed Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV download
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel download
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        st.download_button(
            label="Download as Excel",
            data=buffer.getvalue(),
            file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        # JSON download
        json_str = df.to_json(orient='records', indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_str,
            file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Generate Python code
    st.subheader("🐍 Export Python Code")
    
    if st.button("Generate Python Script"):
        script = st.session_state.code_generator.generate_script()
        
        st.code(script, language='python')
        
        st.download_button(
            label="Download Python Script",
            data=script,
            file_name=f"analysis_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
            mime="text/x-python"
        )
    
    # Generate PDF Report
    st.subheader("📄 Generate PDF Report")
    
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            try:
                eda = EDA(df)
                overview = eda.get_dataset_overview()
                stats = eda.get_statistical_summary()
                file_info = st.session_state.data_handler.get_file_info()
                
                report_path = f"/tmp/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                create_simple_report(
                    file_info=file_info,
                    overview=overview,
                    stats=stats,
                    operations=st.session_state.operations_log,
                    output_path=report_path
                )
                
                with open(report_path, "rb") as f:
                    st.download_button(
                        label="Download PDF Report",
                        data=f.read(),
                        file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                
                st.success("✅ Report generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")


if __name__ == "__main__":
    main()
