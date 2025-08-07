# ShopSavvy - Telegram Deal Finder Bot

## Overview

ShopSavvy is a Telegram bot that helps users find and compare deals across major Indian e-commerce platforms including Flipkart, Amazon, Meesho, and Myntra. The bot provides an interactive interface for product search, category browsing, and deal comparison, making it easy for users to find the best prices and offers across multiple platforms.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework Architecture
The application is built using the python-telegram-bot library, implementing a conversation-based interaction pattern. The architecture follows a modular design with clear separation of concerns across different components.

### Conversation Flow Design
The bot uses Telegram's ConversationHandler to manage multi-step user interactions. The conversation states include platform selection, product search, category browsing, and deal type filtering. This approach provides a guided user experience while maintaining context throughout the interaction.

### Data Management Strategy
The system currently uses mock data stored in Python dictionaries to simulate real e-commerce data. Product information includes pricing details, discount percentages, coupon codes, cashback offers, and product images for each platform. The data is organized into specific categories including dedicated sections for Mobile phones, Televisions, and Shirts with extensive product variety:

- **Mobile Category**: iPhone, Samsung, OnePlus, Xiaomi, Vivo models with platform-specific deals
- **Television Category**: Smart TVs from Samsung, LG, Sony, Mi with 4K/OLED options
- **Shirt Category**: Fashion brands like Tommy Hilfiger, Levi's, Peter England, Van Heusen, Arrow

Each product includes high-quality product images from Unsplash that are sent as photo messages with deal information. This design allows for easy testing and development before integrating with real APIs.

### Message Formatting System
A utility-based approach handles message formatting with platform-specific emojis and consistent pricing display. The formatting system creates rich, readable messages with markdown support and now includes high-quality product images sent via Telegram's photo message feature. Each deal is displayed with an accompanying product image for enhanced visual appeal and better user experience.

### Error Handling and Logging
The application implements comprehensive logging using Python's logging module and includes error handlers for graceful failure management. This ensures reliable operation and easier debugging.

### Modular Component Design
The codebase is organized into distinct modules:
- `main.py` - Application entry point and bot configuration
- `bot_handlers.py` - User interaction handlers and conversation logic
- `utils.py` - Message formatting and utility functions
- `mock_data.py` - Product and deal data simulation
- `config.py` - Configuration constants and environment settings

## External Dependencies

### Telegram Bot API
Primary integration with Telegram's Bot API through the python-telegram-bot library for all user interactions, message handling, and inline keyboard functionality.

### Environment Configuration
Uses environment variables for sensitive configuration like bot tokens, allowing for secure deployment across different environments.

### Python Standard Libraries
Leverages Python's built-in logging, datetime, and random modules for core functionality without additional external dependencies.

### Deployment Architecture
The bot supports multiple deployment modes:
- **Local Development**: Polling mode using `main.py` for testing and development
- **Production Deployment**: Webhook mode using `render_main.py` with Flask web server for Render.com
- **Docker Support**: Containerized deployment with proper health checks and port configuration
- **Render.com Integration**: Automatic webhook setup, health monitoring, and environment-based configuration switching

### Future Integration Points
The architecture is designed to accommodate future integrations with:
- Real e-commerce platform APIs (Flipkart, Amazon, Meesho, Myntra)
- Database systems for user preferences and deal caching
- Web scraping services for real-time price monitoring
- Notification services for price alerts