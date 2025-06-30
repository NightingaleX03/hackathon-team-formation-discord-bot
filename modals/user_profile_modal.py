"""
User Profile Modal for creating and updating user profiles with dropdown menus
"""

import discord
from discord.ui import Modal, TextInput, Select
from utils.data_manager import save_user, get_user_by_id
from config import USER_ROLES, TECH_SKILLS, EXPERIENCE_LEVELS, TIMEZONES
from datetime import datetime

class UserProfileModal(Modal):
    def __init__(self, is_update=False, user=None):
        super().__init__(title="Create Your Developer Profile" if not is_update else "Update Your Profile")
        self.is_update = is_update
        self.user = user
        
        # Auto-populate username with Discord display name or username
        default_username = ""
        if user:
            # Use display name if available, otherwise use username
            default_username = user.display_name if user.display_name else user.name
        
        # Username field - pre-filled with Discord username
        self.username = TextInput(
            label="Username",
            placeholder="Enter your preferred username",
            required=True,
            max_length=32,
            default=default_username
        )
        
        # Add all fields to the modal
        self.add_item(self.username)
        
        # Add dropdown selects
        self.add_item(RolesSelect())
        self.add_item(ExperienceSelect())
        self.add_item(TimezoneSelect())
        self.add_item(TechSkillsSelect())
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle the form submission"""
        user_id = str(interaction.user.id)
        
        # Get values from the modal
        username = self.username.value.strip()
        
        # Get values from the select components
        roles = getattr(self, 'selected_roles', [])
        experience = getattr(self, 'selected_experience', '')
        timezone = getattr(self, 'selected_timezone', '')
        tech_skills = getattr(self, 'selected_tech_skills', [])
        
        # Validate input
        if not username or not roles or not experience or not timezone or not tech_skills:
            await interaction.response.send_message("❌ All fields are required!", ephemeral=True)
            return
        
        # Create or update the profile
        profile_data = {
            "user_id": user_id,
            "username": username,
            "roles": roles,
            "experience": experience,
            "timezone": timezone,
            "tech_skills": tech_skills,
            "looking_for_team": True,
            "updated_at": datetime.now().isoformat()
        }
        
        if not self.is_update:
            profile_data["created_at"] = datetime.now().isoformat()
        
        # Save to database
        success = save_user(profile_data)
        
        if not success:
            await interaction.response.send_message("❌ Failed to save profile. Please try again.", ephemeral=True)
            return
        
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

class RolesSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=role.title(), value=role, description=f"Select {role} role")
            for role in USER_ROLES
        ]
        super().__init__(
            placeholder="Select your roles (multiple allowed)",
            min_values=1,
            max_values=len(USER_ROLES),
            options=options,
            custom_id="roles_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.selected_roles = self.values
        await interaction.response.defer()

class ExperienceSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=level.title(), value=level, description=f"{level} experience level")
            for level in EXPERIENCE_LEVELS
        ]
        super().__init__(
            placeholder="Select your experience level",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="experience_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.selected_experience = self.values[0]
        await interaction.response.defer()

class TimezoneSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=tz, value=tz, description=f"Timezone: {tz}")
            for tz in TIMEZONES
        ]
        super().__init__(
            placeholder="Select your timezone",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="timezone_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.selected_timezone = self.values[0]
        await interaction.response.defer()

class TechSkillsSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=skill.title(), value=skill, description=f"Select {skill} skill")
            for skill in TECH_SKILLS
        ]
        super().__init__(
            placeholder="Select your tech skills (multiple allowed)",
            min_values=1,
            max_values=min(10, len(TECH_SKILLS)),  # Limit to 10 skills max
            options=options,
            custom_id="tech_skills_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.selected_tech_skills = self.values
        await interaction.response.defer() 