import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="🎬",
    layout="wide"
)

# Title
st.title("🎬 Netflix Data Analysis Dashboard")
st.write(
    "An interactive data analysis dashboard to explore Netflix movies and TV shows "
    "using real-world datasets."
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()

# ===============================
# DATA PREPROCESSING
# ===============================

# Convert Release_Date to datetime
df["Release_Date"] = pd.to_datetime(df["Release_Date"], errors="coerce")

# Extract year
df["Release_Year"] = df["Release_Date"].dt.year

# ===============================
# SIDEBAR FILTERS
# ===============================

st.sidebar.header("🔍 Filter Options")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df["Type"].dropna().unique(),
    default=df["Type"].dropna().unique()
)

year_filter = st.sidebar.slider(
    "Select Release Year",
    int(df["Release_Year"].min()),
    int(df["Release_Year"].max()),
    (2010, int(df["Release_Year"].max()))
)

# Apply filters
filtered_df = df[
    (df["Type"].isin(type_filter)) &
    (df["Release_Year"].between(year_filter[0], year_filter[1]))
]

# ===============================
# DATASET VIEW
# ===============================

st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df)

# ===============================
# KPIs
# ===============================

st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", filtered_df.shape[0])
col2.metric("Movies", filtered_df[filtered_df["Type"] == "Movie"].shape[0])
col3.metric("TV Shows", filtered_df[filtered_df["Type"] == "TV Show"].shape[0])

# ===============================
# VISUALIZATIONS
# ===============================

st.subheader("📈 Visual Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("### Content Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x="Type", ax=ax)
    st.pyplot(fig)

with col2:
    st.write("### Top 10 Content Producing Countries")
    country_counts = (
        filtered_df["Country"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )
    fig, ax = plt.subplots()
    sns.barplot(x=country_counts.values, y=country_counts.index, ax=ax)
    st.pyplot(fig)

# Year-wise trend
st.write("### Content Release Trend Over Years")
yearly = filtered_df["Release_Year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x=yearly.index, y=yearly.values, ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Releases")
st.pyplot(fig)

# ===============================
# FOOTER
# ===============================

st.markdown("---")
st.markdown(
    "👩‍💻 **Developed by Shivani D Shetty**  \n"
    "📊 Entry-Level Data Analyst | Python | Pandas | Streamlit"
)
