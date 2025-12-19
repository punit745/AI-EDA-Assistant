"""
AI-EDA Assistant - Main Streamlit Application
An AI-driven tool for automated exploratory data analysis and preprocessing.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
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
from statistical_analysis import StatisticalAnalysis
from ai_insights import AIInsights
from multi_file_analyzer import MultiFileAnalyzer

# Page configuration
st.set_page_config(
    page_title="AI-EDA Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css(theme='dark'):
    """Load custom CSS styling based on theme."""
    try:
        if theme == 'light':
            css_path = os.path.join(os.path.dirname(__file__), 'style_light.css')
        else:
            css_path = os.path.join(os.path.dirname(__file__), 'style.css')
        
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except (FileNotFoundError, IOError):
        pass

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
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"  # default theme
if 'multi_file_analyzer' not in st.session_state:
    st.session_state.multi_file_analyzer = MultiFileAnalyzer()
if 'uploaded_files_count' not in st.session_state:
    st.session_state.uploaded_files_count = 0


def show_home_page():
    """Display the home page with project information."""
    
    # Hero section with animated title
    st.markdown("""
        <div class="home-header">
            <h1 class="home-title">📊 AI-EDA Assistant</h1>
            <p class="home-subtitle">Your Intelligent Data Analysis Companion with AI-Powered Insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # About section
    st.markdown("---")
    st.markdown("## 🎯 About This Project")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to AI-EDA Assistant!
        
        **AI-EDA Assistant** is an intelligent, AI-driven application designed to revolutionize the way you perform 
        **Exploratory Data Analysis (EDA)** and **data preprocessing**. Built with cutting-edge technologies, 
        this tool empowers data scientists, analysts, and enthusiasts to extract meaningful insights from their data 
        with minimal effort.
        
        #### 🎓 Purpose
        
        Our mission is to democratize data analysis by providing:
        - **AI-Powered Insights**: Automated health reports, correlation analysis, and smart recommendations
        - **Automated EDA**: Generate comprehensive visualizations and statistical summaries automatically
        - **Intelligent Preprocessing**: Handle missing values, outliers, and data normalization with smart algorithms
        - **Multi-File Analysis**: Compare, merge, and analyze multiple datasets simultaneously
        - **Advanced Analytics**: Perform complex statistical tests and time series analysis with ease
        - **Machine Learning Integration**: Train and evaluate ML models without writing code
        - **Professional Reports**: Export analysis results and Python code for reproducibility
        
        #### 🔬 Core Functionality
        
        The AI-EDA Assistant simplifies complex data workflows into intuitive, interactive steps:
        1. **Upload** your dataset(s) in various formats (CSV, Excel, JSON, TXT)
        2. **AI Insights** get automated health reports and smart recommendations
        3. **Explore** your data with automated visualizations and statistics
        4. **Analyze** with advanced statistical tests and correlation analysis
        5. **Preprocess** to clean and transform your data
        6. **Validate** data integrity and quality
        7. **Model** with built-in machine learning algorithms
        8. **Compare** multiple datasets with multi-file analysis
        9. **Export** results, code, and professional reports
        """)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3>Quick Start</h3>
            <p>Get started in seconds! Simply upload your dataset and let AI do the heavy lifting.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Fast & Efficient</h3>
            <p>Powered by optimized algorithms for lightning-fast analysis of large datasets.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3>Beautiful Visuals</h3>
            <p>Create stunning, publication-ready visualizations with a single click.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key features section
    st.markdown("---")
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered Insights</h3>
            <ul>
                <li>Data health scoring</li>
                <li>Automated recommendations</li>
                <li>Smart preprocessing hints</li>
                <li>Correlation insights</li>
            </ul>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Dataset Overview</h3>
            <ul>
                <li>Comprehensive data summaries</li>
                <li>Column-wise statistics</li>
                <li>Data type analysis</li>
                <li>Missing value detection</li>
            </ul>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Automated EDA</h3>
            <ul>
                <li>Distribution analysis</li>
                <li>Correlation heatmaps</li>
                <li>Box plots for outliers</li>
                <li>Scatter matrices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Statistical Analysis</h3>
            <ul>
                <li>Hypothesis testing (t-test, ANOVA)</li>
                <li>Correlation analysis</li>
                <li>Time series decomposition</li>
                <li>Probability distributions</li>
            </ul>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🧹</div>
            <h3>Data Preprocessing</h3>
            <ul>
                <li>Missing value imputation</li>
                <li>Outlier detection & removal</li>
                <li>Data normalization</li>
                <li>Feature scaling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✅</div>
            <h3>Data Integrity</h3>
            <ul>
                <li>Duplicate detection</li>
                <li>Type validation</li>
                <li>Format checking</li>
                <li>Consistency analysis</li>
            </ul>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>ML Training</h3>
            <ul>
                <li>10+ regression algorithms</li>
                <li>10+ classification models</li>
                <li>Time series forecasting</li>
                <li>Model evaluation metrics</li>
            </ul>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <h3>Multi-File Analysis</h3>
            <ul>
                <li>Compare multiple datasets</li>
                <li>Merge and join data</li>
                <li>Aggregate analysis</li>
                <li>Relationship detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology stack
    st.markdown("---")
    st.markdown("## 🛠️ Technology Stack")
    
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    
    with tech_col1:
        st.info("**Frontend**\n\n🎨 Streamlit\n\n📊 Plotly")
    
    with tech_col2:
        st.info("**Data Processing**\n\n🐼 Pandas\n\n🔢 NumPy")
    
    with tech_col3:
        st.info("**ML & Stats**\n\n🤖 Scikit-learn\n\n📈 Statsmodels")
    
    with tech_col4:
        st.info("**Visualization**\n\n🎭 Seaborn\n\n📉 Matplotlib")
    
    # Getting started
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    <div class="feature-card">
        <h3>📝 Three Simple Steps to Start Analyzing:</h3>
        <ol>
            <li><strong>Upload Your Data:</strong> Use the sidebar to upload your dataset (CSV, Excel, JSON, or TXT)</li>
            <li><strong>Choose Your Task:</strong> Select from Dataset Overview, EDA, Statistical Analysis, Preprocessing, Data Integrity, Model Training, or Export & Reports</li>
            <li><strong>Explore & Analyze:</strong> Interact with visualizations, run analyses, and export your results</li>
        </ol>
        <p style="margin-top: 1.5rem;"><strong>💡 Tip:</strong> Start with "Dataset Overview" to get familiar with your data, then move to "Automated EDA" for visualizations!</p>
    </div>
    """, unsafe_allow_html=True)


