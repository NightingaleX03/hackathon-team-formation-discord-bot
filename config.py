"""
Configuration file for the Hackathon Team Matcher Discord Bot
"""

import os

# Bot Configuration - basic setup
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
DATA_FILE = "data.json"
HACKATHONS_FILE = "hackathons.json"

# Matching Algorithm Weights - adjust these to change scoring
TIMEZONE_MATCH_SCORE = 2
ROLE_COMPLEMENT_SCORE = 3
TECH_STACK_MATCH_SCORE = 1

# Maximum number of matches to return - keep it reasonable
MAX_MATCHES = 3

# Complementary role pairs for scoring - these work well together
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

# Valid experience levels - keep it simple
VALID_EXPERIENCE_LEVELS = ["beginner", "intermediate", "advanced"]

# Valid yes/no responses - for future use
VALID_YES_NO = ["yes", "no"]

# User roles for profiles - the main developer types
USER_ROLES = [
    "backend",
    "frontend", 
    "AI/ML",
    "VR",
    "designer",
    "web developer",
    "game developer"
]

# Tech skills for profiles - comprehensive list of popular skills
TECH_SKILLS = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
    "React", "Vue.js", "Angular", "Node.js", "Express", "Django", "Flask",
    "MongoDB", "PostgreSQL", "MySQL", "Redis", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD",
    "TensorFlow", "PyTorch", "Scikit-learn", "OpenAI API", "Hugging Face",
    "Unity", "Unreal Engine", "Blender", "Figma", "Adobe Creative Suite",
    "HTML", "CSS", "SASS", "Bootstrap", "Tailwind CSS", "Webpack", "Vite",
    "REST API", "GraphQL", "WebSocket", "Socket.io", "Firebase",
    "Machine Learning", "Deep Learning", "Computer Vision", "NLP",
    "Blockchain", "Smart Contracts", "Solidity", "Web3", "Ethereum",
    "Mobile Development", "React Native", "Flutter", "Swift", "Kotlin",
    "DevOps", "Linux", "Shell Scripting", "Ansible", "Terraform"
]

# Bot status message - what shows under the bot's name
BOT_STATUS = "🤝 Finding hackathon teams"

# Embed colors - for nice-looking Discord messages
EMBED_COLORS = {
    "success": 0x00FF00,  # Green
    "error": 0xFF0000,    # Red
    "warning": 0xFFA500,  # Orange
    "info": 0x0099FF,     # Blue
    "match": 0x00FF00,    # Green for matches
    "hackathon": 0x9932CC, # Purple for hackathons
} 