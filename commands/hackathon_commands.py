"""
Hackathon-related commands for the Hackathon Team Finder Discord Bot
"""

import discord
from datetime import datetime
from modals.hackathon_modal import HackathonModal
from utils.data_manager import (
    get_user_by_id, get_all_users, get_all_hackathons, 
    save_single_hackathon, delete_hackathon_by_id,
    join_hackathon, leave_hackathon
)
from utils.permissions import is_admin
from utils.matching import find_compatible_teammates
from config import EMBED_COLORS, USER_ROLES

async def add_hackathon(interaction: discord.Interaction):
    """Add a new hackathon - admin only, opens the hackathon creation form"""
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ You need admin permissions to add hackathons.", ephemeral=True)
        return
    
    modal = HackathonModal()
    await interaction.response.send_modal(modal)

async def list_hackathons(interaction: discord.Interaction):
    """List all available hackathons - show them in a nice embed"""
    hackathons = get_all_hackathons()
    
    if not hackathons:
        await interaction.response.send_message("❌ No hackathons available.", ephemeral=True)
        return
    
    # Build the hackathon list embed
    embed = discord.Embed(
        title="🏆 Available Hackathons",
        color=EMBED_COLORS["success"]
    )
    
    for hackathon in hackathons:
        teams_count = len(hackathon.get('teams', []))
        embed.add_field(
            name=f"#{hackathon['id']} - {hackathon['name']}",
            value=f"📅 {hackathon.get('date', 'TBD')}\n👥 {teams_count} participants\n📝 {hackathon.get('description', 'No description')[:100]}...",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def remove_hackathon(interaction: discord.Interaction, hackathon_id: int):
    """Remove a hackathon - admin only"""
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ You need admin permissions to remove hackathons.", ephemeral=True)
        return
    
    success = delete_hackathon_by_id(hackathon_id)
    
    if success:
        await interaction.response.send_message(f"✅ Hackathon #{hackathon_id} has been removed.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Hackathon #{hackathon_id} not found.", ephemeral=True)

async def find_team(interaction: discord.Interaction):
    """Find team members for a hackathon - show compatible users"""
    user_id = str(interaction.user.id)
    user_profile = get_user_by_id(user_id)
    
    if not user_profile:
        await interaction.response.send_message("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    all_users = get_all_users()
    # Convert to dict format for compatibility
    users_dict = {user['user_id']: user for user in all_users}
    
    compatible_users = find_compatible_teammates(user_profile, users_dict)
    
    if not compatible_users:
        await interaction.response.send_message("❌ No compatible team members found.", ephemeral=True)
        return
    
    # Build the team finder embed
    embed = discord.Embed(
        title="🤝 Compatible Team Members",
        description="Here are users who might be good teammates:",
        color=EMBED_COLORS["success"]
    )
    
    for i, (user_id, compatibility_score) in enumerate(compatible_users[:5], 1):
        user_data = users_dict[user_id]
        # Add error handling for missing keys
        roles = user_data.get('roles', [])
        tech_skills = user_data.get('tech_skills', [])
        
        embed.add_field(
            name=f"{i}. {user_data.get('username', 'Unknown User')} (Score: {compatibility_score:.1f})",
            value=f"Roles: {', '.join(roles).title() if roles else 'Not specified'}\nSkills: {', '.join(tech_skills[:3]) if tech_skills else 'Not specified'}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def pick_hackathon(interaction: discord.Interaction, hackathon_id: int, looking_for: str):
    """Pick a hackathon and find team members for it"""
    user_id = str(interaction.user.id)
    user_profile = get_user_by_id(user_id)
    
    if not user_profile:
        await interaction.response.send_message("❌ You need to create a profile first. Use `/create-profile`.", ephemeral=True)
        return
    
    # Get hackathons from database
    hackathons = get_all_hackathons()
    
    # Find the specific hackathon
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        await interaction.response.send_message(f"❌ Hackathon #{hackathon_id} not found.", ephemeral=True)
        return
    
    # Add user to hackathon
    success = join_hackathon(hackathon_id, user_id, user_profile['username'])
    
    if not success:
        await interaction.response.send_message(f"❌ You're already participating in {hackathon['name']}.", ephemeral=True)
        return
    
    # Find compatible team members
    all_users = get_all_users()
    users_dict = {user['user_id']: user for user in all_users}
    compatible_users = find_compatible_teammates(user_profile, users_dict)
    
    # Build the response embed
    embed = discord.Embed(
        title=f"🎯 {hackathon['name']} - Team Search",
        description=f"You're looking for: **{looking_for}**",
        color=EMBED_COLORS["success"]
    )
    
    teams_count = len(hackathon.get('teams', []))
    embed.add_field(name="Hackathon Details", value=f"📅 {hackathon.get('date', 'TBD')}\n👥 {teams_count} participants", inline=False)
    
    if compatible_users:
        embed.add_field(name="🤝 Compatible Team Members", value="", inline=False)
        for i, (user_id, compatibility_score) in enumerate(compatible_users[:3], 1):
            user_data = users_dict[user_id]
            # Add error handling for missing keys
            roles = user_data.get('roles', [])
            tech_skills = user_data.get('tech_skills', [])
            
            embed.add_field(
                name=f"{i}. {user_data.get('username', 'Unknown User')} (Score: {compatibility_score:.1f})",
                value=f"Roles: {', '.join(roles).title() if roles else 'Not specified'}\nSkills: {', '.join(tech_skills[:3]) if tech_skills else 'Not specified'}",
                inline=True
            )
    else:
        embed.add_field(name="🤝 Team Members", value="No compatible team members found yet.", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def remove_from_hackathon(interaction: discord.Interaction, hackathon_id: int):
    """Remove user from a hackathon"""
    user_id = str(interaction.user.id)
    
    success = leave_hackathon(hackathon_id, user_id)
    
    if success:
        await interaction.response.send_message(f"✅ You've been removed from hackathon #{hackathon_id}.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ You're not participating in hackathon #{hackathon_id}.", ephemeral=True) 