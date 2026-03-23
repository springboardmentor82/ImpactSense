import mysql.connector
from mysql.connector import Error
import os
import sys

def test_connection():
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = "Joffy123456789@0" # hardcoded for test as per user's edit
    database = os.getenv("DB_NAME", "impactsense")

    print(f"Attempting to connect to MySQL at {host}...")
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print("Successfully connected to the database!")
            conn.close()
    except Error as e:
        print(f"\n--- CONNECTION FAILED ---")
        print(f"Error Code: {e.errno}")
        print(f"SQLSTATE: {e.sqlstate}")
        print(f"Message: {e.msg}")
        
        if e.errno == 1045:
            print("\nAdvice: Access denied. Check your username and password.")
        elif e.errno == 1049:
            print(f"\nAdvice: Database '{database}' does not exist. You need to create it first.")
            print(f"Run: CREATE DATABASE {database};")
        elif e.errno == 2003:
            print("\nAdvice: Can't connect to MySQL server. Is MySQL actually running on your machine?")
        else:
            print("\nAdvice: Please check your MySQL server status and credentials.")

if __name__ == "__main__":
    test_connection()
