# Wholesale2Flip Deployment & Configuration Guide

## Production Deployment Architecture

### Infrastructure Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                          CloudFlare                              │
│                        (CDN & DDoS Protection)                   │
└─────────────────┬───────────────────────────┬───────────────────┘
                  │                           │
         ┌────────▼────────┐         ┌───────▼────────┐
         │   Vercel/Next   │         │  AWS ALB/API   │
         │   (Frontend)    │         │   Gateway      │
         └────────┬────────┘         └───────┬────────┘
                  │                           │
                  │                  ┌────────▼────────┐
                  │                  │   AWS ECS/K8s   │
                  │                  │  (Backend API)  │
                  │                  └────────┬────────┘
                  │                           │
         ┌────────▼───────────────────────────▼────────┐
         │              AWS Infrastructure              │
         ├──────────────────┬──────────────────────────┤
         │    RDS (PostgreSQL)    │   ElastiCache     │
         │                        │     (Redis)        │
         └────────────────────────┴────────────────────┘
```

## Environment Configuration

### 1. Production Environment Variables

```bash
# .env.production
NODE_ENV=production
FRONTEND_URL=https://wholesale2flip.com
API_URL=https://api.wholesale2flip.com

# Database
DATABASE_URL=postgresql://wtf_prod:${DB_PASSWORD}@wtf-db.cluster-xxxxx.us-east-1.rds.amazonaws.com:5432/wholesale2flip

# Redis
REDIS_URL=redis://wtf-cache.xxxxx.cache.amazonaws.com:6379

# Authentication
JWT_SECRET=${PROD_JWT_SECRET}
JWT_EXPIRE=7d

# Discord OAuth
DISCORD_CLIENT_ID=1234567890
DISCORD_CLIENT_SECRET=${DISCORD_SECRET}
DISCORD_REDIRECT_URI=https://wholesale2flip.com/auth/discord/callback

# Discord Bot
DISCORD_BOT_TOKEN=${BOT_TOKEN}
DISCORD_GUILD_ID=9876543210

# Stripe Production
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
STRIPE_PRICE_BASIC=price_1234567890
STRIPE_PRICE_PRO=price_0987654321
STRIPE_PRICE_ELITE=price_1357924680

# SendGrid
SENDGRID_API_KEY=${SENDGRID_KEY}
SENDGRID_FROM_EMAIL=deals@wholesale2flip.com
SENDGRID_TEMPLATE_WELCOME=d-xxxxx
SENDGRID_TEMPLATE_DEAL_ALERT=d-yyyyy
TC_EMAIL=tc@wholesale2flip.com

# Property Data APIs
ATTOM_API_KEY=${ATTOM_KEY}
ATTOM_API_URL=https://api.gateway.attomdata.com/propertyapi/v1.0.0
RENTOMETER_API_KEY=${RENTOMETER_KEY}

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=${AWS_KEY}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET}
AWS_S3_BUCKET=wholesale2flip-assets
AWS_S3_REGION=us-east-1

# GPT Integration
OPENAI_API_KEY=${OPENAI_KEY}
GPT_SCRIPTMASTER_ID=gpt-scriptmaster-wtf
GPT_UNDERWRITER_ID=gpt-underwriter-wtf

# Monitoring
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
NEW_RELIC_LICENSE_KEY=${NEW_RELIC_KEY}
DATADOG_API_KEY=${DATADOG_KEY}
```

### 2. Infrastructure as Code (Terraform)

```hcl
# terraform/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "wholesale2flip-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "wtf-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = true
  
  tags = {
    Environment = "production"
    Project     = "wholesale2flip"
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier = "wtf-postgres"
  
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.r6g.large"
  allocated_storage = 100
  storage_encrypted = true
  
  db_name  = "wholesale2flip"
  username = "wtf_admin"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
  
  tags = {
    Name = "wtf-postgres"
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "wtf-redis"
  engine              = "redis"
  node_type           = "cache.r6g.large"
  num_cache_nodes     = 1
  parameter_group_name = "default.redis7"
  port                = 6379
  
  subnet_group_name = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]
  
  tags = {
    Name = "wtf-redis"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "wtf-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name = "wtf-cluster"
  }
}

