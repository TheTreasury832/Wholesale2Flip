"""
Wholesale2Flip (WTF) - Complete Real Estate Wholesaling Platform
Advanced Streamlit application with AI integration, buyer matching, and automation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import sqlite3
import hashlib
import uuid
from typing import Dict, List, Optional, Any
import openai
from dataclasses import dataclass
import asyncio
import time

# Page configuration
st.set_page_config(
    page_title="WTF - Wholesale2Flip Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WTF branding
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .main-header {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .success-metric {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .warning-metric {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .stButton > button {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    .sidebar .stSelectbox {
        background: rgba(139, 92, 246, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Data classes for type safety
@dataclass
class Property:
    id: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    bedrooms: int
    bathrooms: float
    square_feet: int
    year_built: int
    list_price: float
    arv: float = 0
    rehab_cost: float = 0
    max_offer: float = 0
    profit_potential: float = 0
    created_at: datetime = None

@dataclass
class Buyer:
    id: str
    name: str
    email: str
    phone: str
    property_types: List[str]
    min_price: float
    max_price: float
    states: List[str]
    cities: List[str]
    deal_types: List[str]
    verified: bool = False
    proof_of_funds: bool = False

@dataclass
class Lead:
    id: str
    first_name: str
    last_name: str
    phone: str
    email: str
    property_address: str
    motivation: str
    timeline: str
    source: str
    status: str
    score: int = 0
    created_at: datetime = None

# Database helper class
class DatabaseManager:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with all required tables"""
        conn = sqlite3.connect('wtf_platform.db')
        cursor = conn.cursor()
        
        # Properties table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id TEXT PRIMARY KEY,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                property_type TEXT NOT NULL,
                bedrooms INTEGER,
                bathrooms REAL,
                square_feet INTEGER,
                year_built INTEGER,
                list_price REAL,
                arv REAL DEFAULT 0,
                rehab_cost REAL DEFAULT 0,
                max_offer REAL DEFAULT 0,
                profit_potential REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Buyers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buyers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                property_types TEXT,
                min_price REAL,
                max_price REAL,
                states TEXT,
                cities TEXT,
                deal_types TEXT,
                verified BOOLEAN DEFAULT 0,
                proof_of_funds BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                property_address TEXT NOT NULL,
                motivation TEXT,
                timeline TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Deals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                id TEXT PRIMARY KEY,
                property_id TEXT,
                buyer_id TEXT,
                lead_id TEXT,
                title TEXT NOT NULL,
                purchase_price REAL,
                assignment_fee REAL,
                status TEXT DEFAULT 'lead',
                contract_date TIMESTAMP,
                closing_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id),
                FOREIGN KEY (buyer_id) REFERENCES buyers (id),
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        ''')
        
        # Contracts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                id TEXT PRIMARY KEY,
                deal_id TEXT NOT NULL,
                contract_type TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                earnest_money REAL,
                closing_date TIMESTAMP,
                buyer_name TEXT,
                seller_name TEXT,
                status TEXT DEFAULT 'draft',
                document_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deal_id) REFERENCES deals (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect('wtf_platform.db')

# Property Analysis Service
class PropertyAnalyzer:
    def __init__(self):
        self.db = DatabaseManager()
    
    def analyze_property(self, address: str, property_data: Dict) -> Dict:
        """Analyze property and calculate key metrics"""
        try:
            # Get comparable sales (mock data for demo)
            comps = self.get_comparable_sales(property_data)
            
            # Calculate ARV using comps
            arv = self.calculate_arv(property_data, comps)
            
            # Estimate rehab costs
            rehab_cost = self.estimate_rehab_costs(property_data)
            
            # Calculate max offer (70% rule)
            max_offer = (arv * 0.7) - rehab_cost
            
            # Calculate profit potential
            profit_potential = arv - max_offer - rehab_cost
            
            # Calculate ROI
            roi = (profit_potential / max_offer) * 100 if max_offer > 0 else 0
            
            return {
                'arv': arv,
                'rehab_cost': rehab_cost,
                'max_offer': max_offer,
                'profit_potential': profit_potential,
                'roi': roi,
                'comps': comps,
                'confidence_score': 85  # Mock confidence score
            }
        except Exception as e:
            st.error(f"Property analysis failed: {str(e)}")
            return {}
    
    def get_comparable_sales(self, property_data: Dict) -> List[Dict]:
        """Get comparable sales data"""
        # Mock comparable sales data
        return [
            {
                'address': '123 Similar St',
                'sale_price': 285000,
                'sale_date': '2024-01-15',
                'bedrooms': property_data.get('bedrooms', 3),
                'bathrooms': property_data.get('bathrooms', 2),
                'square_feet': property_data.get('square_feet', 1800),
                'distance': 0.3,
                'price_per_sqft': 158.33
            },
            {
                'address': '456 Nearby Ave',
                'sale_price': 295000,
                'sale_date': '2024-02-01',
                'bedrooms': property_data.get('bedrooms', 3),
                'bathrooms': property_data.get('bathrooms', 2.5),
                'square_feet': property_data.get('square_feet', 1900),
                'distance': 0.5,
                'price_per_sqft': 155.26
            }
        ]
    
    def calculate_arv(self, property_data: Dict, comps: List[Dict]) -> float:
        """Calculate After Repair Value"""
        if not comps:
            return property_data.get('list_price', 0)
        
        # Calculate average price per square foot
        avg_price_per_sqft = sum(comp['price_per_sqft'] for comp in comps) / len(comps)
        
        # Apply to subject property
        square_feet = property_data.get('square_feet', 1800)
        return round(avg_price_per_sqft * square_feet)
    
    def estimate_rehab_costs(self, property_data: Dict) -> float:
        """Estimate rehab costs based on condition and size"""
        square_feet = property_data.get('square_feet', 1800)
        condition = property_data.get('condition', 'fair')
        
        cost_per_sqft_map = {
            'excellent': 0,
            'good': 5,
            'fair': 15,
            'poor': 25,
            'needs_rehab': 40
        }
        
        cost_per_sqft = cost_per_sqft_map.get(condition, 20)
        return round(square_feet * cost_per_sqft)

# Buyer Matching Service
class BuyerMatcher:
    def __init__(self):
        self.db = DatabaseManager()
    
    def find_matches(self, property_data: Dict) -> List[Dict]:
        """Find matching buyers for a property"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM buyers 
            WHERE verified = 1 
            AND min_price <= ? 
            AND max_price >= ?
        ''', (property_data.get('list_price', 0), property_data.get('list_price', 0)))
        
        buyers = cursor.fetchall()
        conn.close()
        
        matches = []
        for buyer in buyers:
            score = self.calculate_match_score(property_data, buyer)
            if score > 50:
                matches.append({
                    'buyer': buyer,
                    'match_score': score,
                    'match_reasons': self.get_match_reasons(property_data, buyer)
                })
        
        return sorted(matches, key=lambda x: x['match_score'], reverse=True)
    
    def calculate_match_score(self, property_data: Dict, buyer: tuple) -> int:
        """Calculate match score between property and buyer"""
        score = 0
        
        # Property type match (30 points)
        buyer_types = buyer[4].split(',') if buyer[4] else []
        if property_data.get('property_type') in buyer_types:
            score += 30
        
        # Price range match (25 points)
        list_price = property_data.get('list_price', 0)
        if buyer[5] <= list_price <= buyer[6]:
            score += 25
        
        # Location match (20 points)
        buyer_states = buyer[7].split(',') if buyer[7] else []
        if property_data.get('state') in buyer_states:
            score += 20
        
        # Verification bonus (25 points)
        if buyer[10]:  # verified
            score += 15
        if buyer[11]:  # proof of funds
            score += 10
        
        return min(score, 100)
    
    def get_match_reasons(self, property_data: Dict, buyer: tuple) -> List[str]:
        """Get reasons why buyer matches property"""
        reasons = []
        
        buyer_types = buyer[4].split(',') if buyer[4] else []
        if property_data.get('property_type') in buyer_types:
            reasons.append('Property type match')
        
        list_price = property_data.get('list_price', 0)
        if buyer[5] <= list_price <= buyer[6]:
            reasons.append('Price range match')
        
        buyer_states = buyer[7].split(',') if buyer[7] else []
        if property_data.get('state') in buyer_states:
            reasons.append('Location preference')
        
        if buyer[11]:  # proof of funds
            reasons.append('Verified buyer with proof of funds')
        
        return reasons

