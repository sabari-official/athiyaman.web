#!/usr/bin/env python
"""Update admin password hash in database"""

from sqlalchemy import create_engine, text
from backend.core.config import settings

# Connect to database
engine = create_engine(settings.DATABASE_URL)

with engine.connect() as connection:
    # Update admin password with Argon2 hash (matching backend/utils/security.py)
    correct_hash = "$argon2id$v=19$m=65536,t=3,p=4$cQ7BmJPyHgPAGGNM6b2X0g$yG4DOlEEUydS/T1oE2Lq/GMSoZNQfPUZDuy3HsKpUPg"
    query = text("UPDATE users SET password_hash = :hash WHERE username = 'admin'")
    connection.execute(query, {"hash": correct_hash})
    connection.commit()
    print("✓ Admin password hash updated successfully!")

# Verify update
with engine.connect() as connection:
    result = connection.execute(text("SELECT username, password_hash FROM users WHERE username = 'admin'"))
    row = result.fetchone()
    if row:
        print(f"✓ Verified: {row[0]} hash: {row[1][:20]}...")
