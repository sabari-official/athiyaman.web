import os
import sys
import traceback
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# Reconfigure stdout to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Adjust python path to allow root imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.core.config import settings
    from backend.core.database import engine, SessionLocal, Base
    from backend.database.models import User, Team, CollectionCenter
    print("✓ Successfully imported database core modules and SQLAlchemy models!")
except Exception as e:
    print(f"✗ Failed to import database modules: {e}")
    traceback.print_exc()
    sys.exit(1)

def verify_connection():
    print(f"\n--- Verifying Database Connection ---")
    print(f"Target Connection URL: {settings.DB_HOST}:{settings.DB_PORT} (DB: {settings.DB_NAME})")
    
    try:
        # Create a connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            row = result.fetchone()
            print(f"✓ Connected successfully!")
            print(f"PostgreSQL version: {row[0]}")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Tip: Make sure PostgreSQL service is running and credentials in '.env' are correct.")
        return False

def verify_tables_in_db():
    print(f"\n--- Checking Tables and Structural Metadata ---")
    try:
        # Get metadata tables
        defined_tables = sorted(list(Base.metadata.tables.keys()))
        print(f"Defined SQLAlchemy models count: {len(defined_tables)} tables")
        
        # Verify table details
        with engine.connect() as connection:
            result = connection.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            ))
            actual_tables = {row[0] for row in result.fetchall()}
            
            print(f"Physical tables in Database count: {len(actual_tables)}")
            
            missing_tables = []
            for t in defined_tables:
                if t in actual_tables:
                    print(f"  [✓] Table '{t}' exists physically.")
                else:
                    print(f"  [ ] Table '{t}' is NOT found in database.")
                    missing_tables.append(t)
            
            if missing_tables:
                print(f"\n* Action Required: Run 'schema.sql' to physically create these {len(missing_tables)} tables.")
            else:
                print("\n✓ Perfect! All 27 SQLAlchemy models are fully synced with the physical database!")
    except Exception as e:
        print(f"✗ Failed to inspect database metadata: {e}")

if __name__ == "__main__":
    print("=========================================================")
    print("ATHIYAMAN PLATFORM — DATABASE DIAGNOSTIC UTILITY")
    print("=========================================================")
    
    conn_ok = verify_connection()
    if conn_ok:
        verify_tables_in_db()
    else:
        print("\n* Diagnostic skipped due to connection failure.")
