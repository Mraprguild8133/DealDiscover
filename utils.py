"""
Utility functions for the Telegram bot
"""
from datetime import datetime, timedelta
import random
from config import PLATFORM_EMOJIS
from mock_data import format_price, calculate_savings

def format_deal_message(product, platform=None):
    """Format a deal message for display"""
    message_parts = []
    
    if platform and platform != 'all':
        # Single platform deal
        deal = product['deals'].get(platform)
        if not deal:
            return f"❌ No deals found for {product['name']} on {platform.title()}"
        
        emoji = PLATFORM_EMOJIS.get(platform, '🛒')
        savings = calculate_savings(deal['original_price'], deal['discount_price'])
        
        message = f"""
{product['image']} **{product['name']}**
{emoji} **{platform.title()}**

💰 **Price:** ~~{format_price(deal['original_price'])}~~ → **{format_price(deal['discount_price'])}**
📊 **Discount:** {deal['discount']}% OFF
💸 **You Save:** {format_price(savings)}
🎟️ **Coupon:** {deal['coupon']}
💳 **Cashback:** {format_price(deal['cashback'])}
⏰ **Valid till:** {get_offer_validity()}
🚚 **Free Delivery:** Yes
🔗 **[Buy Now]({get_product_link(product['name'], platform)})**
        """
        return message.strip()
    
    else:
        # All platforms comparison
        message = f"{product['image']} **{product['name']}**\n\n"
        
        available_deals = [(p, d) for p, d in product['deals'].items() if d is not None]
        
        if not available_deals:
            return f"❌ No deals found for {product['name']}"
        
        # Sort by discount percentage
        available_deals.sort(key=lambda x: x[1]['discount'], reverse=True)
        
        for platform, deal in available_deals:
            emoji = PLATFORM_EMOJIS.get(platform, '🛒')
            savings = calculate_savings(deal['original_price'], deal['discount_price'])
            
            message += f"""
{emoji} **{platform.title()}**
💰 ~~{format_price(deal['original_price'])}~~ → **{format_price(deal['discount_price'])}**
📊 {deal['discount']}% OFF | 💸 Save {format_price(savings)}
🎟️ {deal['coupon']} | 💳 ₹{deal['cashback']} cashback

"""
        
        best_deal = available_deals[0]
        message += f"🏆 **Best Deal:** {best_deal[0].title()} with {best_deal[1]['discount']}% OFF"
        
        return message.strip()

def get_product_link(product_name, platform):
    """Generate product links for different platforms"""
    # Platform base URLs
    platform_urls = {
        'flipkart': 'https://www.flipkart.com/search?q=',
        'amazon': 'https://www.amazon.in/s?k=',
        'myntra': 'https://www.myntra.com/search?q=',
        'meesho': 'https://www.meesho.com/s/p/'
    }
    
    # Clean product name for URL
    search_term = product_name.replace(' ', '+').replace('"', '').replace("'", "")
    base_url = platform_urls.get(platform, 'https://www.google.com/search?q=')
    
    return f"{base_url}{search_term}"

def get_offer_validity():
    """Get a random offer validity date"""
    days_ahead = random.randint(5, 30)
    validity_date = datetime.now() + timedelta(days=days_ahead)
    return validity_date.strftime("%d %B %Y")

def create_product_link_keyboard(product, platform=None):
    """Create inline keyboard with product links"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = []
    
    if platform and platform != 'all':
        # Single platform - direct link
        if product['deals'].get(platform):
            link = get_product_link(product['name'], platform)
            keyboard.append([
                InlineKeyboardButton(
                    f"🛒 Shop on {platform.title()}", 
                    url=link
                )
            ])
    else:
        # Multiple platforms - show available links
        available_platforms = [p for p, d in product['deals'].items() if d is not None]
        
        # Create two buttons per row for better mobile display
        row = []
        for platform_name in available_platforms:
            link = get_product_link(product['name'], platform_name)
            button = InlineKeyboardButton(
                f"🛒 {platform_name.title()}", 
                url=link
            )
            row.append(button)
            
            # Add row when we have 2 buttons or it's the last platform
            if len(row) == 2 or platform_name == available_platforms[-1]:
                keyboard.append(row)
                row = []
    
    return InlineKeyboardMarkup(keyboard) if keyboard else None

def format_trending_deals():
    """Format trending deals message"""
    from mock_data import get_trending_deals
    
    trending = get_trending_deals()
    message = "🔥 **Today's Hottest Deals** 🔥\n\n"
    
    for i, deal in enumerate(trending, 1):
        emoji = PLATFORM_EMOJIS.get(deal['platform'], '🛒')
        message += f"{i}. {emoji} **{deal['product']}** - {deal['discount']}% OFF on {deal['platform'].title()}\n"
    
    message += f"\n📅 Updated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
    return message

def format_festival_deals():
    """Format festival deals message"""
    from mock_data import get_festival_deals
    
    festivals = get_festival_deals()
    message = "🎉 **Upcoming Sale Events** 🎉\n\n"
    
    for event, details in festivals.items():
        event_date = datetime.strptime(details['date'], '%Y-%m-%d')
        days_left = (event_date - datetime.now()).days
        
        if days_left > 0:
            platforms_str = ", ".join([p.title() for p in details['platforms']])
            message += f"📅 **{event}**\n"
            message += f"🗓️ {event_date.strftime('%d %B %Y')} ({days_left} days left)\n"
            message += f"🏪 Platforms: {platforms_str}\n"
            message += f"📝 {details['description']}\n\n"
    
    return message.strip() if message.strip() != "🎉 **Upcoming Sale Events** 🎉" else "No upcoming sales found."

def create_platform_keyboard():
    """Create inline keyboard for platform selection"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [
            InlineKeyboardButton(f"{PLATFORM_EMOJIS['flipkart']} Flipkart", callback_data='platform_flipkart'),
            InlineKeyboardButton(f"{PLATFORM_EMOJIS['amazon']} Amazon", callback_data='platform_amazon')
        ],
        [
            InlineKeyboardButton(f"{PLATFORM_EMOJIS['meesho']} Meesho", callback_data='platform_meesho'),
            InlineKeyboardButton(f"{PLATFORM_EMOJIS['myntra']} Myntra", callback_data='platform_myntra')
        ],
        [
            InlineKeyboardButton(f"{PLATFORM_EMOJIS['all']} All Platforms", callback_data='platform_all')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_category_keyboard():
    """Create inline keyboard for category selection"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from config import CATEGORIES
    
    keyboard = []
    for i in range(0, len(CATEGORIES), 2):
        row = []
        for j in range(2):
            if i + j < len(CATEGORIES):
                category = CATEGORIES[i + j]
                row.append(InlineKeyboardButton(category, callback_data=f'category_{category.lower().replace(" ", "_")}'))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)

def create_deal_type_keyboard():
    """Create inline keyboard for deal type selection"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from config import DEAL_TYPES
    
    keyboard = []
    for deal_type in DEAL_TYPES:
        keyboard.append([InlineKeyboardButton(deal_type, callback_data=f'dealtype_{deal_type.lower().replace(" ", "_")}')])
    
    return InlineKeyboardMarkup(keyboard)

def create_main_menu_keyboard():
    """Create main menu keyboard"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [
            InlineKeyboardButton("🔍 Search Products", callback_data='search_products'),
            InlineKeyboardButton("📂 Browse Categories", callback_data='browse_categories')
        ],
        [
            InlineKeyboardButton("🔥 Trending Deals", callback_data='trending_deals'),
            InlineKeyboardButton("🎉 Festival Sales", callback_data='festival_deals')
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data='help')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