# ALB
resource "aws_lb" "api" {
  name               = "wtf-api-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnets
  
  enable_deletion_protection = true
  enable_http2              = true
  
  tags = {
    Name = "wtf-api-lb"
  }
}
```

### 3. Kubernetes Deployment (Alternative to ECS)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wtf-api
  namespace: wholesale2flip
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wtf-api
  template:
    metadata:
      labels:
        app: wtf-api
    spec:
      containers:
      - name: api
        image: wholesale2flip/api:latest
        ports:
        - containerPort: 5000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: wtf-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: wtf-secrets
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: wtf-api-service
  namespace: wholesale2flip
spec:
  selector:
    app: wtf-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: wtf-api-hpa
  namespace: wholesale2flip
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: wtf-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 4. CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: wholesale2flip
  ECS_SERVICE: wtf-api-service
  ECS_CLUSTER: wtf-cluster
  CONTAINER_NAME: api

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Run linting
        run: npm run lint

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster ${{ env.ECS_CLUSTER }} \
            --service ${{ env.ECS_SERVICE }} \
            --force-new-deployment
      
      - name: Notify Discord
        uses: sarisia/actions-status-discord@v1
        if: always()
        with:
          webhook: ${{ secrets.DISCORD_WEBHOOK }}
          title: "Production Deployment"
          description: "Build ${{ github.sha }} deployed to production"
          color: 0x00ff00
```

### 5. Monitoring & Alerting

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    ports:
      - "3001:3000"

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

### 6. Security Configuration

