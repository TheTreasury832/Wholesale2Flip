// frontend/public/manifest.json
{
  "name": "Wholesale2Flip",
  "short_name": "WTF",
  "description": "The most powerful wholesale real estate platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#6B46C1",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "shortcuts": [
    {
      "name": "Find Deals",
      "short_name": "Deals",
      "description": "Search for new wholesale deals",
      "url": "/dashboard",
      "icons": [{ "src": "/icons/deals.png", "sizes": "192x192" }]
    },
    {
      "name": "My Pipeline",
      "short_name": "Pipeline",
      "description": "View your active deals",
      "url": "/pipeline",
      "icons": [{ "src": "/icons/pipeline.png", "sizes": "192x192" }]
    }
  ]
}

// frontend/src/app/layout.tsx - PWA Setup
import { Metadata, Viewport } from 'next';

export const metadata: Metadata = {
  title: 'Wholesale2Flip - Real Estate Wholesaling Platform',
  description: 'Find deals, match buyers, close fast. The most powerful wholesale real estate platform.',
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'WTF'
  },
  formatDetection: {
    telephone: false
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://wholesale2flip.com',
    siteName: 'Wholesale2Flip',
    title: 'Wholesale2Flip - Real Estate Wholesaling Platform',
    description: 'Find deals, match buyers, close fast.',
    images: [
      {
        url: 'https://wholesale2flip.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Wholesale2Flip'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Wholesale2Flip',
    description: 'Find deals, match buyers, close fast.',
    images: ['https://wholesale2flip.com/twitter-image.png']
  }
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: 'cover'
};

// frontend/src/hooks/useMobile.ts
import { useState, useEffect } from 'react';

export function useMobile() {
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [isDesktop, setIsDesktop] = useState(true);
  const [orientation, setOrientation] = useState<'portrait' | 'landscape'>('portrait');

  useEffect(() => {
    const checkDevice = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);
      setIsDesktop(width >= 1024);
      setOrientation(window.innerHeight > window.innerWidth ? 'portrait' : 'landscape');
    };

    checkDevice();
    window.addEventListener('resize', checkDevice);
    window.addEventListener('orientationchange', checkDevice);

    return () => {
      window.removeEventListener('resize', checkDevice);
      window.removeEventListener('orientationchange', checkDevice);
    };
  }, []);

  return { isMobile, isTablet, isDesktop, orientation };
}

// frontend/src/components/mobile/MobileNav.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Search, PlusCircle, List, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const navItems = [
  { href: '/dashboard', icon: Home, label: 'Home' },
  { href: '/dashboard/search', icon: Search, label: 'Search' },
  { href: '/dashboard/create', icon: PlusCircle, label: 'New Deal' },
  { href: '/pipeline', icon: List, label: 'Pipeline' },
  { href: '/profile', icon: User, label: 'Profile' }
];

