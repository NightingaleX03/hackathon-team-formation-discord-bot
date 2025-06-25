"""
Profile-related commands for the Hackathon Team Finder Discord Bot
"""

import discord
from modals.user_profile_modal import UserProfileModal
from utils.data_manager import load_data
from config import EMBED_COLORS

async def create_profile(ctx: discord.ApplicationContext):
    """Create a new user profile - opens the profile creation form"""
    modal = UserProfileModal()
    await ctx.send_modal(modal)

async def update_profile(ctx: discord.ApplicationContext):
    """Update existing user profile - check if profile exists first"""
    user_id = str(ctx.author.id)
    data = load_data()
    
    if user_id not in data:
        await ctx.respond("❌ You don't have a profile yet. Use `/create-profile` first.", ephemeral=True)
        return
    
    modal = UserProfileModal(is_update=True)
    await ctx.send_modal(modal)

async def view_profile(ctx: discord.ApplicationContext):
    """View user profile - show all the profile details in a nice embed"""
    user_id = str(ctx.author.id)
    data = load_data()
    
    if user_id not in data:
        await ctx.respond("❌ You don't have a profile yet. Use `/create-profile` first.", ephemeral=True)
        return
    
    profile = data[user_id]
    
    # Build the profile display embed - show all the important info
    embed = discord.Embed(
        title=f"👤 {profile['username']}'s Profile",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="Roles", value=", ".join(profile["roles"]).title(), inline=True)
    embed.add_field(name="Experience", value=profile["experience"].title(), inline=True)
    embed.add_field(name="Timezone", value=profile["timezone"], inline=True)
    embed.add_field(name="Tech Skills", value=", ".join(profile["tech_skills"]), inline=False)
    embed.add_field(name="Created", value=profile["created_at"][:10], inline=True)
    embed.add_field(name="Updated", value=profile["updated_at"][:10], inline=True)
    
    await ctx.respond(embed=embed, ephemeral=True) 