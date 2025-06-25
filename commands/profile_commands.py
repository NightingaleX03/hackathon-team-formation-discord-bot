"""
Profile-related commands for the Hackathon Team Finder Discord Bot
"""

import nextcord
from modals.user_profile_modal import UserProfileModal
from utils.data_manager import load_data
from config import EMBED_COLORS

async def create_profile(interaction: nextcord.Interaction):
    """Create a new user profile - opens the profile creation form"""
    modal = UserProfileModal()
    await interaction.response.send_modal(modal)

async def update_profile(interaction: nextcord.Interaction):
    """Update existing user profile - check if profile exists first"""
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data:
        await interaction.response.send_message("❌ You don't have a profile yet. Use `/create-profile` first.", ephemeral=True)
        return
    
    modal = UserProfileModal(is_update=True)
    await interaction.response.send_modal(modal)

async def view_profile(interaction: nextcord.Interaction):
    """View user profile - show all the profile details in a nice embed"""
    user_id = str(interaction.user.id)
    data = load_data()
    
    if user_id not in data:
        await interaction.response.send_message("❌ You don't have a profile yet. Use `/create-profile` first.", ephemeral=True)
        return
    
    profile = data[user_id]
    
    # Build the profile display embed - show all the important info
    embed = nextcord.Embed(
        title=f"👤 {profile['username']}'s Profile",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="Roles", value=", ".join(profile["roles"]).title(), inline=True)
    embed.add_field(name="Experience", value=profile["experience"].title(), inline=True)
    embed.add_field(name="Timezone", value=profile["timezone"], inline=True)
    embed.add_field(name="Tech Skills", value=", ".join(profile["tech_skills"]), inline=False)
    embed.add_field(name="Created", value=profile["created_at"][:10], inline=True)
    embed.add_field(name="Updated", value=profile["updated_at"][:10], inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 