export function MobileNav() {
  const pathname = usePathname();
  const [activeTab, setActiveTab] = useState(pathname);

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#1a1a1a] border-t border-[#2a2a2a] md:hidden z-50">
      <div className="flex justify-around items-center h-16">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className="relative flex flex-col items-center justify-center w-full h-full"
              onClick={() => setActiveTab(item.href)}
            >
              <AnimatePresence>
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 bg-purple-600/20"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                  />
                )}
              </AnimatePresence>
              
              <Icon 
                className={`w-6 h-6 mb-1 transition-colors ${
                  isActive ? 'text-purple-400' : 'text-gray-400'
                }`}
              />
              <span className={`text-xs ${
                isActive ? 'text-purple-400' : 'text-gray-400'
              }`}>
                {item.label}
              </span>
              
              {item.href === '/dashboard/create' && (
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

// frontend/src/components/mobile/SwipeableCard.tsx
import { motion, useAnimation, PanInfo } from 'framer-motion';
import { useState } from 'react';

interface SwipeableCardProps {
  children: React.ReactNode;
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  threshold?: number;
}

export function SwipeableCard({ 
  children, 
  onSwipeLeft, 
  onSwipeRight,
  threshold = 100 
}: SwipeableCardProps) {
  const controls = useAnimation();
  const [exitDirection, setExitDirection] = useState<'left' | 'right' | null>(null);

  const handleDragEnd = async (event: any, info: PanInfo) => {
    const offset = info.offset.x;
    const velocity = info.velocity.x;

    if (Math.abs(offset) > threshold || Math.abs(velocity) > 500) {
      if (offset > 0) {
        setExitDirection('right');
        await controls.start({ x: window.innerWidth, opacity: 0 });
        onSwipeRight?.();
      } else {
        setExitDirection('left');
        await controls.start({ x: -window.innerWidth, opacity: 0 });
        onSwipeLeft?.();
      }
    } else {
      controls.start({ x: 0, opacity: 1 });
    }
  };

  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={handleDragEnd}
      animate={controls}
      whileDrag={{ scale: 0.95 }}
      className="cursor-grab active:cursor-grabbing"
    >
      {children}
    </motion.div>
  );
}

// frontend/src/app/mobile/deal-swiper/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { SwipeableCard } from '@/components/mobile/SwipeableCard';
import { X, Check, DollarSign, Home, MapPin } from 'lucide-react';

export default function DealSwiper() {
  const [deals, setDeals] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleSwipeLeft = () => {
    // Pass on deal
    console.log('Passed on deal:', deals[currentIndex]);
    setCurrentIndex(prev => prev + 1);
  };

  const handleSwipeRight = () => {
    // Interested in deal
    console.log('Interested in deal:', deals[currentIndex]);
    // Add to pipeline or contact seller
    setCurrentIndex(prev => prev + 1);
  };

  const currentDeal = deals[currentIndex];

  if (!currentDeal) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0a0a0a]">
        <p className="text-gray-400">No more deals to review</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] pb-20">
      <div className="p-4">
        <h1 className="text-2xl font-bold text-white mb-4">Deal Swiper</h1>
        
        <SwipeableCard
          onSwipeLeft={handleSwipeLeft}
          onSwipeRight={handleSwipeRight}
        >
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl overflow-hidden">
            {/* Property Image */}
            <div className="relative h-64 bg-gradient-to-br from-purple-900 to-blue-900">
              <div className="absolute inset-0 flex items-center justify-center">
                <Home className="w-24 h-24 text-white/20" />
              </div>
              <div className="absolute bottom-4 left-4">
                <div className="bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                  ${currentDeal.profit.toLocaleString()} Profit
                </div>
              </div>
            </div>

            {/* Property Details */}
            <div className="p-6">
              <h2 className="text-xl font-bold text-white mb-2">{currentDeal.address}</h2>
              <p className="text-gray-400 flex items-center gap-2 mb-4">
                <MapPin className="w-4 h-4" />
                {currentDeal.city}, {currentDeal.state}
              </p>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-[#0a0a0a] rounded-lg p-3">
                  <p className="text-gray-400 text-sm">List Price</p>
                  <p className="text-white font-semibold">${currentDeal.listPrice.toLocaleString()}</p>
                </div>
                <div className="bg-[#0a0a0a] rounded-lg p-3">
                  <p className="text-gray-400 text-sm">ARV</p>
                  <p className="text-white font-semibold">${currentDeal.arv.toLocaleString()}</p>
                </div>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={handleSwipeLeft}
                  className="flex-1 bg-red-500/20 text-red-400 py-4 rounded-xl font-semibold flex items-center justify-center gap-2"
                >
                  <X className="w-5 h-5" />
                  Pass
                </button>
                <button
                  onClick={handleSwipeRight}
                  className="flex-1 bg-green-500/20 text-green-400 py-4 rounded-xl font-semibold flex items-center justify-center gap-2"
                >
                  <Check className="w-5 h-5" />
                  Interested
                </button>
              </div>
            </div>
          </div>
        </SwipeableCard>
      </div>
    </div>
  );
}

// Performance Optimization Guide
// docs/PERFORMANCE.md
# Performance Optimization Guide

## Frontend Optimization

### 1. Code Splitting
```typescript
// Use dynamic imports for route-based code splitting
const DashboardPage = dynamic(() => import('@/app/dashboard/page'), {
  loading: () => <LoadingSpinner />,
  ssr: false
});

// Lazy load heavy components
const ContractGenerator = lazy(() => import('@/components/ContractGenerator'));
```

### 2. Image Optimization
```typescript
// Use Next.js Image component with optimization
import Image from 'next/image';

<Image
  src="/property.jpg"
  alt="Property"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL={blurDataUrl}
  priority={false}
  loading="lazy"
/>
```

### 3. Bundle Optimization
```javascript
// next.config.js
module.exports = {
  webpack: (config, { isServer }) => {
    // Tree shaking
    config.optimization.usedExports = true;
    
    // Split chunks
    if (!isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          default: false,
          vendors: false,
          vendor: {
            name: 'vendor',
            chunks: 'all',
            test: /node_modules/,
            priority: 20
          },
          common: {
            name: 'common',
            minChunks: 2,
            chunks: 'all',
            priority: 10,
            reuseExistingChunk: true,
            enforce: true
          }
        }
      };
    }
    
    return config;
  }
};
```

### 4. React Performance
```typescript
// Memoize expensive computations
const expensiveCalculation = useMemo(() => {
  return calculateComplexMetrics(data);
}, [data]);

// Memoize components
const MemoizedDealCard = memo(DealCard, (prevProps, nextProps) => {
  return prevProps.deal.id === nextProps.deal.id &&
         prevProps.deal.status === nextProps.deal.status;
});

// Use React.lazy for code splitting
const HeavyComponent = lazy(() => 
  import(/* webpackChunkName: "heavy-component" */ './HeavyComponent')
);
```

