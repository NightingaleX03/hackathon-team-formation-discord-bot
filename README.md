# 🤝 Hackathon Team Matcher Discord Bot

A Discord bot that helps hackathon participants find compatible team members based on tech stack, experience level, timezone, and preferred roles.

## ✨ Features

- **Team Profile Creation**: Users can create detailed profiles with their tech stack, experience, timezone, and preferred role
- **Smart Matching**: AI-powered matching algorithm that considers:
  - Tech stack compatibility (+1 point per shared technology)
  - Timezone overlap (+2 points for matching timezones)
  - Role complementarity (+3 points for complementary roles like Frontend + Backend)
- **Slash Commands**: Modern Discord slash command interface
- **Data Persistence**: JSON-based storage for user profiles
- **Rich Embeds**: Beautiful Discord embeds for all responses

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `/looking-for-team` | Create or update your team profile |
| `/reset-team-profile` | Remove your team profile |
| `/view-profile` | View your current team profile |
| `/find-matches` | Find compatible team members |

## 🚀 Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this later)
5. Go to "OAuth2" → "URL Generator"
6. Select scopes: `bot` and `applications.commands`
7. Select bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Send Messages in Threads
8. Use the generated URL to invite the bot to your server

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

Set your Discord bot token as an environment variable:

**Windows (PowerShell):**
```powershell
$env:DISCORD_TOKEN="your_bot_token_here"
```

**Windows (Command Prompt):**
```cmd
set DISCORD_TOKEN=your_bot_token_here
```

**Linux/Mac:**
```bash
export DISCORD_TOKEN="your_bot_token_here"
```

### 4. Run the Bot

```bash
python bot.py
```

## 📋 Usage Guide

### Creating a Team Profile

1. Use `/looking-for-team` in any channel
2. Fill out the form with:
   - **Tech Stack**: Comma-separated list (e.g., "Python, React, Node.js")
   - **Experience Level**: Beginner, Intermediate, or Advanced
   - **Timezone**: Your timezone or UTC offset (e.g., "EST", "UTC-5")
   - **Preferred Role**: Frontend, Backend, PM, Designer, etc.
   - **Looking for Team**: Yes or No

### Finding Matches

- Matches are automatically shown when you create a profile
- Use `/find-matches` to search for new matches anytime
- Use `/view-profile` to see your current profile
- Use `/reset-team-profile` to delete your profile

## 🎯 Matching Algorithm

The bot uses a scoring system to find the best matches:

- **+2 points** for matching timezone
- **+3 points** for complementary roles (Frontend + Backend, PM + Developer, etc.)
- **+1 point** per shared technology in tech stack

Matches are ranked by total score and the top 3 are displayed.

## 📁 Project Structure

```
discord-bot/
├── bot.py              # Main bot code
├── data.json           # User profiles (created automatically)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Customization

### Adding New Roles

To add support for new complementary roles, edit the `complementary_roles` list in the `calculate_compatibility` function:

```python
complementary_roles = [
    ("frontend", "backend"),
    ("backend", "frontend"),
    ("pm", "developer"),
    ("designer", "developer"),
    ("full-stack", "frontend"),
    ("full-stack", "backend"),
    ("your_new_role", "complementary_role")  # Add here
]
```

### Changing Scoring

Modify the scoring weights in the `calculate_compatibility` function:

```python
# Timezone compatibility
if profile1["timezone"].lower() == profile2["timezone"].lower():
    score += 2  # Change this value

# Role compatibility
score += 3  # Change this value

# Tech stack compatibility
score += len(shared_tech)  # Change multiplier if needed
```

## 🐛 Troubleshooting

### Bot Not Responding
- Check if the bot token is correct
- Ensure the bot has the required permissions
- Verify the bot is online in your server

### Commands Not Working
- Make sure you've invited the bot with the `applications.commands` scope
- Commands may take up to 1 hour to appear globally
- Try using `/` to see if commands are available

### Permission Errors
- Ensure the bot has "Send Messages" permission
- Check if the bot can read the channel where you're using commands

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy Hacking! 🚀** 