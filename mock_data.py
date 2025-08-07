"""
Mock data for e-commerce deals across Indian platforms
"""
import random
from datetime import datetime, timedelta

# Mock product database
MOCK_PRODUCTS = {
    'mobile': [
        {
            'name': 'iPhone 15 Pro',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 134900, 'discount_price': 119900, 'discount': 11, 'coupon': 'FLIP10', 'cashback': 2000},
                'amazon': {'original_price': 134900, 'discount_price': 122900, 'discount': 9, 'coupon': 'PRIME5', 'cashback': 1500},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'Samsung Galaxy S24',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 79999, 'discount_price': 69999, 'discount': 13, 'coupon': 'SAMSUNG15', 'cashback': 1000},
                'amazon': {'original_price': 79999, 'discount_price': 71999, 'discount': 10, 'coupon': 'GALAXY10', 'cashback': 800},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'OnePlus 12',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 64999, 'discount_price': 58999, 'discount': 9, 'coupon': 'ONEPLUS10', 'cashback': 500},
                'amazon': {'original_price': 64999, 'discount_price': 57999, 'discount': 11, 'coupon': 'NEVER10', 'cashback': 700},
                'myntra': None,
                'meesho': {'original_price': 64999, 'discount_price': 59999, 'discount': 8, 'coupon': 'MEESHO5', 'cashback': 300}
            }
        },
        {
            'name': 'Xiaomi 14 Pro',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1592286286633-d9baacccb064?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 52999, 'discount_price': 47999, 'discount': 9, 'coupon': 'XIAOMI10', 'cashback': 1500},
                'amazon': {'original_price': 52999, 'discount_price': 48999, 'discount': 8, 'coupon': 'MI15', 'cashback': 1200},
                'myntra': None,
                'meesho': {'original_price': 52999, 'discount_price': 49999, 'discount': 6, 'coupon': 'PHONE5', 'cashback': 800}
            }
        },
        {
            'name': 'Vivo V30 Pro',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 41999, 'discount_price': 37999, 'discount': 10, 'coupon': 'VIVO12', 'cashback': 1000},
                'amazon': {'original_price': 41999, 'discount_price': 38999, 'discount': 7, 'coupon': 'CAMERA10', 'cashback': 800},
                'myntra': None,
                'meesho': {'original_price': 41999, 'discount_price': 39999, 'discount': 5, 'coupon': 'SELFIE5', 'cashback': 500}
            }
        }
    ],
    'smartphones': [
        {
            'name': 'iPhone 15 Pro',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 134900, 'discount_price': 119900, 'discount': 11, 'coupon': 'FLIP10', 'cashback': 2000},
                'amazon': {'original_price': 134900, 'discount_price': 122900, 'discount': 9, 'coupon': 'PRIME5', 'cashback': 1500},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'Samsung Galaxy S24',
            'category': 'Electronics',
            'image': '📱',
            'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 79999, 'discount_price': 69999, 'discount': 13, 'coupon': 'SAMSUNG15', 'cashback': 1000},
                'amazon': {'original_price': 79999, 'discount_price': 71999, 'discount': 10, 'coupon': 'GALAXY10', 'cashback': 800},
                'myntra': None,
                'meesho': None
            }
        }
    ],
    'television': [
        {
            'name': 'Samsung 55" 4K QLED Smart TV',
            'category': 'Electronics',
            'image': '📺',
            'image_url': 'https://images.unsplash.com/photo-1567690187548-f07b1d7bf5a9?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 89999, 'discount_price': 74999, 'discount': 17, 'coupon': 'TV20', 'cashback': 3000},
                'amazon': {'original_price': 89999, 'discount_price': 76999, 'discount': 14, 'coupon': 'SMART15', 'cashback': 2500},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'LG 43" 4K UHD Smart TV',
            'category': 'Electronics',
            'image': '📺',
            'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 49999, 'discount_price': 39999, 'discount': 20, 'coupon': 'LG25', 'cashback': 2000},
                'amazon': {'original_price': 49999, 'discount_price': 41999, 'discount': 16, 'coupon': 'UHD20', 'cashback': 1800},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'Sony Bravia 65" OLED TV',
            'category': 'Electronics',
            'image': '📺',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 199999, 'discount_price': 164999, 'discount': 18, 'coupon': 'OLED25', 'cashback': 8000},
                'amazon': {'original_price': 199999, 'discount_price': 169999, 'discount': 15, 'coupon': 'SONY20', 'cashback': 7000},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'Mi 32" HD Smart TV',
            'category': 'Electronics',
            'image': '📺',
            'image_url': 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 19999, 'discount_price': 14999, 'discount': 25, 'coupon': 'MI30', 'cashback': 1000},
                'amazon': {'original_price': 19999, 'discount_price': 15999, 'discount': 20, 'coupon': 'BUDGET25', 'cashback': 800},
                'myntra': None,
                'meesho': {'original_price': 19999, 'discount_price': 16999, 'discount': 15, 'coupon': 'TV15', 'cashback': 500}
            }
        }
    ],
    'shirt': [
        {
            'name': 'Tommy Hilfiger Cotton Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 2999, 'discount_price': 1799, 'discount': 40, 'coupon': 'FASHION50', 'cashback': 100},
                'amazon': {'original_price': 2999, 'discount_price': 1899, 'discount': 37, 'coupon': 'STYLE30', 'cashback': 80},
                'myntra': {'original_price': 2999, 'discount_price': 1699, 'discount': 43, 'coupon': 'MYNTRA40', 'cashback': 120},
                'meesho': {'original_price': 2999, 'discount_price': 1999, 'discount': 33, 'coupon': 'SHIRT25', 'cashback': 60}
            }
        },
        {
            'name': 'Levi\'s Denim Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 3499, 'discount_price': 2099, 'discount': 40, 'coupon': 'DENIM50', 'cashback': 150},
                'amazon': {'original_price': 3499, 'discount_price': 2199, 'discount': 37, 'coupon': 'LEVIS30', 'cashback': 100},
                'myntra': {'original_price': 3499, 'discount_price': 1999, 'discount': 43, 'coupon': 'MYNTRA45', 'cashback': 180},
                'meesho': None
            }
        },
        {
            'name': 'Peter England Formal Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 1999, 'discount_price': 1199, 'discount': 40, 'coupon': 'FORMAL50', 'cashback': 80},
                'amazon': {'original_price': 1999, 'discount_price': 1299, 'discount': 35, 'coupon': 'OFFICE40', 'cashback': 70},
                'myntra': {'original_price': 1999, 'discount_price': 1099, 'discount': 45, 'coupon': 'MYNTRA45', 'cashback': 100},
                'meesho': {'original_price': 1999, 'discount_price': 1399, 'discount': 30, 'coupon': 'WORK30', 'cashback': 50}
            }
        },
        {
            'name': 'Van Heusen Casual Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 2499, 'discount_price': 1749, 'discount': 30, 'coupon': 'VH35', 'cashback': 120},
                'amazon': {'original_price': 2499, 'discount_price': 1849, 'discount': 26, 'coupon': 'CASUAL30', 'cashback': 100},
                'myntra': {'original_price': 2499, 'discount_price': 1649, 'discount': 34, 'coupon': 'WEEKEND35', 'cashback': 150},
                'meesho': None
            }
        },
        {
            'name': 'Arrow Sports Polo Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 1799, 'discount_price': 1259, 'discount': 30, 'coupon': 'POLO35', 'cashback': 90},
                'amazon': {'original_price': 1799, 'discount_price': 1349, 'discount': 25, 'coupon': 'SPORT30', 'cashback': 75},
                'myntra': {'original_price': 1799, 'discount_price': 1199, 'discount': 33, 'coupon': 'ARROW35', 'cashback': 120},
                'meesho': {'original_price': 1799, 'discount_price': 1439, 'discount': 20, 'coupon': 'ACTIVE20', 'cashback': 60}
            }
        }
    ],
    'shirts': [
        {
            'name': 'Tommy Hilfiger Cotton Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 2999, 'discount_price': 1799, 'discount': 40, 'coupon': 'FASHION50', 'cashback': 100},
                'amazon': {'original_price': 2999, 'discount_price': 1899, 'discount': 37, 'coupon': 'STYLE30', 'cashback': 80},
                'myntra': {'original_price': 2999, 'discount_price': 1699, 'discount': 43, 'coupon': 'MYNTRA40', 'cashback': 120},
                'meesho': {'original_price': 2999, 'discount_price': 1999, 'discount': 33, 'coupon': 'SHIRT25', 'cashback': 60}
            }
        },
        {
            'name': 'Levi\'s Denim Shirt',
            'category': 'Fashion',
            'image': '👔',
            'image_url': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 3499, 'discount_price': 2099, 'discount': 40, 'coupon': 'DENIM50', 'cashback': 150},
                'amazon': {'original_price': 3499, 'discount_price': 2199, 'discount': 37, 'coupon': 'LEVIS30', 'cashback': 100},
                'myntra': {'original_price': 3499, 'discount_price': 1999, 'discount': 43, 'coupon': 'MYNTRA45', 'cashback': 180},
                'meesho': None
            }
        }
    ],
    'home appliances': [
        {
            'name': 'LG 1.5 Ton AC',
            'category': 'Home & Kitchen',
            'image': '❄️',
            'image_url': 'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 45999, 'discount_price': 39999, 'discount': 13, 'coupon': 'AC15', 'cashback': 2000},
                'amazon': {'original_price': 45999, 'discount_price': 41999, 'discount': 9, 'coupon': 'COOL10', 'cashback': 1500},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'Samsung Front Load Washing Machine',
            'category': 'Home & Kitchen',
            'image': '🧺',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 32999, 'discount_price': 27999, 'discount': 15, 'coupon': 'WASH20', 'cashback': 1200},
                'amazon': {'original_price': 32999, 'discount_price': 28999, 'discount': 12, 'coupon': 'CLEAN15', 'cashback': 1000},
                'myntra': None,
                'meesho': None
            }
        }
    ],
    'electronics': [
        {
            'name': 'Sony WH-1000XM5 Headphones',
            'category': 'Electronics',
            'image': '🎧',
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 29990, 'discount_price': 24990, 'discount': 17, 'coupon': 'AUDIO20', 'cashback': 800},
                'amazon': {'original_price': 29990, 'discount_price': 25990, 'discount': 13, 'coupon': 'SONY15', 'cashback': 600},
                'myntra': None,
                'meesho': None
            }
        },
        {
            'name': 'MacBook Air M2',
            'category': 'Electronics',
            'image': '💻',
            'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop',
            'deals': {
                'flipkart': {'original_price': 114900, 'discount_price': 104900, 'discount': 9, 'coupon': 'MAC10', 'cashback': 3000},
                'amazon': {'original_price': 114900, 'discount_price': 107900, 'discount': 6, 'coupon': 'APPLE5', 'cashback': 2500},
                'myntra': None,
                'meesho': None
            }
        }
    ]
}