## Backend Optimization

### 1. Database Query Optimization
```typescript
// Use indexes for frequently queried fields
// prisma/schema.prisma
model Property {
  @@index([state, city])
  @@index([createdAt])
  @@index([userId, status])
}

// Use select to limit data transfer
const properties = await prisma.property.findMany({
  select: {
    id: true,
    address: true,
    city: true,
    state: true,
    listPrice: true
  },
  where: { userId },
  take: 20
});

// Use database views for complex queries
await prisma.$executeRaw`
  CREATE MATERIALIZED VIEW property_analytics AS
  SELECT 
    state,
    COUNT(*) as total_properties,
    AVG(list_price) as avg_price,
    AVG(days_on_market) as avg_dom
  FROM properties
  GROUP BY state;
`;
```

### 2. Caching Strategy
```typescript
// Multi-level caching
class CacheService {
  private memoryCache = new Map();
  private redisTTL = 3600; // 1 hour
  private memoryTTL = 300; // 5 minutes

  async get(key: string): Promise<any> {
    // Check memory cache first
    const memoryResult = this.memoryCache.get(key);
    if (memoryResult && memoryResult.expires > Date.now()) {
      return memoryResult.data;
    }

    // Check Redis
    const redisResult = await redis.get(key);
    if (redisResult) {
      const data = JSON.parse(redisResult);
      // Store in memory cache
      this.memoryCache.set(key, {
        data,
        expires: Date.now() + this.memoryTTL * 1000
      });
      return data;
    }

    return null;
  }

  async set(key: string, data: any, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(data);
    
    // Set in Redis
    await redis.setex(key, ttl || this.redisTTL, serialized);
    
    // Set in memory cache
    this.memoryCache.set(key, {
      data,
      expires: Date.now() + this.memoryTTL * 1000
    });
  }
}
```

### 3. API Response Compression
```typescript
// backend/src/app.ts
import compression from 'compression';

app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  },
  level: 6 // Balance between speed and compression
}));
```

### 4. Connection Pooling
```typescript
// backend/src/config/database.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  // Connection pool configuration
  connectionLimit: 10,
});

// Redis connection pool
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: true,
  // Connection pool settings
  connectionPool: {
    min: 2,
    max: 10
  }
});
```

## Monitoring & Metrics

### 1. Performance Monitoring
```typescript
// backend/src/middleware/performance.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { performance } from 'perf_hooks';

export const performanceMonitoring = (req: Request, res: Response, next: NextFunction) => {
  const start = performance.now();
  
  // Capture the original end function
  const originalEnd = res.end;
  
  // Override the end function
  res.end = function(...args: any[]) {
    const duration = performance.now() - start;
    
    // Log slow requests
    if (duration > 1000) {
      console.warn(`Slow request: ${req.method} ${req.path} - ${duration.toFixed(2)}ms`);
    }
    
    // Send metrics to monitoring service
    sendMetrics({
      method: req.method,
      path: req.path,
      duration,
      statusCode: res.statusCode,
      timestamp: new Date()
    });
    
    // Call the original end function
    originalEnd.apply(res, args);
  };
  
  next();
};
```

### 2. Client-Side Performance
```typescript
// frontend/src/utils/performance.ts
export function measureWebVitals() {
  if (typeof window !== 'undefined' && 'performance' in window) {
    // First Contentful Paint
    const paintEntries = performance.getEntriesByType('paint');
    const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint');
    
    // Largest Contentful Paint
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      const lastEntry = entries[entries.length - 1];
      console.log('LCP:', lastEntry.startTime);
      
      trackEvent('web_vitals', {
        metric: 'LCP',
        value: lastEntry.startTime
      });
    }).observe({ entryTypes: ['largest-contentful-paint'] });
    
    // First Input Delay
    new PerformanceObserver((entryList) => {
      const firstInput = entryList.getEntries()[0];
      const fid = firstInput.processingStart - firstInput.startTime;
      
      trackEvent('web_vitals', {
        metric: 'FID',
        value: fid
      });
    }).observe({ entryTypes: ['first-input'] });
    
    // Cumulative Layout Shift
    let clsValue = 0;
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      }
      
      trackEvent('web_vitals', {
        metric: 'CLS',
        value: clsValue
      });
    }).observe({ entryTypes: ['layout-shift'] });
  }
}
```

## CDN & Asset Optimization

### CloudFlare Configuration
```javascript
// cloudflare-worker.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  
  // Cache static assets
  if (url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$/)) {
    const response = await fetch(request);
    const headers = new Headers(response.headers);
    
    // Set cache headers
    headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    headers.set('X-Content-Type-Options', 'nosniff');
    
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });
  }
  
  // Pass through dynamic requests
  return fetch(request);
}
```

This comprehensive performance optimization guide ensures your Wholesale2Flip platform runs efficiently at scale.