def render_navigation():
    """Render the navigation bar."""
    st.markdown("---")
    
    # Navigation in sidebar
    with st.sidebar:
        # Theme Toggle
        st.markdown("### 🎨 Theme")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark", use_container_width=True, 
                        type="primary" if st.session_state.theme == "dark" else "secondary"):
                st.session_state.theme = "dark"
                st.rerun()
        with col2:
            if st.button("☀️ Light", use_container_width=True,
                        type="primary" if st.session_state.theme == "light" else "secondary"):
                st.session_state.theme = "light"
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        
        pages = [
            "🏠 Home",
            "📊 Dataset Overview",
            "🤖 AI Insights",
            "🔍 Automated EDA",
            "📈 Statistical Analysis",
            "🧹 Preprocessing",
            "✅ Data Integrity",
            "🎯 Model Training",
            "📂 Multi-File Analysis",
            "💾 Export & Reports"
        ]
        
        # Create navigation buttons
        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # File upload section
        st.markdown("### 📁 Upload Dataset")
        
        # Option for single or multiple files
        upload_mode = st.radio("Upload Mode", ["Single File", "Multiple Files"], horizontal=True)
        
        if upload_mode == "Single File":
            uploaded_file = st.file_uploader(
                "Upload your dataset",
                type=['csv', 'xlsx', 'xls', 'json', 'txt'],
                help="Supported formats: CSV, Excel, JSON, TXT",
                key="file_uploader"
            )
            
            if uploaded_file is not None:
                try:
                    if st.session_state.df is None or st.button("🔄 Reload Data"):
                        df = st.session_state.data_handler.load_data(uploaded_file)
                        st.session_state.df = df.copy()
                        st.session_state.original_df = df.copy()
                        st.success(f"✅ Data loaded successfully!")
                        
                        file_info = st.session_state.data_handler.get_file_info()
                        st.info(f"📏 Shape: {file_info['rows']} rows × {file_info['columns']} columns")
                except Exception as e:
                    st.error(f"❌ Error loading file: {str(e)}")
        
        else:  # Multiple Files
            uploaded_files = st.file_uploader(
                "Upload multiple datasets",
                type=['csv', 'xlsx', 'xls', 'json', 'txt'],
                accept_multiple_files=True,
                help="Upload multiple files for comparison",
                key="multi_file_uploader"
            )
            
            if uploaded_files:
                st.info(f"📊 {len(uploaded_files)} file(s) uploaded")
                
                for i, file in enumerate(uploaded_files):
                    try:
                        df = st.session_state.data_handler.load_data(file)
                        file_name = file.name.split('.')[0]
                        st.session_state.multi_file_analyzer.add_dataset(file_name, df)
                        
                        # Set first file as main dataset
                        if i == 0:
                            st.session_state.df = df.copy()
                            st.session_state.original_df = df.copy()
                    except Exception as e:
                        st.error(f"❌ Error loading {file.name}: {str(e)}")
                
                st.success(f"✅ {len(uploaded_files)} dataset(s) loaded!")
                st.info("💡 Go to 'Multi-File Analysis' to compare datasets")


def main():
    """Main application function."""
    
    # Load CSS based on current theme
    load_css(st.session_state.theme)
    
    # Render navigation
    render_navigation()
    
    # Get current page
    page = st.session_state.current_page
    
    # Route to selected page
    if page == "🏠 Home":
        show_home_page()
    elif page == "📊 Dataset Overview":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_dataset_overview()
    elif page == "🤖 AI Insights":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_ai_insights()
    elif page == "🔍 Automated EDA":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_automated_eda()
    elif page == "📈 Statistical Analysis":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_statistical_analysis()
    elif page == "🧹 Preprocessing":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_preprocessing()
    elif page == "✅ Data Integrity":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_data_integrity()
    elif page == "🎯 Model Training":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_model_training()
    elif page == "📂 Multi-File Analysis":
        show_multi_file_analysis()
    elif page == "💾 Export & Reports":
        if st.session_state.df is None:
            st.warning("👆 Please upload a dataset using the sidebar to get started.")
            return
        show_export_reports()




