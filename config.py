"""
Configuration file for the Hackathon Team Matcher Discord Bot
"""

import os

# Bot Configuration
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
DATA_FILE = "data.json"

# Matching Algorithm Weights
TIMEZONE_MATCH_SCORE = 2
ROLE_COMPLEMENT_SCORE = 3
TECH_STACK_MATCH_SCORE = 1

# Maximum number of matches to return
MAX_MATCHES = 3

# Complementary role pairs for scoring
COMPLEMENTARY_ROLES = [
    ("frontend", "backend"),
    ("backend", "frontend"),
    ("pm", "developer"),
    ("pm", "frontend"),
    ("pm", "backend"),
    ("designer", "developer"),
    ("designer", "frontend"),
    ("designer", "backend"),
    ("full-stack", "frontend"),
    ("full-stack", "backend"),
    ("devops", "backend"),
    ("devops", "full-stack"),
    ("data scientist", "backend"),
    ("data scientist", "full-stack"),
    ("mobile", "backend"),
    ("mobile", "full-stack"),
]

# Valid experience levels
VALID_EXPERIENCE_LEVELS = ["beginner", "intermediate", "advanced"]

# Valid yes/no responses
VALID_YES_NO = ["yes", "no"]

# Bot status message
BOT_STATUS = "🤝 Finding hackathon teams"

# Embed colors
EMBED_COLORS = {
    "success": 0x00FF00,  # Green
    "error": 0xFF0000,    # Red
    "warning": 0xFFA500,  # Orange
    "info": 0x0099FF,     # Blue
    "match": 0x00FF00,    # Green for matches
} 