"""
ShopSavvy Bot Configuration (Render.com compatible)
Complete configuration with all required settings
"""

import os
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ======================
# Core Bot Configuration
# ======================
class BotConfig:
    TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    NAME: str = os.getenv("BOT_NAME", "ShopSavvy")
    ADMIN_IDS: List[int] = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    MAINTENANCE: bool = os.getenv("MAINTENANCE", "False").lower() == "true"

# ======================
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

# ======================
# Database Configuration
# ======================
class DatabaseConfig:
    URL: str = os.getenv("DATABASE_URL", "sqlite:///deals.db")
    ECHO: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))

# ======================
# E-commerce Platforms
# ======================
PLATFORMS: Dict[str, Dict[str, str]] = {
    'flipkart': {
        'name': 'Flipkart',
        'emoji': '🛒',
        'base_url': 'https://www.flipkart.com'
    },
    'amazon': {
        'name': 'Amazon',
        'emoji': '📦',
        'base_url': 'https://www.amazon.in'
    },
    'meesho': {
        'name': 'Meesho',
        'emoji': '🛍️',
        'base_url': 'https://www.meesho.com'
    },
    'myntra': {
        'name': 'Myntra',
        'emoji': '👗',
        'base_url': 'https://www.myntra.com'
    }
}

# ======================
# Product Categories
# ======================
CATEGORIES: Dict[str, List[str]] = {
    'electronics': ['Mobile', 'Laptop', 'Tablet', 'Camera', 'Headphones'],
    'fashion': ['Shirt', 'Jeans', 'Dress', 'Shoes', 'Watch'],
    'home': ['Furniture', 'Appliances', 'Decor', 'Kitchenware'],
    'beauty': ['Skincare', 'Makeup', 'Haircare', 'Fragrance']
}

# ======================
# Deal Types
# ======================
DEAL_TYPES: Dict[str, str] = {
    'percentage': 'Percentage Discount',
    'bogo': 'Buy One Get One',
    'cashback': 'Cashback Offer',
    'clearance': 'Clearance Sale',
    'festival': 'Festival Special'
}

# ======================
# Conversation States
# ======================
class States:
    (
        START,
        PLATFORM_SELECTION,
        PRODUCT_SEARCH,
        CATEGORY_SELECTION,
        DEAL_TYPE_SELECTION,
        PRICE_ALERT_SETUP,
        FEEDBACK,
        ADMIN_PANEL
    ) = range(8)

# ======================
# Logging Configuration
# ======================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if BotConfig.DEBUG else logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('shopsavvy.log')
    ]
)
logger = logging.getLogger(__name__)

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
