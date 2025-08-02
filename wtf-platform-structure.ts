# Wholesale2Flip (WTF) Platform - Complete File Structure

## Core Project Structure

```
wholesale2flip/
├── README.md
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── .env.local
├── .env.example
├── .gitignore
├── prisma/
│   ├── schema.prisma
│   ├── seed.ts
│   └── migrations/
├── public/
│   ├── favicon.ico
│   ├── logo-wtf.svg
│   ├── images/
│   └── icons/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │   ├── not-found.tsx
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   ├── register/route.ts
│   │   │   │   ├── login/route.ts
│   │   │   │   └── logout/route.ts
│   │   │   ├── properties/
│   │   │   │   ├── route.ts
│   │   │   │   ├── [id]/route.ts
│   │   │   │   ├── search/route.ts
│   │   │   │   └── analyze/route.ts
│   │   │   ├── buyers/
│   │   │   │   ├── route.ts
│   │   │   │   ├── [id]/route.ts
│   │   │   │   └── match/route.ts
│   │   │   ├── contracts/
│   │   │   │   ├── route.ts
│   │   │   │   ├── generate/route.ts
│   │   │   │   └── [id]/route.ts
│   │   │   ├── leads/
│   │   │   │   ├── route.ts
│   │   │   │   ├── lightning/route.ts
│   │   │   │   └── import/route.ts
│   │   │   ├── webhooks/
│   │   │   │   ├── stripe/route.ts
│   │   │   │   └── discord/route.ts
│   │   │   ├── ai/
│   │   │   │   ├── gpt/route.ts
│   │   │   │   ├── scriptmaster/route.ts
│   │   │   │   └── underwriter/route.ts
│   │   │   └── analytics/
│   │   │       ├── route.ts
│   │   │       └── dashboard/route.ts
│   │   ├── auth/
│   │   │   ├── signin/page.tsx
│   │   │   ├── signup/page.tsx
│   │   │   └── forgot-password/page.tsx
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   ├── properties/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── new/page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── buyers/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── pipeline/
│   │   │   │   └── page.tsx
│   │   │   ├── contracts/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── leads/
│   │   │   │   └── page.tsx
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx
│   │   │   └── profile/
│   │   │       └── page.tsx
│   │   ├── buyers-club/
│   │   │   ├── page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── lightning-leads/
│   │   │   └── page.tsx
│   │   ├── admin/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   ├── users/page.tsx
│   │   │   ├── properties/page.tsx
│   │   │   ├── buyers/page.tsx
│   │   │   ├── analytics/page.tsx
│   │   │   └── settings/page.tsx
│   │   └── pricing/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   ├── modal.tsx
│   │   │   ├── dropdown.tsx
│   │   │   ├── toast.tsx
│   │   │   ├── table.tsx
│   │   │   ├── pagination.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── tooltip.tsx
│   │   │   ├── skeleton.tsx
│   │   │   └── loading.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   ├── property/
│   │   │   ├── PropertyCard.tsx
│   │   │   ├── PropertyForm.tsx
│   │   │   ├── PropertyDetails.tsx
│   │   │   ├── PropertySearch.tsx
│   │   │   ├── PropertyAnalyzer.tsx
│   │   │   ├── ARVCalculator.tsx
│   │   │   ├── RehabCalculator.tsx
│   │   │   └── CompsViewer.tsx
│   │   ├── buyers/
│   │   │   ├── BuyerCard.tsx
│   │   │   ├── BuyerForm.tsx
│   │   │   ├── BuyerProfile.tsx
│   │   │   ├── BuyerMatching.tsx
│   │   │   └── BuyBoxSetup.tsx
│   │   ├── contracts/
│   │   │   ├── ContractGenerator.tsx
│   │   │   ├── ContractViewer.tsx
│   │   │   ├── ContractForm.tsx
│   │   │   └── SignatureFlow.tsx
│   │   ├── leads/
│   │   │   ├── LeadsList.tsx
│   │   │   ├── LeadCard.tsx
│   │   │   ├── LeadForm.tsx
│   │   │   ├── LeadImporter.tsx
│   │   │   └── LightningLeads.tsx
│   │   ├── pipeline/
│   │   │   ├── PipelineView.tsx
│   │   │   ├── DealCard.tsx
│   │   │   ├── StageColumn.tsx
│   │   │   └── DealFlow.tsx
│   │   ├── analytics/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Charts.tsx
│   │   │   ├── Metrics.tsx
│   │   │   └── Reports.tsx
│   │   ├── ai/
│   │   │   ├── GPTChat.tsx
│   │   │   ├── ScriptMaster.tsx
│   │   │   ├── Underwriter.tsx
│   │   │   └── AIAssistant.tsx
│   │   ├── discord/
│   │   │   ├── DiscordBot.tsx
│   │   │   ├── DealAlerts.tsx
│   │   │   └── CommunityFeed.tsx
│   │   └── marketing/
│   │       ├── Hero.tsx
│   │       ├── Features.tsx
│   │       ├── Testimonials.tsx
│   │       ├── Pricing.tsx
│   │       └── CallToAction.tsx
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── database.ts
│   │   ├── prisma.ts
│   │   ├── stripe.ts
│   │   ├── discord.ts
│   │   ├── utils.ts
│   │   ├── validations.ts
│   │   ├── constants.ts
│   │   ├── types.ts
│   │   ├── api/
│   │   │   ├── properties.ts
│   │   │   ├── buyers.ts
│   │   │   ├── contracts.ts
│   │   │   ├── leads.ts
│   │   │   ├── analytics.ts
│   │   │   └── ai.ts
│   │   ├── integrations/
│   │   │   ├── attom.ts
│   │   │   ├── zillow.ts
│   │   │   ├── mls.ts
│   │   │   ├── openai.ts
│   │   │   └── twilio.ts
│   │   └── services/
│   │       ├── PropertyService.ts
│   │       ├── BuyerService.ts
│   │       ├── ContractService.ts
│   │       ├── LeadService.ts
│   │       ├── AnalyticsService.ts
│   │       ├── NotificationService.ts
│   │       └── EmailService.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useProperties.ts
│   │   ├── useBuyers.ts
│   │   ├── useContracts.ts
│   │   ├── useLeads.ts
│   │   ├── usePipeline.ts
│   │   ├── useAnalytics.ts
│   │   ├── useLocalStorage.ts
│   │   └── useDiscord.ts
│   ├── store/
│   │   ├── authStore.ts
│   │   ├── propertyStore.ts
│   │   ├── buyerStore.ts
│   │   ├── pipelineStore.ts
│   │   └── uiStore.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── components.css
│   │   └── utilities.css
│   └── types/
│       ├── auth.ts
│       ├── property.ts
│       ├── buyer.ts
│       ├── contract.ts
│       ├── lead.ts
│       ├── analytics.ts
│       └── api.ts
├── docs/
│   ├── README.md
│   ├── DEPLOYMENT.md
│   ├── API.md
│   ├── CONTRIBUTING.md
│   └── TROUBLESHOOTING.md
├── scripts/
│   ├── build.sh
│   ├── deploy.sh
│   ├── seed.ts
│   ├── migrate.ts
│   └── backup.ts
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
└── tests/
    ├── __mocks__/
    ├── components/
    ├── pages/
    ├── api/
    ├── utils/
    └── setup.ts
```

