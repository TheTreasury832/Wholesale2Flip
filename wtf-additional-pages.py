# pages/pipeline.py
"""
Deal Pipeline Management Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

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

# pages/leads.py
"""
Lead Management System
"""

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

# pages/contracts.py
"""
Contract Generation and Management
"""

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

# pages/analytics.py
"""
Advanced Analytics Dashboard
"""

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

# Add these pages to the main app.py navigation
def add_pages_to_main_app():
    """
    Add these page functions to your main app.py file and update the navigation:
    
    # In the main() function, update the page routing:
    
    elif selected_page == "pipeline":
        render_pipeline_page()
    elif selected_page == "leads":
        render_leads_page()
    elif selected_page == "contracts":
        render_contracts_page()
    elif selected_page == "analytics":
        render_analytics_page()
    """
    pass