"""
Configuration file for the Telegram bot (Render.com compatible)
"""
import os
import logging

# ======================
# Bot Configuration
# ======================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WEBAPP_HOST = "0.0.0.0"  # Required for Render.com
WEBAPP_PORT = int(os.getenv("PORT", 10000))  # Render provides PORT environment variable

# Webhook Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # Set this in Render.com environment variables
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"  # Unique path for your webhook
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}" if WEBHOOK_URL else ""

# ======================
# Logging Configuration
# ======================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======================
# Conversation States
# ======================
(PLATFORM_SELECTION, PRODUCT_SEARCH, CATEGORY_SEARCH, 
 DEAL_TYPE_SELECTION, PRICE_ALERT) = range(5)

# ======================
# Platform Configuration
# ======================
PLATFORM_EMOJIS = {
    'flipkart': '🛒',
    'amazon': '📦',
    'meesho': '🛍️',
    'myntra': '👗',
    'all': '🔍'
}

CATEGORIES = [
    'Mobile', 'Television', 'Shirt', 'Electronics', 'Fashion', 
    'Home & Kitchen', 'Books', 'Sports & Fitness', 
    'Beauty & Personal Care', 'Automotive'
]

DEAL_TYPES = [
    'Percentage Discounts', 'BOGO Offers', 'Bank Discounts', 
    'Clearance Sales', 'Cashback Offers'
]

# ======================
# Database Configuration
# ======================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///deals.db")  # For Render PostgreSQL

# ======================
# Deployment Checks
# ======================
def check_config():
    """Validate essential configuration"""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        raise ValueError("Telegram bot token is required")
    
    if WEBHOOK_URL and not WEBHOOK_URL.startswith(('http://', 'https://')):
        logger.error("Invalid WEBHOOK_URL format")
        raise ValueError("WEBHOOK_URL must start with http:// or https://")

# Validate on import
check_config()
