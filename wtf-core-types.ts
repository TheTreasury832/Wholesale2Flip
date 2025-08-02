// src/types/auth.ts
import { UserRole, SubscriptionTier } from '@prisma/client'

export interface User {
  id: string
  email: string
  name?: string
  image?: string
  role: UserRole
  subscriptionTier: SubscriptionTier
  isActive: boolean
  createdAt: Date
  updatedAt: Date
}

export interface AuthSession {
  user: User
  expires: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  firstName?: string
  lastName?: string
  role?: UserRole
}

// src/types/property.ts
import { PropertyType, PropertyCondition, DealType } from '@prisma/client'

export interface PropertyData {
  id: string
  address: string
  city: string
  state: string
  zipCode: string
  propertyType: PropertyType
  bedrooms?: number
  bathrooms?: number
  squareFeet?: number
  yearBuilt?: number
  condition?: PropertyCondition
  listPrice?: number
  marketValue?: number
  arv?: number
  rehabCost?: number
  photos: string[]
  createdAt: Date
}

export interface PropertyAnalysis {
  arv: number
  rehabCost: number
  maxOffer: number
  profitPotential: number
  roi: number
  capRate?: number
  cashFlow?: number
  comps: CompData[]
}

export interface CompData {
  id: string
  address: string
  salePrice: number
  saleDate: Date
  bedrooms?: number
  bathrooms?: number
  squareFeet?: number
  distance: number
  pricePerSqFt: number
  adjustedPrice?: number
}

export interface PropertySearchFilters {
  propertyTypes?: PropertyType[]
  minPrice?: number
  maxPrice?: number
  minBedrooms?: number
  maxBedrooms?: number
  states?: string[]
  cities?: string[]
  zipCodes?: string[]
  condition?: PropertyCondition[]
  sortBy?: 'price' | 'date' | 'profit' | 'roi'
  sortOrder?: 'asc' | 'desc'
}

// src/types/buyer.ts
export interface BuyerProfile {
  id: string
  userId: string
  propertyTypes: PropertyType[]
  minPrice?: number
  maxPrice?: number
  minBedrooms?: number
  maxBedrooms?: number
  minBathrooms?: number
  maxBathrooms?: number
  states: string[]
  cities: string[]
  zipCodes: string[]
  dealTypes: DealType[]
  minROI?: number
  minCashFlow?: number
  maxRehabCost?: number
  hasProofOfFunds: boolean
  strategy?: string
  isVerified: boolean
  createdAt: Date
}

export interface BuyerMatch {
  buyer: BuyerProfile
  matchScore: number
  matchReasons: string[]
  user: {
    name?: string
    email: string
    phone?: string
  }
}

// src/types/lead.ts
import { LeadSource, LeadStatus } from '@prisma/client'

export interface Lead {
  id: string
  firstName?: string
  lastName?: string
  email?: string
  phone?: string
  propertyAddress: string
  city: string
  state: string
  zipCode: string
  source: LeadSource
  status: LeadStatus
  motivation?: string
  timeline?: string
  lastContact?: Date
  nextFollowUp?: Date
  leadScore?: number
  notes?: string
  createdAt: Date
}

export interface LeadActivity {
  id: string
  type: string
  title: string
  description?: string
  scheduledAt?: Date
  completedAt?: Date
  isCompleted: boolean
  outcome?: string
  createdAt: Date
}

export interface LeadImportData {
  firstName?: string
  lastName?: string
  email?: string
  phone?: string
  address: string
  city: string
  state: string
  zipCode: string
  source?: LeadSource
  motivation?: string
  notes?: string
}

// src/types/deal.ts
import { DealStatus, DealType } from '@prisma/client'

export interface Deal {
  id: string
  title: string
  status: DealStatus
  dealType: DealType
  purchasePrice: number
  arvPrice?: number
  rehabCost?: number
  assignmentFee?: number
  contractDate?: Date
  closingDate?: Date
  property?: PropertyData
  lead?: Lead
  buyer?: BuyerProfile
  progress: DealProgress
  createdAt: Date
}

export interface DealProgress {
  currentStage: string
  stages: DealStage[]
  completion: number
}

export interface DealStage {
  name: string
  completed: boolean
  completedAt?: Date
  tasks: DealTask[]
}

export interface DealTask {
  id: string
  title: string
  completed: boolean
  dueDate?: Date
  assignedTo?: string
}

