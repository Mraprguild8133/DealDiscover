#!/usr/bin/env python3
"""
Combined startup script for Telegram Movie Bot and Web Dashboard

This script starts both the Telegram bot and the web dashboard in separate processes,
allowing users to monitor the bot status through a web interface.
"""

import os
import sys
import time
import signal
import logging
import threading
import subprocess
from multiprocessing import Process

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)

def run_telegram_bot():
    """Run the Telegram bot"""
    try:
        logger.info("Starting Telegram Movie Bot...")
        from main import main
        main()
    except Exception as e:
        logger.error(f"Error running Telegram bot: {str(e)}")
        sys.exit(1)

def run_web_dashboard():
    """Run the web dashboard"""
    try:
        logger.info("Starting Web Dashboard...")
        from web_server import app
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Error running web dashboard: {str(e)}")
        sys.exit(1)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Received shutdown signal, stopping services...")
    sys.exit(0)

def main():
    """Main function to start both services"""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check required environment variables
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    logger.info("All required environment variables found")
    logger.info("Starting Telegram Movie Bot with Web Dashboard...")
    
    try:
        # Start web dashboard in a separate thread
        dashboard_thread = threading.Thread(target=run_web_dashboard, daemon=True)
        dashboard_thread.start()
        
        # Give dashboard time to start
        time.sleep(2)
        logger.info("Web Dashboard started successfully")
        logger.info("Dashboard available at: http://localhost:5000")
        
        # Run Telegram bot in main thread
        run_telegram_bot()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
