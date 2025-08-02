// src/lib/auth.ts
import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import GoogleProvider from 'next-auth/providers/google'
import { PrismaAdapter } from '@next-auth/prisma-adapter'
import { prisma } from '@/lib/prisma'
import bcrypt from 'bcryptjs'
import { UserRole } from '@prisma/client'

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  session: {
    strategy: 'jwt'
  },
  pages: {
    signIn: '/auth/signin',
    signUp: '/auth/signup'
  },
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }),
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email }
        })

        if (!user || !user.password) {
          return null
        }

        const isPasswordValid = await bcrypt.compare(
          credentials.password,
          user.password
        )

        if (!isPasswordValid) {
          return null
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role,
          image: user.image
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub!
        session.user.role = token.role as UserRole
      }
      return session
    }
  },
  events: {
    async signIn({ user, isNewUser }) {
      if (isNewUser) {
        await prisma.user.update({
          where: { id: user.id },
          data: { lastLoginAt: new Date() }
        })
      }
    }
// src/app/api/properties/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { z } from 'zod'
import { PropertyType, PropertyCondition } from '@prisma/client'

const createPropertySchema = z.object({
  address: z.string().min(1),
  city: z.string().min(1),
  state: z.string().min(2),
  zipCode: z.string().min(5),
  propertyType: z.nativeEnum(PropertyType),
  bedrooms: z.number().optional(),
  bathrooms: z.number().optional(),
  squareFeet: z.number().optional(),
  yearBuilt: z.number().optional(),
  condition: z.nativeEnum(PropertyCondition).optional(),
  listPrice: z.number().optional(),
  marketValue: z.number().optional(),
  arv: z.number().optional(),
  rehabCost: z.number().optional()
})

export async function GET(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')
    const search = searchParams.get('search')
    const propertyType = searchParams.get('propertyType')
    const minPrice = searchParams.get('minPrice')
    const maxPrice = searchParams.get('maxPrice')

    const skip = (page - 1) * limit

    const where = {
      userId: session.user.id,
      ...(search && {
        OR: [
          { address: { contains: search, mode: 'insensitive' } },
          { city: { contains: search, mode: 'insensitive' } },
          { state: { contains: search, mode: 'insensitive' } }
        ]
      }),
      ...(propertyType && { propertyType: propertyType as PropertyType }),
      ...(minPrice && { listPrice: { gte: parseFloat(minPrice) } }),
      ...(maxPrice && { listPrice: { lte: parseFloat(maxPrice) } })
    }

    const [properties, total] = await Promise.all([
      prisma.property.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        include: {
          deals: {
            select: {
              id: true,
              status: true,
              assignmentFee: true
            }
          }
        }
      }),
      prisma.property.count({ where })
    ])

    return NextResponse.json({
      success: true,
      data: properties,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    })
  } catch (error) {
    console.error('Properties GET error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const data = createPropertySchema.parse(body)

    const property = await prisma.property.create({
      data: {
        ...data,
        userId: session.user.id
      }
    })

    return NextResponse.json({
      success: true,
      message: 'Property created successfully',
      data: property
    })
  } catch (error) {
    console.error('Property creation error:', error)
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input data', details: error.errors },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// src/app/api/properties/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const property = await prisma.property.findFirst({
      where: {
        id: params.id,
        userId: session.user.id
      },
      include: {
        comps: {
          orderBy: { distance: 'asc' },
          take: 10
        },
        deals: {
          include: {
            buyer: true,
            contracts: true
          }
        }
      }
    })

    if (!property) {
      return NextResponse.json(
        { error: 'Property not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      data: property
    })
  } catch (error) {
    console.error('Property GET error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function PUT(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    
    const property = await prisma.property.findFirst({
      where: {
        id: params.id,
        userId: session.user.id
      }
    })

    if (!property) {
      return NextResponse.json(
        { error: 'Property not found' },
        { status: 404 }
      )
    }

    const updatedProperty = await prisma.property.update({
      where: { id: params.id },
      data: body
    })

    return NextResponse.json({
      success: true,
      message: 'Property updated successfully',
      data: updatedProperty
    })
  } catch (error) {
    console.error('Property update error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const property = await prisma.property.findFirst({
      where: {
        id: params.id,
        userId: session.user.id
      }
    })

    if (!property) {
      return NextResponse.json(
        { error: 'Property not found' },
        { status: 404 }
      )
    }

    await prisma.property.delete({
      where: { id: params.id }
    })

    return NextResponse.json({
      success: true,
      message: 'Property deleted successfully'
    })
  } catch (error) {
    console.error('Property delete error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// src/app/api/properties/analyze/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { PropertyAnalysisService } from '@/lib/services/PropertyAnalysisService'

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { address, propertyData } = await req.json()

    if (!address && !propertyData) {
      return NextResponse.json(
        { error: 'Address or property data is required' },
        { status: 400 }
      )
    }

    const analysisService = new PropertyAnalysisService()
    const analysis = await analysisService.analyzeProperty(address || propertyData)

    return NextResponse.json({
      success: true,
      data: analysis
    })
  } catch (error) {
    console.error('Property analysis error:', error)
    return NextResponse.json(
      { error: 'Analysis failed' },
      { status: 500 }
    )
  }
}

