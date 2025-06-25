"""
Configuration file for the Hackathon Team Finder Discord Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_STATUS = "for hackathon teams! 🚀"

# Admin user IDs (add your Discord user ID here)
ADMIN_USER_IDS = [
    # Add your Discord user ID here for admin access
    # "123456789012345678"  # Example: Replace with your actual Discord user ID
]

# Embed colors for different types of messages
EMBED_COLORS = {
    "success": 0x00ff00,  # Green
    "error": 0xff0000,    # Red
    "info": 0x0099ff,     # Blue
    "warning": 0xffaa00,  # Orange
    "hackathon": 0x9b59b6  # Purple
}

# User roles for validation
USER_ROLES = [
    "frontend", "backend", "fullstack", "mobile", "ai/ml", 
    "devops", "designer", "product", "data", "blockchain"
]

# Tech skills for validation
TECH_SKILLS = [
    "python", "javascript", "typescript", "react", "vue", "angular",
    "node.js", "express", "django", "flask", "fastapi", "spring",
    "java", "c#", "c++", "go", "rust", "php", "ruby", "swift",
    "kotlin", "dart", "flutter", "react native", "ionic",
    "html", "css", "sass", "tailwind", "bootstrap", "material-ui",
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "docker", "kubernetes", "aws", "azure", "gcp", "firebase",
    "git", "github", "gitlab", "jenkins", "circleci", "travis",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "blockchain", "ethereum", "solidity", "web3", "ipfs"
]

# Experience levels
EXPERIENCE_LEVELS = [
    "beginner", "intermediate", "advanced", "expert"
]

# Timezones
TIMEZONES = [
    "UTC", "EST", "CST", "MST", "PST", "GMT", "CET", "JST", "AEST"
] 