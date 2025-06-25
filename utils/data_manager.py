"""
Data management utilities for the Hackathon Team Finder Discord Bot
"""

import json
import os
from typing import List, Dict, Any
from config import DATA_FILE, HACKATHONS_FILE

def load_data() -> Dict[str, Any]:
    """Load user data from JSON file - simple file reading"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data: Dict[str, Any]):
    """Save user data to JSON file - pretty printed for readability"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_hackathons() -> List[Dict[str, Any]]:
    """Load hackathons from JSON file - returns empty list if file doesn't exist"""
    if os.path.exists(HACKATHONS_FILE):
        with open(HACKATHONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_hackathons(hackathons: List[Dict[str, Any]]):
    """Save hackathons to JSON file - same pretty printing as user data"""
    with open(HACKATHONS_FILE, 'w') as f:
        json.dump(hackathons, f, indent=2) 