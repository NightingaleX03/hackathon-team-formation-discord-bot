"""
Team matching utilities for the Hackathon Team Finder Discord Bot
"""

from typing import Dict, List, Tuple, Any
import json

def find_compatible_teammates(user_profile: Dict[str, Any], all_users: Dict[str, Any]) -> List[Tuple[str, float]]:
    """Find compatible team members based on user profile"""
    compatible_users = []
    user_id = user_profile.get("user_id", "")
    
    for other_user_id, other_profile in all_users.items():
        if other_user_id == user_id:
            continue
        
        compatibility_score = calculate_compatibility(user_profile, other_profile)
        if compatibility_score > 0.3:  # Minimum compatibility threshold
            compatible_users.append((other_user_id, compatibility_score))
    
    # Sort by compatibility score (highest first)
    compatible_users.sort(key=lambda x: x[1], reverse=True)
    return compatible_users

def calculate_compatibility(profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
    """Calculate compatibility score between two users"""
    score = 0.0
    
    # Role compatibility (complementary roles get higher scores)
    roles1 = set(profile1.get("roles", []))
    roles2 = set(profile2.get("roles", []))
    
    # Different roles are better for team diversity
    if roles1 != roles2:
        score += 0.3
    
    # Skill overlap (some overlap is good, but not too much)
    skills1 = set(profile1.get("tech_skills", []))
    skills2 = set(profile2.get("tech_skills", []))
    
    overlap = len(skills1.intersection(skills2))
    total_skills = len(skills1.union(skills2))
    
    if total_skills > 0:
        overlap_ratio = overlap / total_skills
        # Moderate overlap is ideal (0.2-0.6)
        if 0.2 <= overlap_ratio <= 0.6:
            score += 0.4
        elif overlap_ratio > 0.6:
            score += 0.2  # Too much overlap
        else:
            score += 0.1  # Too little overlap
    
    # Experience level compatibility
    exp1 = profile1.get("experience", "").lower()
    exp2 = profile2.get("experience", "").lower()
    
    # Mix of experience levels is good
    if exp1 != exp2:
        score += 0.2
    
    # Timezone compatibility (same timezone is better)
    tz1 = profile1.get("timezone", "")
    tz2 = profile2.get("timezone", "")
    
    if tz1 == tz2:
        score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0

def find_team_matches(user_profile: Dict[str, Any], hackathon_id: int) -> List[Dict[str, Any]]:
    """Find team matches for a specific hackathon"""
    # Load all users and hackathon data
    try:
        with open("example_data.json", "r") as f:
            all_users = json.load(f)
    except FileNotFoundError:
        return []
    
    try:
        with open("example_hackathons.json", "r") as f:
            hackathons = json.load(f)
    except FileNotFoundError:
        return []
    
    # Find the specific hackathon
    hackathon = next((h for h in hackathons if h["id"] == hackathon_id), None)
    if not hackathon:
        return []
    
    # Get participants in this hackathon
    participants = hackathon.get("participants", [])
    
    # Find compatible users among participants
    compatible_users = []
    user_id = user_profile.get("user_id", "")
    
    for participant_id in participants:
        if participant_id == user_id or participant_id not in all_users:
            continue
        
        other_profile = all_users[participant_id]
        compatibility_score = calculate_compatibility(user_profile, other_profile)
        
        if compatibility_score > 0.3:
            compatible_users.append({
                "user_id": participant_id,
                "profile": other_profile,
                "compatibility_score": compatibility_score
            })
    
    # Sort by compatibility score
    compatible_users.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return compatible_users

def format_matches(matches: List[Dict[str, Any]]) -> str:
    """Format team matches for display"""
    if not matches:
        return "No compatible team members found."
    
    formatted = []
    for i, match in enumerate(matches[:5], 1):  # Show top 5 matches
        profile = match["profile"]
        score = match["compatibility_score"]
        
        formatted.append(
            f"{i}. **{profile['username']}** (Score: {score:.1f})\n"
            f"   Roles: {', '.join(profile['roles']).title()}\n"
            f"   Skills: {', '.join(profile['tech_skills'][:3])}\n"
            f"   Experience: {profile['experience'].title()}"
        )
    
    return "\n\n".join(formatted) 