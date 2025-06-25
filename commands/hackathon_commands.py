"""
Hackathon-related commands for the Hackathon Team Finder Discord Bot
"""

import disnake
from datetime import datetime
from modals.hackathon_modal import HackathonModal
from utils.data_manager import load_data, load_hackathons, save_hackathons
from utils.permissions import is_admin
from utils.matching import find_compatible_teammates
from config import EMBED_COLORS, USER_ROLES
import json

async def add_hackathon(interaction: disnake.ApplicationCommandInteraction):
    """Add a new hackathon - admin only, opens the hackathon creation form"""
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ You need admin permissions to add hackathons.", ephemeral=True)
        return
    
    modal = HackathonModal()
    await interaction.response.send_modal(modal)

async def list_hackathons(interaction: disnake.ApplicationCommandInteraction):
    """List all available hackathons - show them in a nice embed"""
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("❌ No hackathons found.", ephemeral=True)
        return
    
    if not hackathons:
        await interaction.response.send_message("❌ No hackathons available.", ephemeral=True)
        return
    
    # Build the hackathon list embed
    embed = disnake.Embed(
        title="🏆 Available Hackathons",
        color=EMBED_COLORS["success"]
    )
    
    for hackathon in hackathons:
        embed.add_field(
            name=f"#{hackathon['id']} - {hackathon['name']}",
            value=f"📅 {hackathon['date']}\n📍 {hackathon['location']}\n💰 {hackathon['prize']}\n📝 {hackathon['description'][:100]}...",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def remove_hackathon(interaction: disnake.ApplicationCommandInteraction, hackathon_id: int):
    """Remove a hackathon - admin only"""
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ You need admin permissions to remove hackathons.", ephemeral=True)
        return
    
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("❌ No hackathons found.", ephemeral=True)
        return
    
    # Find and remove the hackathon
    hackathons = [h for h in hackathons if h["id"] != hackathon_id]
    
    with open("example_hackathons.json", "w") as f:
        json.dump(hackathons, f, indent=2)
    
    await interaction.response.send_message(f"✅ Hackathon #{hackathon_id} has been removed.", ephemeral=True)

async def find_team(interaction: disnake.ApplicationCommandInteraction):
    """Find team members for a hackathon - show compatible users"""
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data:
        await interaction.response.send_message("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    user_profile = data[user_id]
    compatible_users = find_compatible_teammates(user_profile, data)
    
    if not compatible_users:
        await interaction.response.send_message("❌ No compatible team members found.", ephemeral=True)
        return
    
    # Build the team finder embed
    embed = disnake.Embed(
        title="🤝 Compatible Team Members",
        description="Here are users who might be good teammates:",
        color=EMBED_COLORS["success"]
    )
    
    for i, (user_id, compatibility_score) in enumerate(compatible_users[:5], 1):
        user_data = data[user_id]
        embed.add_field(
            name=f"{i}. {user_data['username']} (Score: {compatibility_score:.1f})",
            value=f"Roles: {', '.join(user_data['roles']).title()}\nSkills: {', '.join(user_data['tech_skills'][:3])}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def pick_hackathon(interaction: disnake.ApplicationCommandInteraction, hackathon_id: int, looking_for: str):
    """Pick a hackathon and find team members for it"""
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data:
        await interaction.response.send_message("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    # Load hackathons
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("❌ No hackathons found.", ephemeral=True)
        return
    
    # Find the specific hackathon
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        await interaction.response.send_message(f"❌ Hackathon #{hackathon_id} not found.", ephemeral=True)
        return
    
    # Add user to hackathon participants
    if "participants" not in hackathon:
        hackathon["participants"] = []
    
    if user_id not in hackathon["participants"]:
        hackathon["participants"].append(user_id)
    
    # Save updated hackathon data
    with open("example_hackathons.json", "w") as f:
        json.dump(hackathons, f, indent=2)
    
    # Find compatible team members
    user_profile = data[user_id]
    compatible_users = find_compatible_teammates(user_profile, data)
    
    # Build the response embed
    embed = disnake.Embed(
        title=f"🎯 {hackathon['name']} - Team Search",
        description=f"You're looking for: **{looking_for}**",
        color=EMBED_COLORS["success"]
    )
    
    embed.add_field(name="Hackathon Details", value=f"📅 {hackathon['date']}\n📍 {hackathon['location']}\n💰 {hackathon['prize']}", inline=False)
    
    if compatible_users:
        embed.add_field(name="🤝 Compatible Team Members", value="", inline=False)
        for i, (user_id, compatibility_score) in enumerate(compatible_users[:3], 1):
            user_data = data[user_id]
            embed.add_field(
                name=f"{i}. {user_data['username']} (Score: {compatibility_score:.1f})",
                value=f"Roles: {', '.join(user_data['roles']).title()}\nSkills: {', '.join(user_data['tech_skills'][:3])}",
                inline=True
            )
    else:
        embed.add_field(name="🤝 Team Members", value="No compatible team members found yet.", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def remove_from_hackathon(interaction: disnake.ApplicationCommandInteraction, hackathon_id: int):
    """Remove user from a hackathon"""
    user_id = str(interaction.user.id)
    
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("❌ No hackathons found.", ephemeral=True)
        return
    
    # Find the hackathon
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        await interaction.response.send_message(f"❌ Hackathon #{hackathon_id} not found.", ephemeral=True)
        return
    
    # Remove user from participants
    if "participants" in hackathon and user_id in hackathon["participants"]:
        hackathon["participants"].remove(user_id)
        
        with open("example_hackathons.json", "w") as f:
            json.dump(hackathons, f, indent=2)
        
        await interaction.response.send_message(f"✅ You've been removed from {hackathon['name']}.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ You're not participating in {hackathon['name']}.", ephemeral=True)

async def hackathon_teams(interaction: disnake.ApplicationCommandInteraction, hackathon_id: int):
    """View all participants in a hackathon"""
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("❌ No hackathons found.", ephemeral=True)
        return
    
    # Find the hackathon
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        await interaction.response.send_message(f"❌ Hackathon #{hackathon_id} not found.", ephemeral=True)
        return
    
    # Load user data
    data = load_data()
    
    # Build the teams embed
    embed = disnake.Embed(
        title=f"👥 {hackathon['name']} - Participants",
        color=EMBED_COLORS["info"]
    )
    
    if "participants" in hackathon and hackathon["participants"]:
        for user_id in hackathon["participants"]:
            if user_id in data:
                user_data = data[user_id]
                embed.add_field(
                    name=user_data["username"],
                    value=f"Roles: {', '.join(user_data['roles']).title()}\nSkills: {', '.join(user_data['tech_skills'][:3])}",
                    inline=True
                )
    else:
        embed.add_field(name="No Participants", value="No one has joined this hackathon yet.", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 