// src/app/api/ai/gpt/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
})

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { prompt, context, type = 'general' } = await req.json()

    if (!prompt) {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      )
    }

    let systemPrompt = ''
    switch (type) {
      case 'scriptmaster':
        systemPrompt = `You are ScriptMaster AI, an expert real estate wholesaling coach specializing in cold calling scripts, objection handling, and sales conversations. You have access to Mike K's proven Treasury Vault training materials and scripts. Always provide specific, actionable advice with exact phrases and responses. Focus on:

1. Building rapport quickly
2. Identifying motivated sellers
3. Handling common objections
4. Closing for appointments
5. Following up effectively

Provide responses that sound natural and conversational, not robotic.`
        break

      case 'underwriter':
        systemPrompt = `You are the Multifamily Underwriter GPT, an expert in real estate investment analysis and underwriting. You specialize in:

1. Property valuation and ARV calculations
2. Cash flow analysis and cap rate calculations
3. Market comparisons and trends
4. Risk assessment and due diligence
5. Investment strategy recommendations

Always provide specific numbers, calculations, and reasoning behind your analysis.`
        break

      case 'deal_analysis':
        systemPrompt = `You are a real estate deal analysis expert. Analyze properties for wholesaling potential by evaluating:

1. Market value and ARV potential
2. Rehab cost estimates
3. Profit margins and ROI
4. Market conditions and trends
5. Exit strategy recommendations

Provide clear, actionable insights with specific recommendations.`
        break

      default:
        systemPrompt = `You are a helpful real estate wholesaling assistant with expertise in property analysis, buyer matching, and deal structuring.`
    }

    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: `${prompt}\n\nContext: ${JSON.stringify(context || {})}` }
      ],
      temperature: 0.7,
      max_tokens: 1000
    })

    const response = completion.choices[0]?.message?.content

    return NextResponse.json({
      success: true,
      data: {
        content: response,
        usage: completion.usage
      }
    })
  } catch (error) {
    console.error('AI GPT error:', error)
    return NextResponse.json(
      { error: 'AI request failed' },
      { status: 500 }
    )
  }
}

// src/app/api/contracts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { ContractGenerationService } from '@/lib/services/ContractGenerationService'
import { z } from 'zod'

const createContractSchema = z.object({
  dealId: z.string(),
  type: z.string(),
  purchasePrice: z.number(),
  earnestMoney: z.number().optional(),
  closingDate: z.string().datetime().optional(),
  inspectionPeriod: z.number().optional(),
  buyerInfo: z.object({
    name: z.string(),
    email: z.string().email().optional(),
    phone: z.string().optional(),
    address: z.string().optional()
  }),
  sellerInfo: z.object({
    name: z.string(),
    email: z.string().email().optional(),
    phone: z.string().optional(),
    address: z.string().optional()
  }),
  financing: z.object({
    type: z.string(),
    amount: z.number().optional(),
    rate: z.number().optional(),
    term: z.number().optional()
  }).optional(),
  contingencies: z.array(z.string()),
  agentCommission: z.number().optional(),
  balloonPayment: z.object({
    amount: z.number(),
    years: z.number()
  }).optional(),
  closingCosts: z.enum(['buyer', 'seller', 'split']),
  propertyLiens: z.array(z.object({
    type: z.string(),
    amount: z.number(),
    holder: z.string()
  })).optional(),
  tcInfo: z.object({
    name: z.string().optional(),
    email: z.string().optional(),
    phone: z.string().optional()
  }).optional()
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
    const dealId = searchParams.get('dealId')

    const skip = (page - 1) * limit

    const where = {
      userId: session.user.id,
      ...(dealId && { dealId })
    }

    const [contracts, total] = await Promise.all([
      prisma.contract.findMany({
        where,
        skip,
        take: limit,
        include: {
          deal: {
            select: {
              title: true,
              property: {
                select: {
                  address: true,
                  city: true,
                  state: true
                }
              }
            }
          }
        },
        orderBy: { createdAt: 'desc' }
      