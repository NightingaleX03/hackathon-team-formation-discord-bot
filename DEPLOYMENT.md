# 🚀 Deploy to Render

This guide will help you deploy your Discord bot to Render.

## 📋 Prerequisites

1. **Discord Bot Token** - You need your bot token from Discord Developer Portal
2. **GitHub Account** - Your code needs to be on GitHub
3. **Render Account** - Sign up at https://render.com

## 🔧 Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository**:
   - Go to GitHub and create a new repository
   - Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

## 🌐 Step 2: Deploy on Render

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Create New Service**:
   - Click "New +"
   - Select "Web Service"

3. **Connect GitHub**:
   - Connect your GitHub account if not already connected
   - Select your repository

4. **Configure Service**:
   - **Name**: `hackathon-team-finder-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Plan**: `Free`

5. **Add Environment Variables**:
   - Click "Environment" tab
   - Add variable:
     - **Key**: `DISCORD_TOKEN`
     - **Value**: Your Discord bot token
   - Click "Save Changes"

6. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete

## ✅ Step 3: Verify Deployment

1. **Check Logs**: In Render dashboard, check the logs to ensure bot started successfully
2. **Test Commands**: Go to your Discord server and try `/create-profile`

## 🔄 Step 4: Update Bot (Optional)

To update your bot:
1. Push changes to GitHub
2. Render will automatically redeploy

## 🆘 Troubleshooting

### Bot Not Responding
- Check Render logs for errors
- Verify Discord token is correct
- Ensure bot is invited to server with correct permissions

### Commands Not Working
- Commands may take up to 1 hour to appear globally
- Try using `/` to see if commands are available

### Build Failures
- Check that all files are committed to GitHub
- Verify requirements.txt is correct
- Check Render logs for specific error messages

## 📝 Important Notes

- **Free Plan Limitations**: Render free plan has limitations on uptime
- **Environment Variables**: Never commit your Discord token to GitHub
- **Logs**: Check Render logs for debugging information
- **Uptime**: Free plan may have some downtime

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [py-cord Documentation](https://docs.pycord.dev/) 