# Trending deals
TRENDING_DEALS = [
    {'product': 'Mi 32" HD Smart TV', 'platform': 'flipkart', 'discount': 25},
    {'product': 'iPhone 15 Pro', 'platform': 'flipkart', 'discount': 11},
    {'product': 'Peter England Formal Shirt', 'platform': 'myntra', 'discount': 45},
    {'product': 'Samsung 55" 4K QLED Smart TV', 'platform': 'flipkart', 'discount': 17},
    {'product': 'Xiaomi 14 Pro', 'platform': 'flipkart', 'discount': 9},
    {'product': 'Arrow Sports Polo Shirt', 'platform': 'myntra', 'discount': 33},
    {'product': 'Sony Bravia 65" OLED TV', 'platform': 'flipkart', 'discount': 18}
]

# Festival specials
FESTIVAL_DEALS = {
    'Big Billion Days': {'date': '2025-10-15', 'platforms': ['flipkart'], 'description': 'Flipkart\'s biggest sale of the year'},
    'Great Indian Festival': {'date': '2025-10-20', 'platforms': ['amazon'], 'description': 'Amazon\'s mega sale event'},
    'Diwali Sale': {'date': '2025-11-01', 'platforms': ['flipkart', 'amazon', 'myntra', 'meesho'], 'description': 'Festival of lights special offers'},
    'End of Reason Sale': {'date': '2025-12-26', 'platforms': ['myntra'], 'description': 'Myntra\'s year-end fashion sale'}
}

def search_products(query, platform=None):
    """Search for products based on query and platform"""
    results = []
    query_lower = query.lower()
    
    for category, products in MOCK_PRODUCTS.items():
        if query_lower in category or any(query_lower in product['name'].lower() for product in products):
            for product in products:
                if query_lower in product['name'].lower() or query_lower in category:
                    if platform and platform != 'all':
                        if product['deals'].get(platform):
                            results.append({**product, 'platform_filter': platform})
                    else:
                        results.append(product)
    
    return results[:5]  # Limit to 5 results

def get_trending_deals():
    """Get trending deals"""
    return TRENDING_DEALS

def get_festival_deals():
    """Get upcoming festival deals"""
    return FESTIVAL_DEALS

def format_price(price):
    """Format price in Indian currency format"""
    return f"₹{price:,}"

def calculate_savings(original, discounted):
    """Calculate savings amount"""
    return original - discounted
