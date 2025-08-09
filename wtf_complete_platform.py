"""
WTF (Wholesale2Flip) - Complete Real Estate Platform
Enhanced version with landing page, full CRM, contracts, LOI generation, and admin features
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
import json
import base64
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import time
import re

# Page configuration
st.set_page_config(
    page_title="WTF - Wholesale2Flip Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for WTF branding with landing page styles
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Landing Page Styles */
    .landing-hero {
        background: linear-gradient(135deg, #8B5CF6 0%, #10B981 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .pricing-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(139, 92, 246, 0.5);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem;
        transition: all 0.3s ease;
    }
    
    .pricing-card:hover {
        border-color: #10B981;
        transform: scale(1.05);
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
    
    .crm-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .admin-panel {
        background: linear-gradient(135deg, #DC2626 0%, #7C2D12 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .wholesaler-panel {
        background: linear-gradient(135deg, #8B5CF6 0%, #5B21B6 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .buyer-panel {
        background: linear-gradient(135deg, #10B981 0%, #065F46 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
    }
    
    .contract-preview {
        background: rgba(255, 255, 255, 0.95);
        color: black;
        padding: 2rem;
        border-radius: 10px;
        font-family: 'Times New Roman', serif;
        line-height: 1.6;
    }
    
    .loi-preview {
        background: rgba(255, 255, 255, 0.95);
        color: black;
        padding: 2rem;
        border-radius: 10px;
        font-family: 'Arial', sans-serif;
        line-height: 1.5;
    }
    
    .deal-calculator {
        background: rgba(16, 185, 129, 0.1);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .roi-positive {
        color: #10B981;
        font-weight: bold;
    }
    
    .roi-negative {
        color: #EF4444;
        font-weight: bold;
    }
    
    .navbar {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced data classes
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
    condition: str = 'fair'
    created_at: datetime = None
    lead_id: str = None
    status: str = 'new'

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
    property_condition: str = 'fair'
    estimated_value: float = 0
    owed_amount: float = 0
    notes: str = ''
    assigned_to: str = ''
    last_contact: datetime = None
    next_followup: datetime = None
    created_at: datetime = None

@dataclass
class Deal:
    id: str
    title: str
    property_id: str
    buyer_id: str
    lead_id: str
    purchase_price: float
    assignment_fee: float
    status: str
    probability: int
    contract_date: datetime = None
    closing_date: datetime = None
    created_at: datetime = None

@dataclass
class Contract:
    id: str
    deal_id: str
    contract_type: str
    purchase_price: float
    earnest_money: float
    closing_date: datetime
    buyer_name: str
    seller_name: str
    property_address: str
    status: str = 'draft'
    terms: Dict = None
    created_at: datetime = None

# Enhanced Database Manager
class EnhancedDatabaseManager:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize enhanced database with all tables"""
        conn = sqlite3.connect('wtf_platform.db')
        cursor = conn.cursor()
        
        # Enhanced properties table
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
                condition TEXT DEFAULT 'fair',
                lead_id TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced leads table
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
                property_condition TEXT DEFAULT 'fair',
                estimated_value REAL DEFAULT 0,
                owed_amount REAL DEFAULT 0,
                notes TEXT,
                assigned_to TEXT,
                last_contact TIMESTAMP,
                next_followup TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced deals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                property_id TEXT,
                buyer_id TEXT,
                lead_id TEXT,
                purchase_price REAL,
                assignment_fee REAL,
                status TEXT DEFAULT 'lead',
                probability INTEGER DEFAULT 10,
                contract_date TIMESTAMP,
                closing_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced contracts table
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
                property_address TEXT,
                status TEXT DEFAULT 'draft',
                terms TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Letters of Intent table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lois (
                id TEXT PRIMARY KEY,
                lead_id TEXT NOT NULL,
                property_address TEXT NOT NULL,
                offer_price REAL NOT NULL,
                terms TEXT,
                status TEXT DEFAULT 'draft',
                sent_date TIMESTAMP,
                response_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table for enhanced auth
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                company TEXT,
                subscription_tier TEXT DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Buyers table (existing)
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
        
        # Insert default admin user if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            admin_id = str(uuid.uuid4())
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (id, username, email, password_hash, role, full_name, company)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'admin', 'admin@wtf.com', password_hash, 'admin', 'Admin User', 'WTF Platform'))
        
        # Insert sample data if empty
        self._insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def _insert_sample_data(self, cursor):
        """Insert sample data for testing"""
        # Sample buyers
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
        
        # Sample leads
        cursor.execute("SELECT COUNT(*) FROM leads")
        if cursor.fetchone()[0] == 0:
            sample_leads = [
                ('Maria', 'Garcia', '(555) 111-2222', 'maria@email.com', '123 Main St, Dallas, TX', 
                 'divorce', 'asap', 'cold_calling', 'contacted', 85, 'fair', 250000, 180000, 'Motivated to sell quickly'),
                ('David', 'Brown', '(555) 222-3333', 'david@email.com', '456 Oak Ave, Houston, TX',
                 'job_relocation', '30_days', 'direct_mail', 'interested', 72, 'good', 320000, 240000, 'Moving to California'),
                ('Jennifer', 'Lee', '(555) 333-4444', 'jennifer@email.com', '789 Pine Rd, Austin, TX',
                 'inherited_property', '60_days', 'referral', 'new', 68, 'poor', 180000, 0, 'Inherited from grandmother'),
            ]
            
            for lead in sample_leads:
                lead_id = str(uuid.uuid4())
                cursor.execute('''
                    INSERT INTO leads (id, first_name, last_name, phone, email, property_address,
                                     motivation, timeline, source, status, score, property_condition,
                                     estimated_value, owed_amount, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (lead_id,) + lead)

# Deal Calculator Service
class DealCalculator:
    """Advanced deal calculation engine following the 70% rule and other metrics"""
    
    def __init__(self):
        pass
    
    def calculate_arv(self, property_data: Dict, comps: List[Dict] = None) -> float:
        """Calculate After Repair Value using comps or estimate"""
        if comps and len(comps) > 0:
            # Use comparable sales
            total_price_per_sqft = sum(comp.get('price_per_sqft', 150) for comp in comps)
            avg_price_per_sqft = total_price_per_sqft / len(comps)
            arv = property_data.get('square_feet', 1800) * avg_price_per_sqft
        else:
            # Use market multiplier based on area
            base_price = property_data.get('list_price', 200000)
            market_multiplier = {
                'TX': 1.15, 'CA': 1.25, 'FL': 1.10, 'NY': 1.20, 'GA': 1.08
            }
            multiplier = market_multiplier.get(property_data.get('state', 'TX'), 1.10)
            arv = base_price * multiplier
        
        return round(arv)
    
    def estimate_rehab_cost(self, property_data: Dict) -> float:
        """Estimate rehab costs based on condition and size"""
        square_feet = property_data.get('square_feet', 1800)
        condition = property_data.get('condition', 'fair').lower()
        
        # Cost per square foot by condition
        rehab_costs = {
            'excellent': 0,
            'good': 8,
            'fair': 18,
            'poor': 32,
            'needs_rehab': 50,
            'tear_down': 80
        }
        
        cost_per_sqft = rehab_costs.get(condition, 20)
        base_rehab = square_feet * cost_per_sqft
        
        # Add fixed costs
        fixed_costs = {
            'paint': 3000,
            'flooring': 5000,
            'kitchen': 8000,
            'bathrooms': 4000,
            'hvac': 3000,
            'landscaping': 2000,
            'contingency': base_rehab * 0.15  # 15% contingency
        }
        
        total_rehab = base_rehab + sum(fixed_costs.values())
        return round(total_rehab)
    
    def calculate_max_offer(self, arv: float, rehab_cost: float, rule_percentage: float = 0.70) -> float:
        """Calculate maximum offer using the 70% rule or custom percentage"""
        max_offer = (arv * rule_percentage) - rehab_cost
        return max(0, round(max_offer))
    
    def calculate_deal_metrics(self, property_data: Dict) -> Dict:
        """Calculate comprehensive deal metrics"""
        # Get basic values
        arv = self.calculate_arv(property_data)
        rehab_cost = self.estimate_rehab_cost(property_data)
        max_offer_70 = self.calculate_max_offer(arv, rehab_cost, 0.70)
        max_offer_75 = self.calculate_max_offer(arv, rehab_cost, 0.75)
        max_offer_80 = self.calculate_max_offer(arv, rehab_cost, 0.80)
        
        # Calculate different deal structures
        wholesale_fee_range = [5000, 10000, 15000, 20000, 25000]
        
        # Entry fee breakdown for different tiers
        tiers = {
            'low': {
                'offer_price': max_offer_70,
                'down_payment_pct': 0.025,  # 2.5%
                'financing': 'SubTo or Cash'
            },
            'medium': {
                'offer_price': max_offer_75,
                'down_payment_pct': 0.08,   # 8%
                'financing': 'Seller Finance'
            },
            'high': {
                'offer_price': max_offer_80,
                'down_payment_pct': 0.15,   # 15%
                'financing': 'Wrap/Hybrid'
            }
        }
        
        # Calculate entry fees for each tier
        entry_fees = {}
        for tier, data in tiers.items():
            offer_price = data['offer_price']
            down_payment = offer_price * data['down_payment_pct']
            agent_commission = offer_price * 0.03  # 3%
            closing_costs = offer_price * 0.02     # 2%
            
            entry_fees[tier] = {
                'offer_price': offer_price,
                'down_payment': down_payment,
                'agent_commission': agent_commission,
                'closing_costs': closing_costs,
                'rehab_cost': rehab_cost,
                'total_entry_fee': down_payment + agent_commission + closing_costs + rehab_cost,
                'financing_type': data['financing']
            }
        
        # Calculate potential rental income (rough estimate)
        estimated_rent = arv * 0.006  # 0.6% of ARV as monthly rent (rough rule)
        
        # Calculate cash flow and returns for each tier
        returns = {}
        for tier, fees in entry_fees.items():
            monthly_expenses = {
                'piti': fees['offer_price'] * 0.0045,  # 4.5% annually / 12
                'management': estimated_rent * 0.08,   # 8% of rent
                'vacancy': estimated_rent * 0.05,      # 5% vacancy reserve
                'maintenance': estimated_rent * 0.05,  # 5% maintenance
                'insurance': 150,                      # Monthly insurance
                'other': 100                           # Other expenses
            }
            
            total_expenses = sum(monthly_expenses.values())
            net_cash_flow = estimated_rent - total_expenses
            
            # Calculate returns
            annual_cash_flow = net_cash_flow * 12
            total_investment = fees['total_entry_fee']
            
            if total_investment > 0:
                cash_on_cash = (annual_cash_flow / total_investment) * 100
                cap_rate = (annual_cash_flow / fees['offer_price']) * 100
                dscr = (estimated_rent / monthly_expenses['piti']) if monthly_expenses['piti'] > 0 else 0
            else:
                cash_on_cash = 0
                cap_rate = 0
                dscr = 0
            
            returns[tier] = {
                'estimated_rent': estimated_rent,
                'monthly_expenses': total_expenses,
                'net_cash_flow': net_cash_flow,
                'cash_on_cash': cash_on_cash,
                'cap_rate': cap_rate,
                'dscr': dscr
            }
        
        # Wholesale analysis
        wholesale_analysis = {}
        for fee in wholesale_fee_range:
            profit = fee
            roi = (profit / 5000) * 100 if fee > 0 else 0  # Assuming $5K in costs
            wholesale_analysis[f'${fee:,}'] = {
                'assignment_fee': fee,
                'profit': profit,
                'roi': roi,
                'time_to_close': '30-45 days'
            }
        
        return {
            'property_data': property_data,
            'arv': arv,
            'rehab_cost': rehab_cost,
            'max_offers': {
                '70_percent': max_offer_70,
                '75_percent': max_offer_75,
                '80_percent': max_offer_80
            },
            'entry_fees': entry_fees,
            'returns': returns,
            'wholesale_analysis': wholesale_analysis,
            'estimated_rent': estimated_rent,
            'profit_potential': arv - max_offer_70 - rehab_cost,
            'deal_grade': self._grade_deal(returns)
        }
    
    def _grade_deal(self, returns: Dict) -> str:
        """Grade the deal based on returns"""
        # Use medium tier for grading
        medium_returns = returns.get('medium', {})
        cash_on_cash = medium_returns.get('cash_on_cash', 0)
        dscr = medium_returns.get('dscr', 0)
        
        if cash_on_cash >= 15 and dscr >= 1.4:
            return 'A'
        elif cash_on_cash >= 12 and dscr >= 1.25:
            return 'B'
        elif cash_on_cash >= 8 and dscr >= 1.1:
            return 'C'
        else:
            return 'D'

# Contract Generator Service
class ContractGenerator:
    """Generate professional real estate contracts and LOIs"""
    
    def __init__(self):
        pass
    
    def generate_purchase_agreement(self, deal_data: Dict) -> str:
        """Generate a complete purchase agreement"""
        template = f"""
        REAL ESTATE PURCHASE AGREEMENT
        
        This Purchase Agreement ("Agreement") is made on {datetime.now().strftime('%B %d, %Y')} between:
        
        SELLER: {deal_data.get('seller_name', 'SELLER NAME')}
        Address: {deal_data.get('seller_address', 'SELLER ADDRESS')}
        
        BUYER: {deal_data.get('buyer_name', 'BUYER NAME')}
        Address: {deal_data.get('buyer_address', 'BUYER ADDRESS')}
        
        PROPERTY INFORMATION:
        Address: {deal_data.get('property_address', 'PROPERTY ADDRESS')}
        Legal Description: To be obtained from title company
        
        PURCHASE TERMS:
        Purchase Price: ${deal_data.get('purchase_price', 0):,.2f}
        Earnest Money: ${deal_data.get('earnest_money', 1000):,.2f}
        Inspection Period: {deal_data.get('inspection_period', 7)} days
        Closing Date: {deal_data.get('closing_date', 'TBD')}
        
        FINANCING:
        This purchase is subject to buyer obtaining financing within {deal_data.get('financing_days', 21)} days.
        
        CONTINGENCIES:
        1. Property inspection satisfactory to buyer
        2. Clear title and survey
        3. Property to be delivered in same condition as of acceptance
        
        CLOSING COSTS:
        Closing costs will be paid by: {deal_data.get('closing_costs_paid_by', 'Split 50/50')}
        
        SPECIAL PROVISIONS:
        {deal_data.get('special_terms', 'None')}
        
        This agreement shall be binding upon the parties, their heirs, successors, and assigns.
        
        SELLER SIGNATURE: _________________________ DATE: _________
        {deal_data.get('seller_name', 'SELLER NAME')}
        
        BUYER SIGNATURE: _________________________ DATE: _________
        {deal_data.get('buyer_name', 'BUYER NAME')}
        
        Generated by WTF Platform on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Contract ID: {deal_data.get('contract_id', str(uuid.uuid4())[:8])}
        """
        
        return template
    
    def generate_assignment_contract(self, deal_data: Dict) -> str:
        """Generate assignment contract"""
        template = f"""
        ASSIGNMENT OF REAL ESTATE PURCHASE CONTRACT
        
        This Assignment Agreement is made on {datetime.now().strftime('%B %d, %Y')} between:
        
        ASSIGNOR (Original Buyer): {deal_data.get('assignor_name', 'ASSIGNOR NAME')}
        ASSIGNEE (New Buyer): {deal_data.get('assignee_name', 'ASSIGNEE NAME')}
        
        ORIGINAL CONTRACT INFORMATION:
        Property Address: {deal_data.get('property_address', 'PROPERTY ADDRESS')}
        Original Purchase Price: ${deal_data.get('purchase_price', 0):,.2f}
        Original Contract Date: {deal_data.get('original_contract_date', 'TBD')}
        Seller: {deal_data.get('seller_name', 'SELLER NAME')}
        
        ASSIGNMENT TERMS:
        Assignment Fee: ${deal_data.get('assignment_fee', 5000):,.2f}
        Assignee shall assume all rights and obligations under the original purchase contract.
        
        ASSIGNOR WARRANTIES:
        1. Original contract is valid and in full force
        2. No defaults exist under original contract
        3. All conditions have been met or waived
        
        ASSIGNEE ACKNOWLEDGMENTS:
        1. Has reviewed original purchase contract
        2. Accepts all terms and conditions
        3. Will close directly with seller
        
        ASSIGNMENT FEE PAYMENT:
        Assignment fee of ${deal_data.get('assignment_fee', 5000):,.2f} is due at closing.
        
        ASSIGNOR SIGNATURE: _________________________ DATE: _________
        {deal_data.get('assignor_name', 'ASSIGNOR NAME')}
        
        ASSIGNEE SIGNATURE: _________________________ DATE: _________
        {deal_data.get('assignee_name', 'ASSIGNEE NAME')}
        
        Generated by WTF Platform on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Assignment ID: {deal_data.get('assignment_id', str(uuid.uuid4())[:8])}
        """
        
        return template
    
    def generate_loi(self, loi_data: Dict) -> str:
        """Generate Letter of Intent"""
        template = f"""
        LETTER OF INTENT TO PURCHASE REAL ESTATE
        
        Date: {datetime.now().strftime('%B %d, %Y')}
        
        To: {loi_data.get('seller_name', 'PROPERTY OWNER')}
        
        Re: Purchase of Property at {loi_data.get('property_address', 'PROPERTY ADDRESS')}
        
        Dear Property Owner,
        
        I am writing to express my serious interest in purchasing your property located at 
        {loi_data.get('property_address', 'PROPERTY ADDRESS')}.
        
        PROPOSED TERMS:
        
        Purchase Price: ${loi_data.get('offer_price', 0):,.2f}
        Earnest Money: ${loi_data.get('earnest_money', 1000):,.2f}
        Closing Timeframe: {loi_data.get('closing_timeframe', '30 days')}
        Inspection Period: {loi_data.get('inspection_period', '7 days')}
        
        CONDITIONS:
        • Property to be sold in "AS-IS" condition
        • Clear and marketable title
        • All liens and encumbrances to be satisfied at closing
        • Standard property inspection to be completed
        
        ADDITIONAL TERMS:
        {loi_data.get('additional_terms', 'Cash purchase with quick closing')}
        
        This Letter of Intent is non-binding and is intended to outline the basic terms 
        for further negotiation. A formal purchase agreement will be prepared upon 
        mutual acceptance of these terms.
        
        I am a serious buyer with {loi_data.get('buyer_qualification', 'cash available and pre-approval')} 
        and can close quickly. I would appreciate the opportunity to discuss this offer with you.
        
        Please contact me at your earliest convenience.
        
        Sincerely,
        
        {loi_data.get('buyer_name', 'BUYER NAME')}
        {loi_data.get('buyer_phone', 'BUYER PHONE')}
        {loi_data.get('buyer_email', 'BUYER EMAIL')}
        
        Generated by WTF Platform on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        LOI ID: {loi_data.get('loi_id', str(uuid.uuid4())[:8])}
        """
        
        return template

# Enhanced AI Assistant with Script Generation
class EnhancedAIAssistant:
    """Enhanced AI Assistant with full script generation capabilities"""
    
    def __init__(self):
        self.script_templates = {
            'cold_calling': self._get_cold_calling_scripts(),
            'objection_handling': self._get_objection_scripts(),
            'follow_up': self._get_followup_scripts(),
            'closing': self._get_closing_scripts()
        }
    
    def generate_full_script(self, script_type: str, scenario: str) -> str:
        """Generate complete 5x5 script as per Empire ScriptMaster AI"""
        if script_type not in self.script_templates:
            return "Script type not available"
        
        script_data = self.script_templates[script_type]
        
        # Build the complete 5x5 script
        full_script = f"""
# {script_data['title']} - Complete 5x5 Script

## Scenario: {scenario}

{script_data['introduction']}

---

## 📞 PART 1 – Intro & Rapport Building

**Your Opening:**
"{script_data['opening']}"

### Seller Responses & Your Replies:

**💬 Seller Response #1:** "Who is this and what do you want?"
**🔁 Closer Reply Bank:**
1. "Hi [Name], I completely understand the surprise call. I'm [Your Name] with [Company], and I specialize in helping homeowners who need to sell quickly without the hassle of traditional real estate. I was wondering - is your property at [Address] something you'd ever consider selling?"
2. "I know you weren't expecting my call, but I work with homeowners in [Area] who are looking for fast, hassle-free solutions. Have you ever thought about what it would take to sell your property quickly?"
3. "I apologize for the cold call. I'm [Name] and I buy houses in [Area]. I was calling because I'm interested in your property at [Address]. Would you be open to hearing about a quick sale option?"
4. "Hi there! I'm [Name] with [Company]. I know this is unexpected, but I help homeowners sell their properties fast for cash. Is selling your home at [Address] something that might interest you?"
5. "I understand the surprise. I'm a local real estate investor, and I'm interested in purchasing homes in your area. Would you have 30 seconds to hear about how I might be able to help you?"

**💬 Seller Response #2:** "I'm not interested in selling."
**🔁 Closer Reply Bank:**
1. "I completely understand, and most people I talk to say the same thing initially. But let me ask you this - if you could sell quickly without repairs, realtor fees, or showings, would that change anything?"
2. "That's perfectly fine, and I respect that. But just out of curiosity - what would it take for you to consider selling? Sometimes people's situations change."
3. "I hear you, and that's totally okay. Can I ask though - is it that you're not interested in selling at all, or just not interested in the traditional hassle of selling?"
4. "No problem at all. But if I may ask - what if you could get a fair cash offer with no obligations and close in as little as 7 days? Would that be worth a conversation?"
5. "I understand completely. Most homeowners aren't actively thinking about selling until the right opportunity comes along. What would make selling attractive to you?"

**💬 Seller Response #3:** "How did you get my number?"
**🔁 Closer Reply Bank:**
1. "That's a great question. I get leads from public records, marketing campaigns, and referrals. I'm not a telemarketer - I'm a local investor who buys houses. Have you ever considered selling your property?"
2. "I work with a service that identifies homeowners who might benefit from a quick sale. I'm a real estate investor, not a salesperson. Would you be interested in hearing about a cash offer for your property?"
3. "I get homeowner information through public records and marketing. I'm calling because I'm genuinely interested in purchasing your property. Would you be open to discussing a potential sale?"
4. "Fair question. I'm a local real estate investor, and I get leads through various marketing channels. I'm calling because I'm interested in your property specifically. Is selling something you've ever considered?"
5. "I understand your concern. I'm a licensed real estate investor, and I get information through legitimate marketing sources. I'm calling because I buy houses in your area. Would you be interested in a no-obligation offer?"

**💬 Seller Response #4:** "What's this about exactly?"
**🔁 Closer Reply Bank:**
1. "Great question! I buy houses directly from homeowners - no realtors, no repairs needed, and I can close in as little as 7-10 days. I'm calling to see if you'd be interested in a cash offer for your property."
2. "I'm a real estate investor who purchases homes for cash. I can close quickly, handle all the paperwork, and you don't need to make any repairs. Would you be interested in hearing what I could offer for your property?"
3. "I specialize in buying houses from homeowners who need to sell quickly. Whether it's because of job relocation, financial hardship, or you just want to avoid the hassle of traditional selling - I can help. Interested in learning more?"
4. "I'm in the business of buying houses directly from homeowners. I pay cash, close fast, and take properties as-is. No realtor fees, no repairs, no showings. Would that type of sale interest you?"
5. "I purchase homes for cash from homeowners who need a quick, hassle-free sale. I can usually make an offer within 24 hours and close in 1-2 weeks. Is that something that might benefit you?"

**💬 Seller Response #5:** "I'm too busy to talk right now."
**🔁 Closer Reply Bank:**
1. "I completely understand, and I appreciate your honesty. When would be a better time to call you back? This will only take 2-3 minutes, and I think you'll find it valuable."
2. "No problem at all. I know you're busy. What's the best time to reach you for just a quick 2-minute conversation about your property?"
3. "I respect your time completely. Would it be better if I called you back this evening or tomorrow? I just need 60 seconds to explain how I might be able to help you."
4. "Absolutely, I understand. Would you prefer I call you back in a few hours, or would texting be better? I just want to see if I can make you a cash offer for your property."
5. "Of course, I don't want to interrupt your day. When you have just 2 minutes free, I'd love to explain how I buy houses for cash. What time works better for you?"

---

## 📞 PART 2 – Discovery Questions & Motivation

**Transition Statement:**
"Great! Since you're open to hearing more, let me ask you a few quick questions to see if this might be a good fit for both of us."

### Seller Responses & Your Replies:

**💬 Seller Response #1:** "What do you need to know?"
**🔁 Closer Reply Bank:**
1. "Perfect! First, can you tell me a little about your property? How many bedrooms and bathrooms, and what condition would you say it's in?"
2. "Great! I just need to understand your situation better. What's prompting you to consider selling? Is it a timing issue, or are there other factors?"
3. "Excellent! Let me start with the basics - how long have you owned the property, and what's your ideal timeline if you were to sell?"
4. "Wonderful! Can you walk me through what's driving the potential sale? Are you looking to move, or is there another reason you'd consider selling?"
5. "Perfect! I'd love to know more about your property and your situation. What would need to happen for a sale to make sense for you?"

**💬 Seller Response #2:** "Why should I tell you anything?"
**🔁 Closer Reply Bank:**
1. "That's a very reasonable question. I ask because I want to make sure I can actually help you. If your timeline doesn't match what I can offer, or if your property isn't a fit, I'd rather know now and not waste either of our time."
2. "Fair point. I'm asking because I want to give you an accurate offer that makes sense for your situation. If I don't understand your needs, I can't determine if I'm the right solution for you."
3. "I completely understand your hesitation. The reason I ask is that every homeowner's situation is different, and I want to make sure I can provide real value. If I can't help you, I'll tell you honestly."
4. "Great question. I ask these questions because I want to make you a fair offer that actually works for your situation. If your needs don't align with what I do, I'd rather know upfront."
5. "I respect that caution. I ask because I've found that understanding someone's specific situation helps me determine if I can be a good solution. If not, I'm happy to refer you to someone who might be a better fit."

**💬 Seller Response #3:** "The house needs a lot of work."
**🔁 Closer Reply Bank:**
1. "That's actually perfect for what I do! I specialize in buying houses that need work. Can you give me an idea of what kind of repairs we're talking about? Foundation, roof, cosmetic updates?"
2. "No problem at all - I buy houses in any condition. That's one of the benefits of working with me versus a traditional sale. What kind of work does it need?"
3. "That's exactly why homeowners call me! I take properties as-is, so you don't have to worry about repairs. Can you tell me more about what needs to be done?"
4. "Perfect! I actually prefer houses that need work because I can factor that into my offer and you don't have to deal with contractors. What are the main issues?"
5. "That's great to hear because that's my specialty. Most homeowners don't want to deal with repairs before selling, which is exactly why I exist. What's the biggest repair needed?"

**💬 Seller Response #4:** "I don't know what it's worth."
**🔁 Closer Reply Bank:**
1. "No worries at all - that's very common. I can help you figure that out. Can you tell me roughly what similar houses in your neighborhood have sold for recently?"
2. "That's perfectly fine. I do this every day, so I can help determine value. What did you pay for it, and when did you purchase it?"
3. "Don't worry about that - I'll handle the valuation. Can you give me the square footage and number of bedrooms and bathrooms?"
4. "That's okay, most homeowners don't track the market closely. I can run some quick numbers. Do you know what your neighbors' houses have sold for?"
5. "No problem at all. I can provide you with a market analysis. In the meantime, what would you need to get out of the property to make selling worthwhile?"

**💬 Seller Response #5:** "I need to think about it."
**🔁 Closer Reply Bank:**
1. "Absolutely, this is a big decision. What specifically would you like to think over? Maybe I can provide some clarity right now."
2. "Of course, I completely understand. What questions do you have that might help you think through this decision?"
3. "That makes total sense. While you're thinking, what information would be most helpful for you to have?"
4. "I respect that completely. Is there anything specific you'd like me to explain better, or do you need to discuss it with someone?"
5. "Absolutely, take all the time you need. What would help you feel more comfortable with the process?"

---

## 📞 PART 3 – Deal Pivot / Offer Framing

**Transition Statement:**
"Based on what you've told me, I think I might be able to help you. Let me explain how my process works and see if it makes sense for your situation."

### Seller Responses & Your Replies:

**💬 Seller Response #1:** "Okay, what can you offer?"
**🔁 Closer Reply Bank:**
1. "Great question! Before I give you a number, let me explain my process. I make fair cash offers based on current market value minus any needed repairs. I can typically offer between 70-80% of market value, but you get speed, certainty, and no hassles. Does that sound reasonable?"
2. "I'm glad you asked! I determine my offers based on what the property would sell for in perfect condition, minus repair costs and my margin. For a property like yours, I'd estimate an offer in the $[X] to $[Y] range. Would that be worth exploring?"
3. "Perfect! I calculate offers based on the after-repair value of the property. Given what you've told me about the condition and location, I'm thinking somewhere around $[X]. Would an offer in that range make sense for your situation?"
4. "Excellent! Based on our conversation, I believe I can make you an offer between $[X] and $[Y]. The exact number depends on a quick property inspection. Would you be interested in having me take a look?"
5. "I'm excited to help! For properties in your area with similar characteristics, I typically offer between $[X] and $[Y]. The final number depends on seeing the property in person. When could I come take a look?"

**💬 Seller Response #2:** "That sounds too low."
**🔁 Closer Reply Bank:**
1. "I understand that initial reaction, and it's completely normal. Let me ask you this - if you sold traditionally, what would you pay in realtor fees, repairs, carrying costs, and other expenses? When you factor those in, my offer might be closer than you think."
2. "I hear you, and I want to make sure you understand the full picture. With traditional sales, you have 6% realtor fees, repair costs, months of carrying costs, and uncertainty. What would those costs total for you?"
3. "That's a fair concern. Keep in mind though, my offer is net to you - no fees, no repairs, no carrying costs. If you listed with an agent at $[higher price], what would you actually net after all expenses?"
4. "I completely understand. But consider this - I close in 10-14 days with cash, versus 6 months on the market, thousands in repairs, realtor fees, and no guarantee of sale. What's your time and certainty worth?"
5. "I get that reaction often. But think about it this way - my offer is what you'll actually receive. No surprise deductions, no repair negotiations, no deals falling through. Isn't certainty worth something?"

**💬 Seller Response #3:** "How do I know you're legitimate?"
**🔁 Closer Reply Bank:**
1. "Excellent question, and you should absolutely verify that! I'm a licensed real estate investor, and I can provide references from recent sellers. I also use a reputable title company for all closings. Would you like me to send you some references?"
2. "Smart question! I've been buying houses in this area for [X] years. I can show you my business license, provide references, and we'll close through a title company where you'll be protected. What would make you feel most comfortable?"
3. "I'm glad you asked! I'm a legitimate business owner with proper licensing and insurance. All our closings go through licensed title companies, and I can provide testimonials from recent clients. How can I best prove my credibility to you?"
4. "Great question - you should verify anyone you work with! I have an A+ BBB rating, proper business licensing, and can provide references. We also use title companies for all transactions to protect you. What would give you confidence?"
5. "Absolutely the right question to ask! I'm a licensed real estate professional, fully insured, and I can provide proof of funds and references. All closings are handled by licensed professionals. Would you like me to email you my credentials?"

**💬 Seller Response #4:** "What's the catch?"
**🔁 Closer Reply Bank:**
1. "No catch at all! The trade-off is that you get speed, convenience, and certainty, but you get less than retail market value. If you had 6-12 months and wanted to maximize price, listing with an agent might get you more - but most of my sellers value the convenience."
2. "Great question! There's no catch - just a trade-off. You're trading maximum sale price for speed, convenience, and certainty. It's like selling your car to CarMax versus selling it yourself - you get less but save time and hassle."
3. "No hidden catch! The only 'cost' is that you'll get less than if you spent months on the market and thousands on repairs. But you get cash in 2 weeks versus uncertainty for months. Which is more valuable to you?"
4. "Totally fair question! The only trade-off is price versus convenience. You could potentially get more listing with an agent, but you'll wait longer, pay fees, and have no guarantees. I offer certainty and speed."
5. "No catch whatsoever! I make money by buying below market value and either renting or reselling after repairs. You benefit by getting cash quickly without hassles. It's a fair trade where we both win."

**💬 Seller Response #5:** "I need to talk to my spouse/family."
**🔁 Closer Reply Bank:**
1. "Absolutely, you should definitely discuss this with them! This is a big decision. When do you think you'll have a chance to talk it over? I'd be happy to speak with both of you together if that would help."
2. "Of course, that's exactly what you should do! Would it be helpful if I put together a written offer that you can review together? That way you'll have all the details to discuss."
3. "That's exactly the right thing to do. Would your spouse want to be part of the conversation? I'm happy to explain the process to both of you at the same time."
4. "Absolutely, you should both be comfortable with the decision. When would be a good time for me to call back after you've had a chance to discuss it?"
5. "Perfect, that's exactly what I'd expect you to do. Would it be helpful if I sent you some information about my company and the process so you can review it together?"

---

## 📞 PART 4 – Objection Handling

**Common Objections and Response Framework:**

### Seller Responses & Your Replies:

**💬 Seller Response #1:** "I want to think about it more."
**🔁 Closer Reply Bank:**
1. "I completely understand - this is a big decision. Help me understand what specifically you'd like to think over. Is it the offer amount, the timeline, or something else? Maybe I can provide clarity right now."
2. "That makes total sense. What questions are going through your mind that I might be able to answer? I'd rather address your concerns now than have you worry about them."
3. "Absolutely, take the time you need. What information would be most helpful for you to have while you're thinking it over?"
4. "Of course, and I respect that. Is there something specific that's making you hesitant? I'm happy to explain any part of the process in more detail."
5. "That's perfectly reasonable. While you're thinking, what would need to change for this to be a definite yes for you?"

**💬 Seller Response #2:** "I think I can get more money elsewhere."
**🔁 Closer Reply Bank:**
1. "You very well might be able to, and I respect that. Let me ask you this - after realtor fees, repairs, carrying costs, and time, what would you actually net? And what's your time worth over the next 6-12 months?"
2. "That's possible, and you should explore that option. But consider this - I can close in 2 weeks with certainty, versus 6 months of uncertainty, showings, and potential deals falling through. What's that peace of mind worth?"
3. "You might be right, and I encourage you to test the market. Just keep in mind that every month you wait costs you mortgage payments, insurance, utilities, and taxes. What are those monthly costs?"
4. "I understand that thinking. But remember, my offer is guaranteed cash in your hands. A higher listing price doesn't guarantee you'll get it, or that a deal will close. How important is certainty versus potentially getting more?"
5. "That's a fair point. But let me ask you this - if you could get $10,000 more but it takes 8 months longer and costs you $5,000 in carrying costs and stress, is that extra money worth it?"

**💬 Seller Response #3:** "I'm not ready to sell yet."
**🔁 Closer Reply Bank:**
1. "I hear you, and timing is everything. Can I ask what would need to happen for you to be ready? Is it a timing issue, or are there other factors?"
2. "That's totally fine. What's driving the timeline? Is there something specific you're waiting for, or do you just need more time to prepare?"
3. "I understand completely. When do you think you might be ready? I'd be happy to stay in touch and revisit this when the timing is better for you."
4. "No problem at all. Help me understand what 'ready' looks like for you. Is it a certain time of year, or are there things you need to accomplish first?"
5. "I respect that timing. What would change in your situation that would make you ready to sell? Maybe I can help with some of those factors."

**💬 Seller Response #4:** "I don't trust investors."
**🔁 Closer Reply Bank:**
1. "I completely understand that skepticism, and frankly, you should be cautious. There are some bad actors out there. That's exactly why I use licensed title companies, provide references, and have all proper licensing. What specifically concerns you?"
2. "Your caution is smart, and I respect that. I've heard the horror stories too. That's why I'm transparent about my process, use reputable title companies, and can provide references from recent sellers. What would make you feel comfortable?"
3. "That's actually good - you should be careful! The difference is that I'm a licensed professional who's been doing this legitimately for years. I can prove my credibility and track record. What would convince you I'm one of the good ones?"
4. "I don't blame you for feeling that way. Unfortunately, some investors have given the rest of us a bad name. That's why I'm fully licensed, insured, and use title companies for protection. What bad experiences have you heard about?"
5. "Smart to be cautious! I earn trust by being transparent, providing references, and ensuring all transactions go through proper legal channels. I'm happy to prove my legitimacy. What would give you confidence in working with me?"

**💬 Seller Response #5:** "The offer is just too low."
**🔁 Closer Reply Bank:**
1. "I hear you, and I want to make sure you're comparing apples to apples. If you listed for $50,000 more, after 6% realtor fees, that's $3,000 less already. Add repair costs, carrying costs, and time - what would you actually net?"
2. "I understand that feeling. But let me put this in perspective - my offer is guaranteed money in 2 weeks. If you listed higher, what are the chances you'd actually get that price, and how long might it take?"
3. "That's a fair reaction. But consider this - every month you don't sell costs you mortgage, taxes, insurance, and utilities. What are those monthly costs? After 6 months, how much have you spent just carrying the property?"
4. "I get it, and price is important. But what if I could close in 10 days and guarantee you won't have any more monthly expenses, repairs, or hassles? What's that worth to you?"
5. "I understand your position. Let me ask this - if another buyer offered you $10,000 more but needed financing, repairs, and 90 days to close, versus my guaranteed cash in 2 weeks, which would you choose?"

---

## 📞 PART 5 – Close & Next Steps

**Transition Statement:**
"Based on our conversation, I believe I can help you achieve your goals. Let me outline exactly what happens next."

### Seller Responses & Your Replies:

**💬 Seller Response #1:** "Okay, what's the next step?"
**🔁 Closer Reply Bank:**
1. "Perfect! The next step is for me to see the property in person so I can give you an exact offer. I can come by as early as tomorrow morning or afternoon. Which works better for you?"
2. "Excellent! I'll need to do a quick 15-minute walkthrough to finalize my offer. When would be convenient for you? I'm available tomorrow or the next day."
3. "Great! I'll schedule a brief property inspection - usually takes about 10-15 minutes. After that, I can give you a written offer within 24 hours. When can I come take a look?"
4. "Wonderful! I'll need to see the property to give you my final offer. I can usually work around your schedule. What day and time work best for you this week?"
5. "Perfect! The process is simple - I'll do a quick walkthrough, give you a written offer, and if you accept, we can close in 10-14 days. When can I come by to see the property?"

**💬 Seller Response #2:** "I still need to think about it."
**🔁 Closer Reply Bank:**
1. "Absolutely, and I respect that. How about this - let me come take a look at the property so I can give you an exact offer to consider. That way you'll have real numbers to think about. No obligation whatsoever."
2. "Of course, take your time. Would it help to have a written offer in hand while you're thinking? I can do a quick property visit and give you exact terms to consider."
3. "That's completely reasonable. Here's what I suggest - let me see the property and put together a formal offer. Then you can take all the time you need to decide. Fair enough?"
4. "I understand completely. Why don't I do the property walkthrough now so you have a real offer to consider? That way you're making a decision based on actual numbers, not estimates."
5. "Take all the time you need. But while you're thinking, it might help to have a concrete offer in writing. When could I briefly see the property to give you exact terms?"

**💬 Seller Response #3:** "When could you close?"
**🔁 Closer Reply Bank:**
1. "That's a great question! I can typically close in 10-14 days from acceptance. If you needed faster, I could potentially do 7 days. If you needed more time, I can work with your schedule. What timing would work best for you?"
2. "Excellent question! My standard closing is 2 weeks, but I've closed in as little as 5 days when needed. I can also extend the timeline if you need more time to find your next place. What's your ideal timeline?"
3. "I can usually close within 10-14 business days. If you're in a hurry, I can expedite to about a week. If you need more time, that's fine too. What timeframe would be ideal for your situation?"
4. "Great question! Typically 10-14 days, but I'm flexible based on your needs. If you need to close faster because of financial pressure, I can rush it. If you need more time to move, we can extend. What works for you?"
5. "I can close as quickly as 7-10 days if needed, or extend to 30+ days if you need time to find another place. My goal is to work around your timeline. When would be ideal for you?"

**💬 Seller Response #4:** "What if I don't like your offer?"
**🔁 Closer Reply Bank:**
1. "That's totally fine! There's absolutely no obligation. If my offer doesn't work for you, just say no. I'd rather you be completely happy with the decision. At minimum, you'll know exactly what a cash offer looks like for comparison."
2. "No problem whatsoever! This is a no-pressure situation. If my offer doesn't meet your needs, we'll shake hands and part as friends. At least you'll have a baseline for comparison with other options."
3. "Completely understood! You're under zero obligation to accept any offer I make. Think of it as free market research. You'll know what an investor cash offer looks like, which helps with any decision you make."
4. "That's perfectly fine! I make offers all the time that don't get accepted, and that's just business. No hard feelings at all. You'll just have good information to help with your decision-making process."
5. "No worries at all! I'd rather make you an honest offer that you decline than a fake offer that creates problems later. Worst case, you get a free property evaluation and know your options."

**💬 Seller Response #5:** "Let me call you back."
**🔁 Closer Reply Bank:**
1. "Absolutely! I understand you need time to process this. When do you think would be a good time for me to follow up? I don't want to be pushy, but I also don't want this opportunity to slip away if it's right for you."
2. "Of course, take your time. Just so I know how to best help you - when were you thinking of calling back? Tomorrow, next week? I want to make sure I'm available when you're ready."
3. "That sounds perfect. In the meantime, should I put together some information about my company and recent sales for you to review? When do you think you might be ready to continue the conversation?"
4. "Absolutely, I'll wait for your call. Just to set expectations - when do you think you might be ready to move forward? I want to make sure I keep my schedule open for you."
5. "Perfect! I respect that you need time. Would it be easier if I followed up with you instead? That way there's no pressure on you to remember to call. When would be a good time to check back?"

---

## 🎯 CLOSING FRAMEWORK

### Final Push Techniques:

1. **Urgency Creation:** "I'm only in your area this week for appointments. After that, it might be 3-4 weeks before I can get back."

2. **Scarcity:** "I typically only look at 2-3 properties per week, and I have one slot left this Thursday."

3. **Social Proof:** "I just helped a couple on [Street Name] sell their house in 8 days. They were amazed at how simple the process was."

4. **Risk Reversal:** "Here's what I'll do - let me come look at the property with no obligation. If my offer doesn't make sense, just say no. Fair enough?"

5. **Alternative Close:** "Would tomorrow morning or afternoon work better for you?"

---

## 📝 FOLLOW-UP SEQUENCE

If they don't commit on the call:

**Immediate Follow-up (within 2 hours):**
Text: "Hi [Name], thanks for your time today. Just wanted to confirm your address is [Address] and send you my information: [Company Info]. No pressure - here when you're ready!"

**24-Hour Follow-up:**
"Hi [Name], I've been thinking about our conversation yesterday. I realize I might have rushed through some details. Would you like me to explain anything more clearly? I'm here to help, not pressure."

**72-Hour Follow-up:**
"Hi [Name], just checking in. I know selling a house is a big decision. Did any other questions come up since we talked? I'm happy to provide more information or references."

**1-Week Follow-up:**
"Hi [Name], I hope you're doing well. I wanted to reach out one more time about your property. If the timing isn't right now, I completely understand. Would it be okay if I checked back in a few months?"

---

**Generated by WTF Platform ScriptMaster AI**
**Script ID: {str(uuid.uuid4())[:8]}**
**Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
        """
        
        return full_script
    
    def _get_cold_calling_scripts(self):
        return {
            'title': 'Cold Calling Master Script',
            'introduction': 'This script is designed for initial contact with motivated sellers from various lead sources.',
            'opening': "Hi [Name], I'm [Your Name] with [Company]. I know you weren't expecting my call, but I specialize in helping homeowners who need to sell quickly. Do you have 30 seconds?"
        }
    
    def _get_objection_scripts(self):
        return {
            'title': 'Objection Handling Arsenal',
            'introduction': 'Complete responses to every common objection you\'ll encounter.',
            'opening': "I completely understand that concern. Let me address that directly..."
        }
    
    def _get_followup_scripts(self):
        return {
            'title': 'Follow-up Sequence Scripts',
            'introduction': 'Systematic follow-up approaches for different lead temperatures.',
            'opening': "Hi [Name], I wanted to follow up on our conversation about your property..."
        }
    
    def _get_closing_scripts(self):
        return {
            'title': 'Closing Techniques Master Class',
            'introduction': 'Advanced closing techniques for converting leads to appointments.',
            'opening': "Based on everything we\'ve discussed, I believe I can help you..."
        }

# Initialize enhanced services
@st.cache_resource
def get_enhanced_services():
    return {
        'db': EnhancedDatabaseManager(),
        'calculator': DealCalculator(),
        'contract_generator': ContractGenerator(),
        'ai_assistant': EnhancedAIAssistant()
    }

services = get_enhanced_services()

# Enhanced Authentication
def enhanced_authenticate(username: str, password: str) -> tuple:
    """Enhanced authentication with role-based access"""
    conn = services['db'].get_connection()
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        SELECT id, username, email, role, full_name, subscription_tier 
        FROM users 
        WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, {
            'id': user[0],
            'username': user[1], 
            'email': user[2],
            'role': user[3],
            'full_name': user[4],
            'subscription_tier': user[5]
        }
    
    # Fallback to demo credentials
    demo_users = {
        'admin': {'password': 'admin123', 'role': 'admin', 'tier': 'enterprise'},
        'wholesaler': {'password': 'wholesale123', 'role': 'wholesaler', 'tier': 'pro'},
        'buyer': {'password': 'buyer123', 'role': 'buyer', 'tier': 'starter'}
    }
    
    if username in demo_users and demo_users[username]['password'] == password:
        return True, {
            'id': str(uuid.uuid4()),
            'username': username,
            'email': f"{username}@wtf.com",
            'role': demo_users[username]['role'],
            'full_name': username.title(),
            'subscription_tier': demo_users[username]['tier']
        }
    
    return False, None

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'show_landing' not in st.session_state:
    st.session_state.show_landing = True

# Landing Page
def render_landing_page():
    """Render landing page similar to buyboxcartel.com"""
    
    # Navigation bar
    st.markdown("""
    <div class='navbar'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <h2 style='margin: 0; background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                WTF Platform
            </h2>
            <div>
                <button onclick="document.getElementById('login-section').scrollIntoView()" 
                        style='background: transparent; border: 1px solid #8B5CF6; color: #8B5CF6; 
                               padding: 8px 16px; border-radius: 5px; margin-right: 10px;'>
                    Login
                </button>
                <button onclick="document.getElementById('pricing-section').scrollIntoView()" 
                        style='background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%); 
                               color: white; border: none; padding: 8px 16px; border-radius: 5px;'>
                    Get Started
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class='landing-hero'>
        <div class='hero-title'>Wholesale on Steroids</div>
        <div class='hero-subtitle'>The Complete Real Estate Wholesaling Platform</div>
        <p style='font-size: 1.2rem; margin-bottom: 2rem;'>
            Find deals, analyze properties, generate contracts, and close faster than ever before.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("## 🚀 Everything You Need to Scale Your Wholesaling Business")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #8B5CF6; text-align: center;'>🔍 Deal Analyzer</h3>
            <ul style='color: white;'>
                <li>Instant property analysis</li>
                <li>ARV calculations</li>
                <li>Rehab cost estimates</li>
                <li>70% rule automation</li>
                <li>ROI projections</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #10B981; text-align: center;'>👥 Buyer Network</h3>
            <ul style='color: white;'>
                <li>2,500+ verified cash buyers</li>
                <li>Instant buyer matching</li>
                <li>Automated notifications</li>
                <li>Proof of funds verified</li>
                <li>Multi-state coverage</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #F59E0B; text-align: center;'>📄 Contract Generator</h3>
            <ul style='color: white;'>
                <li>Legal contracts in minutes</li>
                <li>State-specific templates</li>
                <li>E-signature integration</li>
                <li>Assignment agreements</li>
                <li>Letters of intent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # More features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #EF4444; text-align: center;'>🤖 AI Assistant</h3>
            <ul style='color: white;'>
                <li>ScriptMaster AI for calls</li>
                <li>Underwriter GPT</li>
                <li>Deal coaching</li>
                <li>Objection handling</li>
                <li>Follow-up automation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #8B5CF6; text-align: center;'>📊 CRM Pipeline</h3>
            <ul style='color: white;'>
                <li>Lead management</li>
                <li>Deal tracking</li>
                <li>Follow-up reminders</li>
                <li>Performance analytics</li>
                <li>Team collaboration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #10B981; text-align: center;'>⚡ Lightning Leads</h3>
            <ul style='color: white;'>
                <li>Pre-qualified motivated sellers</li>
                <li>Real-time delivery</li>
                <li>Skip traced contacts</li>
                <li>AI scored leads</li>
                <li>98% close rate guarantee</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics section
    st.markdown("## 📈 Platform Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Deals Closed", "$50M+", help="Platform users have closed over $50M in deals")
    with col2:
        st.metric("Active Users", "5,000+", help="Growing community of wholesalers")
    with col3:
        st.metric("Average Deal Size", "$25K", help="Average wholesale fee per deal")
    with col4:
        st.metric("Time to Close", "14 Days", help="Average time from lead to close")
    
    # Pricing section
    st.markdown("<div id='pricing-section'></div>", unsafe_allow_html=True)
    st.markdown("## 💰 Choose Your Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='pricing-card'>
            <h3 style='color: #10B981;'>Starter</h3>
            <h2 style='color: white;'>$97/mo</h2>
            <ul style='color: white; text-align: left;'>
                <li>✅ Basic deal analyzer</li>
                <li>✅ 500 buyer network</li>
                <li>✅ Contract templates</li>
                <li>✅ Lead management</li>
                <li>✅ Email support</li>
                <li>❌ AI assistants</li>
                <li>❌ Lightning leads</li>
            </ul>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Starter Plan", key="starter", use_container_width=True):
            st.session_state.selected_plan = 'starter'
            st.session_state.show_landing = False
    
    with col2:
        st.markdown("""
        <div class='pricing-card' style='border-color: #8B5CF6; transform: scale(1.05);'>
            <div style='background: #8B5CF6; margin: -2rem -2rem 1rem -2rem; padding: 0.5rem; border-radius: 18px 18px 0 0;'>
                <h4 style='color: white; margin: 0;'>MOST POPULAR</h4>
            </div>
            <h3 style='color: #8B5CF6;'>Professional</h3>
            <h2 style='color: white;'>$297/mo</h2>
            <ul style='color: white; text-align: left;'>
                <li>✅ Advanced deal analyzer</li>
                <li>✅ 2,500 buyer network</li>
                <li>✅ All contract types</li>
                <li>✅ Full CRM system</li>
                <li>✅ AI assistants</li>
                <li>✅ 50 Lightning leads/mo</li>
                <li>✅ Priority support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Pro Plan", key="pro", use_container_width=True):
            st.session_state.selected_plan = 'professional'
            st.session_state.show_landing = False
    
    with col3:
        st.markdown("""
        <div class='pricing-card'>
            <h3 style='color: #F59E0B;'>Enterprise</h3>
            <h2 style='color: white;'>$997/mo</h2>
            <ul style='color: white; text-align: left;'>
                <li>✅ Everything in Pro</li>
                <li>✅ Unlimited buyers</li>
                <li>✅ White-label option</li>
                <li>✅ Custom integrations</li>
                <li>✅ Dedicated success manager</li>
                <li>✅ Unlimited Lightning leads</li>
                <li>✅ Phone support</li>
            </ul>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Contact Sales", key="enterprise", use_container_width=True):
            st.session_state.selected_plan = 'enterprise'
            st.session_state.show_landing = False
    
    # Login section
    st.markdown("<div id='login-section'></div>", unsafe_allow_html=True)
    st.markdown("## 🔑 Already a Member? Sign In")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(139, 92, 246, 0.3);'>
        """, unsafe_allow_html=True)
        
        with st.form("landing_login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("Sign In", use_container_width=True)
            with col2:
                demo_submitted = st.form_submit_button("Try Demo", use_container_width=True)
            
            if login_submitted:
                success, user_data = enhanced_authenticate(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.show_landing = False
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            
            if demo_submitted:
                # Auto-login as demo user
                success, user_data = enhanced_authenticate('wholesaler', 'wholesale123')
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.show_landing = False
                    st.success("Demo access granted!")
                    st.rerun()
        
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

# Enhanced Sidebar with Role-Based Navigation
def render_enhanced_sidebar():
    """Enhanced sidebar with role-based navigation"""
    user_role = st.session_state.user_data.get('role', 'wholesaler')
    full_name = st.session_state.user_data.get('full_name', 'User')
    
    # Role-based styling
    role_colors = {
        'admin': 'linear-gradient(135deg, #DC2626 0%, #7C2D12 100%)',
        'wholesaler': 'linear-gradient(135deg, #8B5CF6 0%, #5B21B6 100%)',
        'buyer': 'linear-gradient(135deg, #10B981 0%, #065F46 100%)'
    }
    
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: {role_colors.get(user_role, role_colors["wholesaler"])}; 
                border-radius: 10px; margin-bottom: 1rem;'>
        <h1 style='color: white; font-size: 2rem; font-weight: bold; margin: 0;'>WTF</h1>
        <p style='color: white; font-weight: bold; margin: 0;'>Wholesale on Steroids</p>
        <p style='color: white; font-size: 0.9rem; margin: 0;'>{user_role.title()} Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role-based navigation
    if user_role == 'admin':
        pages = {
            "🏠 Admin Dashboard": "admin_dashboard",
            "👥 User Management": "user_management", 
            "📊 Platform Analytics": "platform_analytics",
            "💰 Revenue Dashboard": "revenue_dashboard",
            "🔧 System Settings": "system_settings",
            "📋 Master Dispo": "master_dispo",
            "🤖 AI Management": "ai_management"
        }
    elif user_role == 'wholesaler':
        pages = {
            "🏠 Dashboard": "dashboard",
            "🔍 Deal Analyzer": "deal_analyzer", 
            "👥 Buyer Network": "buyers",
            "📞 Lead Manager": "leads",
            "📋 Pipeline": "pipeline",
            "📄 Contracts & LOI": "contracts",
            "⚡ Lightning Leads": "lightning_leads",
            "🤖 AI Assistant": "ai_assistant",
            "📊 Analytics": "analytics"
        }
    else:  # buyer
        pages = {
            "🏠 Buyer Dashboard": "buyer_dashboard",
            "🔍 Available Deals": "available_deals",
            "📋 My Offers": "my_offers", 
            "📊 Market Analysis": "market_analysis",
            "⚙️ Preferences": "buyer_preferences"
        }
    
    selected_page = st.sidebar.selectbox(
        "Navigate",
        list(pages.keys()),
        key="navigation"
    )
    
    # User info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**User:** {full_name}")
    st.sidebar.markdown(f"**Role:** {user_role.title()}")
    st.sidebar.markdown(f"**Plan:** {st.session_state.user_data.get('subscription_tier', 'Free').title()}")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.show_landing = True
        st.rerun()
    
    return pages[selected_page]

# Enhanced Deal Analyzer Page
def render_deal_analyzer():
    """Enhanced deal analyzer with comprehensive calculations"""
    st.markdown('<h1 class="main-header">🔍 Deal Analyzer</h1>', unsafe_allow_html=True)
    
    # Property input form
    with st.form("deal_analyzer_form"):
        st.markdown("### Property Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            address = st.text_input("Property Address*", placeholder="123 Main Street")
            city = st.text_input("City*", placeholder="Dallas")
            state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA", "NC", "OH", "MI", "PA", "IL"])
            zip_code = st.text_input("ZIP Code*", placeholder="75201")
        
        with col2:
            property_type = st.selectbox("Property Type", 
                                       ["single_family", "multi_family", "condo", "townhouse"])
            bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
            square_feet = st.number_input("Square Feet", min_value=0, max_value=10000, value=1800)
        
        with col3:
            year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1995)
            list_price = st.number_input("List/Asking Price ($)", min_value=0, value=250000)
            condition = st.selectbox("Condition", 
                                   ["excellent", "good", "fair", "poor", "needs_rehab"])
            estimated_rent = st.number_input("Estimated Monthly Rent ($)", min_value=0, value=2000)
        
        # Advanced options
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Market Adjustments")
                market_appreciation = st.slider("Annual Appreciation (%)", 0.0, 10.0, 3.0, 0.1)
                rent_growth = st.slider("Annual Rent Growth (%)", 0.0, 8.0, 2.0, 0.1)
                
            with col2:
                st.markdown("#### Investment Strategy")
                strategy = st.selectbox("Primary Strategy", 
                                       ["wholesale", "fix_flip", "buy_hold", "brrrr"])
                hold_period = st.number_input("Hold Period (years)", 1, 30, 5)
        
        analyze_button = st.form_submit_button("🔍 Analyze Deal", type="primary")
    
    if analyze_button and address and city:
        property_data = {
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'property_type': property_type,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'square_feet': square_feet,
            'year_built': year_built,
            'list_price': list_price,
            'condition': condition,
            'estimated_rent': estimated_rent,
            'market_appreciation': market_appreciation,
            'rent_growth': rent_growth,
            'strategy': strategy,
            'hold_period': hold_period
        }
        
        with st.spinner("🧮 Crunching the numbers..."):
            analysis = services['calculator'].calculate_deal_metrics(property_data)
            
            # Deal Grade
            grade = analysis['deal_grade']
            grade_colors = {'A': '#10B981', 'B': '#8B5CF6', 'C': '#F59E0B', 'D': '#EF4444'}
            
            st.markdown(f"""
            <div class='deal-calculator'>
                <div style='text-align: center;'>
                    <h2 style='color: {grade_colors.get(grade, '#6B7280')}; margin: 0;'>
                        Deal Grade: {grade}
                    </h2>
                    <p style='margin: 0.5rem 0;'>
                        {['Excellent Deal!', 'Good Deal', 'Marginal Deal', 'Poor Deal'][ord(grade) - ord('A')]}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key Metrics
            st.markdown("## 📊 Key Investment Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("ARV", f"${analysis['arv']:,.0f}")
                st.metric("Rehab Cost", f"${analysis['rehab_cost']:,.0f}")
            
            with col2:
                st.metric("Max Offer (70%)", f"${analysis['max_offers']['70_percent']:,.0f}")
                st.metric("Max Offer (75%)", f"${analysis['max_offers']['75_percent']:,.0f}")
            
            with col3:
                st.metric("Max Offer (80%)", f"${analysis['max_offers']['80_percent']:,.0f}")
                st.metric("Profit Potential", f"${analysis['profit_potential']:,.0f}")
            
            with col4:
                st.metric("Monthly Rent", f"${analysis['estimated_rent']:,.0f}")
                spread = analysis['arv'] - list_price
                st.metric("Price vs ARV", f"${spread:,.0f}", 
                         delta=f"{(spread/list_price)*100:.1f}%" if list_price > 0 else "0%")
            
            # Investment Strategy Analysis
            st.markdown("## 💰 Investment Strategy Breakdown")
            
            # Entry Fee Breakdown
            st.markdown("### 💸 Entry Fee Breakdown by Tier")
            
            entry_df = pd.DataFrame({
                'Tier': ['Low (SubTo/Cash)', 'Medium (Seller Finance)', 'High (Wrap/Hybrid)'],
                'Offer Price': [f"${analysis['entry_fees'][tier]['offer_price']:,.0f}" for tier in ['low', 'medium', 'high']],
                'Down Payment': [f"${analysis['entry_fees'][tier]['down_payment']:,.0f}" for tier in ['low', 'medium', 'high']],
                'Total Entry Fee': [f"${analysis['entry_fees'][tier]['total_entry_fee']:,.0f}" for tier in ['low', 'medium', 'high']],
                'Financing Type': [analysis['entry_fees'][tier]['financing_type'] for tier in ['low', 'medium', 'high']]
            })
            
            st.dataframe(entry_df, use_container_width=True)
            
            # Returns Analysis
            st.markdown("### 📈 Returns Analysis")
            
            returns_df = pd.DataFrame({
                'Tier': ['Low', 'Medium', 'High'],
                'Monthly Cash Flow': [f"${analysis['returns'][tier]['net_cash_flow']:,.0f}" for tier in ['low', 'medium', 'high']],
                'Cash-on-Cash Return': [f"{analysis['returns'][tier]['cash_on_cash']:.1f}%" for tier in ['low', 'medium', 'high']],
                'Cap Rate': [f"{analysis['returns'][tier]['cap_rate']:.1f}%" for tier in ['low', 'medium', 'high']],
                'DSCR': [f"{analysis['returns'][tier]['dscr']:.2f}" for tier in ['low', 'medium', 'high']]
            })
            
            st.dataframe(returns_df, use_container_width=True)
            
            # Wholesale Analysis
            st.markdown("### 🏃‍♂️ Wholesale Analysis")
            
            wholesale_data = list(analysis['wholesale_analysis'].values())
            wholesale_df = pd.DataFrame({
                'Assignment Fee': [f"${w['assignment_fee']:,.0f}" for w in wholesale_data],
                'Profit': [f"${w['profit']:,.0f}" for w in wholesale_data],
                'ROI': [f"{w['roi']:.1f}%" for w in wholesale_data],
                'Time to Close': [w['time_to_close'] for w in wholesale_data]
            })
            
            st.dataframe(wholesale_df, use_container_width=True)
            
            # Action buttons
            st.markdown("### 🎯 Next Actions")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📄 Generate LOI", use_container_width=True):
                    st.session_state.generate_loi_data = property_data
                    st.session_state.loi_offer_price = analysis['max_offers']['70_percent']
                    st.success("LOI data prepared! Go to Contracts & LOI page.")
            
            with col2:
                if st.button("👥 Find Buyers", use_container_width=True):
                    st.session_state.property_for_buyers = property_data
                    st.success("Searching buyer network...")
            
            with col3:
                if st.button("📊 Save Analysis", use_container_width=True):
                    # Save to database
                    property_id = str(uuid.uuid4())
                    st.session_state.saved_analysis = {
                        'property_id': property_id,
                        'analysis': analysis
                    }
                    st.success("Analysis saved to pipeline!")
            
            with col4:
                if st.button("📋 Create Deal", use_container_width=True):
                    st.session_state.create_deal_data = {
                        'property_data': property_data,
                        'analysis': analysis
                    }
                    st.success("Deal creation initiated!")

# Enhanced Lead Management with Full CRM
def render_enhanced_leads():
    """Enhanced lead management with full CRM functionality"""
    st.markdown('<h1 class="main-header">📞 Lead Manager CRM</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Lead Dashboard", "➕ Add Lead", "📊 Lead Scoring", "📞 Call Center", "📧 Email Campaign"])
    
    with tab1:
        render_lead_dashboard()
    
    with tab2:
        render_add_lead_form()
    
    with tab3:
        render_lead_scoring()
    
    with tab4:
        render_call_center()
    
    with tab5:
        render_email_campaign()

def render_lead_dashboard():
    """Enhanced lead dashboard with CRM features"""
    # Lead metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Leads", "1,247", delta="47 this week")
    with col2:
        st.metric("Hot Leads", "89", delta="12 new")
    with col3:
        st.metric("Conversion Rate", "24.7%", delta="2.1%")
    with col4:
        st.metric("Avg Response Time", "2.3 hrs", delta="-0.8 hrs")
    with col5:
        st.metric("This Month Revenue", "$127K", delta="$23K")
    
    # Filters and search
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Status", ["All", "New", "Contacted", "Interested", "Under Contract", "Closed", "Dead"])
    with col2:
        source_filter = st.selectbox("Source", ["All", "Cold Calling", "Direct Mail", "PPC", "SEO", "Referral", "Lightning Leads"])
    with col3:
        assigned_filter = st.selectbox("Assigned To", ["All", "Me", "Team Member 1", "Team Member 2", "Unassigned"])
    with col4:
        search_input = st.text_input("🔍 Search", placeholder="Name, phone, address...")
    
    # Lead scoring color coding
    def get_score_color(score):
        if score >= 80:
            return "#10B981"  # Green - Hot
        elif score >= 60:
            return "#F59E0B"  # Yellow - Warm  
        else:
            return "#6B7280"  # Gray - Cold
    
    # Mock lead data with enhanced CRM fields
    leads_data = [
        {
            'id': 'L001',
            'name': 'Maria Garcia',
            'phone': '(555) 111-2222',
            'email': 'maria@email.com',
            'address': '123 Main St, Dallas, TX',
            'status': 'Interested',
            'score': 85,
            'source': 'Cold Calling',
            'motivation': 'Divorce',
            'timeline': 'ASAP',
            'property_value': 250000,
            'owed_amount': 180000,
            'equity': 70000,
            'last_contact': '2024-08-08',
            'next_followup': '2024-08-10',
            'assigned_to': 'John Smith',
            'notes': 'Very motivated, going through divorce proceedings'
        },
        {
            'id': 'L002', 
            'name': 'David Brown',
            'phone': '(555) 222-3333',
            'email': 'david@email.com',
            'address': '456 Oak Ave, Houston, TX',
            'status': 'Contacted',
            'score': 72,
            'source': 'Direct Mail',
            'motivation': 'Job Relocation',
            'timeline': '30-60 days',
            'property_value': 320000,
            'owed_amount': 240000,
            'equity': 80000,
            'last_contact': '2024-08-07',
            'next_followup': '2024-08-09',
            'assigned_to': 'Sarah Johnson', 
            'notes': 'Moving to California for work, needs quick sale'
        },
        {
            'id': 'L003',
            'name': 'Jennifer Lee',
            'phone': '(555) 333-4444', 
            'email': 'jennifer@email.com',
            'address': '789 Pine Rd, Austin, TX',
            'status': 'New',
            'score': 68,
            'source': 'Lightning Leads',
            'motivation': 'Inherited Property',
            'timeline': '60-90 days',
            'property_value': 180000,
            'owed_amount': 0,
            'equity': 180000,
            'last_contact': 'Never',
            'next_followup': '2024-08-09',
            'assigned_to': 'Unassigned',
            'notes': 'Inherited from grandmother, lives out of state'
        }
    ]
    
    # Display leads with CRM functionality
    for lead in leads_data:
        score_color = get_score_color(lead['score'])
        
        with st.expander(f"{lead['name']} - {lead['address']} (Score: {lead['score']}) - {lead['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Contact Info")
                st.write(f"**Phone:** {lead['phone']}")
                st.write(f"**Email:** {lead['email']}")
                st.write(f"**Source:** {lead['source']}")
                st.write(f"**Assigned To:** {lead['assigned_to']}")
            
            with col2:
                st.markdown("#### Property Details")
                st.write(f"**Est. Value:** ${lead['property_value']:,.0f}")
                st.write(f"**Owed Amount:** ${lead['owed_amount']:,.0f}")
                st.write(f"**Equity:** ${lead['equity']:,.0f}")
                st.write(f"**Motivation:** {lead['motivation']}")
            
            with col3:
                st.markdown("#### Timeline & Status")
                st.write(f"**Status:** {lead['status']}")
                st.write(f"**Timeline:** {lead['timeline']}")
                st.write(f"**Last Contact:** {lead['last_contact']}")
                st.write(f"**Next Follow-up:** {lead['next_followup']}")
            
            # Notes section
            st.markdown("#### Notes")
            st.write(lead['notes'])
            
            # Action buttons
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                if st.button("📞 Call", key=f"call_{lead['id']}", use_container_width=True):
                    st.session_state.active_call = lead
                    st.success(f"Initiating call to {lead['name']}")
            
            with col2:
                if st.button("📧 Email", key=f"email_{lead['id']}", use_container_width=True):
                    st.session_state.compose_email = lead
                    st.success(f"Composing email to {lead['name']}")
            
            with col3:
                if st.button("💬 SMS", key=f"sms_{lead['id']}", use_container_width=True):
                    st.session_state.send_sms = lead
                    st.success(f"SMS sent to {lead['name']}")
            
            with col4:
                if st.button("📊 Analyze", key=f"analyze_{lead['id']}", use_container_width=True):
                    st.session_state.analyze_property = lead
                    st.info(f"Analyzing property for {lead['name']}")
            
            with col5:
                if st.button("📄 LOI", key=f"loi_{lead['id']}", use_container_width=True):
                    st.session_state.generate_loi = lead
                    st.success(f"LOI prepared for {lead['name']}")
            
            with col6:
                if st.button("🏠 Deal", key=f"deal_{lead['id']}", use_container_width=True):
                    st.session_state.create_deal = lead
                    st.success(f"Deal created for {lead['name']}")

def render_add_lead_form():
    """Enhanced add lead form"""
    st.markdown("### Add New Lead to CRM")
    
    with st.form("enhanced_add_lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Contact Information")
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*") 
            phone = st.text_input("Phone Number*")
            email = st.text_input("Email")
            secondary_phone = st.text_input("Secondary Phone")
            
        with col2:
            st.markdown("#### Property Information")
            property_address = st.text_input("Property Address*")
            property_city = st.text_input("City*")
            property_state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA", "NC", "OH", "MI"])
            property_zip = st.text_input("ZIP Code*")
            property_type = st.selectbox("Property Type", ["Single Family", "Multi Family", "Condo", "Townhouse"])
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### Motivation & Timeline")
            motivation = st.multiselect("Motivation (select all that apply)", 
                ["Divorce", "Financial Hardship", "Job Relocation", "Inherited Property", 
                 "Tired Landlord", "Downsizing", "Health Issues", "Behind on Payments", "Other"])
            timeline = st.selectbox("Timeline", 
                ["ASAP", "1-30 days", "30-60 days", "60-90 days", "90+ days", "Flexible"])
            source = st.selectbox("Lead Source", 
                ["Cold Calling", "Direct Mail", "PPC", "SEO", "Referral", "Social Media", 
                 "Lightning Leads", "Driving for Dollars", "Bandit Signs", "Other"])
        
        with col4:
            st.markdown("#### Financial Information")
            estimated_value = st.number_input("Estimated Property Value ($)", min_value=0, value=200000)
            owed_amount = st.number_input("Amount Owed ($)", min_value=0, value=150000)
            monthly_payment = st.number_input("Monthly Payment ($)", min_value=0, value=1200)
            property_condition = st.selectbox("Property Condition", 
                ["Excellent", "Good", "Fair", "Poor", "Needs Major Repairs"])
        
        # Additional details
        with st.expander("Additional Details"):
            col5, col6 = st.columns(2)
            
            with col5:
                bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
                bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
                square_feet = st.number_input("Square Feet", min_value=0, value=1800)
                year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1995)
            
            with col6:
                occupancy = st.selectbox("Occupancy", ["Owner Occupied", "Tenant Occupied", "Vacant"])
                rental_income = st.number_input("Monthly Rental Income ($)", min_value=0, value=0)
                repairs_needed = st.text_area("Repairs Needed")
                
        # Assignment and priority
        col7, col8 = st.columns(2)
        
        with col7:
            assigned_to = st.selectbox("Assign To", ["Unassigned", "John Smith", "Sarah Johnson", "Mike Davis"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        with col8:
            next_followup = st.date_input("Next Follow-up Date")
            initial_notes = st.text_area("Initial Notes")
        
        # Submit button
        if st.form_submit_button("Add Lead to CRM", type="primary"):
            if first_name and last_name and phone and property_address:
                # Calculate initial lead score
                lead_score = calculate_lead_score({
                    'motivation': motivation,
                    'timeline': timeline,
                    'equity': estimated_value - owed_amount,
                    'condition': property_condition,
                    'occupancy': occupancy
                })
                
                lead_id = str(uuid.uuid4())
                
                # Here you would save to database
                st.success(f"✅ Lead {first_name} {last_name} added successfully!")
                st.info(f"📊 Initial Lead Score: {lead_score}/100")
                st.info(f"🆔 Lead ID: {lead_id}")
                
                # Show next steps
                st.markdown("#### 🎯 Recommended Next Steps:")
                st.write("• Schedule initial contact call")
                st.write("• Send property analysis request")
                st.write("• Add to appropriate follow-up sequence")
                
            else:
                st.error("Please fill in all required fields")

def calculate_lead_score(lead_data):
    """Calculate lead score based on various factors"""
    score = 0
    
    # Motivation scoring (30 points max)
    high_motivation = ["Divorce", "Financial Hardship", "Behind on Payments", "Health Issues"]
    medium_motivation = ["Job Relocation", "Inherited Property", "Tired Landlord"]
    
    for motivation in lead_data.get('motivation', []):
        if motivation in high_motivation:
            score += 10
        elif motivation in medium_motivation:
            score += 5
    
    # Timeline scoring (25 points max)
    timeline_scores = {
        "ASAP": 25,
        "1-30 days": 20,
        "30-60 days": 15,
        "60-90 days": 10,
        "90+ days": 5,
        "Flexible": 8
    }
    score += timeline_scores.get(lead_data.get('timeline'), 0)
    
    # Equity scoring (25 points max)
    equity = lead_data.get('equity', 0)
    if equity >= 100000:
        score += 25
    elif equity >= 50000:
        score += 20
    elif equity >= 25000:
        score += 15
    elif equity >= 10000:
        score += 10
    elif equity > 0:
        score += 5
    
    # Condition scoring (10 points max)
    condition_scores = {
        "Excellent": 2,
        "Good": 4,
        "Fair": 6,
        "Poor": 8,
        "Needs Major Repairs": 10
    }
    score += condition_scores.get(lead_data.get('condition'), 0)
    
    # Occupancy scoring (10 points max)
    occupancy_scores = {
        "Vacant": 10,
        "Owner Occupied": 8,
        "Tenant Occupied": 5
    }
    score += occupancy_scores.get(lead_data.get('occupancy'), 0)
    
    return min(score, 100)

def render_lead_scoring():
    """Lead scoring analysis and management"""
    st.markdown("### 📊 Lead Scoring System")
    
    # Scoring criteria explanation
    st.markdown("""
    #### How We Score Leads (0-100 points):
    
    **Motivation (30 points max):**
    - High urgency (Divorce, Financial Hardship, Behind on Payments): 10 points each
    - Medium urgency (Job Relocation, Inherited Property): 5 points each
    
    **Timeline (25 points max):**
    - ASAP: 25 points
    - 1-30 days: 20 points  
    - 30-60 days: 15 points
    - 60-90 days: 10 points
    
    **Equity (25 points max):**
    - $100K+: 25 points
    - $50K-100K: 20 points
    - $25K-50K: 15 points
    - $10K-25K: 10 points
    
    **Property Condition (10 points max):**
    - Needs Major Repairs: 10 points
    - Poor: 8 points
    - Fair: 6 points
    
    **Occupancy (10 points max):**
    - Vacant: 10 points
    - Owner Occupied: 8 points
    - Tenant Occupied: 5 points
    """)
    
    # Lead score distribution
    score_data = pd.DataFrame({
        'Score Range': ['80-100 (Hot)', '60-79 (Warm)', '40-59 (Cool)', '0-39 (Cold)'],
        'Count': [23, 45, 89, 156],
        'Conversion Rate': ['45%', '25%', '12%', '3%'],
        'Avg Days to Close': [14, 28, 45, 90]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_score = px.pie(score_data, values='Count', names='Score Range',
                          title='Lead Distribution by Score',
                          color_discrete_sequence=['#10B981', '#F59E0B', '#8B5CF6', '#6B7280'])
        st.plotly_chart(fig_score, use_container_width=True)
    
    with col2:
        fig_conversion = px.bar(score_data, x='Score Range', y='Conversion Rate',
                               title='Conversion Rate by Score Range',
                               color='Score Range',
                               color_discrete_sequence=['#10B981', '#F59E0B', '#8B5CF6', '#6B7280'])
        st.plotly_chart(fig_conversion, use_container_width=True)
    
    # Lead scoring calculator
    st.markdown("#### 🧮 Lead Score Calculator")
    
    with st.form("score_calculator"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            calc_motivation = st.multiselect("Motivation", 
                ["Divorce", "Financial Hardship", "Job Relocation", "Inherited Property", 
                 "Tired Landlord", "Behind on Payments"])
            calc_timeline = st.selectbox("Timeline", 
                ["ASAP", "1-30 days", "30-60 days", "60-90 days", "90+ days"])
        
        with col2:
            calc_equity = st.number_input("Estimated Equity ($)", min_value=0, value=50000)
            calc_condition = st.selectbox("Condition", 
                ["Excellent", "Good", "Fair", "Poor", "Needs Major Repairs"])
        
        with col3:
            calc_occupancy = st.selectbox("Occupancy", 
                ["Owner Occupied", "Tenant Occupied", "Vacant"])
        
        if st.form_submit_button("Calculate Score"):
            calc_data = {
                'motivation': calc_motivation,
                'timeline': calc_timeline,
                'equity': calc_equity,
                'condition': calc_condition,
                'occupancy': calc_occupancy
            }
            
            calculated_score = calculate_lead_score(calc_data)
            
            score_color = "#10B981" if calculated_score >= 80 else "#F59E0B" if calculated_score >= 60 else "#6B7280"
            
            st.markdown(f"""
            <div style='background: rgba(139, 92, 246, 0.1); padding: 2rem; border-radius: 15px; text-align: center;'>
                <h2 style='color: {score_color}; margin: 0;'>Lead Score: {calculated_score}/100</h2>
                <p style='color: white; margin: 0.5rem 0;'>
                    {'🔥 HOT LEAD' if calculated_score >= 80 else '🌡️ WARM LEAD' if calculated_score >= 60 else '❄️ COLD LEAD'}
                </p>
            </div>
            """, unsafe_allow_html=True)

def render_call_center():
    """Call center interface with dialer and script assistant"""
    st.markdown("### 📞 Call Center & Dialer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Today's Call List")
        
        # Call list with priorities
        call_list = [
            {'name': 'Maria Garcia', 'phone': '(555) 111-2222', 'score': 85, 'priority': 'High', 'last_contact': '3 days ago'},
            {'name': 'David Brown', 'phone': '(555) 222-3333', 'score': 72, 'priority': 'Medium', 'last_contact': '1 day ago'},
            {'name': 'Jennifer Lee', 'phone': '(555) 333-4444', 'score': 68, 'priority': 'Medium', 'last_contact': 'Never'},
            {'name': 'Thomas Wilson', 'phone': '(555) 444-5555', 'score': 45, 'priority': 'Low', 'last_contact': '1 week ago'}
        ]
        
        for i, contact in enumerate(call_list):
            priority_color = {'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#6B7280'}
            
            with st.container():
                col_a, col_b, col_c, col_d = st.columns([3, 2, 2, 1])
                
                with col_a:
                    st.write(f"**{contact['name']}** - {contact['phone']}")
                with col_b:
                    st.write(f"Score: {contact['score']}")
                with col_c:
                    st.write(f"Last: {contact['last_contact']}")
                with col_d:
                    if st.button("📞", key=f"call_btn_{i}", help="Start Call"):
                        st.session_state.active_call_contact = contact
                        st.success(f"Calling {contact['name']}...")
                
                st.markdown(f"<div style='height: 3px; background: {priority_color[contact['priority']]}; margin: 5px 0;'></div>", 
                           unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Call Statistics")
        st.metric("Calls Today", "47", delta="12")
        st.metric("Contacts Made", "23", delta="7") 
        st.metric("Appointments Set", "8", delta="3")
        st.metric("Conversion Rate", "17%", delta="2%")
        
        # Quick dial
        st.markdown("#### Quick Dial")
        quick_phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
        if st.button("📞 Call Now", use_container_width=True):
            if quick_phone:
                st.success(f"Calling {quick_phone}...")
    
    # Active call interface
    if 'active_call_contact' in st.session_state:
        st.markdown("---")
        st.markdown("### 📞 Active Call Interface")
        
        contact = st.session_state.active_call_contact
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### Calling: {contact['name']} - {contact['phone']}")
            
            # Call timer (mock)
            st.markdown("**Call Duration:** 00:02:15")
            
            # Script assistant
            st.markdown("#### 📝 Script Assistant")
            
            script_sections = {
                "Opening": "Hi [Name], I'm [Your Name] with [Company]. I know you weren't expecting my call, but I specialize in helping homeowners who need to sell quickly. Do you have 30 seconds?",
                "Discovery": "Can you tell me a little about your property? What's prompting you to consider selling?",
                "Objection - Not Interested": "I completely understand, and most people say the same thing initially. But let me ask - if you could sell quickly without repairs or realtor fees, would that change anything?",
                "Close for Appointment": "Based on what you've told me, I think I can help. When would be a good time for me to take a quick look at the property?"
            }
            
            selected_script = st.selectbox("Select Script Section", list(script_sections.keys()))
            
            st.markdown(f"**Script:**")
            st.info(script_sections[selected_script])
            
        with col2:
            st.markdown("#### Call Actions")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("✅ Contact Made", use_container_width=True):
                    st.success("Contact logged!")
            
            with col_b:
                if st.button("📅 Set Appointment", use_container_width=True):
                    st.success("Appointment scheduled!")
            
            if st.button("📝 Add Notes", use_container_width=True):
                st.session_state.show_call_notes = True
            
            if st.button("❌ End Call", use_container_width=True):
                del st.session_state.active_call_contact
                st.rerun()
            
            # Disposition options
            st.markdown("#### Call Disposition")
            disposition = st.selectbox("Result", 
                ["No Answer", "Busy", "Voicemail", "Contact Made", "Not Interested", 
                 "Interested", "Appointment Set", "Remove from List"])
            
            if st.button("Save Disposition", use_container_width=True):
                st.success(f"Disposition saved: {disposition}")
        
        # Call notes
        if st.session_state.get('show_call_notes', False):
            st.markdown("#### 📝 Call Notes")
            call_notes = st.text_area("Notes from this call:", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Notes"):
                    st.success("Notes saved!")
                    st.session_state.show_call_notes = False
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_call_notes = False
                    st.rerun()

def render_email_campaign():
    """Email campaign management"""
    st.markdown("### 📧 Email Campaign Manager")
    
    tab1, tab2, tab3 = st.tabs(["📤 Send Campaign", "📊 Campaign Analytics", "📝 Templates"])
    
    with tab1:
        st.markdown("#### Create Email Campaign")
        
        with st.form("email_campaign_form"):
            campaign_name = st.text_input("Campaign Name*", placeholder="Monthly Property Update")
            
            col1, col2 = st.columns(2)
            
            with col1:
                recipient_filter = st.multiselect("Send To", 
                    ["All Leads", "Hot Leads (80+)", "Warm Leads (60-79)", "New Leads", 
                     "Contacted Leads", "Interested Leads", "Custom List"])
                
                send_time = st.selectbox("Send Time", 
                    ["Send Immediately", "Schedule for Later", "Best Time (AI Optimized)"])
            
            with col2:
                email_template = st.selectbox("Email Template", 
                    ["Property Update", "Market Report", "New Listing Alert", 
                     "Follow-up Sequence", "Custom"])
                
                if send_time == "Schedule for Later":
                    schedule_date = st.datetime_input("Schedule Date & Time")
            
            subject_line = st.text_input("Subject Line*", 
                                       placeholder="New Investment Opportunity in Your Area")
            
            email_content = st.text_area("Email Content*", height=200,
                                       placeholder="""Hi {first_name},

I hope this email finds you well. I wanted to reach out about your property at {property_address}.

We're currently seeing strong buyer demand in your area, and I believe now might be a great time to discuss your selling options.

Would you be interested in a no-obligation consultation to explore your options?

Best regards,
{sender_name}""")
            
            # Personalization tokens
            st.markdown("**Available Tokens:** {first_name}, {last_name}, {property_address}, {estimated_value}, {sender_name}")
            
            if st.form_submit_button("Send Campaign", type="primary"):
                if campaign_name and subject_line and email_content:
                    recipient_count = 156  # Mock count
                    st.success(f"✅ Campaign '{campaign_name}' sent to {recipient_count} recipients!")
                    st.info("📊 Campaign tracking has been enabled. Check Analytics tab for results.")
                else:
                    st.error("Please fill in all required fields")
    
    with tab2:
        st.markdown("#### Campaign Performance Analytics")
        
        # Campaign metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Campaigns Sent", "47", delta="3 this week")
        with col2:
            st.metric("Total Recipients", "12,456", delta="234")
        with col3:
            st.metric("Open Rate", "24.7%", delta="2.1%")
        with col4:
            st.metric("Response Rate", "3.2%", delta="0.8%")
        
        # Recent campaigns
        st.markdown("#### Recent Campaigns")
        
        campaigns_data = pd.DataFrame({
            'Campaign': ['July Market Update', 'New Listing Alert', 'Follow-up Sequence #3', 'Property Spotlight'],
            'Recipients': [234, 189, 345, 156],
            'Open Rate': ['28.4%', '22.1%', '31.2%', '19.8%'],
            'Click Rate': ['4.2%', '6.1%', '3.8%', '2.9%'],
            'Responses': [8, 12, 6, 3],
            'Status': ['Completed', 'Completed', 'In Progress', 'Scheduled']
        })
        
        st.dataframe(campaigns_data, use_container_width=True)
        
        # Performance chart
        fig_email = px.line(
            x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            y=[22.1, 24.7, 23.8, 26.2],
            title='Email Open Rate Trend',
            labels={'x': 'Week', 'y': 'Open Rate (%)'}
        )
        st.plotly_chart(fig_email, use_container_width=True)
    
    with tab3:
        st.markdown("#### Email Templates")
        
        templates = {
            "Property Update": {
                "subject": "Update on Your Property at {property_address}",
                "content": """Hi {first_name},

I hope you're doing well. I wanted to follow up regarding your property at {property_address}.

The market in your area has been quite active lately, and I believe there are some good opportunities for homeowners looking to sell.

Would you be interested in a brief conversation about your property and current market conditions?

Best regards,
{sender_name}"""
            },
            "Market Report": {
                "subject": "Your Neighborhood Market Report - {city}",
                "content": """Hello {first_name},

I've prepared a market analysis for your area that I thought you might find interesting.

Key highlights for {city}:
• Average home values have increased by 8.2% this year
• Average days on market: 23 days
• Strong buyer demand continues

If you've been considering selling your property at {property_address}, now could be an excellent time to explore your options.

Would you like me to prepare a personalized market analysis for your specific property?

Best regards,
{sender_name}"""
            }
        }
        
        selected_template = st.selectbox("Select Template to Edit", list(templates.keys()))
        
        if selected_template:
            template = templates[selected_template]
            
            edited_subject = st.text_input("Subject Line", value=template["subject"])
            edited_content = st.text_area("Content", value=template["content"], height=300)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Save Template", use_container_width=True):
                    st.success("Template saved successfully!")
            
            with col2:
                if st.button("Create New Template", use_container_width=True):
                    st.info("New template creation interface opened!")

# Enhanced Contracts & LOI Page
def render_enhanced_contracts():
    """Enhanced contracts and LOI generation with full automation"""
    st.markdown('<h1 class="main-header">📄 Contracts & LOI Generator</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Generate LOI", "📋 Create Contract", "📁 Document Library", "🔄 E-Signature"])
    
    with tab1:
        render_loi_generator()
    
    with tab2:
        render_contract_generator()
    
    with tab3:
        render_document_library()
    
    with tab4:
        render_esignature_manager()

def render_loi_generator():
    """Letter of Intent generator"""
    st.markdown("### 📝 Letter of Intent Generator")
    
    # Check if we have property data from analyzer
    if 'generate_loi_data' in st.session_state:
        property_data = st.session_state.generate_loi_data
        offer_price = st.session_state.get('loi_offer_price', 0)
        
        st.success(f"Property data loaded: {property_data['address']}")
        st.info(f"Suggested offer price: ${offer_price:,.0f}")
    
    with st.form("loi_generator_form"):
        st.markdown("#### Property & Seller Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_address = st.text_input("Property Address*", 
                value=st.session_state.get('generate_loi_data', {}).get('address', ''))
            seller_name = st.text_input("Seller Name*")
            seller_phone = st.text_input("Seller Phone")
            seller_email = st.text_input("Seller Email")
        
        with col2:
            offer_price = st.number_input("Offer Price ($)*", 
                min_value=0, 
                value=st.session_state.get('loi_offer_price', 200000))
            earnest_money = st.number_input("Earnest Money ($)", min_value=0, value=1000)
            closing_timeframe = st.selectbox("Closing Timeframe", 
                ["7 days", "14 days", "21 days", "30 days", "45 days"])
            inspection_period = st.selectbox("Inspection Period", 
                ["3 days", "5 days", "7 days", "10 days", "14 days"])
        
        st.markdown("#### Buyer Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            buyer_name = st.text_input("Buyer Name*", value="WTF Investments LLC")
            buyer_phone = st.text_input("Buyer Phone*", value="(555) 123-4567")
            buyer_email = st.text_input("Buyer Email*", value="offers@wtfinvestments.com")
        
        with col4:
            buyer_qualification = st.text_area("Buyer Qualifications", 
                value="Cash buyer with proof of funds available upon request")
        
        st.markdown("#### Additional Terms")
        
        col5, col6 = st.columns(2)
        
        with col5:
            as_is_condition = st.checkbox("Property sold AS-IS", value=True)
            cash_purchase = st.checkbox("Cash purchase (no financing)", value=True)
            quick_closing = st.checkbox("Quick closing capability", value=True)
        
        with col6:
            no_realtor_fees = st.checkbox("No realtor commissions", value=True)
            flexible_timeline = st.checkbox("Flexible on timeline", value=True)
            
        additional_terms = st.text_area("Additional Terms", 
            placeholder="Any special conditions or terms...")
        
        # LOI Style
        loi_style = st.selectbox("LOI Style", 
            ["Professional", "Personal", "Urgent", "Friendly"])
        
        if st.form_submit_button("📝 Generate LOI", type="primary"):
            if property_address and seller_name and buyer_name and offer_price:
                
                loi_data = {
                    'property_address': property_address,
                    'seller_name': seller_name,
                    'seller_phone': seller_phone,
                    'seller_email': seller_email,
                    'offer_price': offer_price,
                    'earnest_money': earnest_money,
                    'closing_timeframe': closing_timeframe,
                    'inspection_period': inspection_period,
                    'buyer_name': buyer_name,
                    'buyer_phone': buyer_phone,
                    'buyer_email': buyer_email,
                    'buyer_qualification': buyer_qualification,
                    'additional_terms': additional_terms,
                    'loi_id': str(uuid.uuid4())[:8]
                }
                
                # Generate LOI
                loi_content = services['contract_generator'].generate_loi(loi_data)
                
                st.markdown("### 📄 Generated Letter of Intent")
                
                st.markdown(f"""
                <div class='loi-preview'>
                    <pre>{loi_content}</pre>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📥 Download PDF", use_container_width=True):
                        st.success("LOI PDF generated and downloaded!")
                
                with col2:
                    if st.button("📧 Email to Seller", use_container_width=True):
                        if seller_email:
                            st.success(f"LOI sent to {seller_email}")
                        else:
                            st.error("Seller email required")
                
                with col3:
                    if st.button("💾 Save to Library", use_container_width=True):
                        st.success("LOI saved to document library!")
                
                with col4:
                    if st.button("🔄 Edit & Regenerate", use_container_width=True):
                        st.info("Scroll up to edit and regenerate")
                
            else:
                st.error("Please fill in all required fields")

def render_contract_generator():
    """Enhanced contract generator"""
    st.markdown("### 📋 Contract Generator")
    
    contract_type = st.selectbox("Contract Type", 
        ["Purchase Agreement", "Assignment Contract", "Wholesale Agreement", 
         "Subject To Agreement", "Seller Finance Contract", "Lease Option"])
    
    if contract_type == "Purchase Agreement":
        render_purchase_agreement_form()
    elif contract_type == "Assignment Contract":
        render_assignment_contract_form()
    else:
        st.info(f"Contract generator for {contract_type} coming soon!")

def render_purchase_agreement_form():
    """Purchase agreement form"""
    with st.form("purchase_agreement_form"):
        st.markdown("#### Property Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_address = st.text_input("Property Address*")
            city = st.text_input("City*")
            state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA"])
            zip_code = st.text_input("ZIP Code*")
        
        with col2:
            purchase_price = st.number_input("Purchase Price ($)*", min_value=0, value=200000)
            earnest_money = st.number_input("Earnest Money ($)", min_value=0, value=1000)
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
            closing_costs = st.selectbox("Closing Costs Paid By", 
                ["Buyer", "Seller", "Split 50/50"])
            title_company = st.text_input("Title Company")
            contingencies = st.multiselect("Contingencies", 
                ["Financing", "Inspection", "Appraisal", "Sale of Buyer's Property"])
        
        with col8:
            financing_type = st.selectbox("Financing Type", 
                ["Cash", "Conventional", "FHA", "VA", "Hard Money", "Private"])
            
            if financing_type != "Cash":
                financing_amount = st.number_input("Loan Amount ($)", min_value=0)
                financing_contingency_days = st.number_input("Financing Contingency (days)", 
                    min_value=0, value=21)
        
        # Special terms
        special_terms = st.text_area("Special Terms and Conditions")
        
        if st.form_submit_button("📋 Generate Purchase Agreement", type="primary"):
            if property_address and buyer_name and seller_name and purchase_price:
                
                deal_data = {
                    'property_address': property_address,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'purchase_price': purchase_price,
                    'earnest_money': earnest_money,
                    'closing_date': closing_date.strftime('%B %d, %Y'),
                    'inspection_period': inspection_period,
                    'buyer_name': buyer_name,
                    'buyer_email': buyer_email,
                    'buyer_phone': buyer_phone,
                    'buyer_address': buyer_address,
                    'seller_name': seller_name,
                    'seller_email': seller_email,
                    'seller_phone': seller_phone,
                    'seller_address': seller_address,
                    'closing_costs_paid_by': closing_costs,
                    'title_company': title_company,
                    'special_terms': special_terms,
                    'contract_id': str(uuid.uuid4())[:8]
                }
                
                # Generate contract
                contract_content = services['contract_generator'].generate_purchase_agreement(deal_data)
                
                st.markdown("### 📋 Generated Purchase Agreement")
                
                st.markdown(f"""
                <div class='contract-preview'>
                    <pre>{contract_content}</pre>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📥 Download PDF", key="pa_download", use_container_width=True):
                        st.success("Contract PDF generated!")
                
                with col2:
                    if st.button("📧 Send to Parties", key="pa_send", use_container_width=True):
                        st.success("Contract sent to buyer and seller!")
                
                with col3:
                    if st.button("✍️ E-Signature", key="pa_esign", use_container_width=True):
                        st.success("E-signature request initiated!")
                
                with col4:
                    if st.button("💾 Save Contract", key="pa_save", use_container_width=True):
                        st.success("Contract saved to library!")
                
            else:
                st.error("Please fill in all required fields")

def render_assignment_contract_form():
    """Assignment contract form"""
    with st.form("assignment_contract_form"):
        st.markdown("#### Original Contract Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_address = st.text_input("Property Address*")
            original_purchase_price = st.number_input("Original Purchase Price ($)*", min_value=0)
            original_contract_date = st.date_input("Original Contract Date")
            seller_name = st.text_input("Seller Name*")
        
        with col2:
            assignment_fee = st.number_input("Assignment Fee ($)*", min_value=0, value=5000)
            closing_date = st.date_input("Expected Closing Date")
            title_company = st.text_input("Title Company")
        
        st.markdown("#### Assignor Information (Original Buyer)")
        
        col3, col4 = st.columns(2)
        
        with col3:
            assignor_name = st.text_input("Assignor Name*")
            assignor_address = st.text_area("Assignor Address")
        
        with col4:
            assignor_phone = st.text_input("Assignor Phone")
            assignor_email = st.text_input("Assignor Email")
        
        st.markdown("#### Assignee Information (New Buyer)")
        
        col5, col6 = st.columns(2)
        
        with col5:
            assignee_name = st.text_input("Assignee Name*")
            assignee_address = st.text_area("Assignee Address")
        
        with col6:
            assignee_phone = st.text_input("Assignee Phone")
            assignee_email = st.text_input("Assignee Email")
        
        # Assignment terms
        st.markdown("#### Assignment Terms")
        
        assignment_fee_payment = st.selectbox("Assignment Fee Payment", 
            ["At Closing", "Upon Execution", "50% Now / 50% at Closing"])
        
        special_conditions = st.text_area("Special Conditions")
        
        if st.form_submit_button("📋 Generate Assignment Contract", type="primary"):
            if (property_address and original_purchase_price and assignor_name 
                and assignee_name and assignment_fee):
                
                deal_data = {
                    'property_address': property_address,
                    'purchase_price': original_purchase_price,
                    'original_contract_date': original_contract_date.strftime('%B %d, %Y'),
                    'seller_name': seller_name,
                    'assignment_fee': assignment_fee,
                    'assignor_name': assignor_name,
                    'assignee_name': assignee_name,
                    'assignment_id': str(uuid.uuid4())[:8]
                }
                
                # Generate assignment contract
                contract_content = services['contract_generator'].generate_assignment_contract(deal_data)
                
                st.markdown("### 📋 Generated Assignment Contract")
                
                st.markdown(f"""
                <div class='contract-preview'>
                    <pre>{contract_content}</pre>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📥 Download PDF", key="ac_download", use_container_width=True):
                        st.success("Assignment contract PDF generated!")
                
                with col2:
                    if st.button("📧 Send to Parties", key="ac_send", use_container_width=True):
                        st.success("Contract sent to assignor and assignee!")
                
                with col3:
                    if st.button("✍️ E-Signature", key="ac_esign", use_container_width=True):
                        st.success("E-signature request initiated!")
                
                with col4:
                    if st.button("💾 Save Contract", key="ac_save", use_container_width=True):
                        st.success("Contract saved to library!")
                
            else:
                st.error("Please fill in all required fields")

def render_document_library():
    """Document library management"""
    st.markdown("### 📁 Document Library")
    
    # Document categories
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        doc_category = st.selectbox("Category", 
            ["All Documents", "LOIs", "Purchase Agreements", "Assignment Contracts", 
             "Templates", "Signed Contracts"])
    
    with col2:
        sort_by = st.selectbox("Sort By", 
            ["Date Created", "Document Type", "Status", "Property Address"])
    
    with col3:
        search_docs = st.text_input("🔍 Search Documents", 
            placeholder="Search by property, buyer, seller...")
    
    # Mock document data
    documents = [
        {
            'id': 'DOC001',
            'name': 'LOI - 123 Main St Dallas',
            'type': 'Letter of Intent',
            'property': '123 Main St, Dallas, TX',
            'status': 'Sent',
            'created': '2024-08-08',
            'size': '156 KB'
        },
        {
            'id': 'DOC002', 
            'name': 'Purchase Agreement - 456 Oak Ave',
            'type': 'Purchase Agreement',
            'property': '456 Oak Ave, Houston, TX',
            'status': 'Signed',
            'created': '2024-08-07',
            'size': '234 KB'
        },
        {
            'id': 'DOC003',
            'name': 'Assignment Contract - 789 Pine Rd',
            'type': 'Assignment Contract', 
            'property': '789 Pine Rd, Austin, TX',
            'status': 'Pending Signature',
            'created': '2024-08-06',
            'size': '198 KB'
        }
    ]
    
    # Display documents
    for doc in documents:
        status_colors = {
            'Draft': '#6B7280',
            'Sent': '#F59E0B', 
            'Pending Signature': '#8B5CF6',
            'Signed': '#10B981',
            'Expired': '#EF4444'
        }
        
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 2])
            
            with col1:
                st.write(f"**{doc['name']}**")
                st.caption(f"{doc['type']} • {doc['created']}")
            
            with col2:
                st.write(doc['property'])
            
            with col3:
                st.markdown(f"<span style='color: {status_colors.get(doc['status'], '#6B7280')};'>●</span> {doc['status']}", 
                           unsafe_allow_html=True)
            
            with col4:
                st.write(doc['size'])
            
            with col5:
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("👁️", key=f"view_{doc['id']}", help="View"):
                        st.info(f"Opening {doc['name']}")
                
                with col_b:
                    if st.button("📥", key=f"download_{doc['id']}", help="Download"):
                        st.success(f"Downloaded {doc['name']}")
                
                with col_c:
                    if st.button("📧", key=f"share_{doc['id']}", help="Share"):
                        st.success(f"Sharing {doc['name']}")
            
            st.markdown("---")

def render_esignature_manager():
    """E-signature management interface"""
    st.markdown("### ✍️ E-Signature Manager")
    
    # E-signature metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Pending Signatures", "12", delta="3 new")
    with col2:
        st.metric("Completed This Week", "8", delta="2")
    with col3:
        st.metric("Average Sign Time", "2.3 days", delta="-0.5 days")
    with col4:
        st.metric("Completion Rate", "94%", delta="1%")
    
    # Pending signatures
    st.markdown("#### Pending Signatures")
    
    pending_sigs = [
        {
            'document': 'Purchase Agreement - 123 Main St',
            'signers': ['John Smith (Buyer)', 'Mary Johnson (Seller)'],
            'sent_date': '2024-08-07',
            'due_date': '2024-08-14',
            'status': 'Waiting for Seller'
        },
        {
            'document': 'Assignment Contract - 456 Oak Ave',
            'signers': ['WTF Investments (Assignor)', 'Cash Buyer LLC (Assignee)'],
            'sent_date': '2024-08-06',
            'due_date': '2024-08-13', 
            'status': 'Waiting for Assignee'
        }
    ]
    
    for sig in pending_sigs:
        with st.expander(f"{sig['document']} - {sig['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Signers:** {', '.join(sig['signers'])}")
                st.write(f"**Sent:** {sig['sent_date']}")
                st.write(f"**Due:** {sig['due_date']}")
            
            with col2:
                st.write(f"**Status:** {sig['status']}")
                
                # Progress bar
                if sig['status'] == 'Waiting for Seller':
                    progress = 50
                elif sig['status'] == 'Waiting for Assignee':
                    progress = 50
                else:
                    progress = 0
                
                st.progress(progress)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📧 Send Reminder", key=f"remind_{sig['document']}", use_container_width=True):
                    st.success("Reminder sent!")
            
            with col2:
                if st.button("👁️ View Document", key=f"view_esig_{sig['document']}", use_container_width=True):
                    st.info("Opening document...")
            
            with col3:
                if st.button("🔄 Resend", key=f"resend_{sig['document']}", use_container_width=True):
                    st.success("Document resent!")
            
            with col4:
                if st.button("❌ Cancel", key=f"cancel_{sig['document']}", use_container_width=True):
                    st.warning("Signature request cancelled")
    
    # Send new e-signature request
    st.markdown("#### Send New E-Signature Request")
    
    with st.form("new_esignature_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            doc_to_sign = st.selectbox("Select Document", 
                ["LOI - 789 Pine Rd", "Purchase Agreement - 321 Elm St", "Assignment Contract - 654 Maple Dr"])
            
            signer1_name = st.text_input("Signer 1 Name*")
            signer1_email = st.text_input("Signer 1 Email*")
        
        with col2:
            due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=7))
            
            signer2_name = st.text_input("Signer 2 Name")
            signer2_email = st.text_input("Signer 2 Email")
        
        message = st.text_area("Message to Signers", 
            value="Please review and sign the attached document. Contact me if you have any questions.")
        
        if st.form_submit_button("📧 Send for E-Signature", type="primary"):
            if doc_to_sign and signer1_name and signer1_email:
                st.success(f"✅ E-signature request sent for {doc_to_sign}")
                st.info(f"📧 Sent to: {signer1_name} ({signer1_email})")
                if signer2_name and signer2_email:
                    st.info(f"📧 Also sent to: {signer2_name} ({signer2_email})")
            else:
                st.error("Please fill in required fields")

# Enhanced AI Assistant Page  
def render_enhanced_ai_assistant():
    """Enhanced AI assistant with full script generation"""
    st.markdown('<h1 class="main-header">🤖 AI Assistant Hub</h1>', unsafe_allow_html=True)
    
    # AI Assistant selector
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 ScriptMaster AI", key="scriptmaster_select", use_container_width=True):
            st.session_state.ai_type = "scriptmaster"
    
    with col2:
        if st.button("🏢 Underwriter GPT", key="underwriter_select", use_container_width=True):
            st.session_state.ai_type = "underwriter"
    
    with col3:
        if st.button("💬 General Assistant", key="general_select", use_container_width=True):
            st.session_state.ai_type = "general"
    
    # Set default AI type
    if 'ai_type' not in st.session_state:
        st.session_state.ai_type = "scriptmaster"
    
    # Display current AI assistant
    ai_descriptions = {
        "scriptmaster": {
            "title": "📞 ScriptMaster AI - Empire Script Generator",
            "description": "Generate complete 5x5 real estate scripts with 125 responses. Perfect for cold calling, objection handling, and closing techniques.",
            "color": "#8B5CF6"
        },
        "underwriter": {
            "title": "🏢 Underwriter GPT - Deal Analysis Expert", 
            "description": "Analyze properties, calculate returns, estimate rehab costs, and provide investment recommendations.",
            "color": "#10B981"
        },
        "general": {
            "title": "💬 General AI Assistant - Wholesaling Expert",
            "description": "Get help with any real estate wholesaling questions, strategies, and general guidance.",
            "color": "#F59E0B"
        }
    }
    
    current_ai = ai_descriptions[st.session_state.ai_type]
    
    st.markdown(f"""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 2rem; border-radius: 15px; border: 2px solid {current_ai["color"]}; margin: 1rem 0;'>
        <h3 style='color: {current_ai["color"]}; margin-bottom: 1rem;'>{current_ai["title"]}</h3>
        <p style='color: white; margin: 0;'>{current_ai["description"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ScriptMaster AI Interface
    if st.session_state.ai_type == "scriptmaster":
        render_scriptmaster_interface()
    
    # Underwriter GPT Interface
    elif st.session_state.ai_type == "underwriter":
        render_underwriter_interface()
    
    # General Assistant Interface
    else:
        render_general_assistant_interface()

def render_scriptmaster_interface():
    """ScriptMaster AI interface for complete script generation"""
    st.markdown("### 📞 ScriptMaster AI - Complete Script Generator")
    
    # Script type selection
    col1, col2 = st.columns(2)
    
    with col1:
        script_type = st.selectbox("Script Type", 
            ["Cold Calling", "Objection Handling", "Follow-up Sequence", 
             "Closing Techniques", "Appointment Setting", "Price Negotiation"])
    
    with col2:
        scenario = st.selectbox("Scenario", 
            ["Distressed Property", "Behind on Payments", "Divorce Situation", 
             "Job Relocation", "Inherited Property", "Tired Landlord", "General Motivated Seller"])
    
    # Deal type specification
    deal_type = st.selectbox("Deal Structure", 
        ["SubTo (Subject To)", "Seller Finance", "Wraparound Mortgage", 
         "Cash Offer", "Lease Option", "Hybrid Deal"])
    
    # Advanced options
    with st.expander("Advanced Script Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            caller_experience = st.selectbox("Caller Experience Level", 
                ["Beginner", "Intermediate", "Advanced"])
            script_tone = st.selectbox("Script Tone", 
                ["Professional", "Casual", "Aggressive", "Empathetic", "Urgent"])
        
        with col2:
            target_demographic = st.selectbox("Target Demographic", 
                ["General", "Seniors", "Young Professionals", "Investors", "First-time Sellers"])
            include_rebuttals = st.checkbox("Include Advanced Rebuttals", value=True)
    
    # Generate complete script
    if st.button("🎭 Generate Complete 5x5 Script", type="primary", use_container_width=True):
        with st.spinner("🤖 ScriptMaster AI is generating your complete 5x5 script..."):
            # Simulate script generation time
            import time
            time.sleep(3)
            
            # Generate full script using AI assistant
            script_prompt = f"Generate a complete {script_type} script for {scenario} with {deal_type} structure"
            full_script = services['ai_assistant'].generate_full_script(
                script_type.lower().replace(' ', '_'), 
                f"{scenario} - {deal_type}"
            )
            
            st.success("✅ Complete 5x5 Script Generated!")
            
            # Display the complete script
            st.markdown("### 📖 Your Complete 5x5 Script")
            
            with st.expander("📄 View Full Script (Click to expand)", expanded=True):
                st.markdown(f"""
                <div style='background: rgba(255, 255, 255, 0.95); color: black; padding: 2rem; 
                            border-radius: 10px; font-family: monospace; white-space: pre-wrap;'>
                {full_script}
                </div>
                """, unsafe_allow_html=True)
            
            # Script actions
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📥 Download Script", use_container_width=True):
                    st.success("Script downloaded as PDF!")
            
            with col2:
                if st.button("📧 Email Script", use_container_width=True):
                    st.success("Script emailed to your team!")
            
            with col3:
                if st.button("💾 Save to Library", use_container_width=True):
                    st.success("Script saved to script library!")
            
            with col4:
                if st.button("🎯 Practice Mode", use_container_width=True):
                    st.session_state.practice_script = full_script
                    st.success("Practice mode activated!")
    
    # Practice mode
    if 'practice_script' in st.session_state:
        st.markdown("---")
        st.markdown("### 🎯 Practice Mode")
        
        st.info("💡 Practice your script with AI feedback!")
        
        practice_response = st.text_area("Your response:", 
            placeholder="Practice your opening line here...")
        
        if st.button("🤖 Get AI Feedback"):
            if practice_response:
                feedback = """
                **AI Feedback on Your Response:**
                
                ✅ **Good Elements:**
                • Clear and confident tone
                • Good use of empathy
                
                🔧 **Areas for Improvement:**
                • Could be more specific about benefits
                • Add urgency to create action
                
                💡 **Suggested Improvement:**
                "Hi [Name], I know you weren't expecting my call, but I specialize in helping homeowners who need to sell quickly without repairs or realtor fees. Do you have just 30 seconds?"
                
                **Score: 7/10**
                """
                st.markdown(feedback)
            else:
                st.warning("Please enter a response to get feedback")

def render_underwriter_interface():
    """Underwriter GPT interface"""
    st.markdown("### 🏢 Underwriter GPT - Investment Analysis")
    
    # Quick analysis tools
    st.markdown("#### 🚀 Quick Analysis Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Property Analysis", use_container_width=True):
            st.session_state.underwriter_mode = "property_analysis"
    
    with col2:
        if st.button("💰 Deal Comparison", use_container_width=True):
            st.session_state.underwriter_mode = "deal_comparison"
    
    with col3:
        if st.button("📊 Market Analysis", use_container_width=True):
            st.session_state.underwriter_mode = "market_analysis"
    
    # Analysis mode
    mode = st.session_state.get('underwriter_mode', 'property_analysis')
    
    if mode == "property_analysis":
        st.markdown("#### 🏠 Property Analysis")
        
        with st.form("underwriter_analysis_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_input("Property Address")
                purchase_price = st.number_input("Purchase Price ($)", min_value=0, value=200000)
                rehab_cost = st.number_input("Estimated Rehab ($)", min_value=0, value=30000)
                arv = st.number_input("ARV ($)", min_value=0, value=280000)
            
            with col2:
                monthly_rent = st.number_input("Monthly Rent ($)", min_value=0, value=2000)
                hold_period = st.number_input("Hold Period (years)", min_value=1, value=5)
                strategy = st.selectbox("Strategy", ["Fix & Flip", "Buy & Hold", "BRRRR", "Wholesale"])
            
            if st.form_submit_button("🔍 Analyze Property"):
                with st.spinner("🤖 Underwriter GPT analyzing..."):
                    analysis_result = """
                    ## 📊 Underwriter GPT Analysis Results
                    
                    **Property:** {address}
                    **Strategy:** {strategy}
                    
                    ### 💰 Financial Metrics
                    - **Purchase Price:** ${purchase_price:,}
                    - **Rehab Cost:** ${rehab_cost:,}
                    - **Total Investment:** ${purchase_price + rehab_cost:,}
                    - **ARV:** ${arv:,}
                    - **Monthly Rent:** ${monthly_rent:,}
                    
                    ### 📈 Returns Analysis
                    - **Gross Yield:** {(monthly_rent * 12 / (purchase_price + rehab_cost)) * 100:.2f}%
                    - **70% Rule Check:** {'✅ PASS' if purchase_price + rehab_cost <= arv * 0.7 else '❌ FAIL'}
                    - **Estimated ROI:** {((arv - purchase_price - rehab_cost) / (purchase_price + rehab_cost)) * 100:.1f}%
                    
                    ### 🎯 Recommendation
                    {'🟢 **STRONG BUY** - This deal meets all investment criteria!' if purchase_price + rehab_cost <= arv * 0.7 else '🟡 **PROCEED WITH CAUTION** - Margins are tight on this deal.' if purchase_price + rehab_cost <= arv * 0.8 else '🔴 **AVOID** - Deal does not meet minimum criteria.'}
                    
                    ### 📋 Next Steps
                    1. Verify ARV with recent comps
                    2. Get contractor bids for rehab
                    3. Confirm rental rates in area
                    4. Check for any liens or issues
                    """.format(
                        address=address if address else "Sample Property",
                        strategy=strategy,
                        purchase_price=purchase_price,
                        rehab_cost=rehab_cost,
                        arv=arv,
                        monthly_rent=monthly_rent
                    )
                    
                    st.markdown(analysis_result)
    
    elif mode == "deal_comparison":
        st.markdown("#### 💰 Deal Comparison Tool")
        st.info("Compare multiple investment opportunities side by side")
        
        # Deal comparison interface
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Deal A**")
            deal_a_price = st.number_input("Purchase Price A ($)", min_value=0, value=200000, key="deal_a_price")
            deal_a_rehab = st.number_input("Rehab Cost A ($)", min_value=0, value=30000, key="deal_a_rehab")
            deal_a_arv = st.number_input("ARV A ($)", min_value=0, value=280000, key="deal_a_arv")
        
        with col2:
            st.markdown("**Deal B**")
            deal_b_price = st.number_input("Purchase Price B ($)", min_value=0, value=180000, key="deal_b_price")
            deal_b_rehab = st.number_input("Rehab Cost B ($)", min_value=0, value=25000, key="deal_b_rehab")
            deal_b_arv = st.number_input("ARV B ($)", min_value=0, value=250000, key="deal_b_arv")
        
        if st.button("⚖️ Compare Deals"):
            # Calculate metrics for both deals
            deal_a_total = deal_a_price + deal_a_rehab
            deal_b_total = deal_b_price + deal_b_rehab
            
            deal_a_profit = deal_a_arv - deal_a_total
            deal_b_profit = deal_b_arv - deal_b_total
            
            deal_a_roi = (deal_a_profit / deal_a_total) * 100 if deal_a_total > 0 else 0
            deal_b_roi = (deal_b_profit / deal_b_total) * 100 if deal_b_total > 0 else 0
            
            # Display comparison
            comparison_df = pd.DataFrame({
                'Metric': ['Total Investment', 'Expected Profit', 'ROI', '70% Rule Check', 'Recommendation'],
                'Deal A': [f'${deal_a_total:,}', f'${deal_a_profit:,}', f'{deal_a_roi:.1f}%', 
                          '✅' if deal_a_total <= deal_a_arv * 0.7 else '❌',
                          '🏆 Winner' if deal_a_roi > deal_b_roi else '🥈 Second'],
                'Deal B': [f'${deal_b_total:,}', f'${deal_b_profit:,}', f'{deal_b_roi:.1f}%',
                          '✅' if deal_b_total <= deal_b_arv * 0.7 else '❌', 
                          '🏆 Winner' if deal_b_roi > deal_a_roi else '🥈 Second']
            })
            
            st.dataframe(comparison_df, use_container_width=True)
    
    else:  # market_analysis
        st.markdown("#### 📊 Market Analysis")
        st.info("Analyze market trends and opportunities")
        
        market_city = st.selectbox("Select Market", ["Dallas, TX", "Houston, TX", "Austin, TX", "San Antonio, TX"])
        
        if st.button("📈 Generate Market Report"):
            st.markdown(f"""
            ## 📊 Market Analysis Report - {market_city}
            
            ### 🏠 Housing Market Overview
            - **Median Home Price:** $285,000 (↑ 8.2% YoY)
            - **Average Days on Market:** 23 days (↓ 12% YoY)
            - **Inventory Levels:** 2.1 months supply (Low)
            - **Price per Sq Ft:** $142 (↑ 9.1% YoY)
            
            ### 💰 Investment Metrics
            - **Average Cap Rate:** 6.8%
            - **Rent Growth (YoY):** 5.2%
            - **Vacancy Rate:** 4.1%
            - **Property Tax Rate:** 2.1%
            
            ### 🎯 Investment Opportunities
            1. **Fix & Flip:** Strong demand, quick sales
            2. **Buy & Hold:** Solid rental yields
            3. **Wholesale:** Active investor market
            
            ### ⚠️ Market Risks
            - Rising interest rates affecting buyer demand
            - Construction costs increasing
            - Potential oversupply in luxury segment
            
            ### 📋 Recommendation
            🟢 **FAVORABLE** - Strong fundamentals support continued investment activity
            """)

def render_general_assistant_interface():
    """General AI assistant interface"""
    st.markdown("### 💬 General AI Assistant")
    
    # Initialize chat messages
    if 'general_ai_messages' not in st.session_state:
        st.session_state.general_ai_messages = [
            {"role": "assistant", "content": "Hi! I'm your General AI Assistant for real estate wholesaling. I can help you with strategies, calculations, market insights, and answer any questions about the business. What would you like to know?"}
        ]
    
    # Quick action buttons
    st.markdown("#### 🚀 Quick Actions")
    
    quick_actions = [
        "Explain the 70% rule",
        "How to find motivated sellers",
        "Best contract assignment strategies", 
        "Marketing to cash buyers",
        "Calculate wholesale fees",
        "Due diligence checklist"
    ]
    
    cols = st.columns(3)
    for i, action in enumerate(quick_actions):
        with cols[i % 3]:
            if st.button(action, key=f"quick_{i}", use_container_width=True):
                st.session_state.general_ai_input = action
    
    # Display chat history
    for message in st.session_state.general_ai_messages:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.write(message['content'])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about real estate wholesaling...")
    
    # Handle quick action input
    if 'general_ai_input' in st.session_state:
        user_input = st.session_state.general_ai_input
        del st.session_state.general_ai_input
    
    if user_input:
        # Add user message
        st.session_state.general_ai_messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("🤖 AI Assistant thinking..."):
            response = services['ai_assistant'].get_response(user_input, "general")
        
        # Add AI response
        st.session_state.general_ai_messages.append({"role": "assistant", "content": response})
        
        # Rerun to display new messages
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.general_ai_messages = [
            {"role": "assistant", "content": "Hi! I'm your General AI Assistant for real estate wholesaling. I can help you with strategies, calculations, market insights, and answer any questions about the business. What would you like to know?"}
        ]
        st.rerun()

# Admin Dashboard
def render_admin_dashboard():
    """Admin dashboard with platform overview"""
    st.markdown('<h1 class="main-header">🔧 Admin Dashboard</h1>', unsafe_allow_html=True)
    
    # Admin warning
    st.markdown("""
    <div class='admin-panel'>
        <h3 style='color: white; margin: 0; text-align: center;'>⚠️ ADMINISTRATOR ACCESS ⚠️</h3>
        <p style='color: white; margin: 0.5rem 0; text-align: center;'>You have full platform access and control</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Platform metrics
    st.markdown("## 📊 Platform Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Users", "5,247", delta="89 this week")
    with col2:
        st.metric("Active Deals", "1,892", delta="156 new")
    with col3:
        st.metric("Revenue (Month)", "$47.2K", delta="$8.3K")
    with col4:
        st.metric("Support Tickets", "23", delta="-12")
    with col5:
        st.metric("System Health", "98.7%", delta="0.2%")
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 User Growth")
        
        growth_data = pd.DataFrame({
            'Date': pd.date_range('2024-07-01', periods=30, freq='D'),
            'New Users': np.random.poisson(8, 30),
            'Active Users': np.random.poisson(150, 30) + 1000
        })
        
        fig_growth = px.line(growth_data, x='Date', y=['New Users', 'Active Users'],
                           title='User Activity Trend')
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Revenue Breakdown")
        
        revenue_data = pd.DataFrame({
            'Plan': ['Starter ($97)', 'Professional ($297)', 'Enterprise ($997)'],
            'Users': [2156, 2834, 257],
            'Revenue': [209132, 841698, 256229]
        })
        
        fig_revenue = px.pie(revenue_data, values='Revenue', names='Plan',
                           title='Revenue by Plan')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # System alerts
    st.markdown("### 🚨 System Alerts")
    
    alerts = [
        {"type": "info", "message": "Database backup completed successfully", "time": "5 minutes ago"},
        {"type": "warning", "message": "API rate limit reached for Lightning Leads service", "time": "1 hour ago"},
        {"type": "success", "message": "New feature deployed: Enhanced AI scripts", "time": "2 hours ago"},
        {"type": "error", "message": "Email service temporary outage (resolved)", "time": "6 hours ago"}
    ]
    
    for alert in alerts:
        alert_colors = {
            "info": "#3B82F6",
            "warning": "#F59E0B", 
            "success": "#10B981",
            "error": "#EF4444"
        }
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-left: 4px solid {alert_colors[alert["type"]]}; margin: 0.5rem 0;'>
            <strong>{alert["message"]}</strong><br>
            <small style='color: #9CA3AF;'>{alert["time"]}</small>
        </div>
        """, unsafe_allow_html=True)

# Main application routing
def main():
    """Main application router"""
    # Show landing page if not authenticated
    if not st.session_state.authenticated or st.session_state.show_landing:
        render_landing_page()
        return
    
    # Render sidebar and get selected page
    selected_page = render_enhanced_sidebar()
    
    # Route to appropriate page based on user role and selection
    user_role = st.session_state.user_data.get('role', 'wholesaler')
    
    try:
        if user_role == 'admin':
            # Admin routes
            if selected_page == "admin_dashboard":
                render_admin_dashboard()
            elif selected_page == "user_management":
                st.markdown('<h1 class="main-header">👥 User Management</h1>', unsafe_allow_html=True)
                st.info("User management interface coming soon!")
            elif selected_page == "platform_analytics":
                render_analytics_page()
            elif selected_page == "revenue_dashboard":
                st.markdown('<h1 class="main-header">💰 Revenue Dashboard</h1>', unsafe_allow_html=True)
                st.info("Revenue dashboard coming soon!")
            elif selected_page == "system_settings":
                st.markdown('<h1 class="main-header">⚙️ System Settings</h1>', unsafe_allow_html=True)
                st.info("System settings coming soon!")
            elif selected_page == "master_dispo":
                st.markdown('<h1 class="main-header">📋 Master Dispo System</h1>', unsafe_allow_html=True)
                st.info("Master disposition system coming soon!")
            elif selected_page == "ai_management":
                st.markdown('<h1 class="main-header">🤖 AI Management</h1>', unsafe_allow_html=True)
                st.info("AI management interface coming soon!")
        
        elif user_role == 'wholesaler':
            # Wholesaler routes
            if selected_page == "dashboard":
                render_dashboard()
            elif selected_page == "deal_analyzer":
                render_deal_analyzer()
            elif selected_page == "buyers":
                render_buyers_page()
            elif selected_page == "leads":
                render_enhanced_leads()
            elif selected_page == "pipeline":
                render_pipeline_page()
            elif selected_page == "contracts":
                render_enhanced_contracts()
            elif selected_page == "lightning_leads":
                render_lightning_leads()
            elif selected_page == "ai_assistant":
                render_enhanced_ai_assistant()
            elif selected_page == "analytics":
                render_analytics_page()
        
        else:  # buyer
            # Buyer routes
            if selected_page == "buyer_dashboard":
                st.markdown('<h1 class="main-header">🏠 Buyer Dashboard</h1>', unsafe_allow_html=True)
                st.info("Buyer dashboard coming soon!")
            elif selected_page == "available_deals":
                st.markdown('<h1 class="main-header">🔍 Available Deals</h1>', unsafe_allow_html=True)
                st.info("Available deals interface coming soon!")
            elif selected_page == "my_offers":
                st.markdown('<h1 class="main-header">📋 My Offers</h1>', unsafe_allow_html=True)
                st.info("Offers management coming soon!")
            elif selected_page == "market_analysis":
                st.markdown('<h1 class="main-header">📊 Market Analysis</h1>', unsafe_allow_html=True)
                st.info("Market analysis coming soon!")
            elif selected_page == "buyer_preferences":
                st.markdown('<h1 class="main-header">⚙️ Buyer Preferences</h1>', unsafe_allow_html=True)
                st.info("Preferences settings coming soon!")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact support.")

# Additional helper functions that were referenced but not fully implemented

def get_connection():
    """Get database connection"""
    return services['db'].get_connection()

def render_dashboard():
    """Original dashboard render function"""
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
    
    # Quick property analyzer
    st.markdown("## 🔍 Quick Property Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        quick_address = st.text_input("Enter property address for instant analysis",
                                    placeholder="123 Main St, City, State")
    
    with col2:
        if st.button("⚡ Analyze", type="primary", use_container_width=True):
            if quick_address:
                with st.spinner("Analyzing..."):
                    st.session_state.quick_analysis_address = quick_address
                    st.success("Analysis complete! Check Deal Analyzer page for full results.")

def render_buyers_page():
    """Original buyers page render function"""
    st.markdown('<h1 class="main-header">👥 Buyer Network</h1>', unsafe_allow_html=True)
    
    # Buyer metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Buyers", "2,341", delta="47 this month")
    with col2:
        st.metric("Verified Buyers", "1,892", delta="23 this month")  
    with col3:
        st.metric("Active This Month", "1,456", delta="12%")
    with col4:
        st.metric("Avg Deal Size", "$185K", delta="$15K")
    
    st.info("Enhanced buyer management available in the sidebar navigation!")

def render_pipeline_page():
    """Original pipeline page render function"""
    st.markdown('<h1 class="main-header">📋 Deal Pipeline</h1>', unsafe_allow_html=True)
    
    # Pipeline metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipeline", "$487K", delta="$23K")
    with col2:
        st.metric("Active Deals", "47", delta="3")
    with col3:
        st.metric("This Month Closed", "$127K", delta="$23K") 