// src/types/contract.ts
export interface Contract {
  id: string
  type: string
  status: string
  purchasePrice: number
  earnestMoney?: number
  closingDate?: Date
  inspectionPeriod?: number
  buyerInfo: ContractParty
  sellerInfo: ContractParty
  terms: ContractTerms
  documentUrl?: string
  isExecuted: boolean
  createdAt: Date
}

export interface ContractParty {
  name: string
  email?: string
  phone?: string
  address?: string
}

export interface ContractTerms {
  financing?: FinancingTerms
  contingencies: string[]
  repairs?: RepairTerms
  inclusions: string[]
  exclusions: string[]
}

export interface FinancingTerms {
  type: string
  amount?: number
  rate?: number
  term?: number
  downPayment?: number
}

export interface RepairTerms {
  maxAmount?: number
  responsibility: 'buyer' | 'seller' | 'split'
  items: string[]
}

export interface ContractFormData {
  purchasePrice: number
  earnestMoney?: number
  closingDate?: Date
  inspectionPeriod?: number
  buyerName: string
  buyerEmail?: string
  buyerPhone?: string
  sellerName: string
  sellerEmail?: string
  sellerPhone?: string
  financing?: FinancingTerms
  contingencies: string[]
  repairs?: RepairTerms
  agentCommission?: number
  balloonPayment?: BalloonPaymentTerms
  closingCosts: 'buyer' | 'seller' | 'split'
  propertyLiens?: LienInfo[]
  tcName?: string
  tcEmail?: string
  tcPhone?: string
}

export interface BalloonPaymentTerms {
  amount: number
  dueDate: Date
  years: number
}

export interface LienInfo {
  type: string
  amount: number
  holder: string
  accountNumber?: string
}

// src/types/analytics.ts
export interface DashboardMetrics {
  totalProperties: number
  totalLeads: number
  totalDeals: number
  activeBuyers: number
  revenueThisMonth: number
  conversionRate: number
  averageDealSize: number
  pipelineValue: number
}

export interface ChartData {
  labels: string[]
  datasets: {
    label: string
    data: number[]
    backgroundColor?: string[]
    borderColor?: string
    fill?: boolean
  }[]
}

export interface RevenueMetrics {
  monthly: number[]
  quarterly: number[]
  yearly: number[]
  growth: {
    monthly: number
    quarterly: number
    yearly: number
  }
}

export interface LeadMetrics {
  totalLeads: number
  newLeads: number
  convertedLeads: number
  conversionRate: number
  leadsBySource: Record<LeadSource, number>
  leadsByStatus: Record<LeadStatus, number>
}

export interface DealMetrics {
  totalDeals: number
  closedDeals: number
  averageDealSize: number
  totalRevenue: number
  dealsByType: Record<DealType, number>
  dealsByStatus: Record<DealStatus, number>
  monthlyClosings: number[]
}

// src/types/api.ts
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
    hasNext: boolean
    hasPrev: boolean
  }
}

export interface ApiError {
  code: string
  message: string
  details?: any
}

// src/types/ai.ts
export interface AIAnalysis {
  propertyAnalysis?: PropertyAIAnalysis
  leadAnalysis?: LeadAIAnalysis
  marketAnalysis?: MarketAIAnalysis
  dealAnalysis?: DealAIAnalysis
}

export interface PropertyAIAnalysis {
  estimatedARV: number
  confidence: number
  rehabEstimate: number
  profitPotential: 'low' | 'medium' | 'high'
  recommendations: string[]
  risks: string[]
  marketComparison: string
}

export interface LeadAIAnalysis {
  motivationScore: number
  timeline: string
  likelihood: 'low' | 'medium' | 'high'
  recommendedApproach: string
  objections: string[]
  nextSteps: string[]
}

export interface MarketAIAnalysis {
  trendDirection: 'up' | 'down' | 'stable'
  priceGrowth: number
  demandLevel: 'low' | 'medium' | 'high'
  investmentGrade: 'A' | 'B' | 'C' | 'D'
  opportunities: string[]
  threats: string[]
}

export interface DealAIAnalysis {
  dealQuality: 'poor' | 'fair' | 'good' | 'excellent'
  riskLevel: 'low' | 'medium' | 'high'
  timeToClose: number
  recommendedStrategy: string
  potentialIssues: string[]
  successProbability: number
}