# AI Assistant Service
class AIAssistant:
    def __init__(self):
        self.api_key = st.secrets.get("openai_api_key", "")
        if self.api_key:
            openai.api_key = self.api_key
    
    def get_response(self, prompt: str, ai_type: str = "general", context: Dict = None) -> str:
        """Get AI response based on type and context"""
        system_prompts = {
            "scriptmaster": """You are ScriptMaster AI, an expert real estate wholesaling coach specializing in cold calling scripts, objection handling, and sales conversations. You have access to Mike K's proven Treasury Vault training materials and scripts. Always provide specific, actionable advice with exact phrases and responses. Focus on:

1. Building rapport quickly
2. Identifying motivated sellers
3. Handling common objections
4. Closing for appointments
5. Following up effectively

Provide responses that sound natural and conversational, not robotic.""",
            
            "underwriter": """You are the Multifamily Underwriter GPT, an expert in real estate investment analysis and underwriting. You specialize in:

1. Property valuation and ARV calculations
2. Cash flow analysis and cap rate calculations
3. Market comparisons and trends
4. Risk assessment and due diligence
5. Investment strategy recommendations

Always provide specific numbers, calculations, and reasoning behind your analysis.""",
            
            "general": "You are a helpful real estate wholesaling assistant with expertise in property analysis, buyer matching, and deal structuring."
        }
        
        if not self.api_key:
            return "AI Assistant is not configured. Please add your OpenAI API key to secrets."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompts.get(ai_type, system_prompts["general"])},
                    {"role": "user", "content": f"{prompt}\n\nContext: {json.dumps(context or {})}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI request failed: {str(e)}"

# Initialize services
@st.cache_resource
def get_services():
    return {
        'property_analyzer': PropertyAnalyzer(),
        'buyer_matcher': BuyerMatcher(),
        'ai_assistant': AIAssistant(),
        'db': DatabaseManager()
    }

services = get_services()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'wholesaler'
if 'ai_messages' not in st.session_state:
    st.session_state.ai_messages = []

# Authentication function
def authenticate_user(username: str, password: str) -> bool:
    """Simple authentication (replace with real auth system)"""
    # Demo credentials
    demo_users = {
        'admin': 'admin123',
        'wholesaler': 'wholesale123',
        'buyer': 'buyer123'
    }
    return demo_users.get(username) == password

# Sidebar Navigation
def render_sidebar():
    """Render sidebar navigation"""
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   font-size: 2rem; font-weight: bold;'>WTF</h1>
        <p style='color: #10B981; font-weight: bold;'>Wholesaling on Steroids</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        return None
    
    pages = {
        "🏠 Dashboard": "dashboard",
        "🔍 Property Search": "property_search",
        "👥 Buyer Network": "buyers",
        "📋 Pipeline": "pipeline",
        "📞 Leads": "leads",
        "📄 Contracts": "contracts",
        "⚡ Lightning Leads": "lightning_leads",
        "🤖 AI Assistant": "ai_assistant",
        "📊 Analytics": "analytics",
        "⚙️ Settings": "settings"
    }
    
    selected_page = st.sidebar.selectbox(
        "Navigate",
        list(pages.keys()),
        key="navigation"
    )
    
    # User info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**User:** {st.session_state.get('username', 'User')}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role.title()}")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    return pages[selected_page]

# Authentication page
def render_auth_page():
    """Render authentication page"""
    st.markdown('<h1 class="main-header">Welcome to WTF Platform</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(139, 92, 246, 0.3);'>
            <h3 style='text-align: center; color: #10B981; margin-bottom: 1rem;'>Sign In</h3>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            role = st.selectbox("Role", ["wholesaler", "buyer", "admin"])
            
            submitted = st.form_submit_button("Sign In")
            
            if submitted:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = role
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Demo credentials
        st.markdown("""
        <div style='margin-top: 1rem; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 10px;'>
            <h4 style='color: #10B981;'>Demo Credentials:</h4>
            <p><strong>Admin:</strong> admin / admin123</p>
            <p><strong>Wholesaler:</strong> wholesaler / wholesale123</p>
            <p><strong>Buyer:</strong> buyer / buyer123</p>
        </div>
        """, unsafe_allow_html=True)

# Dashboard page
def render_dashboard():
    """Render main dashboard"""
    st.markdown('<h1 class="main-header">WTF Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card success-metric'>
            <h3 style='color: #10B981; margin: 0;'>$2.5M+</h3>
            <p style='margin: 0;'>Total Deals Closed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0;'>156</h3>
            <p style='margin: 0;'>Active Properties</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0;'>2,341</h3>
            <p style='margin: 0;'>Verified Buyers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card warning-metric'>
            <h3 style='color: #F59E0B; margin: 0;'>42</h3>
            <p style='margin: 0;'>Leads This Week</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Property search section
    st.markdown("## 🔍 Pop In Your Address")
    st.markdown("Let's find you a buyer and analyze this deal")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        address_input = st.text_input(
            "",
            placeholder="Enter property address (e.g., 123 Main St, City, State)",
            key="dashboard_address"
        )
    
    with col2:
        analyze_button = st.button("Find Buyers", type="primary")
    
    if analyze_button and address_input:
        with st.spinner("Analyzing property and finding buyers..."):
            # Mock property data for demo
            mock_property = {
                'address': address_input,
                'property_type': 'single_family',
                'bedrooms': 3,
                'bathrooms': 2,
                'square_feet': 1800,
                'list_price': 250000,
                'condition': 'fair',
                'state': 'TX',
                'city': 'Dallas'
            }
            
            # Analyze property
            analysis = services['property_analyzer'].analyze_property(address_input, mock_property)
            
            if analysis:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("ARV", f"${analysis['arv']:,.0f}")
                    st.metric("Rehab Cost", f"${analysis['rehab_cost']:,.0f}")
                
                with col2:
                    st.metric("Max Offer", f"${analysis['max_offer']:,.0f}")
                    st.metric("Profit Potential", f"${analysis['profit_potential']:,.0f}")
                
                with col3:
                    st.metric("ROI", f"{analysis['roi']:.1f}%")
                    st.metric("Confidence", f"{analysis['confidence_score']}%")
                
                # Find buyers
                matches = services['buyer_matcher'].find_matches(mock_property)
                
                if matches:
                    st.success(f"Found {len(matches)} matching buyers!")
                    
                    for match in matches[:3]:  # Show top 3 matches
                        buyer = match['buyer']
                        with st.expander(f"Buyer: {buyer[1]} (Match: {match['match_score']}%)"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Email:** {buyer[2]}")
                                st.write(f"**Phone:** {buyer[3]}")
                            with col2:
                                st.write(f"**Price Range:** ${buyer[5]:,.0f} - ${buyer[6]:,.0f}")
                                st.write(f"**Verified:** {'✅' if buyer[10] else '❌'}")
                            
                            st.write("**Match Reasons:**")
                            for reason in match['match_reasons']:
                                st.write(f"• {reason}")
                else:
                    st.warning("No matching buyers found for this property.")
    
    # Recent activity
    st.markdown("## 📈 Recent Activity")
    
    # Mock data for charts
    dates = pd.date_range(start='2024-01-01', end='2024-08-02', freq='D')
    deals_data = pd.DataFrame({
        'Date': dates,
        'New Leads': np.random.poisson(3, len(dates)),
        'Properties Added': np.random.poisson(2, len(dates)),
        'Deals Closed': np.random.poisson(1, len(dates))
    })
    
    # Activity chart
    fig = px.line(deals_data.tail(30), x='Date', y=['New Leads', 'Properties Added', 'Deals Closed'],
                  title="30-Day Activity Trend")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig, use_container_width=True)

# Property Search page
def render_property_search():
    """Render property search and analysis page"""
    st.markdown('<h1 class="main-header">Property Search & Analysis</h1>', unsafe_allow_html=True)
    
    # Search form
    with st.form("property_search_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Property Information")
            address = st.text_input("Property Address*", placeholder="123 Main Street")
            
            col1_1, col1_2, col1_3 = st.columns(3)
            with col1_1:
                city = st.text_input("City*", placeholder="Dallas")
            with col1_2:
                state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA", "NC", "OH", "MI", "PA", "IL"])
            with col1_3:
                zip_code = st.text_input("ZIP Code*", placeholder="75201")
        
        with col2:
            st.markdown("### Property Details")
            property_type = st.selectbox("Property Type", 
                                       ["Single Family", "Multi Family", "Condo", "Townhouse"])
            bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
            square_feet = st.number_input("Square Feet", min_value=0, max_value=10000, value=1800)
            year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1995)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("### Financial Information")
            list_price = st.number_input("List Price ($)", min_value=0, value=250000)
            condition = st.selectbox("Condition", 
                                   ["Excellent", "Good", "Fair", "Poor", "Needs Rehab"])
        
        with col4:
            st.markdown("### Analysis Options")
            analyze_comps = st.checkbox("Include Comparable Sales", value=True)
            estimate_rehab = st.checkbox("Estimate Rehab Costs", value=True)
            find_buyers = st.checkbox("Find Matching Buyers", value=True)
        
        submitted = st.form_submit_button("Analyze Property", type="primary")
    
    if submitted and address and city and state:
        property_data = {
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'property_type': property_type.lower().replace(' ', '_'),
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'square_feet': square_feet,
            'year_built': year_built,
            'list_price': list_price,
            'condition': condition.lower().replace(' ', '_')
        }
        
        with st.spinner("Analyzing property..."):
            analysis = services['property_analyzer'].analyze_property(address, property_data)
            
            if analysis:
                st.success("Analysis complete!")
                
                # Analysis results
                st.markdown("## 📊 Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "After Repair Value (ARV)",
                        f"${analysis['arv']:,.0f}",
                        delta=f"${analysis['arv'] - list_price:,.0f}"
                    )
                
                with col2:
                    st.metric(
                        "Estimated Rehab Cost",
                        f"${analysis['rehab_cost']:,.0f}"
                    )
                
                with col3:
                    st.metric(
                        "Maximum Offer (70% Rule)",
                        f"${analysis['max_offer']:,.0f}"
                    )
                
                with col4:
                    st.metric(
                        "Profit Potential",
                        f"${analysis['profit_potential']:,.0f}",
                        delta=f"{analysis['roi']:.1f}% ROI"
                    )
                
                # Comparable sales
                if analyze_comps and analysis.get('comps'):
                    st.markdown("## 🏘️ Comparable Sales")
                    
                    comps_df = pd.DataFrame(analysis['comps'])
                    st.dataframe(comps_df, use_container_width=True)
                
                # Buyer matches
                if find_buyers:
                    st.markdown("## 👥 Matching Buyers")
                    
                    matches = services['buyer_matcher'].find_matches(property_data)
                    
                    if matches:
                        st.success(f"Found {len(matches)} matching buyers!")
                        
                        for i, match in enumerate(matches):
                            buyer = match['buyer']
                            
                            with st.expander(f"Buyer #{i+1}: {buyer[1]} (Match Score: {match['match_score']}%)"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Name:** {buyer[1]}")
                                    st.write(f"**Email:** {buyer[2]}")
                                    st.write(f"**Phone:** {buyer[3]}")
                                    st.write(f"**Verified:** {'✅ Yes' if buyer[10] else '❌ No'}")
                                    st.write(f"**Proof of Funds:** {'✅ Yes' if buyer[11] else '❌ No'}")
                                
                                with col2:
                                    st.write(f"**Price Range:** ${buyer[5]:,.0f} - ${buyer[6]:,.0f}")
                                    st.write(f"**Property Types:** {buyer[4]}")
                                    st.write(f"**Target States:** {buyer[7]}")
                                    
                                    if st.button(f"Contact Buyer {i+1}", key=f"contact_{i}"):
                                        st.success(f"Contact initiated with {buyer[1]}")
                                
                                st.write("**Why this buyer matches:**")
                                for reason in match['match_reasons']:
                                    st.write(f"• {reason}")
                    else:
                        st.warning("No matching buyers found for this property.")
                        st.info("Consider adjusting your price or property details, or add more buyers to your network.")

# Buyer Network page
def render_buyers_page():
    """Render buyer network management page"""
    st.markdown('<h1 class="main-header">Buyer Network</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Browse Buyers", "Add New Buyer", "Buyer Analytics"])
    
    with tab1:
        st.markdown("### Verified Cash Buyers")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            state_filter = st.selectbox("Filter by State", 
                                      ["All States", "TX", "CA", "FL", "NY", "GA"])
        with col2:
            type_filter = st.selectbox("Property Type", 
                                     ["All Types", "Single Family", "Multi Family", "Condo"])
        with col3:
            verified_filter = st.selectbox("Verification Status", 
                                         ["All", "Verified Only", "Unverified"])
        with col4:
            price_range = st.selectbox("Price Range", 
                                     ["All Ranges", "$0-$100K", "$100K-$250K", "$250K-$500K", "$500K+"])
        
        # Mock buyer data
        buyers_data = [
            {"Name": "John Smith", "Email": "john@example.com", "Phone": "(555) 123-4567", 
             "Price Range": "$100K - $300K", "States": "TX, OK", "Verified": "✅", "POF": "✅"},
            {"Name": "Sarah Johnson", "Email": "sarah@realty.com", "Phone": "(555) 234-5678", 
             "Price Range": "$150K - $400K", "States": "TX, AR", "Verified": "✅", "POF": "✅"},
            {"Name": "Mike Davis", "Email": "mike@invest.com", "Phone": "(555) 345-6789", 
             "Price Range": "$200K - $500K", "States": "TX", "Verified": "✅", "POF": "❌"},
            {"Name": "Lisa Wilson", "Email": "lisa@properties.com", "Phone": "(555) 456-7890", 
             "Price Range": "$75K - $200K", "States": "TX, LA", "Verified": "❌", "POF": "❌"},
        ]
        
        buyers_df = pd.DataFrame(buyers_data)
        
        # Display buyers in cards
        for index, buyer in buyers_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    st.markdown(f"**{buyer['Name']}**")
                    st.write(f"📧 {buyer['Email']}")
                    st.write(f"📱 {buyer['Phone']}")
                
                with col2:
                    st.write(f"💰 {buyer['Price Range']}")
                    st.write(f"📍 {buyer['States']}")
                
                with col3:
                    st.write(f"Verified: {buyer['Verified']}")
                    st.write(f"Proof of Funds: {buyer['POF']}")
                
                with col4:
                    if st.button("Contact", key=f"contact_buyer_{index}"):
                        st.success(f"Contacting {buyer['Name']}")
                
                st.markdown("---")
    
    with tab2:
        st.markdown("### Add New Buyer to Network")
        
        with st.form("add_buyer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Contact Information")
                buyer_name = st.text_input("Full Name*")
                buyer_email = st.text_input("Email*")
                buyer_phone = st.text_input("Phone")
                company = st.text_input("Company/Business Name")
            
            with col2:
                st.markdown("#### Investment Criteria")
                min_price = st.number_input("Minimum Price ($)", min_value=0, value=50000)
                max_price = st.number_input("Maximum Price ($)", min_value=0, value=300000)
                buyer_states = st.multiselect("Target States", 
                                            ["TX", "CA", "FL", "NY", "GA", "NC", "OH", "MI", "PA", "IL"])
                property_types = st.multiselect("Property Types", 
                                              ["Single Family", "Multi Family", "Condo", "Townhouse"])
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### Deal Preferences")
                deal_types = st.multiselect("Deal Types", 
                                          ["Cash", "Creative Finance", "Subject To", "Seller Finance"])
                min_roi = st.number_input("Minimum ROI (%)", min_value=0.0, value=15.0)
                max_rehab = st.number_input("Max Rehab Cost ($)", min_value=0, value=50000)
            
            with col4:
                st.markdown("#### Verification")
                has_pof = st.checkbox("Has Proof of Funds")
                is_verified = st.checkbox("Verified Buyer")
                experience_level = st.selectbox("Experience Level", 
                                              ["Beginner", "Intermediate", "Advanced", "Expert"])
            
            notes = st.text_area("Additional Notes")
            
            if st.form_submit_button("Add Buyer", type="primary"):
                if buyer_name and buyer_email:
                    # Here you would save to database
                    st.success(f"Buyer {buyer_name} added successfully!")
                    st.info("Buyer will receive a welcome email with platform access.")
                else:
                    st.error("Please fill in required fields (Name and Email)")
    
    with tab3:
        st.markdown("### Buyer Network Analytics")
        
        # Mock analytics data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Buyers", "2,341", delta="47 this month")
        with col2:
            st.metric("Verified Buyers", "1,892", delta="23 this month")
        with col3:
            st.metric("Active This Month", "1,456", delta="12%")
        with col4:
            st.metric("Avg. Deal Size", "$185K", delta="$15K")
        
        # Buyer distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            # State distribution
            state_data = pd.DataFrame({
                'State': ['TX', 'CA', 'FL', 'NY', 'GA', 'NC', 'Others'],
                'Buyers': [450, 320, 280, 220, 180, 150, 741]
            })
            
            fig_states = px.pie(state_data, values='Buyers', names='State', 
                              title='Buyers by State')
            fig_states.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                                   paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_states, use_container_width=True)
        
        with col2:
            # Price range distribution
            price_data = pd.DataFrame({
                'Range': ['$0-100K', '$100K-250K', '$250K-500K', '$500K+'],
                'Buyers': [523, 892, 641, 285]
            })
            
            fig_price = px.bar(price_data, x='Range', y='Buyers', 
                             title='Buyers by Price Range')
            fig_price.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                                  paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_price, use_container_width=True)

# AI Assistant page
def render_ai_assistant():
    """Render AI assistant page"""
    st.markdown('<h1 class="main-header">🤖 AI Assistant</h1>', unsafe_allow_html=True)
    
    # AI Type selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 ScriptMaster AI", use_container_width=True):
            st.session_state.ai_type = "scriptmaster"
    
    with col2:
        if st.button("🏢 Underwriter GPT", use_container_width=True):
            st.session_state.ai_type = "underwriter"
    
    with col3:
        if st.button("💬 General Assistant", use_container_width=True):
            st.session_state.ai_type = "general"
    
    # Set default AI type
    if 'ai_type' not in st.session_state:
        st.session_state.ai_type = "scriptmaster"
    
    # Display current AI type
    ai_type_names = {
        "scriptmaster": "📞 ScriptMaster AI - Cold Calling & Objection Handling Expert",
        "underwriter": "🏢 Multifamily Underwriter GPT - Investment Analysis Expert",
        "general": "💬 General AI Assistant - Real Estate Wholesaling Helper"
    }
    
    st.markdown(f"### Current AI: {ai_type_names[st.session_state.ai_type]}")
    
    # Quick prompts based on AI type
    quick_prompts = {
        "scriptmaster": [
            "Give me a cold calling script for distressed properties",
            "How do I handle the 'I'm not interested' objection?",
            "What's a good follow-up sequence for warm leads?",
            "Help me practice handling price objections"
        ],
        "underwriter": [
            "Analyze this property for wholesaling potential",
            "Calculate the ARV for a 3bed/2bath in Dallas",
            "What's a good cap rate for rental properties?",
            "Help me estimate rehab costs for a property"
        ],
        "general": [
            "How do I find more cash buyers?",
            "What's the 70% rule in wholesaling?",
            "How do I market to motivated sellers?",
            "Explain contract assignment process"
        ]
    }
    
    # Display quick prompts
    st.markdown("#### Quick Prompts:")
    cols = st.columns(2)
    for i, prompt in enumerate(quick_prompts[st.session_state.ai_type]):
        with cols[i % 2]:
            if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
                st.session_state.ai_input = prompt
    
    # Chat interface
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.ai_messages:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.write(message['content'])
    
    # Chat input
    user_input = st.chat_input("Ask your AI assistant...")
    
    # Handle quick prompt input
    if 'ai_input' in st.session_state:
        user_input = st.session_state.ai_input
        del st.session_state.ai_input
    
    if user_input:
        # Add user message
        st.session_state.ai_messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            response = services['ai_assistant'].get_response(
                user_input, 
                st.session_state.ai_type,
                {"user_role": st.session_state.user_role}
            )
        
        # Add AI response
        st.session_state.ai_messages.append({"role": "assistant", "content": response})
        
        # Rerun to display new messages
        st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.ai_messages = []
        st.rerun()

# Main application
def main():
    """Main application entry point"""
    if not st.session_state.authenticated:
        render_auth_page()
        return
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    if selected_page == "dashboard":
        render_dashboard()
    elif selected_page == "property_search":
        render_property_search()
    elif selected_page == "buyers":
        render_buyers_page()
    elif selected_page == "ai_assistant":
        render_ai_assistant()
    elif selected_page == "pipeline":
        st.markdown('<h1 class="main-header">Deal Pipeline</h1>', unsafe_allow_html=True)
        st.info("Pipeline management coming soon!")
    elif selected_page == "leads":
        st.markdown('<h1 class="main-header">Lead Management</h1>', unsafe_allow_html=True)
        st.info("Lead management system coming soon!")
    elif selected_page == "contracts":
        st.markdown('<h1 class="main-header">Contract Generation</h1>', unsafe_allow_html=True)
        st.info("Contract generation system coming soon!")
    elif selected_page == "lightning_leads":
        st.markdown('<h1 class="main-header">⚡ Lightning Leads</h1>', unsafe_allow_html=True)
        st.info("Premium lightning leads service coming soon!")
    elif selected_page == "analytics":
        st.markdown('<h1 class="main-header">Analytics Dashboard</h1>', unsafe_allow_html=True)
        st.info("Advanced analytics coming soon!")
    elif selected_page == "settings":
        st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
        st.info("Settings panel coming soon!")

if __name__ == "__main__":
    main()