def show_ai_insights():
    """Display AI-powered insights page."""
    st.header("🤖 AI-Powered Insights")
    
    df = st.session_state.df
    ai_insights = AIInsights(df)
    
    # Data Health Score
    st.subheader("📊 Data Health Report")
    
    health = ai_insights.get_data_health_score()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Overall Health Score",
            f"{health['overall_score']}/100",
            help="Comprehensive data quality score"
        )
        st.info(f"**Grade:** {health['health_grade']}")
    
    with col2:
        # Create a simple gauge chart
        score = health['overall_score']
        color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        st.markdown(f"### {color} Health Status")
        
        progress_bar = st.progress(score / 100)
    
    with col3:
        st.markdown("#### Health Breakdown")
        st.write(f"✓ Missing Values: {health['missing_score']:.0f}/100")
        st.write(f"✓ Duplicates: {health['duplicate_score']:.0f}/100")
        st.write(f"✓ Type Consistency: {health['type_consistency_score']:.0f}/100")
        st.write(f"✓ Outliers: {health['outlier_score']:.0f}/100")
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    for rec in health['recommendations']:
        st.markdown(f"- {rec}")
    
    st.markdown("---")
    
    # Correlation Insights
    st.subheader("🔗 Correlation Insights")
    
    threshold = st.slider("Correlation Threshold", 0.5, 0.95, 0.7, 0.05)
    correlation_insights = ai_insights.generate_correlation_insights(threshold)
    
    for insight in correlation_insights:
        st.info(insight)
    
    st.markdown("---")
    
    # Feature Importance Hints
    st.subheader("🎯 Feature Analysis Hints")
    
    feature_hints = ai_insights.detect_feature_importance_hints()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### High Variance Features")
        if feature_hints['high_variance_features']:
            for feature in feature_hints['high_variance_features'][:5]:
                st.write(f"• **{feature['column']}** (CV: {feature['coefficient_of_variation']})")
        else:
            st.info("No high variance features detected")
        
        st.markdown("##### Potential Target Variables")
        if feature_hints['potential_target_variables']:
            for feature in feature_hints['potential_target_variables'][:5]:
                st.write(f"• **{feature['column']}** ({feature['unique_values']} unique values)")
        else:
            st.info("No obvious target variables detected")
    
    with col2:
        st.markdown("##### Low Cardinality Categories")
        if feature_hints['low_cardinality_categories']:
            for feature in feature_hints['low_cardinality_categories'][:5]:
                st.write(f"• **{feature['column']}** ({feature['unique_values']} categories)")
        else:
            st.info("No low cardinality categorical features")
        
        st.markdown("##### Timestamp Features")
        if feature_hints['timestamp_features']:
            for feature in feature_hints['timestamp_features'][:5]:
                st.write(f"• **{feature}**")
        else:
            st.info("No timestamp features detected")
    
    st.markdown("---")
    
    # Preprocessing Suggestions
    st.subheader("🧹 Smart Preprocessing Suggestions")
    
    suggestions = ai_insights.suggest_preprocessing_steps()
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            with st.expander(f"{i}. {suggestion['step']} - Priority: {suggestion['priority']}", expanded=i==1):
                st.write(f"**Reason:** {suggestion['reason']}")
                st.write(f"**Recommended Action:** {suggestion['recommended_action']}")
                
                if 'columns' in suggestion:
                    st.write(f"**Affected Columns ({len(suggestion['columns'])}):** {', '.join(suggestion['columns'][:5])}")
                    if len(suggestion['columns']) > 5:
                        st.write(f"... and {len(suggestion['columns']) - 5} more")
    else:
        st.success("✅ No preprocessing issues detected! Your data is clean.")
    
    st.markdown("---")
    
    # Chart Recommendations
    st.subheader("📊 Smart Chart Recommendations")
    
    columns = st.multiselect(
        "Select columns to get chart recommendations",
        df.columns.tolist(),
        default=df.columns.tolist()[:3] if len(df.columns) >= 3 else df.columns.tolist()
    )
    
    if columns:
        for col in columns:
            with st.expander(f"📈 Recommendations for: {col}"):
                recommendations = ai_insights.auto_recommend_chart(col)
                for rec in recommendations:
                    st.write(f"• {rec}")


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
    ai_insights = AIInsights(df)
    
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
    st.subheader("📊 Interactive Visualizations")
    
    viz_option = st.selectbox(
        "Select Visualization",
        ["Histograms", "Box Plots", "Correlation Heatmap", "Scatter Matrix", "Missing Values"]
    )
    
    if viz_option == "Histograms":
        fig = eda.create_histograms()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Add AI insights
            st.markdown("#### 💡 Automated Insights")
            numeric_cols = df.select_dtypes(include=[np.number]).columns[:3]
            for col in numeric_cols:
                insight = ai_insights.generate_chart_insights("histogram", df[col])
                if insight and insight != "No specific insights available":
                    st.info(f"**{col}:** {insight}")
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
            
            # Add correlation insights
            st.markdown("#### 💡 Correlation Analysis")
            correlation_insights = ai_insights.generate_correlation_insights(threshold=0.7)
            for insight in correlation_insights[:5]:
                st.info(insight)
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


