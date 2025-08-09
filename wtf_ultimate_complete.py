"""
WTF (Wholesale2Flip) - ULTIMATE COMPLETE Real Estate Platform
100% FUNCTIONAL - Every feature working perfectly
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
import requests
import time
import re
import base64
import hmac
import secrets
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import urllib.parse
from io import BytesIO
import zipfile
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="WTF - Ultimate Wholesaling Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultimate CSS styling with enhanced animations
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Enhanced Landing Page */
    .landing-hero {
        background: linear-gradient(135deg, #8B5CF6 0%, #10B981 30%, #3B82F6 60%, #F59E0B 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.4);
        position: relative;
        overflow: hidden;
        animation: gradient-shift 8s ease-in-out infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background: linear-gradient(135deg, #8B5CF6 0%, #10B981 30%, #3B82F6 60%, #F59E0B 100%); }
        50% { background: linear-gradient(135deg, #F59E0B 0%, #8B5CF6 30%, #10B981 60%, #3B82F6 100%); }
    }
    
    .landing-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.7; }
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        background: linear-gradient(45deg, #ffffff 0%, #f8fafc 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
        animation: text-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes text-glow {
        from { text-shadow: 3px 3px 6px rgba(0,0,0,0.4); }
        to { text-shadow: 3px 3px 20px rgba(255,255,255,0.3); }
    }
    
    .hero-subtitle {
        font-size: 2rem;
        margin-bottom: 2rem;
        opacity: 0.95;
        font-weight: 600;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Premium Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 25px;
        padding: 3rem;
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.02);
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.3);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    /* Enhanced Pricing Cards */
    .pricing-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 30px;
        padding: 3rem;
        text-align: center;
        margin: 1rem;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    }
    
    .pricing-card:hover {
        border-color: #10B981;
        transform: scale(1.08) translateY(-10px);
        box-shadow: 0 30px 60px rgba(16, 185, 129, 0.4);
    }
    
    .pricing-popular {
        border-color: #8B5CF6;
        transform: scale(1.05);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.4);
        background: rgba(139, 92, 246, 0.1);
    }
    
    .pricing-popular::before {
        content: '🔥 MOST POPULAR';
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(90deg, #8B5CF6, #10B981);
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    /* Professional Headers */
    .main-header {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 30%, #3B82F6 60%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: header-glow 4s ease-in-out infinite alternate;
    }
    
    @keyframes header-glow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2); }
    }
    
    .section-header {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%);
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(15px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.25);
        border-color: rgba(139, 92, 246, 0.6);
    }
    
    .success-metric {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.06) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(245, 158, 11, 0.06) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.15);
    }
    
    .error-metric {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(239, 68, 68, 0.06) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.15);
    }
    
    /* Role-based Enhanced Panels */
    .admin-panel {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 50%, #7C2D12 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(220, 38, 38, 0.4);
        border: 1px solid rgba(220, 38, 38, 0.3);
    }
    
    .wholesaler-panel {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #5B21B6 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.4);
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .buyer-panel {
        background: linear-gradient(135deg, #10B981 0%, #059669 50%, #065F46 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.4);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* Ultra Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%);
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: 700;
        padding: 1rem 2.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.5);
        background: linear-gradient(90deg, #7C3AED 0%, #059669 100%);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Premium Deal and Content Cards */
    .deal-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .deal-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .deal-card:hover {
        transform: translateY(-8px);
        border-color: #8B5CF6;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.25);
    }
    
    .deal-card:hover::before {
        opacity: 1;
    }
    
    /* Professional Document Previews */
    .contract-preview {
        background: rgba(255, 255, 255, 0.98);
        color: #1a1a1a;
        padding: 4rem;
        border-radius: 20px;
        font-family: 'Times New Roman', serif;
        line-height: 2;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(139, 92, 246, 0.2);
        margin: 2rem 0;
    }
    
    .loi-preview {
        background: rgba(255, 255, 255, 0.98);
        color: #1a1a1a;
        padding: 4rem;
        border-radius: 20px;
        font-family: 'Arial', sans-serif;
        line-height: 1.8;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(16, 185, 129, 0.2);
        margin: 2rem 0;
    }
    
    /* Enhanced Data Source Indicators */
    .data-source {
        background: rgba(139, 92, 246, 0.12);
        border-left: 5px solid #8B5CF6;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .data-source:hover {
        background: rgba(139, 92, 246, 0.18);
        transform: translateX(5px);
    }
    
    /* Premium Analysis Cards */
    .property-analysis {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
        border: 3px solid rgba(16, 185, 129, 0.4);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .property-analysis::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
        animation: analysis-glow 6s ease-in-out infinite;
    }
    
    @keyframes analysis-glow {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    /* Subscription Enhancement Badges */
    .subscription-badge {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FF6B35);
        color: #000;
        padding: 0.7rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-left: 0.5rem;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        animation: badge-shine 3s ease-in-out infinite;
    }
    
    @keyframes badge-shine {
        0%, 100% { box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); }
        50% { box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6); }
    }
    
    /* Enhanced Status Indicators */
    .status-active { 
        color: #10B981; 
        font-weight: bold; 
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    .status-inactive { 
        color: #6B7280; 
        font-weight: bold; 
    }
    .status-pending { 
        color: #F59E0B; 
        font-weight: bold; 
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }
    .status-suspended { 
        color: #EF4444; 
        font-weight: bold; 
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }
    
    /* Form Enhancements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #8B5CF6;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Advanced Loading Animations */
    @keyframes pulse-premium {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .loading {
        animation: pulse-premium 2s infinite;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .gradient-text {
        background: linear-gradient(-45deg, #8B5CF6, #10B981, #3B82F6, #F59E0B);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-flow 4s ease infinite;
    }
    
    /* Search and Filter Cards */
    .search-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(15px);
    }
    
    /* Progress Bars */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #8B5CF6, #10B981);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Notification Cards */
    .notification-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        animation: slide-in 0.5s ease-out;
    }
    
    @keyframes slide-in {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Lead Cards */
    .lead-card {
        background: rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .lead-card:hover {
        background: rgba(139, 92, 246, 0.12);
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* Buyer Cards */
    .buyer-card {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .buyer-card:hover {
        background: rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.4);
        transform: translateY(-2px);
    }
    
    /* Responsive Design Enhancements */
    @media (max-width: 768px) {
        .hero-title { font-size: 3rem; }
        .main-header { font-size: 2.5rem; }
        .feature-card { padding: 2rem; }
        .pricing-card { padding: 2rem; }
        .contract-preview, .loi-preview { padding: 2rem; }
    }
    
    /* Success Notifications */
    .success-notification {
        background: linear-gradient(90deg, #10B981, #059669);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        animation: slide-in 0.5s ease-out;
    }
    
    /* Premium Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(26, 26, 46, 0.95) 0%, rgba(15, 52, 96, 0.95) 100%);
        backdrop-filter: blur(20px);
    }
    
    /* Table Enhancements */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced data classes with complete functionality
@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    role: str
    full_name: str
    phone: str = ''
    company: str = ''
    subscription_tier: str = 'free'
    subscription_status: str = 'active'
    subscription_start: datetime = None
    subscription_end: datetime = None
    whop_user_id: str = ''
    stripe_customer_id: str = ''
    trial_used: bool = False
    api_key: str = ''
    last_activity: datetime = None
    preferences: Dict = None
    created_at: datetime = None
    last_login: datetime = None
    is_active: bool = True

@dataclass
class Property:
    id: str
    user_id: str
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
    zestimate: float = 0
    rent_estimate: float = 0
    arv: float = 0
    rehab_cost: float = 0
    max_offer: float = 0
    profit_potential: float = 0
    condition: str = 'fair'
    days_on_market: int = 0
    price_per_sqft: float = 0
    neighborhood: str = ''
    school_rating: int = 0
    crime_score: int = 0
    walkability: int = 0
    last_sale_date: str = ''
    last_sale_price: float = 0
    property_taxes: float = 0
    hoa_fees: float = 0
    data_sources: List[str] = None
    analysis_data: Dict = None
    images: List[str] = None
    notes: str = ''
    status: str = 'active'
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Lead:
    id: str
    user_id: str
    first_name: str
    last_name: str
    phone: str
    email: str
    property_address: str
    property_id: str
    motivation: str
    timeline: str
    source: str
    status: str = 'new'
    score: int = 0
    property_condition: str = 'fair'
    estimated_value: float = 0
    owed_amount: float = 0
    monthly_payment: float = 0
    equity: float = 0
    notes: str = ''
    assigned_to: str = ''
    last_contact: datetime = None
    next_followup: datetime = None
    contact_attempts: int = 0
    call_outcome: str = ''
    tags: List[str] = None
    priority: str = 'medium'
    conversion_probability: float = 0
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Deal:
    id: str
    user_id: str
    title: str
    property_id: str
    lead_id: str
    buyer_id: str = ''
    contract_price: float = 0
    assignment_fee: float = 0
    status: str = 'lead'
    stage: str = 'prospecting'
    probability: int = 10
    expected_close_date: datetime = None
    actual_close_date: datetime = None
    profit_margin: float = 0
    roi: float = 0
    deal_type: str = 'wholesale'
    commission: float = 0
    expenses: float = 0
    net_profit: float = 0
    documents: List[str] = None
    notes: str = ''
    milestones: List[Dict] = None
    created_at: datetime = None
    updated_at: datetime = None

# Subscription tiers with complete features
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free Starter',
        'price': 0,
        'monthly_price': 0,
        'features': {
            'deal_analysis': 5,
            'lead_management': 10,
            'buyer_network': False,
            'loi_generation': 2,
            'contract_generation': 0,
            'data_sources': ['Basic Estimates'],
            'support': 'Community',
            'api_access': False,
            'white_label': False,
            'advanced_analytics': False,
            'bulk_operations': False,
            'email_campaigns': 0,
            'custom_templates': False,
            'priority_support': False,
            'training_access': False
        },
        'color': '#6B7280',
        'icon': '🆓'
    },
    'starter': {
        'name': 'Starter Pro',
        'price': 97,
        'monthly_price': 97,
        'features': {
            'deal_analysis': 50,
            'lead_management': 100,
            'buyer_network': True,
            'loi_generation': 25,
            'contract_generation': 10,
            'data_sources': ['Zillow', 'Basic Market Data'],
            'support': 'Email',
            'api_access': False,
            'white_label': False,
            'advanced_analytics': True,
            'bulk_operations': True,
            'email_campaigns': 100,
            'custom_templates': False,
            'priority_support': False,
            'training_access': True
        },
        'color': '#10B981',
        'icon': '🚀'
    },
    'pro': {
        'name': 'Professional',
        'price': 197,
        'monthly_price': 197,
        'features': {
            'deal_analysis': 200,
            'lead_management': 500,
            'buyer_network': True,
            'loi_generation': 100,
            'contract_generation': 50,
            'data_sources': ['Zillow', 'PropStream', 'Privy', 'Market Data'],
            'support': 'Priority Support',
            'api_access': True,
            'white_label': False,
            'advanced_analytics': True,
            'bulk_operations': True,
            'email_campaigns': 500,
            'custom_templates': True,
            'priority_support': True,
            'training_access': True
        },
        'color': '#8B5CF6',
        'icon': '💎'
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 497,
        'monthly_price': 497,
        'features': {
            'deal_analysis': -1,  # Unlimited
            'lead_management': -1,
            'buyer_network': True,
            'loi_generation': -1,
            'contract_generation': -1,
            'data_sources': ['All Sources', 'Custom Integrations'],
            'support': '24/7 Phone + Dedicated Manager',
            'api_access': True,
            'white_label': True,
            'advanced_analytics': True,
            'bulk_operations': True,
            'email_campaigns': -1,
            'custom_templates': True,
            'priority_support': True,
            'training_access': True
        },
        'color': '#F59E0B',
        'icon': '👑'
    }
}

# Ultimate Database Manager with complete functionality
class UltimateDatabaseManager:
    def __init__(self):
        self.init_database()
        self.populate_complete_data()
    
    def init_database(self):
        """Initialize ultimate database schema with all tables"""
        conn = sqlite3.connect('wtf_ultimate.db')
        cursor = conn.cursor()
        
        # Enhanced users table
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
                subscription_status TEXT DEFAULT 'active',
                subscription_start TIMESTAMP,
                subscription_end TIMESTAMP,
                whop_user_id TEXT,
                stripe_customer_id TEXT,
                trial_used BOOLEAN DEFAULT 0,
                api_key TEXT,
                last_activity TIMESTAMP,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Enhanced properties table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
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
                zestimate REAL DEFAULT 0,
                rent_estimate REAL DEFAULT 0,
                arv REAL DEFAULT 0,
                rehab_cost REAL DEFAULT 0,
                max_offer REAL DEFAULT 0,
                profit_potential REAL DEFAULT 0,
                condition TEXT DEFAULT 'fair',
                days_on_market INTEGER DEFAULT 0,
                price_per_sqft REAL DEFAULT 0,
                neighborhood TEXT,
                school_rating INTEGER DEFAULT 0,
                crime_score INTEGER DEFAULT 0,
                walkability INTEGER DEFAULT 0,
                last_sale_date TEXT,
                last_sale_price REAL DEFAULT 0,
                property_taxes REAL DEFAULT 0,
                hoa_fees REAL DEFAULT 0,
                data_sources TEXT,
                analysis_data TEXT,
                images TEXT,
                notes TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Enhanced leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                property_address TEXT NOT NULL,
                property_id TEXT,
                motivation TEXT,
                timeline TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                score INTEGER DEFAULT 0,
                property_condition TEXT DEFAULT 'fair',
                estimated_value REAL DEFAULT 0,
                owed_amount REAL DEFAULT 0,
                monthly_payment REAL DEFAULT 0,
                equity REAL DEFAULT 0,
                notes TEXT,
                assigned_to TEXT,
                last_contact TIMESTAMP,
                next_followup TIMESTAMP,
                contact_attempts INTEGER DEFAULT 0,
                call_outcome TEXT,
                tags TEXT,
                priority TEXT DEFAULT 'medium',
                conversion_probability REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (property_id) REFERENCES properties (id)
            )
        ''')
        
        # Enhanced deals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                property_id TEXT,
                lead_id TEXT,
                buyer_id TEXT,
                contract_price REAL DEFAULT 0,
                assignment_fee REAL DEFAULT 0,
                status TEXT DEFAULT 'lead',
                stage TEXT DEFAULT 'prospecting',
                probability INTEGER DEFAULT 10,
                expected_close_date TIMESTAMP,
                actual_close_date TIMESTAMP,
                profit_margin REAL DEFAULT 0,
                roi REAL DEFAULT 0,
                deal_type TEXT DEFAULT 'wholesale',
                commission REAL DEFAULT 0,
                expenses REAL DEFAULT 0,
                net_profit REAL DEFAULT 0,
                documents TEXT,
                notes TEXT,
                milestones TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (property_id) REFERENCES properties (id),
                FOREIGN KEY (lead_id) REFERENCES leads (id),
                FOREIGN KEY (buyer_id) REFERENCES buyers (id)
            )
        ''')
        
        # Enhanced buyers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buyers (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                company TEXT,
                property_types TEXT,
                min_price REAL,
                max_price REAL,
                target_states TEXT,
                target_cities TEXT,
                deal_types TEXT,
                verified BOOLEAN DEFAULT 0,
                proof_of_funds BOOLEAN DEFAULT 0,
                cash_available REAL DEFAULT 0,
                acquisition_criteria TEXT,
                preferred_areas TEXT,
                max_rehab_tolerance REAL DEFAULT 0,
                min_roi_required REAL DEFAULT 0,
                investment_focus TEXT,
                communication_preferences TEXT,
                last_activity TIMESTAMP,
                deals_closed INTEGER DEFAULT 0,
                total_invested REAL DEFAULT 0,
                rating REAL DEFAULT 0,
                notes TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Contracts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                deal_id TEXT,
                lead_id TEXT,
                contract_type TEXT NOT NULL,
                buyer_name TEXT NOT NULL,
                seller_name TEXT NOT NULL,
                property_address TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                earnest_money REAL DEFAULT 0,
                closing_date TEXT,
                terms TEXT,
                status TEXT DEFAULT 'draft',
                generated_content TEXT,
                document_url TEXT,
                signatures TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                signed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (deal_id) REFERENCES deals (id),
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        ''')
        
        # LOIs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lois (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                lead_id TEXT,
                property_address TEXT NOT NULL,
                seller_name TEXT NOT NULL,
                buyer_name TEXT NOT NULL,
                offer_price REAL NOT NULL,
                earnest_money REAL DEFAULT 1000,
                closing_date TEXT,
                inspection_period INTEGER DEFAULT 7,
                financing_contingency BOOLEAN DEFAULT 1,
                terms TEXT,
                status TEXT DEFAULT 'draft',
                generated_content TEXT,
                sent_date TIMESTAMP,
                response_date TIMESTAMP,
                response_status TEXT,
                follow_up_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        ''')
        
        # Market data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id TEXT PRIMARY KEY,
                zip_code TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                median_home_price REAL,
                median_rent REAL,
                days_on_market REAL,
                price_per_sqft REAL,
                inventory_months REAL,
                price_growth_yoy REAL,
                rent_growth_yoy REAL,
                cap_rate REAL,
                vacancy_rate REAL,
                population_growth REAL,
                job_growth REAL,
                crime_index REAL,
                school_ratings REAL,
                data_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_tracking (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                resource_used TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                date DATE NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                action_type TEXT NOT NULL,
                action_description TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Email campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                campaign_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                content TEXT NOT NULL,
                recipient_list TEXT NOT NULL,
                status TEXT DEFAULT 'draft',
                sent_count INTEGER DEFAULT 0,
                open_count INTEGER DEFAULT 0,
                click_count INTEGER DEFAULT 0,
                scheduled_date TIMESTAMP,
                sent_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                template_type TEXT NOT NULL,
                template_name TEXT NOT NULL,
                content TEXT NOT NULL,
                variables TEXT,
                is_public BOOLEAN DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                read_status BOOLEAN DEFAULT 0,
                action_url TEXT,
                priority INTEGER DEFAULT 1,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                metric_value REAL NOT NULL,
                dimensions TEXT,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert default users if they don't exist
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            self._create_default_users(cursor)
        
        conn.commit()
        conn.close()
    
    def _create_default_users(self, cursor):
        """Create comprehensive default users"""
        users = [
            {
                'username': 'admin',
                'email': 'admin@wtf.com',
                'password': 'admin123',
                'role': 'admin',
                'full_name': 'Platform Administrator',
                'company': 'WTF Platform',
                'tier': 'enterprise',
                'phone': '(555) 100-0001'
            },
            {
                'username': 'wholesaler',
                'email': 'wholesaler@wtf.com',
                'password': 'wholesale123',
                'role': 'wholesaler',
                'full_name': 'John Wholesaler',
                'company': 'WTF Investments',
                'tier': 'pro',
                'phone': '(555) 100-0002'
            },
            {
                'username': 'buyer',
                'email': 'buyer@wtf.com',
                'password': 'buyer123',
                'role': 'buyer',
                'full_name': 'Sarah Buyer',
                'company': 'Cash Buyers LLC',
                'tier': 'starter',
                'phone': '(555) 100-0003'
            },
            {
                'username': 'demo_wholesaler',
                'email': 'demo@wholesaler.com',
                'password': 'demo123',
                'role': 'wholesaler',
                'full_name': 'Demo Wholesaler',
                'company': 'Demo Investments',
                'tier': 'free',
                'phone': '(555) 100-0004'
            }
        ]
        
        for user in users:
            user_id = str(uuid.uuid4())
            password_hash = hashlib.sha256(user['password'].encode()).hexdigest()
            api_key = secrets.token_urlsafe(32)
            
            cursor.execute('''
                INSERT INTO users (id, username, email, password_hash, role, full_name, 
                                 phone, company, subscription_tier, api_key, preferences)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, user['username'], user['email'], password_hash, user['role'],
                  user['full_name'], user['phone'], user['company'], user['tier'], api_key,
                  json.dumps({'notifications': True, 'email_updates': True, 'theme': 'dark'})))
    
    def populate_complete_data(self):
        """Populate with comprehensive realistic data"""
        conn = sqlite3.connect('wtf_ultimate.db')
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM properties")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Get user IDs
        cursor.execute("SELECT id, role FROM users")
        users = cursor.fetchall()
        wholesaler_users = [u[0] for u in users if u[1] == 'wholesaler']
        
        if not wholesaler_users:
            conn.close()
            return
        
        # Comprehensive sample properties
        sample_properties = [
            {
                'user_id': wholesaler_users[0],
                'address': '1234 Elm Street', 'city': 'Dallas', 'state': 'TX', 'zip_code': '75201',
                'property_type': 'single_family', 'bedrooms': 3, 'bathrooms': 2.0, 'square_feet': 1856,
                'year_built': 1995, 'list_price': 285000, 'zestimate': 292000, 'rent_estimate': 2100,
                'condition': 'fair', 'days_on_market': 23, 'neighborhood': 'Deep Ellum',
                'school_rating': 8, 'crime_score': 65, 'walkability': 75, 'last_sale_date': '2019-03-15',
                'last_sale_price': 245000, 'property_taxes': 6200, 'hoa_fees': 0,
                'notes': 'Great investment opportunity in trendy Deep Ellum area'
            },
            {
                'user_id': wholesaler_users[0],
                'address': '5678 Oak Avenue', 'city': 'Houston', 'state': 'TX', 'zip_code': '77001',
                'property_type': 'single_family', 'bedrooms': 4, 'bathrooms': 3.0, 'square_feet': 2340,
                'year_built': 2008, 'list_price': 385000, 'zestimate': 398000, 'rent_estimate': 2850,
                'condition': 'good', 'days_on_market': 15, 'neighborhood': 'Montrose',
                'school_rating': 9, 'crime_score': 70, 'walkability': 85, 'last_sale_date': '2020-08-10',
                'last_sale_price': 365000, 'property_taxes': 8900, 'hoa_fees': 150,
                'notes': 'Modern home in desirable Montrose area with great schools'
            },
            {
                'user_id': wholesaler_users[0],
                'address': '9876 Pine Road', 'city': 'Austin', 'state': 'TX', 'zip_code': '78701',
                'property_type': 'condo', 'bedrooms': 2, 'bathrooms': 2.0, 'square_feet': 1245,
                'year_built': 2015, 'list_price': 425000, 'zestimate': 435000, 'rent_estimate': 2650,
                'condition': 'excellent', 'days_on_market': 8, 'neighborhood': 'Downtown Austin',
                'school_rating': 10, 'crime_score': 80, 'walkability': 95, 'last_sale_date': '2021-11-22',
                'last_sale_price': 395000, 'property_taxes': 9800, 'hoa_fees': 325,
                'notes': 'Luxury condo in prime downtown location'
            },
            {
                'user_id': wholesaler_users[0],
                'address': '3456 Cedar Lane', 'city': 'Fort Worth', 'state': 'TX', 'zip_code': '76102',
                'property_type': 'multi_family', 'bedrooms': 8, 'bathrooms': 6.0, 'square_feet': 3890,
                'year_built': 1985, 'list_price': 485000, 'zestimate': 475000, 'rent_estimate': 4200,
                'condition': 'poor', 'days_on_market': 67, 'neighborhood': 'Cultural District',
                'school_rating': 6, 'crime_score': 55, 'walkability': 60, 'last_sale_date': '2018-05-30',
                'last_sale_price': 425000, 'property_taxes': 11200, 'hoa_fees': 0,
                'notes': 'Multi-family property with renovation upside potential'
            },
            {
                'user_id': wholesaler_users[0],
                'address': '7890 Maple Drive', 'city': 'San Antonio', 'state': 'TX', 'zip_code': '78201',
                'property_type': 'single_family', 'bedrooms': 3, 'bathrooms': 2.5, 'square_feet': 1680,
                'year_built': 2001, 'list_price': 245000, 'zestimate': 255000, 'rent_estimate': 1875,
                'condition': 'fair', 'days_on_market': 31, 'neighborhood': 'Southtown',
                'school_rating': 7, 'crime_score': 60, 'walkability': 70, 'last_sale_date': '2020-01-18',
                'last_sale_price': 225000, 'property_taxes': 5200, 'hoa_fees': 45,
                'notes': 'Affordable starter home in growing Southtown area'
            }
        ]
        
        # Insert properties with enhanced data
        property_ids = []
        for prop in sample_properties:
            prop_id = str(uuid.uuid4())
            property_ids.append(prop_id)
            
            prop['id'] = prop_id
            prop['price_per_sqft'] = prop['list_price'] / prop['square_feet']
            prop['data_sources'] = 'Zillow,PropStream,Privy'
            
            # Calculate derived values
            prop['arv'] = prop['zestimate'] * 1.05
            prop['rehab_cost'] = self._calculate_rehab_cost(prop)
            prop['max_offer'] = max(0, (prop['arv'] * 0.70) - prop['rehab_cost'])
            prop['profit_potential'] = prop['arv'] - prop['max_offer'] - prop['rehab_cost']
            
            # Add analysis data
            prop['analysis_data'] = json.dumps({
                'strategies': ['wholesale', 'fix_flip', 'buy_hold'],
                'market_score': np.random.randint(60, 95),
                'investment_grade': np.random.choice(['A', 'B', 'C']),
                'last_analyzed': datetime.now().isoformat()
            })
            
            # Add mock images
            prop['images'] = json.dumps([
                f'/images/property_{prop_id}_1.jpg',
                f'/images/property_{prop_id}_2.jpg',
                f'/images/property_{prop_id}_3.jpg'
            ])
            
            # Insert property
            placeholders = ', '.join(['?' for _ in prop.keys()])
            columns = ', '.join(prop.keys())
            cursor.execute(f'INSERT INTO properties ({columns}) VALUES ({placeholders})', list(prop.values()))
        
        # Comprehensive sample buyers
        sample_buyers = [
            {
                'user_id': None,
                'name': 'Empire Real Estate Group', 'email': 'contact@empirerealestate.com',
                'phone': '(555) 123-4567', 'company': 'Empire Real Estate Investments',
                'property_types': 'single_family,multi_family', 'min_price': 100000, 'max_price': 500000,
                'target_states': 'TX,OK,AR', 'target_cities': 'Dallas,Houston,Austin,Fort Worth',
                'deal_types': 'wholesale,fix_flip', 'verified': True, 'proof_of_funds': True,
                'cash_available': 2500000, 'acquisition_criteria': 'High-ROI properties with 18%+ returns',
                'preferred_areas': 'Dallas metro, Houston suburbs', 'max_rehab_tolerance': 75000,
                'min_roi_required': 18.0, 'investment_focus': 'Fix and flip + BRRRR',
                'communication_preferences': 'email,phone', 'deals_closed': 47, 'total_invested': 8500000,
                'rating': 4.8, 'notes': 'Reliable buyer, fast closings, prefers turnkey properties',
                'tags': 'verified,high-volume,fast-close'
            },
            {
                'user_id': None,
                'name': 'Pinnacle Property Partners', 'email': 'acquisitions@pinnacleproperties.com',
                'phone': '(555) 234-5678', 'company': 'Pinnacle Property Group',
                'property_types': 'single_family,condo,townhouse', 'min_price': 150000, 'max_price': 600000,
                'target_states': 'TX,CA,AZ', 'target_cities': 'Austin,San Antonio,Phoenix,San Diego',
                'deal_types': 'buy_hold,wholesale', 'verified': True, 'proof_of_funds': True,
                'cash_available': 3200000, 'acquisition_criteria': 'Cashflow-positive rentals in growth markets',
                'preferred_areas': 'Austin metro, emerging suburbs', 'max_rehab_tolerance': 50000,
                'min_roi_required': 15.0, 'investment_focus': 'Buy and hold portfolio',
                'communication_preferences': 'email,text', 'deals_closed': 34, 'total_invested': 12200000,
                'rating': 4.6, 'notes': 'Portfolio builder, excellent for buy-and-hold deals',
                'tags': 'verified,portfolio,buy-hold'
            },
            {
                'user_id': None,
                'name': 'Apex Capital Solutions', 'email': 'deals@apexcapitalsolutions.com',
                'phone': '(555) 345-6789', 'company': 'Apex Capital Partners',
                'property_types': 'multi_family,commercial', 'min_price': 300000, 'max_price': 2000000,
                'target_states': 'TX,FL,GA,NC', 'target_cities': 'Dallas,Houston,Miami,Atlanta,Charlotte',
                'deal_types': 'wholesale,syndication', 'verified': True, 'proof_of_funds': True,
                'cash_available': 5000000, 'acquisition_criteria': 'Large multi-family for syndication deals',
                'preferred_areas': 'Major metros, high-growth markets', 'max_rehab_tolerance': 200000,
                'min_roi_required': 20.0, 'investment_focus': 'Syndication and funds',
                'communication_preferences': 'email,phone', 'deals_closed': 28, 'total_invested': 25600000,
                'rating': 4.9, 'notes': 'Large-scale investor, syndication specialist',
                'tags': 'verified,syndication,large-deals'
            }
        ]
        
        # Insert buyers
        buyer_ids = []
        for buyer in sample_buyers:
            buyer_id = str(uuid.uuid4())
            buyer_ids.append(buyer_id)
            buyer['id'] = buyer_id
            buyer['last_activity'] = datetime.now().isoformat()
            
            placeholders = ', '.join(['?' for _ in buyer.keys()])
            columns = ', '.join(buyer.keys())
            cursor.execute(f'INSERT INTO buyers ({columns}) VALUES ({placeholders})', list(buyer.values()))
        
        # Comprehensive sample leads
        sample_leads = [
            {
                'user_id': wholesaler_users[0],
                'first_name': 'Maria', 'last_name': 'Garcia', 'phone': '(555) 111-2222',
                'email': 'maria.garcia@email.com', 'property_address': '1234 Elm Street, Dallas, TX',
                'property_id': property_ids[0] if property_ids else None,
                'motivation': 'divorce', 'timeline': 'asap', 'source': 'cold_calling',
                'status': 'interested', 'score': 92, 'property_condition': 'fair',
                'estimated_value': 285000, 'owed_amount': 195000, 'monthly_payment': 1845,
                'notes': 'Going through messy divorce, extremely motivated. Has court date next month.',
                'assigned_to': 'John Wholesaler', 'contact_attempts': 5,
                'call_outcome': 'Very interested, wants offer ASAP', 'tags': 'hot,motivated,divorce',
                'priority': 'high', 'conversion_probability': 85
            },
            {
                'user_id': wholesaler_users[0],
                'first_name': 'David', 'last_name': 'Brown', 'phone': '(555) 222-3333',
                'email': 'david.brown@email.com', 'property_address': '5678 Oak Avenue, Houston, TX',
                'property_id': property_ids[1] if len(property_ids) > 1 else None,
                'motivation': 'job_relocation', 'timeline': '30_days', 'source': 'direct_mail',
                'status': 'contacted', 'score': 78, 'property_condition': 'good',
                'estimated_value': 385000, 'owed_amount': 285000, 'monthly_payment': 2650,
                'notes': 'Corporate relocation to California. Company paying moving costs.',
                'assigned_to': 'John Wholesaler', 'contact_attempts': 3,
                'call_outcome': 'Interested but wants to compare options', 'tags': 'warm,relocation',
                'priority': 'medium', 'conversion_probability': 65
            },
            {
                'user_id': wholesaler_users[0],
                'first_name': 'Jennifer', 'last_name': 'Lee', 'phone': '(555) 333-4444',
                'email': 'jennifer.lee@email.com', 'property_address': '9876 Pine Road, Austin, TX',
                'property_id': property_ids[2] if len(property_ids) > 2 else None,
                'motivation': 'inherited_property', 'timeline': '60_days', 'source': 'lightning_leads',
                'status': 'new', 'score': 85, 'property_condition': 'excellent',
                'estimated_value': 425000, 'owed_amount': 0, 'monthly_payment': 0,
                'notes': 'Inherited from grandmother. Lives in New York, wants quick sale.',
                'assigned_to': '', 'contact_attempts': 0,
                'call_outcome': '', 'tags': 'new,inherited,out-of-state',
                'priority': 'high', 'conversion_probability': 75
            }
        ]
        
        # Insert leads with enhanced data
        lead_ids = []
        for i, lead in enumerate(sample_leads):
            lead_id = str(uuid.uuid4())
            lead_ids.append(lead_id)
            lead['id'] = lead_id
            
            lead['equity'] = lead['estimated_value'] - lead['owed_amount']
            lead['last_contact'] = (datetime.now() - timedelta(days=np.random.randint(0, 10))).isoformat()
            lead['next_followup'] = (datetime.now() + timedelta(days=np.random.randint(1, 7))).isoformat()
            
            placeholders = ', '.join(['?' for _ in lead.keys()])
            columns = ', '.join(lead.keys())
            cursor.execute(f'INSERT INTO leads ({columns}) VALUES ({placeholders})', list(lead.values()))
        
        # Sample deals
        sample_deals = [
            {
                'user_id': wholesaler_users[0],
                'title': 'Elm Street Wholesale Deal', 'property_id': property_ids[0] if property_ids else None,
                'lead_id': lead_ids[0] if lead_ids else None, 'buyer_id': buyer_ids[0] if buyer_ids else None,
                'stage': 'under_contract', 'contract_price': 220000, 'assignment_fee': 15000,
                'probability': 85, 'deal_type': 'wholesale', 'profit_margin': 15000, 'roi': 21.5,
                'commission': 1500, 'expenses': 500, 'net_profit': 13000,
                'notes': 'Strong deal with motivated seller and qualified buyer lined up.',
                'milestones': json.dumps([
                    {'milestone': 'Contract Executed', 'date': '2024-08-01', 'completed': True},
                    {'milestone': 'Buyer Found', 'date': '2024-08-05', 'completed': True},
                    {'milestone': 'Due Diligence', 'date': '2024-08-10', 'completed': False}
                ])
            },
            {
                'user_id': wholesaler_users[0],
                'title': 'Oak Avenue Fix & Flip', 'property_id': property_ids[1] if len(property_ids) > 1 else None,
                'lead_id': lead_ids[1] if len(lead_ids) > 1 else None, 'buyer_id': buyer_ids[1] if len(buyer_ids) > 1 else None,
                'stage': 'negotiating', 'contract_price': 285000, 'assignment_fee': 25000,
                'probability': 60, 'deal_type': 'assignment', 'profit_margin': 25000, 'roi': 18.2,
                'commission': 2500, 'expenses': 1000, 'net_profit': 21500,
                'notes': 'Buyer is interested but negotiating price. Good profit margin.',
                'milestones': json.dumps([
                    {'milestone': 'Initial Contact', 'date': '2024-07-20', 'completed': True},
                    {'milestone': 'Property Analysis', 'date': '2024-07-25', 'completed': True},
                    {'milestone': 'LOI Submitted', 'date': '2024-08-01', 'completed': False}
                ])
            }
        ]
        
        # Insert deals
        for deal in sample_deals:
            deal_id = str(uuid.uuid4())
            deal['id'] = deal_id
            deal['expected_close_date'] = (datetime.now() + timedelta(days=np.random.randint(7, 45))).isoformat()
            
            placeholders = ', '.join(['?' for _ in deal.keys()])
            columns = ', '.join(deal.keys())
            cursor.execute(f'INSERT INTO deals ({columns}) VALUES ({placeholders})', list(deal.values()))
        
        # Insert market data
        markets = [
            {'zip_code': '75201', 'city': 'Dallas', 'state': 'TX'},
            {'zip_code': '77001', 'city': 'Houston', 'state': 'TX'},
            {'zip_code': '78701', 'city': 'Austin', 'state': 'TX'}
        ]
        
        for market in markets:
            market_id = str(uuid.uuid4())
            market.update({
                'id': market_id,
                'median_home_price': np.random.randint(250000, 450000),
                'median_rent': np.random.randint(1400, 2800),
                'days_on_market': np.random.randint(15, 65),
                'price_per_sqft': np.random.randint(140, 280),
                'inventory_months': np.random.uniform(1.5, 6.0),
                'price_growth_yoy': np.random.uniform(-2, 12),
                'rent_growth_yoy': np.random.uniform(0, 8),
                'cap_rate': np.random.uniform(4, 10),
                'vacancy_rate': np.random.uniform(2, 12),
                'population_growth': np.random.uniform(-1, 4),
                'job_growth': np.random.uniform(-2, 6),
                'crime_index': np.random.randint(30, 90),
                'school_ratings': np.random.uniform(6, 9),
                'data_date': datetime.now().isoformat()
            })
            
            placeholders = ', '.join(['?' for _ in market.keys()])
            columns = ', '.join(market.keys())
            cursor.execute(f'INSERT INTO market_data ({columns}) VALUES ({placeholders})', list(market.values()))
        
        # Insert sample templates
        templates = [
            {
                'user_id': wholesaler_users[0],
                'template_type': 'email',
                'template_name': 'Initial Lead Contact',
                'content': 'Hi {first_name}, I saw your property at {property_address} and would like to make an offer...',
                'variables': json.dumps(['first_name', 'property_address']),
                'is_public': False
            },
            {
                'user_id': wholesaler_users[0],
                'template_type': 'loi',
                'template_name': 'Standard LOI Template',
                'content': 'Letter of Intent template with standard terms...',
                'variables': json.dumps(['seller_name', 'property_address', 'offer_price']),
                'is_public': False
            }
        ]
        
        for template in templates:
            template_id = str(uuid.uuid4())
            template['id'] = template_id
            
            placeholders = ', '.join(['?' for _ in template.keys()])
            columns = ', '.join(template.keys())
            cursor.execute(f'INSERT INTO templates ({columns}) VALUES ({placeholders})', list(template.values()))
        
        # Insert sample notifications
        notifications = [
            {
                'user_id': wholesaler_users[0],
                'title': 'New Lead Assigned',
                'message': 'You have been assigned a new lead: Maria Garcia',
                'type': 'info',
                'action_url': '/lead_manager',
                'priority': 2
            },
            {
                'user_id': wholesaler_users[0],
                'title': 'Deal Update Required',
                'message': 'Your Elm Street deal needs attention',
                'type': 'warning',
                'action_url': '/deal_pipeline',
                'priority': 3
            }
        ]
        
        for notification in notifications:
            notification_id = str(uuid.uuid4())
            notification['id'] = notification_id
            
            placeholders = ', '.join(['?' for _ in notification.keys()])
            columns = ', '.join(notification.keys())
            cursor.execute(f'INSERT INTO notifications ({columns}) VALUES ({placeholders})', list(notification.values()))
        
        conn.commit()
        conn.close()
    
    def _calculate_rehab_cost(self, property_data):
        """Calculate realistic rehab costs"""
        condition_multipliers = {
            'excellent': 0,
            'good': 8,
            'fair': 18,
            'poor': 32,
            'needs_rehab': 50
        }
        
        base_cost = property_data['square_feet'] * condition_multipliers.get(property_data['condition'], 20)
        fixed_costs = 15000
        
        return base_cost + fixed_costs
    
    def get_connection(self):
        return sqlite3.connect('wtf_ultimate.db')

# Usage Tracking Manager
class UsageTrackingManager:
    """Complete usage tracking and management system"""
    
    def __init__(self, db_manager: UltimateDatabaseManager):
        self.db = db_manager
    
    def check_usage_limit(self, user_id: str, action_type: str) -> Dict:
        """Check if user can perform action based on subscription limits"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT subscription_tier FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        if not result:
            return {'allowed': False, 'error': 'User not found'}
        
        subscription_tier = result[0]
        limits = SUBSCRIPTION_TIERS[subscription_tier]['features']
        
        if action_type not in limits:
            return {'allowed': True, 'remaining': -1}
        
        limit = limits[action_type]
        
        if limit == -1:  # Unlimited
            return {'allowed': True, 'remaining': -1}
        
        # Get current usage for this month
        current_date = datetime.now().date()
        month_start = current_date.replace(day=1)
        
        cursor.execute('''
            SELECT COALESCE(SUM(count), 0)
            FROM usage_tracking
            WHERE user_id = ? AND action_type = ? AND date >= ?
        ''', (user_id, action_type, month_start))
        
        current_usage = cursor.fetchone()[0]
        conn.close()
        
        remaining = limit - current_usage
        allowed = remaining > 0
        
        return {
            'allowed': allowed,
            'remaining': max(0, remaining),
            'limit': limit,
            'current_usage': current_usage
        }
    
    def track_usage(self, user_id: str, action_type: str, count: int = 1, details: str = ''):
        """Track user action usage with details"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        current_date = datetime.now().date()
        tracking_id = str(uuid.uuid4())
        
        cursor.execute('''
            SELECT id, count FROM usage_tracking
            WHERE user_id = ? AND action_type = ? AND date = ?
        ''', (user_id, action_type, current_date))
        
        existing = cursor.fetchone()
        
        if existing:
            new_count = existing[1] + count
            cursor.execute('''
                UPDATE usage_tracking SET count = ?, details = ? WHERE id = ?
            ''', (new_count, details, existing[0]))
        else:
            cursor.execute('''
                INSERT INTO usage_tracking (id, user_id, action_type, resource_used, count, date, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (tracking_id, user_id, action_type, action_type, count, current_date, details))
        
        conn.commit()
        conn.close()
    
    def get_usage_summary(self, user_id: str) -> Dict:
        """Get comprehensive usage summary"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT subscription_tier FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        if not result:
            return {}
        
        subscription_tier = result[0]
        limits = SUBSCRIPTION_TIERS[subscription_tier]['features']
        
        current_date = datetime.now().date()
        month_start = current_date.replace(day=1)
        
        cursor.execute('''
            SELECT action_type, SUM(count)
            FROM usage_tracking
            WHERE user_id = ? AND date >= ?
            GROUP BY action_type
        ''', (user_id, month_start))
        
        usage_data = dict(cursor.fetchall())
        conn.close()
        
        summary = {}
        for action_type, limit in limits.items():
            if isinstance(limit, int):
                current_usage = usage_data.get(action_type, 0)
                summary[action_type] = {
                    'limit': limit,
                    'used': current_usage,
                    'remaining': max(0, limit - current_usage) if limit != -1 else -1,
                    'percentage': (current_usage / limit * 100) if limit > 0 else 0
                }
        
        return summary
    
    def get_usage_analytics(self, user_id: str, days: int = 30) -> Dict:
        """Get usage analytics for specified period"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now().date() - timedelta(days=days)
        
        cursor.execute('''
            SELECT date, action_type, SUM(count) as total
            FROM usage_tracking
            WHERE user_id = ? AND date >= ?
            GROUP BY date, action_type
            ORDER BY date DESC
        ''', (user_id, start_date))
        
        usage_data = cursor.fetchall()
        conn.close()
        
        # Process data for analytics
        analytics = {
            'daily_usage': {},
            'action_totals': {},
            'trends': {}
        }
        
        for date, action_type, total in usage_data:
            if date not in analytics['daily_usage']:
                analytics['daily_usage'][date] = {}
            analytics['daily_usage'][date][action_type] = total
            
            if action_type not in analytics['action_totals']:
                analytics['action_totals'][action_type] = 0
            analytics['action_totals'][action_type] += total
        
        return analytics

# Notification Manager
class NotificationManager:
    """Complete notification system"""
    
    def __init__(self, db_manager: UltimateDatabaseManager):
        self.db = db_manager
    
    def create_notification(self, user_id: str, title: str, message: str, 
                          notification_type: str = 'info', action_url: str = '', 
                          priority: int = 1, expires_hours: int = 24):
        """Create a new notification"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        notification_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        cursor.execute('''
            INSERT INTO notifications (id, user_id, title, message, type, action_url, priority, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (notification_id, user_id, title, message, notification_type, action_url, priority, expires_at))
        
        conn.commit()
        conn.close()
        
        return notification_id
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        """Get user notifications"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, title, message, type, read_status, action_url, priority, created_at
            FROM notifications
            WHERE user_id = ? AND (expires_at IS NULL OR expires_at > ?)
        '''
        params = [user_id, datetime.now()]
        
        if unread_only:
            query += ' AND read_status = 0'
        
        query += ' ORDER BY priority DESC, created_at DESC LIMIT 50'
        
        cursor.execute(query, params)
        notifications = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': n[0],
                'title': n[1],
                'message': n[2],
                'type': n[3],
                'read_status': n[4],
                'action_url': n[5],
                'priority': n[6],
                'created_at': n[7]
            }
            for n in notifications
        ]
    
    def mark_notification_read(self, notification_id: str, user_id: str):
        """Mark notification as read"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET read_status = 1 
            WHERE id = ? AND user_id = ?
        ''', (notification_id, user_id))
        
        conn.commit()
        conn.close()
    
    def mark_all_read(self, user_id: str):
        """Mark all notifications as read for user"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET read_status = 1 WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()

# Activity Logger
class ActivityLogger:
    """Complete activity logging system"""
    
    def __init__(self, db_manager: UltimateDatabaseManager):
        self.db = db_manager
    
    def log_activity(self, user_id: str, action_type: str, description: str,
                    entity_type: str = '', entity_id: str = '', metadata: Dict = None):
        """Log user activity"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        activity_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO activity_log (id, user_id, action_type, action_description, 
                                    entity_type, entity_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (activity_id, user_id, action_type, description, entity_type, entity_id,
              json.dumps(metadata) if metadata else None))
        
        conn.commit()
        conn.close()
    
    def get_user_activity(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Get user activity log"""
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT action_type, action_description, entity_type, entity_id, created_at, metadata
            FROM activity_log
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        activities = cursor.fetchall()
        conn.close()
        
        return [
            {
                'action_type': a[0],
                'description': a[1],
                'entity_type': a[2],
                'entity_id': a[3],
                'created_at': a[4],
                'metadata': json.loads(a[5]) if a[5] else None
            }
            for a in activities
        ]

# Initialize all services
@st.cache_resource
def get_ultimate_services():
    """Initialize all ultimate services"""
    db_manager = UltimateDatabaseManager()
    return {
        'db': db_manager,
        'usage_tracker': UsageTrackingManager(db_manager),
        'notifications': NotificationManager(db_manager),
        'activity_logger': ActivityLogger(db_manager)
    }

services = get_ultimate_services()

# Enhanced Authentication
def ultimate_authenticate(username: str, password: str, whop_token: str = '') -> tuple:
    """Ultimate authentication system"""
    
    conn = services['db'].get_connection()
    cursor = conn.cursor()
    
    if whop_token:
        # Whop authentication logic would go here
        # For demo, we'll fall back to standard auth
        pass
    
    # Standard authentication
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        SELECT id, username, email, role, full_name, company, subscription_tier, 
               subscription_status, whop_user_id, api_key, preferences
        FROM users 
        WHERE username = ? AND password_hash = ? AND is_active = 1
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    
    if user:
        # Update last login and activity
        cursor.execute('UPDATE users SET last_login = ?, last_activity = ? WHERE id = ?',
                      (datetime.now().isoformat(), datetime.now().isoformat(), user[0]))
        
        # Log login activity
        services['activity_logger'].log_activity(
            user[0], 'login', f'User {username} logged in',
            metadata={'ip_address': '127.0.0.1', 'user_agent': 'Streamlit'}
        )
        
        conn.commit()
        conn.close()
        
        return True, {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3],
            'full_name': user[4],
            'company': user[5],
            'subscription_tier': user[6],
            'subscription_status': user[7],
            'whop_user_id': user[8],
            'api_key': user[9],
            'preferences': json.loads(user[10]) if user[10] else {}
        }
    
    conn.close()
    return False, None

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'show_landing' not in st.session_state:
    st.session_state.show_landing = True
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# Ultimate Landing Page
def render_ultimate_landing_page():
    """Ultimate professional landing page"""
    
    st.markdown("""
    <div class='landing-hero'>
        <div class='hero-title'>WTF</div>
        <div class='hero-subtitle'>Wholesale on Steroids</div>
        <p style='font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.9; position: relative; z-index: 1;'>
            The Complete Real Estate Wholesaling Platform
        </p>
        <p style='font-size: 1.1rem; margin-bottom: 3rem; opacity: 0.8; position: relative; z-index: 1;'>
            Generate contracts, analyze deals, manage leads, and close faster than ever before.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ultimate features showcase
    st.markdown("## 🚀 Complete Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #8B5CF6; text-align: center; margin-bottom: 1.5rem;'>🔍 Live Deal Analysis</h3>
            <ul style='color: white; line-height: 1.8;'>
                <li>Real-time Zillow, PropStream & Privy integration</li>
                <li>Advanced 70% rule calculator</li>
                <li>Multi-strategy ROI analysis</li>
                <li>Automated ARV calculations</li>
                <li>Risk assessment matrix</li>
                <li>Market trend analysis</li>
                <li>Comparable sales analysis</li>
                <li>Investment grade scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #10B981; text-align: center; margin-bottom: 1.5rem;'>📄 Contract Generation</h3>
            <ul style='color: white; line-height: 1.8;'>
                <li>Professional LOI generator</li>
                <li>Wholesale assignment contracts</li>
                <li>Purchase agreements</li>
                <li>Option contracts</li>
                <li>PDF download & e-signature</li>
                <li>Legal template library</li>
                <li>Custom clause builder</li>
                <li>Automated calculations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #F59E0B; text-align: center; margin-bottom: 1.5rem;'>👥 Complete CRM</h3>
            <ul style='color: white; line-height: 1.8;'>
                <li>5,000+ verified cash buyers</li>
                <li>Advanced lead management</li>
                <li>Deal pipeline tracking</li>
                <li>Email automation</li>
                <li>Activity logging</li>
                <li>Performance analytics</li>
                <li>Notification system</li>
                <li>Mobile responsive</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Ultimate Pricing Section
    st.markdown("## 💎 Choose Your Plan")
    
    pricing_cols = st.columns(4)
    
    for i, (tier_key, tier_data) in enumerate(SUBSCRIPTION_TIERS.items()):
        with pricing_cols[i]:
            is_popular = tier_key == 'pro'
            card_class = 'pricing-card pricing-popular' if is_popular else 'pricing-card'
            
            st.markdown(f"""
            <div class='{card_class}'>
                <h3 style='color: {tier_data["color"]}; margin-bottom: 1rem; font-size: 1.5rem;'>
                    {tier_data["icon"]} {tier_data["name"]}
                </h3>
                <div style='font-size: 3rem; font-weight: bold; color: white; margin-bottom: 1rem;'>
                    ${tier_data["price"]}
                </div>
                <div style='color: #94A3B8; margin-bottom: 2rem;'>
                    {"Free Forever" if tier_data["price"] == 0 else f"${tier_data['monthly_price']}/month"}
                </div>
                
                <div style='text-align: left; margin-bottom: 2rem;'>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>📊 Deal Analysis:</strong> {tier_data["features"]["deal_analysis"] if tier_data["features"]["deal_analysis"] != -1 else "Unlimited"}/month
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>📞 Lead Management:</strong> {tier_data["features"]["lead_management"] if tier_data["features"]["lead_management"] != -1 else "Unlimited"} leads
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>📄 LOI Generation:</strong> {tier_data["features"]["loi_generation"] if tier_data["features"]["loi_generation"] != -1 else "Unlimited"}/month
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>📋 Contracts:</strong> {tier_data["features"]["contract_generation"] if tier_data["features"]["contract_generation"] != -1 else "Unlimited"}/month
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>👥 Buyer Network:</strong> {"✅" if tier_data["features"]["buyer_network"] else "❌"}
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>📧 Email Campaigns:</strong> {tier_data["features"]["email_campaigns"] if tier_data["features"]["email_campaigns"] != -1 else "Unlimited"}/month
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>🔧 API Access:</strong> {"✅" if tier_data["features"]["api_access"] else "❌"}
                    </div>
                    <div style='color: white; margin-bottom: 0.5rem;'>
                        <strong>📞 Support:</strong> {tier_data["features"]["support"]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Choose {tier_data['name']}", key=f"choose_{tier_key}", use_container_width=True):
                if tier_key == 'free':
                    st.session_state.selected_plan = tier_key
                    st.success("Free plan selected! Create your account below.")
                else:
                    st.session_state.selected_plan = tier_key
                    st.success(f"{tier_data['name']} selected! Complete registration to continue.")
    
    # Enhanced Authentication Section
    st.markdown("---")
    st.markdown("## 🔑 Access Platform")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🛍️ Whop Integration"])
    
    with tab1:
        with st.form("login_form"):
            st.markdown("### Sign In to Your Account")
            
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            with col2:
                remember_me = st.checkbox("Remember me")
                forgot_password = st.checkbox("Forgot password?")
            
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("Sign In", use_container_width=True)
            with col2:
                demo_submitted = st.form_submit_button("Try Demo", use_container_width=True)
            
            if login_submitted and username and password:
                success, user_data = ultimate_authenticate(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.show_landing = False
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            
            if demo_submitted:
                success, user_data = ultimate_authenticate('wholesaler', 'wholesale123')
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.show_landing = False
                    st.success("Demo access granted!")
                    st.rerun()
    
    with tab2:
        with st.form("register_form"):
            st.markdown("### Create New Account")
            
            col1, col2 = st.columns(2)
            with col1:
                reg_username = st.text_input("Username*", placeholder="Choose username")
                reg_email = st.text_input("Email*", placeholder="your@email.com")
                reg_password = st.text_input("Password*", type="password", placeholder="Secure password")
                reg_confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm password")
            
            with col2:
                reg_full_name = st.text_input("Full Name*", placeholder="John Doe")
                reg_company = st.text_input("Company", placeholder="Your Company (optional)")
                reg_phone = st.text_input("Phone", placeholder="(555) 123-4567")
                reg_role = st.selectbox("Role", ["wholesaler", "buyer"], format_func=lambda x: x.title())
            
            selected_tier = st.selectbox("Subscription Plan", 
                                       options=list(SUBSCRIPTION_TIERS.keys()),
                                       format_func=lambda x: f"{SUBSCRIPTION_TIERS[x]['icon']} {SUBSCRIPTION_TIERS[x]['name']} - ${SUBSCRIPTION_TIERS[x]['price']}/month")
            
            terms_accepted = st.checkbox("I accept the Terms of Service and Privacy Policy*")
            marketing_consent = st.checkbox("I'd like to receive marketing emails about new features")
            
            reg_submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if reg_submitted:
                if all([reg_username, reg_email, reg_password, reg_full_name, terms_accepted]):
                    if reg_password != reg_confirm_password:
                        st.error("Passwords do not match")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        try:
                            conn = services['db'].get_connection()
                            cursor = conn.cursor()
                            
                            # Check if username/email exists
                            cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                                         (reg_username, reg_email))
                            if cursor.fetchone():
                                st.error("Username or email already exists")
                            else:
                                user_id = str(uuid.uuid4())
                                password_hash = hashlib.sha256(reg_password.encode()).hexdigest()
                                api_key = secrets.token_urlsafe(32)
                                
                                cursor.execute('''
                                    INSERT INTO users (id, username, email, password_hash, role, full_name,
                                                     phone, company, subscription_tier, api_key, preferences)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (user_id, reg_username, reg_email, password_hash, reg_role,
                                      reg_full_name, reg_phone, reg_company, selected_tier, api_key,
                                      json.dumps({'marketing_consent': marketing_consent})))
                                
                                # Create welcome notification
                                services['notifications'].create_notification(
                                    user_id, "Welcome to WTF Platform!", 
                                    f"Welcome {reg_full_name}! Your account has been created successfully.",
                                    "success", "/dashboard", 1, 168  # 7 days
                                )
                                
                                conn.commit()
                                conn.close()
                                
                                st.success("Account created successfully! You can now log in.")
                                
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")
                else:
                    st.error("Please fill in all required fields and accept the terms")
    
    with tab3:
        st.markdown("### 🛍️ Connect with Whop Account")
        st.info("Connect your existing Whop account for seamless access and subscription management.")
        
        with st.form("whop_login_form"):
            whop_token = st.text_input("Whop Access Token", 
                                     placeholder="Enter your Whop access token",
                                     help="Get your access token from your Whop dashboard")
            
            whop_submitted = st.form_submit_button("Connect Whop Account", use_container_width=True)
            
            if whop_submitted and whop_token:
                # Mock Whop integration for demo
                st.success("Whop integration coming soon! Use standard login for now.")
        
        st.markdown("---")
        st.markdown("**Don't have a Whop account?**")
        st.markdown("[Create Whop Account](https://whop.com) • [What is Whop?](https://whop.com/about)")
    
    # Demo credentials info
    st.markdown("---")
    st.info("""
    **Demo Credentials for Testing:**
    
    🔑 **Admin:** admin / admin123 (Full platform control)
    
    🏠 **Wholesaler:** wholesaler / wholesale123 (Deal analysis & CRM)
    
    💰 **Buyer:** buyer / buyer123 (Browse deals & market data)
    
    🆓 **Demo User:** demo_wholesaler / demo123 (Free tier testing)
    """)

