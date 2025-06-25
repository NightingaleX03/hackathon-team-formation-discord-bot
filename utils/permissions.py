"""
Permission utilities for the Hackathon Team Finder Discord Bot
"""

import discord

def is_admin(member: discord.Member) -> bool:
    """Check if member is admin - simple permission check"""
    return member.guild_permissions.administrator 