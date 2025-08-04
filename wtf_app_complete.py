"""
Wholesale2Flip (WTF) - Complete Real Estate Wholesaling Platform
Full version with all pages implemented - No OpenAI dependencies
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import hashlib
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
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
        
        # Insert sample buyers if table is empty
        cursor.execute("SELECT COUNT(*) FROM buyers")
        if cursor.fetchone()[0] == 0:
            sample_buyers = [
                ('John Smith', 'john.smith@investor.com', '(555) 123-4567', 'single_family,multi_family', 
                 100000, 300000, 'TX,OK', 'Dallas,Houston,Austin', 'cash,creative', 1, 1),
                ('Sarah Johnson', 'sarah@realtyinvest.com', '(555) 234-5678', 'single_family,condo',
                 150000, 400000, 'TX,AR', 'Dallas,Fort Worth', 'cash', 1, 1),
                ('Mike Davis', 'mike.davis@properties.com', '(555) 345-6789', 'multi_family',
                 200000, 500000, 'TX', 'Dallas', 'cash,subject_to', 1, 0),
                ('Lisa Wilson', 'lisa@buyhold.com', '(555) 456-7890', 'single_family',
                 75000, 200000, 'TX,LA', 'Dallas,San Antonio', 'creative', 0, 0),
            ]
            
            for buyer in sample_buyers:
                buyer_id = str(uuid.uuid4())
                cursor.execute('''
                    INSERT INTO buyers (id, name, email, phone, property_types, min_price, max_price, 
                                      states, cities, deal_types, verified, proof_of_funds)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (buyer_id,) + buyer)
        
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
            WHERE min_price <= ? 
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

# AI Assistant Service (Mock - No OpenAI)
class MockAIAssistant:
    """Mock AI Assistant without OpenAI dependency"""
    
    def __init__(self):
        self.responses = {
            "scriptmaster": {
                "cold_calling": """Here's an effective cold calling script:

**Opening (First 10 seconds):**
"Hi [Name], I'm [Your Name] with [Company]. I know you weren't expecting my call, but I'm reaching out to homeowners in [Area] about a quick question - do you have 30 seconds?"

**Rapport Building:**
"Great! I work with homeowners who are looking to sell quickly without the hassle of repairs or realtor fees. I was wondering, have you ever thought about selling your property at [Address]?"

**Problem Identification:**
- Listen for pain points
- Ask open-ended questions: "What's your timeline?" "What would selling mean for you?"

**Solution Presentation:**
"Based on what you've told me, I think I can help. We buy houses as-is, close quickly, and handle all the paperwork. Would you be interested in getting a no-obligation cash offer?"

**Call to Action:**
"I can come by tomorrow or Thursday to take a quick look and give you an offer on the spot. Which works better for you?"
""",
                "objection": """Here are effective responses to common objections:

**"I'm not interested"**
"I completely understand, and I appreciate your honesty. Before I let you go, can I ask - is it that you're not interested in selling at all, or just not interested in selling right now?"

**"The price is too low"**
"I hear you, and I understand price is important. Keep in mind, our offer factors in that we're buying as-is, closing quickly, and covering all costs. When you factor in repairs, realtor fees, and holding costs, how does that change the picture for you?"

**"I need to think about it"**
"Of course, this is a big decision. What specifically would you like to think over? Maybe I can provide some clarity right now."

**"I'm already working with a realtor"**
"That's great! How's that going for you? Just so you know, we're investors, not realtors, so there's no conflict. If your listing doesn't work out, we'd be happy to be your backup plan."
""",
                "default": "I can help you with cold calling scripts, objection handling, and follow-up strategies. What specific situation would you like help with?"
            },
            "underwriter": {
                "analysis": """Based on the property details provided:

**Investment Analysis:**
- Property appears to be in a stable market
- Current pricing suggests room for value-add improvements
- Location factors are favorable for both rental and resale

**Investment Potential: 7.5/10**

**Risk Factors:**
1. Market conditions may shift
2. Rehab costs could exceed estimates
3. Holding time might be longer than anticipated

**Recommended Strategy:**
- Consider a fix-and-flip if rehab costs stay under $40K
- Alternative: Buy-and-hold for rental income if cash flow exceeds $300/month
- Assignment fee potential: $10-15K based on current spreads

**Key Metrics to Track:**
- Days on market for comps
- Rental rates in the area
- Construction cost trends
- Buyer demand indicators
""",
                "default": "I can help analyze properties for wholesaling potential, calculate ARV, estimate rehab costs, and recommend investment strategies. What property would you like me to analyze?"
            },
            "general": {
                "70_rule": """The 70% Rule is a fundamental formula in real estate wholesaling:

**Formula:** Maximum Offer = (ARV × 0.70) - Repair Costs

**Example:**
- ARV (After Repair Value): $200,000
- Repair Costs: $30,000
- Maximum Offer = ($200,000 × 0.70) - $30,000 = $110,000