export interface GPTRequest {
  prompt: string
  context?: any
  temperature?: number
  maxTokens?: number
}

export interface GPTResponse {
  content: string
  usage: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
}

// src/types/discord.ts
export interface DiscordWebhook {
  content?: string
  embeds?: DiscordEmbed[]
  username?: string
  avatarUrl?: string
}

export interface DiscordEmbed {
  title?: string
  description?: string
  color?: number
  fields?: DiscordField[]
  footer?: {
    text: string
    iconUrl?: string
  }
  timestamp?: string
  thumbnail?: {
    url: string
  }
  image?: {
    url: string
  }
}

export interface DiscordField {
  name: string
  value: string
  inline?: boolean
}

// src/types/notifications.ts
export interface Notification {
  id: string
  type: string
  title: string
  message: string
  priority: 'low' | 'normal' | 'high' | 'urgent'
  isRead: boolean
  actionUrl?: string
  actionLabel?: string
  createdAt: Date
}

export interface NotificationPreferences {
  email: boolean
  sms: boolean
  push: boolean
  discord: boolean
  types: {
    dealAlerts: boolean
    leadUpdates: boolean
    taskReminders: boolean
    systemUpdates: boolean
    marketingUpdates: boolean
  }
}

// src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency
  }).format(amount)
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat('en-US').format(num)
}

export function formatDate(date: Date | string, format: 'short' | 'long' | 'relative' = 'short'): string {
  const d = new Date(date)
  
  if (format === 'relative') {
    const now = new Date()
    const diff = now.getTime() - d.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    
    if (days === 0) return 'Today'
    if (days === 1) return 'Yesterday'
    if (days < 7) return `${days} days ago`
    if (days < 30) return `${Math.floor(days / 7)} weeks ago`
    return `${Math.floor(days / 30)} months ago`
  }
  
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: format === 'long' ? 'long' : 'short',
    day: 'numeric'
  })
}

export function formatPhoneNumber(phone: string): string {
  const cleaned = phone.replace(/\D/g, '')
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
  if (match) {
    return `(${match[1]}) ${match[2]}-${match[3]}`
  }
  return phone
}

export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

export function calculateROI(profit: number, investment: number): number {
  if (investment === 0) return 0
  return (profit / investment) * 100
}

export function calculateCapRate(noi: number, propertyValue: number): number {
  if (propertyValue === 0) return 0
  return (noi / propertyValue) * 100
}

export function calculateCashFlow(
  rent: number,
  mortgage: number,
  taxes: number,
  insurance: number,
  maintenance: number = 0
): number {
  return rent - mortgage - taxes - insurance - maintenance
}

export function calculateLTV(loanAmount: number, propertyValue: number): number {
  if (propertyValue === 0) return 0
  return (loanAmount / propertyValue) * 100
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export function validatePhone(phone: string): boolean {
  const phoneRegex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/
  return phoneRegex.test(phone.replace(/\s/g, ''))
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w ]+/g, '')
    .replace(/ +/g, '-')
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

export function copyToClipboard(text: string): Promise<void> {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text)
  } else {
    return new Promise((resolve, reject) => {
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      try {
        document.execCommand('copy')
        resolve()
      } catch (err) {
        reject(err)
      }
      document.body.removeChild(textArea)
    })
  }
}

// src/lib/constants.ts
export const PROPERTY_TYPES = {
  SINGLE_FAMILY: 'Single Family',
  MULTI_FAMILY: 'Multi Family',
  CONDO: 'Condo',
  TOWNHOUSE: 'Townhouse',
  LAND: 'Land',
  COMMERCIAL: 'Commercial',
  MOBILE_HOME: 'Mobile Home'
} as const

export const PROPERTY_CONDITIONS = {
  EXCELLENT: 'Excellent',
  GOOD: 'Good',
  FAIR: 'Fair',
  POOR: 'Poor',
  NEEDS_REHAB: 'Needs Rehab'
} as const

export const DEAL_TYPES = {
  CASH: 'Cash',
  CREATIVE: 'Creative',
  SUBJECT_TO: 'Subject To',
  SELLER_FINANCE: 'Seller Finance',
  LEASE_OPTION: 'Lease Option'
} as const

export const DEAL_STATUSES = {
  LEAD: 'Lead',
  UNDER_CONTRACT: 'Under Contract',
  PENDING: 'Pending',
  CLOSED: 'Closed',
  CANCELLED: 'Cancelled'
} as const

