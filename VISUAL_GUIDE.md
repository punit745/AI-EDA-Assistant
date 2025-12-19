# Screenshots and Visual Guide

## 🎨 Theme Customization

### Dark Theme (Default)
The application launches with a professional dark theme featuring:
- Deep blue-black backgrounds (#0e1117)
- Cyan accent colors (#00d4ff)
- High contrast for comfortable viewing
- Minimalist design elements

### Light Theme
Professional light theme featuring:
- Clean white backgrounds (#ffffff)
- Blue accent colors (#0091ff)
- Excellent readability
- Print-friendly appearance

**To see themes in action, run the application and toggle between dark/light modes in the sidebar.**

---

## 🤖 AI Insights Page

### Data Health Report
The health report provides:
- Overall health score (0-100) with color-coded status (🟢 🟡 🔴)
- Letter grade (A-F)
- Breakdown scores for:
  - Missing values
  - Duplicates
  - Type consistency
  - Outliers
- Prioritized recommendations

### Correlation Insights
- Adjustable threshold slider
- List of strong correlations
- Positive/negative relationship indicators
- Correlation strength values

### Feature Analysis
Four categories of hints:
1. High variance features (good for prediction)
2. Low cardinality categories (good for classification)
3. Potential target variables
4. Timestamp features

### Smart Preprocessing
- Expandable recommendation cards
- Priority levels (High/Medium/Low)
- Specific affected columns
- Recommended actions

---

## 📂 Multi-File Analysis Page

### Summary Metrics
- Total datasets counter
- Total rows across all datasets
- Total columns
- Dataset name list

### Schema Comparison Table
Columns:
- Dataset name
- Rows
- Columns
- Numeric columns
- Categorical columns
- Memory usage (MB)

### Common Columns Analysis
- Left panel: Common columns (shared by all)
- Right panel: Unique columns per dataset

### Relationship Detection
Expandable cards showing:
- Dataset pair names
- Join column suggestion
- Overlap percentage
- Number of common values
- Recommendation level

### Comparative Analysis
- Column selector
- Statistics comparison table
- Visual comparison (box/violin/histogram)
- Side-by-side metric display

### Merge Interface
- Two dropdown menus for dataset selection
- Join column selector (common columns only)
- Join type selector (inner/outer/left/right)
- Preview of merged data
- Option to use as main dataset

---

## 🔍 Enhanced EDA Page

### Visualizations with Insights

#### Histograms
- Multiple columns displayed in grid
- Distribution curves
- Automated insights below showing:
  - Mean and median
  - Skewness interpretation

#### Correlation Heatmap
- Interactive color-coded matrix
- Hover for exact values
- Automated insights listing:
  - Strongest correlations
  - Relationship interpretations

---

## 📊 Interactive Elements

### Navigation
- Sidebar with all page buttons
- Active page highlighted
- Smooth transitions
- Icon-based navigation

### Theme Toggle
- Two-button interface
- Active theme highlighted
- Instant switching
- Persistent across pages

### File Upload
- Single file mode: Traditional uploader
- Multiple files mode: Multi-select uploader
- Progress indication
- Success/error feedback

### Data Preview
- Adjustable row display slider
- Full-width table
- Sortable columns
- Responsive design

---

## 🎯 Key UI Improvements

### Animations
- Fade-in effects on page load
- Smooth transitions between sections
- Hover effects on cards
- Button press animations

### Card Design
- Rounded corners (15px)
- Subtle shadows
- Hover elevation effects
- Consistent spacing

### Color Scheme
- **Dark Theme**: Blue gradient accents on dark backgrounds
- **Light Theme**: Blue accents on white backgrounds
- **Status Colors**: 
  - Success: Green
  - Warning: Orange
  - Error: Red
  - Info: Blue

### Typography
- Clear hierarchy
- Readable font sizes
- Icon integration
- Emoji indicators

---

## 📱 Responsive Design

### Desktop
- Full sidebar navigation
- Multi-column layouts
- Expanded visualizations
- Maximum data density

### Tablet
- Collapsible sidebar
- Adapted column layouts
- Touch-friendly controls
- Optimized spacing

### Mobile
- Hamburger menu
- Single-column layouts
- Stacked visualizations
- Touch-optimized buttons

---

## 🎨 Design Principles Applied

1. **Minimalism**: Clean, uncluttered interface
2. **Consistency**: Uniform design language
3. **Hierarchy**: Clear information structure
4. **Feedback**: Immediate response to actions
5. **Accessibility**: High contrast, readable text
6. **Professional**: Business-appropriate styling

---

## 🖼️ To View Screenshots

**Run the application to see:**
```bash
streamlit run app.py
```

Then navigate through:
1. 🏠 Home - See feature overview
2. 🤖 AI Insights - View health reports
3. 📂 Multi-File Analysis - Compare datasets
4. 🔍 Automated EDA - See enhanced visualizations
5. Toggle between 🌙 Dark and ☀️ Light themes

---

## 📹 Demo Workflow

### Quick Demo Steps:
1. Launch application
2. Upload demo_customer_data.csv
3. Check AI Insights health score
4. View automated EDA visualizations
5. Try multi-file upload with 2 CSV files
6. Explore multi-file analysis features
7. Toggle between themes
8. Export results

### Expected Experience:
- Smooth, professional interface
- Fast response times (with caching)
- Intuitive navigation
- Clear, actionable insights
- Beautiful visualizations
- Professional appearance

---

**Note**: For actual screenshots, please run the application and capture images of each page. The application is designed to be visually impressive and user-friendly.