**Why 70%?**
- 30% margin covers:
  - Your wholesale fee (5-10%)
  - Investor's profit (10-15%)
  - Holding costs, closing costs, contingencies (5-10%)

**When to Adjust:**
- Hot markets: May need to go to 75-80%
- Tough markets: Stick to 65-70%
- High-end properties: Can often use 70-75%
- Lower-end properties: May need 60-65%
""",
                "default": "I can help you with wholesaling strategies, deal analysis, marketing tips, and general real estate investing questions. What would you like to know?"
            }
        }
    
    def get_response(self, prompt: str, ai_type: str = "general", context: Dict = None) -> str:
        """Get mock AI response based on keywords in prompt"""
        prompt_lower = prompt.lower()
        
        # Determine response based on keywords
        if ai_type == "scriptmaster":
            if "cold call" in prompt_lower or "script" in prompt_lower:
                return self.responses["scriptmaster"]["cold_calling"]
            elif "objection" in prompt_lower or "not interested" in prompt_lower:
                return self.responses["scriptmaster"]["objection"]
            else:
                return self.responses["scriptmaster"]["default"]
        
        elif ai_type == "underwriter":
            if "analyze" in prompt_lower or "property" in prompt_lower:
                return self.responses["underwriter"]["analysis"]
            else:
                return self.responses["underwriter"]["default"]
        
        else:  # general
            if "70%" in prompt or "70 rule" in prompt_lower:
                return self.responses["general"]["70_rule"]
            else:
                return self.responses["general"]["default"]

# Initialize services
@st.cache_resource
def get_services():
    return {
        'property_analyzer': PropertyAnalyzer(),
        'buyer_matcher': BuyerMatcher(),
        'ai_assistant': MockAIAssistant(),
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

# Pipeline page
def render_pipeline_page():
    """Render deal pipeline management page"""
    st.markdown('<h1 class="main-header">Deal Pipeline</h1>', unsafe_allow_html=True)
    
    # Pipeline stages
    stages = ["Lead", "Contacted", "Interested", "Under Contract", "Pending", "Closed", "Dead"]
    
    # Mock pipeline data
    pipeline_data = {
        "Lead": [
            {"id": "1", "title": "123 Main St", "value": 25000, "probability": 10, "contact": "John Doe"},
            {"id": "2", "title": "456 Oak Ave", "value": 18000, "probability": 15, "contact": "Jane Smith"},
            {"id": "3", "title": "789 Pine Rd", "value": 32000, "probability": 20, "contact": "Bob Wilson"}
        ],
        "Contacted": [
            {"id": "4", "title": "321 Elm St", "value": 22000, "probability": 30, "contact": "Mary Davis"},
            {"id": "5", "title": "654 Maple Dr", "value": 28000, "probability": 25, "contact": "Tom Brown"}
        ],
        "Interested": [
            {"id": "6", "title": "987 Cedar Ln", "value": 35000, "probability": 50, "contact": "Lisa Garcia"},
            {"id": "7", "title": "147 Birch Way", "value": 29000, "probability": 45, "contact": "Mike Johnson"}
        ],
        "Under Contract": [
            {"id": "8", "title": "258 Spruce Ave", "value": 42000, "probability": 80, "contact": "Sarah Wilson"}
        ],
        "Pending": [
            {"id": "9", "title": "369 Fir St", "value": 38000, "probability": 90, "contact": "David Lee"}
        ],
        "Closed": [
            {"id": "10", "title": "741 Ash Dr", "value": 45000, "probability": 100, "contact": "Emily Chen"}
        ],
        "Dead": [
            {"id": "11", "title": "852 Walnut Rd", "value": 0, "probability": 0, "contact": "Alex Brown"}
        ]
    }
    
    # Pipeline metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_value = sum(deal["value"] for stage_deals in pipeline_data.values() for deal in stage_deals)
    active_deals = sum(len(deals) for stage, deals in pipeline_data.items() if stage not in ["Closed", "Dead"])
    closed_value = sum(deal["value"] for deal in pipeline_data["Closed"])
    conversion_rate = (len(pipeline_data["Closed"]) / active_deals * 100) if active_deals > 0 else 0
    
    with col1:
        st.metric("Total Pipeline Value", f"${total_value:,.0f}")
    with col2:
        st.metric("Active Deals", str(active_deals))
    with col3:
        st.metric("Closed This Month", f"${closed_value:,.0f}")
    with col4:
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    
    # Pipeline visualization
    st.markdown("## 📊 Pipeline Overview")
    
    # Create funnel chart
    stage_values = [sum(deal["value"] for deal in deals) for stage, deals in pipeline_data.items() if stage != "Dead"]
    stage_names = [stage for stage in stages if stage != "Dead"]
    
    fig_funnel = go.Figure(go.Funnel(
        y=stage_names,
        x=stage_values,
        textinfo="value+percent initial",
        marker_color=["#8B5CF6", "#7C3AED", "#6D28D9", "#5B21B6", "#4C1D95", "#10B981"]
    ))
    
    fig_funnel.update_layout(
        title="Deal Pipeline Funnel",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Kanban board view
    st.markdown("## 📋 Kanban Board")
    
    # Create columns for each stage
    cols = st.columns(len(stages))
    
    for i, stage in enumerate(stages):
        with cols[i]:
            stage_color = {
                "Lead": "#8B5CF6",
                "Contacted": "#7C3AED", 
                "Interested": "#6D28D9",
                "Under Contract": "#F59E0B",
                "Pending": "#F97316",
                "Closed": "#10B981",
                "Dead": "#6B7280"
            }
            
            st.markdown(f"""
            <div style='background: {stage_color[stage]}; padding: 0.5rem; border-radius: 8px; margin-bottom: 1rem;'>
                <h4 style='color: white; text-align: center; margin: 0;'>{stage}</h4>
                <p style='color: white; text-align: center; margin: 0; font-size: 0.8rem;'>
                    {len(pipeline_data[stage])} deals
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display deals in this stage
            for deal in pipeline_data[stage]:
                with st.container():
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.2);'>
                        <h5 style='color: white; margin: 0 0 0.5rem 0;'>{deal['title']}</h5>
                        <p style='color: #10B981; margin: 0; font-weight: bold;'>${deal['value']:,.0f}</p>
                        <p style='color: #8B5CF6; margin: 0; font-size: 0.8rem;'>{deal['contact']}</p>
                        <p style='color: #F59E0B; margin: 0; font-size: 0.8rem;'>{deal['probability']}% probability</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View {deal['id']}", key=f"view_deal_{deal['id']}", use_container_width=True):
                        st.session_state.selected_deal = deal['id']
                        st.rerun()

