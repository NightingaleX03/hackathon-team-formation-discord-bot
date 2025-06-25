"""
Main bot file for the Hackathon Team Finder Discord Bot
"""

import nextcord
from nextcord import app_commands
import os
from dotenv import load_dotenv
from config import BOT_TOKEN, BOT_STATUS

# Import commands from organized modules
from commands.profile_commands import create_profile, update_profile, view_profile
from commands.hackathon_commands import (
    add_hackathon, list_hackathons, remove_hackathon, 
    find_team, pick_hackathon, remove_from_hackathon, hackathon_teams
)
from commands.info_commands import stats

# Load environment variables from .env file (if it exists and is readable)
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Make sure your .env file exists and has the correct format:")
    print("DISCORD_TOKEN=your_actual_bot_token_here")

# Bot setup - this is where the magic happens
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = nextcord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Register slash commands - keeping it clean and simple
@tree.command(name="create-profile", description="Create your developer profile")
async def create_profile_command(interaction: nextcord.Interaction):
    await create_profile(interaction)

@tree.command(name="update-profile", description="Update your existing profile")
async def update_profile_command(interaction: nextcord.Interaction):
    await update_profile(interaction)

@tree.command(name="view-profile", description="View your current profile")
async def view_profile_command(interaction: nextcord.Interaction):
    await view_profile(interaction)

@tree.command(name="add-hackathon", description="Add a new hackathon (Admin only)")
async def add_hackathon_command(interaction: nextcord.Interaction):
    await add_hackathon(interaction)

@tree.command(name="list-hackathons", description="List all available hackathons")
async def list_hackathons_command(interaction: nextcord.Interaction):
    await list_hackathons(interaction)

@tree.command(name="remove-hackathon", description="Remove a hackathon (Admin only)")
@app_commands.describe(hackathon_id="The ID of the hackathon to remove")
async def remove_hackathon_command(interaction: nextcord.Interaction, hackathon_id: int):
    await remove_hackathon(interaction, hackathon_id)

@tree.command(name="find-team", description="Find team members for a hackathon")
async def find_team_command(interaction: nextcord.Interaction):
    await find_team(interaction)

@tree.command(name="pick-hackathon", description="Pick a hackathon and find team members")
@app_commands.describe(
    hackathon_id="The ID of the hackathon",
    looking_for="What type of developer you're looking for"
)
async def pick_hackathon_command(interaction: nextcord.Interaction, hackathon_id: int, looking_for: str):
    await pick_hackathon(interaction, hackathon_id, looking_for)

@tree.command(name="remove-from-hackathon", description="Remove yourself from a hackathon")
@app_commands.describe(hackathon_id="The ID of the hackathon to leave")
async def remove_from_hackathon_command(interaction: nextcord.Interaction, hackathon_id: int):
    await remove_from_hackathon(interaction, hackathon_id)

@tree.command(name="hackathon-teams", description="View all participants in a hackathon")
@app_commands.describe(hackathon_id="The ID of the hackathon")
async def hackathon_teams_command(interaction: nextcord.Interaction, hackathon_id: int):
    await hackathon_teams(interaction, hackathon_id)

@tree.command(name="stats", description="View bot statistics")
async def stats_command(interaction: nextcord.Interaction):
    await stats(interaction)

@bot.event
async def on_ready():
    """Bot ready event - this runs when the bot starts up"""
    print(f"🤖 {bot.user} is ready and online!")
    print(f"📊 Bot is in {len(bot.guilds)} guild(s)")
    
    # Set bot status - shows what the bot is "doing"
    activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=BOT_STATUS)
    await bot.change_presence(activity=activity)
    
    # Sync commands
    await tree.sync()
    print("✅ Commands synced!")

# Run the bot - the main entry point
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in environment variables!")
        print("Please set your Discord bot token in the .env file or environment variables.")
        exit(1)
    
    print("🚀 Starting Discord Bot...")
    bot.run(BOT_TOKEN) 