"""
User Profile Modal for creating and updating user profiles
"""

import discord
from discord.ui import Modal, TextInput, Select
from utils.data_manager import load_data, save_data
from config import USER_ROLES, TECH_SKILLS, EXPERIENCE_LEVELS, TIMEZONES
from datetime import datetime

class UserProfileModal(Modal):
    def __init__(self, is_update=False):
        super().__init__(title="Create Your Developer Profile" if not is_update else "Update Your Profile")
        self.is_update = is_update
        
        # Username field
        self.username = TextInput(
            label="Username",
            placeholder="Enter your preferred username",
            required=True,
            max_length=32
        )
        
        # Roles selection
        self.roles = TextInput(
            label="Roles (comma-separated)",
            placeholder="e.g., frontend, backend, fullstack, designer, devops",
            required=True,
            max_length=200
        )
        
        # Experience level
        self.experience = TextInput(
            label="Experience Level",
            placeholder="e.g., beginner, intermediate, advanced, expert",
            required=True,
            max_length=20
        )
        
        # Timezone
        self.timezone = TextInput(
            label="Timezone",
            placeholder="e.g., EST, PST, UTC, GMT",
            required=True,
            max_length=10
        )
        
        # Tech skills
        self.tech_skills = TextInput(
            label="Tech Skills (comma-separated)",
            placeholder="e.g., python, javascript, react, node.js, docker",
            required=True,
            max_length=500
        )
        
        # Add all fields to the modal
        self.add_item(self.username)
        self.add_item(self.roles)
        self.add_item(self.experience)
        self.add_item(self.timezone)
        self.add_item(self.tech_skills)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle the form submission"""
        user_id = str(interaction.user.id)
        data = load_data()
        
        # Parse the input data
        username = self.username.value.strip()
        roles = [role.strip().lower() for role in self.roles.value.split(",") if role.strip()]
        experience = self.experience.value.strip().lower()
        timezone = self.timezone.value.strip().upper()
        tech_skills = [skill.strip().lower() for skill in self.tech_skills.value.split(",") if skill.strip()]
        
        # Validate input
        if not username or not roles or not experience or not timezone or not tech_skills:
            await interaction.response.send_message("❌ All fields are required!", ephemeral=True)
            return
        
        # Create or update the profile
        profile_data = {
            "username": username,
            "roles": roles,
            "experience": experience,
            "timezone": timezone,
            "tech_skills": tech_skills,
            "updated_at": datetime.now().isoformat()
        }
        
        if not self.is_update:
            profile_data["created_at"] = datetime.now().isoformat()
        
        data[user_id] = profile_data
        save_data(data)
        
        # Create success embed
        embed = discord.Embed(
            title="✅ Profile Saved Successfully!",
            color=0x00ff00
        )
        
        embed.add_field(name="Username", value=username, inline=True)
        embed.add_field(name="Roles", value=", ".join(roles).title(), inline=True)
        embed.add_field(name="Experience", value=experience.title(), inline=True)
        embed.add_field(name="Timezone", value=timezone, inline=True)
        embed.add_field(name="Tech Skills", value=", ".join(tech_skills), inline=False)
        
        action = "updated" if self.is_update else "created"
        embed.set_footer(text=f"Your profile has been {action}! Use /find-team to start matching.")
        
        await interaction.response.send_message(embed=embed, ephemeral=True) 