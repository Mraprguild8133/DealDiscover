#!/usr/bin/env python3
"""
ShopSavvy - Telegram Bot for Finding Deals Across Indian E-commerce Platforms
Render.com deployment version with webhook support
"""
import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ConversationHandler, MessageHandler, filters
)

from config import BOT_TOKEN, PLATFORM_SELECTION, PRODUCT_SEARCH, CATEGORY_SEARCH
from bot_handlers import (
    start, help_command, deals_command, button_callback,
    handle_product_search, handle_invalid_input, cancel_conversation,
    handle_text_message, error_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app for webhook
app = Flask(__name__)

# Global application instance
telegram_app = None

def create_telegram_app():
    """Create and configure the Telegram application"""
    global telegram_app
    
    # Validate bot token
    if BOT_TOKEN == "your_bot_token_here":
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
        return None
    
    # Create application
    telegram_app = Application.builder().token(BOT_TOKEN).build()
    
    # Create conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(button_callback, pattern='^(search_products|browse_categories|platform_|category_).*$')
        ],
        states={
            PLATFORM_SELECTION: [
                CallbackQueryHandler(button_callback, pattern='^platform_.*$')
            ],
            PRODUCT_SEARCH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_search)
            ],
            CATEGORY_SEARCH: [
                CallbackQueryHandler(button_callback, pattern='^category_.*$')
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_conversation),
            MessageHandler(filters.TEXT, handle_invalid_input)
        ],
        allow_reentry=True
    )
    
    # Add handlers
    telegram_app.add_handler(conversation_handler)
    telegram_app.add_handler(CommandHandler('help', help_command))
    telegram_app.add_handler(CommandHandler('deals', deals_command))
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Add error handler
    telegram_app.add_error_handler(error_handler)
    
    return telegram_app

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates"""
    if telegram_app is None:
        return "Bot not initialized", 500
        
    try:
        # Get the JSON data
        json_data = request.get_json()
        
        # Create Update object
        update = Update.de_json(json_data, telegram_app.bot)
        
        # Process the update
        telegram_app.update_queue.put_nowait(update)
        
        return "OK", 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return "Error", 500

@app.route('/health')
def health():
    """Health check endpoint for Render.com"""
    return {
        "status": "healthy",
        "bot": "ShopSavvy",
        "version": "1.0.0",
        "mode": "webhook" if os.getenv('RENDER') else "polling"
    }

@app.route('/status')
def status():
    """Bot status endpoint"""
    return {
        "bot_status": "running" if telegram_app else "not_initialized",
        "platform": "render.com" if os.getenv('RENDER') else "local",
        "webhook_url": f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/webhook" if os.getenv('RENDER') else None
    }

@app.route('/')
def home():
    """Root endpoint"""
    return {
        "message": "ShopSavvy Telegram Bot is running!",
        "bot": "@" + telegram_app.bot.username if telegram_app and telegram_app.bot else "Not initialized",
        "status": "Visit /status for bot status",
        "health": "Visit /health for health check"
    }

async def setup_webhook():
    """Set up webhook for production deployment"""
    if telegram_app and os.getenv('RENDER'):
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
        await telegram_app.bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")

def main():
    """Main function to run the bot"""
    
    # Create telegram application
    create_telegram_app()
    
    if telegram_app is None:
        logger.error("Failed to create Telegram application")
        return
    
    logger.info("🤖 ShopSavvy Bot is starting...")
    logger.info("🔍 Ready to help users find the best deals!")
    
    # Check if running on Render.com
    if os.getenv('RENDER'):
        logger.info("🚀 Running in production mode (webhook)")
        # Initialize the application
        import asyncio
        asyncio.run(telegram_app.initialize())
        asyncio.run(setup_webhook())
        
        # Start Flask server
        port = int(os.getenv('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        logger.info("🔧 Running in development mode (polling)")
        try:
            # Use polling for development
            telegram_app.run_polling(
                allowed_updates=['message', 'callback_query'],
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            logger.info("Make sure TELEGRAM_BOT_TOKEN is set correctly")

if __name__ == '__main__':
    main()