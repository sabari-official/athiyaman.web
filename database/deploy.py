import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Reconfigure stdout to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Adjust python path to allow root imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core.config import settings

def create_database_if_not_exists():
    print("--- 1. Checking Database Existence ---")
    
    # Connection URL to postgres default database to check / create our target db
    postgres_url = f"{settings.DB_DRIVER}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
    engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
    
    try:
        with engine.connect() as conn:
            # Check if target db exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}';"))
            exists = result.fetchone()
            
            if not exists:
                print(f"Database '{settings.DB_NAME}' does not exist. Creating it...")
                conn.execute(text(f"CREATE DATABASE {settings.DB_NAME};"))
                print(f"✓ Database '{settings.DB_NAME}' created successfully!")
            else:
                print(f"✓ Database '{settings.DB_NAME}' already exists.")
            return True
    except Exception as e:
        print(f"✗ Failed to check or create database '{settings.DB_NAME}': {e}")
        print("Please check that the PostgreSQL server is running and the credentials in '.env' are correct.")
        return False

def execute_sql_file(file_path):
    print(f"\n--- Executing {os.path.basename(file_path)} ---")
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return False
        
    # Standard connection URL to the target database
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_content = f.read()
            
        with engine.begin() as connection:
            # Execute entire file content in a single transaction
            connection.execute(text(sql_content))
            
        print(f"✓ Successfully executed {os.path.basename(file_path)}!")
        return True
    except Exception as e:
        print(f"✗ Failed to execute {os.path.basename(file_path)}: {e}")
        return False

if __name__ == "__main__":
    print("=========================================================")
    print("ATHIYAMAN PLATFORM — AUTOMATED DATABASE DEPLOYER")
    print("=========================================================")
    
    # 1. Create target database if it doesn't exist
    db_created = create_database_if_not_exists()
    
    if db_created:
        # 2. Execute schema.sql to create tables, indexes, triggers, and views
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        schema_ok = execute_sql_file(schema_path)
        
        if schema_ok:
            # 3. Execute seed.sql to populate defaults and level engines
            seed_path = os.path.join(os.path.dirname(__file__), "seed.sql")
            seed_ok = execute_sql_file(seed_path)
            
            if seed_ok:
                print("\n=========================================================")
                print("🎉 DATABASE DEPLOYMENT COMPLETE & FULLY READY!")
                print("=========================================================")
                sys.exit(0)
                
    sys.exit(1)
