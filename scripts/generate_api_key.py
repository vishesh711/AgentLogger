#!/usr/bin/env python3
import secrets
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.db import SessionLocal
from app.models.db.user import User
from app.models.db.api_key import ApiKey

def generate_api_key():
    """Generate an API key for testing"""
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@agentlogger.com").first()
        
        # Create admin user if it doesn't exist
        if not admin_user:
            print("Creating admin user...")
            now = datetime.utcnow()
            admin_user = User(
                email="admin@agentlogger.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
                full_name="Admin User",
                is_active=True,
                is_superuser=True,
                created_at=now,
                updated_at=now
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        
        # Generate API key
        raw_api_key = secrets.token_urlsafe(32)
        now = datetime.utcnow()
        expires_at = now + timedelta(days=365)  # 1 year expiration
        
        # Use raw SQL to insert the API key
        from sqlalchemy import text
        query = text("""
            INSERT INTO api_keys (id, key, name, description, is_active, user_id, created_at, updated_at, expires_at)
            VALUES (:id, :key, :name, :description, :is_active, :user_id, :created_at, :updated_at, :expires_at)
        """)
        
        import uuid
        api_key_id = str(uuid.uuid4())
        
        db.execute(query, {
            "id": api_key_id,
            "key": raw_api_key,
            "name": "Test API Key",
            "description": "Generated for testing purposes",
            "is_active": True,
            "user_id": admin_user.id,
            "created_at": now,
            "updated_at": now,
            "expires_at": expires_at
        })
        
        db.commit()
        
        print("\nAPI Key generated successfully!")
        print("=" * 60)
        print(f"API Key: {raw_api_key}")
        print(f"User ID: {admin_user.id}")
        print(f"Expires: {expires_at}")
        print("=" * 60)
        print("\nUse this key in your requests with the X-API-Key header:")
        print(f"curl -H 'X-API-Key: {raw_api_key}' http://localhost:8000/api/v1/health")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error generating API key: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_api_key() 