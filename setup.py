#!/usr/bin/env python3
"""
Setup script for Hackathon Team Matcher Discord Bot
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_token():
    """Check if Discord token is set"""
    token = os.getenv("DISCORD_TOKEN")
    if token:
        print("✅ Discord token found in environment")
        return True
    else:
        print("❌ Discord token not found")
        print("Please set your DISCORD_TOKEN environment variable")
        return False

def create_env_file():
    """Create .env file template"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Discord Bot Token\n")
            f.write("# Get your token from: https://discord.com/developers/applications\n")
            f.write("DISCORD_TOKEN=your_bot_token_here\n")
        print("📝 Created .env file template")
        print("Please edit .env and add your Discord bot token")

def main():
    """Main setup function"""
    print("🚀 Hackathon Team Matcher Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create .env file
    create_env_file()
    
    # Check token
    if not check_token():
        print("\n📋 Next steps:")
        print("1. Get your Discord bot token from: https://discord.com/developers/applications")
        print("2. Set the DISCORD_TOKEN environment variable or edit .env file")
        print("3. Run: python bot.py")
        return
    
    print("\n✅ Setup complete!")
    print("Run 'python bot.py' to start the bot")

if __name__ == "__main__":
    main() 