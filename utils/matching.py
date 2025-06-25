"""
Matching algorithm and utilities for the Hackathon Team Finder Discord Bot
"""

from typing import List, Dict, Any
from config import (
    TIMEZONE_MATCH_SCORE, 
    ROLE_COMPLEMENT_SCORE, 
    TECH_STACK_MATCH_SCORE,
    COMPLEMENTARY_ROLES,
    MAX_MATCHES
)
from utils.data_manager import load_hackathons

def find_team_matches(user_id: str, hackathon_id: int, looking_for: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find compatible team members for a user in a specific hackathon - the core matching logic"""
    if user_id not in data:
        return []
    
    user_profile = data[user_id]
    matches = []
    
    hackathons = load_hackathons()
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        return []
    
    # Get all users in this hackathon - only match within the same hackathon
    hackathon_user_ids = [team["user_id"] for team in hackathon["teams"]]
    
    for other_id in hackathon_user_ids:
        if other_id == user_id or other_id not in data:
            continue
        
        other_profile = data[other_id]
        score = calculate_compatibility(user_profile, other_profile, looking_for)
        if score > 0:
            matches.append({
                "user_id": other_id,
                "profile": other_profile,
                "score": score
            })
    
    # Sort by score (highest first) and return top matches - simple ranking
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:MAX_MATCHES]

def calculate_compatibility(profile1: Dict[str, Any], profile2: Dict[str, Any], looking_for: str) -> int:
    """Calculate compatibility score between two profiles - my scoring algorithm"""
    score = 0
    
    # Timezone compatibility - working in same timezone is huge
    if profile1["timezone"].lower() == profile2["timezone"].lower():
        score += TIMEZONE_MATCH_SCORE
    
    # Role compatibility based on what user is looking for
    looking_for_lower = looking_for.lower()
    profile2_roles = [role.lower() for role in profile2["roles"]]
    
    if looking_for_lower in profile2_roles:
        score += ROLE_COMPLEMENT_SCORE * 2  # Direct match gets higher score
    
    # Check for complementary roles - like frontend + backend
    for role_pair in COMPLEMENTARY_ROLES:
        if (looking_for_lower in role_pair and any(role in role_pair for role in profile2_roles)):
            score += ROLE_COMPLEMENT_SCORE
            break
    
    # Tech stack compatibility - shared skills are good
    tech1 = set(tech.lower() for tech in profile1["tech_skills"])
    tech2 = set(tech.lower() for tech in profile2["tech_skills"])
    shared_tech = tech1.intersection(tech2)
    score += len(shared_tech) * TECH_STACK_MATCH_SCORE
    
    return score

def format_matches(matches: List[Dict[str, Any]], data: Dict[str, Any]) -> str:
    """Format matches for display - makes it look nice in Discord"""
    if not matches:
        return "No compatible team members found."
    
    result = []
    for i, match in enumerate(matches, 1):
        profile = match["profile"]
        result.append(
            f"**{i}. {profile['username']}** (Score: {match['score']})\n"
            f"   Roles: {', '.join(profile['roles']).title()}\n"
            f"   Experience: {profile['experience'].title()}\n"
            f"   Skills: {', '.join(profile['tech_skills'][:5])}{'...' if len(profile['tech_skills']) > 5 else ''}"
        )
    
    return "\n\n".join(result) 