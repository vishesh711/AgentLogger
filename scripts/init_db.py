#!/usr/bin/env python
"""
Initialize the database with initial data.
This script creates a default admin user and API key.
"""

import os
import sys
from pathlib import Path
from uuid import uuid4

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.core.db import SessionLocal, engine
from app.models.db.user import User
from app.models.db.api_key import ApiKey
from app.models.db.base import BaseModel


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    BaseModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


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
        
        # Hash the default password
        from app.api.v1.endpoints.auth import get_password_hash
        default_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        admin_user = User(
            id=str(uuid4()),
            email=admin_email,
            full_name=admin_name,
            hashed_password=get_password_hash(default_password),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✓ Admin user created: {admin_email}")
        print(f"✓ Default password: {default_password}")
    else:
        print(f"✓ Admin user already exists: {admin_email}")
    
    # Create a default API key for the admin user if none exists
    api_key = db.query(ApiKey).filter(ApiKey.user_id == admin_user.id).first()
    if not api_key:
        print("Creating API key for admin user...")
        import secrets
        from datetime import datetime, timedelta
        
        raw_api_key = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=365)
        
        api_key = ApiKey(
            id=str(uuid4()),
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
        
        print("\n" + "="*60)
        print("🎉 API Key Generated Successfully!")
        print("="*60)
        print(f"API Key: {raw_api_key}")
        print(f"User ID: {admin_user.id}")
        print(f"Email: {admin_user.email}")
        print(f"Expires: {expires_at}")
        print("="*60)
        print("\n💡 Use this key in your requests:")
        print(f"curl -H 'X-API-Key: {raw_api_key}' http://localhost:8000/api/v1/health")
        print("="*60)
        
        # Save to file for easy access
        with open("api_key.txt", "w") as f:
            f.write(f"API_KEY={raw_api_key}\n")
            f.write(f"USER_ID={admin_user.id}\n")
            f.write(f"EMAIL={admin_user.email}\n")
        print("📝 API key saved to api_key.txt")
        
    else:
        print("✓ API key already exists for admin user")


if __name__ == "__main__":
    print("🚀 Initializing AgentLogger database...")
    
    try:
        # Create tables first
        create_tables()
        
        # Initialize data
        db = SessionLocal()
        try:
            init_db(db)
            print("✅ Database initialized successfully!")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 