import streamlit as st
import sys
import os
import plotly.express as px
import importlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import scripts.analysis
importlib.reload(scripts.analysis)

from scripts.analysis import get_user_metrics_df, get_user_growth_df

st.set_page_config(page_title="User Analytics - Mentoro", layout="wide")

st.markdown("# 👥 User Analytics")
st.markdown("Analyze student and instructor signups, activity logs, statuses, and growth charts.")

users_df = get_user_metrics_df()

# User Status breakdown
st.subheader("Account Status by Role")
col1, col2 = st.columns(2)

with col1:
    fig_status = px.bar(
        users_df,
        x="role",
        y="count",
        color="status",
        barmode="group",
        title="Active vs Blocked Accounts per Role",
        color_discrete_map={"active": "#10B981", "blocked": "#EF4444"}
    )
    st.plotly_chart(fig_status, width='stretch')

with col2:
    st.markdown("### Quick Statistics Summary")
    total_users = users_df["count"].sum()
    active_users = users_df[users_df["status"] == "active"]["count"].sum()
    blocked_users = users_df[users_df["status"] == "blocked"]["count"].sum()
    blocked_pct = (blocked_users / total_users) * 100 if total_users > 0 else 0

    st.metric("Total Registered Accounts", f"{total_users:,}")
    st.metric("Active Portals", f"{active_users:,}")
    st.metric("Suspended Accounts", f"{blocked_users:,}", f"{blocked_pct:.1f}% of total", delta_color="inverse")

st.markdown("---")

st.subheader("Monthly Signups Growth")
growth_df = get_user_growth_df()
fig_growth = px.area(
    growth_df,
    x="month",
    y="new_users",
    title="Cumulative Monthly Acquisition Curve",
    color_discrete_sequence=["#8B5CF6"]
)
st.plotly_chart(fig_growth, width='stretch')