def show_statistical_analysis():
    """Display statistical analysis page."""
    st.header("📈 Advanced Statistical Analysis")
    
    df = st.session_state.df
    stat_analysis = StatisticalAnalysis(df)
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Descriptive Statistics", "Inferential Statistics", "Correlation Analysis", 
         "Time Series Analysis", "Probability Analysis"]
    )
    
    if analysis_type == "Descriptive Statistics":
        st.subheader("📊 Descriptive Statistics")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("No numerical columns found in the dataset.")
            return
        
        selected_cols = st.multiselect(
            "Select Columns (leave empty for all)",
            numeric_cols,
            default=numeric_cols[:min(5, len(numeric_cols))]
        )
        
        if selected_cols or not selected_cols:
            stats = stat_analysis.get_descriptive_statistics(selected_cols if selected_cols else None)
            
            if not stats.empty:
                st.dataframe(stats, use_container_width=True)
                
                # Download option
                csv = stats.to_csv()
                st.download_button(
                    label="Download Statistics as CSV",
                    data=csv,
                    file_name=f"descriptive_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data to display.")
    
    elif analysis_type == "Inferential Statistics":
        st.subheader("📉 Inferential Statistics")
        
        test_type = st.selectbox(
            "Select Statistical Test",
            ["Independent T-Test", "One-Sample T-Test", "ANOVA", "Chi-Square Test", "Confidence Interval"]
        )
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if test_type == "Independent T-Test":
            if len(numeric_cols) < 2:
                st.warning("Need at least 2 numerical columns for t-test.")
                return
            
            col1 = st.selectbox("Select First Column", numeric_cols, key="ttest_col1")
            col2 = st.selectbox("Select Second Column", [c for c in numeric_cols if c != col1], key="ttest_col2")
            
            if st.button("Perform T-Test"):
                result = stat_analysis.perform_ttest_ind(col1, col2)
                
                st.write("**Test Results:**")
                st.json(result)
                
                if result['significant']:
                    st.success(f"✅ The means are significantly different (p={result['p_value']:.4f})")
                else:
                    st.info(f"ℹ️ No significant difference found (p={result['p_value']:.4f})")
        
        elif test_type == "One-Sample T-Test":
            if not numeric_cols:
                st.warning("No numerical columns found.")
                return
            
            col = st.selectbox("Select Column", numeric_cols)
            pop_mean = st.number_input("Population Mean", value=df[col].mean())
            
            if st.button("Perform One-Sample T-Test"):
                result = stat_analysis.perform_ttest_1samp(col, pop_mean)
                
                st.write("**Test Results:**")
                st.json(result)
                
                if result['significant']:
                    st.success(f"✅ Sample mean differs from population mean (p={result['p_value']:.4f})")
                else:
                    st.info(f"ℹ️ No significant difference (p={result['p_value']:.4f})")
        
        elif test_type == "ANOVA":
            if len(numeric_cols) < 2:
                st.warning("Need at least 2 numerical columns for ANOVA.")
                return
            
            selected_cols = st.multiselect(
                "Select Columns (at least 2)",
                numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))]
            )
            
            if len(selected_cols) >= 2 and st.button("Perform ANOVA"):
                result = stat_analysis.perform_anova(selected_cols)
                
                st.write("**ANOVA Results:**")
                st.json(result)
                
                if result['significant']:
                    st.success(f"✅ Significant difference between groups (p={result['p_value']:.4f})")
                else:
                    st.info(f"ℹ️ No significant difference between groups (p={result['p_value']:.4f})")
        
        elif test_type == "Chi-Square Test":
            if len(categorical_cols) < 2:
                st.warning("Need at least 2 categorical columns for chi-square test.")
                return
            
            col1 = st.selectbox("Select First Categorical Column", categorical_cols, key="chi_col1")
            col2 = st.selectbox("Select Second Categorical Column", [c for c in categorical_cols if c != col1], key="chi_col2")
            
            if st.button("Perform Chi-Square Test"):
                result = stat_analysis.perform_chi_square(col1, col2)
                
                st.write("**Chi-Square Test Results:**")
                st.json(result)
                
                if result['significant']:
                    st.success(f"✅ Variables are dependent (p={result['p_value']:.4f})")
                else:
                    st.info(f"ℹ️ Variables are independent (p={result['p_value']:.4f})")
        
        elif test_type == "Confidence Interval":
            if not numeric_cols:
                st.warning("No numerical columns found.")
                return
            
            col = st.selectbox("Select Column", numeric_cols)
            confidence = st.slider("Confidence Level", 0.90, 0.99, 0.95, 0.01)
            
            if st.button("Calculate Confidence Interval"):
                result = stat_analysis.calculate_confidence_interval(col, confidence)
                
                st.write("**Confidence Interval:**")
                st.json(result)
                
                st.info(f"The {confidence*100:.0f}% confidence interval for the mean is [{result['lower_bound']:.4f}, {result['upper_bound']:.4f}]")
    
    elif analysis_type == "Correlation Analysis":
        st.subheader("🔗 Correlation Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            st.warning("Need at least 2 numerical columns for correlation analysis.")
            return
        
        analysis_option = st.selectbox(
            "Select Analysis",
            ["Correlation Matrix", "Pairwise Correlations", "Granger Causality (Time Series)"]
        )
        
        if analysis_option == "Correlation Matrix":
            method = st.selectbox("Correlation Method", ["pearson", "spearman", "kendall"])
            
            selected_cols = st.multiselect(
                "Select Columns (leave empty for all)",
                numeric_cols,
                default=numeric_cols[:min(10, len(numeric_cols))]
            )
            
            if selected_cols or not selected_cols:
                fig = stat_analysis.create_correlation_heatmap(
                    selected_cols if selected_cols else None,
                    method
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show correlation matrix
                    with st.expander("View Correlation Values"):
                        corr_matrix = stat_analysis.calculate_correlations(
                            selected_cols if selected_cols else None,
                            method
                        )
                        st.dataframe(corr_matrix, use_container_width=True)
        
        elif analysis_option == "Pairwise Correlations":
            selected_cols = st.multiselect(
                "Select Columns",
                numeric_cols,
                default=numeric_cols[:min(5, len(numeric_cols))]
            )
            
            if selected_cols and len(selected_cols) >= 2:
                correlations = stat_analysis.get_pairwise_correlations(selected_cols)
                
                tabs = st.tabs(["Pearson", "Spearman", "Kendall"])
                
                with tabs[0]:
                    st.dataframe(correlations['pearson'], use_container_width=True)
                
                with tabs[1]:
                    st.dataframe(correlations['spearman'], use_container_width=True)
                
                with tabs[2]:
                    st.dataframe(correlations['kendall'], use_container_width=True)
        
        elif analysis_option == "Granger Causality (Time Series)":
            st.info("Granger causality test determines if one time series helps predict another.")
            
            col1 = st.selectbox("Cause Variable", numeric_cols, key="granger_col1")
            col2 = st.selectbox("Effect Variable", [c for c in numeric_cols if c != col1], key="granger_col2")
            max_lag = st.slider("Maximum Lag", 1, 20, 5)
            
            if st.button("Perform Granger Causality Test"):
                result = stat_analysis.perform_granger_causality(col1, col2, max_lag)
                
                if 'error' in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.write("**Granger Causality Results:**")
                    st.json(result)
                    
                    if result['significant']:
                        st.success(f"✅ {result['interpretation']}")
                    else:
                        st.info(f"ℹ️ {result['interpretation']}")
    
    elif analysis_type == "Time Series Analysis":
        st.subheader("📅 Time Series Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("No numerical columns found.")
            return
        
        ts_option = st.selectbox(
            "Select Analysis",
            ["Decomposition", "Stationarity Test", "Autocorrelation"]
        )
        
        col = st.selectbox("Select Time Series Column", numeric_cols)
        
        if ts_option == "Decomposition":
            period = st.number_input("Period (seasonality)", min_value=2, value=12)
            model = st.selectbox("Model Type", ["additive", "multiplicative"])
            
            if st.button("Decompose Time Series"):
                fig = stat_analysis.create_decomposition_plot(col, period, model)
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Unable to decompose time series. Check if you have sufficient data.")
        
        elif ts_option == "Stationarity Test":
            if st.button("Test Stationarity"):
                result = stat_analysis.test_stationarity(col)
                
                st.write("**Augmented Dickey-Fuller Test Results:**")
                st.json(result)
                
                if result['stationary']:
                    st.success(f"✅ {result['interpretation']}")
                else:
                    st.warning(f"⚠️ {result['interpretation']}")
                
                st.write("**Critical Values:**")
                st.write(result['critical_values'])
        
        elif ts_option == "Autocorrelation":
            nlags = st.slider("Number of Lags", 10, 100, 40)
            
            if st.button("Calculate Autocorrelation"):
                fig = stat_analysis.create_acf_pacf_plot(col, nlags)
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("Red dashed lines indicate 95% confidence intervals.")
    
    elif analysis_type == "Probability Analysis":
        st.subheader("🎲 Probability Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("No numerical columns found.")
            return
        
        prob_option = st.selectbox(
            "Select Analysis",
            ["Distribution Fitting", "Probability Statistics"]
        )
        
        if prob_option == "Distribution Fitting":
            col = st.selectbox("Select Column", numeric_cols)
            distribution = st.selectbox(
                "Select Distribution",
                ["norm", "expon", "gamma", "lognorm"],
                format_func=lambda x: {
                    "norm": "Normal (Gaussian)",
                    "expon": "Exponential",
                    "gamma": "Gamma",
                    "lognorm": "Log-Normal"
                }[x]
            )
            
            if st.button("Fit Distribution"):
                result = stat_analysis.fit_distribution(col, distribution)
                
                if 'error' in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.write("**Distribution Fit Results:**")
                    st.json(result)
                    
                    fig = stat_analysis.create_distribution_plot(col, distribution)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    
                    if result['fit_quality'] == 'good':
                        st.success(f"✅ Good fit (p-value={result['p_value']:.4f})")
                    else:
                        st.warning(f"⚠️ Poor fit (p-value={result['p_value']:.4f})")
        
        elif prob_option == "Probability Statistics":
            col = st.selectbox("Select Column", numeric_cols)
            
            if st.button("Calculate Probabilities"):
                result = stat_analysis.calculate_probabilities(col)
                
                st.write("**Probability Statistics:**")
                st.json(result)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Expected Value (Mean)", f"{result['expected_value']:.4f}")
                    st.metric("Variance", f"{result['variance']:.4f}")
                    st.metric("Std Deviation", f"{result['std']:.4f}")
                
                with col2:
                    st.metric("Median", f"{result['median']:.4f}")
                    st.metric("IQR", f"{result['iqr']:.4f}")
                    st.metric("CV%", f"{result['coefficient_of_variation']:.2f}%")


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
                st.rerun()
    
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
            st.rerun()
    
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
            st.rerun()
    
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
        st.rerun()


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
            st.rerun()
    
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
    
    st.info("💡 Select features, target, and models for training")
    
    # Get available models
    available_models = ModelTrainer.get_available_models()
    
    # Model category selection
    model_category = st.selectbox(
        "Select Model Category",
        ["Regression", "Classification", "Gradient Boosting", "Time Series"]
    )
    
    # Task type
    if model_category in ["Regression", "Classification"]:
        task_type = model_category.lower()
        
        # Model selection based on category
        if model_category == "Regression":
            model_options = available_models['regression']
        else:
            model_options = available_models['classification']
        
        selected_models = st.multiselect(
            "Select Models to Train (can select multiple)",
            model_options,
            default=[model_options[0]] if model_options else []
        )
        
        if not selected_models:
            st.warning("Please select at least one model.")
            return
        
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
        
        # Hyperparameter controls
        with st.expander("⚙️ Hyperparameter Settings"):
            hyperparams = {}
            
            if any("Ridge" in m or "Lasso" in m for m in selected_models):
                hyperparams['alpha'] = st.slider("Alpha (Regularization)", 0.01, 10.0, 1.0, 0.01)
            
            if any("Tree" in m or "Forest" in m for m in selected_models):
                hyperparams['max_depth'] = st.slider("Max Depth", 2, 20, 5)
            
            if any("KNN" in m for m in selected_models):
                hyperparams['n_neighbors'] = st.slider("Number of Neighbors", 1, 20, 5)
            
            if any("SV" in m for m in selected_models):
                hyperparams['kernel'] = st.selectbox("Kernel", ["rbf", "linear", "poly"])
                hyperparams['C'] = st.slider("C (Regularization)", 0.01, 10.0, 1.0, 0.01)
            
            if any("Random Forest" in m for m in selected_models):
                hyperparams['n_estimators'] = st.slider("Number of Estimators", 10, 200, 100, 10)
        
        # Train button
        if st.button("🚀 Train Selected Models"):
            with st.spinner("Training models..."):
                try:
                    trainer = ModelTrainer(df)
                    trainer.prepare_data(target_col, feature_cols, test_size=test_size)
                    
                    results_list = []
                    
                    for model_name in selected_models:
                        st.write(f"Training {model_name}...")
                        
                        try:
                            if model_name == "Linear Regression":
                                results = trainer.train_linear_regression()
                            elif model_name == "Ridge Regression":
                                results = trainer.train_ridge_regression(hyperparams.get('alpha', 1.0))
                            elif model_name == "Lasso Regression":
                                results = trainer.train_lasso_regression(hyperparams.get('alpha', 1.0))
                            elif model_name == "Decision Tree":
                                results = trainer.train_decision_tree(task_type, hyperparams.get('max_depth', 5))
                            elif model_name == "Random Forest":
                                results = trainer.train_random_forest(task_type, hyperparams.get('n_estimators', 100), hyperparams.get('max_depth', 5))
                            elif model_name == "SVR (Support Vector Regression)":
                                results = trainer.train_svr(hyperparams.get('kernel', 'rbf'), hyperparams.get('C', 1.0))
                            elif model_name == "SVC (Support Vector Classification)":
                                results = trainer.train_svc(hyperparams.get('kernel', 'rbf'), hyperparams.get('C', 1.0))
                            elif model_name == "KNN Regressor":
                                results = trainer.train_knn_regressor(hyperparams.get('n_neighbors', 5))
                            elif model_name == "KNN Classifier":
                                results = trainer.train_knn_classifier(hyperparams.get('n_neighbors', 5))
                            elif model_name == "Logistic Regression":
                                results = trainer.train_logistic_regression(hyperparams.get('C', 1.0))
                            else:
                                st.warning(f"Model {model_name} not yet implemented in UI.")
                                continue
                            
                            results_list.append(results)
                            
                        except Exception as e:
                            st.error(f"Error training {model_name}: {str(e)}")
                    
                    if results_list:
                        st.success(f"✅ Successfully trained {len(results_list)} model(s)!")
                        
                        # Display results for each model
                        for idx, results in enumerate(results_list):
                            with st.expander(f"📊 {results['model_name']} Results", expanded=idx==0):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write("**Training Metrics:**")
                                    st.json(results['train_metrics'])
                                
                                with col2:
                                    st.write("**Testing Metrics:**")
                                    st.json(results['test_metrics'])
                                
                                # Feature importance
                                if 'feature_importance' in results:
                                    st.write("**Feature Importance:**")
                                    importance_df = pd.DataFrame({
                                        'Feature': list(results['feature_importance'].keys()),
                                        'Importance': list(results['feature_importance'].values())
                                    }).sort_values('Importance', ascending=False)
                                    
                                    st.bar_chart(importance_df.set_index('Feature'))
                        
                        # Compare models
                        if len(results_list) > 1:
                            st.subheader("📊 Model Comparison")
                            comparison_data = []
                            for results in results_list:
                                if task_type == 'regression':
                                    comparison_data.append({
                                        'Model': results['model_name'],
                                        'Test RMSE': results['test_metrics']['rmse'],
                                        'Test MAE': results['test_metrics']['mae'],
                                        'Test R²': results['test_metrics']['r2_score']
                                    })
                                else:
                                    comparison_data.append({
                                        'Model': results['model_name'],
                                        'Test Accuracy': results['test_metrics']['accuracy']
                                    })
                            
                            comparison_df = pd.DataFrame(comparison_data)
                            st.dataframe(comparison_df, use_container_width=True)
                            
                            # Highlight best model
                            if task_type == 'regression':
                                best_model = comparison_df.loc[comparison_df['Test R²'].idxmax()]['Model']
                                st.success(f"🏆 Best Model (by R²): {best_model}")
                            else:
                                best_model = comparison_df.loc[comparison_df['Test Accuracy'].idxmax()]['Model']
                                st.success(f"🏆 Best Model (by Accuracy): {best_model}")
                        
                        # Log operation
                        for results in results_list:
                            operation_text = f"Trained {results['model_name']} - Test Score: {results['test_metrics']}"
                            st.session_state.operations_log.append(operation_text)
                
                except Exception as e:
                    st.error(f"❌ Error during model training: {str(e)}")
    
    elif model_category == "Gradient Boosting":
        if not available_models['gradient_boosting']:
            st.warning("No gradient boosting libraries installed. Install with: pip install xgboost lightgbm catboost")
            return
        
        selected_models = st.multiselect(
            "Select Gradient Boosting Models",
            available_models['gradient_boosting'],
            default=[available_models['gradient_boosting'][0]]
        )
        
        if not selected_models:
            st.warning("Please select at least one model.")
            return
        
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
        
        with st.expander("⚙️ Hyperparameter Settings"):
            n_estimators = st.slider("Number of Estimators", 10, 500, 100, 10)
            max_depth = st.slider("Max Depth", 2, 20, 5)
            learning_rate = st.slider("Learning Rate", 0.01, 0.3, 0.1, 0.01)
        
        if st.button("🚀 Train Gradient Boosting Models"):
            with st.spinner("Training models..."):
                try:
                    trainer = ModelTrainer(df)
                    trainer.prepare_data(target_col, feature_cols, test_size=test_size)
                    
                    results_list = []
                    
                    for model_name in selected_models:
                        st.write(f"Training {model_name}...")
                        
                        try:
                            if model_name == "XGBoost":
                                results = trainer.train_xgboost(task_type, n_estimators, max_depth, learning_rate)
                            elif model_name == "LightGBM":
                                results = trainer.train_lightgbm(task_type, n_estimators, max_depth, learning_rate)
                            elif model_name == "CatBoost":
                                results = trainer.train_catboost(task_type, n_estimators, max_depth, learning_rate)
                            
                            if 'error' in results:
                                st.error(results['error'])
                                continue
                            
                            results_list.append(results)
                            
                        except Exception as e:
                            st.error(f"Error training {model_name}: {str(e)}")
                    
                    if results_list:
                        st.success(f"✅ Successfully trained {len(results_list)} model(s)!")
                        
                        # Display results
                        for idx, results in enumerate(results_list):
                            with st.expander(f"📊 {results['model_name']} Results", expanded=idx==0):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write("**Training Metrics:**")
                                    st.json(results['train_metrics'])
                                
                                with col2:
                                    st.write("**Testing Metrics:**")
                                    st.json(results['test_metrics'])
                                
                                if 'feature_importance' in results:
                                    st.write("**Feature Importance:**")
                                    importance_df = pd.DataFrame({
                                        'Feature': list(results['feature_importance'].keys()),
                                        'Importance': list(results['feature_importance'].values())
                                    }).sort_values('Importance', ascending=False)
                                    
                                    st.bar_chart(importance_df.set_index('Feature'))
                
                except Exception as e:
                    st.error(f"❌ Error during model training: {str(e)}")
    
    elif model_category == "Time Series":
        if not available_models['time_series']:
            st.warning("No time series libraries installed. Install with: pip install statsmodels prophet")
            return
        
        model_name = st.selectbox("Select Time Series Model", available_models['time_series'])
        
        if model_name == "ARIMA":
            target_col = st.selectbox("Select Target Column", numeric_cols)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                p = st.number_input("p (AR order)", min_value=0, max_value=10, value=1)
            with col2:
                d = st.number_input("d (Differencing)", min_value=0, max_value=3, value=1)
            with col3:
                q = st.number_input("q (MA order)", min_value=0, max_value=10, value=1)
            
            if st.button("🚀 Train ARIMA Model"):
                with st.spinner("Training ARIMA model..."):
                    try:
                        trainer = ModelTrainer(df)
                        results = trainer.train_arima(target_col, order=(p, d, q))
                        
                        if 'error' in results:
                            st.error(f"Error: {results['error']}")
                        else:
                            st.success("✅ ARIMA model trained successfully!")
                            
                            st.write("**Model Information:**")
                            st.json({
                                'Order (p,d,q)': results['order'],
                                'AIC': results['aic'],
                                'BIC': results['bic']
                            })
                            
                            st.write("**Performance Metrics:**")
                            st.json(results['metrics'])
                            
                            # Plot forecast vs actual
                            forecast_df = pd.DataFrame({
                                'Actual': results['test_values'],
                                'Forecast': results['forecast']
                            })
                            st.line_chart(forecast_df)
                    
                    except Exception as e:
                        st.error(f"❌ Error training ARIMA: {str(e)}")
        
        elif model_name == "Prophet":
            # Check for date column
            date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            
            if not date_cols:
                st.warning("No datetime columns found. Prophet requires a date column.")
                st.info("Try converting a column to datetime first in preprocessing.")
                return
            
            date_col = st.selectbox("Select Date Column", date_cols)
            target_col = st.selectbox("Select Target Column", numeric_cols)
            periods = st.number_input("Forecast Periods", min_value=1, max_value=365, value=30)
            
            if st.button("🚀 Train Prophet Model"):
                with st.spinner("Training Prophet model..."):
                    try:
                        trainer = ModelTrainer(df)
                        results = trainer.train_prophet(date_col, target_col, periods)
                        
                        if 'error' in results:
                            st.error(f"Error: {results['error']}")
                        else:
                            st.success("✅ Prophet model trained successfully!")
                            
                            st.write("**Performance Metrics:**")
                            st.json(results['metrics'])
                            
                            st.write("**Forecast:**")
                            forecast_df = pd.DataFrame(results['forecast'])
                            st.dataframe(forecast_df.tail(periods), use_container_width=True)
                    
                    except Exception as e:
                        st.error(f"❌ Error training Prophet: {str(e)}")


def show_multi_file_analysis():
    """Display multi-file analysis page."""
    st.header("📂 Multi-File Analysis")
    
    analyzer = st.session_state.multi_file_analyzer
    datasets = analyzer.get_dataset_names()
    
    if len(datasets) == 0:
        st.info("👆 No datasets loaded yet. Upload multiple files using 'Multiple Files' mode in the sidebar.")
        st.markdown("""
        ### How to use Multi-File Analysis:
        
        1. Switch to **Multiple Files** mode in the sidebar
        2. Upload 2 or more datasets
        3. Return to this page to compare and analyze them
        
        **Use Cases:**
        - Compare sales data across different regions
        - Analyze trends across time periods
        - Merge customer and transaction data
        - Aggregate data from multiple sources
        """)
        return
    
    st.success(f"✅ {len(datasets)} dataset(s) loaded: {', '.join(datasets)}")
    
    # Summary
    st.subheader("📊 Datasets Summary")
    summary = analyzer.get_summary()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Datasets", summary['total_datasets'])
    with col2:
        st.metric("Total Rows", summary['total_rows'])
    with col3:
        st.metric("Total Columns", summary['total_columns'])
    
    # Schema comparison
    st.subheader("📋 Schema Comparison")
    schema_df = analyzer.compare_schemas()
    st.dataframe(schema_df, use_container_width=True)
    
    # Common columns
    st.subheader("🔗 Column Analysis")
    common_cols = analyzer.find_common_columns()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Common Columns")
        if common_cols['common']:
            for col in common_cols['common']:
                st.write(f"• {col}")
        else:
            st.info("No common columns found")
    
    with col2:
        st.markdown("##### Unique Columns")
        for dataset, cols in common_cols['unique'].items():
            if cols:
                with st.expander(f"{dataset} ({len(cols)} unique)"):
                    for col in cols[:10]:
                        st.write(f"• {col}")
                    if len(cols) > 10:
                        st.write(f"... and {len(cols) - 10} more")
    
    # Relationship detection
    st.subheader("🔍 Potential Relationships")
    relationships = analyzer.detect_relationships()
    
    if relationships:
        st.success(f"Found {len(relationships)} potential join relationship(s)")
        
        for i, rel in enumerate(relationships[:5], 1):
            with st.expander(f"{i}. {rel['dataset1']} ↔ {rel['dataset2']} on '{rel['join_column']}'", 
                           expanded=i==1):
                st.write(f"**Join Column:** {rel['join_column']}")
                st.write(f"**Common Values:** {rel['common_values']}")
                st.write(f"**Overlap:** {rel['overlap_percentage']:.1f}%")
                st.write(f"**Recommendation:** {rel['recommendation']}")
    else:
        st.info("No obvious relationships detected between datasets")
    
    # Comparison Analysis
    if len(datasets) >= 2:
        st.subheader("📊 Comparative Analysis")
        
        # Column selection for comparison
        if common_cols['common']:
            selected_column = st.selectbox(
                "Select column to compare",
                common_cols['common']
            )
            
            if selected_column:
                # Statistics comparison
                st.markdown("##### Statistics Comparison")
                stats_df = analyzer.compare_statistics(selected_column)
                st.dataframe(stats_df, use_container_width=True)
                
                # Visual comparison
                st.markdown("##### Visual Comparison")
                chart_type = st.selectbox(
                    "Chart Type",
                    ["box", "violin", "histogram"],
                    format_func=lambda x: x.title()
                )
                
                try:
                    fig = analyzer.create_comparison_chart(selected_column, chart_type)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
        else:
            st.warning("No common columns available for comparison")
    
    # Merge datasets
    if len(datasets) >= 2:
        st.subheader("🔀 Merge Datasets")
        
        col1, col2 = st.columns(2)
        with col1:
            dataset1 = st.selectbox("Select first dataset", datasets, key="merge_ds1")
        with col2:
            dataset2 = st.selectbox("Select second dataset", 
                                   [d for d in datasets if d != dataset1], 
                                   key="merge_ds2")
        
        if dataset1 and dataset2:
            # Find common columns for join
            common = list(set(analyzer.datasets[dataset1].columns) & 
                         set(analyzer.datasets[dataset2].columns))
            
            if common:
                col1, col2 = st.columns(2)
                with col1:
                    join_column = st.selectbox("Join column", common)
                with col2:
                    join_type = st.selectbox("Join type", 
                                            ["inner", "outer", "left", "right"])
                
                if st.button("🔀 Merge Datasets"):
                    try:
                        merged_df = analyzer.merge_datasets(dataset1, dataset2, 
                                                           join_column, join_type)
                        
                        st.success(f"✅ Merged {len(merged_df)} rows")
                        st.dataframe(merged_df.head(20), use_container_width=True)
                        
                        # Option to use merged dataset
                        if st.button("Use merged dataset as main dataset"):
                            st.session_state.df = merged_df
                            st.session_state.original_df = merged_df.copy()
                            st.success("Merged dataset is now the active dataset!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error merging datasets: {str(e)}")
            else:
                st.warning("No common columns found for merging these datasets")
    
    # Aggregation analysis
    if len(datasets) >= 2 and common_cols['common']:
        st.subheader("📊 Aggregation Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            group_col = st.selectbox("Group by column", common_cols['common'], key="agg_group")
        with col2:
            value_col = st.selectbox("Value column", common_cols['common'], key="agg_value")
        with col3:
            agg_func = st.selectbox("Aggregation", ["mean", "sum", "count", "median"])
        
        if st.button("📊 Perform Aggregation"):
            try:
                agg_df = analyzer.aggregate_analysis(group_col, value_col, agg_func)
                
                if not agg_df.empty:
                    st.dataframe(agg_df, use_container_width=True)
                    
                    # Visualize aggregation
                    fig = px.bar(agg_df, barmode='group', 
                               title=f"{agg_func.title()} of {value_col} by {group_col}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data available for aggregation")
            except Exception as e:
                st.error(f"Error performing aggregation: {str(e)}")


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
