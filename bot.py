import discord
import json
import os
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from config import *

# Load environment variables from .env file (if it exists and is readable)
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Make sure your .env file exists and has the correct format:")
    print("DISCORD_TOKEN=your_actual_bot_token_here")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

def load_data() -> Dict[str, Any]:
    """Load user data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data: Dict[str, Any]):
    """Save user data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class TeamProfileModal(discord.ui.Modal):
    """Modal for collecting team profile information"""
    
    def __init__(self):
        super().__init__(title="Team Profile Setup")
        
        self.tech_stack = discord.ui.TextInput(
            label="Tech Stack(s)",
            placeholder="e.g., Python, React, Node.js, AWS (comma-separated)",
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
        
        self.role = discord.ui.TextInput(
            label="Preferred Role",
            placeholder="e.g., Frontend, Backend, PM, Designer, Full-stack",
            max_length=50,
            required=True
        )
        
        self.looking_for_team = discord.ui.TextInput(
            label="Looking for Team? (Yes/No)",
            placeholder="Yes or No",
            max_length=5,
            required=True
        )
        
        self.add_item(self.tech_stack)
        self.add_item(self.experience)
        self.add_item(self.timezone)
        self.add_item(self.role)
        self.add_item(self.looking_for_team)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        user_id = str(interaction.user.id)
        
        # Validate experience level
        experience = self.experience.value.strip().lower()
        if experience not in VALID_EXPERIENCE_LEVELS:
            await interaction.response.send_message(
                f"❌ Invalid experience level. Please use: {', '.join(VALID_EXPERIENCE_LEVELS).title()}",
                ephemeral=True
            )
            return
        
        # Validate looking for team
        looking = self.looking_for_team.value.strip().lower()
        if looking not in VALID_YES_NO:
            await interaction.response.send_message(
                f"❌ Invalid response. Please use: {', '.join(VALID_YES_NO).title()}",
                ephemeral=True
            )
            return
        
        # Create profile
        profile = {
            "user_id": user_id,
            "username": interaction.user.display_name,
            "tech_stack": [tech.strip() for tech in self.tech_stack.value.split(',')],
            "experience": experience,
            "timezone": self.timezone.value.strip(),
            "role": self.role.value.strip(),
            "looking_for_team": looking == 'yes',
            "created_at": datetime.now().isoformat()
        }
        
        # Save profile
        data = load_data()
        data[user_id] = profile
        save_data(data)
        
        # Find matches
        matches = find_matches(user_id, data)
        
        # Create response
        embed = discord.Embed(
            title="✅ Profile Created Successfully!",
            description=f"Your team profile has been saved.",
            color=EMBED_COLORS["success"]
        )
        
        embed.add_field(name="Tech Stack", value=", ".join(profile["tech_stack"]), inline=True)
        embed.add_field(name="Experience", value=profile["experience"].title(), inline=True)
        embed.add_field(name="Timezone", value=profile["timezone"], inline=True)
        embed.add_field(name="Role", value=profile["role"], inline=True)
        embed.add_field(name="Looking for Team", value="Yes" if profile["looking_for_team"] else "No", inline=True)
        
        if matches:
            embed.add_field(
                name="🤝 Suggested Matches",
                value=format_matches(matches, data),
                inline=False
            )
        else:
            embed.add_field(
                name="🤝 No Matches Found",
                value="No compatible team members found yet. Check back later!",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def find_matches(user_id: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find compatible team members for a user"""
    if user_id not in data:
        return []
    
    user_profile = data[user_id]
    matches = []
    
    for other_id, other_profile in data.items():
        if other_id == user_id or not other_profile.get("looking_for_team", False):
            continue
        
        score = calculate_compatibility(user_profile, other_profile)
        if score > 0:
            matches.append({
                "user_id": other_id,
                "profile": other_profile,
                "score": score
            })
    
    # Sort by score (highest first) and return top matches
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:MAX_MATCHES]

def calculate_compatibility(profile1: Dict[str, Any], profile2: Dict[str, Any]) -> int:
    """Calculate compatibility score between two profiles"""
    score = 0
    
    # Timezone compatibility
    if profile1["timezone"].lower() == profile2["timezone"].lower():
        score += TIMEZONE_MATCH_SCORE
    
    # Role compatibility
    role1 = profile1["role"].lower()
    role2 = profile2["role"].lower()
    
    for role_pair in COMPLEMENTARY_ROLES:
        if (role1 in role_pair and role2 in role_pair) or (role1 == role2):
            score += ROLE_COMPLEMENT_SCORE
            break
    
    # Tech stack compatibility
    tech1 = set(tech.lower() for tech in profile1["tech_stack"])
    tech2 = set(tech.lower() for tech in profile2["tech_stack"])
    shared_tech = tech1.intersection(tech2)
    score += len(shared_tech) * TECH_STACK_MATCH_SCORE
    
    return score

def format_matches(matches: List[Dict[str, Any]], data: Dict[str, Any]) -> str:
    """Format matches for display"""
    if not matches:
        return "No matches found."
    
    formatted = []
    for i, match in enumerate(matches, 1):
        profile = match["profile"]
        score = match["score"]
        
        # Get user mention
        user_mention = f"<@{profile['user_id']}>"
        
        # Format compatibility notes
        notes = []
        if score >= 5:
            notes.append("🌟 Excellent match!")
        elif score >= 3:
            notes.append("👍 Good match")
        else:
            notes.append("🤝 Compatible")
        
        formatted.append(
            f"{i}. {user_mention} (Score: {score})\n"
            f"   Role: {profile['role']} | Tech: {', '.join(profile['tech_stack'][:3])}\n"
            f"   {' '.join(notes)}"
        )
    
    return "\n\n".join(formatted)

@bot.slash_command(name="looking-for-team", description="Set up your team profile and find matches")
async def looking_for_team(ctx: discord.ApplicationContext):
    """Command to set up team profile"""
    modal = TeamProfileModal()
    await ctx.send_modal(modal)

@bot.slash_command(name="reset-team-profile", description="Remove or update your team profile")
async def reset_team_profile(ctx: discord.ApplicationContext):
    """Command to reset team profile"""
    user_id = str(ctx.user.id)
    data = load_data()
    
    if user_id in data:
        del data[user_id]
        save_data(data)
        
        embed = discord.Embed(
            title="🗑️ Profile Removed",
            description="Your team profile has been deleted successfully.",
            color=EMBED_COLORS["error"]
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="❌ No Profile Found",
            description="You don't have a team profile to remove.",
            color=EMBED_COLORS["warning"]
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="view-profile", description="View your current team profile")
async def view_profile(ctx: discord.ApplicationContext):
    """Command to view current profile"""
    user_id = str(ctx.user.id)
    data = load_data()
    
    if user_id in data:
        profile = data[user_id]
        
        embed = discord.Embed(
            title="👤 Your Team Profile",
            color=EMBED_COLORS["info"]
        )
        
        embed.add_field(name="Tech Stack", value=", ".join(profile["tech_stack"]), inline=True)
        embed.add_field(name="Experience", value=profile["experience"].title(), inline=True)
        embed.add_field(name="Timezone", value=profile["timezone"], inline=True)
        embed.add_field(name="Role", value=profile["role"], inline=True)
        embed.add_field(name="Looking for Team", value="Yes" if profile["looking_for_team"] else "No", inline=True)
        embed.add_field(name="Created", value=profile["created_at"][:10], inline=True)
        
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="❌ No Profile Found",
            description="You don't have a team profile. Use `/looking-for-team` to create one!",
            color=EMBED_COLORS["warning"]
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="find-matches", description="Find team matches for your profile")
async def find_matches_command(ctx: discord.ApplicationContext):
    """Command to find matches"""
    user_id = str(ctx.user.id)
    data = load_data()
    
    if user_id not in data:
        embed = discord.Embed(
            title="❌ No Profile Found",
            description="You need to create a profile first using `/looking-for-team`",
            color=EMBED_COLORS["warning"]
        )
        await ctx.respond(embed=embed, ephemeral=True)
        return
    
    matches = find_matches(user_id, data)
    
    if matches:
        embed = discord.Embed(
            title="🤝 Team Matches Found",
            description=format_matches(matches, data),
            color=EMBED_COLORS["match"]
        )
    else:
        embed = discord.Embed(
            title="🤝 No Matches Found",
            description="No compatible team members found yet. Check back later!",
            color=EMBED_COLORS["warning"]
        )
    
    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="stats", description="View bot statistics")
async def stats(ctx: discord.ApplicationContext):
    """Command to view bot statistics"""
    data = load_data()
    total_profiles = len(data)
    looking_for_team = sum(1 for profile in data.values() if profile.get("looking_for_team", False))
    
    # Count by experience level
    experience_counts = {}
    for profile in data.values():
        exp = profile.get("experience", "unknown")
        experience_counts[exp] = experience_counts.get(exp, 0) + 1
    
    # Count by role
    role_counts = {}
    for profile in data.values():
        role = profile.get("role", "unknown")
        role_counts[role] = role_counts.get(role, 0) + 1
    
    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=EMBED_COLORS["info"]
    )
    
    embed.add_field(name="Total Profiles", value=str(total_profiles), inline=True)
    embed.add_field(name="Looking for Team", value=str(looking_for_team), inline=True)
    embed.add_field(name="Active Users", value=str(total_profiles), inline=True)
    
    if experience_counts:
        exp_text = "\n".join([f"{exp.title()}: {count}" for exp, count in experience_counts.items()])
        embed.add_field(name="Experience Levels", value=exp_text, inline=True)
    
    if role_counts:
        role_text = "\n".join([f"{role}: {count}" for role, count in list(role_counts.items())[:5]])
        embed.add_field(name="Top Roles", value=role_text, inline=True)
    
    await ctx.respond(embed=embed, ephemeral=True)

@bot.event
async def on_ready():
    """Bot startup event"""
    print(f"🤖 {bot.user} is ready!")
    print(f"📊 Bot is in {len(bot.guilds)} guilds")
    
    # Set bot status
    await bot.change_presence(activity=discord.Game(name=BOT_STATUS))

# Run the bot
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ Please set your DISCORD_TOKEN environment variable")
        print("You can get your token from: https://discord.com/developers/applications")
    else:
        bot.run(BOT_TOKEN) 