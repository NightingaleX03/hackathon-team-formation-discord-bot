"""
Hackathon Modal for creating new hackathons
"""

import discord
from discord.ui import Modal, TextInput
from utils.data_manager import load_data
import json
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
        
        # Location
        self.location = TextInput(
            label="Location",
            placeholder="e.g., San Francisco, CA or Virtual",
            required=True,
            max_length=100
        )
        
        # Prize
        self.prize = TextInput(
            label="Prize Pool",
            placeholder="e.g., $50,000 or TBD",
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
        self.add_item(self.location)
        self.add_item(self.prize)
        self.add_item(self.description)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle the form submission"""
        # Load existing hackathons
        try:
            with open("example_hackathons.json", "r") as f:
                hackathons = json.load(f)
        except FileNotFoundError:
            hackathons = []
        
        # Generate new ID
        new_id = max([h["id"] for h in hackathons], default=0) + 1
        
        # Create new hackathon
        new_hackathon = {
            "id": new_id,
            "name": self.name.value.strip(),
            "date": self.date.value.strip(),
            "location": self.location.value.strip(),
            "prize": self.prize.value.strip(),
            "description": self.description.value.strip(),
            "created_by": str(interaction.user.id),
            "created_at": datetime.now().isoformat(),
            "participants": []
        }
        
        # Add to hackathons list
        hackathons.append(new_hackathon)
        
        # Save to file
        with open("example_hackathons.json", "w") as f:
            json.dump(hackathons, f, indent=2)
        
        # Create success embed
        embed = discord.Embed(
            title="✅ Hackathon Added Successfully!",
            color=0x00ff00
        )
        
        embed.add_field(name="Name", value=new_hackathon["name"], inline=True)
        embed.add_field(name="Date", value=new_hackathon["date"], inline=True)
        embed.add_field(name="Location", value=new_hackathon["location"], inline=True)
        embed.add_field(name="Prize", value=new_hackathon["prize"], inline=True)
        embed.add_field(name="Description", value=new_hackathon["description"][:100] + "...", inline=False)
        embed.add_field(name="ID", value=f"#{new_hackathon['id']}", inline=True)
        
        embed.set_footer(text="Users can now join this hackathon using /pick-hackathon")
        
        await interaction.response.send_message(embed=embed, ephemeral=True) 