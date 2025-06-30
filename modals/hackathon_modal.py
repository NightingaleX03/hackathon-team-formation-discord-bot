"""
Hackathon Modal for creating new hackathons
"""

import discord
from discord.ui import Modal, TextInput
from utils.data_manager import save_single_hackathon, get_all_hackathons
from datetime import datetime

class HackathonModal(Modal):
    def __init__(self):
        super().__init__(title="Add New Hackathon")
        
        # Hackathon name
        self.name = TextInput(
            label="Hackathon Name",
            placeholder="e.g., TechCrunch Disrupt 2024",
            required=True,
            max_length=100
        )
        
        # Date
        self.date = TextInput(
            label="Date",
            placeholder="e.g., March 15-17, 2024",
            required=True,
            max_length=50
        )
        
        # Description
        self.description = TextInput(
            label="Description",
            placeholder="Brief description of the hackathon...",
            required=True,
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        
        # Add all fields to the modal
        self.add_item(self.name)
        self.add_item(self.date)
        self.add_item(self.description)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle the form submission"""
        # Get existing hackathons to generate new ID
        existing_hackathons = get_all_hackathons()
        new_id = max([h["id"] for h in existing_hackathons], default=0) + 1
        
        # Create new hackathon
        new_hackathon = {
            "name": self.name.value.strip(),
            "date": self.date.value.strip(),
            "description": self.description.value.strip(),
            "teams": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to database
        success = save_single_hackathon(new_hackathon)
        
        if not success:
            await interaction.response.send_message("❌ Failed to create hackathon. Please try again.", ephemeral=True)
            return
        
        # Create success embed
        embed = discord.Embed(
            title="✅ Hackathon Added Successfully!",
            color=0x00ff00
        )
        
        embed.add_field(name="Name", value=new_hackathon["name"], inline=True)
        embed.add_field(name="Date", value=new_hackathon["date"], inline=True)
        embed.add_field(name="Description", value=new_hackathon["description"][:100] + "...", inline=False)
        embed.add_field(name="ID", value=f"#{new_id}", inline=True)
        
        embed.set_footer(text="Users can now join this hackathon using /pick-hackathon")
        
        await interaction.response.send_message(embed=embed, ephemeral=True) 