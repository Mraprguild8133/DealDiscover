"""
Telegram bot handlers for ShopSavvy deal finder bot
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

from config import PLATFORM_SELECTION, PRODUCT_SEARCH, CATEGORY_SEARCH, DEAL_TYPE_SELECTION
from mock_data import search_products, MOCK_PRODUCTS
from utils import (
    format_deal_message, format_trending_deals, format_festival_deals,
    create_platform_keyboard, create_category_keyboard, 
    create_deal_type_keyboard, create_main_menu_keyboard, 
    get_product_link, create_product_link_keyboard
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🛍️ **Welcome to ShopSavvy!** 🛍️

I can help you find the best deals on:
🛒 Flipkart
📦 Amazon  
🛍️ Meesho
👗 Myntra

What would you like to do today?
    """
    
    keyboard = create_main_menu_keyboard()
    
    await update.message.reply_text(
        welcome_message.strip(),
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return PLATFORM_SELECTION

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🤖 **ShopSavvy Help** 🤖

**Commands:**
/start - Start the bot
/help - Show this help message
/deals - Browse trending deals

**How to use:**
1️⃣ Choose a platform or search all platforms
2️⃣ Search for products by name or browse categories
3️⃣ View deals with prices, discounts, and coupons
4️⃣ Get direct purchase links

**Features:**
🔍 Product search across platforms
📊 Price comparison
🎟️ Coupon codes and cashback info
🔥 Trending deals
🎉 Festival sale alerts

Need help? Just type your product name!
    """
    
    keyboard = create_main_menu_keyboard()
    
    await update.message.reply_text(
        help_text.strip(),
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def deals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /deals command"""
    trending_message = format_trending_deals()
    
    keyboard = create_main_menu_keyboard()
    
    await update.message.reply_text(
        trending_message,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('platform_'):
        platform = data.replace('platform_', '')
        context.user_data['selected_platform'] = platform
        
        await query.edit_message_text(
            f"✅ Selected: {platform.title() if platform != 'all' else 'All Platforms'}\n\n"
            f"Now, what product are you looking for?\n"
            f"💡 Try: smartphones, shirts, home appliances, electronics",
            parse_mode=ParseMode.MARKDOWN
        )
        return PRODUCT_SEARCH
    
    elif data == 'search_products':
        keyboard = create_platform_keyboard()
        await query.edit_message_text(
            "🏪 **Choose Platform** 🏪\n\n"
            "Would you like to search one platform or compare deals across all?",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return PLATFORM_SELECTION
    
    elif data == 'browse_categories':
        keyboard = create_category_keyboard()
        await query.edit_message_text(
            "📂 **Browse by Category** 📂\n\n"
            "Select a category to explore:",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return CATEGORY_SEARCH
    
    elif data.startswith('category_'):
        category = data.replace('category_', '').replace('_', ' ')
        context.user_data['selected_category'] = category
        
        keyboard = create_platform_keyboard()
        await query.edit_message_text(
            f"📂 **Category:** {category.title()}\n\n"
            f"🏪 **Choose Platform:**",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return PLATFORM_SELECTION
    
    elif data == 'trending_deals':
        trending_message = format_trending_deals()
        keyboard = create_main_menu_keyboard()
        
        await query.edit_message_text(
            trending_message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == 'festival_deals':
        festival_message = format_festival_deals()
        keyboard = create_main_menu_keyboard()
        
        await query.edit_message_text(
            festival_message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == 'help':
        help_text = """
🤖 **ShopSavvy Help** 🤖

**Commands:**
/start - Start the bot
/help - Show this help message
/deals - Browse trending deals

**How to use:**
1️⃣ Choose a platform or search all platforms
2️⃣ Search for products by name or browse categories
3️⃣ View deals with prices, discounts, and coupons
4️⃣ Get direct purchase links

**Features:**
🔍 Product search across platforms
📊 Price comparison
🎟️ Coupon codes and cashback info
🔥 Trending deals
🎉 Festival sale alerts

Need help? Just type your product name!
        """
        
        keyboard = create_main_menu_keyboard()
        
        await query.edit_message_text(
            help_text.strip(),
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data.startswith('dealtype_'):
        deal_type = data.replace('dealtype_', '').replace('_', ' ')
        
        await query.edit_message_text(
            f"✅ Looking for: {deal_type.title()}\n\n"
            f"This feature will be available in the next update! 🚀\n\n"
            f"For now, try searching for specific products.",
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_product_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle product search input"""
    query = update.message.text.lower().strip()
    platform = context.user_data.get('selected_platform', 'all')
    category = context.user_data.get('selected_category')
    
    # If category was selected, search within that category
    if category:
        search_query = category.lower()
    else:
        search_query = query
    
    await update.message.reply_text("🔍 Searching for deals... Please wait!")
    
    try:
        # Search products
        results = search_products(search_query, platform)
        
        if not results:
            keyboard = create_main_menu_keyboard()
            await update.message.reply_text(
                f"❌ Sorry, I couldn't find any offers matching '{search_query}'. "
                f"Try different keywords or check back later.\n\n"
                f"💡 **Suggestions:**\n"
                f"• Try broader terms like 'phone' instead of specific models\n"
                f"• Check spelling\n"
                f"• Browse categories instead",
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            return ConversationHandler.END
        
        # Send header message
        await update.message.reply_text(
            f"🎯 **Found {len(results)} deals for '{search_query}'**\n\nLet me show you the best deals:",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Send each product with image and shopping links
        for i, product in enumerate(results, 1):
            deal_message = format_deal_message(product, platform)
            product_keyboard = create_product_link_keyboard(product, platform)
            
            try:
                # Send photo with deal info and shopping buttons
                if product.get('image_url'):
                    await update.message.reply_photo(
                        photo=product['image_url'],
                        caption=f"**Deal {i}/{len(results)}**\n\n{deal_message}",
                        reply_markup=product_keyboard,
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    # Fallback to text message if no image
                    await update.message.reply_text(
                        f"**Deal {i}/{len(results)}**\n\n{deal_message}",
                        reply_markup=product_keyboard,
                        parse_mode=ParseMode.MARKDOWN
                    )
            except Exception as e:
                logger.error(f"Error sending image for {product['name']}: {e}")
                # Fallback to text message
                await update.message.reply_text(
                    f"**Deal {i}/{len(results)}**\n\n{deal_message}",
                    reply_markup=product_keyboard,
                    parse_mode=ParseMode.MARKDOWN
                )
        
        # Send final menu
        keyboard = create_main_menu_keyboard()
        await update.message.reply_text(
            "✅ **All deals shown!** What would you like to do next?",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Clear user data
        context.user_data.clear()
        
    except Exception as e:
        logger.error(f"Error in product search: {e}")
        keyboard = create_main_menu_keyboard()
        await update.message.reply_text(
            "❌ **Oops! Something went wrong** ❌\n\n"
            "Our deal-finding robots are taking a quick break. "
            "Please try again in a moment!\n\n"
            "💡 You can also try:\n"
            "• Different search terms\n"
            "• Browsing categories\n"
            "• Checking trending deals",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    return ConversationHandler.END

async def handle_invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle invalid input during conversation"""
    await update.message.reply_text(
        "❓ I didn't understand that. Please try again or use the menu buttons below.",
        reply_markup=create_main_menu_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation"""
    keyboard = create_main_menu_keyboard()
    await update.message.reply_text(
        "✅ **Operation cancelled**\n\nWhat would you like to do next?",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    
    context.user_data.clear()
    return ConversationHandler.END

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle direct text messages (product searches)"""
    query = update.message.text.lower().strip()
    
    # Skip if it's a command
    if query.startswith('/'):
        return
    
    await update.message.reply_text("🔍 Let me search for deals on that...")
    
    # Search across all platforms by default
    results = search_products(query, 'all')
    
    if not results:
        keyboard = create_main_menu_keyboard()
        await update.message.reply_text(
            f"❌ No deals found for '{query}'\n\n"
            f"💡 **Try:**\n"
            f"• More general terms (e.g., 'phone' instead of 'iPhone 15 Pro')\n"
            f"• Browse categories using the menu\n"
            f"• Check trending deals",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Send results with images
    for i, product in enumerate(results, 1):
        deal_message = format_deal_message(product, 'all')
        keyboard = create_main_menu_keyboard() if i == len(results) else None
        
        try:
            # Send photo with deal info
            if product.get('image_url'):
                await update.message.reply_photo(
                    photo=product['image_url'],
                    caption=f"**Result {i}/{len(results)}**\n\n{deal_message}",
                    reply_markup=keyboard,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Fallback to text message if no image
                await update.message.reply_text(
                    f"**Result {i}/{len(results)}**\n\n{deal_message}",
                    reply_markup=keyboard,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            logger.error(f"Error sending image for {product['name']}: {e}")
            # Fallback to text message
            await update.message.reply_text(
                f"**Result {i}/{len(results)}**\n\n{deal_message}",
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f'Update {update} caused error {context.error}')
    
    try:
        if update and hasattr(update, 'message') and update.message:
            from utils import create_main_menu_keyboard
            await update.message.reply_text(
                "❌ **Something went wrong!**\n\n"
                "Please try again or contact support if the issue persists.",
                reply_markup=create_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        elif update and hasattr(update, 'callback_query') and update.callback_query:
            await update.callback_query.answer("Something went wrong! Please try again.")
    except Exception as e:
        logger.error(f"Error in error handler: {e}")
