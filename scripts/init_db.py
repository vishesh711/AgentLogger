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
from app.models.schemas.user import UserCreate
from app.models.schemas.api_key import ApiKeyCreate
from app.services.user_service import create_user
from app.services.api_key_service import create_api_key


def init_db(db: Session) -> None:
    """
    Initialize the database with initial data
    """
    # Create a default admin user
    admin_email = os.getenv("ADMIN_EMAIL", "admin@agentlogger.com")
    admin_name = os.getenv("ADMIN_NAME", "Admin")
    
    # Check if the admin user already exists
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        print(f"Creating admin user: {admin_email}")
        admin_user = User(
            email=admin_email,
            name=admin_name,
            is_active=True,
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
        api_key = ApiKey(
            key=ApiKey.generate_key(),
            name="Default API Key",
            is_active=True,
            expires_at=ApiKey.generate_expiry(days=365),
            user_id=admin_user.id,
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        
        print(f"API Key: {api_key.key}")
        print("IMPORTANT: Save this API key as it will not be shown again!")
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