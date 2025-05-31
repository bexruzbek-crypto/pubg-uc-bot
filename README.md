
# PUBG UC Telegram Bot

This bot allows users to order PUBG UC via Telegram and submit payment confirmation screenshots.

## 🚀 Deployment (Railway)

1. Push this project to a GitHub repository.
2. Go to [https://railway.app](https://railway.app) and create a new project.
3. Link your GitHub repo and deploy it.
4. In Railway settings, add the following environment variables:
   - `API_TOKEN`: Your Telegram Bot token
   - `ADMIN_ID`: Your admin Telegram ID

The bot will start automatically.

## 📁 Included Files

- `ucc.py` — main bot logic
- `requirements.txt` — dependencies
- `Procfile` — for Railway worker
- `.env.example` — environment variable example
