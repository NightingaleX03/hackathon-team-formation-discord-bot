"""
Hackathon-related commands for the Hackathon Team Finder Discord Bot
"""

import discord
from datetime import datetime
from modals.hackathon_modal import HackathonModal
from utils.data_manager import load_data, load_hackathons, save_hackathons
from utils.permissions import is_admin
from utils.matching import find_team_matches, format_matches
from config import EMBED_COLORS, USER_ROLES

async def add_hackathon(ctx: discord.ApplicationContext):
    """Add a new hackathon (admin only) - opens the hackathon creation form"""
    if not is_admin(ctx.author):
        await ctx.respond("❌ Only administrators can add hackathons.", ephemeral=True)
        return
    
    modal = HackathonModal()
    await ctx.send_modal(modal)

async def list_hackathons(ctx: discord.ApplicationContext):
    """List all hackathons - show available hackathons with participant counts"""
    hackathons = load_hackathons()
    
    if not hackathons:
        await ctx.respond("❌ No hackathons available yet.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🏆 Available Hackathons",
        color=EMBED_COLORS["hackathon"]
    )
    
    for hackathon in hackathons:
        team_count = len(hackathon["teams"])
        embed.add_field(
            name=f"{hackathon['id']}. {hackathon['name']}",
            value=f"📅 {hackathon['date']}\n📝 {hackathon['description']}\n👥 {team_count} participants",
            inline=False
        )
    
    await ctx.respond(embed=embed, ephemeral=True)

async def remove_hackathon(ctx: discord.ApplicationContext, hackathon_id: int):
    """Remove a hackathon (admin only) - delete from the list"""
    if not is_admin(ctx.author):
        await ctx.respond("❌ Only administrators can remove hackathons.", ephemeral=True)
        return
    
    hackathons = load_hackathons()
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    
    if not hackathon:
        await ctx.respond("❌ Hackathon not found.", ephemeral=True)
        return
    
    # Remove the hackathon - filter it out
    hackathons = [h for h in hackathons if h["id"] != hackathon_id]
    save_hackathons(hackathons)
    
    embed = discord.Embed(
        title="✅ Hackathon Removed",
        description=f"**{hackathon['name']}** has been removed.",
        color=EMBED_COLORS["success"]
    )
    
    await ctx.respond(embed=embed, ephemeral=True)

async def find_team(ctx: discord.ApplicationContext):
    """Find team members for a hackathon - show available hackathons first"""
    user_id = str(ctx.author.id)
    data = load_data()
    
    if user_id not in data:
        await ctx.respond("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    hackathons = load_hackathons()
    
    if not hackathons:
        await ctx.respond("❌ No hackathons available yet.", ephemeral=True)
        return
    
    # Create hackathon selection embed - let user pick which hackathon
    embed = discord.Embed(
        title="🏆 Select a Hackathon",
        description="Choose a hackathon to find team members:",
        color=EMBED_COLORS["hackathon"]
    )
    
    for hackathon in hackathons:
        team_count = len(hackathon["teams"])
        embed.add_field(
            name=f"{hackathon['id']}. {hackathon['name']}",
            value=f"📅 {hackathon['date']}\n👥 {team_count} participants",
            inline=True
        )
    
    embed.add_field(
        name="Next Step",
        value="Use `/pick-hackathon <number>` to select a hackathon and find team members.",
        inline=False
    )
    
    await ctx.respond(embed=embed, ephemeral=True)

async def pick_hackathon(ctx: discord.ApplicationContext, hackathon_id: int, looking_for: str):
    """Pick a hackathon and find team members - the main team-finding logic"""
    user_id = str(ctx.author.id)
    data = load_data()
    
    if user_id not in data:
        await ctx.respond("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    hackathons = load_hackathons()
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    
    if not hackathon:
        await ctx.respond("❌ Hackathon not found. Use `/list-hackathons` to see available hackathons.", ephemeral=True)
        return
    
    # Check if user is already in this hackathon - don't add duplicates
    user_in_hackathon = any(team["user_id"] == user_id for team in hackathon["teams"])
    
    if not user_in_hackathon:
        # Add user to hackathon - join the participant list
        hackathon["teams"].append({
            "user_id": user_id,
            "username": ctx.author.display_name,
            "joined_at": datetime.now().isoformat()
        })
        save_hackathons(hackathons)
    
    # Find matches - use the matching algorithm
    matches = find_team_matches(user_id, hackathon_id, looking_for, data)
    
    # Create response - show matches and ping users
    embed = discord.Embed(
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
    
    await ctx.respond(embed=embed)

async def remove_from_hackathon(ctx: discord.ApplicationContext, hackathon_id: int):
    """Remove user from a hackathon - when team is formed"""
    user_id = str(ctx.author.id)
    hackathons = load_hackathons()
    
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        await ctx.respond("❌ Hackathon not found.", ephemeral=True)
        return
    
    # Remove user from hackathon - filter them out
    hackathon["teams"] = [team for team in hackathon["teams"] if team["user_id"] != user_id]
    save_hackathons(hackathons)
    
    embed = discord.Embed(
        title="✅ Removed from Hackathon",
        description=f"You have been removed from **{hackathon['name']}**.",
        color=EMBED_COLORS["success"]
    )
    
    await ctx.respond(embed=embed, ephemeral=True)

async def hackathon_teams(ctx: discord.ApplicationContext, hackathon_id: int):
    """View all participants in a hackathon - see who's joined"""
    hackathons = load_hackathons()
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    
    if not hackathon:
        await ctx.respond("❌ Hackathon not found.", ephemeral=True)
        return
    
    data = load_data()
    
    embed = discord.Embed(
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
    
    await ctx.respond(embed=embed, ephemeral=True) 