export const LEAD_SOURCES = {
  DRIVING_FOR_DOLLARS: 'Driving for Dollars',
  DIRECT_MAIL: 'Direct Mail',
  COLD_CALLING: 'Cold Calling',
  PPC: 'Pay Per Click',
  SEO: 'SEO',
  REFERRAL: 'Referral',
  SOCIAL_MEDIA: 'Social Media',
  LIGHTNING_LEADS: 'Lightning Leads',
  IMPORTED: 'Imported'
} as const

export const LEAD_STATUSES = {
  NEW: 'New',
  CONTACTED: 'Contacted',
  INTERESTED: 'Interested',
  NOT_INTERESTED: 'Not Interested',
  CALLBACK: 'Callback',
  DEAL: 'Deal',
  DEAD: 'Dead'
} as const

export const USER_ROLES = {
  ADMIN: 'Admin',
  WHOLESALER: 'Wholesaler',
  BUYER: 'Buyer',
  AGENT: 'Agent',
  INVESTOR: 'Investor'
} as const

export const SUBSCRIPTION_TIERS = {
  FREE: 'Free',
  BASIC: 'Basic',
  PRO: 'Pro',
  ENTERPRISE: 'Enterprise'
} as const

export const US_STATES = [
  { code: 'AL', name: 'Alabama' },
  { code: 'AK', name: 'Alaska' },
  { code: 'AZ', name: 'Arizona' },
  { code: 'AR', name: 'Arkansas' },
  { code: 'CA', name: 'California' },
  { code: 'CO', name: 'Colorado' },
  { code: 'CT', name: 'Connecticut' },
  { code: 'DE', name: 'Delaware' },
  { code: 'FL', name: 'Florida' },
  { code: 'GA', name: 'Georgia' },
  { code: 'HI', name: 'Hawaii' },
  { code: 'ID', name: 'Idaho' },
  { code: 'IL', name: 'Illinois' },
  { code: 'IN', name: 'Indiana' },
  { code: 'IA', name: 'Iowa' },
  { code: 'KS', name: 'Kansas' },
  { code: 'KY', name: 'Kentucky' },
  { code: 'LA', name: 'Louisiana' },
  { code: 'ME', name: 'Maine' },
  { code: 'MD', name: 'Maryland' },
  { code: 'MA', name: 'Massachusetts' },
  { code: 'MI', name: 'Michigan' },
  { code: 'MN', name: 'Minnesota' },
  { code: 'MS', name: 'Mississippi' },
  { code: 'MO', name: 'Missouri' },
  { code: 'MT', name: 'Montana' },
  { code: 'NE', name: 'Nebraska' },
  { code: 'NV', name: 'Nevada' },
  { code: 'NH', name: 'New Hampshire' },
  { code: 'NJ', name: 'New Jersey' },
  { code: 'NM', name: 'New Mexico' },
  { code: 'NY', name: 'New York' },
  { code: 'NC', name: 'North Carolina' },
  { code: 'ND', name: 'North Dakota' },
  { code: 'OH', name: 'Ohio' },
  { code: 'OK', name: 'Oklahoma' },
  { code: 'OR', name: 'Oregon' },
  { code: 'PA', name: 'Pennsylvania' },
  { code: 'RI', name: 'Rhode Island' },
  { code: 'SC', name: 'South Carolina' },
  { code: 'SD', name: 'South Dakota' },
  { code: 'TN', name: 'Tennessee' },
  { code: 'TX', name: 'Texas' },
  { code: 'UT', name: 'Utah' },
  { code: 'VT', name: 'Vermont' },
  { code: 'VA', name: 'Virginia' },
  { code: 'WA', name: 'Washington' },
  { code: 'WV', name: 'West Virginia' },
  { code: 'WI', name: 'Wisconsin' },
  { code: 'WY', name: 'Wyoming' }
] as const

export const DEFAULT_PAGINATION = {
  page: 1,
  limit: 20
} as const

export const API_ENDPOINTS = {
  AUTH: '/api/auth',
  PROPERTIES: '/api/properties',
  BUYERS: '/api/buyers',
  LEADS: '/api/leads',
  DEALS: '/api/deals',
  CONTRACTS: '/api/contracts',
  ANALYTICS: '/api/analytics',
  AI: '/api/ai'
} as const
  