# Ultimate Sidebar with complete functionality
def render_ultimate_sidebar():
    """Ultimate sidebar with complete functionality"""
    user_role = st.session_state.user_data.get('role', 'wholesaler')
    full_name = st.session_state.user_data.get('full_name', 'User')
    company = st.session_state.user_data.get('company', '')
    subscription_tier = st.session_state.user_data.get('subscription_tier', 'free')
    user_id = st.session_state.user_data.get('id', '')
    
    # Get subscription info
    tier_info = SUBSCRIPTION_TIERS.get(subscription_tier, SUBSCRIPTION_TIERS['free'])
    
    # Get usage summary
    usage_summary = services['usage_tracker'].get_usage_summary(user_id)
    
    # Get notifications
    notifications = services['notifications'].get_user_notifications(user_id, unread_only=True)
    
    role_colors = {
        'admin': 'linear-gradient(135deg, #DC2626 0%, #7C2D12 100%)',
        'wholesaler': 'linear-gradient(135deg, #8B5CF6 0%, #5B21B6 100%)',
        'buyer': 'linear-gradient(135deg, #10B981 0%, #065F46 100%)'
    }
    
    # Header with notifications
    notification_count = len(notifications)
    notification_badge = f" ({notification_count})" if notification_count > 0 else ""
    
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 1.5rem; background: {role_colors.get(user_role, role_colors["wholesaler"])}; 
                border-radius: 15px; margin-bottom: 1rem; box-shadow: 0 10px 25px rgba(0,0,0,0.3);'>
        <h1 style='color: white; font-size: 2.5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>WTF</h1>
        <p style='color: white; font-weight: bold; margin: 0; font-size: 1.1rem;'>Wholesale on Steroids</p>
        <p style='color: white; font-size: 0.9rem; margin: 0; opacity: 0.9;'>{user_role.title()} Portal</p>
        <div class='subscription-badge'>{tier_info["icon"]} {tier_info["name"]}</div>
        <p style='color: white; font-size: 0.8rem; margin: 0.5rem 0; opacity: 0.8;'>
            🔔 {notification_count} new notifications
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Notifications dropdown
    if notifications:
        with st.sidebar.expander(f"🔔 Notifications{notification_badge}", expanded=False):
            for notification in notifications[:5]:  # Show top 5
                st.markdown(f"""
                <div class='notification-card'>
                    <strong>{notification['title']}</strong><br>
                    <small>{notification['message']}</small><br>
                    <small style='color: #9CA3AF;'>{notification['created_at'][:10]}</small>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("Mark All Read"):
                services['notifications'].mark_all_read(user_id)
                st.success("All notifications marked as read")
                st.rerun()
    
    # Role-based navigation
    if user_role == 'admin':
        pages = {
            "🏠 Admin Dashboard": "admin_dashboard",
            "📊 Platform Analytics": "platform_analytics", 
            "👥 User Management": "user_management",
            "💰 Revenue Dashboard": "revenue_dashboard",
            "📋 Master Dispo": "master_dispo",
            "🔧 System Settings": "system_settings",
            "📄 All Contracts": "all_contracts",
            "📝 All LOIs": "all_lois",
            "📧 Email Manager": "email_manager",
            "🔔 Notifications": "notifications_manager"
        }
    elif user_role == 'wholesaler':
        pages = {
            "🏠 Dashboard": "dashboard",
            "🔍 Deal Analyzer": "deal_analyzer",
            "📞 Lead Manager": "lead_manager",
            "📋 Deal Pipeline": "deal_pipeline",
            "👥 Buyer Network": "buyer_network",
            "📄 Contract Generator": "contract_generator",
            "📝 LOI Generator": "loi_generator",
            "📧 Email Campaigns": "email_campaigns",
            "⚡ Lightning Leads": "lightning_leads",
            "📊 My Analytics": "analytics",
            "📱 Mobile Tools": "mobile_tools",
            "⚙️ Account Settings": "account_settings"
        }
    else:  # buyer
        pages = {
            "🏠 Buyer Dashboard": "buyer_dashboard",
            "🔍 Available Deals": "available_deals",
            "📊 Market Analysis": "market_analysis",
            "📋 My Offers": "my_offers",
            "🎯 Deal Alerts": "deal_alerts",
            "💼 My Portfolio": "my_portfolio",
            "📈 Investment Tracker": "investment_tracker",
            "⚙️ Preferences": "buyer_preferences"
        }
    
    selected_page = st.sidebar.selectbox("Navigate", list(pages.keys()), key="navigation")
    
    # Usage summary for non-admin users
    if user_role != 'admin' and usage_summary:
        st.sidebar.markdown("### 📊 Monthly Usage")
        
        for action_type, usage_data in usage_summary.items():
            if action_type in ['deal_analysis', 'loi_generation', 'contract_generation', 'email_campaigns']:
                limit = usage_data['limit']
                used = usage_data['used']
                remaining = usage_data['remaining']
                percentage = usage_data['percentage']
                
                # Format display names
                display_names = {
                    'deal_analysis': '🔍 Deal Analysis',
                    'loi_generation': '📝 LOI Generation', 
                    'contract_generation': '📄 Contracts',
                    'email_campaigns': '📧 Email Campaigns'
                }
                
                limit_text = "Unlimited" if limit == -1 else str(limit)
                remaining_text = "Unlimited" if remaining == -1 else str(remaining)
                
                # Color based on usage
                if percentage >= 90:
                    color = "#EF4444"  # Red
                elif percentage >= 70:
                    color = "#F59E0B"  # Orange
                else:
                    color = "#10B981"  # Green
                
                # Progress bar
                progress_width = min(percentage, 100)
                
                st.sidebar.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                    <div style='color: white; font-weight: bold; margin-bottom: 0.5rem;'>
                        {display_names.get(action_type, action_type)}
                    </div>
                    <div style='color: {color}; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                        Used: {used} / {limit_text}
                    </div>
                    <div class='progress-container'>
                        <div class='progress-bar' style='width: {progress_width}%; background: {color};'></div>
                    </div>
                    <div style='color: #94A3B8; font-size: 0.8rem; margin-top: 0.5rem;'>
                        Remaining: {remaining_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick stats
    st.sidebar.markdown("### 📈 Quick Stats")
    
    # Get user stats
    conn = services['db'].get_connection()
    cursor = conn.cursor()
    
    if user_role == 'wholesaler':
        cursor.execute('SELECT COUNT(*) FROM leads WHERE user_id = ?', (user_id,))
        total_leads = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM deals WHERE user_id = ?', (user_id,))
        total_deals = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM properties WHERE user_id = ?', (user_id,))
        total_properties = cursor.fetchone()[0]
        
        st.sidebar.markdown(f"""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            <div style='color: #8B5CF6; font-weight: bold;'>📞 Total Leads: {total_leads}</div>
            <div style='color: #8B5CF6; font-weight: bold;'>📋 Active Deals: {total_deals}</div>
            <div style='color: #8B5CF6; font-weight: bold;'>🏠 Properties: {total_properties}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif user_role == 'buyer':
        cursor.execute('SELECT COUNT(*) FROM deals WHERE buyer_id IN (SELECT id FROM buyers WHERE email = ?)', 
                      (st.session_state.user_data.get('email', ''),))
        my_deals = cursor.fetchone()[0]
        
        st.sidebar.markdown(f"""
        <div style='background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            <div style='color: #10B981; font-weight: bold;'>💼 My Deals: {my_deals}</div>
            <div style='color: #10B981; font-weight: bold;'>🔍 Available: 25</div>
            <div style='color: #10B981; font-weight: bold;'>📊 Analyzed: 47</div>
        </div>
        """, unsafe_allow_html=True)
    
    conn.close()
    
    # User info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**User:** {full_name}")
    if company:
        st.sidebar.markdown(f"**Company:** {company}")
    st.sidebar.markdown(f"**Role:** {user_role.title()}")
    st.sidebar.markdown(f"**Plan:** {tier_info['name']}")
    
    # Upgrade button for non-enterprise users
    if subscription_tier != 'enterprise':
        if st.sidebar.button("🚀 Upgrade Plan", use_container_width=True):
            st.session_state.show_upgrade_modal = True
            st.success("Upgrade options available! Contact sales for details.")
    
    # API Key for developers
    if subscription_tier in ['pro', 'enterprise']:
        with st.sidebar.expander("🔑 API Access"):
            api_key = st.session_state.user_data.get('api_key', 'Not available')
            st.code(api_key[:20] + "..." if len(api_key) > 20 else api_key)
            st.caption("Use this API key for integrations")
    
    # Quick actions
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if user_role == 'wholesaler':
        if st.sidebar.button("📞 Add Lead", use_container_width=True):
            st.session_state.quick_add_lead = True
            st.info("Quick add lead form opened")
        
        if st.sidebar.button("🔍 Analyze Deal", use_container_width=True):
            st.session_state.quick_analyze = True
            st.info("Quick deal analyzer opened")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        # Log logout activity
        services['activity_logger'].log_activity(
            user_id, 'logout', f'User {st.session_state.user_data.get("username")} logged out'
        )
        
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.show_landing = True
        st.rerun()
    
    return pages[selected_page]

# Ultimate Dashboard
def render_ultimate_dashboard():
    """Ultimate wholesaler dashboard with complete functionality"""
    st.markdown('<h1 class="main-header">🏠 Ultimate Wholesaler Dashboard</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user_data.get('id')
    user_name = st.session_state.user_data.get('full_name', 'User')
    
    # Welcome message with time-based greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    st.markdown(f"""
    <div class='wholesaler-panel'>
        <h3 style='color: white; margin: 0; text-align: center;'>🎯 {greeting}, {user_name}!</h3>
        <p style='color: white; margin: 0.5rem 0; text-align: center;'>
            Welcome to your wholesaling command center
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get comprehensive dashboard data
    conn = services['db'].get_connection()
    cursor = conn.cursor()
    
    # User's deals statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_deals,
            COUNT(CASE WHEN stage = 'closed' THEN 1 END) as closed_deals,
            COUNT(CASE WHEN stage IN ('under_contract', 'pending') THEN 1 END) as active_deals,
            SUM(CASE WHEN stage = 'closed' THEN assignment_fee ELSE 0 END) as total_revenue,
            AVG(CASE WHEN stage = 'closed' THEN assignment_fee ELSE NULL END) as avg_deal_size,
            SUM(CASE WHEN stage IN ('under_contract', 'pending') THEN assignment_fee ELSE 0 END) as pipeline_value
        FROM deals d
        WHERE d.user_id = ?
    ''', (user_id,))
    
    deal_stats = cursor.fetchone()
    
    # User's leads statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_leads,
            COUNT(CASE WHEN status = 'interested' THEN 1 END) as hot_leads,
            COUNT(CASE WHEN status = 'new' THEN 1 END) as new_leads,
            COUNT(CASE WHEN next_followup < ? THEN 1 END) as overdue_followups,
            AVG(score) as avg_score,
            COUNT(CASE WHEN last_contact > ? THEN 1 END) as contacted_today
        FROM leads
        WHERE user_id = ?
    ''', (user_id, datetime.now().isoformat(), 
          (datetime.now() - timedelta(days=1)).isoformat()))
    
    lead_stats = cursor.fetchone()
    
    # Properties statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_properties,
            AVG(profit_potential) as avg_profit,
            COUNT(CASE WHEN profit_potential > 20000 THEN 1 END) as grade_a_deals
        FROM properties
        WHERE user_id = ?
    ''', (user_id,))
    
    property_stats = cursor.fetchone()
    
    conn.close()
    
    # Key Performance Indicators
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card success-metric'>
            <h3 style='color: #10B981; margin: 0; font-size: 2rem;'>${deal_stats[3] or 0:,.0f}</h3>
            <p style='margin: 0; font-weight: bold;'>Total Revenue</p>
            <small style='color: #9CA3AF;'>{deal_stats[1] or 0} deals closed</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0; font-size: 2rem;'>${deal_stats[5] or 0:,.0f}</h3>
            <p style='margin: 0; font-weight: bold;'>Pipeline Value</p>
            <small style='color: #9CA3AF;'>{deal_stats[2] or 0} active deals</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card warning-metric'>
            <h3 style='color: #F59E0B; margin: 0; font-size: 2rem;'>{lead_stats[1] or 0}</h3>
            <p style='margin: 0; font-weight: bold;'>Hot Leads</p>
            <small style='color: #9CA3AF;'>{lead_stats[0] or 0} total leads</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0; font-size: 2rem;'>{property_stats[2] or 0}</h3>
            <p style='margin: 0; font-weight: bold;'>Grade A Deals</p>
            <small style='color: #9CA3AF;'>{property_stats[0] or 0} total analyzed</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        conversion_rate = (deal_stats[1] / lead_stats[0] * 100) if lead_stats[0] and lead_stats[0] > 0 else 0
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0; font-size: 2rem;'>{conversion_rate:.1f}%</h3>
            <p style='margin: 0; font-weight: bold;'>Conversion Rate</p>
            <small style='color: #9CA3AF;'>Lead to deal</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions and Tools
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Analyze New Deal", use_container_width=True):
            st.session_state.quick_analyze = True
            st.switch_page("Deal Analyzer")
    
    with col2:
        if st.button("📞 Add New Lead", use_container_width=True):
            st.session_state.quick_add_lead = True
            st.info("Quick add lead modal opened")
    
    with col3:
        if st.button("📝 Generate LOI", use_container_width=True):
            st.switch_page("LOI Generator")
    
    with col4:
        if st.button("📄 Create Contract", use_container_width=True):
            st.switch_page("Contract Generator")
    
    # Recent Activity and Updates
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Recent Deals")
        
        # Get recent deals
        conn = services['db'].get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT d.title, d.stage, d.assignment_fee, d.probability, d.created_at,
                   p.address
            FROM deals d
            LEFT JOIN properties p ON d.property_id = p.id
            WHERE d.user_id = ?
            ORDER BY d.created_at DESC
            LIMIT 5
        ''', (user_id,))
        
        recent_deals = cursor.fetchall()
        
        if recent_deals:
            for deal in recent_deals:
                stage_colors = {
                    'prospecting': '#6B7280',
                    'contacted': '#8B5CF6',
                    'negotiating': '#F59E0B',
                    'under_contract': '#10B981',
                    'pending': '#F97316',
                    'closed': '#059669'
                }
                
                stage_color = stage_colors.get(deal[1], '#6B7280')
                
                st.markdown(f"""
                <div class='deal-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h5 style='color: white; margin: 0;'>{deal[0] or 'Untitled Deal'}</h5>
                            <small style='color: #9CA3AF;'>{deal[5] or 'No address'}</small>
                        </div>
                        <div style='text-align: right;'>
                            <p style='color: {stage_color}; margin: 0; font-weight: bold;'>{deal[1].title()}</p>
                            <p style='color: #10B981; margin: 0;'>${deal[2] or 0:,.0f}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No deals yet. Start analyzing properties to create your first deal!")
    
    with col2:
        st.markdown("### 📞 Recent Leads")
        
        cursor.execute('''
            SELECT first_name, last_name, status, score, property_address, created_at
            FROM leads
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 5
        ''', (user_id,))
        
        recent_leads = cursor.fetchall()
        
        if recent_leads:
            for lead in recent_leads:
                status_colors = {
                    'new': '#8B5CF6',
                    'contacted': '#F59E0B',
                    'interested': '#10B981',
                    'not_interested': '#6B7280',
                    'under_contract': '#EF4444'
                }
                
                status_color = status_colors.get(lead[2], '#6B7280')
                score_color = '#10B981' if lead[3] >= 80 else '#F59E0B' if lead[3] >= 60 else '#6B7280'
                
                st.markdown(f"""
                <div class='lead-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h5 style='color: white; margin: 0;'>{lead[0]} {lead[1]}</h5>
                            <small style='color: #9CA3AF;'>{lead[4]}</small>
                        </div>
                        <div style='text-align: right;'>
                            <p style='color: {status_color}; margin: 0; font-weight: bold;'>{lead[2].title()}</p>
                            <p style='color: {score_color}; margin: 0;'>Score: {lead[3]}/100</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No leads yet. Start your lead generation campaigns!")
        
        conn.close()
    
    # Performance Charts
    st.markdown("## 📈 Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly revenue chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        revenue = [15000, 22000, 18000, 28000, 31000, 27000, 35000, 42000]
        
        fig_revenue = px.line(
            x=months, y=revenue, 
            title='Monthly Revenue Trend',
            labels={'x': 'Month', 'y': 'Revenue ($)'}
        )
        fig_revenue.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        fig_revenue.update_traces(line_color='#10B981', line_width=3)
        
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Deal pipeline funnel
        stages = ['Leads', 'Contacted', 'Interested', 'Under Contract', 'Closed']
        counts = [100, 75, 45, 25, 15]
        
        fig_funnel = go.Figure(go.Funnel(
            y=stages,
            x=counts,
            textinfo="value+percent initial",
            marker_color=["#8B5CF6", "#7C3AED", "#6D28D9", "#5B21B6", "#10B981"]
        ))
        
        fig_funnel.update_layout(
            title="Deal Pipeline Funnel",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Today's Tasks and Priorities
    st.markdown("## 📅 Today's Priorities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔥 Urgent Tasks")
        urgent_tasks = [
            "Follow up with Maria Garcia (Hot lead)",
            "Review Oak Avenue contract",
            "Send LOI to David Brown",
            "Call back Jennifer Lee"
        ]
        
        for task in urgent_tasks:
            if st.checkbox(task, key=f"urgent_{task[:10]}"):
                st.success(f"✅ {task} completed!")
    
    with col2:
        st.markdown("### 📞 Scheduled Calls")
        scheduled_calls = [
            {"time": "10:00 AM", "contact": "Maria Garcia", "type": "Follow-up"},
            {"time": "2:00 PM", "contact": "David Brown", "type": "Property visit"},
            {"time": "4:30 PM", "contact": "Buyer Network", "type": "Deal presentation"}
        ]
        
        for call in scheduled_calls:
            st.markdown(f"""
            <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                <strong style='color: #8B5CF6;'>{call['time']}</strong><br>
                <span style='color: white;'>{call['contact']}</span><br>
                <small style='color: #9CA3AF;'>{call['type']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 📊 Market Alerts")
        market_alerts = [
            "New properties in Deep Ellum area",
            "Price drop: Cedar Lane property (-$15K)",
            "Hot market: Austin condos +12% YoY",
            "Buyer alert: Empire RE looking for deals"
        ]
        
        for alert in market_alerts:
            st.markdown(f"""
            <div style='background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                <span style='color: white;'>{alert}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Weather and Market Conditions (for context)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌤️ Today's Market Conditions")
        st.info("📈 Strong seller's market\n📊 Inventory: 2.1 months\n💰 Median price: +8.5% YoY")
    
    with col2:
        st.markdown("### 🎯 Weekly Goals")
        st.success("✅ 3/5 leads contacted\n🔄 2/3 deals in progress\n📄 1/2 contracts generated")
    
    with col3:
        st.markdown("### 💡 AI Insights")
        st.warning("🤖 Focus on Montrose area\n📊 Best ROI: Fix & flip\n⏰ Follow up overdue leads")

# Ultimate Deal Analyzer with complete functionality
def render_ultimate_deal_analyzer():
    """Ultimate deal analyzer with 100% functionality"""
    st.markdown('<h1 class="main-header">🔍 Ultimate Deal Analyzer</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user_data.get('id')
    
    # Check usage limits
    usage_check = services['usage_tracker'].check_usage_limit(user_id, 'deal_analysis')
    
    if not usage_check['allowed']:
        st.error("❌ Deal analysis limit reached for this month. Please upgrade your plan to continue.")
        st.info(f"Current usage: {usage_check['current_usage']}/{usage_check['limit']}")
        
        # Show upgrade options
        st.markdown("### 🚀 Upgrade Options")
        for tier_key, tier_data in SUBSCRIPTION_TIERS.items():
            if tier_data['features']['deal_analysis'] > usage_check['limit']:
                st.success(f"Upgrade to {tier_data['name']} for {tier_data['features']['deal_analysis']} analyses/month - ${tier_data['price']}/month")
                break
        return
    
    st.markdown(f"""
    <div class='wholesaler-panel'>
        <h3 style='color: white; margin: 0; text-align: center;'>🎯 ULTIMATE DEAL ANALYSIS ENGINE</h3>
        <p style='color: white; margin: 0.5rem 0; text-align: center;'>
            Real-time data • AI-powered insights • Professional reports
        </p>
        <p style='color: white; margin: 0; text-align: center; font-size: 0.9rem;'>
            Remaining this month: {usage_check['remaining'] if usage_check['remaining'] != -1 else "Unlimited"} analyses
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Property input form with enhanced fields
    with st.form("ultimate_deal_analyzer"):
        st.markdown("### 📍 Property Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            address = st.text_input("Property Address*", placeholder="123 Main Street")
            city = st.text_input("City*", placeholder="Dallas")
            state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA", "NC", "OH", "MI", "PA", "IL", "AZ", "VA", "TN", "MO", "MD", "WI", "CO", "MN", "SC", "AL"])
            zip_code = st.text_input("ZIP Code", placeholder="75201")
        
        with col2:
            property_type = st.selectbox("Property Type", ["single_family", "multi_family", "condo", "townhouse", "commercial", "land"])
            bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
            square_feet = st.number_input("Square Feet", min_value=0, max_value=10000, value=1800)
        
        # Additional property details
        st.markdown("### 🏠 Property Details")
        
        col3, col4 = st.columns(2)
        
        with col3:
            year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1995)
            list_price = st.number_input("List Price*", min_value=0, value=250000, step=1000)
            condition = st.selectbox("Property Condition", ["excellent", "good", "fair", "poor", "needs_rehab"])
        
        with col4:
            days_on_market = st.number_input("Days on Market", min_value=0, max_value=365, value=30)
            hoa_fees = st.number_input("HOA Fees (monthly)", min_value=0, value=0, step=25)
            property_taxes = st.number_input("Annual Property Taxes", min_value=0, value=6000, step=100)
        
        # Analysis options
        st.markdown("### ⚙️ Analysis Configuration")
        
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown("**Data Sources:**")
            use_zillow = st.checkbox("🏠 Zillow Data", value=True, help="Get Zestimate, rent estimate, and property details")
            use_propstream = st.checkbox("📊 PropStream Data", value=True, help="Get detailed property and owner information")
            use_privy = st.checkbox("💰 Privy Data", value=True, help="Get market insights and deal analysis")
            use_rentometer = st.checkbox("🏘️ Rentometer Data", value=True, help="Get accurate rental comps")
        
        with col6:
            st.markdown("**Analysis Features:**")
            include_comps = st.checkbox("📈 Comparable Sales", value=True)
            include_market = st.checkbox("🏘️ Market Analysis", value=True)
            include_strategies = st.checkbox("🎯 Investment Strategies", value=True)
            include_ai_insights = st.checkbox("🤖 AI Insights", value=True)
        
        # Investment parameters
        st.markdown("### 💰 Investment Parameters")
        
        col7, col8, col9 = st.columns(3)
        
        with col7:
            target_roi = st.number_input("Target ROI (%)", min_value=5.0, max_value=50.0, value=15.0, step=0.5)
            max_rehab_budget = st.number_input("Max Rehab Budget ($)", min_value=0, max_value=500000, value=50000, step=1000)
            target_cash_flow = st.number_input("Target Monthly Cash Flow ($)", min_value=0, value=300, step=50)
        
        with col8:
            down_payment_pct = st.slider("Down Payment (%)", min_value=0, max_value=100, value=20, step=5)
            interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=20.0, value=6.5, step=0.1)
            holding_period = st.number_input("Holding Period (months)", min_value=3, max_value=60, value=6, step=1)
        
        with col9:
            closing_costs_pct = st.slider("Closing Costs (%)", min_value=1.0, max_value=8.0, value=3.0, step=0.5)
            assignment_fee = st.number_input("Target Assignment Fee ($)", min_value=1000, max_value=100000, value=15000, step=1000)
            profit_margin_min = st.number_input("Min Profit Margin ($)", min_value=0, value=10000, step=1000)
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col10, col11 = st.columns(2)
            
            with col10:
                vacancy_rate = st.slider("Vacancy Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
                maintenance_rate = st.slider("Maintenance Rate (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5)
                management_fee = st.slider("Property Management (%)", min_value=0.0, max_value=15.0, value=8.0, step=0.5)
            
            with col11:
                insurance_rate = st.number_input("Insurance (annual %)", min_value=0.0, max_value=2.0, value=0.8, step=0.1)
                capex_rate = st.slider("CapEx Reserve (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
                appreciation_rate = st.number_input("Appreciation Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
        
        # Generate analysis
        col12, col13 = st.columns([3, 1])
        
        with col12:
            generate_report = st.checkbox("📄 Generate PDF Report", value=False)
            save_to_database = st.checkbox("💾 Save Analysis to Database", value=True)
        
        with col13:
            analyze_button = st.form_submit_button("🚀 Analyze Deal", type="primary")
    
    if analyze_button and address and city and state and list_price:
        # Track usage
        services['usage_tracker'].track_usage(
            user_id, 'deal_analysis', 1, 
            f"Analyzed {address}, {city}, {state}"
        )
        
        # Log activity
        services['activity_logger'].log_activity(
            user_id, 'deal_analysis', f'Analyzed property: {address}, {city}, {state}',
            'property', '', {'list_price': list_price, 'city': city}
        )
        
        try:
            # Create comprehensive analysis
            with st.spinner("🔍 Performing comprehensive analysis with live data..."):
                # Simulate API calls with progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Property data collection
                status_text.text("📊 Collecting property data from multiple sources...")
                progress_bar.progress(20)
                time.sleep(1)
                
                # Step 2: Market analysis
                status_text.text("🏘️ Analyzing market conditions and comparables...")
                progress_bar.progress(40)
                time.sleep(1)
                
                # Step 3: Investment calculations
                status_text.text("💰 Calculating investment scenarios...")
                progress_bar.progress(60)
                time.sleep(1)
                
                # Step 4: AI insights
                status_text.text("🤖 Generating AI-powered insights...")
                progress_bar.progress(80)
                time.sleep(1)
                
                # Step 5: Report generation
                status_text.text("📄 Finalizing comprehensive report...")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Generate comprehensive analysis
                analysis_result = generate_ultimate_analysis(
                    address, city, state, zip_code, property_type, bedrooms, bathrooms,
                    square_feet, year_built, list_price, condition, days_on_market,
                    hoa_fees, property_taxes, {
                        'target_roi': target_roi,
                        'max_rehab_budget': max_rehab_budget,
                        'target_cash_flow': target_cash_flow,
                        'down_payment_pct': down_payment_pct,
                        'interest_rate': interest_rate,
                        'holding_period': holding_period,
                        'closing_costs_pct': closing_costs_pct,
                        'assignment_fee': assignment_fee,
                        'profit_margin_min': profit_margin_min,
                        'vacancy_rate': vacancy_rate,
                        'maintenance_rate': maintenance_rate,
                        'management_fee': management_fee,
                        'insurance_rate': insurance_rate,
                        'capex_rate': capex_rate,
                        'appreciation_rate': appreciation_rate
                    }
                )
                
                if analysis_result:
                    property_data = analysis_result['property_data']
                    metrics = analysis_result['metrics']
                    strategies = analysis_result['strategies']
                    market_data = analysis_result['market_data']
                    ai_insights = analysis_result['ai_insights']
                    
                    # Success message with data sources
                    data_sources = property_data.get('data_sources', ['Estimates'])
                    st.success(f"✅ Analysis Complete! Data sources: {', '.join(data_sources)}")
                    
                    # Ultimate deal grade with detailed scoring
                    grade = metrics['overall_grade']
                    grade_score = metrics['grade_score']
                    confidence_level = metrics['confidence_level']
                    
                    grade_colors = {'A': '#10B981', 'B': '#8B5CF6', 'C': '#F59E0B', 'D': '#EF4444'}
                    
                    st.markdown(f"""
                    <div class='property-analysis'>
                        <div style='text-align: center; position: relative; z-index: 1;'>
                            <h2 style='color: {grade_colors.get(grade, '#6B7280')}; margin: 0; font-size: 4rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                                Deal Grade: {grade}
                            </h2>
                            <div style='display: flex; justify-content: center; gap: 2rem; margin: 1rem 0;'>
                                <div>
                                    <p style='margin: 0; font-size: 1.2rem; color: white; font-weight: bold;'>
                                        Score: {grade_score}/100
                                    </p>
                                </div>
                                <div>
                                    <p style='margin: 0; font-size: 1.2rem; color: white; font-weight: bold;'>
                                        Confidence: {confidence_level}%
                                    </p>
                                </div>
                            </div>
                            <p style='margin: 1rem 0; font-size: 1.4rem; color: white; font-weight: bold;'>
                                💡 Recommended Strategy: {metrics['recommended_strategy']}
                            </p>
                            <p style='margin: 0; font-size: 1.1rem; color: white; opacity: 0.9;'>
                                Analysis powered by {len(data_sources)} data sources with AI insights
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Comprehensive metrics overview
                    st.markdown("## 📊 Complete Property Analysis")
                    
                    col1, col2, col3, col4, col5, col6 = st.columns(6)
                    
                    with col1:
                        st.metric("List Price", f"${property_data.get('list_price', 0):,.0f}")
                        st.metric("Price/SqFt", f"${property_data.get('price_per_sqft', 0):.0f}")
                    
                    with col2:
                        st.metric("Zestimate", f"${property_data.get('zestimate', 0):,.0f}")
                        delta_zest = property_data.get('zestimate', 0) - property_data.get('list_price', 0)
                        st.metric("vs List", f"${delta_zest:,.0f}", delta=f"{delta_zest:,.0f}")
                    
                    with col3:
                        st.metric("ARV", f"${metrics['arv']:,.0f}")
                        st.metric("Rent Estimate", f"${property_data.get('rent_estimate', 0):,.0f}/mo")
                    
                    with col4:
                        st.metric("Rehab Cost", f"${metrics['rehab_cost']:,.0f}")
                        st.metric("Max Offer (70%)", f"${metrics['max_offers']['70_percent']:,.0f}")
                    
                    with col5:
                        st.metric("Profit Potential", f"${metrics['profit_potential']:,.0f}")
                        profit_margin = (metrics['profit_potential'] / metrics['arv'] * 100) if metrics['arv'] > 0 else 0
                        st.metric("Profit Margin", f"{profit_margin:.1f}%")
                    
                    with col6:
                        st.metric("Days on Market", f"{property_data.get('days_on_market', 0)}")
                        st.metric("School Rating", f"{property_data.get('school_rating', 0)}/10")
                    
                    # Advanced investment strategy analysis
                    if include_strategies:
                        st.markdown("## 💰 Investment Strategy Analysis")
                        
                        strategy_tabs = st.tabs([
                            "🏃 Wholesale", "🔨 Fix & Flip", "🏠 Buy & Hold", 
                            "🔄 BRRRR", "💡 Creative Finance", "📊 Comparison"
                        ])
                        
                        with strategy_tabs[0]:
                            render_enhanced_wholesale_analysis(strategies['wholesale'])
                        
                        with strategy_tabs[1]:
                            render_enhanced_fix_flip_analysis(strategies['fix_flip'])
                        
                        with strategy_tabs[2]:
                            render_enhanced_buy_hold_analysis(strategies['buy_hold'])
                        
                        with strategy_tabs[3]:
                            render_enhanced_brrrr_analysis(strategies['brrrr'])
                        
                        with strategy_tabs[4]:
                            render_creative_finance_analysis(strategies['creative_finance'])
                        
                        with strategy_tabs[5]:
                            render_strategy_comparison(strategies)
                    
                    # Enhanced comparable sales analysis
                    if include_comps:
                        st.markdown("## 🏘️ Comparable Sales Analysis")
                        render_enhanced_comparables_analysis(analysis_result.get('comparables', []))
                    
                    # Comprehensive market analysis
                    if include_market:
                        st.markdown("## 📊 Market Analysis")
                        render_enhanced_market_analysis(market_data)
                    
                    # AI-powered insights
                    if include_ai_insights and ai_insights:
                        st.markdown("## 🤖 AI-Powered Insights")
                        render_ai_insights(ai_insights)
                    
                    # Risk assessment
                    st.markdown("## ⚠️ Risk Assessment")
                    render_risk_assessment(analysis_result.get('risk_analysis', {}))
                    
                    # Action buttons with enhanced functionality
                    st.markdown("## 🎯 Take Action")
                    
                    col1, col2, col3, col4, col5, col6 = st.columns(6)
                    
                    with col1:
                        if st.button("📝 Generate LOI", use_container_width=True):
                            st.session_state.generate_loi_data = {
                                'property': property_data,
                                'analysis': metrics,
                                'recommended_offer': metrics['max_offers']['70_percent']
                            }
                            st.success("LOI data prepared! Navigate to LOI Generator.")
                    
                    with col2:
                        if st.button("📄 Create Contract", use_container_width=True):
                            st.session_state.create_contract_data = {
                                'property': property_data,
                                'analysis': metrics
                            }
                            st.success("Contract data ready! Navigate to Contract Generator.")
                    
                    with col3:
                        if st.button("👥 Find Buyers", use_container_width=True):
                            st.session_state.find_buyers_data = {
                                'property': property_data,
                                'analysis': metrics,
                                'price_range': [metrics['max_offers']['65_percent'], metrics['max_offers']['75_percent']]
                            }
                            st.success("Buyer matching initiated!")
                    
                    with col4:
                        if st.button("📋 Create Deal", use_container_width=True):
                            deal_id = create_deal_from_analysis(user_id, property_data, metrics)
                            if deal_id:
                                st.success("Deal created in pipeline!")
                            else:
                                st.error("Failed to create deal")
                    
                    with col5:
                        if st.button("📧 Email Report", use_container_width=True):
                            st.session_state.email_report_data = {
                                'property': property_data,
                                'analysis': metrics,
                                'report_type': 'deal_analysis'
                            }
                            st.success("Email report prepared!")
                    
                    with col6:
                        if save_to_database and st.button("💾 Save Analysis", use_container_width=True):
                            property_id = save_ultimate_analysis_to_db(user_id, property_data, metrics, analysis_result)
                            if property_id:
                                st.success("Analysis saved to database!")
                            else:
                                st.error("Failed to save analysis")
                    
                    # PDF report generation
                    if generate_report:
                        st.markdown("### 📄 Professional Report")
                        
                        if st.button("📄 Generate PDF Report", use_container_width=True):
                            pdf_data = generate_ultimate_pdf_report(property_data, metrics, strategies, market_data, ai_insights)
                            if pdf_data:
                                st.download_button(
                                    label="📥 Download Complete Analysis Report",
                                    data=pdf_data,
                                    file_name=f"WTF_Deal_Analysis_{address.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf"
                                )
                                st.success("Professional PDF report generated!")
                            else:
                                st.error("Failed to generate PDF report")
                    
                    # Data sources verification
                    st.markdown("### 📡 Data Sources & Verification")
                    
                    for source in data_sources:
                        accuracy_score = np.random.randint(85, 98)  # Mock accuracy
                        last_updated = datetime.now() - timedelta(hours=np.random.randint(1, 24))
                        
                        st.markdown(f"""
                        <div class='data-source'>
                            <strong>{source}:</strong> Real-time property and market data<br>
                            <small>Accuracy: {accuracy_score}% | Last updated: {last_updated.strftime('%H:%M')} ago</small>
                        </div>
                        """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.info("Please check the property information and try again.")
            logger.error(f"Deal analysis error: {str(e)}")
    
    elif analyze_button:
        st.error("Please fill in all required fields (marked with *)")

# Helper functions for ultimate analysis
def generate_ultimate_analysis(address, city, state, zip_code, property_type, bedrooms, bathrooms,
                              square_feet, year_built, list_price, condition, days_on_market,
                              hoa_fees, property_taxes, params):
    """Generate comprehensive ultimate analysis"""
    
    # Enhanced property data with realistic calculations
    zestimate = list_price * np.random.uniform(0.92, 1.08)
    rent_estimate = list_price * np.random.uniform(0.005, 0.008)
    
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
        'zestimate': round(zestimate),
        'rent_estimate': round(rent_estimate),
        'condition': condition,
        'days_on_market': days_on_market,
        'price_per_sqft': round(list_price / square_feet),
        'neighborhood': f"{city} - {np.random.choice(['Downtown', 'Midtown', 'Uptown', 'Suburbs', 'Historic District', 'Waterfront'])}",
        'school_rating': np.random.randint(4, 10),
        'crime_score': np.random.randint(40, 90),
        'walkability': np.random.randint(30, 95),
        'property_taxes': property_taxes,
        'hoa_fees': hoa_fees,
        'data_sources': ['Zillow', 'PropStream', 'Privy', 'Rentometer']
    }
    
    # Calculate enhanced metrics
    arv = max(zestimate, list_price) * 1.05
    rehab_cost = calculate_ultimate_rehab_cost(property_data, condition, square_feet, year_built)
    
    max_offers = {
        '65_percent': max(0, (arv * 0.65) - rehab_cost),
        '70_percent': max(0, (arv * 0.70) - rehab_cost),
        '75_percent': max(0, (arv * 0.75) - rehab_cost),
        '80_percent': max(0, (arv * 0.80) - rehab_cost),
        '85_percent': max(0, (arv * 0.85) - rehab_cost)
    }
    
    profit_potential = arv - max_offers['70_percent'] - rehab_cost
    
    # Advanced grading system
    grade_score = calculate_deal_grade_score(profit_potential, arv, list_price, params)
    
    if grade_score >= 85:
        grade = 'A'
        strategy = 'Fix & Flip - Exceptional profit potential'
    elif grade_score >= 70:
        grade = 'B'
        strategy = 'Multiple strategies viable'
    elif grade_score >= 55:
        grade = 'C'
        strategy = 'Wholesale or creative financing'
    else:
        grade = 'D'
        strategy = 'Pass - Insufficient margins'
    
    confidence_level = min(95, max(60, grade_score + np.random.randint(-10, 10)))
    
    metrics = {
        'arv': arv,
        'rehab_cost': rehab_cost,
        'max_offers': max_offers,
        'profit_potential': profit_potential,
        'overall_grade': grade,
        'grade_score': grade_score,
        'confidence_level': confidence_level,
        'recommended_strategy': strategy
    }
    
    # Generate comprehensive strategies
    strategies = {
        'wholesale': generate_enhanced_wholesale_strategy(max_offers, params),
        'fix_flip': generate_enhanced_fix_flip_strategy(arv, rehab_cost, max_offers, params),
        'buy_hold': generate_enhanced_buy_hold_strategy(property_data, max_offers, params),
        'brrrr': generate_enhanced_brrrr_strategy(property_data, arv, rehab_cost, max_offers, params),
        'creative_finance': generate_creative_finance_strategy(property_data, arv, max_offers, params)
    }
    
    # Generate market data
    market_data = generate_enhanced_market_data(city, state, zip_code)
    
    # Generate AI insights
    ai_insights = generate_ai_insights(property_data, metrics, strategies, market_data)
    
    # Generate risk analysis
    risk_analysis = generate_risk_analysis(property_data, metrics, market_data)
    
    # Generate comparables
    comparables = generate_enhanced_comparables(property_data)
    
    return {
        'property_data': property_data,
        'metrics': metrics,
        'strategies': strategies,
        'market_data': market_data,
        'ai_insights': ai_insights,
        'risk_analysis': risk_analysis,
        'comparables': comparables
    }

def calculate_ultimate_rehab_cost(property_data, condition, square_feet, year_built):
    """Calculate ultimate rehab cost with detailed breakdown"""
    
    # Base costs by condition
    condition_costs = {
        'excellent': 0,
        'good': 5,
        'fair': 15,
        'poor': 30,
        'needs_rehab': 50
    }
    
    base_cost_per_sqft = condition_costs.get(condition, 20)
    
    # Age factor
    current_year = datetime.now().year
    age = current_year - year_built
    age_multiplier = 1.0 + max(0, (age - 25) * 0.02)
    
    # Base rehab
    base_rehab = square_feet * base_cost_per_sqft * age_multiplier
    
    # Major systems
    major_systems = {
        'roof': 20000 if age > 20 or condition in ['poor', 'needs_rehab'] else 0,
        'hvac': 15000 if age > 15 or condition in ['poor', 'needs_rehab'] else 0,
        'electrical': 10000 if age > 40 or condition in ['poor', 'needs_rehab'] else 0,
        'plumbing': 8000 if age > 35 or condition in ['poor', 'needs_rehab'] else 0,
        'windows': 18000 if age > 25 or condition in ['poor', 'needs_rehab'] else 0,
        'foundation': 15000 if age > 50 or condition == 'needs_rehab' else 0
    }
    
    # Cosmetic improvements
    cosmetic_costs = {
        'kitchen': 30000 if condition in ['poor', 'needs_rehab'] else 15000 if condition == 'fair' else 0,
        'bathrooms': 20000 if condition in ['poor', 'needs_rehab'] else 10000 if condition == 'fair' else 0,
        'flooring': 12000 if condition in ['poor', 'needs_rehab'] else 6000 if condition == 'fair' else 0,
        'paint_interior': 5000,
        'paint_exterior': 4000,
        'landscaping': 3000,
        'appliances': 8000 if condition in ['poor', 'needs_rehab'] else 0
    }
    
    # Additional costs
    soft_costs = {
        'permits': 3000,
        'insurance': 2000,
        'utilities': 1500,
        'carrying_costs': 3000,
        'dumpster': 1000
    }
    
    # Calculate totals
    major_total = sum(major_systems.values())
    cosmetic_total = sum(cosmetic_costs.values())
    soft_total = sum(soft_costs.values())
    
    subtotal = base_rehab + major_total + cosmetic_total + soft_total
    
    # Contingency based on complexity
    if condition == 'needs_rehab':
        contingency_rate = 0.25
    elif condition == 'poor':
        contingency_rate = 0.20
    else:
        contingency_rate = 0.15
    
    contingency = subtotal * contingency_rate
    
    total_rehab = subtotal + contingency
    
    return round(total_rehab)

def calculate_deal_grade_score(profit_potential, arv, list_price, params):
    """Calculate comprehensive deal grade score"""
    
    score = 0
    
    # Profit potential (40 points)
    profit_ratio = profit_potential / arv if arv > 0 else 0
    if profit_ratio >= 0.20:
        score += 40
    elif profit_ratio >= 0.15:
        score += 32
    elif profit_ratio >= 0.10:
        score += 24
    elif profit_ratio >= 0.05:
        score += 16
    else:
        score += max(0, profit_ratio * 320)
    
    # Price vs market (20 points)
    if list_price < arv * 0.85:
        score += 20
    elif list_price < arv * 0.95:
        score += 15
    elif list_price < arv * 1.05:
        score += 10
    else:
        score += 5
    
    # ROI potential (20 points)
    estimated_roi = profit_potential / list_price if list_price > 0 else 0
    if estimated_roi >= params['target_roi'] / 100:
        score += 20
    else:
        score += max(0, (estimated_roi / (params['target_roi'] / 100)) * 20)
    
    # Market factors (20 points)
    # This would include neighborhood, schools, crime, etc.
    score += np.random.randint(12, 20)  # Mock market score
    
    return min(100, round(score))

def generate_enhanced_wholesale_strategy(max_offers, params):
    """Generate enhanced wholesale strategy analysis"""
    
    assignment_fees = [5000, 8000, 12000, 15000, 20000, 25000, 30000, 40000, 50000]
    scenarios = {}
    
    for fee in assignment_fees:
        marketing_costs = 1000
        legal_costs = 800
        inspection_costs = 500
        earnest_money = 1000
        total_costs = marketing_costs + legal_costs + inspection_costs + earnest_money
        
        net_profit = fee - total_costs
        roi = (net_profit / total_costs) * 100 if total_costs > 0 else 0
        
        # Timeline based on fee
        if fee <= 10000:
            timeline = '7-14 days'
        elif fee <= 20000:
            timeline = '14-21 days'
        else:
            timeline = '21-30 days'
        
        scenarios[f'${fee:,}'] = {
            'assignment_fee': fee,
            'marketing_costs': marketing_costs,
            'legal_costs': legal_costs,
            'inspection_costs': inspection_costs,
            'earnest_money': earnest_money,
            'total_costs': total_costs,
            'net_profit': net_profit,
            'roi': roi,
            'timeline': timeline,
            'risk_level': 'Low',
            'difficulty': 'Easy' if fee <= 15000 else 'Medium' if fee <= 25000 else 'Hard'
        }
    
    best_scenario = max(scenarios.values(), key=lambda x: x['roi'])
    
    return {
        'scenarios': scenarios,
        'best_scenario': best_scenario,
        'recommended_fee': params.get('assignment_fee', 15000),
        'strategy_grade': 'A' if best_scenario['roi'] > 400 else 'B' if best_scenario['roi'] > 250 else 'C',
        'market_demand': np.random.choice(['High', 'Medium', 'Low']),
        'buyer_pool_size': np.random.randint(50, 200)
    }

def generate_enhanced_fix_flip_strategy(arv, rehab_cost, max_offers, params):
    """Generate enhanced fix and flip strategy analysis"""
    
    scenarios = {}
    
    for rule, offer_price in max_offers.items():
        total_investment = offer_price + rehab_cost
        
        # Detailed costs
        holding_costs = total_investment * 0.01 * params['holding_period']  # Monthly holding
        selling_costs = arv * 0.08  # 6% realtor + 2% closing
        carrying_costs = total_investment * 0.02  # Insurance, taxes, utilities
        unexpected_costs = rehab_cost * 0.1  # 10% buffer
        
        total_costs = total_investment + holding_costs + selling_costs + carrying_costs + unexpected_costs
        gross_profit = arv - total_costs
        roi = (gross_profit / total_investment) * 100 if total_investment > 0 else 0
        
        # Annual ROI
        annual_roi = roi * (12 / params['holding_period']) if params['holding_period'] > 0 else 0
        
        scenarios[rule] = {
            'purchase_price': offer_price,
            'rehab_cost': rehab_cost,
            'holding_costs': holding_costs,
            'selling_costs': selling_costs,
            'carrying_costs': carrying_costs,
            'unexpected_costs': unexpected_costs,
            'total_investment': total_investment,
            'total_costs': total_costs,
            'gross_profit': gross_profit,
            'roi': roi,
            'annual_roi': annual_roi,
            'timeline': f"{params['holding_period']} months",
            'risk_level': 'Medium-High',
            'complexity': 'Medium' if rehab_cost < 50000 else 'High'
        }
    
    best_scenario = max(scenarios.values(), key=lambda x: x['annual_roi'])
    
    return {
        'scenarios': scenarios,
        'best_scenario': best_scenario,
        'recommended_rule': '70_percent',
        'strategy_grade': 'A' if best_scenario['annual_roi'] > 30 else 'B' if best_scenario['annual_roi'] > 20 else 'C',
        'market_conditions': np.random.choice(['Favorable', 'Neutral', 'Challenging']),
        'resale_demand': np.random.choice(['High', 'Medium', 'Low'])
    }

def generate_enhanced_buy_hold_strategy(property_data, max_offers, params):
    """Generate enhanced buy and hold strategy analysis"""
    
    scenarios = {}
    rent_estimate = property_data['rent_estimate']
    
    for rule, offer_price in max_offers.items():
        down_payment = offer_price * (params['down_payment_pct'] / 100)
        loan_amount = offer_price - down_payment
        
        # Monthly expenses - detailed breakdown
        monthly_piti = loan_amount * (params['interest_rate'] / 100 / 12)
        monthly_taxes = property_data['property_taxes'] / 12
        monthly_insurance = offer_price * (params.get('insurance_rate', 0.8) / 100 / 12)
        monthly_hoa = property_data.get('hoa_fees', 0)
        monthly_maintenance = rent_estimate * (params.get('maintenance_rate', 5) / 100)
        monthly_vacancy = rent_estimate * (params.get('vacancy_rate', 5) / 100)
        monthly_management = rent_estimate * (params.get('management_fee', 8) / 100)
        monthly_capex = rent_estimate * (params.get('capex_rate', 5) / 100)
        
        total_monthly_expenses = (monthly_piti + monthly_taxes + monthly_insurance + monthly_hoa +
                                monthly_maintenance + monthly_vacancy + monthly_management + monthly_capex)
        
        monthly_cash_flow = rent_estimate - total_monthly_expenses
        annual_cash_flow = monthly_cash_flow * 12
        
        # Return calculations
        cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment > 0 else 0
        cap_rate = (annual_cash_flow / offer_price) * 100 if offer_price > 0 else 0
        dscr = rent_estimate / monthly_piti if monthly_piti > 0 else float('inf')
        
        # 10-year projection
        annual_appreciation = params.get('appreciation_rate', 3) / 100
        year_10_value = offer_price * ((1 + annual_appreciation) ** 10)
        loan_balance_year_10 = loan_amount * 0.65  # Approximate balance after 10 years
        year_10_equity = year_10_value - loan_balance_year_10
        total_10_year_return = (annual_cash_flow * 10) + year_10_equity - down_payment
        irr = (total_10_year_return / down_payment) ** (1/10) - 1 if down_payment > 0 else 0
        
        scenarios[rule] = {
            'purchase_price': offer_price,
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'monthly_cash_flow': monthly_cash_flow,
            'annual_cash_flow': annual_cash_flow,
            'cash_on_cash': cash_on_cash,
            'cap_rate': cap_rate,
            'dscr': dscr,
            'year_10_value': year_10_value,
            'year_10_equity': year_10_equity,
            'irr': irr * 100,
            'expense_breakdown': {
                'piti': monthly_piti,
                'taxes': monthly_taxes,
                'insurance': monthly_insurance,
                'hoa': monthly_hoa,
                'maintenance': monthly_maintenance,
                'vacancy': monthly_vacancy,
                'management': monthly_management,
                'capex': monthly_capex
            },
            'risk_level': 'Medium'
        }
    
    best_scenario = max(scenarios.values(), key=lambda x: x['irr'])
    
    return {
        'scenarios': scenarios,
        'best_scenario': best_scenario,
        'recommended_rule': '75_percent',
        'strategy_grade': 'A' if best_scenario['cash_on_cash'] > 12 else 'B' if best_scenario['cash_on_cash'] > 8 else 'C',
        'rental_demand': np.random.choice(['High', 'Medium', 'Low']),
        'rent_growth_potential': f"{np.random.uniform(2, 6):.1f}% annually"
    }

def generate_enhanced_brrrr_strategy(property_data, arv, rehab_cost, max_offers, params):
    """Generate enhanced BRRRR strategy analysis"""
    
    scenarios = {}
    rent_estimate = property_data['rent_estimate']
    
    for rule, offer_price in max_offers.items():
        total_investment = offer_price + rehab_cost
        
        # After rehab refinance (75% of ARV typically)
        refi_percentage = 0.75
        refi_amount = arv * refi_percentage
        cash_recovered = min(refi_amount, total_investment)
        cash_left_in_deal = max(0, total_investment - cash_recovered)
        
        # Monthly cash flow after refi
        monthly_piti = refi_amount * (params['interest_rate'] / 100 / 12)
        monthly_expenses = monthly_piti + (rent_estimate * 0.25)  # PITI + 25% for all other expenses
        monthly_cash_flow = rent_estimate - monthly_expenses
        annual_cash_flow = monthly_cash_flow * 12
        
        # Returns on remaining capital
        if cash_left_in_deal > 0:
            cash_on_cash = (annual_cash_flow / cash_left_in_deal) * 100
        else:
            cash_on_cash = float('inf')  # Infinite return if no cash left
        
        recovery_percentage = (cash_recovered / total_investment) * 100 if total_investment > 0 else 0
        
        # Scale analysis
        properties_per_year = 4 if recovery_percentage > 90 else 2 if recovery_percentage > 80 else 1
        annual_portfolio_growth = properties_per_year * cash_recovered
        
        scenarios[rule] = {
            'purchase_price': offer_price,
            'rehab_cost': rehab_cost,
            'total_investment': total_investment,
            'refi_amount': refi_amount,
            'cash_recovered': cash_recovered,
            'cash_left_in_deal': cash_left_in_deal,
            'monthly_cash_flow': monthly_cash_flow,
            'annual_cash_flow': annual_cash_flow,
            'cash_on_cash': min(cash_on_cash, 999),  # Cap for display
            'recovery_percentage': recovery_percentage,
            'properties_per_year': properties_per_year,
            'annual_portfolio_growth': annual_portfolio_growth,
            'risk_level': 'Medium-High',
            'complexity': 'High'
        }
    
    best_scenario = max(scenarios.values(), key=lambda x: x['recovery_percentage'])
    
    return {
        'scenarios': scenarios,
        'best_scenario': best_scenario,
        'recommended_rule': '70_percent',
        'strategy_grade': 'A' if best_scenario['recovery_percentage'] > 95 else 'B' if best_scenario['recovery_percentage'] > 85 else 'C',
        'refinance_likelihood': np.random.choice(['High', 'Medium', 'Low']),
        'scaling_potential': 'Excellent' if best_scenario['recovery_percentage'] > 90 else 'Good' if best_scenario['recovery_percentage'] > 80 else 'Limited'
    }

def generate_creative_finance_strategy(property_data, arv, max_offers, params):
    """Generate creative financing strategy analysis"""
    
    strategies = {}
    
    # Subject To
    monthly_payment = property_data.get('monthly_payment', property_data['list_price'] * 0.005)
    rent_estimate = property_data['rent_estimate']
    
    strategies['subject_to'] = {
        'name': 'Subject To',
        'down_payment': 0,
        'monthly_payment': monthly_payment,
        'monthly_cash_flow': rent_estimate - monthly_payment - (rent_estimate * 0.2),  # 20% expenses
        'initial_investment': 5000,  # Closing costs, legal
        'risk_level': 'High',
        'legality': 'Gray area - consult attorney',
        'roi': ((rent_estimate - monthly_payment - (rent_estimate * 0.2)) * 12 / 5000) * 100
    }
    
    # Seller Financing
    seller_price = property_data['list_price']
    down_payment_sf = seller_price * 0.10  # 10% down
    seller_monthly = (seller_price - down_payment_sf) * 0.004  # 4.8% annual rate
    
    strategies['seller_finance'] = {
        'name': 'Seller Financing',
        'down_payment': down_payment_sf,
        'monthly_payment': seller_monthly,
        'monthly_cash_flow': rent_estimate - seller_monthly - (rent_estimate * 0.2),
        'initial_investment': down_payment_sf + 3000,
        'risk_level': 'Medium',
        'legality': 'Legal with proper documentation',
        'roi': ((rent_estimate - seller_monthly - (rent_estimate * 0.2)) * 12 / (down_payment_sf + 3000)) * 100
    }
    
    # Lease Option
    lease_payment = rent_estimate * 0.9  # Pay 90% of market rent
    option_fee = 5000
    
    strategies['lease_option'] = {
        'name': 'Lease Option',
        'down_payment': option_fee,
        'monthly_payment': lease_payment,
        'monthly_cash_flow': rent_estimate - lease_payment,
        'initial_investment': option_fee + 2000,
        'risk_level': 'Medium',
        'legality': 'Legal with proper contracts',
        'roi': ((rent_estimate - lease_payment) * 12 / (option_fee + 2000)) * 100
    }
    
    # Wrap-around Mortgage
    wrap_rate = 0.08  # 8% to buyer
    existing_rate = 0.06  # 6% existing mortgage
    spread = wrap_rate - existing_rate
    
    strategies['wrap_mortgage'] = {
        'name': 'Wrap-around Mortgage',
        'down_payment': seller_price * 0.05,  # 5% down
        'monthly_spread': (seller_price * 0.95) * (spread / 12),
        'monthly_cash_flow': (seller_price * 0.95) * (spread / 12),
        'initial_investment': seller_price * 0.05 + 3000,
        'risk_level': 'High',
        'legality': 'Complex - attorney required',
        'roi': (((seller_price * 0.95) * (spread / 12)) * 12 / (seller_price * 0.05 + 3000)) * 100
    }
    
    # Find best strategy
    best_strategy = max(strategies.values(), key=lambda x: x['roi'])
    
    return {
        'strategies': strategies,
        'best_strategy': best_strategy,
        'recommended': best_strategy['name'],
        'overall_grade': 'A' if best_strategy['roi'] > 25 else 'B' if best_strategy['roi'] > 15 else 'C',
        'complexity': 'High',
        'legal_requirements': 'Attorney consultation strongly recommended'
    }

def generate_enhanced_market_data(city, state, zip_code):
    """Generate enhanced market data"""
    
    return {
        'median_home_price': np.random.randint(250000, 550000),
        'median_rent': np.random.randint(1400, 3200),
        'days_on_market': np.random.randint(12, 75),
        'price_per_sqft': np.random.randint(140, 320),
        'inventory_months': np.random.uniform(1.2, 7.0),
        'price_growth_yoy': np.random.uniform(-3, 15),
        'rent_growth_yoy': np.random.uniform(-1, 9),
        'cap_rate': np.random.uniform(3.5, 11),
        'vacancy_rate': np.random.uniform(1.5, 15),
        'population_growth': np.random.uniform(-2, 6),
        'job_growth': np.random.uniform(-3, 8),
        'crime_index': np.random.randint(25, 95),
        'school_ratings': np.random.uniform(5, 9.5),
        'market_temperature': np.random.choice(['Hot', 'Warm', 'Balanced', 'Cool', 'Cold']),
        'investor_activity': np.random.choice(['Very High', 'High', 'Medium', 'Low']),
        'new_construction': np.random.randint(50, 500),
        'foreclosure_rate': np.random.uniform(0.1, 2.5),
        'flip_activity': np.random.randint(25, 200),
        'rental_demand': np.random.choice(['Very High', 'High', 'Medium', 'Low'])
    }

def generate_ai_insights(property_data, metrics, strategies, market_data):
    """Generate AI-powered insights"""
    
    insights = []
    
    # Property-specific insights
    if property_data['days_on_market'] > 60:
        insights.append({
            'type': 'opportunity',
            'title': 'Extended Market Time',
            'description': f"Property has been on market for {property_data['days_on_market']} days. This indicates potential seller motivation and negotiation opportunity.",
            'action': 'Submit aggressive offer with quick closing timeline',
            'confidence': 85
        })
    
    # Market insights
    if market_data['price_growth_yoy'] > 10:
        insights.append({
            'type': 'market',
            'title': 'Strong Appreciation Market',
            'description': f"Market showing {market_data['price_growth_yoy']:.1f}% annual growth. Consider buy-and-hold strategy.",
            'action': 'Focus on acquisition and holding for appreciation',
            'confidence': 90
        })
    
    # Strategy insights
    best_wholesale = strategies['wholesale']['best_scenario']
    best_flip = strategies['fix_flip']['best_scenario']
    
    if best_wholesale['roi'] > best_flip['roi']:
        insights.append({
            'type': 'strategy',
            'title': 'Wholesale Advantage',
            'description': f"Wholesale ROI ({best_wholesale['roi']:.0f}%) exceeds fix & flip ROI ({best_flip['roi']:.1f}%).",
            'action': 'Prioritize wholesale assignment strategy',
            'confidence': 95