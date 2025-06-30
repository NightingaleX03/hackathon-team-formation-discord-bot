"""
Database utilities for the Hackathon Team Finder Discord Bot
"""

import os
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create base class for models
Base = declarative_base()

class UserProfile(Base):
    """User profile model"""
    __tablename__ = 'user_profiles'
    
    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), nullable=False)
    roles = Column(JSON, default=list)
    tech_skills = Column(JSON, default=list)
    experience = Column(String(50))
    timezone = Column(String(10))
    looking_for_team = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Hackathon(Base):
    """Hackathon model"""
    __tablename__ = 'hackathons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(String(100))
    teams = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatabaseManager:
    """Database manager for handling PostgreSQL operations"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._setup_database()
    
    def _setup_database(self):
        """Set up database connection"""
        try:
            # Get database URL from environment variable
            database_url = os.getenv('DATABASE_URL')
            
            if not database_url:
                # Fallback to local SQLite for development
                logger.warning("DATABASE_URL not found, using SQLite for development")
                database_url = "sqlite:///./bot_data.db"
            
            # Create engine
            self.engine = create_engine(database_url)
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables
            Base.metadata.create_all(bind=self.engine)
            
            logger.info("Database connection established successfully")
            
        except Exception as e:
            logger.error(f"Failed to set up database: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def close_session(self, session: Session):
        """Close database session"""
        session.close()

# Global database manager instance
db_manager = DatabaseManager()

def get_db_session() -> Session:
    """Get a database session"""
    return db_manager.get_session()

def close_db_session(session: Session):
    """Close a database session"""
    db_manager.close_session(session)

# User profile operations
def save_user_profile(user_data: Dict[str, Any]) -> bool:
    """Save or update user profile"""
    session = get_db_session()
    try:
        # Check if user exists
        existing_user = session.query(UserProfile).filter(UserProfile.user_id == user_data['user_id']).first()
        
        if existing_user:
            # Update existing user
            for key, value in user_data.items():
                if hasattr(existing_user, key):
                    setattr(existing_user, key, value)
            existing_user.updated_at = datetime.utcnow()
        else:
            # Create new user
            new_user = UserProfile(**user_data)
            session.add(new_user)
        
        session.commit()
        logger.info(f"User profile saved/updated for user {user_data['user_id']}")
        return True
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error saving user profile: {e}")
        return False
    finally:
        close_db_session(session)

def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile by user ID"""
    session = get_db_session()
    try:
        user = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if user:
            return {
                'user_id': user.user_id,
                'username': user.username,
                'roles': user.roles or [],
                'tech_skills': user.tech_skills or [],
                'experience': user.experience,
                'timezone': user.timezone,
                'looking_for_team': user.looking_for_team,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
        return None
        
    except SQLAlchemyError as e:
        logger.error(f"Error getting user profile: {e}")
        return None
    finally:
        close_db_session(session)

def get_all_users() -> List[Dict[str, Any]]:
    """Get all user profiles"""
    session = get_db_session()
    try:
        users = session.query(UserProfile).all()
        return [
            {
                'user_id': user.user_id,
                'username': user.username,
                'roles': user.roles or [],
                'tech_skills': user.tech_skills or [],
                'experience': user.experience,
                'timezone': user.timezone,
                'looking_for_team': user.looking_for_team,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
            for user in users
        ]
        
    except SQLAlchemyError as e:
        logger.error(f"Error getting all users: {e}")
        return []
    finally:
        close_db_session(session)

def delete_user_profile(user_id: str) -> bool:
    """Delete user profile"""
    session = get_db_session()
    try:
        user = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            logger.info(f"User profile deleted for user {user_id}")
            return True
        return False
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error deleting user profile: {e}")
        return False
    finally:
        close_db_session(session)

# Hackathon operations
def save_hackathon(hackathon_data: Dict[str, Any]) -> bool:
    """Save or update hackathon"""
    session = get_db_session()
    try:
        if 'id' in hackathon_data and hackathon_data['id']:
            # Update existing hackathon
            existing_hackathon = session.query(Hackathon).filter(Hackathon.id == hackathon_data['id']).first()
            if existing_hackathon:
                for key, value in hackathon_data.items():
                    if hasattr(existing_hackathon, key) and key != 'id':
                        setattr(existing_hackathon, key, value)
                existing_hackathon.updated_at = datetime.utcnow()
        else:
            # Create new hackathon
            new_hackathon = Hackathon(**hackathon_data)
            session.add(new_hackathon)
        
        session.commit()
        logger.info(f"Hackathon saved/updated: {hackathon_data.get('name', 'Unknown')}")
        return True
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error saving hackathon: {e}")
        return False
    finally:
        close_db_session(session)

def get_hackathon(hackathon_id: int) -> Optional[Dict[str, Any]]:
    """Get hackathon by ID"""
    session = get_db_session()
    try:
        hackathon = session.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if hackathon:
            return {
                'id': hackathon.id,
                'name': hackathon.name,
                'description': hackathon.description,
                'date': hackathon.date,
                'teams': hackathon.teams or [],
                'created_at': hackathon.created_at.isoformat() if hackathon.created_at else None,
                'updated_at': hackathon.updated_at.isoformat() if hackathon.updated_at else None
            }
        return None
        
    except SQLAlchemyError as e:
        logger.error(f"Error getting hackathon: {e}")
        return None
    finally:
        close_db_session(session)

def get_all_hackathons() -> List[Dict[str, Any]]:
    """Get all hackathons"""
    session = get_db_session()
    try:
        hackathons = session.query(Hackathon).all()
        return [
            {
                'id': hackathon.id,
                'name': hackathon.name,
                'description': hackathon.description,
                'date': hackathon.date,
                'teams': hackathon.teams or [],
                'created_at': hackathon.created_at.isoformat() if hackathon.created_at else None,
                'updated_at': hackathon.updated_at.isoformat() if hackathon.updated_at else None
            }
            for hackathon in hackathons
        ]
        
    except SQLAlchemyError as e:
        logger.error(f"Error getting all hackathons: {e}")
        return []
    finally:
        close_db_session(session)

def delete_hackathon(hackathon_id: int) -> bool:
    """Delete hackathon"""
    session = get_db_session()
    try:
        hackathon = session.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if hackathon:
            session.delete(hackathon)
            session.commit()
            logger.info(f"Hackathon deleted: {hackathon.name}")
            return True
        return False
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error deleting hackathon: {e}")
        return False
    finally:
        close_db_session(session)

def add_user_to_hackathon(hackathon_id: int, user_id: str, username: str) -> bool:
    """Add user to hackathon team"""
    session = get_db_session()
    try:
        hackathon = session.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if hackathon:
            teams = hackathon.teams or []
            
            # Check if user is already in the team
            if not any(member.get('user_id') == user_id for member in teams):
                teams.append({
                    'user_id': user_id,
                    'username': username,
                    'joined_at': datetime.utcnow().isoformat()
                })
                hackathon.teams = teams
                hackathon.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"User {username} added to hackathon {hackathon.name}")
                return True
            else:
                logger.info(f"User {username} is already in hackathon {hackathon.name}")
                return False
        return False
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error adding user to hackathon: {e}")
        return False
    finally:
        close_db_session(session)

def remove_user_from_hackathon(hackathon_id: int, user_id: str) -> bool:
    """Remove user from hackathon team"""
    session = get_db_session()
    try:
        hackathon = session.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if hackathon:
            teams = hackathon.teams or []
            original_length = len(teams)
            
            # Remove user from team
            teams = [member for member in teams if member.get('user_id') != user_id]
            
            if len(teams) < original_length:
                hackathon.teams = teams
                hackathon.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"User {user_id} removed from hackathon {hackathon.name}")
                return True
            else:
                logger.info(f"User {user_id} not found in hackathon {hackathon.name}")
                return False
        return False
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error removing user from hackathon: {e}")
        return False
    finally:
        close_db_session(session) 