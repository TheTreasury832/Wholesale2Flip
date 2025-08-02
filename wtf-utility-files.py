# database_init.py
"""
Database initialization and seeding script for WTF Platform
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for testing the platform"""
    conn = sqlite3.connect('wtf_platform.db')
    cursor = conn.cursor()
    
    # Sample buyers
    sample_buyers = [
        ('John Smith', 'john.smith@investor.com', '(555) 123-4567', 'single_family,multi_family', 
         100000, 300000, 'TX,OK', 'Dallas,Houston,Austin', 'cash,creative', 1, 1),
        ('Sarah Johnson', 'sarah@realtyinvest.com', '(555) 234-5678', 'single_family,condo',
         150000, 400000, 'TX,AR', 'Dallas,Fort Worth', 'cash', 1, 1),
        ('Mike Davis', 'mike.davis@properties.com', '(555) 345-6789', 'multi_family',
         200000, 500000, 'TX', 'Dallas', 'cash,subject_to', 1, 0),
        ('Lisa Wilson', 'lisa@buyhold.com', '(555) 456-7890', 'single_family',
         75000, 200000, 'TX,LA', 'Dallas,San Antonio', 'creative', 0, 0),
        ('Robert Chen', 'robert@fastcash.com', '(555) 567-8901', 'single_family,townhouse',
         120000, 350000, 'TX,NM', 'Austin,El Paso', 'cash', 1, 1),
    ]
    
    for buyer in sample_buyers:
        buyer_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO buyers (id, name, email, phone, property_types, min_price, max_price, 
                              states, cities, deal_types, verified, proof_of_funds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (buyer_id,) + buyer)
    
    # Sample properties
    sample_properties = [
        ('123 Main Street', 'Dallas', 'TX', '75201', 'single_family', 3, 2.0, 1800, 1995, 185000),
        ('456 Oak Avenue', 'Houston', 'TX', '77001', 'single_family', 4, 2.5, 2200, 1988, 220000),
        ('789 Pine Road', 'Austin', 'TX', '73301', 'multi_family', 6, 4.0, 3200, 1975, 280000),
        ('321 Elm Street', 'San Antonio', 'TX', '78201', 'single_family', 3, 2.0, 1650, 2001, 165000),
        ('654 Maple Drive', 'Fort Worth', 'TX', '76101', 'townhouse', 3, 2.5, 1900, 1992, 195000),
    ]
    
    for prop in sample_properties:
        property_id = str(uuid.uuid4())
        # Calculate sample analysis values
        arv = prop[9] * random.uniform(1.15, 1.35)  # ARV 15-35% higher than list price
        rehab_cost = random.randint(15000, 45000)
        max_offer = (arv * 0.7) - rehab_cost
        profit_potential = arv - max_offer - rehab_cost
        
        cursor.execute('''
            INSERT INTO properties (id, address, city, state, zip_code, property_type, 
                                  bedrooms, bathrooms, square_feet, year_built, list_price,
                                  arv, rehab_cost, max_offer, profit_potential)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (property_id,) + prop + (arv, rehab_cost, max_offer, profit_potential))
    
    # Sample leads
    sample_leads = [
        ('Maria', 'Garcia', '(555) 111-2222', 'maria.garcia@email.com', '100 First Street, Dallas, TX',
         'Divorce,Financial hardship', 'ASAP', 'cold_calling', 'contacted', 85),
        ('David', 'Brown', '(555) 222-3333', 'david.brown@email.com', '200 Second Ave, Houston, TX',
         'Job relocation', '30-60 days', 'direct_mail', 'interested', 72),
        ('Jennifer', 'Lee', '(555) 333-4444', 'jen.lee@email.com', '300 Third Blvd, Austin, TX',
         'Inherited property', '60-90 days', 'referral', 'new', 68),
        ('Thomas', 'Anderson', '(555) 444-5555', 'tom.anderson@email.com', '400 Fourth St, San Antonio, TX',
         'Tired landlord', 'Flexible', 'seo', 'callback', 55),
    ]
    
    for lead in sample_leads:
        lead_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO leads (id, first_name, last_name, phone, email, property_address,
                             motivation, timeline, source, status, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (lead_id,) + lead)
    
    conn.commit()
    conn.close()
    print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()

# utils.py
"""
Utility functions for the WTF Platform
"""

import hashlib
import uuid
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import sqlite3

def generate_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    pattern = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return re.match(pattern, phone) is not None

def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"${amount:,.0f}"

def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.1f}%"

def calculate_roi(profit: float, investment: float) -> float:
    """Calculate Return on Investment"""
    if investment == 0:
        return 0
    return (profit / investment) * 100

def calculate_cap_rate(noi: float, property_value: float) -> float:
    """Calculate Cap Rate"""
    if property_value == 0:
        return 0
    return (noi / property_value) * 100

def calculate_cash_flow(rent: float, mortgage: float, taxes: float, insurance: float, maintenance: float = 0) -> float:
    """Calculate monthly cash flow"""
    return rent - mortgage - taxes - insurance - maintenance

def days_between_dates(date1: datetime, date2: datetime) -> int:
    """Calculate days between two dates"""
    return abs((date2 - date1).days)

def get_property_age(year_built: int) -> int:
    """Calculate property age"""
    current_year = datetime.now().year
    return current_year - year_built

def estimate_arv_confidence(comps_count: int, days_old: int) -> int:
    """Estimate confidence level for ARV calculation"""
    base_confidence = 70
    
    # Add confidence based on number of comps
    comp_bonus = min(comps_count * 5, 20)
    
    # Reduce confidence based on age of comps
    age_penalty = max(days_old // 30 * 2, 0)  # 2% per month old
    
    confidence = base_confidence + comp_bonus - age_penalty
    return max(min(confidence, 100), 30)  # Cap between 30-100%

def parse_address(full_address: str) -> Dict[str, str]:
    """Parse a full address into components"""
    # Simple address parsing - in production, use a proper address API
    parts = full_address.split(',')
    
    address_parts = {
        'street': parts[0].strip() if len(parts) > 0 else '',
        'city': parts[1].strip() if len(parts) > 1 else '',
        'state': '',
        'zip_code': ''
    }
    
    if len(parts) > 2:
        state_zip = parts[2].strip().split()
        address_parts['state'] = state_zip[0] if len(state_zip) > 0 else ''
        address_parts['zip_code'] = state_zip[1] if len(state_zip) > 1 else ''
    
    return address_parts

def clean_phone_number(phone: str) -> str:
    """Clean and format phone number"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format as (555) 123-4567
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format

def get_database_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect('wtf_platform.db')
    conn.row_factory = sqlite3.Row  # This allows column access by name
    return conn

# property_analyzer.py
"""
Advanced Property Analysis Module
"""

import sqlite3
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

class PropertyDataAPI:
    """Mock property data API - replace with real API integration"""
    
    @staticmethod
    def get_property_details(address: str) -> Dict:
        """Get property details from address"""
        # Mock data - replace with ATTOM Data, Zillow, etc.
        return {
            'bedrooms': random.randint(2, 5),
            'bathrooms': round(random.uniform(1.0, 3.5), 1),
            'square_feet': random.randint(1200, 3500),
            'year_built': random.randint(1970, 2020),
            'lot_size': round(random.uniform(0.15, 0.8), 2),
            'property_type': random.choice(['single_family', 'townhouse', 'condo']),
            'zestimate': random.randint(180000, 400000)
        }
    
    @staticmethod
    def get_comparable_sales(address: str, radius: float = 1.0, limit: int = 10) -> List[Dict]:
        """Get comparable sales within radius"""
        comps = []
        
        for i in range(limit):
            sale_date = datetime.now() - timedelta(days=random.randint(30, 180))
            price = random.randint(200000, 350000)
            sqft = random.randint(1400, 2800)
            
            comps.append({
                'address': f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm'])} {random.choice(['St', 'Ave', 'Dr', 'Ln'])}",
                'sale_price': price,
                'sale_date': sale_date.strftime('%Y-%m-%d'),
                'bedrooms': random.randint(2, 4),
                'bathrooms': round(random.uniform(1.5, 3.0), 1),
                'square_feet': sqft,
                'price_per_sqft': round(price / sqft, 2),
                'distance': round(random.uniform(0.1, radius), 2),
                'days_old': (datetime.now() - sale_date).days
            })
        
        return sorted(comps, key=lambda x: x['distance'])

class RehabEstimator:
    """Rehab cost estimation based on property condition and type"""
    
    COST_PER_SQFT = {
        'excellent': 0,
        'good': 8,
        'fair': 18,
        'poor': 28,
        'needs_rehab': 45
    }
    
    ROOM_COSTS = {
        'kitchen': {'light': 8000, 'medium': 15000, 'heavy': 25000},
        'bathroom': {'light': 3000, 'medium': 8000, 'heavy': 15000},
        'flooring': {'light': 2000, 'medium': 5000, 'heavy': 8000},
        'paint': {'light': 1500, 'medium': 3000, 'heavy': 5000},
        'roof': {'light': 3000, 'medium': 8000, 'heavy': 15000},
        'hvac': {'light': 2000, 'medium': 6000, 'heavy': 12000},
        'electrical': {'light': 1500, 'medium': 4000, 'heavy': 8000},
        'plumbing': {'light': 1500, 'medium': 4000, 'heavy': 7000}
    }
    
    @classmethod
    def estimate_total_rehab(cls, property_data: Dict, condition: str = 'fair') -> Dict:
        """Estimate total rehab cost with breakdown"""
        square_feet = property_data.get('square_feet', 1800)
        base_cost = cls.COST_PER_SQFT.get(condition, 18) * square_feet
        
        # Add specific room costs based on condition
        room_level = 'light' if condition in ['excellent', 'good'] else 'medium' if condition == 'fair' else 'heavy'
        
        breakdown = {}
        for room, costs in cls.ROOM_COSTS.items():
            if condition != 'excellent':  # No costs for excellent condition
                breakdown[room] = costs[room_level]
        
        total_rooms_cost = sum(breakdown.values())
        
        # Use higher of base cost or itemized cost
        total_cost = max(base_cost, total_rooms_cost)
        
        return {
            'total_cost': round(total_cost),
            'cost_per_sqft': round(total_cost / square_feet, 2),
            'breakdown': breakdown,
            'confidence': 85 if condition in ['fair', 'poor'] else 70
        }

# ai_prompts.py
"""
AI Prompt Templates for different scenarios
"""

SCRIPTMASTER_PROMPTS = {
    'cold_calling': """
    You are ScriptMaster AI. Provide a cold calling script for {situation}.
    Include:
    1. Opening (first 10 seconds)
    2. Rapport building
    3. Problem identification
    4. Solution presentation
    5. Call to action
    
    Make it conversational and natural. Property type: {property_type}, Motivation: {motivation}
    """,
    
    'objection_handling': """
    You are ScriptMaster AI. The prospect said: "{objection}"
    
    Provide a response that:
    1. Acknowledges their concern
    2. Addresses the objection directly
    3. Turns it into a question
    4. Moves toward next step
    
    Context: {context}
    """,
    
    'follow_up': """
    You are ScriptMaster AI. Create a follow-up sequence for a {lead_type} lead.
    Last contact: {last_contact}
    Interest level: {interest_level}
    Timeline: {timeline}
    
    Provide 3 touch points with different approaches (call, text, email).
    """
}

UNDERWRITER_PROMPTS = {
    'property_analysis': """
    You are Multifamily Underwriter GPT. Analyze this property:
    
    Address: {address}
    Price: ${price:,}
    Type: {property_type}
    Size: {square_feet} sqft
    Year: {year_built}
    Condition: {condition}
    
    Provide:
    1. Market analysis
    2. Investment potential (1-10 scale)
    3. Risk factors
    4. Recommended strategy
    5. Key metrics to track
    """,
    
    'market_analysis': """
    You are Multifamily Underwriter GPT. Analyze the {city}, {state} market:
    
    Recent data points:
    - Median home price: ${median_price:,}
    - Days on market: {days_on_market}
    - Price trend: {price_trend}
    - Inventory: {inventory_level}
    
    Provide investment outlook and opportunities.
    """,
    
    'deal_structure': """
    You are Multifamily Underwriter GPT. Structure this deal:
    
    ARV: ${arv:,}
    Purchase: ${purchase_price:,}
    Rehab: ${rehab_cost:,}
    
    Recommend:
    1. Deal structure (assignment vs flip)
    2. Financing options
    3. Exit strategy
    4. Risk mitigation
    """
}

# Discord bot integration example
# discord_bot.py
"""
Discord Bot for WTF Platform Notifications
"""

import discord
from discord.ext import commands
import asyncio
import json

class WTFDiscordBot:
    def __init__(self, token: str):
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!wtf ', intents=intents)
        self.token = token
        self.setup_commands()
    
    def setup_commands(self):
        @self.bot.command(name='deal')
        async def send_deal_alert(ctx, *, deal_info):
            """Send a deal alert to the channel"""
            embed = discord.Embed(
                title="🏠 New Deal Alert!",
                description=deal_info,
                color=0x8B5CF6
            )
            await ctx.send(embed=embed)
        
        @self.bot.command(name='buyer')
        async def find_buyers(ctx, price: int, location: str):
            """Find buyers for a deal"""
            embed = discord.Embed(
                title="👥 Buyer Search",
                description=f"Searching for buyers in {location} for ${price:,}",
                color=0x10B981
            )
            await ctx.send(embed=embed)
        
        @self.bot.command(name='analyze')
        async def analyze_property(ctx, *, address):
            """Quick property analysis"""
            embed = discord.Embed(
                title="📊 Property Analysis",
                description=f"Analyzing: {address}",
                color=0xF59E0B
            )
            embed.add_field(name="Status", value="Analysis in progress...", inline=False)
            await ctx.send(embed=embed)
    
    async def send_notification(self, channel_id: int, title: str, message: str, color: int = 0x8B5CF6):
        """Send notification to specific channel"""
        channel = self.bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(title=title, description=message, color=color)
            await channel.send(embed=embed)
    
    def run(self):
        """Start the bot"""
        self.bot.run(self.token)

# Example usage in main app:
# if st.secrets.get("discord", {}).get("bot_token"):
#     discord_bot = WTFDiscordBot(st.secrets["discord"]["bot_token"])
#     # discord_bot.run()  # Run in separate thread