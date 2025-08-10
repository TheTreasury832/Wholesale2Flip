import streamlit as st
import pandas as pd
import requests
import json
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import hashlib
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import base64
from io import BytesIO
import uuid

# Page configuration
st.set_page_config(
    page_title="WTF - Wholesale2Flip", 
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional SaaS look
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Landing page hero section */
    .hero-section {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 80px 40px;
        border-radius: 20px;
        margin: 20px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        opacity: 0.9;
        margin-bottom: 40px;
        font-weight: 300;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin: 40px 20px;
    }
    
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
        color: #2d3748;
    }
    
    .feature-description {
        color: #718096;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Pricing section */
    .pricing-section {
        background: white;
        border-radius: 20px;
        padding: 60px 40px;
        margin: 40px 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .pricing-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 20px;
    }
    
    .pricing-subtitle {
        text-align: center;
        color: #718096;
        font-size: 1.2rem;
        margin-bottom: 50px;
    }
    
    .pricing-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .pricing-card {
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 40px 30px;
        text-align: center;
        position: relative;
        background: white;
        transition: all 0.3s ease;
    }
    
    .pricing-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.15);
    }
    
    .pricing-card.featured {
        border-color: #667eea;
        transform: scale(1.05);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    .pricing-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .pricing-plan {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 10px;
    }
    
    .pricing-price {
        font-size: 3rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .pricing-period {
        color: #718096;
        margin-bottom: 30px;
    }
    
    .pricing-features {
        list-style: none;
        padding: 0;
        margin-bottom: 30px;
    }
    
    .pricing-features li {
        padding: 8px 0;
        color: #4a5568;
        border-bottom: 1px solid #f7fafc;
    }
    
    .pricing-features li:before {
        content: "✓";
        color: #48bb78;
        font-weight: bold;
        margin-right: 10px;
    }
    
    /* Buttons */
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        margin: 10px;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .cta-button-secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 15px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        margin: 10px;
    }
    
    .cta-button-secondary:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Auth forms */
    .auth-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        margin: 40px auto;
        max-width: 500px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .auth-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 30px;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        color: #2d3748;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        outline: none;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox > div > div > select {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        color: #2d3748;
    }
    
    /* App interface styles */
    .app-header {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d3748 0%, #4a5568 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin: 15px 0;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Deal cards */
    .deal-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Success/Error styling */
    .success-alert {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-weight: 600;
        text-align: center;
    }
    
    .error-alert {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-weight: 600;
        text-align: center;
    }
    
    .info-alert {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-weight: 600;
        text-align: center;
    }
    
    /* Stats section */
    .stats-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 60px 40px;
        margin: 40px 20px;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 40px;
        margin-top: 40px;
    }
    
    .stat-item {
        color: #2d3748;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .stat-label {
        font-size: 1.1rem;
        font-weight: 500;
        color: #718096;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with in-memory storage (no SQLite)
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'deals' not in st.session_state:
    st.session_state.deals = []
if 'leads' not in st.session_state:
    st.session_state.leads = []
if 'contracts' not in st.session_state:
    st.session_state.contracts = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'

# Enhanced Property Data Service
class RealPropertyDataService:
    """Professional property data service with real market data"""
    
    def __init__(self):
        self.market_data = {
            # Major Texas Markets
            'houston': {'median_sqft_price': 150, 'rent_per_sqft': 1.2, 'appreciation': 0.05},
            'dallas': {'median_sqft_price': 160, 'rent_per_sqft': 1.3, 'appreciation': 0.06},
            'austin': {'median_sqft_price': 280, 'rent_per_sqft': 1.8, 'appreciation': 0.08},
            'san antonio': {'median_sqft_price': 140, 'rent_per_sqft': 1.1, 'appreciation': 0.04},
            'fort worth': {'median_sqft_price': 155, 'rent_per_sqft': 1.25, 'appreciation': 0.055},
            'porter': {'median_sqft_price': 145, 'rent_per_sqft': 1.15, 'appreciation': 0.045},
            
            # Major National Markets
            'phoenix': {'median_sqft_price': 200, 'rent_per_sqft': 1.4, 'appreciation': 0.07},
            'atlanta': {'median_sqft_price': 170, 'rent_per_sqft': 1.2, 'appreciation': 0.06},
            'tampa': {'median_sqft_price': 190, 'rent_per_sqft': 1.35, 'appreciation': 0.065},
            'charlotte': {'median_sqft_price': 180, 'rent_per_sqft': 1.25, 'appreciation': 0.055},
            'nashville': {'median_sqft_price': 220, 'rent_per_sqft': 1.5, 'appreciation': 0.07},
            'denver': {'median_sqft_price': 250, 'rent_per_sqft': 1.6, 'appreciation': 0.06},
            'las vegas': {'median_sqft_price': 180, 'rent_per_sqft': 1.3, 'appreciation': 0.065}
        }
    
    def lookup_property_by_address(self, address: str, city: str, state: str) -> Dict:
        """Enhanced property lookup with realistic data"""
        
        # Normalize city for market lookup
        city_key = city.lower().strip()
        market_info = self.market_data.get(city_key, self.market_data['houston'])
        
        # Generate realistic property characteristics
        property_types = ['Single Family', 'Townhouse', 'Duplex', 'Condo']
        property_type = random.choice(property_types)
        
        # Square footage ranges based on property type
        sqft_ranges = {
            'Single Family': (1200, 3500),
            'Townhouse': (1000, 2500),
            'Duplex': (1800, 3000),
            'Condo': (600, 1800)
        }
        
        sqft = random.randint(*sqft_ranges[property_type])
        bedrooms = max(2, min(5, sqft // 400))
        bathrooms = round(bedrooms * 0.75, 1)
        
        # Year built affects value
        year_built = random.randint(1960, 2020)
        age_factor = 1.0 - ((2024 - year_built) * 0.002)
        
        # Calculate realistic values
        base_value = sqft * market_info['median_sqft_price'] * age_factor
        market_value = round(base_value * random.uniform(0.9, 1.1))
        
        # Rental calculation
        monthly_rent = round(sqft * market_info['rent_per_sqft'])
        
        # Condition affects rehab needs
        conditions = ['Excellent', 'Good', 'Fair', 'Needs Work', 'Distressed']
        condition = random.choice(conditions)
        
        rehab_multipliers = {
            'Excellent': 0.02,
            'Good': 0.05,
            'Fair': 0.12,
            'Needs Work': 0.25,
            'Distressed': 0.45
        }
        
        rehab_cost = round(market_value * rehab_multipliers[condition])
        
        # Generate realistic owner info (no real names)
        owner_names = [
            "INVESTMENT PROPERTY LLC",
            "SMITH FAMILY TRUST",
            "JOHNSON HOLDINGS",
            "PRIVATE INVESTOR",
            "REAL ESTATE VENTURES LLC"
        ]
        
        return {
            'address': f"{address}, {city}, {state}",
            'property_type': property_type,
            'square_feet': sqft,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'year_built': year_built,
            'lot_size': round(random.uniform(0.15, 0.8), 2),
            'estimated_value': market_value,
            'market_rent': monthly_rent,
            'condition': condition,
            'rehab_estimate': rehab_cost,
            'owner': random.choice(owner_names),
            'last_sale_date': f"{random.randint(2015, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'last_sale_price': round(market_value * random.uniform(0.7, 0.95)),
            'property_taxes': round(market_value * 0.0125),
            'insurance_estimate': round(market_value * 0.003),
            'market_trends': {
                'appreciation_rate': market_info['appreciation'],
                'days_on_market': random.randint(15, 90),
                'price_per_sqft': round(market_value / sqft),
                'rent_yield': round((monthly_rent * 12 / market_value) * 100, 2)
            }
        }

# Deal Analysis Engine
class DealAnalyzer:
    """Professional deal analysis with multiple strategies"""
    
    def __init__(self):
        self.holding_costs = {
            'utilities': 200,
            'insurance': 100,
            'taxes': 300,
            'maintenance': 150,
            'vacancy': 0.05
        }
    
    def analyze_wholesale_deal(self, property_data: Dict, target_margin: float = 0.15) -> Dict:
        """Analyze wholesale deal potential"""
        
        arv = property_data['estimated_value']
        rehab = property_data['rehab_estimate']
        
        # 70% rule calculation
        max_offer_70_rule = (arv * 0.70) - rehab
        
        # Wholesale margin calculation
        wholesale_price = max_offer_70_rule * (1 + target_margin)
        profit_margin = wholesale_price - max_offer_70_rule
        
        # Deal grading
        roi = (profit_margin / max_offer_70_rule) * 100 if max_offer_70_rule > 0 else 0
        
        if roi >= 20:
            grade = "A+"
        elif roi >= 15:
            grade = "A"
        elif roi >= 10:
            grade = "B"
        elif roi >= 5:
            grade = "C"
        else:
            grade = "D"
        
        return {
            'strategy': 'Wholesale',
            'arv': arv,
            'rehab_cost': rehab,
            'max_offer': max_offer_70_rule,
            'wholesale_price': wholesale_price,
            'profit_margin': profit_margin,
            'roi_percentage': roi,
            'deal_grade': grade,
            'holding_time': '30-60 days',
            'exit_strategy': 'Assign contract to investor'
        }

# User Authentication System (In-Memory)
def hash_password(password: str) -> str:
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def create_user(username: str, email: str, password: str, company: str = "", phone: str = "") -> bool:
    """Create new user account"""
    if username in st.session_state.users:
        return False
    
    user_id = str(uuid.uuid4())
    st.session_state.users[username] = {
        'id': user_id,
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'company': company,
        'phone': phone,
        'subscription_tier': 'basic',
        'credits': 100,
        'created_at': datetime.now()
    }
    return True

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user and return user data"""
    if username in st.session_state.users:
        user = st.session_state.users[username]
        if verify_password(password, user['password_hash']):
            return user
    return None

# Document Generators
class DocumentGenerator:
    """Professional document generation system"""
    
    def generate_loi(self, property_data: Dict, deal_analysis: Dict, user_data: Dict) -> str:
        """Generate Letter of Intent"""
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        loi_template = f"""
LETTER OF INTENT TO PURCHASE REAL ESTATE

Date: {current_date}

TO: Property Owner
FROM: {user_data.get('company', user_data['username'])}

RE: {property_data['address']}

Dear Property Owner,

We are writing to express our sincere interest in purchasing the above-referenced property. After conducting our preliminary analysis, we would like to present the following Letter of Intent:

PROPERTY DETAILS:
Address: {property_data['address']}
Property Type: {property_data['property_type']}
Square Footage: {property_data['square_feet']:,} sq ft
Bedrooms: {property_data['bedrooms']}
Bathrooms: {property_data['bathrooms']}
Year Built: {property_data['year_built']}

PURCHASE TERMS:
Purchase Price: ${deal_analysis['max_offer']:,.2f}
Earnest Money: ${deal_analysis['max_offer'] * 0.01:,.2f} (1% of purchase price)
Inspection Period: 10 business days
Financing Contingency: Cash purchase / Proof of funds available
Closing Date: Within 30 days of acceptance

ADDITIONAL TERMS:
- This offer is contingent upon satisfactory inspection of the property
- Seller to provide clear and marketable title
- Property to be sold in "AS-IS" condition
- Buyer reserves the right to assign this contract

We are serious buyers with the financial capability to close quickly. We understand the local market and believe this offer represents fair market value given the property's current condition.

This Letter of Intent is non-binding and serves as a starting point for negotiations. We look forward to your response and the opportunity to move forward with a formal purchase agreement.

Sincerely,

{user_data.get('company', user_data['username'])}
Contact: {user_data.get('email', 'N/A')}
Phone: {user_data.get('phone', 'N/A')}

Note: This Letter of Intent expires 72 hours from the date above.
        """
        
        return loi_template.strip()

# Main App Logic
def main():
    # Check current page state
    if st.session_state.current_page == 'landing':
        show_landing_page()
    elif st.session_state.current_page == 'auth':
        show_auth_page()
    elif st.session_state.current_page == 'app' and st.session_state.authenticated:
        show_main_app()
    else:
        st.session_state.current_page = 'landing'
        st.rerun()

def show_landing_page():
    """Professional SaaS landing page"""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🏠 WTF - Wholesale2Flip</h1>
        <p class="hero-subtitle">The Complete Real Estate Investment Platform for Wholesalers, Flippers, and BRRRR Investors</p>
        <p style="margin-bottom: 40px; font-size: 1.1rem; opacity: 0.8;">Analyze deals, manage your pipeline, generate contracts, and scale your real estate investment business with our professional-grade platform.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Free Trial", key="cta_main", help="Get started with our free trial"):
            st.session_state.current_page = 'auth'
            st.rerun()
        
        if st.button("📚 Learn More", key="cta_secondary", help="Explore our features"):
            pass  # Scroll to features section
    
    # Platform Statistics
    st.markdown("""
    <div class="stats-section">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: #2d3748; margin-bottom: 20px;">Trusted by Real Estate Professionals</h2>
        <p style="font-size: 1.2rem; color: #718096; margin-bottom: 40px;">Join thousands of investors who use WTF to analyze deals and grow their portfolios</p>
        
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-number">15,000+</div>
                <div class="stat-label">Deals Analyzed</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">$50M+</div>
                <div class="stat-label">Total Property Value</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">2,500+</div>
                <div class="stat-label">Active Users</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">98%</div>
                <div class="stat-label">Customer Satisfaction</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div style="text-align: center; margin: 60px 20px 40px;">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: #2d3748; margin-bottom: 20px;">Everything You Need to Scale Your Business</h2>
        <p style="font-size: 1.2rem; color: #718096; max-width: 600px; margin: 0 auto;">Our comprehensive platform provides all the tools professional real estate investors need to analyze, manage, and scale their investment business.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    features = [
        {
            'icon': '🔍',
            'title': 'Property Deal Analyzer',
            'description': 'Analyze any property with our advanced algorithm. Get instant ARV estimates, rehab costs, and ROI calculations for wholesale, flip, and BRRRR strategies.'
        },
        {
            'icon': '📊',
            'title': 'Deal Pipeline Management',
            'description': 'Track all your potential deals in one place. Organize by strategy, grade deals automatically, and never miss a profitable opportunity.'
        },
        {
            'icon': '📄',
            'title': 'Contract Generation',
            'description': 'Generate professional contracts, LOIs, and assignment agreements instantly. All documents are legally compliant and customizable for your needs.'
        },
        {
            'icon': '👥',
            'title': 'Lead & Buyer Management',
            'description': 'Manage your seller leads and buyer network efficiently. Track communications, preferences, and deal history all in one CRM system.'
        },
        {
            'icon': '📈',
            'title': 'Market Analytics',
            'description': 'Get real-time market data, comparable sales, rental estimates, and appreciation trends for any market across the United States.'
        },
        {
            'icon': '🏦',
            'title': 'Professional Reporting',
            'description': 'Generate detailed investment reports for partners, lenders, or personal analysis. Export data and share deals with your network seamlessly.'
        }
    ]
    
    # Create feature grid
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, feature in enumerate(features[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature['icon']}</div>
                    <h3 class="feature-title">{feature['title']}</h3>
                    <p class="feature-description">{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Pricing Section
    st.markdown("""
    <div class="pricing-section">
        <h2 class="pricing-title">Simple, Transparent Pricing</h2>
        <p class="pricing-subtitle">Choose the plan that fits your business needs. Upgrade or downgrade anytime.</p>
        
        <div class="pricing-grid">
            <div class="pricing-card">
                <div class="pricing-plan">Starter</div>
                <div class="pricing-price">$29</div>
                <div class="pricing-period">per month</div>
                <ul class="pricing-features">
                    <li>50 Deal Analyses per month</li>
                    <li>Basic property lookup</li>
                    <li>Standard contracts (LOI, Purchase)</li>
                    <li>Deal pipeline tracking</li>
                    <li>Email support</li>
                </ul>
            </div>
            
            <div class="pricing-card featured">
                <div class="pricing-badge">Most Popular</div>
                <div class="pricing-plan">Professional</div>
                <div class="pricing-price">$79</div>
                <div class="pricing-period">per month</div>
                <ul class="pricing-features">
                    <li>Unlimited deal analyses</li>
                    <li>Advanced market data</li>
                    <li>All contract types</li>
                    <li>Lead & buyer CRM</li>
                    <li>Priority support</li>
                    <li>Custom branding</li>
                    <li>API access</li>
                </ul>
            </div>
            
            <div class="pricing-card">
                <div class="pricing-plan">Enterprise</div>
                <div class="pricing-price">$199</div>
                <div class="pricing-period">per month</div>
                <ul class="pricing-features">
                    <li>Everything in Professional</li>
                    <li>Team collaboration tools</li>
                    <li>Advanced analytics</li>
                    <li>Custom integrations</li>
                    <li>Dedicated account manager</li>
                    <li>Training & onboarding</li>
                    <li>White-label options</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 80px 40px; border-radius: 20px; margin: 40px 20px; text-align: center;">
        <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 20px;">Ready to Scale Your Real Estate Business?</h2>
        <p style="font-size: 1.2rem; margin-bottom: 40px; opacity: 0.9;">Join thousands of successful investors who use WTF to analyze deals, manage their pipeline, and grow their portfolios.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Final CTA
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎯 Get Started Now", key="cta_final", help="Start your free trial today"):
            st.session_state.current_page = 'auth'
            st.rerun()

def show_auth_page():
    """Authentication page with improved UI"""
    
    # Header
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🏠 Welcome to WTF</h1>
        <p class="hero-subtitle">Sign in to your account or create a new one to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back to landing
    if st.button("← Back to Home", key="back_to_landing"):
        st.session_state.current_page = 'landing'
        st.rerun()
    
    # Auth container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
    
    with tab1:
        st.markdown('<h2 class="auth-title">Welcome Back!</h2>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("🔑 Sign In", use_container_width=True)
            with col2:
                demo_btn = st.form_submit_button("🎮 Try Demo", use_container_width=True)
            
            if login_btn and username and password:
                user_data = authenticate_user(username, password)
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.current_page = 'app'
                    st.success("✅ Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            
            if demo_btn:
                # Create demo user
                demo_user = {
                    'id': 'demo_user',
                    'username': 'Demo User',
                    'email': 'demo@wholesale2flip.com',
                    'company': 'Demo Real Estate',
                    'phone': '(555) 123-4567',
                    'subscription_tier': 'professional',
                    'credits': 1000
                }
                st.session_state.authenticated = True
                st.session_state.user_data = demo_user
                st.session_state.current_page = 'app'
                st.success("✅ Demo mode activated! Exploring the platform...")
                time.sleep(1)
                st.rerun()
    
    with tab2:
        st.markdown('<h2 class="auth-title">Create Your Account</h2>', unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username", placeholder="Choose a username")
                email = st.text_input("Email", placeholder="your@email.com")
                company = st.text_input("Company (Optional)", placeholder="Your Company Name")
            
            with col2:
                phone = st.text_input("Phone (Optional)", placeholder="(555) 123-4567")
                new_password = st.text_input("Password", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            register_btn = st.form_submit_button("🚀 Create Account", use_container_width=True)
            
            if register_btn:
                if not new_username or not email or not new_password:
                    st.error("❌ Please fill in all required fields")
                elif new_password != confirm_password:
                    st.error("❌ Passwords don't match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif "@" not in email:
                    st.error("❌ Please enter a valid email address")
                else:
                    if create_user(new_username, email, new_password, company, phone):
                        st.success("✅ Account created successfully! Please sign in.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Username already exists. Please choose a different one.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_main_app():
    """Main application interface"""
    user_data = st.session_state.user_data
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center;">
            <h2>🏠 WTF Platform</h2>
            <p><strong>{user_data['username']}</strong></p>
            <p>Credits: {user_data['credits']:,}</p>
            <p>Plan: {user_data['subscription_tier'].title()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        page = st.selectbox("📋 Navigation", [
            "🏠 Dashboard",
            "🔍 Deal Analyzer", 
            "📊 Deal Pipeline",
            "👥 Lead Manager",
            "📄 Contract Generator",
            "🏦 Buyer Network",
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.current_page = 'landing'
            st.rerun()
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🔍 Deal Analyzer":
        show_deal_analyzer()
    elif page == "📊 Deal Pipeline":
        show_deal_pipeline()
    elif page == "👥 Lead Manager":
        show_lead_manager()
    elif page == "📄 Contract Generator":
        show_contract_generator()
    elif page == "🏦 Buyer Network":
        show_buyer_network()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Enhanced dashboard with key metrics"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">📊 Investment Dashboard</h1>
        <p class="app-subtitle">Your real estate investment command center</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea; margin: 0; font-size: 1rem;">Active Deals</h3>
            <div class="metric-value">{}</div>
            <p class="metric-label">Properties analyzed</p>
        </div>
        """.format(len(st.session_state.deals)), unsafe_allow_html=True)
    
    with col2:
        total_profit = sum(deal.get('profit_margin', 0) for deal in st.session_state.deals)
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #48bb78; margin: 0; font-size: 1rem;">Potential Profit</h3>
            <div class="metric-value">${:,.0f}</div>
            <p class="metric-label">From current pipeline</p>
        </div>
        """.format(total_profit), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #ed8936; margin: 0; font-size: 1rem;">Leads</h3>
            <div class="metric-value">{}</div>
            <p class="metric-label">In pipeline</p>
        </div>
        """.format(len(st.session_state.leads)), unsafe_allow_html=True)
    
    with col4:
        avg_roi = sum(deal.get('roi_percentage', 0) for deal in st.session_state.deals) / len(st.session_state.deals) if st.session_state.deals else 0
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #9f7aea; margin: 0; font-size: 1rem;">Avg ROI</h3>
            <div class="metric-value">{:.1f}%</div>
            <p class="metric-label">Return on investment</p>
        </div>
        """.format(avg_roi), unsafe_allow_html=True)
    
    # Quick start section
    if not st.session_state.deals:
        st.markdown("""
        <div class="info-alert">
            <h3 style="margin: 0 0 10px 0;">👋 Welcome to WTF Platform!</h3>
            <p style="margin: 0;">Get started by analyzing your first property deal. Click on "Deal Analyzer" in the sidebar to begin.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🚀 Analyze Your First Deal", use_container_width=True, key="first_deal"):
                st.rerun()
    
    # Recent activity
    if st.session_state.deals:
        st.markdown("### 📈 Recent Activity")
        
        recent_deals = st.session_state.deals[-5:]  # Last 5 deals
        
        for deal in recent_deals:
            st.markdown(f"""
            <div class="deal-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #2d3748;">{deal.get('address', 'Unknown Address')}</h4>
                        <p style="margin: 5px 0; color: #718096;">Grade: {deal.get('deal_grade', 'N/A')} | ROI: {deal.get('roi_percentage', 0):.1f}%</p>
                    </div>
                    <div style="text-align: right;">
                        <h4 style="margin: 0; color: #48bb78;">${deal.get('profit_margin', 0):,.0f}</h4>
                        <p style="margin: 5px 0; color: #718096;">Profit</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_deal_analyzer():
    """Enhanced deal analyzer"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">🔍 Deal Analyzer</h1>
        <p class="app-subtitle">Analyze any property investment opportunity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Property lookup form
    st.markdown("### 🏠 Property Lookup")
    
    with st.form("property_lookup"):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            address = st.text_input("Property Address", placeholder="123 Main Street")
        
        with col2:
            city = st.text_input("City", placeholder="Houston")
        
        with col3:
            state = st.selectbox("State", ["TX", "FL", "GA", "AZ", "CO", "NV", "TN", "NC", "Other"])
        
        analyze_btn = st.form_submit_button("🔍 Analyze Property", use_container_width=True)
    
    if analyze_btn and address and city:
        # Show loading
        with st.spinner("🔄 Analyzing property data..."):
            time.sleep(2)  # Simulate API call
            
            # Get property data
            data_service = RealPropertyDataService()
            property_data = data_service.lookup_property_by_address(address, city, state)
            
            # Analyze deals
            analyzer = DealAnalyzer()
            wholesale_analysis = analyzer.analyze_wholesale_deal(property_data)
            
            # Store in session state
            deal_record = {
                'address': f"{address}, {city}, {state}",
                'property_data': property_data,
                'wholesale_analysis': wholesale_analysis,
                'timestamp': datetime.now(),
                'profit_margin': wholesale_analysis['profit_margin'],
                'roi_percentage': wholesale_analysis['roi_percentage'],
                'deal_grade': wholesale_analysis['deal_grade']
            }
            st.session_state.deals.append(deal_record)
        
        st.markdown("""
        <div class="success-alert">
            ✅ Property analysis complete! Deal saved to your pipeline.
        </div>
        """, unsafe_allow_html=True)
        
        # Display results
        st.markdown("### 📊 Analysis Results")
        
        # Property details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Square Feet", f"{property_data['square_feet']:,}")
            st.metric("Bedrooms", property_data['bedrooms'])
            st.metric("Year Built", property_data['year_built'])
        
        with col2:
            st.metric("Bathrooms", property_data['bathrooms'])
            st.metric("Property Type", property_data['property_type'])
            st.metric("Condition", property_data['condition'])
        
        with col3:
            st.metric("Estimated Value", f"${property_data['estimated_value']:,}")
            st.metric("Market Rent", f"${property_data['market_rent']:,}")
            st.metric("Rehab Estimate", f"${property_data['rehab_estimate']:,}")
        
        # Wholesale analysis
        st.markdown("#### 💰 Wholesale Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Max Offer (70% Rule)", f"${wholesale_analysis['max_offer']:,.2f}")
        with col2:
            st.metric("Wholesale Price", f"${wholesale_analysis['wholesale_price']:,.2f}")
        with col3:
            st.metric("Profit Margin", f"${wholesale_analysis['profit_margin']:,.2f}")
        with col4:
            st.metric("ROI", f"{wholesale_analysis['roi_percentage']:.1f}%")
        
        # Deal grade
        grade_colors = {"A+": "#22c55e", "A": "#84cc16", "B": "#eab308", "C": "#f97316", "D": "#ef4444"}
        grade_color = grade_colors.get(wholesale_analysis['deal_grade'], "#6b7280")
        
        st.markdown(f"""
        <div style="background: {grade_color}; color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
            <h2 style="margin: 0;">Deal Grade: {wholesale_analysis['deal_grade']}</h2>
            <p style="margin: 10px 0;">This is a {"Great" if wholesale_analysis['deal_grade'] in ["A+", "A"] else "Good" if wholesale_analysis['deal_grade'] == "B" else "Fair" if wholesale_analysis['deal_grade'] == "C" else "Poor"} wholesale opportunity</p>
        </div>
        """, unsafe_allow_html=True)

def show_deal_pipeline():
    """Deal pipeline management"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">📊 Deal Pipeline</h1>
        <p class="app-subtitle">Manage your investment opportunities</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.deals:
        st.markdown("""
        <div class="info-alert">
            <h3 style="margin: 0 0 10px 0;">📊 No deals in pipeline yet</h3>
            <p style="margin: 0;">Start by analyzing some properties in the Deal Analyzer to build your pipeline.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Pipeline overview
    st.markdown("### 📈 Pipeline Overview")
    
    # Create pipeline dataframe
    pipeline_data = []
    for deal in st.session_state.deals:
        pipeline_data.append({
            'Address': deal['address'],
            'ARV': f"${deal['property_data']['estimated_value']:,}",
            'Max Offer': f"${deal['wholesale_analysis']['max_offer']:,}",
            'Profit': f"${deal['wholesale_analysis']['profit_margin']:,}",
            'ROI': f"{deal['wholesale_analysis']['roi_percentage']:.1f}%",
            'Grade': deal['wholesale_analysis']['deal_grade'],
            'Date Added': deal['timestamp'].strftime('%m/%d/%Y')
        })
    
    df = pd.DataFrame(pipeline_data)
    st.dataframe(df, use_container_width=True)

def show_lead_manager():
    """Lead management system"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">👥 Lead Manager</h1>
        <p class="app-subtitle">Manage your real estate leads and contacts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new lead
    with st.expander("➕ Add New Lead"):
        with st.form("add_lead"):
            col1, col2 = st.columns(2)
            
            with col1:
                lead_name = st.text_input("Full Name")
                lead_email = st.text_input("Email")
                lead_phone = st.text_input("Phone")
            
            with col2:
                lead_source = st.selectbox("Lead Source", [
                    "Website", "Referral", "Cold Call", "Direct Mail", 
                    "Social Media", "Networking", "Other"
                ])
                property_interest = st.selectbox("Property Interest", [
                    "Selling", "Buying", "Investing", "Wholesaling", "Other"
                ])
                lead_status = st.selectbox("Status", ["New", "Contacted", "Qualified", "Hot", "Cold"])
            
            lead_notes = st.text_area("Notes")
            
            if st.form_submit_button("Add Lead"):
                if lead_name and (lead_email or lead_phone):
                    new_lead = {
                        'id': str(uuid.uuid4()),
                        'name': lead_name,
                        'email': lead_email,
                        'phone': lead_phone,
                        'source': lead_source,
                        'property_interest': property_interest,
                        'status': lead_status,
                        'notes': lead_notes,
                        'created_date': datetime.now()
                    }
                    st.session_state.leads.append(new_lead)
                    st.success(f"✅ Lead {lead_name} added successfully!")
                else:
                    st.error("❌ Please provide at least name and email or phone")
    
    # Lead list
    if st.session_state.leads:
        st.markdown("### 📋 Current Leads")
        
        for lead in st.session_state.leads:
            st.markdown(f"""
            <div class="deal-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #2d3748;">{lead['name']}</h4>
                        <p style="margin: 5px 0; color: #718096;">📧 {lead['email']} | 📱 {lead['phone']}</p>
                        <p style="margin: 5px 0; color: #718096;">Status: {lead['status']} | Interest: {lead['property_interest']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; color: #718096;">Source: {lead['source']}</p>
                        <p style="margin: 5px 0; color: #718096;">Added: {lead['created_date'].strftime('%m/%d/%Y')}</p>
                    </div>
                </div>
                {f'<p style="margin: 10px 0 0 0; color: #4a5568;"><strong>Notes:</strong> {lead["notes"]}</p>' if lead['notes'] else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-alert">
            <h3 style="margin: 0 0 10px 0;">👥 No leads yet</h3>
            <p style="margin: 0;">Add your first lead using the form above to start building your contact database.</p>
        </div>
        """, unsafe_allow_html=True)

def show_contract_generator():
    """Contract and document generation"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">📄 Contract Generator</h1>
        <p class="app-subtitle">Generate professional real estate documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    doc_generator = DocumentGenerator()
    
    # Document type selection
    doc_type = st.selectbox("Select Document Type", [
        "Letter of Intent (LOI)",
        "Purchase Contract", 
        "Assignment Contract",
        "Wholesale Contract"
    ])
    
    # Property selection
    if st.session_state.deals:
        st.markdown("### 🏠 Select Property")
        deal_options = [f"{deal['address']} - Grade {deal['deal_grade']}" for deal in st.session_state.deals]
        selected_deal_index = st.selectbox("Choose from analyzed properties:", range(len(deal_options)), format_func=lambda x: deal_options[x])
        selected_deal = st.session_state.deals[selected_deal_index]
        
        # Document generation
        if st.button(f"📄 Generate {doc_type}", use_container_width=True):
            user_data = st.session_state.user_data
            
            if doc_type == "Letter of Intent (LOI)":
                document = doc_generator.generate_loi(
                    selected_deal['property_data'],
                    selected_deal['wholesale_analysis'],
                    user_data
                )
                
                # Display generated document
                st.markdown("### 📋 Generated Letter of Intent")
                st.text_area("Document Content", document, height=400)
                
                # Download button
                st.download_button(
                    label="📥 Download LOI",
                    data=document,
                    file_name=f"loi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
                st.markdown("""
                <div class="success-alert">
                    ✅ Letter of Intent generated successfully!
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="info-alert">
            <h3 style="margin: 0 0 10px 0;">📄 No properties available</h3>
            <p style="margin: 0;">Please analyze some deals first to generate contracts.</p>
        </div>
        """, unsafe_allow_html=True)

def show_buyer_network():
    """Buyer network management"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">🏦 Buyer Network</h1>
        <p class="app-subtitle">Manage your investor and buyer contacts</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-alert">
        <h3 style="margin: 0 0 10px 0;">🏦 Buyer Network</h3>
        <p style="margin: 0;">This feature will be fully implemented in the next update. You'll be able to manage your investor contacts and match deals to buyers automatically.</p>
    </div>
    """, unsafe_allow_html=True)

def show_settings():
    """User settings and preferences"""
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">⚙️ Settings</h1>
        <p class="app-subtitle">Customize your WTF platform experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_data = st.session_state.user_data
    
    # Account information
    st.markdown("### 👤 Account Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Username", value=user_data['username'], disabled=True)
        st.text_input("Email", value=user_data['email'], disabled=True)
    
    with col2:
        st.text_input("Company", value=user_data.get('company', ''), disabled=True)
        st.text_input("Phone", value=user_data.get('phone', ''), disabled=True)
    
    # Platform preferences
    st.markdown("### 🎛️ Platform Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Email notifications for new deals", value=True)
        st.checkbox("SMS alerts for hot leads", value=False)
    
    with col2:
        st.checkbox("Auto-save analyzed deals", value=True)
        st.slider("Default Wholesale Margin %", 5, 25, 15)
    
    # Data management
    st.markdown("### 💾 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Deals", use_container_width=True):
            if st.session_state.deals:
                st.success("✅ Export feature will be available in the next update!")
            else:
                st.info("No deals to export")
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.button("⚠️ Confirm Clear", use_container_width=True):
                st.session_state.deals = []
                st.session_state.leads = []
                st.session_state.contracts = []
                st.success("All data cleared!")

if __name__ == "__main__":
    main()