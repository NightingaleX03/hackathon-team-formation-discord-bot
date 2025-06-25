"""
Hackathon modal for the Hackathon Team Finder Discord Bot
"""

import discord
from datetime import datetime
from config import EMBED_COLORS
from utils.data_manager import load_hackathons, save_hackathons
from utils.permissions import is_admin

class HackathonModal(discord.ui.Modal):
    """Modal for adding hackathons (admin only) - simple form for hackathon details"""
    
    def __init__(self):
        super().__init__(title="Add Hackathon")
        
        self.name = discord.ui.TextInput(
            label="Hackathon Name",
            placeholder="e.g., HackMIT 2024",
            max_length=100,
            required=True
        )
        
        self.description = discord.ui.TextInput(
            label="Description",
            placeholder="Brief description of the hackathon",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=True
        )
        
        self.date = discord.ui.TextInput(
            label="Date",
            placeholder="e.g., December 15-17, 2024",
            max_length=50,
            required=True
        )
        
        self.add_item(self.name)
        self.add_item(self.description)
        self.add_item(self.date)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission - check admin and save hackathon"""
        if not is_admin(interaction.user):
            await interaction.response.send_message("❌ Only administrators can add hackathons.", ephemeral=True)
            return
        
        # Create hackathon object - auto-generate ID based on existing count
        hackathon = {
            "id": len(load_hackathons()) + 1,
            "name": self.name.value.strip(),
            "description": self.description.value.strip(),
            "date": self.date.value.strip(),
            "teams": [],
            "created_at": datetime.now().isoformat()
        }
        
        # Save to file - append to existing hackathons
        hackathons = load_hackathons()
        hackathons.append(hackathon)
        save_hackathons(hackathons)
        
        # Show success message - confirm the hackathon was added
        embed = discord.Embed(
            title="✅ Hackathon Added Successfully!",
            description=f"**{hackathon['name']}** has been added to the list.",
            color=EMBED_COLORS["hackathon"]
        )
        embed.add_field(name="Description", value=hackathon["description"], inline=False)
        embed.add_field(name="Date", value=hackathon["date"], inline=True)
        embed.add_field(name="ID", value=str(hackathon["id"]), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True) 