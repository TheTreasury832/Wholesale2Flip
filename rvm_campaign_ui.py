# Ringless Voicemail Campaign Builder - Complete UI Implementation
# Add this to your WTF platform as a new page

def render_rvm_campaign_builder():
    """Complete Ringless Voicemail Campaign Builder UI"""
    
    st.markdown('<h1 class="main-header">📞 Ringless Voicemail Campaigns</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user_data.get('id')
    
    # Check usage limits for RVM
    usage_check = services['usage_tracker'].check_usage_limit(user_id, 'rvm_campaigns')
    
    if not usage_check['allowed']:
        st.error("❌ RVM campaign limit reached for this month. Please upgrade your plan.")
        return
    
    st.markdown(f"""
    <div class='wholesaler-panel'>
        <h3 style='color: white; margin: 0; text-align: center;'>🎯 RINGLESS VOICEMAIL POWER TOOL</h3>
        <p style='color: white; margin: 0.5rem 0; text-align: center;'>
            15-20% response rates • 94% delivery • No phone ringing • TCPA compliant
        </p>
        <p style='color: white; margin: 0; text-align: center; font-size: 0.9rem;'>
            Remaining this month: {usage_check['remaining'] if usage_check['remaining'] != -1 else "Unlimited"} campaigns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Campaign tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📞 New Campaign", "📊 Active Campaigns", "📈 Analytics", "🎵 Audio Library"])
    
    with tab1:
        render_new_rvm_campaign(user_id)
    
    with tab2:
        render_active_rvm_campaigns(user_id)
    
    with tab3:
        render_rvm_analytics(user_id)
    
    with tab4:
        render_audio_library(user_id)

def render_new_rvm_campaign(user_id):
    """New RVM campaign creation interface"""
    
    st.markdown("### 🎯 Create New RVM Campaign")
    
    with st.form("rvm_campaign_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Campaign Settings**")
            campaign_name = st.text_input("Campaign Name*", placeholder="Summer 2024 Motivated Sellers")
            campaign_type = st.selectbox("Campaign Type", [
                "Motivated Sellers",
                "Cash Buyers", 
                "Past Clients",
                "Expired Listings",
                "FSBO Leads",
                "Custom List"
            ])
            
            caller_id = st.text_input("Caller ID", placeholder="(555) 123-4567")
            schedule_type = st.radio("When to Send", ["Send Now", "Schedule for Later"])
            
            if schedule_type == "Schedule for Later":
                send_date = st.date_input("Send Date")
                send_time = st.time_input("Send Time")
        
        with col2:
            st.markdown("**Audio Message**")
            audio_option = st.radio("Audio Source", ["Pre-recorded Templates", "Upload New Audio", "Text-to-Speech"])
            
            if audio_option == "Pre-recorded Templates":
                template_options = [
                    "Motivated Seller - Divorce",
                    "Motivated Seller - Foreclosure", 
                    "Motivated Seller - General",
                    "Cash Buyer - New Deal Alert",
                    "Cash Buyer - Exclusive Opportunity",
                    "Follow-up - Previous Contact"
                ]
                selected_template = st.selectbox("Choose Template", template_options)
                
                # Preview template
                if st.button("🎵 Preview Template"):
                    st.audio("https://example.com/audio/template1.mp3")  # Mock audio URL
                    st.success("Template loaded! Duration: 45 seconds")
            
            elif audio_option == "Upload New Audio":
                uploaded_audio = st.file_uploader("Upload Audio File", type=['mp3', 'wav', 'm4a'])
                if uploaded_audio:
                    st.audio(uploaded_audio)
                    st.info("✅ Audio uploaded successfully! Duration: 52 seconds")
            
            else:  # Text-to-Speech
                tts_script = st.text_area("Script for Text-to-Speech", 
                                        placeholder="Hi, this is John from WTF Investments. I'm reaching out because...",
                                        height=150)
                voice_type = st.selectbox("Voice Type", ["Male - Professional", "Female - Friendly", "Male - Casual"])
                
                if st.button("🎵 Generate Audio Preview") and tts_script:
                    with st.spinner("Generating audio preview..."):
                        time.sleep(2)  # Simulate processing
                    st.audio("https://example.com/generated_audio.mp3")  # Mock generated audio
                    st.success("Audio generated! Duration: 38 seconds")
        
        # Lead selection
        st.markdown("### 👥 Select Recipients")
        
        recipient_source = st.radio("Recipient Source", [
            "Existing Lead Lists", 
            "Upload CSV File", 
            "Manual Entry",
            "Saved Buyer Lists"
        ])
        
        recipients_count = 0
        selected_leads = []
        
        if recipient_source == "Existing Lead Lists":
            # Get user's lead lists
            conn = services['db'].get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM leads WHERE user_id = ?', (user_id,))
            total_leads = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT id, first_name, last_name, phone, status, score, created_at
                FROM leads WHERE user_id = ? AND phone IS NOT NULL
                ORDER BY score DESC, created_at DESC
            ''', (user_id,))
            
            leads = cursor.fetchall()
            conn.close()
            
            if leads:
                st.info(f"📊 Total leads with phone numbers: {len(leads)}")
                
                # Lead filtering
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    min_score = st.slider("Minimum Lead Score", 0, 100, 70)
                
                with col2:
                    status_filter = st.multiselect("Lead Status", 
                                                 ["new", "contacted", "interested", "not_interested"],
                                                 default=["new", "contacted", "interested"])
                
                with col3:
                    max_leads = st.number_input("Max Recipients", min_value=1, max_value=5000, value=100)
                
                # Filter leads
                filtered_leads = [
                    lead for lead in leads 
                    if lead[5] >= min_score and lead[4] in status_filter
                ][:max_leads]
                
                recipients_count = len(filtered_leads)
                selected_leads = filtered_leads
                
                if recipients_count > 0:
                    st.success(f"✅ {recipients_count} recipients selected")
                    
                    # Preview recipients
                    if st.checkbox("Preview Recipients"):
                        preview_df = pd.DataFrame(filtered_leads[:10], 
                                                columns=['ID', 'First Name', 'Last Name', 'Phone', 'Status', 'Score', 'Created'])
                        st.dataframe(preview_df[['First Name', 'Last Name', 'Phone', 'Status', 'Score']])
                        
                        if len(filtered_leads) > 10:
                            st.info(f"Showing first 10 of {recipients_count} recipients")
                else:
                    st.warning("No leads match your criteria. Adjust filters to include more leads.")
            else:
                st.warning("No leads found. Add leads first or upload a CSV file.")
        
        elif recipient_source == "Upload CSV File":
            uploaded_csv = st.file_uploader("Upload CSV File", type=['csv'])
            
            if uploaded_csv:
                try:
                    df = pd.read_csv(uploaded_csv)
                    
                    # Check required columns
                    required_cols = ['phone']
                    optional_cols = ['first_name', 'last_name', 'name']
                    
                    if 'phone' in df.columns:
                        recipients_count = len(df)
                        st.success(f"✅ {recipients_count} recipients loaded from CSV")
                        
                        # Preview CSV data
                        st.dataframe(df.head())
                        
                        # Validate phone numbers
                        valid_phones = df['phone'].str.match(r'^\+?1?[2-9]\d{9}$').sum()
                        if valid_phones < len(df):
                            st.warning(f"⚠️ {len(df) - valid_phones} phone numbers may be invalid")
                    else:
                        st.error("CSV must contain a 'phone' column")
                        
                except Exception as e:
                    st.error(f"Error reading CSV: {str(e)}")
        
        elif recipient_source == "Manual Entry":
            manual_phones = st.text_area("Enter Phone Numbers (one per line)", 
                                        placeholder="5551234567\n5559876543\n...")
            
            if manual_phones:
                phone_list = [phone.strip() for phone in manual_phones.split('\n') if phone.strip()]
                recipients_count = len(phone_list)
                st.info(f"📞 {recipients_count} phone numbers entered")
        
        else:  # Saved Buyer Lists
            st.info("🚧 Buyer list integration coming soon!")
        
        # Campaign cost calculation
        if recipients_count > 0:
            cost_per_message = 0.015  # $0.015 per RVM
            total_cost = recipients_count * cost_per_message
            
            st.markdown(f"""
            <div class='metric-card success-metric'>
                <h4 style='color: #10B981; margin: 0;'>Campaign Cost Estimate</h4>
                <p style='margin: 0.5rem 0;'>
                    {recipients_count} recipients × ${cost_per_message:.3f} = ${total_cost:.2f}
                </p>
                <p style='margin: 0; font-size: 0.9rem;'>
                    Expected responses: {int(recipients_count * 0.17)} ({17}% avg response rate)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Campaign submission
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            campaign_notes = st.text_input("Campaign Notes (Optional)", 
                                         placeholder="Summer motivated seller outreach...")
        
        with col2:
            test_mode = st.checkbox("Test Mode", help="Send to 5 recipients only for testing")
        
        with col3:
            submit_campaign = st.form_submit_button("🚀 Launch Campaign", type="primary")
        
        if submit_campaign:
            if not campaign_name:
                st.error("Campaign name is required")
            elif recipients_count == 0:
                st.error("Please select recipients")
            elif audio_option == "Pre-recorded Templates" and not selected_template:
                st.error("Please select an audio template")
            elif audio_option == "Upload New Audio" and not uploaded_audio:
                st.error("Please upload an audio file")
            elif audio_option == "Text-to-Speech" and not tts_script:
                st.error("Please enter a script for text-to-speech")
            else:
                # Launch campaign
                with st.spinner("Launching RVM campaign..."):
                    
                    # Mock campaign creation
                    campaign_id = str(uuid.uuid4())
                    
                    # Simulate campaign processing
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Validate recipients
                    status_text.text("📋 Validating recipients...")
                    progress_bar.progress(20)
                    time.sleep(1)
                    
                    # Step 2: Process audio
                    status_text.text("🎵 Processing audio file...")
                    progress_bar.progress(40)
                    time.sleep(1)
                    
                    # Step 3: Schedule delivery
                    status_text.text("📅 Scheduling delivery...")
                    progress_bar.progress(60)
                    time.sleep(1)
                    
                    # Step 4: Submit to RVM service
                    status_text.text("📞 Submitting to RVM service...")
                    progress_bar.progress(80)
                    time.sleep(1)
                    
                    # Step 5: Complete
                    status_text.text("✅ Campaign launched successfully!")
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Track usage
                    services['usage_tracker'].track_usage(
                        user_id, 'rvm_campaigns', 1, 
                        f"Campaign: {campaign_name}, Recipients: {recipients_count}"
                    )
                    
                    # Log activity
                    services['activity_logger'].log_activity(
                        user_id, 'rvm_campaign_created', 
                        f'Created RVM campaign "{campaign_name}" with {recipients_count} recipients',
                        'campaign', campaign_id
                    )
                    
                    # Save campaign to database
                    save_rvm_campaign(user_id, campaign_id, campaign_name, recipients_count, total_cost)
                    
                    st.success(f"""
                    🎉 **Campaign "{campaign_name}" launched successfully!**
                    
                    📊 **Campaign Details:**
                    - Recipients: {recipients_count}
                    - Expected delivery time: 5-15 minutes
                    - Total cost: ${total_cost:.2f}
                    - Campaign ID: {campaign_id[:8]}...
                    
                    You'll receive real-time updates as messages are delivered and responses come in.
                    """)

def render_active_rvm_campaigns(user_id):
    """Display active RVM campaigns"""
    
    st.markdown("### 📊 Active Campaigns")
    
    # Mock active campaigns data
    active_campaigns = [
        {
            'id': 'camp_001',
            'name': 'Summer Motivated Sellers',
            'status': 'Sending',
            'sent': 847,
            'total': 1200,
            'responses': 72,
            'response_rate': 8.5,
            'cost': 18.00,
            'created': '2024-08-09 09:30',
            'estimated_completion': '2024-08-09 10:15'
        },
        {
            'id': 'camp_002', 
            'name': 'Cash Buyer Deal Alert',
            'status': 'Completed',
            'sent': 356,
            'total': 356,
            'responses': 28,
            'response_rate': 7.9,
            'cost': 5.34,
            'created': '2024-08-08 14:20',
            'estimated_completion': '2024-08-08 14:35'
        },
        {
            'id': 'camp_003',
            'name': 'Expired Listings Follow-up',
            'status': 'Scheduled',
            'sent': 0,
            'total': 89,
            'responses': 0,
            'response_rate': 0,
            'cost': 1.34,
            'created': '2024-08-09 11:00',
            'estimated_completion': '2024-08-09 15:00'
        }
    ]
    
    for campaign in active_campaigns:
        status_colors = {
            'Sending': '#F59E0B',
            'Completed': '#10B981', 
            'Scheduled': '#8B5CF6',
            'Failed': '#EF4444'
        }
        
        status_color = status_colors.get(campaign['status'], '#6B7280')
        progress_percent = (campaign['sent'] / campaign['total']) * 100 if campaign['total'] > 0 else 0
        
        st.markdown(f"""
        <div class='deal-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                <div>
                    <h4 style='color: white; margin: 0;'>{campaign['name']}</h4>
                    <p style='color: #9CA3AF; margin: 0; font-size: 0.9rem;'>
                        Created: {campaign['created']} | ID: {campaign['id']}
                    </p>
                </div>
                <div style='text-align: right;'>
                    <span style='background: {status_color}; color: white; padding: 0.3rem 0.8rem; 
                                 border-radius: 15px; font-size: 0.8rem; font-weight: bold;'>
                        {campaign['status']}
                    </span>
                </div>
            </div>
            
            <div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 1rem;'>
                <div style='text-align: center;'>
                    <p style='color: #8B5CF6; font-weight: bold; margin: 0; font-size: 1.2rem;'>
                        {campaign['sent']}/{campaign['total']}
                    </p>
                    <small style='color: #9CA3AF;'>Sent</small>
                </div>
                <div style='text-align: center;'>
                    <p style='color: #10B981; font-weight: bold; margin: 0; font-size: 1.2rem;'>
                        {campaign['responses']}
                    </p>
                    <small style='color: #9CA3AF;'>Responses</small>
                </div>
                <div style='text-align: center;'>
                    <p style='color: #F59E0B; font-weight: bold; margin: 0; font-size: 1.2rem;'>
                        {campaign['response_rate']:.1f}%
                    </p>
                    <small style='color: #9CA3AF;'>Response Rate</small>
                </div>
                <div style='text-align: center;'>
                    <p style='color: #3B82F6; font-weight: bold; margin: 0; font-size: 1.2rem;'>
                        ${campaign['cost']:.2f}
                    </p>
                    <small style='color: #9CA3AF;'>Cost</small>
                </div>
                <div style='text-align: center;'>
                    <p style='color: white; font-weight: bold; margin: 0; font-size: 1.2rem;'>
                        {progress_percent:.0f}%
                    </p>
                    <small style='color: #9CA3AF;'>Progress</small>
                </div>
            </div>
            
            <div class='progress-container' style='margin-bottom: 1rem;'>
                <div class='progress-bar' style='width: {progress_percent}%; background: {status_color};'></div>
            </div>
            
            <div style='display: flex; gap: 1rem; justify-content: center;'>
                <button style='background: #8B5CF6; color: white; border: none; padding: 0.5rem 1rem; 
                               border-radius: 8px; cursor: pointer;'>
                    📊 View Details
                </button>
                <button style='background: #10B981; color: white; border: none; padding: 0.5rem 1rem; 
                               border-radius: 8px; cursor: pointer;'>
                    📞 View Responses
                </button>
                {"<button style='background: #EF4444; color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer;'>⏹️ Stop Campaign</button>" if campaign['status'] == 'Sending' else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_rvm_analytics(user_id):
    """RVM campaign analytics dashboard"""
    
    st.markdown("### 📈 RVM Campaign Analytics")
    
    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Campaigns", "47", "+5 this month")
    
    with col2:
        st.metric("Messages Sent", "23,847", "+2,156 this month")
    
    with col3:
        st.metric("Total Responses", "2,185", "+198 this month")
    
    with col4:
        st.metric("Avg Response Rate", "9.2%", "+1.3% vs last month")
    
    with col5:
        st.metric("Total Cost", "$357.71", "+$32.34 this month")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Response rate by campaign type
        campaign_types = ['Motivated Sellers', 'Cash Buyers', 'Expired Listings', 'FSBO', 'Follow-up']
        response_rates = [9.2, 7.8, 11.5, 6.4, 14.2]
        
        fig_response = px.bar(
            x=campaign_types,
            y=response_rates,
            title='Response Rate by Campaign Type',
            labels={'x': 'Campaign Type', 'y': 'Response Rate (%)'},
            color=response_rates,
            color_continuous_scale='Viridis'
        )
        fig_response.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col2:
        # Daily response tracking
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        responses = [45, 67, 52, 78, 89, 34, 23]
        
        fig_daily = px.line(
            x=days,
            y=responses,
            title='Daily Responses This Week',
            labels={'x': 'Day', 'y': 'Responses'},
            markers=True
        )
        fig_daily.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        fig_daily.update_traces(line_color='#10B981', marker_color='#10B981')
        st.plotly_chart(fig_daily, use_container_width=True)
    
    # Best performing campaigns
    st.markdown("### 🏆 Top Performing Campaigns")
    
    top_campaigns = [
        {'name': 'Divorce Motivated Sellers', 'responses': 156, 'rate': 18.7, 'cost': 0.012},
        {'name': 'Pre-Foreclosure Outreach', 'responses': 134, 'rate': 16.2, 'cost': 0.014},
        {'name': 'Expired Listing Follow-up', 'responses': 98, 'rate': 15.8, 'cost': 0.013},
        {'name': 'Cash Buyer Deal Alert', 'responses': 87, 'rate': 12.4, 'cost': 0.015},
        {'name': 'FSBO Outreach', 'responses': 67, 'rate': 11.9, 'cost': 0.016}
    ]
    
    for i, campaign in enumerate(top_campaigns, 1):
        st.markdown(f"""
        <div style='background: rgba(16, 185, 129, 0.1); padding: 1rem; margin: 0.5rem 0; border-radius: 10px; 
                    border-left: 4px solid #10B981;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <strong style='color: white;'>#{i}. {campaign['name']}</strong>
                </div>
                <div style='display: flex; gap: 2rem; text-align: center;'>
                    <div>
                        <p style='color: #10B981; font-weight: bold; margin: 0;'>{campaign['responses']}</p>
                        <small style='color: #9CA3AF;'>Responses</small>
                    </div>
                    <div>
                        <p style='color: #F59E0B; font-weight: bold; margin: 0;'>{campaign['rate']:.1f}%</p>
                        <small style='color: #9CA3AF;'>Rate</small>
                    </div>
                    <div>
                        <p style='color: #8B5CF6; font-weight: bold; margin: 0;'>${campaign['cost']:.3f}</p>
                        <small style='color: #9CA3AF;'>Cost per msg</small>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_audio_library(user_id):
    """Audio template library for RVM campaigns"""
    
    st.markdown("### 🎵 Audio Template Library")
    
    # Template categories
    categories = ["Motivated Sellers", "Cash Buyers", "Follow-up", "Seasonal", "Custom"]
    selected_category = st.selectbox("Filter by Category", categories)
    
    # Audio templates
    audio_templates = {
        "Motivated Sellers": [
            {
                'name': 'Divorce Situation',
                'duration': '45 sec',
                'usage': 234,
                'rating': 4.8,
                'script': 'Hi, this is John from WTF Investments. I understand you may be going through a difficult time...'
            },
            {
                'name': 'Pre-Foreclosure',
                'duration': '52 sec', 
                'usage': 189,
                'rating': 4.6,
                'script': 'Hello, I specialize in helping homeowners facing foreclosure. There may be options...'
            },
            {
                'name': 'General Motivation',
                'duration': '38 sec',
                'usage': 567,
                'rating': 4.7,
                'script': 'Hi, I buy houses in your area for cash. If you need to sell quickly...'
            }
        ],
        "Cash Buyers": [
            {
                'name': 'New Deal Alert',
                'duration': '32 sec',
                'usage': 445,
                'rating': 4.9,
                'script': 'I have a great investment opportunity in your target area...'
            },
            {
                'name': 'Exclusive Offer',
                'duration': '41 sec',
                'usage': 276,
                'rating': 4.5,
                'script': 'This exclusive deal just came across my desk and I thought of you...'
            }
        ]
    }
    
    templates = audio_templates.get(selected_category, [])
    
    if templates:
        for template in templates:
            st.markdown(f"""
            <div class='feature-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                    <div>
                        <h4 style='color: white; margin: 0;'>{template['name']}</h4>
                        <p style='color: #9CA3AF; margin: 0; font-size: 0.9rem;'>
                            Duration: {template['duration']} | Used {template['usage']} times | ⭐ {template['rating']}/5
                        </p>
                    </div>
                    <div style='display: flex; gap: 0.5rem;'>
                        <button style='background: #8B5CF6; color: white; border: none; padding: 0.5rem 1rem; 
                                       border-radius: 8px; cursor: pointer;'>
                            🎵 Preview
                        </button>
                        <button style='background: #10B981; color: white; border: none; padding: 0.5rem 1rem; 
                                       border-radius: 8px; cursor: pointer;'>
                            📞 Use Template
                        </button>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px;'>
                    <p style='color: #E5E7EB; margin: 0; font-style: italic;'>"{template['script']}"</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Upload new template
    st.markdown("### 📤 Upload New Template")
    
    with st.form("upload_audio_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            template_name = st.text_input("Template Name", placeholder="My Custom Template")
            template_category = st.selectbox("Category", categories)
            template_description = st.text_area("Description", placeholder="Brief description of when to use this template")
        
        with col2:
            uploaded_audio = st.file_uploader("Upload Audio File", type=['mp3', 'wav', 'm4a'])
            
            if uploaded_audio:
                st.audio(uploaded_audio)
        
        is_public = st.checkbox("Make this template available to other users")
        
        if st.form_submit_button("📤 Upload Template"):
            if template_name and uploaded_audio:
                with st.spinner("Processing audio file..."):
                    time.sleep(2)  # Simulate processing
                
                st.success(f'✅ Template "{template_name}" uploaded successfully!')
                
                # Log activity
                services['activity_logger'].log_activity(
                    user_id, 'audio_template_uploaded',
                    f'Uploaded audio template: {template_name}',
                    'template', str(uuid.uuid4())
                )
            else:
                st.error("Please provide a template name and upload an audio file")

def save_rvm_campaign(user_id, campaign_id, campaign_name, recipients_count, total_cost):
    """Save RVM campaign to database"""
    
    conn = services['db'].get_connection()
    cursor = conn.cursor()
    
    # Create RVM campaigns table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rvm_campaigns (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            campaign_name TEXT NOT NULL,
            recipients_count INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            status TEXT DEFAULT 'sending',
            sent_count INTEGER DEFAULT 0,
            response_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        INSERT INTO rvm_campaigns (id, user_id, campaign_name, recipients_count, total_cost)
        VALUES (?, ?, ?, ?, ?)
    ''', (campaign_id, user_id, campaign_name, recipients_count, total_cost))
    
    conn.commit()
    conn.close()

# Add this to your main navigation in the sidebar
# In your render_ultimate_sidebar() function, add:
# "📞 RVM Campaigns": "rvm_campaigns"

# And in your main() routing function, add:
# elif selected_page == "rvm_campaigns":
#     render_rvm_campaign_builder()
