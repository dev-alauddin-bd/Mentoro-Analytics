import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import importlib

# Trigger reload with certifi 2
# Include the parent directory in Python path to import from scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scripts.db_connect
importlib.reload(scripts.db_connect)
import scripts.analysis
importlib.reload(scripts.analysis)

from scripts.analysis import (
    get_user_metrics_df,
    get_course_performance_df,
    get_revenue_metrics_df,
    get_live_session_metrics_df,
    get_connection_status
)

# Set page configuration with premium styling
st.set_page_config(
    page_title="Mentoro Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #3B82F6;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1F2937;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Design
st.sidebar.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=200&auto=format&fit=crop&q=60", width=120)
st.sidebar.title("Mentoro Portal")
st.sidebar.info("Use the pages below or the sidebar list to explore specific domains.")

# Content layout
st.markdown('<div class="main-title">Mentoro Analytics 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time educational portal overview and analytics insight engine.</div>', unsafe_allow_html=True)

# Fetching aggregated data
users_df = get_user_metrics_df()
courses_df = get_course_performance_df()
revenue_df = get_revenue_metrics_df()
live_df = get_live_session_metrics_df()

# Metrics calculations
total_students = users_df[users_df['role'] == 'student']['count'].sum()
total_instructors = users_df[users_df['role'] == 'instructor']['count'].sum()
total_courses = len(courses_df)
completed_rev = revenue_df[revenue_df['status'] == 'COMPLETED']['total_amount'].sum()

# Displaying KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #3B82F6;">
        <div class="metric-label">Total Active Students</div>
        <div class="metric-value">{total_students:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10B981;">
        <div class="metric-label">Total Instructors</div>
        <div class="metric-value">{total_instructors}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #F59E0B;">
        <div class="metric-label">Active Courses</div>
        <div class="metric-value">{total_courses}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #8B5CF6;">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${completed_rev:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Page Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("User Distribution by Role")
    role_summary = users_df.groupby('role')['count'].sum().reset_index()
    fig_roles = px.pie(
        role_summary, 
        values='count', 
        names='role', 
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4
    )
    fig_roles.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_roles, width='stretch')

with col_right:
    st.subheader("Upcoming Live Sessions Registrations")
    upcoming_sessions = live_df.head(5)
    fig_live = px.bar(
        upcoming_sessions,
        x='registrations_count',
        y='title',
        orientation='h',
        color='level',
        labels={'registrations_count': 'Registrations', 'title': 'Session Title'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_live.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_live, width='stretch')
st.write("👈 Select a detailed view page in the sidebar (Overview, Users, Revenue, or Courses) to see deeper metrics.")

# Dynamic Connection Status Display
status = get_connection_status()
if status["connected"]:
    if "empty" in status["reason"]:
        st.warning(f"⚠️ {status['reason']}")
    else:
        st.success(f"✅ Dashboard successfully loaded! Real-time connection: {status['reason']}")
else:
    st.error(f"❌ Showing Mock Fallback. Database connection failed: {status['reason']}")