// src/app/api/buyers/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { z } from 'zod'
import { PropertyType, DealType } from '@prisma/client'

const createBuyerSchema = z.object({
  propertyTypes: z.array(z.nativeEnum(PropertyType)),
  minPrice: z.number().optional(),
  maxPrice: z.number().optional(),
  minBedrooms: z.number().optional(),
  maxBedrooms: z.number().optional(),
  minBathrooms: z.number().optional(),
  maxBathrooms: z.number().optional(),
  states: z.array(z.string()),
  cities: z.array(z.string()).optional(),
  zipCodes: z.array(z.string()).optional(),
  dealTypes: z.array(z.nativeEnum(DealType)),
  minROI: z.number().optional(),
  minCashFlow: z.number().optional(),
  maxRehabCost: z.number().optional(),
  strategy: z.string().optional()
})

export async function GET(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')
    const search = searchParams.get('search')
    const propertyType = searchParams.get('propertyType')
    const state = searchParams.get('state')

    const skip = (page - 1) * limit

    const where = {
      isVerified: true,
      ...(search && {
        user: {
          OR: [
            { name: { contains: search, mode: 'insensitive' } },
            { email: { contains: search, mode: 'insensitive' } },
            { businessName: { contains: search, mode: 'insensitive' } }
          ]
        }
      }),
      ...(propertyType && {
        propertyTypes: {
          has: propertyType as PropertyType
        }
      }),
      ...(state && {
        states: {
          has: state
        }
      })
    }

    const [buyers, total] = await Promise.all([
      prisma.buyerProfile.findMany({
        where,
        skip,
        take: limit,
        include: {
          user: {
            select: {
              id: true,
              name: true,
              email: true,
              phone: true,
              businessName: true,
              image: true
            }
          },
          deals: {
            select: {
              id: true,
              status: true,
              closingDate: true
            },
            take: 5
          }
        },
        orderBy: { createdAt: 'desc' }
      }),
      prisma.buyerProfile.count({ where })
    ])

    return NextResponse.json({
      success: true,
      data: buyers,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    })
  } catch (error) {
    console.error('Buyers GET error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const data = createBuyerSchema.parse(body)

    // Check if user already has a buyer profile
    const existingProfile = await prisma.buyerProfile.findUnique({
      where: { userId: session.user.id }
    })

    if (existingProfile) {
      return NextResponse.json(
        { error: 'Buyer profile already exists' },
        { status: 400 }
      )
    }

    const buyerProfile = await prisma.buyerProfile.create({
      data: {
        ...data,
        userId: session.user.id
      },
      include: {
        user: {
          select: {
            id: true,
            name: true,
            email: true,
            phone: true,
            businessName: true
          }
        }
      }
    })

    return NextResponse.json({
      success: true,
      message: 'Buyer profile created successfully',
      data: buyerProfile
    })
  } catch (error) {
    console.error('Buyer creation error:', error)
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input data', details: error.errors },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// src/app/api/buyers/match/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { BuyerMatchingService } from '@/lib/services/BuyerMatchingService'

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { propertyId, propertyData } = await req.json()

    if (!propertyId && !propertyData) {
      return NextResponse.json(
        { error: 'Property ID or property data is required' },
        { status: 400 }
      )
    }

    const matchingService = new BuyerMatchingService()
    const matches = await matchingService.findMatches(propertyId || propertyData)

    return NextResponse.json({
      success: true,
      data: matches
    })
  } catch (error) {
    console.error('Buyer matching error:', error)
    return NextResponse.json(
      { error: 'Matching failed' },
      { status: 500 }
    )
  }
}