## Key Technologies & Dependencies

### Core Stack
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Database**: PostgreSQL + Prisma ORM
- **Authentication**: NextAuth.js / Auth.js
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod validation
- **Payments**: Stripe
- **Deployment**: Vercel / Docker

### Real Estate Integrations
- **Property Data**: ATTOM Data API, Zillow API
- **MLS Integration**: RETS/TRESLE
- **Skip Tracing**: TruePeopleSearch API
- **Mapping**: Google Maps API
- **Address Validation**: Google Places API

### AI & Communication
- **AI Integration**: OpenAI GPT-4, custom training
- **Discord Bot**: Discord.js
- **SMS/Email**: Twilio, SendGrid
- **Document Generation**: jsPDF, docx-templates
- **File Storage**: AWS S3 / Vercel Blob

### Analytics & Monitoring
- **Analytics**: PostHog / Google Analytics 4
- **Error Tracking**: Sentry
- **Performance**: Vercel Analytics
- **Logging**: Winston / Pino

## Environment Variables (.env.example)

```bash
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/wholesale2flip"
DIRECT_URL="postgresql://username:password@localhost:5432/wholesale2flip"

# Auth
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"

# Stripe
STRIPE_PUBLISHABLE_KEY="pk_test_..."
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# OpenAI
OPENAI_API_KEY="sk-..."

# Property Data APIs
ATTOM_API_KEY="your-attom-key"
ZILLOW_API_KEY="your-zillow-key"

# Communication
TWILIO_ACCOUNT_SID="AC..."
TWILIO_AUTH_TOKEN="..."
SENDGRID_API_KEY="SG..."

# Discord
DISCORD_BOT_TOKEN="..."
DISCORD_CLIENT_ID="..."
DISCORD_CLIENT_SECRET="..."

# File Storage
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_BUCKET_NAME="wholesale2flip-files"

# Analytics
POSTHOG_KEY="..."
SENTRY_DSN="..."
```

This structure provides a complete foundation for building the Wholesale2Flip platform with all the features needed to match and exceed BuyBox Cartel's functionality while integrating your specific WTF branding and additional AI/automation features.