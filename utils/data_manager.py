"""
Data management utilities for the Hackathon Team Finder Discord Bot
"""

import json
import os
from typing import Dict, Any, List

def load_data() -> Dict[str, Any]:
    """Load user data from JSON file"""
    try:
        with open("example_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data: Dict[str, Any]) -> None:
    """Save user data to JSON file"""
    with open("example_data.json", "w") as f:
        json.dump(data, f, indent=2)

def load_hackathons() -> List[Dict[str, Any]]:
    """Load hackathon data from JSON file"""
    try:
        with open("example_hackathons.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_hackathons(hackathons: List[Dict[str, Any]]) -> None:
    """Save hackathon data to JSON file"""
    with open("example_hackathons.json", "w") as f:
        json.dump(hackathons, f, indent=2) 