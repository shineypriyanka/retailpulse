import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

os.chdir(r"E:\retailpulse")

st.set_page_config(
    page_title="RetailPulse | AI Analytics",
    layout="wide",
    page_icon="📊")

# ── Load All Data ─────────────────────────────────────────
@st.cache_data
def load_data():
    master   = pd.read_csv("data/processed/master.csv",
                            parse_dates=["order_date"])
    rfm      = pd.read_csv("data/processed/rfm_churn.csv")
    seg      = pd.read_csv("data/processed/segment_summary.csv")
    monthly  = pd.read_csv("data/processed/monthly_sales.csv")
    cat_rev  = pd.read_csv("data/processed/category_revenue.csv")
    forecast = pd.read_csv("data/processed/future_forecast.csv",
                            parse_dates=["order_date"])
    weekly   = pd.read_csv("data/processed/weekly_features.csv",
                            parse_dates=["order_date"])
    inv      = pd.read_csv("data/processed/inventory_abc.csv")
    abc_sum  = pd.read_csv("data/processed/abc_summary.csv")
    return (master, rfm, seg, monthly,
            cat_rev, forecast, weekly, inv, abc_sum)

(master, rfm, seg, monthly,
 cat_rev, forecast, weekly, inv, abc_sum) = load_data()

# ── Sidebar Navigation ────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart.png",
    width=60)
st.sidebar.title("RetailPulse")
st.sidebar.caption("AI-Powered Retail Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", [
    "📊 Sales Dashboard",
    "👥 Customer Dashboard",
    "📈 Forecast Dashboard",
    "📦 Inventory Dashboard"])

st.sidebar.markdown("---")
st.sidebar.caption(f"Total Revenue: BRL "
                   f"{master['revenue'].sum()/1e6:.2f}M")
st.sidebar.caption(f"Total Orders: "
                   f"{master['order_id'].nunique():,}")
st.sidebar.caption(f"Total Customers: "
                   f"{master['customer_id_unique'].nunique():,}")

# ════════════════════════════════════════════════════════
# PAGE 1 — SALES DASHBOARD
# ════════════════════════════════════════════════════════
if page == "📊 Sales Dashboard":
    st.title("📊 Sales Analytics Dashboard")
    st.caption("Overview of revenue, orders, and product performance")

    # KPIs
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Revenue",
              f"BRL {master['revenue'].sum()/1e6:.2f}M")
    k2.metric("Total Orders",
              f"{master['order_id'].nunique():,}")
    k3.metric("Total Customers",
              f"{master['customer_id_unique'].nunique():,}")
    k4.metric("Avg Order Value",
              f"BRL {master.groupby('order_id')['revenue'].sum().mean():.2f}")

    st.divider()

    # Monthly revenue trend
    st.subheader("Monthly Revenue Trend")
    fig = px.area(monthly, x="order_date", y="revenue",
                  labels={"order_date":"Month",
                          "revenue":"Revenue (BRL)"},
                  color_discrete_sequence=["#2563eb"])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Categories by Revenue")
        fig2 = px.bar(cat_rev,
                      x="revenue", y="category",
                      orientation="h",
                      color="revenue",
                      color_continuous_scale="Blues",
                      labels={"revenue":"Revenue (BRL)",
                              "category":"Category"})
        fig2.update_layout(
            yaxis={"categoryorder":"total ascending"},
            showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Revenue by Customer State")
        state_rev = (master.groupby("customer_state")["revenue"]
                           .sum()
                           .sort_values(ascending=False)
                           .head(10)
                           .reset_index())
        fig3 = px.bar(state_rev,
                      x="customer_state", y="revenue",
                      color="revenue",
                      color_continuous_scale="Greens",
                      labels={"customer_state":"State",
                              "revenue":"Revenue (BRL)"})
        st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════
# PAGE 2 — CUSTOMER DASHBOARD
# ════════════════════════════════════════════════════════
elif page == "👥 Customer Dashboard":
    st.title("👥 Customer Analytics Dashboard")
    st.caption("RFM Segmentation, Churn Risk & Customer Insights")

    # KPIs
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Customers",
              f"{len(rfm):,}")
    k2.metric("Champions",
              f"{(rfm['segment']=='Champions').sum():,}")
    k3.metric("High Churn Risk",
              f"{(rfm['churn_risk']=='High Risk').sum():,}")
    k4.metric("Revenue at Risk",
              f"BRL {rfm[rfm['churn_risk']=='High Risk']['monetary'].sum()/1e6:.2f}M")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Segments")
        seg_counts = rfm["segment"].value_counts().reset_index()
        seg_counts.columns = ["segment","count"]
        fig = px.pie(seg_counts,
                     values="count",
                     names="segment",
                     color_discrete_sequence=
                     px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Churn Risk Distribution")
        risk_counts = rfm["churn_risk"].value_counts().reset_index()
        risk_counts.columns = ["risk","count"]
        fig2 = px.bar(risk_counts,
                      x="risk", y="count",
                      color="risk",
                      color_discrete_map={
                          "Low Risk":    "#22c55e",
                          "Medium Risk": "#f59e0b",
                          "High Risk":   "#ef4444"})
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Segment Details")
    st.dataframe(seg.style.format({
        "avg_recency":   "{:.0f}",
        "avg_frequency": "{:.2f}",
        "avg_monetary":  "BRL {:.2f}",
        "total_revenue": "BRL {:.0f}"}),
        use_container_width=True)

    st.subheader("High Risk Customers — Top Spenders")
    high_risk = (rfm[rfm["churn_risk"]=="High Risk"]
                 .sort_values("monetary", ascending=False)
                 .head(20))
    st.dataframe(
        high_risk[["customer_id_unique","segment",
                   "recency","frequency","monetary",
                   "churn_probability"]]
        .style.format({"monetary":"BRL {:.2f}",
                       "churn_probability":"{:.2%}"}),
        use_container_width=True)

# ════════════════════════════════════════════════════════
# PAGE 3 — FORECAST DASHBOARD
# ════════════════════════════════════════════════════════
elif page == "📈 Forecast Dashboard":
    st.title("📈 Demand Forecasting Dashboard")
    st.caption("Weekly revenue forecast using baseline model")

    last_4_avg = weekly["revenue"].tail(4).mean()
    total_forecast = last_4_avg * 8

    k1,k2,k3 = st.columns(3)
    k1.metric("Avg Weekly Revenue (Last 4W)",
              f"BRL {last_4_avg:,.0f}")
    k2.metric("8-Week Revenue Forecast",
              f"BRL {total_forecast:,.0f}")
    k3.metric("Forecast Model",
              "Naive Baseline (WAPE 16.1%)")

    st.divider()

    st.subheader("Historical Revenue + 8-Week Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weekly["order_date"],
        y=weekly["revenue"],
        name="Historical",
        line=dict(color="#2563eb", width=2),
        fill="tozeroy",
        fillcolor="rgba(37,99,235,0.1)"))
    fig.add_trace(go.Scatter(
        x=forecast["order_date"],
        y=forecast["predicted_revenue"],
        name="Forecast",
        line=dict(color="#f59e0b", width=2, dash="dash")))
    fig.add_vline(
        x=weekly["order_date"].max(),
        line_dash="dot", line_color="gray",
        annotation_text="Forecast Start")
    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Revenue (BRL)",
        hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast Table")
    st.dataframe(
        forecast.rename(columns={
            "order_date":"Week",
            "predicted_revenue":"Forecasted Revenue (BRL)"})
        .style.format({"Forecasted Revenue (BRL)":"BRL {:.0f}"}),
        use_container_width=True)

    st.info("ℹ️ Naive baseline was selected over LightGBM "
            "(WAPE 16.1% vs 25.1%) due to limited training data "
            "(73 weeks). Accuracy will improve with more history.")

