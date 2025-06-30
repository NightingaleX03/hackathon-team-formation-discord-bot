"""
Profile-related commands for the Hackathon Team Finder Discord Bot
"""

import discord
from modals.user_profile_modal import UserProfileModal
from utils.data_manager import get_user_by_id, get_all_users
from config import EMBED_COLORS

async def create_profile(interaction: discord.Interaction):
    """Create a new user profile - opens the profile creation form"""
    modal = UserProfileModal(user=interaction.user)
    await interaction.response.send_modal(modal)

async def update_profile(interaction: discord.Interaction):
    """Update existing user profile - check if profile exists first"""
    user_id = str(interaction.user.id)
    profile = get_user_by_id(user_id)
    
    if not profile:
        await interaction.response.send_message("❌ You don't have a profile yet. Use `/create-profile` first.", ephemeral=True)
        return
    
    modal = UserProfileModal(is_update=True, user=interaction.user)
    await interaction.response.send_modal(modal)

async def view_profile(interaction: discord.Interaction):
    """View user profile - show all the profile details in a nice embed"""
    user_id = str(interaction.user.id)
    profile = get_user_by_id(user_id)
    
    if not profile:
        await interaction.response.send_message("❌ You don't have a profile yet. Use `/create-profile` first.", ephemeral=True)
        return
    
    # Build the profile display embed - show all the important info
    embed = discord.Embed(
        title=f"👤 {profile['username']}'s Profile",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="Roles", value=", ".join(profile["roles"]).title(), inline=True)
    embed.add_field(name="Experience", value=profile["experience"].title(), inline=True)
    embed.add_field(name="Timezone", value=profile["timezone"], inline=True)
    embed.add_field(name="Tech Skills", value=", ".join(profile["tech_skills"]), inline=False)
    embed.add_field(name="Created", value=profile["created_at"][:10] if profile["created_at"] else "Unknown", inline=True)
    embed.add_field(name="Updated", value=profile["updated_at"][:10] if profile["updated_at"] else "Unknown", inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 