import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from .db_connect import get_connection
from . import queries

def fetch_data_or_mock(query, mock_func):
    """
    Tries to connect to the DB and execute the query.
    If it fails or connection is None, calls mock_func to return mock data.
    """
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db_error.log")
    conn = get_connection()
    if conn is None:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"Fallback to mock: connection is None at {datetime.now()}\n")
        return mock_func()
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        # If DB is empty, return mock data to keep dashboard visually complete
        if df.empty:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"Fallback to mock: query returned empty dataframe for query: {query[:50]}... at {datetime.now()}\n")
            return mock_func()
        return df
    except Exception as e:
        error_msg = f"Database query failed: {e}. Falling back to mock data.\n"
        print(error_msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"Fallback to mock: query failed: {e} for query: {query[:50]}... at {datetime.now()}\n")
        try:
            conn.close()
        except:
            pass
        return mock_func()


# --- Mock Data Generators ---

def get_mock_user_metrics():
    return pd.DataFrame([
        {"role": "student", "status": "active", "count": 1250},
        {"role": "student", "status": "blocked", "count": 15},
        {"role": "instructor", "status": "active", "count": 48},
        {"role": "admin", "status": "active", "count": 5}
    ])

def get_mock_user_growth():
    months = [datetime.now() - timedelta(days=30 * i) for i in range(6, 0, -1)]
    return pd.DataFrame({
        "month": [m.strftime("%Y-%m") for m in months],
        "new_users": [85, 120, 150, 190, 240, 310]
    })

def get_mock_course_performance():
    return pd.DataFrame([
        {"id": "1", "title": "Full-Stack Web Development BootCamp", "price": 99.99, "isPublished": True, "total_enrollments": 450, "average_rating": 4.8, "total_revenue": 44995.50},
        {"id": "2", "title": "Python for Data Science & AI", "price": 79.99, "isPublished": True, "total_enrollments": 380, "average_rating": 4.7, "total_revenue": 30396.20},
        {"id": "3", "title": "Advanced React & Next.js Pattern Guide", "price": 49.99, "isPublished": True, "total_enrollments": 290, "average_rating": 4.6, "total_revenue": 14497.10},
        {"id": "4", "title": "Introduction to Machine Learning", "price": 120.00, "isPublished": True, "total_enrollments": 180, "average_rating": 4.5, "total_revenue": 21600.00},
        {"id": "5", "title": "UI/UX Design Fundamentals", "price": 39.99, "isPublished": True, "total_enrollments": 150, "average_rating": 4.3, "total_revenue": 5998.50},
        {"id": "6", "title": "NestJS Microservices Mastery", "price": 89.99, "isPublished": False, "total_enrollments": 0, "average_rating": 0.0, "total_revenue": 0.0}
    ])

def get_mock_revenue_metrics():
    return pd.DataFrame([
        {"status": "COMPLETED", "type": "COURSE_PURCHASE", "total_amount": 117487.30, "payment_count": 1450},
        {"status": "PENDING", "type": "COURSE_PURCHASE", "total_amount": 3450.00, "payment_count": 45},
        {"status": "FAILED", "type": "COURSE_PURCHASE", "total_amount": 1200.00, "payment_count": 12},
        {"status": "COMPLETED", "type": "FEATURED_REQUEST", "total_amount": 1500.00, "payment_count": 15}
    ])

def get_mock_revenue_over_time():
    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    revenues = [np.random.randint(1000, 5000) for _ in range(30)]
    return pd.DataFrame({
        "date": [d.strftime("%Y-%m-%d") for d in dates],
        "daily_revenue": revenues
    })

def get_mock_live_session_metrics():
    return pd.DataFrame([
        {"title": "Mastering Git & GitHub Collaboration", "level": "BEGINNER", "sessionDate": datetime.now() + timedelta(days=2), "maxCapacity": 100, "registrations_count": 87},
        {"title": "Building REST APIs with Express & Prisma", "level": "INTERMEDIATE", "sessionDate": datetime.now() + timedelta(days=5), "maxCapacity": 150, "registrations_count": 124},
        {"title": "Intro to Pandas Dataframes & Streamlit", "level": "BEGINNER", "sessionDate": datetime.now() - timedelta(days=3), "maxCapacity": 80, "registrations_count": 78},
        {"title": "Deploying Docker Containers to AWS", "level": "ADVANCED", "sessionDate": datetime.now() + timedelta(days=12), "maxCapacity": 50, "registrations_count": 42}
    ])

# --- Exported functions ---

def get_user_metrics_df():
    return fetch_data_or_mock(queries.GET_USER_METRICS, get_mock_user_metrics)

def get_user_growth_df():
    return fetch_data_or_mock(queries.GET_USER_GROWTH, get_mock_user_growth)

def get_course_performance_df():
    return fetch_data_or_mock(queries.GET_COURSE_PERFORMANCE, get_mock_course_performance)

def get_revenue_metrics_df():
    return fetch_data_or_mock(queries.GET_REVENUE_METRICS, get_mock_revenue_metrics)

def get_revenue_over_time_df():
    return fetch_data_or_mock(queries.GET_REVENUE_OVER_TIME, get_mock_revenue_over_time)

def get_live_session_metrics_df():
    return fetch_data_or_mock(queries.GET_LIVE_SESSION_METRICS, get_mock_live_session_metrics)

def get_connection_status():
    conn = get_connection()
    if conn is None:
        return {"connected": False, "reason": "Connection failed (check DATABASE_URL or network)"}
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        if count == 0:
            return {"connected": True, "reason": "Connected, but database is empty (0 users). Run seed script."}
        return {"connected": True, "reason": f"Connected with active data ({count} users)"}
    except Exception as e:
        try:
            conn.close()
        except:
            pass
        return {"connected": False, "reason": f"Connected, but query failed: {e}"}

