})
    
    # Financial insights
    if metrics['profit_potential'] > 50000:
        insights.append({
            'type': 'financial',
            'title': 'High Profit Potential',
            'description': f"Deal shows exceptional profit potential of ${metrics['profit_potential']:,.0f}. Consider multiple exit strategies.",
            'action': 'Secure contract quickly and evaluate all strategies',
            'confidence': 92
        })
    
    # Risk insights
    if property_data['year_built'] < 1950:
        insights.append({
            'type': 'risk',
            'title': 'Older Property Risk',
            'description': f"Property built in {property_data['year_built']} may have hidden issues (lead, asbestos, electrical).",
            'action': 'Budget extra for inspections and environmental testing',
            'confidence': 80
        })
    
    # Neighborhood insights
    if property_data['school_rating'] >= 8:
        insights.append({
            'type': 'opportunity',
            'title': 'Excellent School District',
            'description': f"School rating of {property_data['school_rating']}/10 attracts families and supports property values.",
            'action': 'Market to family buyers and emphasize school district',
            'confidence': 95
        })
    
    return insights

def generate_risk_analysis(property_data, metrics, market_data):
    """Generate comprehensive risk analysis"""
    
    risks = []
    risk_score = 0
    
    # Market risks
    if market_data['inventory_months'] > 6:
        risks.append({
            'category': 'Market',
            'risk': 'High Inventory',
            'description': f"{market_data['inventory_months']:.1f} months inventory indicates buyer's market",
            'impact': 'High',
            'mitigation': 'Price aggressively, consider rent-ready condition'
        })
        risk_score += 20
    
    # Property risks
    if property_data['year_built'] < 1960:
        risks.append({
            'category': 'Property',
            'risk': 'Older Construction',
            'description': 'Potential for outdated systems, materials, and code issues',
            'impact': 'Medium',
            'mitigation': 'Comprehensive inspection, extra rehab budget'
        })
        risk_score += 15
    
    # Financial risks
    if metrics['profit_potential'] < 15000:
        risks.append({
            'category': 'Financial',
            'risk': 'Thin Margins',
            'description': f"Low profit potential of ${metrics['profit_potential']:,.0f}",
            'impact': 'High',
            'mitigation': 'Negotiate lower price or find cost savings'
        })
        risk_score += 25
    
    # Location risks
    if property_data.get('crime_score', 50) < 40:
        risks.append({
            'category': 'Location',
            'risk': 'High Crime Area',
            'description': 'Crime score below 40 may affect resale and rental demand',
            'impact': 'Medium',
            'mitigation': 'Target cash buyers, price for quick sale'
        })
        risk_score += 10
    
    # Market timing risks
    if market_data['price_growth_yoy'] < 0:
        risks.append({
            'category': 'Timing',
            'risk': 'Declining Market',
            'description': f"Market down {abs(market_data['price_growth_yoy']):.1f}% year-over-year",
            'impact': 'High',
            'mitigation': 'Focus on cash flow, avoid speculation'
        })
        risk_score += 20
    
    # Overall risk assessment
    if risk_score <= 20:
        risk_level = 'Low'
        risk_color = '#10B981'
    elif risk_score <= 40:
        risk_level = 'Medium'
        risk_color = '#F59E0B'
    else:
        risk_level = 'High'
        risk_color = '#EF4444'
    
    return {
        'risks': risks,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'recommendation': 'Proceed with caution' if risk_score > 40 else 'Acceptable risk' if risk_score > 20 else 'Low risk opportunity'
    }

def generate_enhanced_comparables(property_data):
    """Generate enhanced comparable sales"""
    
    comparables = []
    base_price = property_data['list_price']
    
    for i in range(6):
        # Generate realistic comparable properties
        comp_price = base_price * np.random.uniform(0.85, 1.15)
        comp_sqft = property_data['square_feet'] * np.random.uniform(0.9, 1.1)
        days_ago = np.random.randint(15, 180)
        
        comparables.append({
            'address': f"{np.random.randint(100, 9999)} {np.random.choice(['Oak', 'Elm', 'Pine', 'Maple', 'Cedar', 'Birch'])} {np.random.choice(['St', 'Ave', 'Dr', 'Ln', 'Ct'])}",
            'price': comp_price,
            'sqft': comp_sqft,
            'price_per_sqft': comp_price / comp_sqft,
            'bedrooms': property_data['bedrooms'] + np.random.randint(-1, 2),
            'bathrooms': property_data['bathrooms'] + np.random.uniform(-0.5, 1.0),
            'year_built': property_data['year_built'] + np.random.randint(-10, 10),
            'days_ago': days_ago,
            'status': 'Sold',
            'dom': np.random.randint(5, 90),
            'distance': np.random.uniform(0.1, 2.5)
        })
    
    # Sort by relevance (price similarity)
    comparables.sort(key=lambda x: abs(x['price'] - base_price))
    
    return comparables

