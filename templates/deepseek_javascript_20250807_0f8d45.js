const express = require('express');
const WebSocket = require('ws');
const http = require('http');
const axios = require('axios');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const PORT = process.env.PORT || 3000;
const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;

// Store connected clients
const clients = new Set();

// WebSocket connection handler
wss.on('connection', (ws) => {
    console.log('New WebSocket connection');
    clients.add(ws);
    
    // Send initial data
    sendInitialData(ws);
    
    // Handle messages from client
    ws.on('message', (message) => {
        console.log('Received:', message);
        const data = JSON.parse(message);
        
        if (data.type === 'request') {
            if (data.data === 'status') {
                checkBotStatus().then(status => {
                    ws.send(JSON.stringify({
                        type: 'status',
                        status: status.bot,
                        webhook: status.webhook
                    }));
                });
            }
        }
    });
    
    // Handle disconnection
    ws.on('close', () => {
        console.log('Client disconnected');
        clients.delete(ws);
    });
});

// Function to send initial data to client
function sendInitialData(ws) {
    // Get initial stats (in a real app, this would come from your database)
    const stats = {
        type: 'stats',
        totalUsers: 1428,
        activeToday: 217,
        searches: 5843,
        alerts: 326
    };
    
    ws.send(JSON.stringify(stats));
    
    // Get bot status
    checkBotStatus().then(status => {
        ws.send(JSON.stringify({
            type: 'status',
            status: status.bot,
            webhook: status.webhook
        }));
    });
}

// Check bot and webhook status
async function checkBotStatus() {
    try {
        // Check bot status
        const botResponse = await axios.get(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/getMe`);
        const botStatus = botResponse.data.ok ? 'online' : 'offline';
        
        // Check webhook status
        const webhookResponse = await axios.get(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/getWebhookInfo`);
        const webhookStatus = webhookResponse.data.ok && webhookResponse.data.result.url;
        
        return { bot: botStatus, webhook: !!webhookStatus };
    } catch (error) {
        console.error('Error checking bot status:', error);
        return { bot: 'error', webhook: false };
    }
}

// Simulate real-time updates (in a real app, this would come from your Telegram bot)
function simulateUpdates() {
    setInterval(() => {
        // Generate random activity
        const activities = [
            { action: 'New user registered', details: '@shopper123' },
            { action: 'Product search', details: 'wireless headphones' },
            { action: 'Price comparison', details: 'iPhone 13 vs iPhone 14' },
            { action: 'User feedback', details: '⭐️⭐️⭐️⭐️⭐️' }
        ];
        
        const randomActivity = activities[Math.floor(Math.random() * activities.length)];
        
        // Broadcast to all clients
        clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({
                    type: 'activity',
                    ...randomActivity,
                    timestamp: new Date().toISOString()
                }));
            }
        });
    }, 5000);
    
    // Simulate price alerts
    setInterval(() => {
        const products = [
            { name: 'iPhone 13', oldPrice: 69900, newPrice: 64900 },
            { name: 'Sony WH-1000XM4', oldPrice: 28990, newPrice: 24990 },
            { name: 'MacBook Air M1', oldPrice: 89900, newPrice: 84900 }
        ];
        
        const randomProduct = products[Math.floor(Math.random() * products.length)];
        const difference = Math.round(((randomProduct.newPrice - randomProduct.oldPrice) / randomProduct.oldPrice) * 100);
        
        clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({
                    type: 'priceAlert',
                    product: randomProduct.name,
                    oldPrice: randomProduct.oldPrice,
                    newPrice: randomProduct.newPrice,
                    difference: difference,
                    timestamp: new Date().toISOString()
                }));
            }
        });
    }, 10000);
}

// Start the server
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    simulateUpdates();
});