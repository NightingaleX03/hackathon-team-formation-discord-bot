"""
User profile modal for the Hackathon Team Finder Discord Bot
"""

import discord
from datetime import datetime
from typing import Dict, Any
from config import USER_ROLES, TECH_SKILLS, VALID_EXPERIENCE_LEVELS, EMBED_COLORS
from utils.data_manager import load_data, save_data

class UserProfileModal(discord.ui.Modal):
    """Modal for creating/updating user profile - the form users fill out"""
    
    def __init__(self, is_update: bool = False):
        title = "Update Profile" if is_update else "Create Profile"
        super().__init__(title=title)
        
        self.roles = discord.ui.TextInput(
            label="Your Roles (comma-separated)",
            placeholder="e.g., backend, frontend, AI/ML (pick from: " + ", ".join(USER_ROLES) + ")",
            style=discord.TextStyle.paragraph,
            max_length=200,
            required=True
        )
        
        self.tech_skills = discord.ui.TextInput(
            label="Tech Skills (comma-separated)",
            placeholder="e.g., Python, React, AWS (pick from available skills)",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=True
        )
        
        self.experience = discord.ui.TextInput(
            label="Experience Level",
            placeholder="Beginner, Intermediate, or Advanced",
            max_length=20,
            required=True
        )
        
        self.timezone = discord.ui.TextInput(
            label="Timezone/UTC Offset",
            placeholder="e.g., EST, UTC-5, or PST",
            max_length=20,
            required=True
        )
        
        self.add_item(self.roles)
        self.add_item(self.tech_skills)
        self.add_item(self.experience)
        self.add_item(self.timezone)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission - validate and save the profile"""
        user_id = str(interaction.user.id)
        
        # Validate experience level - make sure it's one of the valid options
        experience = self.experience.value.strip().lower()
        if experience not in VALID_EXPERIENCE_LEVELS:
            await interaction.response.send_message(
                f"❌ Invalid experience level. Please use: {', '.join(VALID_EXPERIENCE_LEVELS).title()}",
                ephemeral=True
            )
            return
        
        # Validate roles - check against the predefined list
        roles = [role.strip().lower() for role in self.roles.value.split(',')]
        valid_roles = [role.lower() for role in USER_ROLES]
        invalid_roles = [role for role in roles if role not in valid_roles]
        if invalid_roles:
            await interaction.response.send_message(
                f"❌ Invalid roles: {', '.join(invalid_roles)}. Valid roles: {', '.join(USER_ROLES)}",
                ephemeral=True
            )
            return
        
        # Validate tech skills - same validation as roles
        tech_skills = [skill.strip() for skill in self.tech_skills.value.split(',')]
        valid_skills = [skill.lower() for skill in TECH_SKILLS]
        invalid_skills = [skill for skill in tech_skills if skill.lower() not in valid_skills]
        if invalid_skills:
            await interaction.response.send_message(
                f"❌ Invalid tech skills: {', '.join(invalid_skills)}. Please check the available skills list.",
                ephemeral=True
            )
            return
        
        # Create/update profile - build the profile object
        profile = {
            "user_id": user_id,
            "username": interaction.user.display_name,
            "roles": roles,
            "tech_skills": tech_skills,
            "experience": experience,
            "timezone": self.timezone.value.strip(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save profile - write to JSON file
        data = load_data()
        data[user_id] = profile
        save_data(data)
        
        # Create response - show success message with profile details
        embed = discord.Embed(
            title="✅ Profile Created Successfully!" if not is_update else "✅ Profile Updated Successfully!",
            description=f"Your profile has been saved.",
            color=EMBED_COLORS["success"]
        )
        
        embed.add_field(name="Roles", value=", ".join(roles).title(), inline=True)
        embed.add_field(name="Experience", value=experience.title(), inline=True)
        embed.add_field(name="Timezone", value=profile["timezone"], inline=True)
        embed.add_field(name="Tech Skills", value=", ".join(tech_skills), inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True) 