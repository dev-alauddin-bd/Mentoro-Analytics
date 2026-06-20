import os
import psycopg2
import certifi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
)


def get_connection():
    """
    Establish PostgreSQL connection
    """
    try:
        conn = psycopg2.connect(DATABASE_URL, sslrootcert=certifi.where())
        print("✅ Database connected successfully")
        return conn

    except Exception as e:
        error_msg = f"❌ Error connecting to database: {e}\n"
        print(error_msg)
        try:
            log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db_error.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(error_msg)
        except Exception as log_err:
            print(f"Failed to write log file: {log_err}")
        return None