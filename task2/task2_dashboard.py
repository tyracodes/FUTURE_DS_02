import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="Customer Retention & Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "WA_Fn-UseC_-Telco-Customer-Churn.csv")

    df = pd.read_csv(file_path)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna()

    df["CustomerLifetimeValue"] = df["MonthlyCharges"] * df["tenure"]

    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[0,12,24,36,48,60,72],
        labels=["0-12","13-24","25-36","37-48","49-60","61-72"]
    )

    return df

df = load_data()

st.title("📊 Customer Retention & Churn Analysis Dashboard")

st.markdown("""
This dashboard analyzes customer churn patterns, retention drivers,
and customer lifetime trends for a subscription-based business.
""")

churn_rate = (df["Churn"] == "Yes").mean() * 100
retention_rate = (df["Churn"] == "No").mean() * 100
avg_clv = df["CustomerLifetimeValue"].mean()
avg_tenure = df["tenure"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Churn Rate", f"{churn_rate:.2f}%")
col2.metric("Retention Rate", f"{retention_rate:.2f}%")
col3.metric("Average CLV", f"${avg_clv:,.0f}")
col4.metric("Average Tenure", f"{avg_tenure:.1f} Months")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Churn Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="Churn", ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Churn Rate by Contract Type")
    contract_churn = pd.crosstab(df["Contract"], df["Churn"], normalize="index") * 100
    fig, ax = plt.subplots()
    contract_churn["Yes"].plot(kind="bar", ax=ax)
    ax.set_ylabel("Churn %")
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Rate by Payment Method")
    payment_churn = pd.crosstab(df["PaymentMethod"], df["Churn"], normalize="index") * 100
    fig, ax = plt.subplots()
    payment_churn["Yes"].sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Churn %")
    st.pyplot(fig)

with col2:
    st.subheader("Retention by Tenure Group")
    retention = pd.crosstab(df["TenureGroup"], df["Churn"], normalize="index") * 100
    fig, ax = plt.subplots()
    retention["No"].plot(kind="bar", ax=ax)
    ax.set_ylabel("Retention %")
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tenure Distribution")
    fig, ax = plt.subplots()
    sns.histplot(data=df, x="tenure", hue="Churn", bins=30, kde=True, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Customer Lifetime Value Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["CustomerLifetimeValue"], bins=30, ax=ax)
    st.pyplot(fig)

st.divider()

st.header("Key Insights")

st.markdown("""
### Churn Patterns
- Overall churn rate is **26.58%**
- Month-to-month customers churn the most
- Electronic check users have the highest churn
- New customers are more likely to leave early

### Retention Drivers
- Long-term contracts improve retention
- Longer tenure increases loyalty
- Customers beyond 60 months rarely churn

### Customer Lifetime Trends
- Average CLV is approximately **$2,283**
- High tenure customers generate more value
- Early churn reduces lifetime revenue significantly
""")

st.header("Recommendations")

st.markdown("""
1. Encourage annual contracts with discounts
2. Improve onboarding in first 12 months
3. Target electronic check users with retention offers
4. Reward long-term customers
5. Identify high-risk users early
""")

with st.expander("View Dataset"):
    st.dataframe(df)
