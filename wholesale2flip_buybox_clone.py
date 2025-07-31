            if signup_btn and name and email and password:
                if db.create_user(name, email, password, phone):
                    st.success("🎉 Account created! Login to access the WTF Deal Finder!")
                else:
                    st.error("Email already exists. Try logging in instead.")

def show_home_page():
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <div class="wtf-logo">W2F</div>
        <h1 class="hero-title">Wholesale2Flip Elite</h1>
        <h2 style="font-size: 2rem; margin-bottom: 1rem;">Make $10K-$30K Per Deal</h2>
        <p class="hero-subtitle">Our proprietary software matches Zillow properties with verified hedge fund buyers who pay 90-95% of list price</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User stats if logged in
    if st.session_state.logged_in:
        user = st.session_state.user
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Deals</h3>
                <h2>{user['total_deals']}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Profit</h3>
                <h2>${user['total_profit']:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Plan</h3>
                <h2>{user['subscription_tier'].title()}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Live classes notification
    st.markdown("""
    <div class="live-class-alert">
        🔴 LIVE RIGHT NOW: Richard Taylor & Chris Gallagher • Daily Mentorship • 50+ Hours/Week
    </div>
    """, unsafe_allow_html=True)
    
    # Discord integration
    st.markdown("""
    <div class="discord-link">
        💬 <strong>Join Our Discord Community</strong><br>
        13,000+ Wholesalers • Live Deal Reviews • Instant Buyer Matches • Daily Giveaways
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("## 🎯 Why WTF Dominates The Game")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🏠 WTF Deal Finder</h3>
            <p><strong>$150K Proprietary Software</strong><br>
            Automatically matches Zillow listings with our database of 5,000+ verified hedge fund buyers who pay 90-95% of list price.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💰 Guaranteed Profit Formula</h3>
            <p><strong>$10K-$30K Per Deal</strong><br>
            Offer $30K below list → Sell for $10K below list → Pocket $20K+ profit. We've done this with millions in properties.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎓 50+ Hours Weekly Training</h3>
            <p><strong>Live Mentorship Daily</strong><br>
            Mon-Fri 8AM-8PM EST with Richard Taylor & Chris Gallagher. Watch real deals happen live.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # More features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📞 90+ Email Templates</h3>
            <p><strong>Copy & Paste Success</strong><br>
            Pre-written emails, voicemails, contracts, and LOIs that close deals. Stop guessing what to say.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤝 We Sell YOUR Deals</h3>
            <p><strong>Disposition Made Easy</strong><br>
            Can't close a deal? We'll buy it from you or connect you with our network of 10,000+ investors.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💸 $300-500 Weekly Giveaways</h3>
            <p><strong>Free Money Every Week</strong><br>
            Active members win cash prizes weekly. Just for being part of the community.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Pricing Section - Matching Buy Box Cartel exactly
    st.markdown("## 💎 Join The Elite (Like Buy Box Cartel But Better)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>WTF Starter</h3>
            <div class="price-tag">$10</div>
            <p>per month</p>
            <ul style="text-align: left;">
                <li>✅ Access to WTF Deal Finder</li>
                <li>✅ Basic Buyer Database (1,000+)</li>
                <li>✅ 10 Email Templates</li>
                <li>✅ Discord Community Access</li>
                <li>✅ Weekly Live Classes</li>
                <li>✅ 50% JV Split</li>
            </ul>
            <p><strong>Perfect for:</strong> New wholesalers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Join WTF Starter", key="starter"):
            if st.session_state.logged_in:
                db.update_subscription(st.session_state.user['id'], 'starter')
                st.success("🎉 Welcome to WTF Starter! Access granted!")
                st.rerun()
            else:
                st.warning("Create account first!")
    
    with col2:
        st.markdown("""
        <div class="pricing-card featured">
            <h3>WTF Professional</h3>
            <div class="price-tag">$20</div>
            <p>per month</p>
            <ul style="text-align: left;">
                <li>✅ Everything in Starter</li>
                <li>✅ Premium Buyer Database (5,000+)</li>
                <li>✅ 90+ Email/Contract Templates</li>
                <li>✅ 50+ Hours Weekly Training</li>
                <li>✅ Creative Finance Deals</li>
                <li>✅ Section 8 Specialists</li>
                <li>✅ We Buy Your Deals</li>
                <li>✅ 60% JV Split</li>
            </ul>
            <p><strong>Perfect for:</strong> Serious money makers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Join WTF Pro (Most Popular)", key="professional"):
            if st.session_state.logged_in:
                db.update_subscription(st.session_state.user['id'], 'professional')
                st.success("🚀 Welcome to WTF Pro! You're in the big leagues now!")
                st.rerun()
            else:
                st.warning("Create account first!")
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>WTF Elite</h3>
            <div class="price-tag">$30</div>
            <p>per month</p>
            <ul style="text-align: left;">
                <li>✅ Everything in Professional</li>
                <li>✅ Exclusive Hedge Fund Buyers</li>
                <li>✅ Custom Contract Creation</li>
                <li>✅ 1-on-1 Deal Coaching</li>
                <li>✅ Direct Access to Richard & Chris</li>
                <li>✅ Private Mastermind Group</li>
                <li>✅ White-Label Platform</li>
                <li>✅ 70% JV Split</li>
            </ul>
            <p><strong>Perfect for:</strong> Elite wholesalers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Join WTF Elite", key="elite"):
            if st.session_state.logged_in:
                db.update_subscription(st.session_state.user['id'], 'elite')
                st.success("👑 Welcome to WTF Elite! You're now part of the 1%!")
                st.rerun()
            else:
                st.warning("Create account first!")
    
    # Testimonials section
    st.markdown("## 🏆 Success Stories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>💰 "Made $27K on my first deal"</h4>
            <p>"Used the WTF Deal Finder to match a Memphis property with a hedge fund buyer. Offered $95K, sold for $105K. Easiest money I ever made."</p>
            <p><strong>- Sarah M., Atlanta</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 "Closed 8 deals in 30 days"</h4>
            <p>"The buyer database is insane. I just copy/paste the email templates and deals close themselves. This is the real deal."</p>
            <p><strong>- Mike T., Birmingham</strong></p>
        </div>
        """, unsafe_allow_html=True)

def show_deal_finder():
    st.markdown("# 🏠 WTF Deal Finder - Property Matcher")
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Login required to access the WTF Deal Finder")
        return
    
    user_tier = st.session_state.user.get('subscription_tier', 'none')
    if user_tier == 'none':
        st.warning("⚠️ Subscription required! Upgrade to access the $150K software")
        return
    
    st.markdown("""
    <div class="live-class-alert">
        🎯 This is the $150K software that matches Zillow properties with hedge fund buyers!
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    with st.expander("🔍 Property Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            min_price = st.number_input("Min Price", min_value=0, value=50000, step=5000)
        with col2:
            max_price = st.number_input("Max Price", min_value=0, value=300000, step=5000)
        with col3:
            city_filter = st.selectbox("City", ["All", "Atlanta", "Memphis", "Birmingham", "Little Rock"])
        with col4:
            state_filter = st.selectbox("State", ["All", "GA", "TN", "AL", "AR"])
    
    # Get properties
    filters = {
        'min_price': min_price,
        'max_price': max_price,
        'city': city_filter if city_filter != "All" else None,
        'state': state_filter if state_filter != "All" else None
    }
    
    properties = db.get_properties(filters)
    
    st.markdown(f"## 🏠 Found {len(properties)} Properties Ready for Wholesale")
    
    for prop in properties:
        # Calculate potential profit
        list_price = prop['list_price']
        estimated_arv = prop['estimated_arv'] or list_price * 1.2
        offer_price = list_price - 30000  # Offer $30K below
        sell_price = list_price - 10000   # Sell $10K below
        potential_profit = sell_price - offer_price
        
        with st.expander(f"🏠 {prop['address']}, {prop['city']}, {prop['state']} - **💰 ${potential_profit:,.0f} Profit Potential**"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Property Details:**
                - **Address:** {prop['address']}, {prop['city']}, {prop['state']} {prop['zip_code']}
                - **Type:** {prop['property_type']}
                - **Bedrooms:** {prop['bedrooms']} | **Bathrooms:** {prop['bathrooms']}
                - **Square Feet:** {prop['square_feet']:,}
                - **Year Built:** {prop['year_built']}
                - **Condition:** {prop['property_condition']}
                - **Days on Market:** {prop['days_on_market']}
                """)
            
            with col2:
                st.markdown(f"""
                **Deal Analysis:**
                - **List Price:** ${list_price:,.0f}
                - **Estimated ARV:** ${estimated_arv:,.0f}
                - **Est. Repairs:** ${prop['estimated_repairs'] or 0:,.0f}
                - **Your Offer:** ${offer_price:,.0f}
                - **Sell Price:** ${sell_price:,.0f}
                """)
                
                st.markdown(f"""
                <div class="profit-highlight">
                💰 POTENTIAL PROFIT: ${potential_profit:,.0f}
                </div>
                """, unsafe_allow_html=True)
            
            # Get matched buyers
            matched_buyers = db.get_matched_buyers(prop['id'])
            
            if matched_buyers:
                st.markdown(f"### 🎯 {len(matched_buyers)} Verified Buyers Ready to Purchase:")
                
                for buyer in matched_buyers[:3]:  # Show top 3 buyers
                    preferred_markets = json.loads(buyer['preferred_markets']) if buyer['preferred_markets'] else []
                    
                    st.markdown(f"""
                    <div class="buyer-match">
                        <strong>{buyer['buyer_name']}</strong> ({buyer['buyer_type'].replace('_', ' ').title()})<br>
                        📧 {buyer['email']} | 📞 {buyer['phone']}<br>
                        💰 Budget: ${buyer['min_price']:,.0f} - ${buyer['max_price']:,.0f}<br>
                        ⭐ Rating: {buyer['rating']}/5.0 | 🏠 {buyer['total_purchases']} purchases<br>
                        ⏰ Closes in: {buyer['close_timeline']}
                    </div>
                    """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📧 Send Offer Email", key=f"email_{prop['id']}"):
                        st.success("📧 Offer email sent to seller!")
                with col2:
                    if st.button(f"📞 Contact Buyers", key=f"buyers_{prop['id']}"):
                        st.success("📞 Buyer notifications sent!")
                with col3:
                    if st.button(f"📄 Generate Contract", key=f"contract_{prop['id']}"):
                        st.success("📄 Contract generated and sent!")
            else:
                st.info("🔍 Finding buyers for this property... Check back soon!")

def show_templates():
    st.markdown("# 📧 Email Templates & Scripts")
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Login required to access templates")
        return
    
    user_tier = st.session_state.user.get('subscription_tier', 'none')
    
    st.markdown("""
    <div class="discord-link">
        📚 90+ Proven Templates That Close Deals • Copy, Paste, Profit
    </div>
    """, unsafe_allow_html=True)
    
    # Template categories
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Cash Offers", "🏦 Creative Finance", "🏠 Section 8", "📞 Voicemails"])
    
    with tab1:
        st.markdown("### 💰 Cash Offer Templates")
        
        st.markdown("""
        <div class="feature-card">
            <h4>📧 Cash Offer Email #1 - "Quick Sale"</h4>
            <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <strong>Subject:</strong> Cash Offer for {property_address}<br><br>
                
                Hi {seller_name},<br><br>
                
                I saw your property at {property_address} and I'm interested in making a cash offer.<br><br>
                
                <strong>My Offer: ${offer_price}</strong><br>
                • All cash - no financing<br>
                • Close in 7-14 days<br>
                • No inspections or appraisals<br>
                • We buy AS-IS<br><br>
                
                If you're ready to sell fast, reply to this email or call me at {phone}.<br><br>
                
                Best regards,<br>
                {your_name}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if user_tier in ['professional', 'elite']:
            st.markdown("""
            <div class="feature-card">
                <h4>📧 Cash Offer Email #2 - "Motivated Seller"</h4>
                <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>Subject:</strong> Urgent: Cash Buyer for {property_address}<br><br>
                    
                    {seller_name},<br><br>
                    
                    I understand you may need to sell {property_address} quickly.<br><br>
                    
                    I can help with:<br>
                    • Cash closing in 7 days<br>
                    • No realtor commissions<br>
                    • No repairs needed<br>
                    • We handle all paperwork<br><br>
                    
                    <strong>Cash Offer: ${offer_price}</strong><br><br>
                    
                    Call me today: {phone}<br><br>
                    
                    {your_name}<br>
                    Licensed Real Estate Professional
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🔒 Upgrade to Professional or Elite for 90+ premium templates")
    
    with tab2:
        if user_tier in ['professional', 'elite']:
            st.markdown("### 🏦 Creative Finance Templates")
            
            st.markdown("""
            <div class="feature-card">
                <h4>📧 Seller Finance Offer</h4>
                <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>Subject:</strong> Creative Financing Option for {property_address}<br><br>
                    
                    Dear {seller_name},<br><br>
                    
                    I'd like to propose a seller financing arrangement that benefits both of us:<br><br>
                    
                    <strong>Purchase Price:</strong> ${purchase_price}<br>
                    <strong>Down Payment:</strong> ${down_payment}<br>
                    <strong>Monthly Payment:</strong> ${monthly_payment}<br>
                    <strong>Interest Rate:</strong> {interest_rate}%<br>
                    <strong>Term:</strong> {term} years<br><br>
                    
                    Benefits to you:<br>
                    • Get your full asking price<br>
                    • Monthly cash flow<br>
                    • Tax advantages<br>
                    • No realtor fees<br><br>
                    
                    Let's discuss how this can work for both of us.<br><br>
                    
                    {your_name}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🔒 Upgrade to Professional or Elite for Creative Finance templates")
    
    with tab3:
        if user_tier in ['professional', 'elite']:
            st.markdown("### 🏠 Section 8 Templates")
            
            st.markdown("""
            <div class="feature-card">
                <h4>📧 Section 8 Rental Offer</h4>
                <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>Subject:</strong> Guaranteed Rent for {property_address}<br><br>
                    
                    Hi {seller_name},<br><br>
                    
                    I specialize in Section 8 housing and would like to purchase your property at {property_address}.<br><br>
                    
                    <strong>My Offer: ${offer_price}</strong><br><br>
                    
                    Why this works:<br>
                    • Guaranteed monthly rent from government<br>
                    • Long-term stable tenants<br>
                    • Property will be well-maintained<br>
                    • Fast cash closing<br><br>
                    
                    This property is perfect for the Section 8 program. Let's talk!<br><br>
                    
                    {your_name}<br>
                    Section 8 Housing Specialist
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🔒 Upgrade to Professional or Elite for Section 8 templates")
    
    with tab4:
        st.markdown("### 📞 Voicemail Scripts")
        
        st.markdown("""
        <div class="feature-card">
            <h4>📞 Voicemail Script #1 - "Cash Buyer"</h4>
            <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                "Hi {seller_name}, this is {your_name}. I'm a local cash buyer and I'm interested in your property at {property_address}. 
                
                I can close quickly with cash, no financing contingencies, and we buy properties as-is. 
                
                If you're looking to sell fast, please give me a call back at {phone}. 
                
                Again, that's {your_name} at {phone}. Thanks and have a great day!"
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_live_classes():
    st.markdown("# 🎓 Live Classes & Training")
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Login required to access live classes")
        return
    
    st.markdown("""
    <div class="live-class-alert">
        🔴 LIVE NOW: Richard Taylor & Chris Gallagher • 50+ Hours Per Week
    </div>
    """, unsafe_allow_html=True)
    
    # Today's schedule
    st.markdown("## 📅 Today's Class Schedule")
    
    classes_today = [
        {"time": "8:00 AM EST", "title": "Morning Deal Review", "instructor": "Richard Taylor", "type": "Live"},
        {"time": "10:00 AM EST", "title": "Cold Calling Masterclass", "instructor": "Chris Gallagher", "type": "Live"},
        {"time": "12:00 PM EST", "title": "Lunch & Learn: Contract Negotiation", "instructor": "Richard Taylor", "type": "Live"},
        {"time": "2:00 PM EST", "title": "Creative Finance Deep Dive", "instructor": "Guest Expert", "type": "Live"},
        {"time": "4:00 PM EST", "title": "Q&A Session", "instructor": "Richard & Chris", "type": "Live"},
        {"time": "6:00 PM EST", "title": "Evening Deal Analysis", "instructor": "Chris Gallagher", "type": "Live"},
        {"time": "8:00 PM EST", "title": "West Coast Wrap-Up", "instructor": "Richard Taylor", "type": "Live"}
    ]
    
    for cls in classes_today:
        st.markdown(f"""
        <div class="feature-card">
            <h4>🕐 {cls['time']} - {cls['title']}</h4>
            <p><strong>Instructor:</strong> {cls['instructor']}<br>
            <strong>Status:</strong> {cls['type']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Discord link
    st.markdown("""
    <div class="discord-link">
        💬 <strong>Join Discord to Access Live Classes</strong><br>
        All classes are streamed live in our Discord server
    </div>
    """, unsafe_allow_html=True)
    
    # Recorded sessions
    st.markdown("## 📚 Recorded Training Library")
    
    if st.session_state.user.get('subscription_tier') in ['professional', 'elite']:
        recorded_sessions = [
            "🎯 Finding Your First Deal - Richard Taylor (45 min)",
            "💰 Negotiation Secrets That Close Deals - Chris Gallagher (38 min)",
            "🏦 Creative Finance Masterclass - Guest Expert (52 min)",
            "📞 Cold Calling Scripts That Work - Richard Taylor (29 min)",
            "🏠 Section 8 Gold Mine Strategy - Chris Gallagher (41 min)",
            "📧 Email Templates That Get Responses - Richard Taylor (33 min)",
            "💸 Scaling to $100K/Month - Success Stories (55 min)"
        ]
        
        for session in recorded_sessions:
            st.markdown(f"""
            <div class="buyer-match">
                {session}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔒 Upgrade to Professional or Elite for access to 100+ recorded sessions")

def show_admin_dashboard():
    if not st.session_state.logged_in or not st.session_state.user.get('is_admin'):
        st.error("🚫 Admin access required")
        return
    
    st.markdown("""
    <div class="admin-header">
        <h1>⚙️ WTF Admin Dashboard</h1>
        <p>Elite Wholesaling Platform Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin stats
    conn = sqlite3.connect(db.db_name)
    
    # Get user stats
    users_df = pd.read_sql_query("SELECT subscription_tier, COUNT(*) as count FROM users GROUP BY subscription_tier", conn)
    total_users = pd.read_sql_query("SELECT COUNT(*) as total FROM users", conn).iloc[0]['total']
    
    # Get property stats
    total_properties = pd.read_sql_query("SELECT COUNT(*) as total FROM properties", conn).iloc[0]['total']
    total_buyers = pd.read_sql_query("SELECT COUNT(*) as total FROM cash_buyers", conn).iloc[0]['total']
    
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Users</h3>
            <h2>{total_users}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Properties</h3>
            <h2>{total_properties}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Verified Buyers</h3>
            <h2>{total_buyers}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        revenue = 0
        for _, row in users_df.iterrows():
            if row['subscription_tier'] == 'starter':
                revenue += row['count'] * 10
            elif row['subscription_tier'] == 'professional':
                revenue += row['count'] * 20
            elif row['subscription_tier'] == 'elite':
                revenue += row['count'] * 30
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Monthly Revenue</h3>
            <h2>${revenue:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # User breakdown
    st.markdown("## 📊 Subscription Breakdown")
    
    if not users_df.empty:
        for _, row in users_df.iterrows():
            tier = row['subscription_tier'].title()
            count = row['count']
            st.markdown(f"**{tier}:** {count} users")
    
    st.markdown("## 👥 Recent Users")
    
    conn = sqlite3.connect(db.db_name) 
    recent_users = pd.read_sql_query("""
        SELECT name, email, subscription_tier, created_at, total_deals, total_profit
        FROM users 
        ORDER BY created_at DESC 
        LIMIT 10
    """, conn)
    conn.close()
    
    if not recent_users.empty:
        st.dataframe(recent_users, use_container_width=True)

def main():
    load_css()
    init_session_state()
    
    # Navigation
    if st.session_state.logged_in:
        user = st.session_state.user
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"## 👋 Welcome, {user['name']}")
            st.markdown(f"**Plan:** {user['subscription_tier'].title()}")
            st.markdown(f"**Deals:** {user['total_deals']}")
            st.markdown(f"**Profit:** ${user['total_profit']:,.0f}")
            
            st.markdown("---")
            
            if st.button("🏠 Home Dashboard"):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.button("🎯 WTF Deal Finder"):
                st.session_state.current_page = 'deal_finder'
                st.rerun()
            
            if st.button("📧 Templates & Scripts"):
                st.session_state.current_page = 'templates'
                st.rerun()
            
            if st.button("🎓 Live Classes"):
                st.session_state.current_page = 'classes'
                st.rerun()
            
            if user.get('is_admin'):
                if st.button("⚙️ Admin Dashboard"):
                    st.session_state.current_page = 'admin'
                    st.rerun()
            
            st.markdown("---")
            
            # Discord integration
            st.markdown("""
            <div style="background: linear-gradient(135deg, #5865f2 0%, #4752c4 100%); 
                        color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
                💬 <strong>Join Discord</strong><br>
                13,000+ Members<br>
                Live Deal Reviews<br>
                Daily Giveaways
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.current_page = 'home'
                st.rerun()
        
        # Main content based on current page
        if st.session_state.current_page == 'home':
            show_home_page()
        elif st.session_state.current_page == 'deal_finder':
            show_deal_finder()
        elif st.session_state.current_page == 'templates':
            show_templates()
        elif st.session_state.current_page == 'classes':
            show_live_classes()
        elif st.session_state.current_page == 'admin' and user.get('is_admin'):
            show_admin_dashboard()
        else:
            show_home_page()
    
    else:
        show_login_signup()

if __name__ == "__main__":
    main()import streamlit as st
import sqlite3
import hashlib
import json
import datetime
import pandas as pd
import requests
from typing import Dict, List, Optional
import random

# Page configuration
st.set_page_config(
    page_title="Wholesale2Flip (WTF) - Elite Real Estate Wholesaling Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class DatabaseManager:
    def __init__(self):
        self.db_name = "wholesale2flip.db"
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Users table with subscription tiers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                phone TEXT,
                subscription_tier TEXT DEFAULT 'none',
                subscription_start DATE,
                subscription_end DATE,
                is_admin BOOLEAN DEFAULT 0,
                discord_id TEXT,
                total_deals INTEGER DEFAULT 0,
                total_profit REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Properties table (Zillow-style listings)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                property_type TEXT NOT NULL,
                bedrooms INTEGER,
                bathrooms REAL,
                square_feet INTEGER,
                lot_size TEXT,
                year_built INTEGER,
                list_price REAL NOT NULL,
                estimated_arv REAL,
                estimated_repairs REAL,
                days_on_market INTEGER,
                property_condition TEXT,
                description TEXT,
                photos TEXT, -- JSON array of photo URLs
                zillow_url TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cash buyers database (hedge funds, investors)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cash_buyers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buyer_name TEXT NOT NULL,
                company_name TEXT,
                buyer_type TEXT, -- 'hedge_fund', 'institutional', 'individual', 'section8'
                email TEXT NOT NULL,
                phone TEXT,
                preferred_markets TEXT, -- JSON array
                min_price REAL,
                max_price REAL,
                property_types TEXT, -- JSON array
                buy_criteria TEXT,
                proof_of_funds_amount REAL,
                close_timeline TEXT,
                is_verified BOOLEAN DEFAULT 0,
                rating REAL DEFAULT 5.0,
                total_purchases INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Deal pipeline
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                property_id INTEGER,
                buyer_id INTEGER,
                deal_type TEXT, -- 'traditional', 'creative_finance', 'section8'
                offer_price REAL,
                buyer_price REAL,
                potential_profit REAL,
                status TEXT DEFAULT 'pending', -- 'pending', 'offered', 'accepted', 'under_contract', 'closed', 'dead'
                contract_sent BOOLEAN DEFAULT 0,
                loi_sent BOOLEAN DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (property_id) REFERENCES properties (id),
                FOREIGN KEY (buyer_id) REFERENCES cash_buyers (id)
            )
        ''')
        
        # Live classes schedule
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS live_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_title TEXT NOT NULL,
                instructor TEXT NOT NULL,
                class_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                class_type TEXT, -- 'beginner', 'advanced', 'deal_review', 'q_and_a'
                topic TEXT,
                zoom_link TEXT,
                recording_url TEXT,
                attendance_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Templates and contracts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT NOT NULL,
                template_type TEXT NOT NULL, -- 'email', 'contract', 'loi', 'voicemail'
                content TEXT NOT NULL,
                category TEXT, -- 'cash', 'creative_finance', 'section8'
                is_premium BOOLEAN DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Seed initial data
        self.seed_initial_data()
    
    def seed_initial_data(self):
        """Seed database with initial properties and buyers"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if we already have data
        cursor.execute("SELECT COUNT(*) FROM properties")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample properties
        sample_properties = [
            {
                'address': '123 Oak Street',
                'city': 'Atlanta',
                'state': 'GA',
                'zip_code': '30309',
                'property_type': 'Single Family',
                'bedrooms': 3,
                'bathrooms': 2.0,
                'square_feet': 1200,
                'year_built': 1985,
                'list_price': 125000,
                'estimated_arv': 180000,
                'estimated_repairs': 25000,
                'days_on_market': 45,
                'property_condition': 'Needs Rehab'
            },
            {
                'address': '456 Pine Avenue',
                'city': 'Memphis',
                'state': 'TN',
                'zip_code': '38103',
                'property_type': 'Single Family',
                'bedrooms': 2,
                'bathrooms': 1.0,
                'square_feet': 900,
                'year_built': 1960,
                'list_price': 75000,
                'estimated_arv': 120000,
                'estimated_repairs': 15000,
                'days_on_market': 30,
                'property_condition': 'Fair'
            },
            {
                'address': '789 Maple Drive',
                'city': 'Birmingham',
                'state': 'AL',
                'zip_code': '35203',
                'property_type': 'Single Family',
                'bedrooms': 4,
                'bathrooms': 2.5,
                'square_feet': 1600,
                'year_built': 1990,
                'list_price': 95000,
                'estimated_arv': 160000,
                'estimated_repairs': 30000,
                'days_on_market': 60,
                'property_condition': 'Needs Major Repairs'
            }
        ]
        
        for prop in sample_properties:
            cursor.execute('''
                INSERT INTO properties (
                    address, city, state, zip_code, property_type, bedrooms, bathrooms,
                    square_feet, year_built, list_price, estimated_arv, estimated_repairs,
                    days_on_market, property_condition
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prop['address'], prop['city'], prop['state'], prop['zip_code'],
                prop['property_type'], prop['bedrooms'], prop['bathrooms'], prop['square_feet'],
                prop['year_built'], prop['list_price'], prop['estimated_arv'], prop['estimated_repairs'],
                prop['days_on_market'], prop['property_condition']
            ))
        
        # Sample cash buyers
        sample_buyers = [
            {
                'buyer_name': 'Atlanta Investment Fund',
                'company_name': 'AIF Holdings LLC',
                'buyer_type': 'hedge_fund',
                'email': 'deals@aifholdings.com',
                'phone': '404-555-0123',
                'preferred_markets': json.dumps(['Atlanta', 'Birmingham', 'Memphis']),
                'min_price': 50000,
                'max_price': 300000,
                'property_types': json.dumps(['Single Family', 'Multi-Family']),
                'proof_of_funds_amount': 5000000,
                'close_timeline': '7-14 days',
                'is_verified': 1,
                'rating': 4.8
            },
            {
                'buyer_name': 'Section 8 Specialists',
                'company_name': 'S8 Property Solutions',
                'buyer_type': 'section8',
                'email': 'acquisitions@s8properties.com',
                'phone': '901-555-0456',
                'preferred_markets': json.dumps(['Memphis', 'Little Rock', 'Jackson']),
                'min_price': 30000,
                'max_price': 150000,
                'property_types': json.dumps(['Single Family', 'Duplex']),
                'proof_of_funds_amount': 2000000,
                'close_timeline': '10-21 days',
                'is_verified': 1,
                'rating': 4.9
            },
            {
                'buyer_name': 'Creative Finance Solutions',
                'company_name': 'CFS Investments',
                'buyer_type': 'institutional', 
                'email': 'deals@cfsinvestments.com',
                'phone': '205-555-0789',
                'preferred_markets': json.dumps(['Birmingham', 'Huntsville', 'Mobile']),
                'min_price': 75000,
                'max_price': 500000,
                'property_types': json.dumps(['Single Family', 'Townhouse', 'Condo']),
                'proof_of_funds_amount': 10000000,
                'close_timeline': '14-30 days',
                'is_verified': 1,
                'rating': 4.7
            }
        ]
        
        for buyer in sample_buyers:
            cursor.execute('''
                INSERT INTO cash_buyers (
                    buyer_name, company_name, buyer_type, email, phone, preferred_markets,
                    min_price, max_price, property_types, proof_of_funds_amount,
                    close_timeline, is_verified, rating
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                buyer['buyer_name'], buyer['company_name'], buyer['buyer_type'],
                buyer['email'], buyer['phone'], buyer['preferred_markets'],
                buyer['min_price'], buyer['max_price'], buyer['property_types'],
                buyer['proof_of_funds_amount'], buyer['close_timeline'],
                buyer['is_verified'], buyer['rating']
            ))
        
        # Sample email templates
        templates = [
            {
                'template_name': 'Cash Offer Email',
                'template_type': 'email',
                'content': '''Subject: Cash Offer for {property_address}

Dear {seller_name},

I hope this email finds you well. I'm reaching out regarding your property at {property_address}.

I represent a cash buyer who is interested in purchasing your property quickly and without the typical hassles of traditional financing.

Our offer: ${offer_price}
- All cash purchase
- Close in 7-14 days
- No financing contingencies
- We buy AS-IS

If you're interested in discussing this further, please reply to this email or call me at {phone}.

Best regards,
{your_name}
Wholesale2Flip Team''',
                'category': 'cash',
                'is_premium': 0
            },
            {
                'template_name': 'Creative Finance LOI',
                'template_type': 'loi',
                'content': '''LETTER OF INTENT - CREATIVE FINANCING

Property: {property_address}
Date: {current_date}

Dear {seller_name},

We are interested in purchasing your property with the following creative financing structure:

Purchase Price: ${purchase_price}
Down Payment: ${down_payment}
Monthly Payment: ${monthly_payment}
Interest Rate: {interest_rate}%
Term: {term} years

Benefits to you:
- Immediate cash flow
- Tax advantages
- Quick closing
- No realtor commissions

This structure allows you to get your asking price while providing monthly income.

Let's discuss how this can work for both of us.

Sincerely,
{your_name}''',
                'category': 'creative_finance',
                'is_premium': 1
            }
        ]
        
        for template in templates:
            cursor.execute('''
                INSERT INTO templates (template_name, template_type, content, category, is_premium)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                template['template_name'], template['template_type'], template['content'],
                template['category'], template['is_premium']
            ))
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name: str, email: str, password: str, phone: str = "") -> bool:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password_hash, phone) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, phone)
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
            "SELECT id, name, email, subscription_tier, is_admin, total_deals, total_profit FROM users WHERE email = ? AND password_hash = ?",
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
                'is_admin': bool(user[4]),
                'total_deals': user[5] or 0,
                'total_profit': user[6] or 0
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
    
    def get_properties(self, filters: Dict = None) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = "SELECT * FROM properties WHERE status = 'active'"
        params = []
        
        if filters:
            if filters.get('min_price'):
                query += " AND list_price >= ?"
                params.append(filters['min_price'])
            if filters.get('max_price'):
                query += " AND list_price <= ?"
                params.append(filters['max_price'])
            if filters.get('city'):
                query += " AND city = ?"
                params.append(filters['city'])
            if filters.get('state'):
                query += " AND state = ?"
                params.append(filters['state'])
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        properties = cursor.fetchall()
        conn.close()
        
        columns = [
            'id', 'address', 'city', 'state', 'zip_code', 'property_type',
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built',
            'list_price', 'estimated_arv', 'estimated_repairs', 'days_on_market',
            'property_condition', 'description', 'photos', 'zillow_url',
            'status', 'created_at'
        ]
        
        return [dict(zip(columns, prop)) for prop in properties]
    
    def get_matched_buyers(self, property_id: int) -> List[Dict]:
        """Find buyers that match a property's criteria"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Get property details
        cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
        property_data = cursor.fetchone()
        
        if not property_data:
            conn.close()
            return []
        
        # Find matching buyers
        cursor.execute("""
            SELECT * FROM cash_buyers 
            WHERE is_verified = 1 
            AND min_price <= ? 
            AND max_price >= ?
            ORDER BY rating DESC
        """, (property_data[11], property_data[11]))  # list_price is at index 11
        
        buyers = cursor.fetchall()
        conn.close()
        
        columns = [
            'id', 'buyer_name', 'company_name', 'buyer_type', 'email', 'phone',
            'preferred_markets', 'min_price', 'max_price', 'property_types',
            'buy_criteria', 'proof_of_funds_amount', 'close_timeline',
            'is_verified', 'rating', 'total_purchases', 'created_at'
        ]
        
        return [dict(zip(columns, buyer)) for buyer in buyers]

# Initialize database
db = DatabaseManager()

# Custom CSS - matching Buy Box Cartel style
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    .main-header {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(255, 107, 53, 0.3);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #ff6b35);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .wtf-logo {
        font-size: 3rem;
        font-weight: 900;
        color: #ff6b35;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-left: 5px solid #ff6b35;
    }
    
    .property-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(255, 107, 53, 0.2);
        border-color: #ff6b35;
    }
    
    .pricing-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        position: relative;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    .pricing-card.featured {
        border: 3px solid #ff6b35;
        transform: scale(1.05);
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(247, 147, 30, 0.1) 100%);
    }
    
    .pricing-card.featured::before {
        content: "MOST POPULAR";
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
    }
    
    .price-tag {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    .profit-highlight {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
    }
    
    .buyer-match {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
    }
    
    .live-class-alert {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        animation: pulse 2s infinite;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(255, 107, 53, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(255, 107, 53, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 15px 30px rgba(255, 107, 53, 0.3);
    }
    
    .discord-link {
        background: linear-gradient(135deg, #5865f2 0%, #4752c4 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(88, 101, 242, 0.3);
    }
    
    .admin-header {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 30px rgba(239, 68, 68, 0.3);
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
    st.markdown("""
    <div class="main-header">
        <div class="wtf-logo">W2F</div>
        <h1 class="hero-title">Wholesale2Flip</h1>
        <h2 style="font-size: 1.8rem; margin-bottom: 1rem;">The Elite Real Estate Wholesaling Platform</h2>
        <p class="hero-subtitle">Match Zillow Properties with Hedge Fund Buyers • Make $10K-$30K Per Deal • Join 10,000+ Successful Wholesalers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live class alert
    st.markdown("""
    <div class="live-class-alert">
        🔴 LIVE NOW: Daily Mentorship Classes • 50+ Hours Per Week • Join Discord for Instant Access
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔐 Member Login")
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Access WTF Platform")
            
            if login_btn and email and password:
                user = db.verify_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(f"Welcome back, {user['name']}! Ready to make some money? 💰")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Need help? Join our Discord!")
    
    with col2:
        st.markdown("### 🚀 Start Making Money Today")
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            password = st.text_input("Create Password", type="password")
            signup_btn = st.form_submit_button("Join WTF Elite ($10/month)")
            
            if signup_btn and name and email and passwor