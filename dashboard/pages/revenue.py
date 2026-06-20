import streamlit as st
import sys
import os
import plotly.express as px
import importlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import scripts.analysis
importlib.reload(scripts.analysis)

from scripts.analysis import get_revenue_metrics_df, get_revenue_over_time_df

st.set_page_config(page_title="Revenue Insights - Mentoro", layout="wide")

st.markdown("# 💰 Revenue Insights")
st.markdown("Detailed analytics on platform sales, course transactions, and Stripe performance.")

revenue_df = get_revenue_metrics_df()

# Metrics calculations
completed_tx = revenue_df[revenue_df['status'] == 'COMPLETED']
total_completed_revenue = completed_tx['total_amount'].sum()
total_completed_sales = completed_tx['payment_count'].sum()

pending_tx = revenue_df[revenue_df['status'] == 'PENDING']
total_pending_revenue = pending_tx['total_amount'].sum()

failed_tx = revenue_df[revenue_df['status'] == 'FAILED']

# Metric row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Realized Earnings", f"${total_completed_revenue:,.2f}")
with col2:
    st.metric("Completed Transactions", f"{total_completed_sales:,} payments")
with col3:
    st.metric("Pending Invoices Value", f"${total_pending_revenue:,.2f}")

st.markdown("---")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Revenue Breakdown by Transaction Type")
    # type distribution
    type_df = revenue_df.groupby('type')['total_amount'].sum().reset_index()
    fig_type = px.pie(
        type_df,
        values='total_amount',
        names='type',
        title="Revenue by Purchase Option",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_type, width='stretch')

with col_chart2:
    st.subheader("Invoice Volume Status Distribution")
    status_df = revenue_df.groupby('status')['payment_count'].sum().reset_index()
    fig_status = px.bar(
        status_df,
        x='status',
        y='payment_count',
        color='status',
        title="Number of Invoices by Current Status",
        color_discrete_map={"COMPLETED": "#10B981", "PENDING": "#F59E0B", "FAILED": "#EF4444", "REFUNDED": "#6B7280"}
    )
    st.plotly_chart(fig_status, width='stretch')