// src/lib/services/PropertyAnalysisService.ts
import { prisma } from '@/lib/prisma'
import { PropertyAnalysis, CompData } from '@/types/property'

export class PropertyAnalysisService {
  async analyzeProperty(propertyData: any): Promise<PropertyAnalysis> {
    try {
      // Get comparable sales
      const comps = await this.getComparableSales(propertyData)
      
      // Calculate ARV
      const arv = this.calculateARV(propertyData, comps)
      
      // Estimate rehab costs
      const rehabCost = this.estimateRehabCosts(propertyData)
      
      // Calculate max offer (70% rule)
      const maxOffer = (arv * 0.7) - rehabCost
      
      // Calculate profit potential
      const profitPotential = arv - maxOffer - rehabCost
      
      // Calculate ROI
      const roi = maxOffer > 0 ? (profitPotential / maxOffer) * 100 : 0

      return {
        arv,
        rehabCost,
        maxOffer,
        profitPotential,
        roi,
        comps
      }
    } catch (error) {
      console.error('Property analysis error:', error)
      throw new Error('Failed to analyze property')
    }
  }

  private async getComparableSales(propertyData: any): Promise<CompData[]> {
    // In a real implementation, this would query MLS data or property APIs
    // For now, return mock data
    return [
      {
        id: '1',
        address: '123 Similar St',
        salePrice: 285000,
        saleDate: new Date('2024-01-15'),
        bedrooms: propertyData.bedrooms || 3,
        bathrooms: propertyData.bathrooms || 2,
        squareFeet: propertyData.squareFeet || 1800,
        distance: 0.3,
        pricePerSqFt: 158.33
      },
      {
        id: '2',
        address: '456 Nearby Ave',
        salePrice: 295000,
        saleDate: new Date('2024-02-01'),
        bedrooms: propertyData.bedrooms || 3,
        bathrooms: propertyData.bathrooms || 2.5,
        squareFeet: propertyData.squareFeet || 1900,
        distance: 0.5,
        pricePerSqFt: 155.26
      }
    ]
  }

  private calculateARV(propertyData: any, comps: CompData[]): number {
    if (comps.length === 0) return propertyData.listPrice || 0

    // Calculate average price per square foot from comps
    const avgPricePerSqFt = comps.reduce((sum, comp) => sum + comp.pricePerSqFt, 0) / comps.length
    
    // Apply to subject property
    const squareFeet = propertyData.squareFeet || 1800
    return Math.round(avgPricePerSqFt * squareFeet)
  }

  private estimateRehabCosts(propertyData: any): number {
    // Basic rehab cost estimation based on condition and size
    const squareFeet = propertyData.squareFeet || 1800
    const condition = propertyData.condition

    let costPerSqFt = 0
    switch (condition) {
      case 'EXCELLENT':
        costPerSqFt = 0
        break
      case 'GOOD':
        costPerSqFt = 5
        break
      case 'FAIR':
        costPerSqFt = 15
        break
      case 'POOR':
        costPerSqFt = 25
        break
      case 'NEEDS_REHAB':
        costPerSqFt = 40
        break
      default:
        costPerSqFt = 20
    }

    return Math.round(squareFeet * costPerSqFt)
  }
}

// src/lib/services/BuyerMatchingService.ts
import { prisma } from '@/lib/prisma'
import { BuyerMatch } from '@/types/buyer'

