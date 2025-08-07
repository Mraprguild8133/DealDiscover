"""
Configuration file for the Telegram bot
"""
import os
import logging

# Bot configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")

# Server Configuration
# ======================
class ServerConfig:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "10000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

# ======================
# Webhook Configuration
# ======================
class WebhookConfig:
    URL: str = os.getenv("WEBHOOK_URL", "")
    PATH: str = f"/webhook/{BotConfig.TOKEN}"
    FULL_URL: str = f"{URL}{PATH}" if URL else ""
    SECRET: Optional[str] = os.getenv("WEBHOOK_SECRET")
    
# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conversation states
(PLATFORM_SELECTION, PRODUCT_SEARCH, CATEGORY_SEARCH, 
 DEAL_TYPE_SELECTION, PRICE_ALERT) = range(5)

# Platform emojis
PLATFORM_EMOJIS = {
    'flipkart': '🛒',
    'amazon': '📦',
    'meesho': '🛍️',
    'myntra': '👗',
    'all': '🔍'
}

# Categories
CATEGORIES = [
    'Mobile', 'Television', 'Shirt', 'Electronics', 'Fashion', 
    'Home & Kitchen', 'Books', 'Sports & Fitness', 
    'Beauty & Personal Care', 'Automotive'
]

# Deal types
DEAL_TYPES = [
    'Percentage Discounts', 'BOGO Offers', 'Bank Discounts', 
    'Clearance Sales', 'Cashback Offers'
]
# ======================
# Configuration Validation
# ======================
def validate_config():
    """Validate all required configurations"""
    if not BotConfig.TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is required!")
        raise ValueError("Telegram bot token not configured")
    
    if WebhookConfig.URL and not WebhookConfig.URL.startswith(('http://', 'https://')):
        logger.error("Invalid WEBHOOK_URL format")
        raise ValueError("WEBHOOK_URL must start with http:// or https://")
    
    logger.info("Configuration validated successfully")

validate_config()
