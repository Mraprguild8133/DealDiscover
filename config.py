"""
Configuration file for the Telegram bot
"""
import os
import logging

# Bot configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")

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