# ════════════════════════════════════════════════════════
# PAGE 4 — INVENTORY DASHBOARD
# ════════════════════════════════════════════════════════
elif page == "📦 Inventory Dashboard":
    st.title("📦 Inventory Optimization Dashboard")
    st.caption("ABC Analysis & Economic Order Quantity (EOQ)")

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Products", f"{len(inv):,}")
    k2.metric("Class A Products",
              f"{(inv['abc_class']=='A').sum():,}",
              "Drive 80% revenue")
    k3.metric("Class B Products",
              f"{(inv['abc_class']=='B').sum():,}",
              "Drive 15% revenue")
    k4.metric("Class C Products",
              f"{(inv['abc_class']=='C').sum():,}",
              "Drive 5% revenue")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ABC Revenue Distribution")
        fig = px.pie(abc_sum,
                     values="total_revenue",
                     names="abc_class",
                     color="abc_class",
                     color_discrete_map={
                         "A":"#22c55e",
                         "B":"#f59e0b",
                         "C":"#ef4444"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("ABC Class Summary")
        st.dataframe(
            abc_sum.style.format({
                "total_revenue": "BRL {:.0f}",
                "avg_price":     "BRL {:.2f}",
                "revenue_pct":   "{:.1f}%",
                "product_pct":   "{:.1f}%"}),
            use_container_width=True)

    st.subheader("Product Reorder Recommendations")

    abc_filter = st.selectbox(
        "Filter by ABC Class", ["A","B","C","All"])

    display_inv = inv.copy()
    if abc_filter != "All":
        display_inv = display_inv[
            display_inv["abc_class"]==abc_filter]

    display_inv = display_inv.sort_values(
        "total_revenue", ascending=False)

    st.dataframe(
        display_inv[["product_id","category","abc_class",
                     "total_revenue","annual_demand",
                     "EOQ","safety_stock"]]
        .head(50)
        .style.format({
            "total_revenue":  "BRL {:.0f}",
            "annual_demand":  "{:.0f}",
            "EOQ":            "{:.0f}",
            "safety_stock":   "{:.0f}"}),
        use_container_width=True)

    csv = display_inv.to_csv(index=False)
    st.download_button(
        "⬇️ Download Reorder List",
        csv, "reorder_list.csv", "text/csv")

st.divider()
st.caption("RetailPulse v1.0 | "
           "Built with Python, LightGBM & Streamlit | "
           "Olist E-Commerce Dataset")