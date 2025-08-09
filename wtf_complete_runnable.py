"""
WTF (Wholesale2Flip) - Complete Runnable Platform
This is the main application file that should work immediately
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
import time
import secrets
from typing import Dict, List, Optional, Any

# Page configuration
st.set_page_config(
    page_title="WTF - Wholesale on Steroids", 
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 30%, #3B82F6 60%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #8B5CF6 0%, #10B981 30%, #3B82F6 60%, #F59E0B 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%);
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.15);
    }
    
    .success-metric {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.06) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.15);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(245, 158, 11, 0.06) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.15);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #8B5CF6 0%, #10B981 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.8rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
    }
    
    .sidebar-panel {
        background: linear-gradient(135deg, #8B5CF6 0%, #5B21B6 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        color: white;
    }
    
    .deal-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(15px);
    }
    
    .deal-card:hover {
        transform: translateY(-3px);
        border-color: #8B5CF6;
        box-shadow: 0 15px 30px rgba(139, 92, 246, 0.2);
    }
    
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'

# Mock database and services
class MockServices:
    """Mock services for demo purposes"""
    
    @staticmethod
    def authenticate(username, password):
        """Simple authentication"""
        valid_users = {
            'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Admin User'},
            'wholesaler': {'password': 'demo123', 'role': 'wholesaler', 'name': 'Demo Wholesaler'},
            'demo': {'password': 'demo', 'role': 'wholesaler', 'name': 'Demo User'}
        }
        
        if username in valid_users and valid_users[username]['password'] == password:
            return True, {
                'id': str(uuid.uuid4()),
                'username': username,
                'role': valid_users[username]['role'],
                'name': valid_users[username]['name'],
                'subscription_tier': 'pro'
            }
        return False, None
    
    @staticmethod
    def get_sample_deals():
        """Get sample deals data"""
        return [
            {
                'id': '1',
                'title': 'Elm Street Wholesale Deal',
                'address': '1234 Elm Street, Dallas, TX',
                'status': 'Under Contract',
                'profit': 15000,
                'stage': 'due_diligence'
            },
            {
                'id': '2', 
                'title': 'Oak Avenue Fix & Flip',
                'address': '5678 Oak Avenue, Houston, TX',
                'status': 'Negotiating',
                'profit': 25000,
                'stage': 'negotiating'
            },
            {
                'id': '3',
                'title': 'Pine Road Investment',
                'address': '9876 Pine Road, Austin, TX', 
                'status': 'New Lead',
                'profit': 18000,
                'stage': 'prospecting'
            }
        ]
    
    @staticmethod
    def get_sample_leads():
        """Get sample leads data"""
        return [
            {
                'name': 'Maria Garcia',
                'phone': '(555) 111-2222',
                'address': '1234 Elm Street, Dallas, TX',
                'status': 'Hot',
                'score': 92,
                'motivation': 'Divorce'
            },
            {
                'name': 'David Brown',
                'phone': '(555) 222-3333', 
                'address': '5678 Oak Avenue, Houston, TX',
                'status': 'Warm',
                'score': 78,
                'motivation': 'Job Relocation'
            },
            {
                'name': 'Jennifer Lee',
                'phone': '(555) 333-4444',
                'address': '9876 Pine Road, Austin, TX',
                'status': 'New',
                'score': 85,
                'motivation': 'Inherited Property'
            }
        ]

def render_landing_page():
    """Landing page with authentication"""
    
    st.markdown("""
    <div class='hero-section'>
        <h1 style='font-size: 4rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>WTF</h1>
        <h2 style='font-size: 2rem; margin: 0.5rem 0;'>Wholesale on Steroids</h2>
        <p style='font-size: 1.2rem; margin: 1rem 0; opacity: 0.9;'>
            The Ultimate Real Estate Wholesaling Platform
        </p>
        <p style='font-size: 1rem; opacity: 0.8;'>
            Generate contracts • Analyze deals • Manage leads • Close faster
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview
    st.markdown("## 🚀 Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #8B5CF6; text-align: center;'>🔍 Deal Analysis</h3>
            <ul style='color: white; line-height: 1.8;'>
                <li>Real-time property analysis</li>
                <li>ARV calculations</li>
                <li>Profit projections</li>
                <li>Multiple strategies</li>
                <li>AI-powered insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #10B981; text-align: center;'>📞 Lead Management</h3>
            <ul style='color: white; line-height: 1.8;'>
                <li>CRM system</li>
                <li>Lead scoring</li>
                <li>Follow-up automation</li>
                <li>Communication tracking</li>
                <li>Pipeline management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #F59E0B; text-align: center;'>📄 Documents</h3>
            <ul style='color: white; line-height: 1.8;'>
                <li>Contract generation</li>
                <li>LOI creation</li>
                <li>E-signatures</li>
                <li>Template library</li>
                <li>Legal compliance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Login section
    st.markdown("---")
    st.markdown("## 🔑 Access Platform")
    
    tab1, tab2 = st.tabs(["🔐 Login", "ℹ️ Demo Info"])
    
    with tab1:
        with st.form("login_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
            
            with col2:
                st.markdown("**Quick Access:**")
                st.info("Use 'demo' / 'demo' for instant access")
                st.info("Or 'wholesaler' / 'demo123'")
            
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
            with col2:
                demo_btn = st.form_submit_button("🎮 Try Demo", use_container_width=True)
            
            if login_btn and username and password:
                success, user_data = MockServices.authenticate(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.current_page = 'dashboard'
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            
            if demo_btn:
                success, user_data = MockServices.authenticate('demo', 'demo')
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.current_page = 'dashboard'
                    st.success("Demo access granted!")
                    st.rerun()
    
    with tab2:
        st.markdown("### 📋 Demo Credentials")
        st.markdown("""
        **Available Demo Accounts:**
        
        🎮 **Quick Demo:** `demo` / `demo`
        
        🏠 **Wholesaler:** `wholesaler` / `demo123` 
        
        👑 **Admin:** `admin` / `admin123`
        
        **Features Available:**
        - Full deal analysis
        - Lead management 
        - Contract generation
        - Analytics dashboard
        - RVM campaigns (mock)
        """)

def render_sidebar():
    """Enhanced sidebar navigation"""
    
    user_name = st.session_state.user_data.get('name', 'User')
    user_role = st.session_state.user_data.get('role', 'wholesaler')
    
    st.sidebar.markdown(f"""
    <div class='sidebar-panel'>
        <h2 style='color: white; text-align: center; margin: 0;'>🏠 WTF</h2>
        <p style='color: white; text-align: center; margin: 0; opacity: 0.9;'>Wholesale on Steroids</p>
        <hr style='border: 1px solid rgba(255,255,255,0.2); margin: 1rem 0;'>
        <p style='color: white; text-align: center; margin: 0;'>Welcome, {user_name}!</p>
        <p style='color: white; text-align: center; margin: 0; font-size: 0.9rem; opacity: 0.8;'>Role: {user_role.title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    st.sidebar.markdown("### 🧭 Navigation")
    
    pages = {
        "🏠 Dashboard": "dashboard",
        "🔍 Deal Analyzer": "deal_analyzer", 
        "📞 Lead Manager": "lead_manager",
        "📋 Deal Pipeline": "deal_pipeline",
        "📄 Contract Generator": "contract_generator",
        "📝 LOI Generator": "loi_generator",
        "📞 RVM Campaigns": "rvm_campaigns",
        "📊 Analytics": "analytics"
    }
    
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()
    
    # Quick stats
    st.sidebar.markdown("### 📈 Quick Stats")
    st.sidebar.markdown("""
    <div class='metric-card'>
        <div style='color: #8B5CF6; font-weight: bold;'>📋 Active Deals: 12</div>
        <div style='color: #10B981; font-weight: bold;'>📞 Hot Leads: 28</div>
        <div style='color: #F59E0B; font-weight: bold;'>💰 Pipeline: $485K</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.current_page = 'landing'
        st.rerun()

def render_dashboard():
    """Main dashboard"""
    
    st.markdown('<h1 class="main-header">🏠 Wholesaling Dashboard</h1>', unsafe_allow_html=True)
    
    user_name = st.session_state.user_data.get('name', 'User')
    
    st.markdown(f"""
    <div class='feature-card'>
        <h3 style='color: white; text-align: center; margin: 0;'>🎯 Welcome back, {user_name}!</h3>
        <p style='color: white; text-align: center; margin: 0.5rem 0;'>
            Your wholesaling command center is ready
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class='metric-card success-metric'>
            <h3 style='color: #10B981; margin: 0; font-size: 2rem;'>$125K</h3>
            <p style='margin: 0; font-weight: bold;'>Total Revenue</p>
            <small style='color: #9CA3AF;'>8 deals closed</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0; font-size: 2rem;'>$285K</h3>
            <p style='margin: 0; font-weight: bold;'>Pipeline Value</p>
            <small style='color: #9CA3AF;'>12 active deals</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card warning-metric'>
            <h3 style='color: #F59E0B; margin: 0; font-size: 2rem;'>28</h3>
            <p style='margin: 0; font-weight: bold;'>Hot Leads</p>
            <small style='color: #9CA3AF;'>156 total leads</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0; font-size: 2rem;'>67</h3>
            <p style='margin: 0; font-weight: bold;'>Grade A Deals</p>
            <small style='color: #9CA3AF;'>234 total analyzed</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #8B5CF6; margin: 0; font-size: 2rem;'>18.5%</h3>
            <p style='margin: 0; font-weight: bold;'>Conversion Rate</p>
            <small style='color: #9CA3AF;'>Lead to deal</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Analyze New Deal", use_container_width=True):
            st.session_state.current_page = 'deal_analyzer'
            st.rerun()
    
    with col2:
        if st.button("📞 Add New Lead", use_container_width=True):
            st.session_state.current_page = 'lead_manager'
            st.rerun()
    
    with col3:
        if st.button("📝 Generate LOI", use_container_width=True):
            st.session_state.current_page = 'loi_generator'
            st.rerun()
    
    with col4:
        if st.button("📄 Create Contract", use_container_width=True):
            st.session_state.current_page = 'contract_generator'
            st.rerun()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Recent Deals")
        
        deals = MockServices.get_sample_deals()
        
        for deal in deals:
            stage_colors = {
                'prospecting': '#6B7280',
                'negotiating': '#F59E0B', 
                'due_diligence': '#8B5CF6',
                'under_contract': '#10B981'
            }
            
            color = stage_colors.get(deal['stage'], '#6B7280')
            
            st.markdown(f"""
            <div class='deal-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h5 style='color: white; margin: 0;'>{deal['title']}</h5>
                        <small style='color: #9CA3AF;'>{deal['address']}</small>
                    </div>
                    <div style='text-align: right;'>
                        <p style='color: {color}; margin: 0; font-weight: bold;'>{deal['status']}</p>
                        <p style='color: #10B981; margin: 0;'>${deal['profit']:,}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📞 Recent Leads")
        
        leads = MockServices.get_sample_leads()
        
        for lead in leads:
            status_colors = {
                'New': '#8B5CF6',
                'Warm': '#F59E0B',
                'Hot': '#10B981'
            }
            
            color = status_colors.get(lead['status'], '#6B7280')
            
            st.markdown(f"""
            <div class='deal-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h5 style='color: white; margin: 0;'>{lead['name']}</h5>
                        <small style='color: #9CA3AF;'>{lead['phone']}</small>
                    </div>
                    <div style='text-align: right;'>
                        <p style='color: {color}; margin: 0; font-weight: bold;'>{lead['status']}</p>
                        <p style='color: #F59E0B; margin: 0;'>Score: {lead['score']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Performance charts
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

def render_deal_analyzer():
    """Deal analysis tool"""
    
    st.markdown('<h1 class="main-header">🔍 Deal Analyzer</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color: white; text-align: center; margin: 0;'>🎯 ULTIMATE DEAL ANALYSIS ENGINE</h3>
        <p style='color: white; text-align: center; margin: 0.5rem 0;'>
            Real-time data • AI-powered insights • Professional reports
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("deal_analyzer_form"):
        st.markdown("### 📍 Property Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            address = st.text_input("Property Address*", placeholder="123 Main Street")
            city = st.text_input("City*", placeholder="Dallas")
            state = st.selectbox("State*", ["TX", "CA", "FL", "NY", "GA"])
            list_price = st.number_input("List Price*", min_value=0, value=250000, step=1000)
        
        with col2:
            bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
            square_feet = st.number_input("Square Feet", min_value=0, max_value=10000, value=1800)
            condition = st.selectbox("Condition", ["excellent", "good", "fair", "poor", "needs_rehab"])
        
        analyze_btn = st.form_submit_button("🚀 Analyze Deal", type="primary")
        
        if analyze_btn and address and city and state and list_price:
            with st.spinner("🔍 Performing comprehensive analysis..."):
                
                # Simulate analysis
                progress_bar = st.progress(0)
                time.sleep(0.5)
                progress_bar.progress(25)
                time.sleep(0.5)
                progress_bar.progress(50)
                time.sleep(0.5)
                progress_bar.progress(75)
                time.sleep(0.5)
                progress_bar.progress(100)
                time.sleep(0.3)
                progress_bar.empty()
                
                # Mock analysis results
                arv = list_price * 1.15
                rehab_cost = square_feet * 25
                max_offer = (arv * 0.70) - rehab_cost
                profit_potential = arv - max_offer - rehab_cost
                
                grade = "A" if profit_potential > 30000 else "B" if profit_potential > 15000 else "C"
                grade_score = min(95, max(60, (profit_potential / arv) * 300))
                
                st.success("✅ Analysis Complete!")
                
                # Results display
                grade_colors = {'A': '#10B981', 'B': '#8B5CF6', 'C': '#F59E0B', 'D': '#EF4444'}
                
                st.markdown(f"""
                <div class='feature-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%); 
                            border: 3px solid {grade_colors.get(grade, '#6B7280')}; text-align: center;'>
                    <h2 style='color: {grade_colors.get(grade, '#6B7280')}; margin: 0; font-size: 3rem;'>
                        Deal Grade: {grade}
                    </h2>
                    <div style='display: flex; justify-content: center; gap: 2rem; margin: 1rem 0;'>
                        <div>
                            <p style='margin: 0; font-size: 1.2rem; color: white; font-weight: bold;'>
                                Score: {grade_score:.0f}/100
                            </p>
                        </div>
                        <div>
                            <p style='margin: 0; font-size: 1.2rem; color: white; font-weight: bold;'>
                                Confidence: 85%
                            </p>
                        </div>
                    </div>
                    <p style='margin: 1rem 0; font-size: 1.4rem; color: white; font-weight: bold;'>
                        💡 Recommended Strategy: Wholesale
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("List Price", f"${list_price:,}")
                    st.metric("ARV", f"${arv:,.0f}")
                
                with col2:
                    st.metric("Rehab Cost", f"${rehab_cost:,.0f}")
                    st.metric("Max Offer (70%)", f"${max_offer:,.0f}")
                
                with col3:
                    st.metric("Profit Potential", f"${profit_potential:,.0f}")
                    profit_margin = (profit_potential / arv * 100)
                    st.metric("Profit Margin", f"{profit_margin:.1f}%")
                
                with col4:
                    st.metric("Square Feet", f"{square_feet:,}")
                    st.metric("Price/SqFt", f"${list_price/square_feet:.0f}")
                
                # Action buttons
                st.markdown("### 🎯 Take Action")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📝 Generate LOI", use_container_width=True):
                        st.success("LOI data prepared!")
                
                with col2:
                    if st.button("📄 Create Contract", use_container_width=True):
                        st.success("Contract template ready!")
                
                with col3:
                    if st.button("👥 Find Buyers", use_container_width=True):
                        st.success("Buyer matching initiated!")
                
                with col4:
                    if st.button("📋 Create Deal", use_container_width=True):
                        st.success("Deal added to pipeline!")

def render_rvm_campaigns():
    """Ringless Voicemail Campaigns - Enhanced Demo"""
    
    st.markdown('<h1 class="main-header">📞 Ringless Voicemail Campaigns</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color: white; text-align: center; margin: 0;'>🎯 RINGLESS VOICEMAIL POWER TOOL</h3>
        <p style='color: white; text-align: center; margin: 0.5rem 0;'>
            15-20% response rates • 94% delivery • No phone ringing • TCPA compliant
        </p>
        <p style='color: white; text-align: center; margin: 0; font-size: 0.9rem;'>
            Remaining this month: Unlimited campaigns (Pro Plan)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📞 New Campaign", "📊 Active Campaigns", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 🎯 Create New RVM Campaign")
        
        with st.form("rvm_campaign_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                campaign_name = st.text_input("Campaign Name*", placeholder="Summer 2024 Motivated Sellers")
                campaign_type = st.selectbox("Campaign Type", [
                    "Motivated Sellers",
                    "Cash Buyers",
                    "Expired Listings",
                    "FSBO Leads"
                ])
                caller_id = st.text_input("Caller ID", placeholder="(555) 123-4567")
            
            with col2:
                st.markdown("**Audio Message**")
                audio_template = st.selectbox("Choose Template", [
                    "Motivated Seller - General",
                    "Motivated Seller - Divorce",
                    "Cash Buyer - Deal Alert",
                    "Follow-up - Previous Contact"
                ])
                
                if st.button("🎵 Preview Template"):
                    st.success("Audio preview: 'Hi, this is John from WTF Investments...'")
            
            # Recipients
            st.markdown("### 👥 Select Recipients")
            
            recipient_count = st.number_input("Number of Recipients", min_value=1, max_value=5000, value=100)
            
            # Cost calculation
            cost_per_message = 0.015
            total_cost = recipient_count * cost_per_message
            expected_responses = int(recipient_count * 0.17)
            
            st.markdown(f"""
            <div class='metric-card success-metric'>
                <h4 style='color: #10B981; margin: 0;'>Campaign Cost Estimate</h4>
                <p style='margin: 0.5rem 0;'>
                    {recipient_count} recipients × ${cost_per_message:.3f} = ${total_cost:.2f}
                </p>
                <p style='margin: 0; font-size: 0.9rem;'>
                    Expected responses: {expected_responses} (17% avg response rate)
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("🚀 Launch Campaign", type="primary"):
                if campaign_name:
                    with st.spinner("Launching RVM campaign..."):
                        time.sleep(2)
                    
                    st.success(f"""
                    🎉 **Campaign "{campaign_name}" launched successfully!**
                    
                    📊 **Campaign Details:**
                    - Recipients: {recipient_count}
                    - Expected delivery time: 5-15 minutes
                    - Total cost: ${total_cost:.2f}
                    - Campaign ID: RVM_{uuid.uuid4().hex[:8].upper()}
                    """)
                else:
                    st.error("Campaign name is required")
    
    with tab2:
        st.markdown("### 📊 Active Campaigns")
        
        # Mock campaign data
        campaigns = [
            {
                'name': 'Summer Motivated Sellers',
                'status': 'Sending',
                'sent': 847,
                'total': 1200,
                'responses': 72,
                'cost': 18.00
            },
            {
                'name': 'Cash Buyer Deal Alert',
                'status': 'Completed', 
                'sent': 356,
                'total': 356,
                'responses': 28,
                'cost': 5.34
            }
        ]
        
        for campaign in campaigns:
            progress = (campaign['sent'] / campaign['total']) * 100
            response_rate = (campaign['responses'] / campaign['sent']) * 100 if campaign['sent'] > 0 else 0
            
            st.markdown(f"""
            <div class='deal-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                    <div>
                        <h4 style='color: white; margin: 0;'>{campaign['name']}</h4>
                        <p style='color: #9CA3AF; margin: 0; font-size: 0.9rem;'>Status: {campaign['status']}</p>
                    </div>
                </div>
                
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem;'>
                    <div style='text-align: center;'>
                        <p style='color: #8B5CF6; font-weight: bold; margin: 0;'>{campaign['sent']}/{campaign['total']}</p>
                        <small style='color: #9CA3AF;'>Sent</small>
                    </div>
                    <div style='text-align: center;'>
                        <p style='color: #10B981; font-weight: bold; margin: 0;'>{campaign['responses']}</p>
                        <small style='color: #9CA3AF;'>Responses</small>
                    </div>
                    <div style='text-align: center;'>
                        <p style='color: #F59E0B; font-weight: bold; margin: 0;'>{response_rate:.1f}%</p>
                        <small style='color: #9CA3AF;'>Response Rate</small>
                    </div>
                    <div style='text-align: center;'>
                        <p style='color: #3B82F6; font-weight: bold; margin: 0;'>${campaign['cost']:.2f}</p>
                        <small style='color: #9CA3AF;'>Cost</small>
                    </div>
                </div>
                
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {progress}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📈 RVM Campaign Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Campaigns", "47", "+5 this month")
        
        with col2:
            st.metric("Messages Sent", "23,847", "+2,156 this month")
        
        with col3:
            st.metric("Total Responses", "2,185", "+198 this month")
        
        with col4:
            st.metric("Avg Response Rate", "9.2%", "+1.3% vs last month")
        
        # Response rate chart
        campaign_types = ['Motivated Sellers', 'Cash Buyers', 'Expired Listings', 'FSBO']
        response_rates = [9.2, 7.8, 11.5, 6.4]
        
        fig = px.bar(
            x=campaign_types,
            y=response_rates,
            title='Response Rate by Campaign Type',
            labels={'x': 'Campaign Type', 'y': 'Response Rate (%)'},
            color=response_rates,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

def render_placeholder_page(title, description):
    """Placeholder for pages under development"""
    
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='feature-card'>
        <h3 style='color: white; text-align: center; margin: 0;'>🚧 Coming Soon!</h3>
        <p style='color: white; text-align: center; margin: 1rem 0;'>
            {description}
        </p>
        <p style='color: #9CA3AF; text-align: center; margin: 0; font-size: 0.9rem;'>
            This feature is under development and will be available soon.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature preview
    st.markdown("### 🎯 Planned Features")
    
    if "Lead Manager" in title:
        features = [
            "📞 Lead scoring and prioritization",
            "🔄 Automated follow-up sequences", 
            "📊 Communication tracking",
            "🎯 Conversion optimization",
            "📱 Mobile lead capture"
        ]
    elif "Contract" in title:
        features = [
            "📄 Professional contract templates",
            "✍️ E-signature integration",
            "📋 State-specific forms",
            "🔄 Automated filling",
            "📱 Mobile signing"
        ]
    elif "LOI" in title:
        features = [
            "📝 Professional LOI templates",
            "💰 Automated calculations",
            "📧 Email delivery",
            "📊 Response tracking",
            "📋 Template library"
        ]
    else:
        features = [
            "📊 Advanced analytics",
            "🔄 Process automation",
            "📱 Mobile optimization", 
            "🔗 Third-party integrations",
            "📈 Performance tracking"
        ]
    
    for feature in features:
        st.markdown(f"- {feature}")

# Main application logic
def main():
    """Main application controller"""
    
    if not st.session_state.authenticated:
        render_landing_page()
    else:
        render_sidebar()
        
        # Route to pages
        current_page = st.session_state.current_page
        
        if current_page == 'dashboard':
            render_dashboard()
        elif current_page == 'deal_analyzer':
            render_deal_analyzer()
        elif current_page == 'rvm_campaigns':
            render_rvm_campaigns()
        elif current_page == 'lead_manager':
            render_placeholder_page("📞 Lead Manager", "Comprehensive lead management and CRM system")
        elif current_page == 'deal_pipeline':
            render_placeholder_page("📋 Deal Pipeline", "Track deals from lead to closing")
        elif current_page == 'contract_generator':
            render_placeholder_page("📄 Contract Generator", "Professional contract creation and e-signature")
        elif current_page == 'loi_generator':
            render_placeholder_page("📝 LOI Generator", "Letter of Intent creation and management")
        elif current_page == 'analytics':
            render_placeholder_page("📊 Analytics", "Advanced business intelligence and reporting")
        else:
            render_dashboard()

# Run the application
if __name__ == "__main__":
    main()
