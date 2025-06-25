"""
Information and utility commands for the Hackathon Team Finder Discord Bot
"""

import nextcord
from utils.data_manager import load_data
from config import EMBED_COLORS

async def stats(interaction: nextcord.Interaction):
    """Show bot statistics - user count, hackathon count, etc."""
    data = load_data()
    
    # Calculate statistics
    total_users = len(data)
    total_profiles = sum(1 for user in data.values() if user.get("username"))
    
    # Count roles and skills
    all_roles = []
    all_skills = []
    
    for user in data.values():
        if "roles" in user:
            all_roles.extend(user["roles"])
        if "tech_skills" in user:
            all_skills.extend(user["tech_skills"])
    
    # Get most common roles and skills
    role_counts = {}
    for role in all_roles:
        role_counts[role] = role_counts.get(role, 0) + 1
    
    skill_counts = {}
    for skill in all_skills:
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Build the stats embed
    embed = nextcord.Embed(
        title="📊 Bot Statistics",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="👥 Total Users", value=str(total_users), inline=True)
    embed.add_field(name="📝 Profiles Created", value=str(total_profiles), inline=True)
    embed.add_field(name="🏆 Active Hackathons", value="3", inline=True)
    
    if top_roles:
        roles_text = "\n".join([f"• {role.title()}: {count}" for role, count in top_roles])
        embed.add_field(name="🎭 Top Roles", value=roles_text, inline=True)
    
    if top_skills:
        skills_text = "\n".join([f"• {skill.title()}: {count}" for skill, count in top_skills])
        embed.add_field(name="💻 Top Skills", value=skills_text, inline=True)
    
    embed.set_footer(text="Keep building amazing teams! 🚀")
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 