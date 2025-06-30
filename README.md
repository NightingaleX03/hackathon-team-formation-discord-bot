# 🏆 Hackathon Team Finder Discord Bot

A comprehensive Discord bot designed to help developers find team members for hackathons. The bot allows users to create profiles, join hackathons, and find compatible team members based on skills, roles, and preferences.

## ✨ Features

### 🎯 Core Functionality
- **User Profiles**: Create and manage developer profiles with roles, skills, and experience
- **Hackathon Management**: Admins can add/remove hackathons from the list
- **Team Matching**: Find compatible team members based on skills and preferences
- **Smart Matching Algorithm**: Matches users based on timezone, roles, and tech skills
- **Real-time Notifications**: Ping matched users to facilitate connections

### 👤 User Profile System
- **Multiple Roles**: Choose from backend, frontend, AI/ML, VR, designer, web developer, game developer
- **Tech Skills**: Select from 50+ predefined tech skills
- **Experience Levels**: Beginner, Intermediate, Advanced
- **Timezone Support**: Specify your timezone for better matching
- **Profile Updates**: Update your profile anytime

### 🏆 Hackathon Management
- **Admin Controls**: Only server admins can add/remove hackathons
- **Hackathon Details**: Name, description, dates, and participant tracking
- **Team Formation**: Join hackathons and find team members
- **Participant Lists**: View all participants in each hackathon

## 🚀 Commands

### User Commands

#### Profile Management
- `/create-profile` - Create your developer profile
- `/update-profile` - Update your existing profile
- `/view-profile` - View your current profile

#### Hackathon Participation
- `/find-team` - Start the team-finding process
- `/pick-hackathon <id> <looking_for>` - Select a hackathon and specify what you're looking for
- `/remove-from-hackathon <id>` - Remove yourself from a hackathon
- `/hackathon-teams <id>` - View all participants in a hackathon

#### Information
- `/list-hackathons` - View all available hackathons
- `/stats` - View bot statistics

### Admin Commands

#### Hackathon Management
- `/add-hackathon` - Add a new hackathon to the list
- `/remove-hackathon <id>` - Remove a hackathon from the list

## 🎮 How to Use

### 1. Create Your Profile
```
/create-profile
```
Fill out the form with:
- **Roles**: Choose from backend, frontend, AI/ML, VR, designer, web developer, game developer
- **Tech Skills**: Select from 50+ available skills
- **Experience Level**: Beginner, Intermediate, or Advanced
- **Timezone**: Your timezone for better matching

### 2. Find Team Members
```
/find-team
```
This will show you all available hackathons. Then use:
```
/pick-hackathon <hackathon_id> <what_you_are_looking_for>
```

**Example:**
```
/pick-hackathon 1 frontend
```

### 3. Get Matched
The bot will:
- Add you to the hackathon participant list
- Find compatible team members based on your criteria
- Show you the best matches with compatibility scores
- Ping the matched users so they can connect with you

### 4. Form Your Team
Once you find team members:
- Connect with them via Discord
- Use `/remove-from-hackathon <id>` when your team is formed


## 📊 Available Roles

Users can select from these roles:
- **Backend Developer**
- **Frontend Developer**
- **AI/ML Engineer**
- **VR Developer**
- **Designer**
- **Web Developer**
- **Game Developer**

## 🛠️ Tech Skills

The bot includes 50+ predefined tech skills including:
- **Programming Languages**: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust
- **Frameworks**: React, Vue.js, Angular, Node.js, Express, Django, Flask
- **Databases**: MongoDB, PostgreSQL, MySQL, Redis
- **Cloud Platforms**: AWS, Azure, GCP
- **DevOps**: Docker, Kubernetes, Git, CI/CD
- **AI/ML**: TensorFlow, PyTorch, Scikit-learn, OpenAI API
- **Game Development**: Unity, Unreal Engine
- **Design Tools**: Figma, Adobe Creative Suite
- **And many more...**

## 🎯 Matching Algorithm

The bot uses a sophisticated matching algorithm that considers:

1. **Role Compatibility** (Score: 3-6 points)
   - Direct role matches get higher scores
   - Complementary roles (e.g., frontend + backend) get bonus points

2. **Timezone Matching** (Score: 2 points)
   - Users in the same timezone get bonus points

3. **Tech Stack Overlap** (Score: 1 point per shared skill)
   - Shared technical skills increase compatibility

## 📁 File Structure

```
discord-bot/
├── bot.py                    # Main bot file
├── config.py                 # Configuration and constants
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── example_data.json        # Example user profiles
├── example_hackathons.json  # Example hackathon data
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── data_manager.py      # Data loading/saving utilities
│   ├── matching.py          # Matching algorithm
│   └── permissions.py       # Permission checks
├── modals/                  # Discord UI modals
│   ├── __init__.py
│   ├── user_profile_modal.py # User profile creation modal
│   └── hackathon_modal.py   # Hackathon creation modal
└── commands/                # Bot commands
    ├── __init__.py
    ├── profile_commands.py  # Profile-related commands
    ├── hackathon_commands.py # Hackathon-related commands
    └── info_commands.py     # Information and utility commands
```

## 🏗️ Code Organization

The bot is organized into logical modules for better maintainability:

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Adding more tech skills or roles
- Improving the matching algorithm

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the bot's help commands
2. Ensure you have the correct permissions
3. Verify your Discord bot token is correct
4. Check that the bot has been invited with the right permissions

Thank you <3
