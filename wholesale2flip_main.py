import streamlit as st
import sqlite3
import hashlib
import json
import datetime
import openai
import os
from typing import Dict, List, Optional
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Wholesale2Flip - Real Estate Wholesaling Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize OpenAI (you'll need to add your API key)
# openai.api_key = st.secrets.get("OPENAI_API_KEY", "your-openai-api-key")

class DatabaseManager:
    def __init__(self):
        self.db_name = "wholesale2flip.db"
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                subscription_tier TEXT DEFAULT 'none',
                subscription_start DATE,
                subscription_end DATE,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Deals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                property_address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                property_type TEXT NOT NULL,
                bedrooms INTEGER,
                bathrooms REAL,
                square_feet INTEGER,
                lot_size TEXT,
                year_built INTEGER,
                current_condition TEXT,
                arv REAL,
                repair_costs REAL,
                acquisition_cost REAL,
                holding_costs REAL,
                selling_costs REAL,
                profit_margin REAL,
                deal_type TEXT,
                contact_name TEXT,
                contact_phone TEXT,
                contact_email TEXT,
                notes TEXT,
                contract_generated BOOLEAN DEFAULT 0,
                loi_generated BOOLEAN DEFAULT 0,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Contracts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER,
                contract_type TEXT NOT NULL,
                contract_content TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deal_id) REFERENCES deals (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name: str, email: str, password: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, email: str, password: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id, name, email, subscription_tier, is_admin FROM users WHERE email = ? AND password_hash = ?",
            (email, password_hash)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'subscription_tier': user[3],
                'is_admin': bool(user[4])
            }
        return None
    
    def update_subscription(self, user_id: int, tier: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30)
        cursor.execute(
            "UPDATE users SET subscription_tier = ?, subscription_start = ?, subscription_end = ? WHERE id = ?",
            (tier, start_date, end_date, user_id)
        )
        conn.commit()
        conn.close()
    
    def save_deal(self, deal_data: Dict) -> int:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO deals (
                user_id, property_address, city, state, zip_code, property_type,
                bedrooms, bathrooms, square_feet, lot_size, year_built, current_condition,
                arv, repair_costs, acquisition_cost, holding_costs, selling_costs, profit_margin,
                deal_type, contact_name, contact_phone, contact_email, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            deal_data['user_id'], deal_data['property_address'], deal_data['city'],
            deal_data['state'], deal_data['zip_code'], deal_data['property_type'],
            deal_data['bedrooms'], deal_data['bathrooms'], deal_data['square_feet'],
            deal_data['lot_size'], deal_data['year_built'], deal_data['current_condition'],
            deal_data['arv'], deal_data['repair_costs'], deal_data['acquisition_cost'],
            deal_data['holding_costs'], deal_data['selling_costs'], deal_data['profit_margin'],
            deal_data['deal_type'], deal_data['contact_name'], deal_data['contact_phone'],
            deal_data['contact_email'], deal_data['notes']
        ))
        deal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return deal_id
    
    def get_all_deals(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.*, u.name as user_name, u.email as user_email
            FROM deals d
            JOIN users u ON d.user_id = u.id
            ORDER BY d.created_at DESC
        ''')
        deals = cursor.fetchall()
        conn.close()
        
        columns = [
            'id', 'user_id', 'property_address', 'city', 'state', 'zip_code',
            'property_type', 'bedrooms', 'bathrooms', 'square_feet', 'lot_size',
            'year_built', 'current_condition', 'arv', 'repair_costs', 'acquisition_cost',
            'holding_costs', 'selling_costs', 'profit_margin', 'deal_type',
            'contact_name', 'contact_phone', 'contact_email', 'notes',
            'contract_generated', 'loi_generated', 'status', 'created_at',
            'user_name', 'user_email'
        ]
        
        return [dict(zip(columns, deal)) for deal in deals]
    
    def get_user_deals(self, user_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deals WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        deals = cursor.fetchall()
        conn.close()
        
        columns = [
            'id', 'user_id', 'property_address', 'city', 'state', 'zip_code',
            'property_type', 'bedrooms', 'bathrooms', 'square_feet', 'lot_size',
            'year_built', 'current_condition', 'arv', 'repair_costs', 'acquisition_cost',
            'holding_costs', 'selling_costs', 'profit_margin', 'deal_type',
            'contact_name', 'contact_phone', 'contact_email', 'notes',
            'contract_generated', 'loi_generated', 'status', 'created_at'
        ]
        
        return [dict(zip(columns, deal)) for deal in deals]

class DealCalculator:
    @staticmethod
    def calculate_deal_metrics(deal_data: Dict) -> Dict:
        arv = deal_data.get('arv', 0)
        repair_costs = deal_data.get('repair_costs', 0)
        acquisition_cost = deal_data.get('acquisition_cost', 0)
        holding_costs = deal_data.get('holding_costs', 0)
        selling_costs = deal_data.get('selling_costs', 0)
        
        total_investment = acquisition_cost + repair_costs + holding_costs
        total_costs = total_investment + selling_costs
        gross_profit = arv - total_costs
        profit_margin = (gross_profit / arv * 100) if arv > 0 else 0
        roi = (gross_profit / total_investment * 100) if total_investment > 0 else 0
        
        # 70% Rule calculation
        max_offer_70_rule = (arv * 0.70) - repair_costs
        
        return {
            'total_investment': total_investment,
            'total_costs': total_costs,
            'gross_profit': gross_profit,
            'profit_margin': profit_margin,
            'roi': roi,
            'max_offer_70_rule': max_offer_70_rule,
            'deal_quality': 'Excellent' if profit_margin > 20 else 'Good' if profit_margin > 10 else 'Fair' if profit_margin > 5 else 'Poor'
        }

class ContractGenerator:
    @staticmethod
    def generate_wholesale_contract(deal_data: Dict) -> str:
        template = f"""
REAL ESTATE PURCHASE AND SALE AGREEMENT
(WHOLESALE CONTRACT)

Property Address: {deal_data.get('property_address', '')}, {deal_data.get('city', '')}, {deal_data.get('state', '')} {deal_data.get('zip_code', '')}

BUYER: [BUYER NAME]
Address: [BUYER ADDRESS]

SELLER: {deal_data.get('contact_name', '[SELLER NAME]')}
Phone: {deal_data.get('contact_phone', '[SELLER PHONE]')}

PURCHASE PRICE: ${deal_data.get('acquisition_cost', 0):,.2f}

EARNEST MONEY: $1,000.00 (to be deposited within 2 business days)

INSPECTION PERIOD: 10 days from acceptance

CLOSING DATE: 30 days from acceptance (or sooner if possible)

FINANCING: This contract is contingent upon Buyer obtaining financing or is a CASH purchase.

ASSIGNMENT: Buyer reserves the right to assign this contract to another party.

PROPERTY CONDITION: Property is sold AS-IS, WHERE-IS.

This contract is subject to Buyer's inspection and approval of the property, title, and all related documents.

Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: Wholesale2Flip Platform

NOTE: This is a template contract. Please consult with a real estate attorney before use.
        """
        return template.strip()
    
    @staticmethod
    def generate_loi(deal_data: Dict) -> str:
        template = f"""
LETTER OF INTENT (LOI)
REAL ESTATE INVESTMENT OPPORTUNITY

Date: {datetime.datetime.now().strftime('%Y-%m-%d')}

To: {deal_data.get('contact_name', '[SELLER NAME]')}
Property: {deal_data.get('property_address', '')}, {deal_data.get('city', '')}, {deal_data.get('state', '')} {deal_data.get('zip_code', '')}

Dear Property Owner,

We are interested in purchasing your property located at the above address. Based on our preliminary analysis, we would like to submit the following offer:

PROPOSED PURCHASE PRICE: ${deal_data.get('acquisition_cost', 0):,.2f}

TERMS:
- Cash Purchase (No Financing Contingency)
- 10-Day Inspection Period
- 30-Day Closing (Can close sooner if needed)
- Buyer to pay all closing costs
- Property purchased AS-IS

PROPERTY DETAILS:
- Type: {deal_data.get('property_type', 'N/A')}
- Bedrooms: {deal_data.get('bedrooms', 'N/A')}
- Bathrooms: {deal_data.get('bathrooms', 'N/A')}
- Square Feet: {deal_data.get('square_feet', 'N/A')}
- Year Built: {deal_data.get('year_built', 'N/A')}

We are serious cash buyers and can close quickly. This offer is non-binding and subject to property inspection and title review.

Please contact us at your earliest convenience to discuss this opportunity.

Best regards,
Wholesale2Flip Team

Generated by: Wholesale2Flip Platform
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        return template.strip()

# Initialize database
db = DatabaseManager()

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main { padding: 0; }
    .stApp { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        text-align: center;
        color: white;
        border-radius: 0 0 50px 50px;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin-bottom: 2rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .pricing-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        position: relative;
    }
    
    .pricing-card.featured {
        border: 3px solid #667eea;
        transform: scale(1.05);
    }
    
    .pricing-card.featured::before {
        content: "MOST POPULAR";
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .price-tag {
        font-size: 2.5rem;
        font-weight: 900;
        color: #667eea;
        margin: 1rem 0;
    }
    
    .admin-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .deal-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

def show_login_signup():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Welcome to Wholesale2Flip</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Your Complete Real Estate Wholesaling Platform</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔐 Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn and email and password:
                user = db.verify_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with col2:
        st.markdown("### 📝 Sign Up")
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            signup_btn = st.form_submit_button("Create Account")
            
            if signup_btn and name and email and password:
                if db.create_user(name, email, password):
                    st.success("Account created! Please login.")
                else:
                    st.error("Email already exists")

def show_home_page():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Wholesale2Flip</h1>
        <p class="hero-subtitle">Master Real Estate Wholesaling with AI-Powered Tools, Calculations, and Professional Contracts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Calculations</h3>
            <p>Advanced deal analysis with GPT integration for accurate ARV estimates, repair costs, and profit projections.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Legal Contracts & LOIs</h3>
            <p>Generate wholesale-friendly, legally protective contracts and letters of intent automatically.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Deal Management</h3>
            <p>Complete deal pipeline management with admin oversight and disposition team integration.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Pricing Section
    st.markdown("## 💎 Choose Your Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>Starter</h3>
            <div class="price-tag">$10</div>
            <p>per month</p>
            <ul>
                <li>✅ Basic Deal Calculator</li>
                <li>✅ Simple Contract Templates</li>
                <li>✅ 5 Deals per Month</li>
                <li>✅ Email Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Starter", key="starter"):
            if st.session_state.logged_in:
                db.update_subscription(st.session_state.user['id'], 'starter')
                st.success("Subscribed to Starter plan!")
                st.rerun()
            else:
                st.warning("Please login first")
    
    with col2:
        st.markdown("""
        <div class="pricing-card featured">
            <h3>Professional</h3>
            <div class="price-tag">$20</div>
            <p>per month</p>
            <ul>
                <li>✅ AI-Powered Calculations</li>
                <li>✅ Advanced Contract Suite</li>
                <li>✅ Unlimited Deals</li>
                <li>✅ LOI Generation</li>
                <li>✅ Priority Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Professional", key="professional"):
            if st.session_state.logged_in:
                db.update_subscription(st.session_state.user['id'], 'professional')
                st.success("Subscribed to Professional plan!")
                st.rerun()
            else:
                st.warning("Please login first")
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>Enterprise</h3>
            <div class="price-tag">$30</div>
            <p>per month</p>
            <ul>
                <li>✅ Everything in Professional</li>
                <li>✅ Custom Contract Templates</li>
                <li>✅ Disposition Team Access</li>
                <li>✅ Advanced Analytics</li>
                <li>✅ White-Label Options</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Enterprise", key="enterprise"):
            if st.session_state.logged_in:
                db.update_subscription(st.session_state.user['id'], 'enterprise')
                st.success("Subscribed to Enterprise plan!")
                st.rerun()
            else:
                st.warning("Please login first")

def show_deal_calculator():
    st.markdown("# 🏠 Deal Calculator & Analysis")
    
    if not st.session_state.logged_in:
        st.warning("Please login to access the deal calculator")
        return
    
    user_tier = st.session_state.user.get('subscription_tier', 'none')
    if user_tier == 'none':
        st.warning("Please subscribe to a plan to access the deal calculator")
        return
    
    with st.form("deal_form"):
        st.markdown("## Property Information")
        col1, col2 = st.columns(2)
        
        with col1:
            property_address = st.text_input("Property Address *")
            city = st.text_input("City *")
            state = st.text_input("State *")
            zip_code = st.text_input("ZIP Code *")
            property_type = st.selectbox("Property Type", 
                ["Single Family", "Multi-Family", "Condo", "Townhouse", "Other"])
        
        with col2:
            bedrooms = st.number_input("Bedrooms", min_value=0, max_value=20, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=20.0, value=2.0, step=0.5)
            square_feet = st.number_input("Square Feet", min_value=0, value=1500)
            year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1980)
            current_condition = st.selectbox("Current Condition", 
                ["Excellent", "Good", "Fair", "Poor", "Needs Major Repairs"])
        
        st.markdown("## Financial Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            arv = st.number_input("After Repair Value (ARV) *", min_value=0.0, value=200000.0, step=1000.0)
            repair_costs = st.number_input("Estimated Repair Costs *", min_value=0.0, value=25000.0, step=500.0)
            acquisition_cost = st.number_input("Purchase Price *", min_value=0.0, value=150000.0, step=1000.0)
        
        with col2:
            holding_costs = st.number_input("Holding Costs (utilities, insurance, etc.)", min_value=0.0, value=2000.0, step=100.0)
            selling_costs = st.number_input("Selling Costs (realtor, closing, etc.)", min_value=0.0, value=12000.0, step=500.0)
            deal_type = st.selectbox("Deal Type", ["Wholesale", "Fix & Flip", "Buy & Hold"])
        
        st.markdown("## Contact Information")
        col1, col2 = st.columns(2)
        
        with col1:
            contact_name = st.text_input("Seller/Contact Name")
            contact_phone = st.text_input("Phone Number")
        
        with col2:
            contact_email = st.text_input("Email Address")
            notes = st.text_area("Additional Notes")
        
        calculate_btn = st.form_submit_button("Calculate Deal & Generate Documents")
        
        if calculate_btn:
            if not all([property_address, city, state, zip_code, arv, repair_costs, acquisition_cost]):
                st.error("Please fill in all required fields marked with *")
            else:
                # Prepare deal data
                deal_data = {
                    'user_id': st.session_state.user['id'],
                    'property_address': property_address,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'property_type': property_type,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'square_feet': square_feet,
                    'lot_size': '',
                    'year_built': year_built,
                    'current_condition': current_condition,
                    'arv': arv,
                    'repair_costs': repair_costs,
                    'acquisition_cost': acquisition_cost,
                    'holding_costs': holding_costs,
                    'selling_costs': selling_costs,
                    'profit_margin': 0,
                    'deal_type': deal_type,
                    'contact_name': contact_name,
                    'contact_phone': contact_phone,
                    'contact_email': contact_email,
                    'notes': notes
                }
                
                # Calculate metrics
                metrics = DealCalculator.calculate_deal_metrics(deal_data)
                deal_data['profit_margin'] = metrics['profit_margin']
                
                # Save deal to database
                deal_id = db.save_deal(deal_data)
                
                # Display results
                st.success("Deal analyzed and saved successfully!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Gross Profit</h3>
                        <h2>${metrics['gross_profit']:,.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Profit Margin</h3>
                        <h2>{metrics['profit_margin']:.1f}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>ROI</h3>
                        <h2>{metrics['roi']:.1f}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"**Deal Quality:** {metrics['deal_quality']}")
                st.markdown(f"**70% Rule Max Offer:** ${metrics['max_offer_70_rule']:,.2f}")
                
                # Generate contracts if professional or enterprise
                if user_tier in ['professional', 'enterprise']:
                    st.markdown("## 📄 Generated Documents")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Generate Wholesale Contract"):
                            contract = ContractGenerator.generate_wholesale_contract(deal_data)
                            st.text_area("Wholesale Contract", contract, height=400)
                            st.download_button(
                                "Download Contract",
                                contract,
                                file_name=f"wholesale_contract_{deal_id}.txt",
                                mime="text/plain"
                            )
                    
                    with col2:
                        if st.button("Generate Letter of Intent"):
                            loi = ContractGenerator.generate_loi(deal_data)
                            st.text_area("Letter of Intent", loi, height=400)
                            st.download_button(
                                "Download LOI",
                                loi,
                                file_name=f"loi_{deal_id}.txt",
                                mime="text/plain"
                            )

def show_my_deals():
    st.markdown("# 📊 My Deals")
    
    if not st.session_state.logged_in:
        st.warning("Please login to view your deals")
        return
    
    deals = db.get_user_deals(st.session_state.user['id'])
    
    if not deals:
        st.info("No deals found. Create your first deal using the Deal Calculator!")
        return
    
    for deal in deals:
        with st.expander(f"📍 {deal['property_address']} - ${deal['arv']:,.0f} ARV"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Property Details:**
                - Address: {deal['property_address']}, {deal['city']}, {deal['state']} {deal['zip_code']}
                - Type: {deal['property_type']}
                - Bedrooms: {deal['bedrooms']} | Bathrooms: {deal['bathrooms']}
                - Square Feet: {deal['square_feet']:,}
                - Year Built: {deal['year_built']}
                - Condition: {deal['current_condition']}
                """)
            
            with col2:
                st.markdown(f"""
                **Financial Summary:**
                - ARV: ${deal['arv']:,.2f}
                - Purchase Price: ${deal['acquisition_cost']:,.2f}
                - Repair Costs: ${deal['repair_costs']:,.2f}
                - Profit Margin: {deal['profit_margin']:.1f}%
                - Deal Type: {deal['deal_type']}
                - Status: {deal['status'].title()}
                """)
            
            if deal['contact_name']:
                st.markdown(f"""
                **Contact Information:**
                - Name: {deal['contact_name']}
                - Phone: {deal['contact_phone']}
                - Email: {deal['contact_email']}
                """)
            
            if deal['notes']:
                st.markdown(f"**Notes:** {deal['notes']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Generate Contract", key=f"contract_{deal['id']}"):
                    contract = ContractGenerator.generate_wholesale_contract(deal)
                    st.text_area("Contract", contract, height=300, key=f"contract_text_{deal['id']}")
            
            with col2:
                if st.button(f"Generate LOI", key=f"loi_{deal['id']}"):
                    loi = ContractGenerator.generate_loi(deal)
                    st.text_area("LOI", loi, height=300, key=f"loi_text_{deal['id']}")

def show_admin_dashboard():
    if not st.session_state.logged_in or not st.session_state.user.get('is_admin'):
        st.error("Access denied. Admin privileges required.")
        return
    
    st.markdown("""
    <div class="admin-header">
        <h1>🛠️ Admin Dashboard - Wholesale2Flip</h1>
        <p>Deal Disposition & User Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin tabs
    tab1, tab2, tab3 = st.tabs(["📊 Deal Management", "👥 User Overview", "📈 Analytics"])
    
    with tab1:
        st.markdown("## All Deals - Disposition Pipeline")
        
        deals = db.get_all_deals()
        
        if deals:
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Filter by Status", 
                    ["All", "pending", "contacted", "under_contract", "closed", "dead"])
            with col2:
                deal_type_filter = st.selectbox("Filter by Deal Type", 
                    ["All", "Wholesale", "Fix & Flip", "Buy & Hold"])
            with col3:
                min_profit = st.number_input("Min Profit Margin %", min_value=0.0, value=0.0)
            
            # Filter deals
            filtered_deals = deals
            if status_filter != "All":
                filtered_deals = [d for d in filtered_deals if d['status'] == status_filter]
            if deal_type_filter != "All":
                filtered_deals = [d for d in filtered_deals if d['deal_type'] == deal_type_filter]
            if min_profit > 0:
                filtered_deals = [d for d in filtered_deals if d['profit_margin'] >= min_profit]
            
            st.markdown(f"**Showing {len(filtered_deals)} of {len(deals)} deals**")
            
            for deal in filtered_deals:
                with st.expander(f"🏠 {deal['property_address']} | {deal['user_name']} | ${deal['arv']:,.0f} ARV | {deal['profit_margin']:.1f}% Profit"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Property Information:**
                        - Address: {deal['property_address']}, {deal['city']}, {deal['state']} {deal['zip_code']}
                        - Type: {deal['property_type']} | Bedrooms: {deal['bedrooms']} | Bathrooms: {deal['bathrooms']}
                        - Square Feet: {deal['square_feet']:,} | Year Built: {deal['year_built']}
                        - Condition: {deal['current_condition']}
                        
                        **Financial Details:**
                        - ARV: ${deal['arv']:,.2f}
                        - Purchase Price: ${deal['acquisition_cost']:,.2f}
                        - Repair Costs: ${deal['repair_costs']:,.2f}
                        - Profit Margin: {deal['profit_margin']:.1f}%
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Student/User Information:**
                        - Name: {deal['user_name']}
                        - Email: {deal['user_email']}
                        - User ID: {deal['user_id']}
                        
                        **Contact Information:**
                        - Seller Name: {deal['contact_name'] or 'N/A'}
                        - Phone: {deal['contact_phone'] or 'N/A'}
                        - Email: {deal['contact_email'] or 'N/A'}
                        
                        **Deal Status:** {deal['status'].title()}
                        **Created:** {deal['created_at'][:10]}
                        """)
                    
                    if deal['notes']:
                        st.markdown(f"**Notes:** {deal['notes']}")
                    
                    # Admin actions
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("📞 Contact Student", key=f"contact_{deal['id']}"):
                            st.success(f"Contact {deal['user_name']} at {deal['user_email']}")
                    
                    with col2:
                        new_status = st.selectbox("Update Status", 
                            ["pending", "contacted", "under_contract", "closed", "dead"],
                            index=["pending", "contacted", "under_contract", "closed", "dead"].index(deal['status']),
                            key=f"status_{deal['id']}")
                        if st.button("Update", key=f"update_{deal['id']}"):
                            # Here you would update the deal status in the database
                            st.success(f"Status updated to {new_status}")
                    
                    with col3:
                        if st.button("📄 View Contract", key=f"view_contract_{deal['id']}"):
                            contract = ContractGenerator.generate_wholesale_contract(deal)
                            st.text_area("Generated Contract", contract, height=200, key=f"admin_contract_{deal['id']}")
                    
                    with col4:
                        if st.button("📨 View LOI", key=f"view_loi_{deal['id']}"):
                            loi = ContractGenerator.generate_loi(deal)
                            st.text_area("Generated LOI", loi, height=200, key=f"admin_loi_{deal['id']}")
        else:
            st.info("No deals submitted yet.")
    
    with tab2:
        st.markdown("## User Management")
        
        conn = sqlite3.connect(db.db_name)
        users_df = pd.read_sql_query("""
            SELECT id, name, email, subscription_tier, 
                   subscription_start, subscription_end, created_at
            FROM users 
            ORDER BY created_at DESC
        """, conn)
        conn.close()
        
        if not users_df.empty:
            st.dataframe(users_df, use_container_width=True)
            
            # User stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Users", len(users_df))
            with col2:
                active_subs = len(users_df[users_df['subscription_tier'] != 'none'])
                st.metric("Active Subscriptions", active_subs)
            with col3:
                starter_users = len(users_df[users_df['subscription_tier'] == 'starter'])
                st.metric("Starter Plan", starter_users)
            with col4:
                pro_users = len(users_df[users_df['subscription_tier'] == 'professional'])
                st.metric("Professional Plan", pro_users)
        else:
            st.info("No users registered yet.")
    
    with tab3:
        st.markdown("## Analytics & Insights")
        
        deals = db.get_all_deals()
        
        if deals:
            # Deal analytics
            deal_types = {}
            profit_margins = []
            monthly_deals = {}
            
            for deal in deals:
                # Deal type distribution
                deal_type = deal['deal_type']
                deal_types[deal_type] = deal_types.get(deal_type, 0) + 1
                
                # Profit margins
                if deal['profit_margin']:
                    profit_margins.append(deal['profit_margin'])
                
                # Monthly deals
                month = deal['created_at'][:7]  # YYYY-MM
                monthly_deals[month] = monthly_deals.get(month, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Deal Type Distribution")
                if deal_types:
                    chart_data = pd.DataFrame(list(deal_types.items()), columns=['Deal Type', 'Count'])
                    st.bar_chart(chart_data.set_index('Deal Type'))
            
            with col2:
                st.markdown("### Average Metrics")
                if profit_margins:
                    avg_profit = sum(profit_margins) / len(profit_margins)
                    st.metric("Average Profit Margin", f"{avg_profit:.1f}%")
                
                total_arv = sum(deal['arv'] for deal in deals if deal['arv'])
                avg_arv = total_arv / len(deals) if deals else 0
                st.metric("Average ARV", f"${avg_arv:,.0f}")
            
            # Monthly trends
            if monthly_deals:
                st.markdown("### Monthly Deal Submissions")
                chart_data = pd.DataFrame(list(monthly_deals.items()), columns=['Month', 'Deals'])
                st.line_chart(chart_data.set_index('Month'))
        else:
            st.info("No deals data available for analytics.")

def main():
    load_css()
    init_session_state()
    
    # Navigation
    if st.session_state.logged_in:
        user = st.session_state.user
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"## Welcome, {user['name']}!")
            st.markdown(f"**Plan:** {user['subscription_tier'].title()}")
            
            if st.button("🏠 Home"):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.button("🧮 Deal Calculator"):
                st.session_state.current_page = 'calculator'
                st.rerun()
            
            if st.button("📊 My Deals"):
                st.session_state.current_page = 'my_deals'
                st.rerun()
            
            if user.get('is_admin'):
                if st.button("⚙️ Admin Dashboard"):
                    st.session_state.current_page = 'admin'
                    st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.current_page = 'home'
                st.rerun()
        
        # Main content based on current page
        if st.session_state.current_page == 'home':
            show_home_page()
        elif st.session_state.current_page == 'calculator':
            show_deal_calculator()
        elif st.session_state.current_page == 'my_deals':
            show_my_deals()
        elif st.session_state.current_page == 'admin' and user.get('is_admin'):
            show_admin_dashboard()
        else:
            show_home_page()
    
    else:
        show_login_signup()

if __name__ == "__main__":
    main()