# Enhanced rendering functions
def render_enhanced_wholesale_analysis(wholesale_data):
    """Render enhanced wholesale analysis"""
    
    st.markdown("### 🏃 Wholesale Strategy Analysis")
    
    # Best scenario highlight
    best = wholesale_data['best_scenario']
    st.markdown(f"""
    <div class='success-metric'>
        <h4 style='color: #10B981; margin: 0;'>Recommended Assignment Fee: ${best['assignment_fee']:,}</h4>
        <p style='margin: 0.5rem 0;'>Net Profit: ${best['net_profit']:,} | ROI: {best['roi']:.0f}% | Timeline: {best['timeline']}</p>
        <p style='margin: 0; font-size: 0.9rem;'>Risk Level: {best['risk_level']} | Difficulty: {best['difficulty']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Assignment Fee Scenarios:**")
        for fee, scenario in list(wholesale_data['scenarios'].items())[:4]:
            st.markdown(f"""
            <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; margin: 0.5rem 0; border-radius: 10px;'>
                <strong>{fee}:</strong> ${scenario['net_profit']:,} profit ({scenario['roi']:.0f}% ROI)<br>
                <small>Timeline: {scenario['timeline']} | Difficulty: {scenario['difficulty']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Market Intelligence:**")
        st.info(f"""
        📊 **Strategy Grade:** {wholesale_data['strategy_grade']}
        
        📈 **Market Demand:** {wholesale_data['market_demand']}
        
        👥 **Buyer Pool:** {wholesale_data['buyer_pool_size']} potential buyers
        
        ⚡ **Speed:** Fastest exit strategy (7-30 days)
        """)

def render_enhanced_fix_flip_analysis(fix_flip_data):
    """Render enhanced fix and flip analysis"""
    
    st.markdown("### 🔨 Fix & Flip Strategy Analysis")
    
    best = fix_flip_data['best_scenario']
    st.markdown(f"""
    <div class='warning-metric'>
        <h4 style='color: #F59E0B; margin: 0;'>Best Scenario: ${best['gross_profit']:,} Profit</h4>
        <p style='margin: 0.5rem 0;'>ROI: {best['roi']:.1f}% | Annual ROI: {best['annual_roi']:.1f}% | Timeline: {best['timeline']}</p>
        <p style='margin: 0; font-size: 0.9rem;'>Risk: {best['risk_level']} | Complexity: {best['complexity']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Investment Breakdown:**")
        st.markdown(f"""
        - **Purchase Price:** ${best['purchase_price']:,}
        - **Rehab Cost:** ${best['rehab_cost']:,}
        - **Holding Costs:** ${best['holding_costs']:,}
        - **Selling Costs:** ${best['selling_costs']:,}
        - **Carrying Costs:** ${best['carrying_costs']:,}
        - **Buffer (10%):** ${best['unexpected_costs']:,}
        """)
        st.markdown(f"**Total Investment:** ${best['total_costs']:,}")
    
    with col2:
        st.markdown("**Market Analysis:**")
        st.info(f"""
        🎯 **Strategy Grade:** {fix_flip_data['strategy_grade']}
        
        🏘️ **Market Conditions:** {fix_flip_data['market_conditions']}
        
        📈 **Resale Demand:** {fix_flip_data['resale_demand']}
        
        ⚠️ **Risk Factors:** Market timing, rehab overruns
        """)

def render_enhanced_buy_hold_analysis(buy_hold_data):
    """Render enhanced buy and hold analysis"""
    
    st.markdown("### 🏠 Buy & Hold Strategy Analysis")
    
    best = buy_hold_data['best_scenario']
    st.markdown(f"""
    <div class='success-metric'>
        <h4 style='color: #10B981; margin: 0;'>Cash Flow: ${best['monthly_cash_flow']:,}/month</h4>
        <p style='margin: 0.5rem 0;'>Cash-on-Cash: {best['cash_on_cash']:.1f}% | Cap Rate: {best['cap_rate']:.1f}% | DSCR: {best['dscr']:.2f}</p>
        <p style='margin: 0; font-size: 0.9rem;'>10-Year IRR: {best['irr']:.1f}% | Year 10 Equity: ${best['year_10_equity']:,}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Expense breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Monthly Expense Breakdown:**")
        expenses = best['expense_breakdown']
        st.markdown(f"""
        - **PITI:** ${expenses['piti']:,.0f}
        - **Taxes:** ${expenses['taxes']:,.0f}
        - **Insurance:** ${expenses['insurance']:,.0f}
        - **Maintenance:** ${expenses['maintenance']:,.0f}
        - **Vacancy:** ${expenses['vacancy']:,.0f}
        - **Management:** ${expenses['management']:,.0f}
        - **CapEx:** ${expenses['capex']:,.0f}
        """)
        if expenses['hoa'] > 0:
            st.markdown(f"- **HOA:** ${expenses['hoa']:,.0f}")
    
    with col2:
        st.markdown("**Investment Metrics:**")
        st.success(f"""
        🏆 **Strategy Grade:** {buy_hold_data['strategy_grade']}
        
        🏠 **Rental Demand:** {buy_hold_data['rental_demand']}
        
        📈 **Rent Growth:** {buy_hold_data['rent_growth_potential']}
        
        💰 **Long-term wealth building strategy**
        """)

def render_enhanced_brrrr_analysis(brrrr_data):
    """Render enhanced BRRRR strategy analysis"""
    
    st.markdown("### 🔄 BRRRR Strategy Analysis")
    
    best = brrrr_data['best_scenario']
    st.markdown(f"""
    <div class='metric-card'>
        <h4 style='color: #8B5CF6; margin: 0;'>Capital Recovery: {best['recovery_percentage']:.1f}%</h4>
        <p style='margin: 0.5rem 0;'>Cash Recovered: ${best['cash_recovered']:,} | Left in Deal: ${best['cash_left_in_deal']:,}</p>
        <p style='margin: 0; font-size: 0.9rem;'>Infinite ROI Potential | Scale: {best['properties_per_year']} properties/year</p>
    </div>
    """, unsafe_allow_html=True)
    
    # BRRRR breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**BRRRR Process:**")
        st.markdown(f"""
        1. **Buy:** ${best['purchase_price']:,}
        2. **Rehab:** ${best['rehab_cost']:,}
        3. **Rent:** ${best['monthly_cash_flow']:,}/month
        4. **Refinance:** ${best['refi_amount']:,} (75% ARV)
        5. **Repeat:** Scale with recovered capital
        """)
    
    with col2:
        st.markdown("**Scaling Potential:**")
        st.info(f"""
        🚀 **Strategy Grade:** {brrrr_data['strategy_grade']}
        
        🏦 **Refinance Likelihood:** {brrrr_data['refinance_likelihood']}
        
        📈 **Scaling Potential:** {brrrr_data['scaling_potential']}
        
        💼 **Portfolio Growth:** ${best['annual_portfolio_growth']:,}/year
        """)

def render_creative_finance_analysis(creative_data):
    """Render creative financing analysis"""
    
    st.markdown("### 💡 Creative Finance Strategies")
    
    best = creative_data['best_strategy']
    st.markdown(f"""
    <div class='warning-metric'>
        <h4 style='color: #F59E0B; margin: 0;'>Best Strategy: {best['name']}</h4>
        <p style='margin: 0.5rem 0;'>ROI: {best['roi']:.1f}% | Monthly Cash Flow: ${best['monthly_cash_flow']:,}</p>
        <p style='margin: 0; font-size: 0.9rem;'>Risk: {best['risk_level']} | {best['legality']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategy details
    for name, strategy in creative_data['strategies'].items():
        st.markdown(f"""
        <div class='deal-card'>
            <h5 style='color: #F59E0B; margin: 0;'>{strategy['name']}</h5>
            <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                <span>Down Payment: ${strategy['down_payment']:,}</span>
                <span>ROI: {strategy['roi']:.1f}%</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>Risk: {strategy['risk_level']}</span>
                <span>Legal: {strategy['legality']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.warning(f"⚠️ **Legal Disclaimer:** {creative_data['legal_requirements']}")

def render_strategy_comparison(strategies):
    """Render strategy comparison chart"""
    
    st.markdown("### 📊 Strategy Comparison")
    
    # Create comparison data
    strategy_names = []
    rois = []
    risks = []
    timelines = []
    
    # Wholesale
    wholesale_best = strategies['wholesale']['best_scenario']
    strategy_names.append('Wholesale')
    rois.append(wholesale_best['roi'])
    risks.append(1)  # Low risk
    timelines.append(15)  # Days
    
    # Fix & Flip
    flip_best = strategies['fix_flip']['best_scenario']
    strategy_names.append('Fix & Flip')
    rois.append(flip_best['annual_roi'])
    risks.append(3)  # Medium-High risk
    timelines.append(180)  # Days
    
    # Buy & Hold
    hold_best = strategies['buy_hold']['best_scenario']
    strategy_names.append('Buy & Hold')
    rois.append(hold_best['cash_on_cash'])
    risks.append(2)  # Medium risk
    timelines.append(3650)  # 10 years in days
    
    # BRRRR
    brrrr_best = strategies['brrrr']['best_scenario']
    strategy_names.append('BRRRR')
    rois.append(min(brrrr_best['cash_on_cash'], 100))  # Cap at 100% for chart
    risks.append(3)  # Medium-High risk
    timelines.append(365)  # 1 year
    
    # Create comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        # ROI comparison
        fig_roi = px.bar(
            x=strategy_names, 
            y=rois,
            title='ROI Comparison (%)',
            color=rois,
            color_continuous_scale='Viridis'
        )
        fig_roi.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with col2:
        # Risk vs Timeline
        fig_risk = px.scatter(
            x=timelines,
            y=risks,
            text=strategy_names,
            title='Risk vs Timeline',
            size=[20, 20, 20, 20],
            color=rois
        )
        fig_risk.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title='Timeline (Days)',
            yaxis_title='Risk Level (1-5)'
        )
        fig_risk.update_traces(textposition="top center")
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Recommendation matrix
    st.markdown("**Strategy Recommendations:**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.success("""
        **🏃 Wholesale**
        - Quick cash
        - Low risk
        - No capital needed
        - Market agnostic
        """)
    
    with col2:
        st.warning("""
        **🔨 Fix & Flip**
        - High profits
        - Active involvement
        - Market dependent
        - Higher risk
        """)
    
    with col3:
        st.info("""
        **🏠 Buy & Hold**
        - Passive income
        - Long-term wealth
        - Tax benefits
        - Lower returns
        """)
    
    with col4:
        st.error("""
        **🔄 BRRRR**
        - Scale quickly
        - Infinite ROI
        - Complex process
        - Refinance risk
        """)

def render_enhanced_comparables_analysis(comparables):
    """Render enhanced comparables analysis"""
    
    if not comparables:
        st.info("No comparable sales data available")
        return
    
    # Summary statistics
    avg_price = np.mean([comp['price'] for comp in comparables])
    avg_psf = np.mean([comp['price_per_sqft'] for comp in comparables])
    median_dom = np.median([comp['dom'] for comp in comparables])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Sale Price", f"${avg_price:,.0f}")
    
    with col2:
        st.metric("Average $/SqFt", f"${avg_psf:.0f}")
    
    with col3:
        st.metric("Median DOM", f"{median_dom:.0f} days")
    
    # Detailed comparables table
    st.markdown("**Comparable Sales:**")
    
    for i, comp in enumerate(comparables):
        days_text = f"{comp['days_ago']} days ago"
        
        st.markdown(f"""
        <div class='deal-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h5 style='color: white; margin: 0;'>{comp['address']}</h5>
                    <small style='color: #9CA3AF;'>{comp['bedrooms']}bd/{comp['bathrooms']:.1f}ba • {comp['sqft']:,.0f} sqft • Built {comp['year_built']}</small>
                </div>
                <div style='text-align: right;'>
                    <p style='color: #10B981; margin: 0; font-weight: bold;'>${comp['price']:,.0f}</p>
                    <p style='color: #8B5CF6; margin: 0;'>${comp['price_per_sqft']:.0f}/sqft</p>
                    <small style='color: #9CA3AF;'>{days_text} • {comp['distance']:.1f} mi</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_enhanced_market_analysis(market_data):
    """Render enhanced market analysis"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Market Fundamentals:**")
        st.metric("Median Home Price", f"${market_data['median_home_price']:,}")
        st.metric("Days on Market", f"{market_data['days_on_market']}")
        st.metric("Inventory", f"{market_data['inventory_months']:.1f} months")
        st.metric("Market Temp", market_data['market_temperature'])
    
    with col2:
        st.markdown("**Price Trends:**")
        st.metric("Price Growth YoY", f"{market_data['price_growth_yoy']:+.1f}%")
        st.metric("Rent Growth YoY", f"{market_data['rent_growth_yoy']:+.1f}%")
        st.metric("Median Rent", f"${market_data['median_rent']:,}")
        st.metric("Cap Rate", f"{market_data['cap_rate']:.1f}%")
    
    with col3:
        st.markdown("**Area Metrics:**")
        st.metric("Population Growth", f"{market_data['population_growth']:+.1f}%")
        st.metric("Job Growth", f"{market_data['job_growth']:+.1f}%")
        st.metric("Crime Index", f"{market_data['crime_index']}/100")
        st.metric("School Rating", f"{market_data['school_ratings']:.1f}/10")
    
    # Market trends chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_trend = [market_data['median_home_price'] * (1 + np.random.uniform(-0.02, 0.02)) for _ in months]
    
    fig_trend = px.line(
        x=months, 
        y=price_trend,
        title='Market Price Trend',
        labels={'x': 'Month', 'y': 'Median Price ($)'}
    )
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    fig_trend.update_traces(line_color='#10B981', line_width=3)
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Investment climate
    investor_activity = market_data['investor_activity']
    rental_demand = market_data['rental_demand']
    
    if investor_activity == 'Very High' and rental_demand == 'Very High':
        market_grade = 'A+'
        market_color = '#10B981'
    elif investor_activity in ['High', 'Very High'] and rental_demand in ['High', 'Very High']:
        market_grade = 'A'
        market_color = '#10B981'
    elif investor_activity == 'Medium' or rental_demand == 'Medium':
        market_grade = 'B'
        market_color = '#F59E0B'
    else:
        market_grade = 'C'
        market_color = '#EF4444'
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0; text-align: center;'>
        <h3 style='color: {market_color}; margin: 0;'>Market Investment Grade: {market_grade}</h3>
        <p style='color: white; margin: 0.5rem 0;'>
            Investor Activity: {investor_activity} | Rental Demand: {rental_demand}
        </p>
        <p style='color: white; margin: 0; font-size: 0.9rem;'>
            Foreclosure Rate: {market_data['foreclosure_rate']:.1f}% | 
            New Construction: {market_data['new_construction']} units | 
            Flip Activity: {market_data['flip_activity']} deals
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_ai_insights(ai_insights):
    """Render AI-powered insights"""
    
    if not ai_insights:
        st.info("No AI insights available")
        return
    
    insight_colors = {
        'opportunity': '#10B981',
        'risk': '#EF4444',
        'market': '#8B5CF6',
        'strategy': '#F59E0B',
        'financial': '#3B82F6'
    }
    
    for insight in ai_insights:
        color = insight_colors.get(insight['type'], '#6B7280')
        confidence = insight['confidence']
        
        # Confidence indicator
        if confidence >= 90:
            confidence_text = 'Very High'
            confidence_color = '#10B981'
        elif confidence >= 80:
            confidence_text = 'High'
            confidence_color = '#8B5CF6'
        elif confidence >= 70:
            confidence_text = 'Medium'
            confidence_color = '#F59E0B'
        else:
            confidence_text = 'Low'
            confidence_color = '#EF4444'
        
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.08); border-left: 5px solid {color}; 
                    padding: 1.5rem; margin: 1rem 0; border-radius: 0 15px 15px 0;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                <h4 style='color: {color}; margin: 0; text-transform: capitalize;'>
                    {insight['type']}: {insight['title']}
                </h4>
                <span style='background: {confidence_color}; color: white; padding: 0.3rem 0.8rem; 
                             border-radius: 15px; font-size: 0.8rem; font-weight: bold;'>
                    {confidence_text} ({confidence}%)
                </span>
            </div>
            <p style='color: white; margin: 0.5rem 0; line-height: 1.6;'>{insight['description']}</p>
            <p style='color: #10B981; margin: 0; font-weight: bold;'>💡 Action: {insight['action']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_risk_assessment(risk_analysis):
    """Render comprehensive risk assessment"""
    
    if not risk_analysis:
        st.info("No risk analysis available")
        return
    
    risk_score = risk_analysis['risk_score']
    risk_level = risk_analysis['risk_level']
    risk_color = risk_analysis['risk_color']
    
    # Risk score display
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.15) 50%, rgba(16, 185, 129, 0.15) 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0; text-align: center;'>
        <h3 style='color: {risk_color}; margin: 0;'>Risk Assessment: {risk_level}</h3>
        <p style='color: white; margin: 0.5rem 0; font-size: 1.2rem;'>Risk Score: {risk_score}/100</p>
        <p style='color: white; margin: 0; font-size: 0.9rem;'>{risk_analysis['recommendation']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk breakdown
    if risk_analysis['risks']:
        st.markdown("**Identified Risks:**")
        
        for risk in risk_analysis['risks']:
            impact_colors = {'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'}
            impact_color = impact_colors.get(risk['impact'], '#6B7280')
            
            st.markdown(f"""
            <div class='deal-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <h5 style='color: white; margin: 0;'>{risk['category']}: {risk['risk']}</h5>
                    <span style='background: {impact_color}; color: white; padding: 0.2rem 0.6rem; 
                                 border-radius: 10px; font-size: 0.8rem;'>{risk['impact']} Impact</span>
                </div>
                <p style='color: #9CA3AF; margin: 0.5rem 0; font-size: 0.9rem;'>{risk['description']}</p>
                <p style='color: #10B981; margin: 0; font-size: 0.9rem;'><strong>Mitigation:</strong> {risk['mitigation']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No significant risks identified")

# Helper functions for database operations
def save_ultimate_analysis_to_db(user_id, property_data, metrics, analysis_result):
    """Save complete analysis to database"""
    
    try:
        conn = services['db'].get_connection()
        cursor = conn.cursor()
        
        property_id = str(uuid.uuid4())
        
        # Prepare property data for database
        property_insert = {
            'id': property_id,
            'user_id': user_id,
            'address': property_data['address'],
            'city': property_data['city'],
            'state': property_data['state'],
            'zip_code': property_data.get('zip_code', ''),
            'property_type': property_data['property_type'],
            'bedrooms': property_data['bedrooms'],
            'bathrooms': property_data['bathrooms'],
            'square_feet': property_data['square_feet'],
            'year_built': property_data['year_built'],
            'list_price': property_data['list_price'],
            'zestimate': property_data.get('zestimate', 0),
            'rent_estimate': property_data.get('rent_estimate', 0),
            'arv': metrics['arv'],
            'rehab_cost': metrics['rehab_cost'],
            'max_offer': metrics['max_offers']['70_percent'],
            'profit_potential': metrics['profit_potential'],
            'condition': property_data.get('condition', 'fair'),
            'days_on_market': property_data.get('days_on_market', 0),
            'price_per_sqft': property_data.get('price_per_sqft', 0),
            'neighborhood': property_data.get('neighborhood', ''),
            'school_rating': property_data.get('school_rating', 0),
            'crime_score': property_data.get('crime_score', 0),
            'walkability': property_data.get('walkability', 0),
            'property_taxes': property_data.get('property_taxes', 0),
            'hoa_fees': property_data.get('hoa_fees', 0),
            'data_sources': ','.join(property_data.get('data_sources', [])),
            'analysis_data': json.dumps({
                'metrics': metrics,
                'strategies': analysis_result.get('strategies', {}),
                'market_data': analysis_result.get('market_data', {}),
                'ai_insights': analysis_result.get('ai_insights', []),
                'risk_analysis': analysis_result.get('risk_analysis', {}),
                'grade': metrics['overall_grade'],
                'grade_score': metrics['grade_score'],
                'confidence_level': metrics['confidence_level']
            }),
            'images': json.dumps([]),
            'notes': f"Analysis completed on {datetime.now().strftime('%Y-%m-%d %H:%M')}. Grade: {metrics['overall_grade']} ({metrics['grade_score']}/100)"
        }
        
        # Insert property
        columns = ', '.join(property_insert.keys())
        placeholders = ', '.join(['?' for _ in property_insert.values()])
        
        cursor.execute(f'''
            INSERT INTO properties ({columns})
            VALUES ({placeholders})
        ''', list(property_insert.values()))
        
        conn.commit()
        conn.close()
        
        return property_id
        
    except Exception as e:
        logger.error(f"Failed to save analysis: {str(e)}")
        return None

def create_deal_from_analysis(user_id, property_data, metrics):
    """Create deal from analysis"""
    
    try:
        conn = services['db'].get_connection()
        cursor = conn.cursor()
        
        deal_id = str(uuid.uuid4())
        
        # Create deal record
        deal_data = {
            'id': deal_id,
            'user_id': user_id,
            'title': f"{property_data['address']} - {metrics['recommended_strategy']}",
            'property_id': None,  # Would link to property if saved
            'lead_id': None,
            'buyer_id': None,
            'contract_price': metrics['max_offers']['70_percent'],
            'assignment_fee': 15000,  # Default assignment fee
            'status': 'lead',
            'stage': 'prospecting',
            'probability': max(10, min(90, metrics['grade_score'])),
            'expected_close_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'profit_margin': metrics['profit_potential'],
            'roi': (metrics['profit_potential'] / metrics['max_offers']['70_percent'] * 100) if metrics['max_offers']['70_percent'] > 0 else 0,
            'deal_type': 'wholesale',
            'notes': f"Created from analysis. Grade: {metrics['overall_grade']} ({metrics['grade_score']}/100). ARV: ${metrics['arv']:,.0f}",
            'milestones': json.dumps([
                {'milestone': 'Analysis Complete', 'date': datetime.now().isoformat(), 'completed': True},
                {'milestone': 'Contact Seller', 'date': '', 'completed': False},
                {'milestone': 'Submit Offer', 'date': '', 'completed': False},
                {'milestone': 'Under Contract', 'date': '', 'completed': False},
                {'milestone': 'Find Buyer', 'date': '', 'completed': False},
                {'milestone': 'Close Deal', 'date': '', 'completed': False}
            ])
        }
        
        columns = ', '.join(deal_data.keys())
        placeholders = ', '.join(['?' for _ in deal_data.values()])
        
        cursor.execute(f'''
            INSERT INTO deals ({columns})
            VALUES ({placeholders})
        ''', list(deal_data.values()))
        
        conn.commit()
        conn.close()
        
        return deal_id
        
    except Exception as e:
        logger.error(f"Failed to create deal: {str(e)}")
        return None

def generate_ultimate_pdf_report(property_data, metrics, strategies, market_data, ai_insights):
    """Generate comprehensive PDF report"""
    
    try:
        # This would normally use a PDF generation library like ReportLab
        # For now, we'll create a mock PDF-like content
        
        report_content = f"""
WTF PLATFORM - COMPREHENSIVE DEAL ANALYSIS REPORT
================================================================

PROPERTY INFORMATION
-------------------
Address: {property_data['address']}, {property_data['city']}, {property_data['state']}
Property Type: {property_data['property_type'].replace('_', ' ').title()}
Bedrooms: {property_data['bedrooms']} | Bathrooms: {property_data['bathrooms']}
Square Feet: {property_data['square_feet']:,} | Year Built: {property_data['year_built']}
List Price: ${property_data['list_price']:,}

ANALYSIS SUMMARY
--------------
Overall Grade: {metrics['overall_grade']} ({metrics['grade_score']}/100)
Confidence Level: {metrics['confidence_level']}%
Recommended Strategy: {metrics['recommended_strategy']}

KEY METRICS
----------
ARV (After Repair Value): ${metrics['arv']:,}
Estimated Rehab Cost: ${metrics['rehab_cost']:,}
Max Offer (70% Rule): ${metrics['max_offers']['70_percent']:,}
Profit Potential: ${metrics['profit_potential']:,}

INVESTMENT STRATEGIES
-------------------
1. WHOLESALE STRATEGY
   Best Assignment Fee: ${strategies['wholesale']['best_scenario']['assignment_fee']:,}
   Net Profit: ${strategies['wholesale']['best_scenario']['net_profit']:,}
   ROI: {strategies['wholesale']['best_scenario']['roi']:.1f}%

2. FIX & FLIP STRATEGY
   Gross Profit: ${strategies['fix_flip']['best_scenario']['gross_profit']:,}
   ROI: {strategies['fix_flip']['best_scenario']['roi']:.1f}%
   Timeline: {strategies['fix_flip']['best_scenario']['timeline']}

3. BUY & HOLD STRATEGY
   Monthly Cash Flow: ${strategies['buy_hold']['best_scenario']['monthly_cash_flow']:,}
   Cash-on-Cash Return: {strategies['buy_hold']['best_scenario']['cash_on_cash']:.1f}%
   Cap Rate: {strategies['buy_hold']['best_scenario']['cap_rate']:.1f}%

MARKET ANALYSIS
--------------
Median Home Price: ${market_data['median_home_price']:,}
Days on Market: {market_data['days_on_market']}
Price Growth YoY: {market_data['price_growth_yoy']:+.1f}%
Market Temperature: {market_data['market_temperature']}

AI INSIGHTS
-----------
"""
        
        for insight in ai_insights:
            report_content += f"""
{insight['type'].upper()}: {insight['title']}
{insight['description']}
Action: {insight['action']}
Confidence: {insight['confidence']}%
"""
        
        report_content += f"""

DISCLAIMER
----------
This analysis is for informational purposes only and should not be considered as investment advice. 
Property values, market conditions, and investment returns can vary significantly. Always conduct 
your own due diligence and consult with qualified professionals before making investment decisions.

Report generated by WTF Platform on {datetime.now().strftime('%Y-%m-%d at %H:%M')}
Data sources: {', '.join(property_data.get('data_sources', ['Estimates']))}

© 2024 WTF Platform - Wholesale on Steroids
"""
        
        # Convert to bytes (mock PDF)
        return report_content.encode('utf-8')
        
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {str(e)}")
        return None

# Continue with the main application routing
def main():
    """Main application router"""
    
    # Landing page or authenticated app
    if not st.session_state.authenticated:
        render_ultimate_landing_page()
    else:
        # Render sidebar and get selected page
        selected_page = render_ultimate_sidebar()
        
        # Route to selected page
        if selected_page == "dashboard":
            render_ultimate_dashboard()
        elif selected_page == "deal_analyzer":
            render_ultimate_deal_analyzer()
        elif selected_page == "lead_manager":
            render_lead_manager()
        elif selected_page == "deal_pipeline":
            render_deal_pipeline()
        elif selected_page == "buyer_network":
            render_buyer_network()
        elif selected_page == "contract_generator":
            render_contract_generator()
        elif selected_page == "loi_generator":
            render_loi_generator()
        elif selected_page == "email_campaigns":
            render_email_campaigns()
        elif selected_page == "lightning_leads":
            render_lightning_leads()
        elif selected_page == "analytics":
            render_analytics()
        elif selected_page == "mobile_tools":
            render_mobile_tools()
        elif selected_page == "account_settings":
            render_account_settings()
        elif selected_page == "admin_dashboard":
            render_admin_dashboard()
        elif selected_page == "platform_analytics":
            render_platform_analytics()
        elif selected_page == "user_management":
            render_user_management()
        elif selected_page == "revenue_dashboard":
            render_revenue_dashboard()
        elif selected_page == "buyer_dashboard":
            render_buyer_dashboard()
        elif selected_page == "available_deals":
            render_available_deals()
        elif selected_page == "market_analysis":
            render_enhanced_market_analysis({
                'median_home_price': 350000,
                'median_rent': 2100,
                'days_on_market': 35,
                'price_growth_yoy': 8.5,
                'rent_growth_yoy': 4.2,
                'market_temperature': 'Hot',
                'investor_activity': 'High',
                'rental_demand': 'Very High'
            })
        else:
            st.error(f"Page '{selected_page}' not implemented yet")
            st.info("This feature is coming soon! The development team is working on implementing all features.")

# Additional feature implementations (placeholders for now)
def render_lead_manager():
    """Render lead management system"""
    st.markdown('<h1 class="main-header">📞 Lead Manager</h1>', unsafe_allow_html=True)
    st.info("🚧 Lead Manager coming soon! This will include lead tracking, scoring, and follow-up automation.")

def render_deal_pipeline():
    """Render deal pipeline management"""
    st.markdown('<h1 class="main-header">📋 Deal Pipeline</h1>', unsafe_allow_html=True)
    st.info("🚧 Deal Pipeline coming soon! This will include deal tracking, milestone management, and closing coordination.")

def render_buyer_network():
    """Render buyer network system"""
    st.markdown('<h1 class="main-header">👥 Buyer Network</h1>', unsafe_allow_html=True)
    st.info("🚧 Buyer Network coming soon! This will include verified buyer database, deal matching, and buyer communication tools.")

def render_contract_generator():
    """Render contract generation system"""
    st.markdown('<h1 class="main-header">📄 Contract Generator</h1>', unsafe_allow_html=True)
    st.info("🚧 Contract Generator coming soon! This will include professional contract templates, e-signature, and legal compliance.")

def render_loi_generator():
    """Render LOI generation system"""
    st.markdown('<h1 class="main-header">📝 LOI Generator</h1>', unsafe_allow_html=True)
    st.info("🚧 LOI Generator coming soon! This will include professional LOI templates, automated calculations, and tracking.")

def render_email_campaigns():
    """Render email campaign system"""
    st.markdown('<h1 class="main-header">📧 Email Campaigns</h1>', unsafe_allow_html=True)
    st.info("🚧 Email Campaigns coming soon! This will include lead nurturing, buyer outreach, and automated follow-ups.")

def render_lightning_leads():
    """Render lightning leads system"""
    st.markdown('<h1 class="main-header">⚡ Lightning Leads</h1>', unsafe_allow_html=True)
    st.info("🚧 Lightning Leads coming soon! This will include skip tracing, motivated seller identification, and lead scoring.")

def render_analytics():
    """Render analytics dashboard"""
    st.markdown('<h1 class="main-header">📊 Analytics</h1>', unsafe_allow_html=True)
    st.info("🚧 Analytics Dashboard coming soon! This will include performance tracking, ROI analysis, and business intelligence.")

def render_mobile_tools():
    """Render mobile tools"""
    st.markdown('<h1 class="main-header">📱 Mobile Tools</h1>', unsafe_allow_html=True)
    st.info("🚧 Mobile Tools coming soon! This will include mobile-optimized interfaces and on-the-go functionality.")

def render_account_settings():
    """Render account settings"""
    st.markdown('<h1 class="main-header">⚙️ Account Settings</h1>', unsafe_allow_html=True)
    st.info("🚧 Account Settings coming soon! This will include profile management, subscription control, and preferences.")

def render_admin_dashboard():
    """Render admin dashboard"""
    st.markdown('<h1 class="main-header">🏠 Admin Dashboard</h1>', unsafe_allow_html=True)
    st.info("🚧 Admin Dashboard coming soon! This will include platform overview, user management, and system monitoring.")

def render_platform_analytics():
    """Render platform analytics"""
    st.markdown('<h1 class="main-header">📊 Platform Analytics</h1>', unsafe_allow_html=True)
    st.info("🚧 Platform Analytics coming soon! This will include usage statistics, revenue tracking, and performance metrics.")

def render_user_management():
    """Render user management"""
    st.markdown('<h1 class="main-header">👥 User Management</h1>', unsafe_allow_html=True)
    st.info("🚧 User Management coming soon! This will include user administration, role management, and access control.")

def render_revenue_dashboard():
    """Render revenue dashboard"""
    st.markdown('<h1 class="main-header">💰 Revenue Dashboard</h1>', unsafe_allow_html=True)
    st.info("🚧 Revenue Dashboard coming soon! This will include subscription tracking, payment processing, and financial reporting.")

def render_buyer_dashboard():
    """Render buyer dashboard"""
    st.markdown('<h1 class="main-header">🏠 Buyer Dashboard</h1>', unsafe_allow_html=True)
    st.info("🚧 Buyer Dashboard coming soon! This will include deal alerts, portfolio tracking, and investment analysis.")

def render_available_deals():
    """Render available deals"""
    st.markdown('<h1 class="main-header">🔍 Available Deals</h1>', unsafe_allow_html=True)
    st.info("🚧 Available Deals coming soon! This will include deal marketplace, filtering, and purchase options.")

# Run the application
if __name__ == "__main__":
    main()
