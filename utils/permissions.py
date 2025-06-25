"""
Permission utilities for the Hackathon Team Finder Discord Bot
"""

import nextcord
from config import ADMIN_USER_IDS

def is_admin(user: nextcord.Member) -> bool:
    """Check if user has admin permissions"""
    # Check if user is in admin list
    if str(user.id) in ADMIN_USER_IDS:
        return True
    
    # Check if user has admin role
    if user.guild_permissions.administrator:
        return True
    
    # Check for specific admin role
    admin_role = nextcord.utils.get(user.guild.roles, name="Hackathon Admin")
    if admin_role and admin_role in user.roles:
        return True
    
    return False 