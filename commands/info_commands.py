"""
Information and utility commands for the Hackathon Team Finder Discord Bot
"""

import discord
from utils.data_manager import load_data, load_hackathons
from config import EMBED_COLORS

async def stats(ctx: discord.ApplicationContext):
    """View bot statistics - show overall usage numbers"""
    data = load_data()
    hackathons = load_hackathons()
    
    # Calculate basic stats - total users, hackathons, participants
    total_users = len(data)
    total_hackathons = len(hackathons)
    total_participants = sum(len(h["teams"]) for h in hackathons)
    
    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="Total Users", value=str(total_users), inline=True)
    embed.add_field(name="Total Hackathons", value=str(total_hackathons), inline=True)
    embed.add_field(name="Total Participants", value=str(total_participants), inline=True)
    
    # Show most popular hackathon if any exist
    if hackathons:
        most_popular = max(hackathons, key=lambda h: len(h["teams"]))
        embed.add_field(
            name="Most Popular Hackathon",
            value=f"{most_popular['name']} ({len(most_popular['teams'])} participants)",
            inline=False
        )
    
    await ctx.respond(embed=embed, ephemeral=True) 