```nginx
# nginx/nginx.conf
server {
    listen 443 ssl http2;
    server_name wholesale2flip.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/wholesale2flip.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/wholesale2flip.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.wholesale2flip.com wss://api.wholesale2flip.com";

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Proxy to API
    location /api {
        proxy_pass http://api-backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 7. Database Migrations & Seeding

```typescript
// scripts/seed-production.ts
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding production database...');

  // Create admin user
  const adminPassword = await bcrypt.hash(process.env.ADMIN_PASSWORD!, 10);
  const admin = await prisma.user.create({
    data: {
      email: 'admin@wholesale2flip.com',
      firstName: 'Admin',
      lastName: 'User',
      passwordHash: adminPassword,
      subscriptionTier: 'ELITE'
    }
  });

  // Create sample buyer criteria for different states
  const states = ['TX', 'FL', 'GA', 'AZ', 'NC'];
  const buyerTypes = ['FIX_FLIP', 'SECTION_8', 'RENTAL', 'CREATIVE'];
  
  for (const state of states) {
    for (const buyerType of buyerTypes) {
      await prisma.buyerCriteria.create({
        data: {
          userId: admin.id,
          buyerType: buyerType as any,
          states: [state],
          cities: [],
          propertyTypes: ['SINGLE_FAMILY', 'MULTI_FAMILY'],
          minPrice: 50000,
          maxPrice: 500000,
          minROI: 15
        }
      });
    }
  }

  console.log('✅ Production seeding complete!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

### 8. Backup & Disaster Recovery

```bash
#!/bin/bash
# scripts/backup.sh

# Database Backup
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
S3_BUCKET="wholesale2flip-backups"

# Create backup
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/backup_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://$S3_BUCKET/postgres/

# Clean old local backups (keep 7 days)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

# Redis Backup
redis-cli --rdb /backups/redis/dump_$DATE.rdb
aws s3 cp /backups/redis/dump_$DATE.rdb s3://$S3_BUCKET/redis/

# Application files
tar -czf /backups/app/app_$DATE.tar.gz /app
aws s3 cp /backups/app/app_$DATE.tar.gz s3://$S3_BUCKET/app/

echo "Backup completed: $DATE"
```

### 9. Performance Optimization

```typescript
// backend/src/middleware/cache.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { redis } from '../config/redis';

export const cacheMiddleware = (duration: number = 300) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (req.method !== 'GET') {
      return next();
    }

    const key = `cache:${req.originalUrl}`;
    
    try {
      const cached = await redis.get(key);
      
      if (cached) {
        return res.json(JSON.parse(cached));
      }
    } catch (error) {
      console.error('Cache error:', error);
    }

    // Store original send function
    const originalSend = res.json;
    
    // Override send function
    res.json = function(data: any) {
      // Cache the response
      redis.setex(key, duration, JSON.stringify(data));
      
      // Call original send
      return originalSend.call(this, data);
    };
    
    next();
  };
};

// Usage
router.get('/api/properties', cacheMiddleware(300), propertyController.list);
router.get('/api/buyers/by-state', cacheMiddleware(3600), buyerController.byState);
```

### 10. Launch Checklist

- [ ] **Infrastructure**
  - [ ] AWS account setup with proper IAM roles
  - [ ] Domain registered and DNS configured
  - [ ] SSL certificates obtained
  - [ ] CDN configured (CloudFlare)
  
- [ ] **Database**
  - [ ] Production database created
  - [ ] Migrations run
  - [ ] Initial data seeded
  - [ ] Backup system tested
  
- [ ] **Application**
  - [ ] Environment variables set
  - [ ] Docker images built and pushed
  - [ ] Services deployed
  - [ ] Health checks passing
  
- [ ] **Integrations**
  - [ ] Stripe webhooks configured
  - [ ] Discord OAuth app created
  - [ ] Discord bot added to server
  - [ ] SendGrid verified and configured
  - [ ] Property data API keys obtained
  
- [ ] **Monitoring**
  - [ ] Error tracking (Sentry) configured
  - [ ] Application monitoring (New Relic/Datadog) setup
  - [ ] Log aggregation working
  - [ ] Alerts configured
  
- [ ] **Security**
  - [ ] Security audit completed
  - [ ] Penetration testing performed
  - [ ] OWASP compliance checked
  - [ ] Data encryption verified
  
- [ ] **Legal**
  - [ ] Terms of Service published
  - [ ] Privacy Policy published
  - [ ] GDPR compliance verified
  - [ ] Payment processing compliance
  
- [ ] **Marketing**
  - [ ] Landing page live
  - [ ] Social media accounts created
  - [ ] Launch email prepared
  - [ ] Discord community ready

## Post-Launch Monitoring

```javascript
// monitoring/health-checks.js
const checks = [
  {
    name: 'API Health',
    url: 'https://api.wholesale2flip.com/health',
    interval: 60
  },
  {
    name: 'Database Connection',
    url: 'https://api.wholesale2flip.com/health/db',
    interval: 300
  },
  {
    name: 'Redis Connection',
    url: 'https://api.wholesale2flip.com/health/redis',
    interval: 300
  },
  {
    name: 'Discord Bot',
    url: 'https://api.wholesale2flip.com/health/discord',
    interval: 300
  }
];

// Run health checks and alert on failures
setInterval(() => {
  checks.forEach(async (check) => {
    try {
      const response = await fetch(check.url);
      if (!response.ok) {
        await alertTeam(`${check.name} is down!`);
      }
    } catch (error) {
      await alertTeam(`${check.name} is unreachable!`);
    }
  });
}, 60000);
```

## Conclusion

This comprehensive deployment guide ensures the Wholesale2Flip platform is production-ready with:

- Scalable infrastructure
- Secure configuration
- Automated deployment
- Comprehensive monitoring
- Disaster recovery plans
- Performance optimization

Following this guide will result in a robust, enterprise-grade platform ready to handle thousands of users and millions in deal flow.

For questions or support during deployment:
- Technical: tech@wholesale2flip.com
- Discord: Join the #dev-support channel
- Documentation: https://docs.wholesale2flip.com