import mysql.connector
import os
from mysql.connector import Error

def get_db_connection():
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "Joffy123456789@0")
    db_name = os.getenv("DB_NAME", "impactsense")
    
    try:
        # Connect with SSL enabled and a longer timeout for cloud environments
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            connection_timeout=20, # 20 second timeout
            ssl_disabled=False     # Aiven requires SSL
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cursor.close()
            # Now switch to the database
            conn.database = db_name
            return conn
            
    except Error as e:
        print(f"CRITICAL SQL ERROR: {e}")
        # Log specific helpful hints for Error 2003/110
        if "2003" in str(e) or "110" in str(e):
            print("HINT: This is a connection timeout. Check Aiven IP filters and DB_HOST format on Render.")
        return None
    return None

def init_db():
    conn = get_db_connection()
    if conn is None:
        print("CRITICAL: Could not establish database connection for initialization.")
        return
    
    cursor = conn.cursor()
    # Use standard VARCHAR lengths for compatibility
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            cdi FLOAT,
            mmi FLOAT,
            sig FLOAT,
            magnitude FLOAT,
            depth FLOAT,
            alert_level VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialization complete.")
