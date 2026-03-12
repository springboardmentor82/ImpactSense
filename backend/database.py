import mysql.connector
import os
from mysql.connector import Error

def get_db_connection():
    host_raw = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "Joffy123456789@0")
    db_name = os.getenv("DB_NAME", "impactsense")
    
    # Clean host and extract port if present (e.g., "host:3306")
    port = 3306
    if ":" in host_raw:
        host, port_str = host_raw.split(":")
        try:
            port = int(port_str)
        except ValueError:
            pass
    else:
        host = host_raw

    try:
        # Aiven requires SSL. Using 'ssl_disabled=False' for maximum compatibility 
        # with different versions of mysql-connector-python.
        print(f"DEBUG: Attempting connection to {host} on port {port} as user {user}")
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connection_timeout=20,
            use_pure=True,
            ssl_disabled=False # This forces SSL on for Aiven
        )
        
        if conn.is_connected():
            print("DEBUG: Connection established!")
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cursor.close()
            conn.database = db_name
            return conn
            
    except Error as e:
        print(f"CRITICAL SQL ERROR: {e}")
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
