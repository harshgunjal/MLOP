import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

# Set page title and layout
st.set_page_config(page_title="Advanced CSV Data Visualizer", page_icon="📊", layout="wide")

# Main title and description
st.title("📊 Advanced CSV Data Visualizer")
st.write("""
Upload a CSV file to explore and analyze your data using various chart options. This tool includes preprocessing features,
interactive customizations, and supports both numerical and categorical data.
""")

# File uploader section
uploaded_file = st.file_uploader("📂 Upload your CSV file here", type="csv")

if uploaded_file:
    # Load the CSV file
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Overview")
    st.dataframe(df.head())
    
    # Data summary
    st.write("### 📊 Data Summary")
    st.write(df.describe())

    # Data cleaning and preprocessing options
    st.sidebar.header("⚙️ Data Preprocessing")
    if st.sidebar.checkbox("Drop Missing Values"):
        df = df.dropna()
        st.write("Dropped missing values.")
    if st.sidebar.checkbox("Standardize Numerical Columns"):
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        st.write("Standardized numerical columns.")

    # Check column data types and show info
    st.write("### 🗃 Column Information")
    st.write(df.dtypes)
    
    # Detect numeric and categorical columns automatically
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    if numeric_columns or categorical_columns:
        # Sidebar for chart options
        st.sidebar.header("🔧 Visualization Settings")

        # Multiselect for multiple chart types
        selected_charts = st.sidebar.multiselect(
            "Select the Charts You Want to Generate", 
            ["Line Chart", "Bar Chart", "Histogram", "Scatter Plot", 
             "Box Plot", "Area Chart", "Correlation Heatmap", "Pair Plot", 
             "Pie Chart", "Density Plot", "Violin Plot"],
            default=["Line Chart", "Bar Chart"]
        )

        # Additional options for histogram and scatter plot
        if "Histogram" in selected_charts:
            bins = st.sidebar.slider("Histogram Bins", min_value=10, max_value=100, value=30)
        if "Scatter Plot" in selected_charts:
            x_axis = st.sidebar.selectbox("X-axis for Scatter Plot", options=numeric_columns)
            y_axis = st.sidebar.selectbox("Y-axis for Scatter Plot", options=[col for col in numeric_columns if col != x_axis])
            color_scatter = st.sidebar.selectbox("Color by (for Scatter Plot)", options=[None] + categorical_columns)

        if "Bar Chart" in selected_charts and categorical_columns:
            bar_chart_col = st.sidebar.selectbox("Select Category for Bar Chart", options=categorical_columns)

        if "Pie Chart" in selected_charts and categorical_columns:
            pie_chart_col = st.sidebar.selectbox("Select Category for Pie Chart", options=categorical_columns)
        
        if "Density Plot" in selected_charts:
            density_col = st.sidebar.selectbox("Select Column for Density Plot", options=numeric_columns)

        st.write("## 📈 Data Visualizations")

        # Line Chart
        if "Line Chart" in selected_charts:
            st.write("### 📈 Line Chart")
            for col in numeric_columns:
                fig = px.line(df, x=df.index, y=col, title=f"Line Chart of {col}", markers=True)
                st.plotly_chart(fig)

        # Bar Chart
        if "Bar Chart" in selected_charts and bar_chart_col:
            st.write(f"### 📊 Bar Chart by {bar_chart_col}")
            fig = px.bar(df, x=bar_chart_col, y=numeric_columns[0], title=f"Bar Chart of {numeric_columns[0]} by {bar_chart_col}")
            st.plotly_chart(fig)

        # Histogram
        if "Histogram" in selected_charts:
            st.write("### 📊 Histogram")
            for col in numeric_columns:
                fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}")
                st.plotly_chart(fig)

        # Scatter Plot
        if "Scatter Plot" in selected_charts and color_scatter:
            st.write("### 📈 Scatter Plot")
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_scatter, title=f"Scatter Plot of {x_axis} vs {y_axis}", trendline="ols")
            st.plotly_chart(fig)

        # Box Plot
        if "Box Plot" in selected_charts:
            st.write("### 📦 Box Plot")
            for col in numeric_columns:
                fig = px.box(df, y=col, title=f"Box Plot of {col}")
                st.plotly_chart(fig)

        # Area Chart
        if "Area Chart" in selected_charts:
            st.write("### 📈 Area Chart")
            for col in numeric_columns:
                fig = px.area(df, x=df.index, y=col, title=f"Area Chart of {col}")
                st.plotly_chart(fig)

        # Correlation Heatmap
        if "Correlation Heatmap" in selected_charts:
            st.write("### 🔥 Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        # Pair Plot
        if "Pair Plot" in selected_charts:
            st.write("### 👫 Pair Plot")
            fig = sns.pairplot(df[numeric_columns])
            st.pyplot(fig)

        # Pie Chart
        if "Pie Chart" in selected_charts and pie_chart_col:
            st.write(f"### 🥧 Pie Chart by {pie_chart_col}")
            fig = px.pie(df, names=pie_chart_col, title=f"Distribution of {pie_chart_col}")
            st.plotly_chart(fig)

        # Density Plot
        if "Density Plot" in selected_charts and density_col:
            st.write(f"### 🌄 Density Plot of {density_col}")
            fig = px.density_contour(df, x=density_col, title=f"Density Plot of {density_col}")
            st.plotly_chart(fig)

        # Violin Plot
        if "Violin Plot" in selected_charts and categorical_columns:
            st.write(f"### 🎻 Violin Plot")
            for col in numeric_columns:
                fig = px.violin(df, y=col, color=categorical_columns[0], box=True, title=f"Violin Plot of {col} by {categorical_columns[0]}")
                st.plotly_chart(fig)

    else:
        st.write("⚠️ No numeric or categorical columns found in this dataset for visualization.")

else:
    st.write("📂 Please upload a CSV file to proceed with visualizations.")
