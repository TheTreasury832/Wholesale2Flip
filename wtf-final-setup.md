# Wholesale2Flip Developer Documentation

## Table of Contents
1. [Getting Started](#getting-started)
2. [Architecture Overview](#architecture-overview)
3. [API Reference](#api-reference)
4. [User Onboarding Flow](#user-onboarding-flow)
5. [Error Handling](#error-handling)
6. [Logging & Monitoring](#logging-monitoring)
7. [Database Management](#database-management)
8. [Deployment Guide](#deployment-guide)
9. [Contributing](#contributing)

## Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- PostgreSQL 15+
- Redis 7+
- Docker and Docker Compose
- Git

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/wholesale2flip/platform.git
cd platform

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Start Docker services
docker-compose up -d postgres redis

# Run database migrations
cd backend && npx prisma migrate dev

# Seed development data
npm run seed:dev

# Start development servers
npm run dev
```

### Project Structure
```
wholesale2flip/
├── frontend/          # Next.js 14 frontend application
├── backend/           # Node.js/Express API server
├── discord-bot/       # Discord bot service
├── scripts/           # Build and deployment scripts
├── docs/              # Documentation
└── docker/            # Docker configurations
```

## Architecture Overview

### Tech Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, Prisma ORM
- **Database**: PostgreSQL (primary), Redis (cache)
- **Real-time**: Socket.io
- **Authentication**: JWT + Discord OAuth
- **Payment**: Stripe
- **Infrastructure**: AWS (ECS, RDS, ElastiCache)

### Service Architecture
```mermaid
graph TB
    A[CloudFlare CDN] --> B[Load Balancer]
    B --> C[Next.js Frontend]
    B --> D[API Gateway]
    D --> E[Backend API]
    E --> F[PostgreSQL]
    E --> G[Redis Cache]
    E --> H[Discord Bot]
    E --> I[WebSocket Server]
```

## API Reference

### Authentication Endpoints

#### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "subscriptionTier": "BASIC"
  }
}
```

#### POST /api/auth/login
Authenticate existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### Property Endpoints

#### POST /api/properties/search
Search for property data.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "address": "123 Main St, Houston, TX 77001"
}
```

### Deal Endpoints

#### GET /api/deals/my-pipeline
Get user's deal pipeline.

**Query Parameters:**
- `status`: Filter by deal status (active, pending, closed)
- `limit`: Number of results (default: 20)
- `offset`: Pagination offset

## User Onboarding Flow

### Implementation

```typescript
// frontend/src/components/onboarding/OnboardingFlow.tsx
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';

const steps = [
  { id: 'welcome', component: WelcomeStep },
  { id: 'profile', component: ProfileStep },
  { id: 'goals', component: GoalsStep },
  { id: 'buyer-criteria', component: BuyerCriteriaStep },
  { id: 'tutorial', component: TutorialStep },
  { id: 'complete', component: CompleteStep }
];

export function OnboardingFlow() {
  const [currentStep, setCurrentStep] = useState(0);
  const [userData, setUserData] = useState({});
  const router = useRouter();

  const CurrentStepComponent = steps[currentStep].component;

  const handleNext = (data: any) => {
    setUserData(prev => ({ ...prev, ...data }));
    
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      completeOnboarding();
    }
  };

  const completeOnboarding = async () => {
    try {
      await fetch('/api/users/complete-onboarding', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });

      router.push('/dashboard');
    } catch (error) {
      console.error('Onboarding error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
      <div className="w-full max-w-2xl p-8">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`flex-1 h-2 mx-1 rounded-full transition-all ${
                  index <= currentStep ? 'bg-purple-600' : 'bg-[#2a2a2a]'
                }`}
              />
            ))}
          </div>
          <p className="text-center text-gray-400 text-sm">
            Step {currentStep + 1} of {steps.length}
          </p>
        </div>

        {/* Step Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <CurrentStepComponent
              onNext={handleNext}
              onBack={() => setCurrentStep(Math.max(0, currentStep - 1))}
              userData={userData}
            />
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

// Individual step components
function WelcomeStep({ onNext }: any) {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-white mb-4">
        Welcome to Wholesale2Flip! 🎉
      </h1>
      <p className="text-xl text-gray-400 mb-8">
        Let's get you set up in just a few minutes
      </p>
      <button
        onClick={() => onNext({})}
        className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-lg font-semibold text-lg"
      >
        Let's Get Started
      </button>
    </div>
  );
}

function ProfileStep({ onNext, onBack, userData }: any) {
  const [formData, setFormData] = useState({
    businessName: '',
    phone: '',
    experience: ''
  });

  return (
    <div>
      <h2 className="text-3xl font-bold text-white mb-6">
        Tell us about yourself
      </h2>
      
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-2">
            Business Name (Optional)
          </label>
          <input
            type="text"
            value={formData.businessName}
            onChange={(e) => setFormData(prev => ({ ...prev, businessName: e.target.value }))}
            className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white"
            placeholder="Your Company LLC"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-400 mb-2">
            Phone Number
          </label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
            className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white"
            placeholder="(555) 123-4567"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-400 mb-2">
            Experience Level
          </label>
          <select
            value={formData.experience}
            onChange={(e) => setFormData(prev => ({ ...prev, experience: e.target.value }))}
            className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-3 text-white"
          >
            <option value="">Select your experience</option>
            <option value="beginner">New to Wholesaling</option>
            <option value="intermediate">1-10 Deals Completed</option>
            <option value="advanced">10+ Deals Completed</option>
          </select>
        </div>
      </div>

      <div className="flex gap-4 mt-8">
        <button
          onClick={onBack}
          className="flex-1 bg-[#1a1a1a] text-white px-6 py-3 rounded-lg font-semibold"
        >
          Back
        </button>
        <button
          onClick={() => onNext(formData)}
          className="flex-1 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
```

## Error Handling

### Global Error Handler

```typescript
// backend/src/middleware/error.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';

export class AppError extends Error {
  statusCode: number;
  isOperational: boolean;

  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  let error = { ...err };
  error.message = err.message;

  // Log error
  logger.error({
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    user: req.user?.id
  });

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    const message = 'Resource not found';
    error = new AppError(message, 404);
  }

  // Mongoose duplicate key
  if ((err as any).code === 11000) {
    const message = 'Duplicate field value entered';
    error = new AppError(message, 400);
  }

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const message = Object.values((err as any).errors)
      .map((val: any) => val.message)
      .join(', ');
    error = new AppError(message, 400);
  }

  res.status((error as any).statusCode || 500).json({
    success: false,
    error: {
      message: error.message || 'Server Error',
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
};

// Async error wrapper
export const asyncHandler = (fn: Function) => (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

### Frontend Error Boundary

```typescript
// frontend/src/components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { trackError } from '@/utils/analytics';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    
    // Track error in analytics
    trackError(error, {
      componentStack: errorInfo.componentStack,
      location: window.location.href
    });
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-4">
              Oops! Something went wrong
            </h1>
            <p className="text-gray-400 mb-8">
              We're sorry for the inconvenience. Please try refreshing the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold"
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Logging & Monitoring

### Logger Configuration

```typescript
// backend/src/utils/logger.ts
import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';

const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json()
);

// Create transports
const transports: winston.transport[] = [
  // Console transport
  new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }),
  
  // File transport for errors
  new DailyRotateFile({
    filename: 'logs/error-%DATE%.log',
    datePattern: 'YYYY-MM-DD',
    level: 'error',
    maxSize: '20m',
    maxFiles: '14d'
  }),
  
  // File transport for all logs
  new DailyRotateFile({
    filename: 'logs/combined-%DATE%.log',
    datePattern: 'YYYY-MM-DD',
    maxSize: '20m',
    maxFiles: '14d'
  })
];

// Add CloudWatch transport in production
if (process.env.NODE_ENV === 'production') {
  const CloudWatchTransport = require('winston-cloudwatch');
  transports.push(
    new CloudWatchTransport({
      logGroupName: 'wholesale2flip',
      logStreamName: `api-${process.env.NODE_ENV}`,
      awsRegion: process.env.AWS_REGION,
      jsonMessage: true
    })
  );
}

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  transports,
  exceptionHandlers: [
    new winston.transports.File({ filename: 'logs/exceptions.log' })
  ],
  rejectionHandlers: [
    new winston.transports.File({ filename: 'logs/rejections.log' })
  ]
});
```

### Request Logging Middleware

```typescript
// backend/src/middleware/request-logger.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';
import { v4 as uuidv4 } from 'uuid';

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  // Add request ID
  req.id = uuidv4();
  
  // Log request
  logger.info({
    type: 'request',
    requestId: req.id,
    method: req.method,
    url: req.url,
    ip: req.ip,
    userAgent: req.get('user-agent'),
    userId: req.user?.id
  });

  // Capture response
  const originalSend = res.send;
  res.send = function(data) {
    logger.info({
      type: 'response',
      requestId: req.id,
      statusCode: res.statusCode,
      responseTime: Date.now() - req.startTime
    });
    
    return originalSend.call(this, data);
  };

  req.startTime = Date.now();
  next();
};
```

## Database Management

### Migration Scripts

```bash
# Create a new migration
cd backend && npx prisma migrate dev --name add_user_preferences

# Apply migrations in production
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset
```

### Backup Scripts

```typescript
// scripts/backup-database.ts
import { exec } from 'child_process';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { createReadStream } from 'fs';
import { promisify } from 'util';

const execAsync = promisify(exec);
const s3Client = new S3Client({ region: process.env.AWS_REGION });

async function backupDatabase() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `backup-${timestamp}.sql`;
  
  try {
    // Create backup
    console.log('Creating database backup...');
    await execAsync(
      `pg_dump ${process.env.DATABASE_URL} > /tmp/${filename}`
    );
    
    // Compress backup
    console.log('Compressing backup...');
    await execAsync(`gzip /tmp/${filename}`);
    
    // Upload to S3
    console.log('Uploading to S3...');
    const fileStream = createReadStream(`/tmp/${filename}.gz`);
    
    await s3Client.send(new PutObjectCommand({
      Bucket: process.env.BACKUP_BUCKET,
      Key: `database/${filename}.gz`,
      Body: fileStream,
      ServerSideEncryption: 'AES256'
    }));
    
    console.log('Backup completed successfully!');
    
    // Clean up local file
    await execAsync(`rm /tmp/${filename}.gz`);
    
    // Verify backup
    await verifyBackup(filename);
    
  } catch (error) {
    console.error('Backup failed:', error);
    // Send alert
    await sendAlert('Database backup failed', error);
    process.exit(1);
  }
}

async function verifyBackup(filename: string) {
  // Download and test restore on a test database
  console.log('Verifying backup...');
  // Implementation here
}

async function sendAlert(subject: string, error: any) {
  // Send email/SMS alert to team
  console.log('Sending alert:', subject);
}

// Run backup
backupDatabase();
```

### Data Migration Script

```typescript
// scripts/migrate-data.ts
import { PrismaClient as OldPrisma } from './generated/old-client';
import { PrismaClient as NewPrisma } from '@prisma/client';

const oldDb = new OldPrisma();
const newDb = new NewPrisma();

async function migrateData() {
  console.log('Starting data migration...');
  
  try {
    // Start transaction
    await newDb.$transaction(async (tx) => {
      // Migrate users
      console.log('Migrating users...');
      const users = await oldDb.user.findMany();
      
      for (const user of users) {
        await tx.user.create({
          data: {
            id: user.id,
            email: user.email,
            // Map old fields to new schema
            firstName: user.name?.split(' ')[0],
            lastName: user.name?.split(' ')[1],
            // ... other fields
          }
        });
      }
      
      // Migrate properties
      console.log('Migrating properties...');
      const properties = await oldDb.property.findMany();
      
      for (const property of properties) {
        await tx.property.create({
          data: {
            // Map fields
          }
        });
      }
      
      // Add more migrations as needed
    });
    
    console.log('Migration completed successfully!');
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  } finally {
    await oldDb.$disconnect();
    await newDb.$disconnect();
  }
}

migrateData();
```

## Deployment Guide

### Production Checklist

- [ ] **Environment Variables**
  - [ ] All production secrets set
  - [ ] API keys configured
  - [ ] Database connection strings updated
  
- [ ] **Security**
  - [ ] SSL certificates installed
  - [ ] Security headers configured
  - [ ] Rate limiting enabled
  - [ ] CORS properly configured
  
- [ ] **Database**
  - [ ] Migrations run
  - [ ] Indexes optimized
  - [ ] Backup system tested
  
- [ ] **Monitoring**
  - [ ] Error tracking configured
  - [ ] Performance monitoring active
  - [ ] Alerts set up
  
- [ ] **Performance**
  - [ ] CDN configured
  - [ ] Assets optimized
  - [ ] Caching strategy implemented

### Deployment Commands

```bash
# Build production assets
npm run build

# Run database migrations
npm run migrate:prod

# Deploy to AWS ECS
npm run deploy:ecs

# Deploy to Kubernetes
kubectl apply -f k8s/

# Rollback deployment
npm run deploy:rollback
```

## Contributing

### Code Style

We use ESLint and Prettier for code formatting:

```bash
# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

### Git Workflow

1. Create feature branch from `develop`
2. Make changes and commit with conventional commits
3. Push branch and create pull request
4. Code review and approval
5. Merge to `develop`
6. Deploy to staging
7. Merge to `main` for production release

### Commit Convention

```
feat: add buyer matching algorithm
fix: resolve memory leak in socket connection
docs: update API documentation
chore: upgrade dependencies
refactor: optimize database queries
test: add unit tests for auth service
```

## Support

- **Documentation**: https://docs.wholesale2flip.com
- **Discord**: Join our developer channel
- **Email**: dev@wholesale2flip.com

---

## Quick Reference

### Common Commands

```bash
# Development
npm run dev              # Start all services
npm run dev:frontend     # Start frontend only
npm run dev:backend      # Start backend only
npm run dev:bot          # Start Discord bot

# Testing
npm test                 # Run all tests
npm run test:unit        # Unit tests only
npm run test:e2e         # E2E tests
npm run test:coverage    # Coverage report

# Database
npm run db:migrate       # Run migrations
npm run db:seed          # Seed database
npm run db:reset         # Reset database

# Production
npm run build            # Build for production
npm run start            # Start production server
npm run deploy           # Deploy to production
```

### Environment Variables Reference

```env
# Application
NODE_ENV=production
APP_URL=https://wholesale2flip.com
API_URL=https://api.wholesale2flip.com

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379

# Authentication
JWT_SECRET=your-secret-key
DISCORD_CLIENT_ID=your-client-id
DISCORD_CLIENT_SECRET=your-client-secret

# Third-party APIs
STRIPE_SECRET_KEY=sk_live_xxx
SENDGRID_API_KEY=SG.xxx
TWILIO_ACCOUNT_SID=ACxxx
ATTOM_API_KEY=xxx

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
```

---

This completes the comprehensive documentation for the Wholesale2Flip platform. The system is now ready for development, testing, and deployment.