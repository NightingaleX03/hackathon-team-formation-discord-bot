"""
Info-related commands for the Hackathon Team Finder Discord Bot
"""

import discord
from utils.data_manager import get_all_users
from config import EMBED_COLORS

async def server_stats(interaction: discord.Interaction):
    """Show server statistics - total users, active profiles, etc."""
    users = get_all_users()
    
    total_users = len(users)
    active_profiles = len([u for u in users if u.get('looking_for_team', True)])
    
    # Count roles
    role_counts = {}
    for user in users:
        for role in user.get('roles', []):
            role_counts[role] = role_counts.get(role, 0) + 1
    
    # Count experience levels
    experience_counts = {}
    for user in users:
        exp = user.get('experience', 'unknown')
        experience_counts[exp] = experience_counts.get(exp, 0) + 1
    
    embed = discord.Embed(
        title="📊 Server Statistics",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="Total Users", value=total_users, inline=True)
    embed.add_field(name="Active Profiles", value=active_profiles, inline=True)
    embed.add_field(name="Looking for Team", value=active_profiles, inline=True)
    
    # Top roles
    if role_counts:
        top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        roles_text = "\n".join([f"• {role.title()}: {count}" for role, count in top_roles])
        embed.add_field(name="Top Roles", value=roles_text, inline=True)
    
    # Experience distribution
    if experience_counts:
        exp_text = "\n".join([f"• {exp.title()}: {count}" for exp, count in experience_counts.items()])
        embed.add_field(name="Experience Levels", value=exp_text, inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 