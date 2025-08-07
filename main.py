#!/usr/bin/env python3
"""
ShopSavvy - Telegram Bot for Finding Deals Across Indian E-commerce Platforms
"""
import logging
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ConversationHandler, MessageHandler, filters,
    ContextTypes
)
from fastapi import FastAPI, Request, Response
import uvicorn
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

# Set up templates directory
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def create_web_app(app: Application) -> FastAPI:
    """Create FastAPI app for webhook and status endpoint"""
    web_app = FastAPI(title="ShopSavvy Bot")
    
    # Mount static files
    web_app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @web_app.get("/")
    async def index(request: Request):
        """Main landing page"""
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "bot_username": app.bot.username}
        )
    
    @web_app.get("/status")
    async def status():
        """Health check endpoint"""
        return {
            "status": "running",
            "bot": app.bot.username,
            "webhook_set": app.updater is not None
        }
    
    @web_app.post(f"/{BOT_TOKEN}")
    async def telegram_webhook(request: Request):
        """Handle incoming Telegram updates"""
        json_data = await request.json()
        update = Update.de_json(json_data, app.bot)
        await app.process_update(update)
        return Response(status_code=200)
    
    return web_app

def main():
    """Main function to run the bot"""
    
    # Validate bot token
    if BOT_TOKEN == "TELEGRAM_BOT_TOKEN":
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
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
    app.add_handler(conversation_handler)
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('deals', deals_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    logger.info("🤖 ShopSavvy Bot is starting...")
    logger.info("🔍 Ready to help users find the best deals!")

    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8443))
            
    # Start the bot
    try:
        if 'RENDER' in os.environ or 'WEBHOOK' in os.environ:
            # Webhook configuration for production
            web_app = create_web_app(app)
            
            @web_app.on_event("startup")
            async def on_startup():
                await app.initialize()
                await app.start()
                webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
                await app.bot.set_webhook(webhook_url)
                logger.info(f"🌐 Webhook configured at {webhook_url}")
            
            uvicorn.run(
                web_app,
                host="0.0.0.0",
                port=port,
                ssl_certfile=None,
            )
        else:
            # Use polling for local development
            app.run_polling(
                allowed_updates=['message', 'callback_query'],
                drop_pending_updates=True
            )
            logger.info("🔌 Using polling method (local development)")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        logger.info("Make sure TELEGRAM_BOT_TOKEN is set correctly")

if __name__ == '__main__':
    main()
