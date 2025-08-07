# ShopSavvy Bot - Render.com Deployment Guide

## Overview

This guide explains how to deploy your ShopSavvy Telegram bot to Render.com using Docker with proper port configuration and webhook support.

## Files Created

- `Dockerfile` - Docker container configuration
- `render_main.py` - Production version with webhook support
- `render-requirements.txt` - Python dependencies for deployment
- `render.yaml` - Render.com service configuration
- `.dockerignore` - Files to exclude from Docker build

## Quick Deploy to Render.com

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render.com deployment support"
   git push origin main
   ```

2. **Connect to Render.com**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**
   - In your Render.com dashboard, go to your service
   - Navigate to "Environment" tab
   - Add: `TELEGRAM_BOT_TOKEN` (your bot token from BotFather)

### Option 2: Manual Docker Deploy

1. **Create New Web Service**
   - Go to Render.com dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: shopsavvy-telegram-bot
   - **Environment**: Docker
   - **Region**: Oregon (or preferred)
   - **Branch**: main
   - **Dockerfile Path**: ./Dockerfile

3. **Environment Variables**
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `RENDER`: true
   - `PORT`: 10000

4. **Advanced Settings**
   - **Health Check Path**: /health
   - **Auto Deploy**: Yes

## Bot Features in Production

### Webhook Mode
The bot automatically switches to webhook mode when deployed on Render.com, which is more efficient than polling.

### Health Monitoring
- **Health Check**: `/health` - Returns bot status
- **Status Endpoint**: `/status` - Detailed bot information
- **Root Endpoint**: `/` - Welcome message

### Port Configuration
The bot automatically uses Render.com's `PORT` environment variable and listens on `0.0.0.0` for external traffic.

## Environment Variables Required

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | Yes |
| `RENDER` | Set to 'true' for production mode | Auto-set |
| `PORT` | Port number (auto-set by Render) | Auto-set |

## Monitoring Your Bot

### Check Bot Status
Visit your deployed app URL to see:
- Bot running status
- Webhook information
- Health check results

### Logs
Monitor your bot through Render.com dashboard:
- Go to your service
- Click "Logs" tab
- View real-time bot activity

### Webhook URL
Your webhook will be automatically set to:
```
https://your-app-name.onrender.com/webhook
```

## Local vs Production Differences

### Local Development (main.py)
- Uses polling mode
- Runs on localhost
- No webhook setup required

### Production (render_main.py)
- Uses webhook mode
- Includes Flask web server
- Health check endpoints
- Automatic webhook configuration

## Troubleshooting

### Bot Not Responding
1. Check environment variables are set
2. Verify bot token is correct
3. Check logs for errors
4. Visit `/health` endpoint

### Webhook Issues
1. Ensure HTTPS is working
2. Check webhook URL is accessible
3. Verify bot token permissions

### Port Issues
Render automatically assigns ports. The bot uses the `PORT` environment variable provided by Render.

## Cost Estimation

**Render.com Starter Plan**: $7/month
- 512MB RAM
- 0.1 CPU
- Perfect for Telegram bots
- Automatic SSL
- Custom domains supported

## Post-Deployment

1. **Test Your Bot**
   - Message your bot on Telegram
   - Verify all features work
   - Check search and image functionality

2. **Monitor Performance**
   - Watch logs for errors
   - Monitor response times
   - Check health endpoint regularly

3. **Update Bot**
   - Push changes to GitHub
   - Auto-deploy will update your bot
   - No downtime required

## Support

For issues:
- Check Render.com logs
- Visit health endpoints
- Verify environment variables
- Test locally first with `main.py`