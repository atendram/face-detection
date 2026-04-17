
import pyodbc
from .config.config import settings


def get_connection():
    conn = pyodbc.connect(
            "DRIVER={SQL Server};" 
            f"SERVER={settings.DB_SERVER};"
            f"DATABASE={settings.DB_NAME};"
            f"UID={settings.DB_USER};"
            f"PWD={settings.DB_PASSWORD};"
        )
    return conn

    