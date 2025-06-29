#!/usr/bin/env python
"""
Initialize the database with initial data.
This script creates a default admin user and API key.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.db.user import User
from app.models.db.api_key import ApiKey


def init_db(db: Session) -> None:
    """
    Initialize the database with initial data
    """
    # Create a default admin user
    admin_email = os.getenv("ADMIN_EMAIL", "admin@agentlogger.com")
    admin_name = os.getenv("ADMIN_NAME", "Admin User")
    
    # Check if the admin user already exists
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        print(f"Creating admin user: {admin_email}")
        admin_user = User(
            email=admin_email,
            full_name=admin_name,
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    else:
        print(f"Admin user already exists: {admin_email}")
    
    # Create a default API key for the admin user if none exists
    api_key = db.query(ApiKey).filter(ApiKey.user_id == admin_user.id).first()
    if not api_key:
        print("Creating API key for admin user")
        import secrets
        from datetime import datetime, timedelta
        
        raw_api_key = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=365)
        
        api_key = ApiKey(
            key=raw_api_key,
            name="Default API Key",
            description="Default API key for admin user",
            is_active=True,
            expires_at=expires_at,
            user_id=admin_user.id,
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        
        print(f"\nAPI Key generated successfully!")
        print("=" * 60)
        print(f"API Key: {raw_api_key}")
        print(f"User ID: {admin_user.id}")
        print(f"Expires: {expires_at}")
        print("=" * 60)
        print("\nUse this key in your requests with the X-API-Key header:")
        print(f"curl -H 'X-API-Key: {raw_api_key}' http://localhost:8000/api/v1/health")
        print("=" * 60)
    else:
        print("API key already exists for admin user")


if __name__ == "__main__":
    print("Initializing database...")
    db = SessionLocal()
    try:
        init_db(db)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close() 