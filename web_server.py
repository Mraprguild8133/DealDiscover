#!/usr/bin/env python3
"""
Web Status Dashboard for Telegram Movie Bot

A Flask web server that provides a status dashboard showing the bot's
current status, statistics, and available commands.
"""

from flask import Flask, render_template, jsonify
import psutil
import os
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Store bot statistics
bot_stats = {
    'start_time': time.time(),
    'total_searches': 0,
    'active_users': set(),
    'images_sent': 0,
    'last_activity': None
}

@app.route('/')
def dashboard():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """API endpoint to get current bot status"""
    try:
        # Calculate uptime
        uptime_seconds = int(time.time() - bot_stats['start_time'])
        uptime_hours = uptime_seconds // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        uptime_secs = uptime_seconds % 60
        uptime_str = f"{uptime_hours}h {uptime_minutes}m {uptime_secs}s"
        
        # Get system stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        status_data = {
            'bot_status': 'online',
            'uptime': uptime_str,
            'last_update': datetime.now().isoformat(),
            'total_searches': bot_stats['total_searches'],
            'active_users': len(bot_stats['active_users']),
            'images_sent': bot_stats['images_sent'],
            'last_activity': bot_stats['last_activity'],
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': f"{memory.available // (1024**2)} MB"
            },
            'services': {
                'omdb_api': 'connected',
                'telegram_api': 'connected',
                'database': 'available',
                'image_upload': 'working'
            }
        }
        
        return jsonify(status_data)
        
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({
            'bot_status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/stats/increment/<stat_type>')
def increment_stat(stat_type):
    """API endpoint to increment statistics"""
    try:
        if stat_type == 'search':
            bot_stats['total_searches'] += 1
        elif stat_type == 'image':
            bot_stats['images_sent'] += 1
        
        bot_stats['last_activity'] = datetime.now().isoformat()
        
        return jsonify({'status': 'success', 'value': bot_stats.get(f'total_{stat_type}s', 0)})
        
    except Exception as e:
        logger.error(f"Error incrementing stat {stat_type}: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/stats/user/<user_id>')
def track_user(user_id):
    """API endpoint to track active users"""
    try:
        bot_stats['active_users'].add(user_id)
        bot_stats['last_activity'] = datetime.now().isoformat()
        
        return jsonify({
            'status': 'success', 
            'active_users': len(bot_stats['active_users'])
        })
        
    except Exception as e:
        logger.error(f"Error tracking user {user_id}: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': int(time.time() - bot_stats['start_time'])
    })

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting web dashboard on port {port}")
    logger.info("Dashboard will be available at: http://localhost:5000")
    
    # Start the Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
      )
