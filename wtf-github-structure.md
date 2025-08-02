# Wholesale2Flip (WTF) Platform - GitHub Repository Structure

## Repository Overview
Complete codebase for the Wholesale2Flip real estate wholesaling platform, featuring buyer matching, deal analysis, and educational resources.

```
wholesale2flip/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── package.json
├── 
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── logo.svg
│   │   └── images/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── login/
│   │   │   ├── signup/
│   │   │   ├── dashboard/
│   │   │   ├── buyboxes/
│   │   │   ├── pipeline/
│   │   │   ├── tutorials/
│   │   │   ├── profile/
│   │   │   └── leads/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── dashboard/
│   │   │   ├── deals/
│   │   │   ├── buyers/
│   │   │   └── common/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── styles/
│   │   └── types/
│   └── tests/
│
├── backend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── index.ts
│   │   ├── app.ts
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── types/
│   ├── prisma/
│   │   ├── schema.prisma
│   │   └── migrations/
│   └── tests/
│
├── discord-bot/
│   ├── package.json
│   ├── src/
│   │   ├── index.ts
│   │   ├── commands/
│   │   ├── events/
│   │   └── utils/
│   └── config/
│
├── scripts/
│   ├── setup.sh
│   ├── deploy.sh
│   └── seed-data.ts
│
└── docs/
    ├── API.md
    ├── SETUP.md
    └── DEPLOYMENT.md
```

## Key Files Content

### 1. Root README.md
```markdown
# Wholesale2Flip (WTF) Platform

The most powerful wholesale real estate platform. Find deals in seconds, match with buyers instantly, close with confidence.

## Features

- 🔍 **Smart Deal Finder** - AI-powered property analysis
- 🤝 **Buyer Matching** - Instant connection with cash buyers and hedge funds
- 📚 **Live Education** - 40+ hours weekly training
- 📄 **Contract Generation** - Auto-generate all deal documents
- 💬 **Discord Integration** - Active community support
- 🤖 **AI Tools** - ScriptMaster and Underwriter GPTs

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/wholesale2flip.git

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Run development servers
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# Discord Bot: Automatic connection
```

## Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, PostgreSQL, Redis
- **Real-time**: Socket.io
- **Authentication**: Auth0 + Discord OAuth
- **Payment**: Stripe
- **Infrastructure**: Docker, AWS

## Documentation

