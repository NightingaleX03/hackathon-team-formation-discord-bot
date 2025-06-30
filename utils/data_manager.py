"""
Data management utilities for the Hackathon Team Finder Discord Bot
"""

import json
import os
from typing import Dict, Any, List
from .database import (
    save_user_profile, get_user_profile, get_all_users, delete_user_profile,
    save_hackathon, get_hackathon, get_all_hackathons, delete_hackathon,
    add_user_to_hackathon, remove_user_from_hackathon
)

def load_data() -> Dict[str, Any]:
    """Load user data from database"""
    try:
        users = get_all_users()
        # Convert list to dict format for backward compatibility
        user_dict = {}
        for user in users:
            user_dict[user['user_id']] = user
        return user_dict
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return {}

def save_data(data: Dict[str, Any]) -> None:
    """Save user data to database"""
    try:
        for user_id, user_data in data.items():
            save_user_profile(user_data)
    except Exception as e:
        print(f"Error saving data to database: {e}")

def load_hackathons() -> List[Dict[str, Any]]:
    """Load hackathon data from database"""
    try:
        return get_all_hackathons()
    except Exception as e:
        print(f"Error loading hackathons from database: {e}")
        return []

def save_hackathons(hackathons: List[Dict[str, Any]]) -> None:
    """Save hackathon data to database"""
    try:
        for hackathon in hackathons:
            save_hackathon(hackathon)
    except Exception as e:
        print(f"Error saving hackathons to database: {e}")

# Additional helper functions for better database integration
def get_user_by_id(user_id: str) -> Dict[str, Any]:
    """Get a specific user by ID"""
    return get_user_profile(user_id) or {}

def save_user(user_data: Dict[str, Any]) -> bool:
    """Save a single user"""
    return save_user_profile(user_data)

def delete_user(user_id: str) -> bool:
    """Delete a user by ID"""
    return delete_user_profile(user_id)

def get_hackathon_by_id(hackathon_id: int) -> Dict[str, Any]:
    """Get a specific hackathon by ID"""
    return get_hackathon(hackathon_id) or {}

def save_single_hackathon(hackathon_data: Dict[str, Any]) -> bool:
    """Save a single hackathon"""
    return save_hackathon(hackathon_data)

def delete_hackathon_by_id(hackathon_id: int) -> bool:
    """Delete a hackathon by ID"""
    return delete_hackathon(hackathon_id)

def join_hackathon(hackathon_id: int, user_id: str, username: str) -> bool:
    """Add user to hackathon team"""
    return add_user_to_hackathon(hackathon_id, user_id, username)

def leave_hackathon(hackathon_id: int, user_id: str) -> bool:
    """Remove user from hackathon team"""
    return remove_user_from_hackathon(hackathon_id, user_id) 