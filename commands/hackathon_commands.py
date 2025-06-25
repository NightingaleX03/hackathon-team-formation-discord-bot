"""
Hackathon-related commands for the Hackathon Team Finder Discord Bot
"""

import nextcord
from datetime import datetime
from modals.hackathon_modal import HackathonModal
from utils.data_manager import load_data, load_hackathons, save_hackathons
from utils.permissions import is_admin
from utils.matching import find_team_matches, format_matches
from config import EMBED_COLORS, USER_ROLES
import json

async def add_hackathon(interaction: nextcord.Interaction):
    """Add a new hackathon (admin only) - opens the hackathon creation form"""
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ Only administrators can add hackathons.", ephemeral=True)
        return
    
    modal = HackathonModal()
    await interaction.response.send_modal(modal)

async def list_hackathons(interaction: nextcord.Interaction):
    """List all hackathons - show available hackathons with participant counts"""
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("❌ No hackathons found.", ephemeral=True)
        return
    
    if not hackathons:
        await interaction.response.send_message("❌ No hackathons available.", ephemeral=True)
        return
    
    embed = nextcord.Embed(
        title="🏆 Available Hackathons",
        color=EMBED_COLORS["hackathon"]
    )
    
    for hackathon in hackathons:
        team_count = len(hackathon["teams"])
        embed.add_field(
            name=f"#{hackathon['id']} - {hackathon['name']}",
            value=f"📅 {hackathon['date']}\n📍 {hackathon['location']}\n💰 {hackathon['prize']}\n📝 {hackathon['description'][:100]}...",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def remove_hackathon(interaction: nextcord.Interaction, hackathon_id: int):
    """Remove a hackathon (admin only) - delete from the list"""
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ Only administrators can remove hackathons.", ephemeral=True)
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

async def find_team(interaction: nextcord.Interaction):
    """Find team members for a hackathon - show available hackathons first"""
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data:
        await interaction.response.send_message("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    hackathons = load_hackathons()
    
    if not hackathons:
        await interaction.response.send_message("❌ No hackathons available yet.", ephemeral=True)
        return
    
    # Create hackathon selection embed - let user pick which hackathon
    embed = nextcord.Embed(
        title="🏆 Select a Hackathon",
        description="Choose a hackathon to find team members:",
        color=EMBED_COLORS["hackathon"]
    )
    
    for hackathon in hackathons:
        team_count = len(hackathon["teams"])
        embed.add_field(
            name=f"#{hackathon['id']} - {hackathon['name']}",
            value=f"📅 {hackathon['date']}\n📍 {hackathon['location']}\n💰 {hackathon['prize']}\n📝 {hackathon['description'][:100]}...",
            inline=True
        )
    
    embed.add_field(
        name="Next Step",
        value="Use `/pick-hackathon <number>` to select a hackathon and find team members.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def pick_hackathon(interaction: nextcord.Interaction, hackathon_id: int, looking_for: str):
    """Pick a hackathon and find team members - the main team-finding logic"""
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data:
        await interaction.response.send_message("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    hackathons = load_hackathons()
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    
    if not hackathon:
        await interaction.response.send_message("❌ Hackathon not found. Use `/list-hackathons` to see available hackathons.", ephemeral=True)
        return
    
    # Check if user is already in this hackathon - don't add duplicates
    user_in_hackathon = any(team["user_id"] == user_id for team in hackathon["teams"])
    
    if not user_in_hackathon:
        # Add user to hackathon - join the participant list
        hackathon["teams"].append({
            "user_id": user_id,
            "username": interaction.user.display_name,
            "joined_at": datetime.now().isoformat()
        })
        save_hackathons(hackathons)
    
    # Find matches - use the matching algorithm
    matches = find_team_matches(user_id, hackathon_id, looking_for, data)
    
    # Create response - show matches and ping users
    embed = nextcord.Embed(
        title=f"🤝 Team Matches for {hackathon['name']}",
        description=f"Looking for: **{looking_for}**",
        color=EMBED_COLORS["match"]
    )
    
    if matches:
        embed.add_field(
            name="🎯 Best Matches",
            value=format_matches(matches, data),
            inline=False
        )
        
        # Ping the matched users - notify them they were matched
        ping_message = " ".join([f"<@{match['user_id']}>" for match in matches])
        embed.add_field(
            name="📢 Notifications",
            value=f"Pinging matched users: {ping_message}",
            inline=False
        )
    else:
        embed.add_field(
            name="😔 No Matches Found",
            value="No compatible team members found yet. Check back later or try different criteria!",
            inline=False
        )
    
    embed.add_field(
        name="📋 Available Roles",
        value=", ".join(USER_ROLES),
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

async def remove_from_hackathon(interaction: nextcord.Interaction, hackathon_id: int):
    """Remove user from a hackathon - when team is formed"""
    user_id = str(interaction.user.id)
    hackathons = load_hackathons()
    
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        await interaction.response.send_message("❌ Hackathon not found.", ephemeral=True)
        return
    
    # Remove user from hackathon - filter them out
    hackathon["teams"] = [team for team in hackathon["teams"] if team["user_id"] != user_id]
    save_hackathons(hackathons)
    
    embed = nextcord.Embed(
        title="✅ Removed from Hackathon",
        description=f"You have been removed from **{hackathon['name']}**.",
        color=EMBED_COLORS["success"]
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def hackathon_teams(interaction: nextcord.Interaction, hackathon_id: int):
    """View all participants in a hackathon - see who's joined"""
    hackathons = load_hackathons()
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    
    if not hackathon:
        await interaction.response.send_message("❌ Hackathon not found.", ephemeral=True)
        return
    
    data = load_data()
    
    embed = nextcord.Embed(
        title=f"👥 Participants in {hackathon['name']}",
        description=f"Total participants: {len(hackathon['teams'])}",
        color=EMBED_COLORS["hackathon"]
    )
    
    if hackathon["teams"]:
        for team in hackathon["teams"]:
            user_id = team["user_id"]
            if user_id in data:
                profile = data[user_id]
                roles = ", ".join(profile["roles"]).title()
                embed.add_field(
                    name=f"👤 {team['username']}",
                    value=f"Roles: {roles}\nExperience: {profile['experience'].title()}",
                    inline=True
                )
            else:
                embed.add_field(
                    name=f"👤 {team['username']}",
                    value="No profile created",
                    inline=True
                )
    else:
        embed.add_field(name="No Participants", value="No one has joined this hackathon yet.", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 