- [API Documentation](./docs/API.md)
- [Setup Guide](./docs/SETUP.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## License

Proprietary - Wholesale2Flip © 2025
```

### 2. docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://api:5000
      - NEXT_PUBLIC_WS_URL=ws://api:5000
    depends_on:
      - api
    volumes:
      - ./frontend:/app
      - /app/node_modules

  api:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://wtf:password@postgres:5432/wholesale2flip
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=your-secret-key
      - DISCORD_CLIENT_ID=${DISCORD_CLIENT_ID}
      - DISCORD_CLIENT_SECRET=${DISCORD_CLIENT_SECRET}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
      - /app/node_modules

  discord-bot:
    build: ./discord-bot
    environment:
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
      - API_URL=http://api:5000
    depends_on:
      - api
    volumes:
      - ./discord-bot:/app
      - /app/node_modules

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=wtf
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=wholesale2flip
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 3. Frontend package.json
```json
{
  "name": "wholesale2flip-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0",
    "framer-motion": "^11.0.0",
    "socket.io-client": "^4.6.0",
    "@stripe/stripe-js": "^2.0.0",
    "react-hot-toast": "^2.4.0",
    "date-fns": "^3.0.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.300.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0"
  }
}
```

### 4. Backend package.json
```json
{
  "name": "wholesale2flip-backend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "nodemon src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "migrate": "prisma migrate dev",
    "generate": "prisma generate"
  },
  "dependencies": {
    "express": "^4.18.0",
    "typescript": "^5.0.0",
    "@prisma/client": "^5.0.0",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3",
    "socket.io": "^4.6.0",
    "redis": "^4.6.0",
    "stripe": "^14.0.0",
    "axios": "^1.6.0",
    "@sendgrid/mail": "^8.0.0",
    "multer": "^1.4.5",
    "sharp": "^0.33.0",
    "pdf-lib": "^1.17.0",
    "winston": "^3.11.0",
    "joi": "^17.11.0",
    "rate-limiter-flexible": "^3.0.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.0",
    "@types/node": "^20.0.0",
    "nodemon": "^3.0.0",
    "ts-node": "^10.9.0",
    "prisma": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
```

### 5. Database Schema (prisma/schema.prisma)
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id                String    @id @default(uuid())
  email             String    @unique
  discordId         String?   @unique
  firstName         String?
  lastName          String?
  businessName      String?
  phone             String?
  passwordHash      String?
  subscriptionTier  SubscriptionTier @default(BASIC)
  stripeCustomerId  String?
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt
  
  wholesalerDeals   Deal[]    @relation("WholesalerDeals")
  buyerDeals        Deal[]    @relation("BuyerDeals")
  buyerCriteria     BuyerCriteria[]
  properties        Property[]
  notifications     Notification[]
}

model Property {
  id              String    @id @default(uuid())
  address         String
  city            String
  state           String
  zip             String
  county          String?
  propertyType    PropertyType
  bedrooms        Int
  bathrooms       Float
  squareFeet      Int
  yearBuilt       Int?
  listPrice       Decimal?
  arv             Decimal?
  repairCost      Decimal?
  daysOnMarket    Int?
  propertyData    Json?
  userId          String
  user            User      @relation(fields: [userId], references: [id])
  deals           Deal[]
  createdAt       DateTime  @default(now())
  updatedAt       DateTime  @updatedAt
}

model Deal {
  id                String    @id @default(uuid())
  propertyId        String
  property          Property  @relation(fields: [propertyId], references: [id])
  wholesalerId      String
  wholesaler        User      @relation("WholesalerDeals", fields: [wholesalerId], references: [id])
  buyerId           String?
  buyer             User?     @relation("BuyerDeals", fields: [buyerId], references: [id])
  dealType          DealType
  offerAmount       Decimal
  contractType      ContractType
  status            DealStatus @default(ACTIVE)
  matchScore        Int?
  contractData      Json?
  closingDate       DateTime?
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt
}

model BuyerCriteria {
  id              String    @id @default(uuid())
  userId          String
  user            User      @relation(fields: [userId], references: [id])
  buyerType       BuyerType
  states          String[]
  cities          String[]
  zips            String[]
  propertyTypes   PropertyType[]
  minBedrooms     Int?
  maxBedrooms     Int?
  minBathrooms    Float?
  maxBathrooms    Float?
  minSquareFeet   Int?
  maxSquareFeet   Int?
  minPrice        Decimal?
  maxPrice        Decimal?
  minROI          Float?
  maxRepairCost   Decimal?
  active          Boolean   @default(true)
  createdAt       DateTime  @default(now())
  updatedAt       DateTime  @updatedAt
}

model Notification {
  id          String    @id @default(uuid())
  userId      String
  user        User      @relation(fields: [userId], references: [id])
  type        NotificationType
  title       String
  message     String
  data        Json?
  read        Boolean   @default(false)
  createdAt   DateTime  @default(now())
}

enum SubscriptionTier {
  BASIC
  PRO
  ELITE
}

enum PropertyType {
  SINGLE_FAMILY
  MULTI_FAMILY
  CONDO
  TOWNHOUSE
  LAND
  COMMERCIAL
}

enum DealType {
  CASH
  CREATIVE
  SUBJECT_TO
  SELLER_FINANCE
  WRAP
  LEASE_OPTION
}

enum ContractType {
  ASSIGNMENT
  DOUBLE_CLOSE
  NOVATION
  JV
}

enum DealStatus {
  ACTIVE
  PENDING
  UNDER_CONTRACT
  CLOSED
  CANCELLED
}

enum BuyerType {
  FIX_FLIP
  SECTION_8
  RENTAL
  CREATIVE
}

enum NotificationType {
  NEW_MATCH
  DEAL_UPDATE
  MESSAGE
  SYSTEM
}
```

### 6. Main Application Entry (frontend/src/app/page.tsx)
```typescript
'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowRight, Home, Users, BookOpen, Zap } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black">
      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />
      
      {/* Navigation */}
      <nav className="relative z-10 p-6">
        <div className="container mx-auto flex justify-between items-center">
          <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Wholesale2Flip
          </div>
          <div className="flex gap-8 items-center">
            <Link href="/features" className="text-gray-300 hover:text-white transition">Features</Link>
            <Link href="/pricing" className="text-gray-300 hover:text-white transition">Pricing</Link>
            <Link href="/education" className="text-gray-300 hover:text-white transition">Education</Link>
            <Link href="/login" className="text-gray-300 hover:text-white transition">Login</Link>
            <Link 
              href="/signup" 
              className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-semibold transition"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 container mx-auto px-6 py-20">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-4xl mx-auto"
        >
          <h1 className="text-6xl font-bold text-white mb-6">
            Find Deals. Match Buyers.{' '}
            <span className="bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
              Close Fast.
            </span>
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            The most powerful wholesale real estate platform. Instantly match properties 
            with cash buyers, generate contracts, and scale your business.
          </p>
          
          <div className="flex gap-4 justify-center mb-12">
            <Link 
              href="/signup"
              className="bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition flex items-center gap-2"
            >
              Start Free Trial <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              href="/demo"
              className="bg-white/10 hover:bg-white/20 text-white border-2 border-white/30 px-8 py-4 rounded-lg font-semibold text-lg transition"
            >
              Watch Demo
            </Link>
          </div>

          {/* Feature Pills */}
          <div className="flex flex-wrap gap-4 justify-center">
            <div className="bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full text-sm text-white">
              ✓ No Credit Card Required
            </div>
            <div className="bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full text-sm text-white">
              ✓ 40+ Hours Weekly Training
            </div>
            <div className="bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full text-sm text-white">
              ✓ Instant Buyer Matching
            </div>
          </div>
        </motion.div>
      </section>

      {/* Feature Cards */}
      <section className="relative z-10 container mx-auto px-6 py-20">
        <div className="grid md:grid-cols-3 gap-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition"
          >
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center mb-6">
              <Home className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">Smart Deal Finder</h3>
            <p className="text-gray-400">
              AI-powered algorithm finds profitable deals across multiple sources in seconds. 
              Never miss an opportunity again.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition"
          >
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-blue-500 rounded-lg flex items-center justify-center mb-6">
              <Users className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">Buyer Matching</h3>
            <p className="text-gray-400">
              Instantly connect with verified cash buyers and hedge funds. Our algorithm 
              matches your deals with the perfect buyer.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition"
          >
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-green-500 rounded-lg flex items-center justify-center mb-6">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">Live Education</h3>
            <p className="text-gray-400">
              40+ hours of live training weekly. Learn from experts doing millions in 
              wholesale deals every month.
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
```

### 7. Dashboard Component (frontend/src/app/dashboard/page.tsx)
```typescript
'use client';

import { useState } from 'react';
import { Search, Home, TrendingUp, DollarSign, Clock } from 'lucide-react';
import { motion } from 'framer-motion';

export default function DashboardPage() {
  const [address, setAddress] = useState('');

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Navigation */}
      <nav className="bg-[#1a1a1a] border-b border-[#2a2a2a]">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-8">
              <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                WTF
              </div>
              <div className="flex gap-6">
                <a href="/dashboard" className="text-purple-400 font-semibold">Home</a>
                <a href="/buyboxes" className="text-gray-400 hover:text-white transition">BuyBoxes</a>
                <a href="/pipeline" className="text-gray-400 hover:text-white transition">Pipeline</a>
                <a href="/tutorials" className="text-gray-400 hover:text-white transition">Tutorials</a>
                <a href="/profile" className="text-gray-400 hover:text-white transition">Profile</a>
                <a href="/leads" className="text-gray-400 hover:text-white transition flex items-center gap-1">
                  <Zap className="w-4 h-4 text-yellow-400" /> Leads
                </a>
              </div>
            </div>
            <button className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold transition">
              Log Out
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section with Search */}
      <section className="relative overflow-hidden">
        {/* Background House Image with Neon Outline */}
        <div className="absolute inset-0 opacity-50">
          <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0a] via-transparent to-transparent z-10" />
          <img 
            src="/api/placeholder/1920/600" 
            alt="House" 
            className="w-full h-full object-cover"
          />
          {/* Neon outline effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-green-500/20 via-yellow-500/20 to-green-500/20" />
        </div>

        <div className="relative z-20 container mx-auto px-6 py-32">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <h1 className="text-5xl font-bold text-white mb-4">Pop In Your Address</h1>
            <p className="text-xl text-gray-300 mb-8">Let's find you a buyer</p>
            
            <div className="max-w-2xl mx-auto">
              <div className="bg-white/10 backdrop-blur-md rounded-lg p-2">
                <div className="flex items-center gap-3">
                  <Search className="w-6 h-6 text-purple-400 ml-4" />
                  <input
                    type="text"
                    placeholder="Enter address..."
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="flex-1 bg-transparent text-white placeholder-gray-400 py-3 outline-none"
                  />
                  <button className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition">
                    Search
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-6 py-12">
        <div className="grid md:grid-cols-4 gap-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6 hover:border-[#3a3a3a] transition"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                <Home className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Active Deals</p>
                <p className="text-3xl font-bold text-white">24</p>
              </div>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6 hover:border-[#3a3a3a] transition"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-green-400" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Total Profit</p>
                <p className="text-3xl font-bold text-green-400">$487K</p>
              </div>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6 hover:border-[#3a3a3a] transition"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Success Rate</p>
                <p className="text-3xl font-bold text-white">87%</p>
              </div>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6 hover:border-[#3a3a3a] transition"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-yellow-400" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Avg Deal Time</p>
                <p className="text-3xl font-bold text-white">14 days</p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
```

### 8. API Routes (backend/src/routes/index.ts)
```typescript
import { Router } from 'express';
import authRoutes from './auth.routes';
import propertyRoutes from './property.routes';
import dealRoutes from './deal.routes';
import buyerRoutes from './buyer.routes';
import contractRoutes from './contract.routes';
import webhookRoutes from './webhook.routes';

const router = Router();

router.use('/auth', authRoutes);
router.use('/properties', propertyRoutes);
router.use('/deals', dealRoutes);
router.use('/buyers', buyerRoutes);
router.use('/contracts', contractRoutes);
router.use('/webhooks', webhookRoutes);

// Health check
router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

export default router;
```

### 9. Property Matching Service (backend/src/services/matching.service.ts)
```typescript
import { PrismaClient } from '@prisma/client';
import { redis } from '../config/redis';

const prisma = new PrismaClient();

export class MatchingService {
  async findBuyersForProperty(propertyId: string) {
    // Get property details
    const property = await prisma.property.findUnique({
      where: { id: propertyId },
      include: { deals: true }
    });

    if (!property) {
      throw new Error('Property not found');
    }

    // Get all active buyer criteria
    const buyerCriteria = await prisma.buyerCriteria.findMany({
      where: { active: true },
      include: { user: true }
    });

    // Score and rank buyers
    const matches = buyerCriteria
      .map(criteria => ({
        buyer: criteria.user,
        criteria,
        score: this.calculateMatchScore(property, criteria)
      }))
      .filter(match => match.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 20); // Top 20 matches

    // Cache results
    await redis.setex(
      `matches:${propertyId}`,
      3600,
      JSON.stringify(matches)
    );

    return matches;
  }

  private calculateMatchScore(property: any, criteria: any): number {
    let score = 0;

    // Location match (highest priority)
    if (criteria.states.includes(property.state)) score += 20;
    if (criteria.cities.includes(property.city)) score += 15;
    if (criteria.zips.includes(property.zip)) score += 10;

    // Property type match
    if (criteria.propertyTypes.includes(property.propertyType)) score += 15;

    // Size requirements
    if (
      (!criteria.minBedrooms || property.bedrooms >= criteria.minBedrooms) &&
      (!criteria.maxBedrooms || property.bedrooms <= criteria.maxBedrooms)
    ) {
      score += 10;
    }

    if (
      (!criteria.minBathrooms || property.bathrooms >= criteria.minBathrooms) &&
      (!criteria.maxBathrooms || property.bathrooms <= criteria.maxBathrooms)
    ) {
      score += 5;
    }

    if (
      (!criteria.minSquareFeet || property.squareFeet >= criteria.minSquareFeet) &&
      (!criteria.maxSquareFeet || property.squareFeet <= criteria.maxSquareFeet)
    ) {
      score += 10;
    }

    // Price range
    const effectivePrice = property.listPrice || property.arv;
    if (
      (!criteria.minPrice || effectivePrice >= criteria.minPrice) &&
      (!criteria.maxPrice || effectivePrice <= criteria.maxPrice)
    ) {
      score += 15;
    }

    // ROI calculation
    if (property.arv && property.repairCost && criteria.minROI) {
      const purchasePrice = Number(property.listPrice);
      const totalInvestment = purchasePrice + Number(property.repairCost);
      const profit = Number(property.arv) - totalInvestment;
      const roi = (profit / totalInvestment) * 100;

      if (roi >= criteria.minROI) {
        score += 20;
      }
    }

    return score;
  }

  async notifyMatchedBuyers(propertyId: string, matches: any[]) {
    for (const match of matches) {
      await prisma.notification.create({
        data: {
          userId: match.buyer.id,
          type: 'NEW_MATCH',
          title: 'New Property Match!',
          message: `A new property matching your criteria is available with a ${match.score}% match score.`,
          data: {
            propertyId,
            matchScore: match.score
          }
        }
      });

      // Send real-time notification via WebSocket
      // this.socketService.notifyUser(match.buyer.id, 'new-match', { propertyId, score: match.score });
    }
  }
}
```

### 10. Contract Generation Service (backend/src/services/contract.service.ts)
```typescript
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import fs from 'fs/promises';
import path from 'path';

export class ContractService {
  async generateContract(contractData: any): Promise<Buffer> {
    // Load template based on contract type
    const templatePath = path.join(
      __dirname,
      `../../templates/${contractData.contractType}.pdf`
    );
    const templateBytes = await fs.readFile(templatePath);
    const pdfDoc = await PDFDocument.load(templateBytes);
    
    // Get form fields
    const form = pdfDoc.getForm();
    
    // Fill in contract details
    form.getTextField('purchasePrice').setText(contractData.purchasePrice.toString());
    form.getTextField('propertyAddress').setText(contractData.propertyAddress);
    form.getTextField('buyerName').setText(contractData.buyerName);
    form.getTextField('sellerName').setText(contractData.sellerName);
    form.getTextField('closingDate').setText(contractData.closingDate);
    form.getTextField('earnestMoney').setText(contractData.earnestMoney.toString());
    
    // Handle special fields based on contract type
    if (contractData.contractType === 'CREATIVE') {
      form.getTextField('interestRate').setText(contractData.interestRate);
      form.getTextField('termYears').setText(contractData.termYears);
      form.getTextField('monthlyPayment').setText(contractData.monthlyPayment);
    }
    
    // Flatten form to prevent editing
    form.flatten();
    
    // Save and return PDF bytes
    const pdfBytes = await pdfDoc.save();
    return Buffer.from(pdfBytes);
  }

  async sendToTransactionCoordinator(contractData: any, pdfBuffer: Buffer) {
    // Email service integration
    const emailData = {
      to: process.env.TC_EMAIL,
      subject: `New Contract: ${contractData.propertyAddress}`,
      html: this.generateEmailTemplate(contractData),
      attachments: [{
        filename: `contract_${contractData.propertyAddress.replace(/\s+/g, '_')}.pdf`,
        content: pdfBuffer
      }]
    };
    
    // await emailService.send(emailData);
  }

  private generateEmailTemplate(contractData: any): string {
    return `
      <h2>New Contract Ready for Signatures</h2>
      <p><strong>Property:</strong> ${contractData.propertyAddress}</p>
      <p><strong>Purchase Price:</strong> $${contractData.purchasePrice.toLocaleString()}</p>
      <p><strong>Buyer:</strong> ${contractData.buyerName}</p>
      <p><strong>Seller:</strong> ${contractData.sellerName}</p>
      <p><strong>Closing Date:</strong> ${contractData.closingDate}</p>
      <p><strong>Contract Type:</strong> ${contractData.contractType}</p>
      <hr>
      <p>Please review the attached contract and coordinate signatures.</p>
    `;
  }
}
```

### 11. Discord Bot Main File (discord-bot/src/index.ts)
```typescript
import { Client, GatewayIntentBits, REST, Routes } from 'discord.js';
import { config } from './config';
import { commands } from './commands';
import axios from 'axios';

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
  ]
});

// Register slash commands
const rest = new REST({ version: '10' }).setToken(config.token);

async function registerCommands() {
  try {
    console.log('Started refreshing application (/) commands.');
    
    await rest.put(
      Routes.applicationGuildCommands(config.clientId, config.guildId),
      { body: commands.map(cmd => cmd.data.toJSON()) }
    );
    
    console.log('Successfully reloaded application (/) commands.');
  } catch (error) {
    console.error(error);
  }
}

// Bot ready event
client.once('ready', () => {
  console.log(`WTF Bot is online as ${client.user?.tag}!`);
  registerCommands();
});

// Handle slash commands
client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;
  
  const command = commands.find(cmd => cmd.data.name === interaction.commandName);
  
  if (!command) return;
  
  try {
    await command.execute(interaction);
  } catch (error) {
    console.error(error);
    await interaction.reply({ 
      content: 'There was an error executing this command!', 
      ephemeral: true 
    });
  }
});

// Handle messages for legacy commands
client.on('messageCreate', async message => {
  if (message.author.bot) return;
  
  // Script command
  if (message.content.toLowerCase() === '!scripts') {
    const scriptEmbed = {
      color: 0x6B46C1,
      title: '📚 WTF Script Library',
      description: 'Access all sales scripts with these commands:',
      fields: [
        {
          name: 'Seller Finance Scripts',
          value: '`!script-sf-1` through `!script-sf-5`'
        },
        {
          name: 'Subject-To Scripts',
          value: '`!script-st-1` through `!script-st-5`'
        },
        {
          name: 'Wrap & Hybrid Scripts',
          value: '`!script-wrap` and `!script-hybrid`'
        }
      ],
      footer: {
        text: 'WTF Script System • Powered by The Treasury'
      }
    };
    
    await message.reply({ embeds: [scriptEmbed] });
  }
  
  // Calculator command
  if (message.content.startsWith('!calc')) {
    const args = message.content.split(' ').slice(1);
    
    if (args.length < 3) {
      await message.reply('Usage: `!calc [purchase_price] [arv] [repair_cost]`');
      return;
    }
    
    const [purchase, arv, repairs] = args.map(Number);
    const profit = arv - purchase - repairs;
    const roi = ((profit / (purchase + repairs)) * 100).toFixed(2);
    
    const calcEmbed = {
      color: 0x10B981,
      title: '🧮 Deal Calculator',
      fields: [
        { name: 'Purchase Price', value: `$${purchase.toLocaleString()}`, inline: true },
        { name: 'ARV', value: `$${arv.toLocaleString()}`, inline: true },
        { name: 'Repair Cost', value: `$${repairs.toLocaleString()}`, inline: true },
        { name: 'Potential Profit', value: `$${profit.toLocaleString()}`, inline: true },
        { name: 'ROI', value: `${roi}%`, inline: true }
      ]
    };
    
    await message.reply({ embeds: [calcEmbed] });
  }
  
  // Deal alert command
  if (message.content.startsWith('!deal')) {
    try {
      const response = await axios.get(`${config.apiUrl}/deals/latest`);
      const deals = response.data;
      
      if (deals.length === 0) {
        await message.reply('No active deals at the moment. Keep grinding! 💪');
        return;
      }
      
      const dealEmbed = {
        color: 0x3B82F6,
        title: '🏠 Latest Deals',
        description: 'Hot deals ready for disposition:',
        fields: deals.slice(0, 5).map((deal: any) => ({
          name: deal.address,
          value: `💰 Profit: $${deal.profit.toLocaleString()} | 📍 ${deal.city}, ${deal.state}`,
          inline: false
        })),
        footer: {
          text: 'Use !deal [id] for more details'
        }
      };
      
      await message.reply({ embeds: [dealEmbed] });
    } catch (error) {
      await message.reply('Error fetching deals. Please try again later.');
    }
  }
});

// Login
client.login(config.token);
```

### 12. Environment Variables (.env.example)
```env
# Application
NODE_ENV=development
PORT=5000
FRONTEND_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://wtf:password@localhost:5432/wholesale2flip

# Redis
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRE=7d

# Discord OAuth
DISCORD_CLIENT_ID=your-discord-client-id
DISCORD_CLIENT_SECRET=your-discord-client-secret
DISCORD_REDIRECT_URI=http://localhost:3000/auth/discord/callback

# Discord Bot
DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_GUILD_ID=your-guild-id

# Stripe
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
STRIPE_PRICE_BASIC=price_basic_id
STRIPE_PRICE_PRO=price_pro_id
STRIPE_PRICE_ELITE=price_elite_id

# SendGrid
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=deals@wholesale2flip.com
TC_EMAIL=tc@wholesale2flip.com

# Property Data API
PROPERTY_API_KEY=your-property-data-api-key
PROPERTY_API_URL=https://api.propertydata.com

# AWS S3 (for file storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=wholesale2flip-assets

# GPT Integration
OPENAI_API_KEY=your-openai-api-key
GPT_SCRIPTMASTER_ID=gpt-scriptmaster-id
GPT_UNDERWRITER_ID=gpt-underwriter-id
```

### 13. Setup Script (scripts/setup.sh)
```bash
#!/bin/bash

echo "🚀 Setting up Wholesale2Flip Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Copy environment file
if [ ! -f .env ]; then
    echo "📋 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual values"
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install backend dependencies
cd backend && npm install && cd ..

# Install Discord bot dependencies
cd discord-bot && npm install && cd ..

# Generate Prisma client
echo "🗄️  Generating Prisma client..."
cd backend && npx prisma generate && cd ..

# Start Docker containers
echo "🐳 Starting Docker containers..."
docker-compose up -d postgres redis

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
sleep 5

# Run database migrations
echo "🗄️  Running database migrations..."
cd backend && npx prisma migrate dev && cd ..

# Seed initial data
echo "🌱 Seeding database..."
cd backend && npm run seed && cd ..

echo "✅ Setup complete!"
echo ""
echo "To start the development servers, run:"
echo "  docker-compose up"
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:5000"
echo "  API Docs: http://localhost:5000/api-docs"
echo ""
echo "Happy wholesaling! 🏠💰"
```

## Deployment Instructions

### Production Deployment with AWS

1. **Frontend (Vercel/Netlify)**
   - Connect GitHub repository
   - Set environment variables
   - Enable automatic deployments

2. **Backend (AWS ECS/Railway)**
   - Build Docker image
   - Push to registry
   - Deploy with proper scaling

3. **Database (AWS RDS)**
   - PostgreSQL instance
   - Automated backups
   - Read replicas for scaling

4. **Redis (AWS ElastiCache)**
   - Cluster mode enabled
   - Automatic failover

5. **Discord Bot (AWS EC2/Railway)**
   - Always-on instance
   - Auto-restart on failure

## Additional Resources

- [API Documentation](./docs/API.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Security Policy](./SECURITY.md)
- [Discord Community](https://discord.gg/wholesale2flip)

## Support

For questions or support:
- Discord: Join our community server
- Email: support@wholesale2flip.com
- Documentation: https://docs.wholesale2flip.com
```

This comprehensive GitHub repository structure includes everything needed to build the Wholesale2Flip platform based on the BuyBox Cartel model with your unique features and branding.