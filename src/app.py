import streamlit as st
import pandas as pd

# ===============================
# Load data
# ===============================
@st.cache_data
def load_data():
    clusters = pd.read_csv("data/processed/customer_clusters_from_rules.csv")
    rules = pd.read_csv("data/processed/rules_apriori_filtered.csv")
    return clusters, rules

df_clusters, df_rules = load_data()

# ===============================
# Sidebar – chọn cụm
# ===============================
st.sidebar.title("Customer Cluster Filter")

cluster_ids = sorted(df_clusters["cluster"].unique())
selected_cluster = st.sidebar.selectbox(
    "Chọn cụm khách hàng",
    cluster_ids
)

# ===============================
# Thông tin tổng quan cụm
# ===============================
st.title("Customer Segmentation Dashboard")

cluster_df = df_clusters[df_clusters["cluster"] == selected_cluster]

st.subheader(f"Tổng quan cụm {selected_cluster}")

col1, col2, col3 = st.columns(3)
col1.metric("Số khách hàng", len(cluster_df))
col2.metric("Recency (avg)", round(cluster_df["Recency"].mean(), 2))
col3.metric("Monetary (avg)", round(cluster_df["Monetary"].mean(), 2))

# ===============================
# Top rule-features theo cụm
# ===============================
st.subheader("Top rule-features được kích hoạt nhiều nhất")

rule_cols = [c for c in df_clusters.columns if c.startswith("rule_")]

top_rules = (
    cluster_df[rule_cols]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_rules.columns = ["Rule Feature", "Activation Rate"]

st.dataframe(top_rules)

# ===============================
# Gợi ý bundle / cross-sell
# ===============================
st.subheader("Gợi ý bundle / cross-sell theo cụm")

# Lấy tên luật tương ứng
top_rule_names = (
    top_rules["Rule Feature"]
    .str.replace("rule_", "", regex=False)
    .str.replace("__", " → ", regex=False)
)

recommendations = pd.DataFrame({
    "Gợi ý mua kèm": top_rule_names
})

st.table(recommendations)

# ===============================
# Xem danh sách khách hàng (tuỳ chọn)
# ===============================
with st.expander("Xem danh sách khách hàng trong cụm"):
    st.dataframe(cluster_df.head(50))