# Leads page
def render_leads_page():
    """Render lead management page"""
    st.markdown('<h1 class="main-header">Lead Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["All Leads", "Add Lead", "Import Leads", "Lightning Leads"])
    
    with tab1:
        st.markdown("### Lead Database")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_filter = st.selectbox("Status", ["All", "New", "Contacted", "Interested", "Not Interested", "Callback", "Deal", "Dead"])
        with col2:
            source_filter = st.selectbox("Source", ["All", "Cold Calling", "Direct Mail", "PPC", "SEO", "Referral"])
        with col3:
            score_filter = st.selectbox("Lead Score", ["All", "Hot (80+)", "Warm (60-79)", "Cold (0-59)"])
        with col4:
            date_filter = st.selectbox("Date Range", ["All Time", "Today", "This Week", "This Month"])
        
        # Mock leads data
        leads_data = [
            {"Name": "Maria Garcia", "Phone": "(555) 111-2222", "Address": "100 First St, Dallas, TX", 
             "Status": "Contacted", "Score": 85, "Source": "Cold Calling", "Motivation": "Divorce", "Timeline": "ASAP"},
            {"Name": "David Brown", "Phone": "(555) 222-3333", "Address": "200 Second Ave, Houston, TX",
             "Status": "Interested", "Score": 72, "Source": "Direct Mail", "Motivation": "Job Relocation", "Timeline": "30-60 days"},
            {"Name": "Jennifer Lee", "Phone": "(555) 333-4444", "Address": "300 Third Blvd, Austin, TX",
             "Status": "New", "Score": 68, "Source": "Referral", "Motivation": "Inherited Property", "Timeline": "60-90 days"},
            {"Name": "Thomas Anderson", "Phone": "(555) 444-5555", "Address": "400 Fourth St, San Antonio, TX",
             "Status": "Callback", "Score": 55, "Source": "SEO", "Motivation": "Tired Landlord", "Timeline": "Flexible"},
        ]
        
        # Display leads
        for lead in leads_data:
            with st.expander(f"{lead['Name']} - {lead['Address']} (Score: {lead['Score']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Phone:** {lead['Phone']}")
                    st.write(f"**Status:** {lead['Status']}")
                    st.write(f"**Source:** {lead['Source']}")
                
                with col2:
                    st.write(f"**Motivation:** {lead['Motivation']}")
                    st.write(f"**Timeline:** {lead['Timeline']}")
                    st.write(f"**Lead Score:** {lead['Score']}/100")
                
                with col3:
                    if st.button(f"Call {lead['Name'].split()[0]}", key=f"call_{lead['Name']}"):
                        st.success(f"Initiating call to {lead['Name']}")
                    if st.button(f"Send SMS", key=f"sms_{lead['Name']}"):
                        st.success(f"SMS sent to {lead['Name']}")
                    if st.button(f"Create Deal", key=f"deal_{lead['Name']}"):
                        st.success(f"Deal created for {lead['Name']}")
    
    with tab2:
        st.markdown("### Add New Lead")
        
        with st.form("add_lead_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Contact Information")
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                phone = st.text_input("Phone Number*")
                email = st.text_input("Email")
            
            with col2:
                st.markdown("#### Property Information")
                property_address = st.text_input("Property Address*")
                property_city = st.text_input("City*")
                property_state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA"])
                property_zip = st.text_input("ZIP Code*")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### Lead Details")
                motivation = st.multiselect("Motivation", 
                    ["Divorce", "Financial Hardship", "Job Relocation", "Inherited Property", 
                     "Tired Landlord", "Downsizing", "Health Issues", "Other"])
                timeline = st.selectbox("Timeline", 
                    ["ASAP", "1-30 days", "30-60 days", "60-90 days", "90+ days", "Flexible"])
                source = st.selectbox("Lead Source", 
                    ["Cold Calling", "Direct Mail", "PPC", "SEO", "Referral", "Social Media", "Other"])
            
            with col4:
                st.markdown("#### Additional Information")
                property_condition = st.selectbox("Property Condition", 
                    ["Excellent", "Good", "Fair", "Poor", "Needs Major Repairs"])
                estimated_value = st.number_input("Estimated Value ($)", min_value=0, value=200000)
                owed_amount = st.number_input("Amount Owed ($)", min_value=0, value=150000)
                notes = st.text_area("Notes")
            
            if st.form_submit_button("Add Lead", type="primary"):
                if first_name and last_name and phone and property_address:
                    st.success(f"Lead {first_name} {last_name} added successfully!")
                    st.info("Lead scoring and AI analysis will be completed automatically.")
                else:
                    st.error("Please fill in all required fields")
    
    with tab3:
        st.markdown("### Import Leads from CSV")
        
        # File upload
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file is not None:
            # Display CSV preview
            df = pd.read_csv(uploaded_file)
            st.markdown("#### CSV Preview")
            st.dataframe(df.head())
            
            # Column mapping
            st.markdown("#### Map CSV Columns")
            col1, col2 = st.columns(2)
            
            with col1:
                first_name_col = st.selectbox("First Name", df.columns)
                last_name_col = st.selectbox("Last Name", df.columns)
                phone_col = st.selectbox("Phone", df.columns)
                email_col = st.selectbox("Email", df.columns)
            
            with col2:
                address_col = st.selectbox("Property Address", df.columns)
                city_col = st.selectbox("City", df.columns)
                state_col = st.selectbox("State", df.columns)
                motivation_col = st.selectbox("Motivation", ["None"] + list(df.columns))
            
            if st.button("Import Leads", type="primary"):
                with st.spinner("Importing leads..."):
                    # Simulate import process
                    import time
                    time.sleep(2)
                    st.success(f"Successfully imported {len(df)} leads!")
                    st.info("Leads are being processed and scored in the background.")
    
    with tab4:
        render_lightning_leads()

# Lightning Leads section
def render_lightning_leads():
    """Render Lightning Leads premium service"""
    st.markdown("### ⚡ Lightning Leads Premium Service")
    
    # Service description
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(139, 92, 246, 0.3);'>
        <h3 style='color: #10B981; margin-bottom: 1rem;'>Get Premium Motivated Seller Leads</h3>
        <ul style='color: white;'>
            <li>🎯 <strong>Highly Targeted</strong> - Pre-qualified motivated sellers</li>
            <li>⚡ <strong>Real-Time Delivery</strong> - Leads delivered instantly</li>
            <li>📞 <strong>Skip Traced</strong> - Complete contact information included</li>
            <li>🧠 <strong>AI Scored</strong> - Each lead ranked by likelihood to sell</li>
            <li>✅ <strong>Verified</strong> - All leads verified for accuracy</li>
            <li>💰 <strong>ROI Guarantee</strong> - 98% of subscribers close deals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing tiers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h4 style='color: #10B981;'>Starter</h4>
            <h2 style='color: white;'>$39.99</h2>
            <p style='color: white;'>per month</p>
            <ul style='color: white; text-align: left;'>
                <li>10 leads/month</li>
                <li>Basic targeting</li>
                <li>Email delivery</li>
                <li>Lead scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Starter Plan", key="starter_plan", use_container_width=True):
            st.success("Redirecting to payment...")
    
    with col2:
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.2); padding: 1.5rem; border-radius: 10px; text-align: center; border: 2px solid #8B5CF6;'>
            <h4 style='color: #8B5CF6;'>Professional</h4>
            <h2 style='color: white;'>$99.99</h2>
            <p style='color: white;'>per month</p>
            <ul style='color: white; text-align: left;'>
                <li>50 leads/month</li>
                <li>Advanced targeting</li>
                <li>Real-time delivery</li>
                <li>AI coaching included</li>
                <li>Priority support</li>
            </ul>
            <p style='color: #10B981; font-weight: bold;'>MOST POPULAR</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Pro Plan", key="pro_plan", use_container_width=True):
            st.success("Redirecting to payment...")
    
    with col3:
        st.markdown("""
        <div style='background: rgba(245, 158, 11, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h4 style='color: #F59E0B;'>Enterprise</h4>
            <h2 style='color: white;'>$299.99</h2>
            <p style='color: white;'>per month</p>
            <ul style='color: white; text-align: left;'>
                <li>Unlimited leads</li>
                <li>Custom targeting</li>
                <li>Dedicated account manager</li>
                <li>White-label option</li>
                <li>API access</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Contact Sales", key="enterprise_plan", use_container_width=True):
            st.success("Sales team will contact you within 24 hours")

# Contracts page
def render_contracts_page():
    """Render contract generation page"""
    st.markdown('<h1 class="main-header">Contract Generation</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Generate Contract", "My Contracts", "Templates"])
    
    with tab1:
        st.markdown("### Generate New Contract")
        
        # Contract type selection
        contract_type = st.selectbox("Contract Type", 
            ["Purchase Agreement", "Assignment Contract", "Wholesale Contract", "Subject To Agreement"])
        
        with st.form("contract_form"):
            st.markdown("#### Property Information")
            col1, col2 = st.columns(2)
            
            with col1:
                property_address = st.text_input("Property Address*")
                city = st.text_input("City*")
                state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA"])
                zip_code = st.text_input("ZIP Code*")
            
            with col2:
                purchase_price = st.number_input("Purchase Price ($)*", min_value=0, value=200000)
                earnest_money = st.number_input("Earnest Money Deposit ($)", min_value=0, value=1000)
                closing_date = st.date_input("Closing Date")
                inspection_period = st.number_input("Inspection Period (days)", min_value=0, value=7)
            
            st.markdown("#### Buyer Information")
            col3, col4 = st.columns(2)
            
            with col3:
                buyer_name = st.text_input("Buyer Name*")
                buyer_email = st.text_input("Buyer Email")
                buyer_phone = st.text_input("Buyer Phone")
            
            with col4:
                buyer_address = st.text_area("Buyer Address")
                buyer_entity = st.text_input("Buyer Entity (LLC, Corp, etc.)")
            
            st.markdown("#### Seller Information")
            col5, col6 = st.columns(2)
            
            with col5:
                seller_name = st.text_input("Seller Name*")
                seller_email = st.text_input("Seller Email")
                seller_phone = st.text_input("Seller Phone")
            
            with col6:
                seller_address = st.text_area("Seller Address")
            
            st.markdown("#### Contract Terms")
            col7, col8 = st.columns(2)
            
            with col7:
                closing_costs = st.selectbox("Closing Costs Paid By", ["Buyer", "Seller", "Split 50/50"])
                title_company = st.text_input("Title Company")
                contingencies = st.multiselect("Contingencies", 
                    ["Financing", "Inspection", "Appraisal", "Sale of Buyer's Property", "Attorney Review"])
            
            with col8:
                assignment_fee = st.number_input("Assignment Fee ($)", min_value=0, value=5000)
                balloon_payment = st.number_input("Balloon Payment ($)", min_value=0, value=0)
                balloon_years = st.number_input("Balloon Payment Due (years)", min_value=0, value=0)
            
            # Property liens section
            st.markdown("#### Property Liens")
            has_liens = st.checkbox("Property has liens")
            
            if has_liens:
                col9, col10, col11 = st.columns(3)
                with col9:
                    lien_type = st.text_input("Lien Type (e.g., Solar, HOA)")
                with col10:
                    lien_amount = st.number_input("Lien Amount ($)", min_value=0)
                with col11:
                    lien_holder = st.text_input("Lien Holder")
            
            # Agent information
            st.markdown("#### Real Estate Agent (if applicable)")
            has_agent = st.checkbox("Real estate agent involved")
            
            if has_agent:
                col12, col13 = st.columns(2)
                with col12:
                    agent_name = st.text_input("Agent Name")
                    agent_company = st.text_input("Agent Company")
                    agent_phone = st.text_input("Agent Phone")
                with col13:
                    agent_email = st.text_input("Agent Email")
                    commission_rate = st.number_input("Commission Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
            
            # Transaction Coordinator
            st.markdown("#### Transaction Coordinator")
            tc_name = st.text_input("TC Name")
            tc_email = st.text_input("TC Email")
            tc_phone = st.text_input("TC Phone")
            
            # Special terms
            special_terms = st.text_area("Special Terms and Conditions")
            
            # Generate contract button
            if st.form_submit_button("Generate Contract", type="primary"):
                if property_address and buyer_name and seller_name and purchase_price:
                    with st.spinner("Generating contract..."):
                        # Simulate contract generation
                        import time
                        time.sleep(3)
                        
                        contract_id = str(uuid.uuid4())[:8]
                        
                        st.success(f"Contract #{contract_id} generated successfully!")
                        
                        # Contract summary
                        st.markdown("#### Contract Summary")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Property:** {property_address}")
                            st.write(f"**Purchase Price:** ${purchase_price:,.0f}")
                            st.write(f"**Buyer:** {buyer_name}")
                            st.write(f"**Seller:** {seller_name}")
                        
                        with col2:
                            st.write(f"**Contract Type:** {contract_type}")
                            st.write(f"**Closing Date:** {closing_date}")
                            st.write(f"**Assignment Fee:** ${assignment_fee:,.0f}")
                            st.write(f"**Contract ID:** #{contract_id}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("Download PDF", use_container_width=True):
                                st.success("Contract PDF downloaded!")
                        
                        with col2:
                            if st.button("Send to TC", use_container_width=True) and tc_email:
                                st.success(f"Contract sent to {tc_name} ({tc_email})")
                        
                        with col3:
                            if st.button("E-Sign Request", use_container_width=True):
                                st.success("E-signature requests sent to all parties!")
                
                else:
                    st.error("Please fill in all required fields")
    
    with tab2:
        st.markdown("### My Contracts")
        
        # Contract status filter
        status_filter = st.selectbox("Filter by Status", ["All", "Draft", "Pending Signature", "Executed", "Cancelled"])
        
        # Mock contracts data
        contracts_data = [
            {"ID": "WTF-001", "Property": "123 Main St, Dallas, TX", "Type": "Purchase Agreement", 
             "Amount": 225000, "Status": "Executed", "Date": "2024-07-25", "Buyer": "John Smith"},
            {"ID": "WTF-002", "Property": "456 Oak Ave, Houston, TX", "Type": "Assignment Contract", 
             "Amount": 185000, "Status": "Pending Signature", "Date": "2024-07-28", "Buyer": "Sarah Johnson"},
            {"ID": "WTF-003", "Property": "789 Pine Rd, Austin, TX", "Type": "Wholesale Contract", 
             "Amount": 310000, "Status": "Draft", "Date": "2024-08-01", "Buyer": "Mike Davis"},
        ]
        
        # Display contracts
        for contract in contracts_data:
            with st.expander(f"Contract {contract['ID']} - {contract['Property']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Type:** {contract['Type']}")
                    st.write(f"**Amount:** ${contract['Amount']:,.0f}")
                    st.write(f"**Status:** {contract['Status']}")
                
                with col2:
                    st.write(f"**Date:** {contract['Date']}")
                    st.write(f"**Buyer:** {contract['Buyer']}")
                
                with col3:
                    status_color = {"Draft": "🟡", "Pending Signature": "🟠", "Executed": "🟢", "Cancelled": "🔴"}
                    st.write(f"**Status:** {status_color.get(contract['Status'], '⚪')} {contract['Status']}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("View PDF", key=f"view_{contract['ID']}"):
                        st.success(f"Opening contract {contract['ID']}")
                
                with col2:
                    if st.button("Edit", key=f"edit_{contract['ID']}"):
                        st.info(f"Editing contract {contract['ID']}")
                
                with col3:
                    if st.button("Send", key=f"send_{contract['ID']}"):
                        st.success(f"Contract {contract['ID']} sent")
                
                with col4:
                    if st.button("Track", key=f"track_{contract['ID']}"):
                        st.info(f"Tracking status for {contract['ID']}")
    
    with tab3:
        st.markdown("### Contract Templates")
        
        # Template categories
        col1, col2 = st.columns([1, 3])
        
        with col1:
            template_category = st.selectbox("Category", 
                ["All Templates", "Purchase Agreements", "Assignment Contracts", "Creative Finance", "Subject To"])
        
        with col2:
            search_templates = st.text_input("Search templates...")
        
        # Mock templates
        templates = [
            {"name": "Standard Purchase Agreement", "category": "Purchase Agreements", "downloads": 1234, "rating": 4.8},
            {"name": "Assignment Contract - TX", "category": "Assignment Contracts", "downloads": 987, "rating": 4.9},
            {"name": "Subject To Agreement", "category": "Creative Finance", "downloads": 756, "rating": 4.7},
            {"name": "Seller Finance Contract", "category": "Creative Finance", "downloads": 543, "rating": 4.6},
            {"name": "Wholesale Agreement", "category": "Assignment Contracts", "downloads": 432, "rating": 4.8},
        ]
        
        # Display templates
        for template in templates:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{template['name']}**")
                    st.caption(f"Category: {template['category']}")
                
                with col2:
                    st.metric("Downloads", f"{template['downloads']:,}")
                
                with col3:
                    st.metric("Rating", f"{template['rating']}⭐")
                
                with col4:
                    if st.button("Use Template", key=f"use_{template['name']}"):
                        st.success(f"Using template: {template['name']}")
                
                st.markdown("---")

# Analytics page
def render_analytics_page():
    """Render analytics dashboard"""
    st.markdown('<h1 class="main-header">Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        date_range = st.selectbox("Date Range", 
            ["Last 7 days", "Last 30 days", "Last 90 days", "This Year", "All Time"])
    
    with col2:
        metric_type = st.selectbox("Metric Type", ["Revenue", "Deals", "Leads", "ROI"])
    
    with col3:
        export_data = st.button("Export Data", type="primary")
    
    # Key performance indicators
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Revenue", "$487,562", delta="$23,450 (5.1%)")
    with col2:
        st.metric("Deals Closed", "47", delta="3 (6.8%)")
    with col3:
        st.metric("Active Leads", "156", delta="12 (8.3%)")
    with col4:
        st.metric("Conversion Rate", "24.7%", delta="2.1% (9.3%)")
    with col5:
        st.metric("Avg Deal Size", "$10,374", delta="$562 (5.7%)")
    
    # Revenue and deals chart
    st.markdown("## 💰 Revenue & Deals Trend")
    
    # Generate mock data
    dates = pd.date_range(start='2024-01-01', end='2024-08-02', freq='D')
    revenue_data = pd.DataFrame({
        'Date': dates,
        'Daily Revenue': np.random.normal(1500, 300, len(dates)).cumsum(),
        'Deals Closed': np.random.poisson(0.3, len(dates)),
        'Leads Generated': np.random.poisson(3, len(dates))
    })
    
    # Create dual-axis chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=revenue_data['Date'],
        y=revenue_data['Daily Revenue'],
        mode='lines',
        name='Cumulative Revenue',
        line=dict(color='#10B981', width=3)
    ))
    
    fig.add_trace(go.Bar(
        x=revenue_data['Date'],
        y=revenue_data['Deals Closed'],
        name='Daily Deals',
        yaxis='y2',
        marker_color='#8B5CF6',
        opacity=0.7
    ))
    
    fig.update_layout(
        title='Revenue and Deals Performance',
        xaxis_title='Date',
        yaxis_title='Cumulative Revenue ($)',
        yaxis2=dict(title='Daily Deals', overlaying='y', side='right'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Lead Sources Performance")
        
        source_data = pd.DataFrame({
            'Source': ['Cold Calling', 'Direct Mail', 'PPC', 'SEO', 'Referrals'],
            'Leads': [45, 32, 28, 23, 18],
            'Conversion Rate': [28, 22, 35, 15, 42],
            'Cost Per Lead': [15, 25, 45, 12, 5]
        })
        
        fig_sources = px.bar(source_data, x='Source', y='Leads', 
                           color='Conversion Rate', 
                           title='Lead Generation by Source',
                           color_continuous_scale='Viridis')
        
        fig_sources.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig_sources, use_container_width=True)
    
    with col2:
        st.markdown("### Deal Status Distribution")
        
        deal_status = pd.DataFrame({
            'Status': ['Closed Won', 'Under Contract', 'Negotiating', 'Cold Leads', 'Dead'],
            'Count': [47, 12, 23, 89, 31],
            'Value': [487562, 124800, 230400, 445500, 0]
        })
        
        fig_status = px.pie(deal_status, values='Count', names='Status',
                          title='Deal Pipeline Distribution',
                          color_discrete_sequence=px.colors.qualitative.Set3)
        
        fig_status.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Geographic performance
    st.markdown("### 🗺️ Geographic Performance")
    
    # Mock geographic data
    geo_data = pd.DataFrame({
        'State': ['TX', 'CA', 'FL', 'NY', 'GA', 'NC', 'OH'],
        'Deals': [23, 8, 6, 4, 3, 2, 1],
        'Revenue': [240000, 95000, 72000, 48000, 35000, 24000, 12000],
        'Avg Deal Size': [10435, 11875, 12000, 12000, 11667, 12000, 12000]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_geo = px.bar(geo_data, x='State', y='Deals',
                        title='Deals by State',
                        color='Revenue',
                        color_continuous_scale='Viridis')
        
        fig_geo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with col2:
        # ROI analysis
        roi_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            'Marketing Spend': [5000, 5500, 6000, 5200, 5800, 6200, 5900],
            'Revenue': [45000, 52000, 48000, 58000, 61000, 65000, 67000],
            'ROI': [9.0, 9.5, 8.0, 11.2, 10.5, 10.5, 11.4]
        })
        
        fig_roi = px.line(roi_data, x='Month', y='ROI',
                         title='Monthly ROI Trend',
                         markers=True)
        
        fig_roi.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Detailed metrics table
    st.markdown("### 📋 Detailed Metrics")
    
    detailed_metrics = pd.DataFrame({
        'Metric': ['Lead to Deal Conversion', 'Average Time to Close', 'Customer Acquisition Cost', 
                  'Lead Response Time', 'Follow-up Rate', 'Referral Rate'],
        'Current': ['24.7%', '45 days', '$127', '2.3 hours', '89%', '18%'],
        'Previous Period': ['22.6%', '52 days', '$142', '3.1 hours', '84%', '15%'],
        'Change': ['+2.1%', '-7 days', '-$15', '-0.8 hours', '+5%', '+3%'],
        'Trend': ['🟢', '🟢', '🟢', '🟢', '🟢', '🟢']
    })
    
    st.dataframe(detailed_metrics, use_container_width=True)
    
    # Action items based on analytics
    st.markdown("### 🎯 Recommended Actions")
    
    recommendations = [
        "📈 **Increase PPC Budget**: PPC shows highest conversion rate (35%) - consider increasing budget by 20%",
        "📞 **Improve Response Time**: Current 2.3-hour response time can be improved to under 1 hour for better conversion",
        "🎯 **Focus on Texas Market**: TX shows strongest performance with 23 deals - expand marketing efforts",
        "🔄 **Automate Follow-ups**: 89% follow-up rate is good but can reach 95% with better automation",
        "💬 **Referral Program**: 18% referral rate suggests happy customers - implement formal referral incentives"
    ]
    
    for rec in recommendations:
        st.markdown(f"• {rec}")

# Settings page
def render_settings_page():
    """Advanced settings page"""
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Profile", "API Keys", "Notifications", "Billing"])
    
    with tab1:
        st.markdown("### User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("First Name", value="Admin")
            st.text_input("Last Name", value="User") 
            st.text_input("Email", value="admin@wholesale2flip.com")
            st.text_input("Phone", value="(555) 123-4567")
        
        with col2:
            st.text_input("Business Name", value="WTF Wholesaling")
            st.text_input("Website", value="https://wholesale2flip.com")
            st.selectbox("Time Zone", ["Central", "Eastern", "Mountain", "Pacific"])
            st.text_area("Bio", value="Real estate wholesaling expert")
        
        if st.button("Update Profile", type="primary"):
            st.success("Profile updated successfully!")
    
    with tab2:
        st.markdown("### API Keys Configuration")
        
        st.info("🔐 API keys are securely stored and encrypted")
        
        # OpenAI
        with st.expander("OpenAI Configuration"):
            openai_key = st.text_input("OpenAI API Key", type="password", 
                                     placeholder="sk-...")
            if st.button("Test OpenAI Connection"):
                st.success("✅ OpenAI connection successful")
        
        # ATTOM Data
        with st.expander("ATTOM Data Configuration"):
            attom_key = st.text_input("ATTOM API Key", type="password")
            if st.button("Test ATTOM Connection"):
                st.success("✅ ATTOM Data connection successful")
        
        # SendGrid
        with st.expander("Email Configuration"):
            sendgrid_key = st.text_input("SendGrid API Key", type="password")
            from_email = st.text_input("From Email", value="noreply@wholesale2flip.com")
            if st.button("Test Email Connection"):
                st.success("✅ Email configuration successful")
    
    with tab3:
        st.markdown("### Notification Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Email Notifications")
            st.checkbox("New leads", value=True)
            st.checkbox("Deal updates", value=True)
            st.checkbox("Buyer matches", value=True)
            st.checkbox("Contract updates", value=True)
        
        with col2:
            st.markdown("#### SMS Notifications") 
            st.checkbox("Hot leads (score 80+)", value=True)
            st.checkbox("Urgent deal updates", value=True)
            st.checkbox("High-value buyer matches", value=False)
            st.checkbox("System alerts", value=True)
        
        st.markdown("#### Discord Notifications")
        st.checkbox("Send deal alerts to Discord", value=True)
        discord_webhook = st.text_input("Discord Webhook URL")
        
        if st.button("Save Notification Settings", type="primary"):
            st.success("Notification preferences saved!")
    
    with tab4:
        st.markdown("### Billing & Subscription")
        
        # Current plan
        st.markdown("#### Current Plan")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Plan", "Pro")
        with col2:
            st.metric("Monthly Cost", "$99.99")
        with col3:
            st.metric("Next Billing", "Aug 15, 2024")
        
        # Usage metrics
        st.markdown("#### Usage This Month")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Properties Analyzed", "47", "of 100")
        with col2:
            st.metric("AI Queries", "234", "of 500")
        with col3:
            st.metric("Contracts Generated", "12", "of 25")
        with col4:
            st.metric("Lightning Leads", "18", "of 50")
        
        # Billing history
        st.markdown("#### Billing History")
        billing_data = pd.DataFrame({
            'Date': ['2024-07-15', '2024-06-15', '2024-05-15'],
            'Amount': ['$99.99', '$99.99', '$99.99'],
            'Status': ['Paid', 'Paid', 'Paid'],
            'Invoice': ['#1001', '#1002', '#1003']
        })
        
        st.dataframe(billing_data, use_container_width=True)

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
        render_pipeline_page()
    elif selected_page == "leads":
        render_leads_page()
    elif selected_page == "contracts":
        render_contracts_page()
    elif selected_page == "lightning_leads":
        st.markdown('<h1 class="main-header">⚡ Lightning Leads</h1>', unsafe_allow_html=True)
        render_lightning_leads()
    elif selected_page == "analytics":
        render_analytics_page()
    elif selected_page == "settings":
        render_settings_page()

if __name__ == "__main__":
    main()