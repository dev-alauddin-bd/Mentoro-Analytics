import streamlit as st
import sys
import os
import plotly.express as px
import importlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import scripts.analysis
importlib.reload(scripts.analysis)

from scripts.analysis import get_course_performance_df

st.set_page_config(page_title="Course Engagement - Mentoro", layout="wide")

st.markdown("# 🎓 Course Performance & Engagement")
st.markdown("Track enrollments, pricing, ratings, and gross earnings by courses.")

courses_df = get_course_performance_df()

# Metrics
total_courses = len(courses_df)
published_courses = len(courses_df[courses_df["isPublished"] == True])
draft_courses = total_courses - published_courses

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Catalog Items", total_courses)
with col2:
    st.metric("Published Catalog", published_courses)
with col3:
    st.metric("Draft Catalog Items", draft_courses)

st.markdown("---")

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Enrollment Leaderboard")
    enrollment_df = courses_df.sort_values(by="total_enrollments", ascending=True)
    fig_enroll = px.bar(
        enrollment_df,
        x="total_enrollments",
        y="title",
        orientation="h",
        title="Top Enrolled Courses",
        color="total_enrollments",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_enroll, width='stretch')

with col_chart2:
    st.subheader("Average Ratings & Pricing Relationship")
    fig_ratings = px.scatter(
        courses_df,
        x="price",
        y="average_rating",
        size="total_enrollments",
        hover_name="title",
        title="Course Rating vs Price (Bubble size = enrollments)",
        color="average_rating",
        color_continuous_scale=px.colors.sequential.Cividis
    )
    st.plotly_chart(fig_ratings, width='stretch')

