# 🏠 Wholesale2Flip - Complete Real Estate Wholesaling Platform

A comprehensive, professional-grade real estate wholesaling platform built with Streamlit, featuring AI-powered calculations, automated contract generation, and complete deal management.

## 🚀 Live Demo

Deploy to Streamlit Cloud: [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## ✨ Features

### 🎯 Core Platform Features
- **AI-Powered Deal Analysis** - GPT integration for accurate calculations
- **Professional Contract Generation** - Wholesale-friendly legal documents
- **Letter of Intent (LOI) Generator** - Automated offer letters
- **Complete Deal Pipeline** - From analysis to closing
- **Admin Dashboard** - Full disposition team management
- **Multi-Tier Subscriptions** - Flexible pricing for all users

### 💡 Smart Calculations
- **70% Rule Calculator** - Industry-standard quick analysis
- **ARV Estimation** - AI-assisted after repair value
- **Profit Margin Analysis** - Real-time ROI calculations
- **Holding Cost Calculator** - Comprehensive expense tracking
- **Deal Quality Scoring** - Automated deal grading

### 📄 Legal Documents
- **Wholesale Purchase Agreements** - Legally protective contracts
- **Assignment Clauses** - Proper wholesale language
- **Letters of Intent** - Professional offer presentations
- **Custom Contract Templates** - Tailored to your state/market

### 🛠️ Admin Tools
- **Deal Disposition Dashboard** - Complete pipeline overview
- **Student Contact Management** - Direct access to user details
- **Deal Status Tracking** - From submission to closing
- **Analytics & Reporting** - Performance insights
- **User Management** - Subscription and access control

## 💎 Subscription Tiers

### 🥉 Starter - $10/month
- ✅ Basic Deal Calculator
- ✅ Simple Contract Templates
- ✅ 5 Deals per Month
- ✅ Email Support
- ✅ Basic Analytics

### 🥈 Professional - $20/month (Most Popular)
- ✅ **Everything in Starter**
- ✅ AI-Powered Calculations
- ✅ Advanced Contract Suite
- ✅ Unlimited Deals
- ✅ LOI Generation
- ✅ Priority Support
- ✅ Deal Status Tracking

### 🥇 Enterprise - $30/month
- ✅ **Everything in Professional**
- ✅ Custom Contract Templates
- ✅ Disposition Team Access
- ✅ Advanced Analytics Dashboard
- ✅ White-Label Options
- ✅ Dedicated Account Manager
- ✅ API Access

## 🛠️ Tech Stack

- **Frontend:** Streamlit + Custom CSS
- **Backend:** Python with SQLite/PostgreSQL
- **AI Integration:** OpenAI GPT API
- **Authentication:** Secure password hashing
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Deployment:** Streamlit Cloud / Heroku / Docker

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/wholesale2flip.git
cd wholesale2flip

# Install dependencies
pip install -r requirements.txt

# Set up your secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your OpenAI API key

# Run the application
streamlit run app.py
```

### Option 2: Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your forked repository
5. Add your secrets in the Streamlit Cloud dashboard
6. Deploy!

## 🔧 Configuration

### Environment Setup

1. **OpenAI API Key**: Required for AI-powered calculations
   ```toml
   [api_keys]
   OPENAI_API_KEY = "your-api-key-here"
   ```

2. **Admin Account**: Set up the initial admin user
   ```toml
   [admin]
   ADMIN_EMAIL = "admin@wholesale2flip.com"
   ADMIN_PASSWORD = "secure-password"
   ```

### Database Schema

The platform automatically creates the following tables:

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    subscription_tier TEXT DEFAULT 'none',
    subscription_start DATE,
    subscription_end DATE,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Deals Table
```sql
CREATE TABLE deals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    property_address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    property_type TEXT NOT NULL,
    -- ... (complete schema in app.py)
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 👥 User Roles

### 👨‍💼 Admin Users
- Access to admin dashboard
- View all deals from all users
- Contact information for disposition
- Deal status management
- User subscription management
- Platform analytics

### 👨‍💻 Regular Users (Students)
- Deal calculator access
- Contract generation
- Personal deal history
- Subscription management
- Document downloads

## 📊 Admin Dashboard Features

### Deal Management
- **Complete Deal Pipeline** - View all submitted deals
- **Student Contact Info** - Direct access to user details
- **Deal Status Updates** - Track progress from submission to close
- **Document Generation** - View contracts and LOIs for any deal
- **Filter & Search** - Find deals by status, type, profit margin

### User Management
- **Subscription Overview** - See all active subscriptions
- **User Analytics** - Registration and usage statistics
- **Plan Distribution** - Visual breakdown of subscription tiers

### Analytics
- **Deal Metrics** - Average profit margins, ARV, etc.
- **Monthly Trends** - Deal submission patterns
- **Performance Insights** - Platform usage analytics

## 🔒 Security Features

- **Secure Authentication** - SHA-256 password hashing
- **Session Management** - Streamlit session state
- **SQL Injection Protection** - Parameterized queries
- **Role-Based Access** - Admin vs. user permissions
- **Data Validation** - Input sanitization and validation

## 📱 Mobile Responsive

- **Responsive Design** - Works on all devices
- **Touch-Friendly Interface** - Mobile-optimized interactions
- **Fast Loading** - Optimized for mobile networks

## 🎨 Customization

### Branding
The platform uses a professional color scheme:
- Primary: `#667eea` (Purple-blue gradient)
- Secondary: `#764ba2` (Deep purple)
- Accent: Various complementary colors

### Custom Contracts
Enterprise users can customize contract templates for their specific market and legal requirements.

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
```bash
# Push to GitHub and deploy via share.streamlit.io
git add .
git commit -m "Initial deployment"
git push origin main
```

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create wholesale2flip
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Subscription tier upgrades
- [ ] Deal calculator functionality
- [ ] Contract generation
- [ ] Admin dashboard access
- [ ] Deal status updates
- [ ] Document downloads

### Automated Testing (Future)
```bash
# Install test dependencies
pip install pytest streamlit-testing

# Run tests
pytest tests/
```

## 📈 Roadmap

### Phase 1 (Current)
- [x] Core platform functionality
- [x] Basic deal calculator
- [x] Contract generation
- [x] Admin dashboard
- [x] Multi-tier subscriptions

### Phase 2 (Next Release)
- [ ] Advanced AI calculations with GPT-4
- [ ] Email notifications for deal updates
- [ ] SMS integration for instant alerts
- [ ] Advanced reporting and analytics
- [ ] Bulk deal import/export

### Phase 3 (Future)
- [ ] Mobile app (React Native)
- [ ] CRM integration (HubSpot, Salesforce)
- [ ] MLS integration
- [ ] Automated comps pulling
- [ ] Team collaboration features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Email**: support@wholesale2flip.com
- **Phone**: (555) 123-FLIP
- **Documentation**: [docs.wholesale2flip.com](https://docs.wholesale2flip.com)
- **Community**: Join our Discord server

## 🏆 Success Stories

> "Wholesale2Flip helped me analyze and close 15 deals in my first month. The contract generation saved me hours of legal work!" - **Sarah M., Real Estate Investor**

> "The admin dashboard makes managing our disposition team effortless. We can track every deal from submission to closing." - **Mike T., Wholesaling Company Owner**

---

**Built with ❤️ for the real estate wholesaling community**

*Wholesale2Flip - Where Deals Get Done*