export class BuyerMatchingService {
  async findMatches(propertyData: any): Promise<BuyerMatch[]> {
    try {
      const buyers = await prisma.buyerProfile.findMany({
        where: {
          isVerified: true,
          // Match property type
          propertyTypes: {
            has: propertyData.propertyType
          },
          // Match location
          OR: [
            { states: { has: propertyData.state } },
            { cities: { has: propertyData.city } },
            { zipCodes: { has: propertyData.zipCode } }
          ],
          // Match price range
          ...(propertyData.listPrice && {
            AND: [
              { 
                OR: [
                  { minPrice: null },
                  { minPrice: { lte: propertyData.listPrice } }
                ]
              },
              {
                OR: [
                  { maxPrice: null },
                  { maxPrice: { gte: propertyData.listPrice } }
                ]
              }
            ]
          })
        },
        include: {
          user: {
            select: {
              id: true,
              name: true,
              email: true,
              phone: true,
              businessName: true
            }
          }
        }
      })

      // Calculate match scores and return sorted results
      const matches = buyers.map(buyer => ({
        buyer,
        matchScore: this.calculateMatchScore(propertyData, buyer),
        matchReasons: this.getMatchReasons(propertyData, buyer),
        user: buyer.user
      }))

      return matches
        .filter(match => match.matchScore > 50)
        .sort((a, b) => b.matchScore - a.matchScore)
    } catch (error) {
      console.error('Buyer matching error:', error)
      throw new Error('Failed to find buyer matches')
    }
  }

  private calculateMatchScore(propertyData: any, buyer: any): number {
    let score = 0

    // Property type match (30 points)
    if (buyer.propertyTypes.includes(propertyData.propertyType)) {
      score += 30
    }

    // Location match (25 points)
    if (buyer.states.includes(propertyData.state)) score += 15
    if (buyer.cities?.includes(propertyData.city)) score += 5
    if (buyer.zipCodes?.includes(propertyData.zipCode)) score += 5

    // Price range match (20 points)
    if (propertyData.listPrice) {
      const inMinRange = !buyer.minPrice || propertyData.listPrice >= buyer.minPrice
      const inMaxRange = !buyer.maxPrice || propertyData.listPrice <= buyer.maxPrice
      if (inMinRange && inMaxRange) score += 20
    }

    // Bedroom match (15 points)
    if (propertyData.bedrooms && buyer.minBedrooms && buyer.maxBedrooms) {
      if (propertyData.bedrooms >= buyer.minBedrooms && propertyData.bedrooms <= buyer.maxBedrooms) {
        score += 15
      }
    }

    // Bathroom match (10 points)
    if (propertyData.bathrooms && buyer.minBathrooms && buyer.maxBathrooms) {
      if (propertyData.bathrooms >= buyer.minBathrooms && propertyData.bathrooms <= buyer.maxBathrooms) {
        score += 10
      }
    }

    return Math.min(score, 100)
  }

  private getMatchReasons(propertyData: any, buyer: any): string[] {
    const reasons = []

    if (buyer.propertyTypes.includes(propertyData.propertyType)) {
      reasons.push('Property type match')
    }

    if (buyer.states.includes(propertyData.state)) {
      reasons.push('Location preference')
    }

    if (propertyData.listPrice && buyer.minPrice && buyer.maxPrice) {
      if (propertyData.listPrice >= buyer.minPrice && propertyData.listPrice <= buyer.maxPrice) {
        reasons.push('Price range match')
      }
    }

    if (buyer.hasProofOfFunds) {
      reasons.push('Verified buyer with proof of funds')
    }

    return reasons
  }
}

// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

// src/app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import { authOptions } from '@/lib/auth'

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }

// src/app/api/auth/register/route.ts
import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { z } from 'zod'
import { prisma } from '@/lib/prisma'
import { UserRole } from '@prisma/client'

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  firstName: z.string().optional(),
  lastName: z.string().optional(),
  role: z.nativeEnum(UserRole).optional()
})

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { email, password, firstName, lastName, role } = registerSchema.parse(body)

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email }
    })

    if (existingUser) {
      return NextResponse.json(
        { error: 'User already exists with this email' },
        { status: 400 }
      )
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12)

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        firstName,
        lastName,
        name: firstName && lastName ? `${firstName} ${lastName}` : undefined,
        role: role || UserRole.WHOLESALER
      },
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        createdAt: true
      }
    })

    return NextResponse.json({
      success: true,
      message: 'User created successfully',
      user
    })
  } catch (error) {
    console.error('Registration error:', error)
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input data', details: error.errors },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}