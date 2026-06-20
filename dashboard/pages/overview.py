import streamlit as st
import sys
import os
import plotly.express as px
import importlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import scripts.analysis
importlib.reload(scripts.analysis)

from scripts.analysis import (
    get_user_growth_df,
    get_revenue_over_time_df,
    get_course_performance_df
)

st.set_page_config(page_title="Overview Analytics - Mentoro", layout="wide")

st.markdown("# 📊 Platform Overview")
st.markdown("Detailed breakdown of system-wide analytics, including revenue growth trends and top-performing elements.")

# Metrics Over Time
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Revenue Trend (Last 30 Days)")
    revenue_df = get_revenue_over_time_df()
    fig_rev = px.line(
        revenue_df,
        x="date",
        y="daily_revenue",
        title="Revenue ($) per Day",
        color_discrete_sequence=["#10B981"]
    )
    fig_rev.update_traces(mode="lines+markers")
    st.plotly_chart(fig_rev, width='stretch')

with col2:
    st.subheader("User Account Registrations Growth")
    growth_df = get_user_growth_df()
    fig_growth = px.bar(
        growth_df,
        x="month",
        y="new_users",
        title="New Signups per Month",
        color_discrete_sequence=["#3B82F6"]
    )
    st.plotly_chart(fig_growth, width='stretch')

st.markdown("---")

st.subheader("Course Breakdown Overview")
courses_df = get_course_performance_df()

# Display tabular data of courses
st.dataframe(
    courses_df[["title", "price", "total_enrollments", "average_rating", "total_revenue"]],
    column_config={
        "title": "Course Name",
        "price": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
        "total_enrollments": st.column_config.NumberColumn("Enrollments"),
        "average_rating": st.column_config.NumberColumn("Avg Rating ⭐", format="%.1f"),
        "total_revenue": st.column_config.NumberColumn("Gross Income ($)", format="$%.2f")
    },
    width='stretch',
    hide_index=True
)

