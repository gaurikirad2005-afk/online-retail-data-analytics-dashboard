import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Online Retail Data Analytics",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Online Retail Data Analytics Dashboard")

st.write(
    "An ongoing Data Analytics internship project focused on "
    "data cleaning, exploratory data analysis and business insights."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Internship Project")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Dataset Overview",
        "Data Cleaning",
        "Customer Analysis",
        "Sales Analysis",
        "Product Analysis",
        "Project Workflow"
    ]
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("retail_sample.csv", low_memory=False)

    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df

df = load_data()

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("Project Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sales",
        f"{df['TotalAmount'].sum():,.2f}"
    )

    col2.metric(
        "Unique Customers",
        df["CustomerID"].nunique()
    )

    col3.metric(
        "Unique Products",
        df["StockCode"].nunique()
    )

    col4.metric(
        "Countries",
        df["Country"].nunique()
    )

    st.subheader("Dataset Snapshot")

    st.dataframe(df.head())

    st.subheader("Project Objective")

    st.write("""
    The objective of this project is to analyze online retail transaction
    data and identify meaningful patterns related to customers, products,
    sales and geographical distribution.
    """)


# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

elif page == "Dataset Overview":

    st.header("Dataset Overview")

    col1, col2 = st.columns(2)

    col1.metric("Total Records", df.shape[0])
    col2.metric("Total Features", df.shape[1])

    st.subheader("Dataset Columns")

    st.write(list(df.columns))

    st.subheader("Data Types")

    st.dataframe(
        pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str)
        })
    )

    st.subheader("Sample Data")

    st.dataframe(df.head(10))


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

elif page == "Data Cleaning":

    st.header("Data Cleaning and Preprocessing")

    st.write("""
    The raw dataset was processed before analysis to improve
    data quality and prepare it for further exploration.
    """)

    st.subheader("Cleaning Steps Performed")

    st.write("""
    • Checked dataset structure and data types  
    • Examined missing values  
    • Removed duplicate records  
    • Converted InvoiceDate into datetime format  
    • Created TotalAmount feature  
    • Performed basic data validation  
    • Identified potential quantity outliers  
    """)

    st.subheader("Cleaned Dataset")

    st.metric("Final Number of Records", df.shape[0])


# --------------------------------------------------
# CUSTOMER ANALYSIS
# --------------------------------------------------

elif page == "Customer Analysis":

    st.header("Customer Analysis")

    total_customers = df["CustomerID"].nunique()

    st.metric(
        "Unique Customers",
        total_customers
    )

    st.subheader("Top Customers by Sales")

    customer_sales = (
        df.groupby("CustomerID")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.dataframe(customer_sales)

    fig, ax = plt.subplots(figsize=(10, 5))

    customer_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 Customers by Total Sales")
    ax.set_xlabel("Customer ID")
    ax.set_ylabel("Total Sales")

    plt.xticks(rotation=45)

    st.pyplot(fig)


# --------------------------------------------------
# SALES ANALYSIS
# --------------------------------------------------

elif page == "Sales Analysis":

    st.header("Sales Analysis")

    st.metric(
        "Total Sales",
        f"{df['TotalAmount'].sum():,.2f}"
    )

    if "InvoiceDate" in df.columns:

        st.subheader("Monthly Sales Trend")

        df["Month"] = df["InvoiceDate"].dt.to_period("M")

        monthly_sales = (
            df.groupby("Month")["TotalAmount"]
            .sum()
        )

        monthly_sales.index = monthly_sales.index.astype(str)

        fig, ax = plt.subplots(figsize=(10, 5))

        monthly_sales.plot(
            kind="line",
            marker="o",
            ax=ax
        )

        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Sales")

        plt.xticks(rotation=45)

        st.pyplot(fig)


# --------------------------------------------------
# PRODUCT ANALYSIS
# --------------------------------------------------

elif page == "Product Analysis":

    st.header("Product Analysis")

    st.metric(
        "Unique Products",
        df["StockCode"].nunique()
    )

    st.subheader("Top Products by Sales")

    product_sales = (
        df.groupby("Description")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.dataframe(product_sales)

    fig, ax = plt.subplots(figsize=(10, 5))

    product_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 Products by Total Sales")
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Sales")

    plt.xticks(rotation=45)

    st.pyplot(fig)


# --------------------------------------------------
# PROJECT WORKFLOW
# --------------------------------------------------

elif page == "Project Workflow":

    st.header("Data Analytics Workflow")

    st.markdown("""
    ### 1. Data Collection
    Collected and loaded the Online Retail dataset.

    ↓

    ### 2. Data Understanding
    Examined dataset structure, columns, data types and quality.

    ↓

    ### 3. Data Cleaning
    Handled missing values, removed duplicates and prepared the data.

    ↓

    ### 4. Feature Engineering
    Created the TotalAmount feature using Quantity × UnitPrice.

    ↓

    ### 5. Exploratory Data Analysis
    Analyzed customers, products, countries and sales patterns.

    ↓

    ### 6. Visualization and Insights
    Created charts and summarized important findings.
    """)

    st.success(
        "Project Status: Ongoing – Advanced analysis and insight generation in progress."
    )