// src/app/dashboard/layout.tsx
import { Sidebar } from '@/components/layout/Sidebar'
import { DashboardHeader } from '@/components/layout/DashboardHeader'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await getServerSession(authOptions)
  
  if (!session) {
    redirect('/auth/signin')
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <div className="flex">
        <Sidebar />
        <div className="flex-1 flex flex-col min-h-screen ml-64">
          <DashboardHeader />
          <main className="flex-1 p-6">
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}

// src/app/dashboard/page.tsx
import { DashboardMetrics } from '@/components/analytics/Dashboard'
import { RecentDeals } from '@/components/pipeline/RecentDeals'
import { PropertySearch } from '@/components/property/PropertySearch'
import { QuickActions } from '@/components/dashboard/QuickActions'
import { AIInsights } from '@/components/ai/AIInsights'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 mt-1">Welcome back! Here's what's happening with your deals.</p>
        </div>
        <QuickActions />
      </div>

      {/* Main Property Search */}
      <PropertySearch />

      {/* Metrics */}
      <DashboardMetrics />

      {/* Grid Layout */}
      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <RecentDeals />
        </div>
        <div>
          <AIInsights />
        </div>
      </div>
    </div>
  )
}

// src/components/layout/Sidebar.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import {
  Home,
  Search,
  Users,
  FileText,
  TrendingUp,
  Zap,
  Settings,
  PieChart,
  MapPin,
  MessageSquare,
  Brain,
  ChevronLeft,
  ChevronRight,
  Building
} from 'lucide-react'

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: Home
  },
  {
    name: 'Properties',
    href: '/dashboard/properties',
    icon: Building
  },
  {
    name: 'BuyBoxes',
    href: '/dashboard/buyers',
    icon: Users
  },
  {
    name: 'Pipeline',
    href: '/dashboard/pipeline',
    icon: TrendingUp
  },
  {
    name: 'Leads',
    href: '/dashboard/leads',
    icon: Search
  },
  {
    name: 'Contracts',
    href: '/dashboard/contracts',
    icon: FileText
  },
  {
    name: 'Lightning Leads',
    href: '/dashboard/lightning-leads',
    icon: Zap
  },
  {
    name: 'Analytics',
    href: '/dashboard/analytics',
    icon: PieChart
  },
  {
    name: 'AI Assistant',
    href: '/dashboard/ai',
    icon: Brain
  },
  {
    name: 'Discord',
    href: '/dashboard/discord',
    icon: MessageSquare
  }
]

const bottomNavigation = [
  {
    name: 'Settings',
    href: '/dashboard/settings',
    icon: Settings
  }
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const pathname = usePathname()

  return (
    <div className={cn(
      "fixed left-0 top-0 z-40 h-screen bg-gray-800 border-r border-gray-700 transition-all duration-300",
      collapsed ? "w-16" : "w-64"
    )}>
      <div className="flex flex-col h-full">
        {/* Logo Section */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          {!collapsed && (
            <Link href="/dashboard" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-wtf-gradient rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">WTF</span>
            </Link>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1 rounded-lg hover:bg-gray-700 transition-colors"
          >
            {collapsed ? (
              <ChevronRight className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronLeft className="w-5 h-5 text-gray-400" />
            )}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors",
                  isActive
                    ? "bg-wtf-purple text-white"
                    : "text-gray-300 hover:bg-gray-700 hover:text-white",
                  collapsed && "justify-center"
                )}
                title={collapsed ? item.name : undefined}
              >
                <item.icon className={cn("w-5 h-5", !collapsed && "mr-3")} />
                {!collapsed && item.name}
              </Link>
            )
          })}
        </nav>

        {/* Bottom Navigation */}
        <div className="p-3 border-t border-gray-700">
          {bottomNavigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors",
                  isActive
                    ? "bg-wtf-purple text-white"
                    : "text-gray-300 hover:bg-gray-700 hover:text-white",
                  collapsed && "justify-center"
                )}
                title={collapsed ? item.name : undefined}
              >
                <item.icon className={cn("w-5 h-5", !collapsed && "mr-3")} />
                {!collapsed && item.name}
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}

// src/components/layout/DashboardHeader.tsx
'use client'

import { Bell, Search, User, Settings, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { useSession, signOut } from 'next-auth/react'
import Link from 'next/link'

export function DashboardHeader() {
  const { data: session } = useSession()

  return (
    <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search */}
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              placeholder="Search properties, leads, buyers..."
              className="pl-10 bg-gray-700 border-gray-600 text-white placeholder-gray-400"
            />
          </div>
        </div>

        {/* Right Side */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="relative">
                <Bell className="w-5 h-5 text-gray-400" />
                <Badge className="absolute -top-1 -right-1 w-5 h-5 text-xs bg-wtf-purple">
                  3
                </Badge>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80">
              <div className="p-3 border-b">
                <h3 className="font-semibold">Notifications</h3>
              </div>
              <div className="p-3 space-y-3">
                <div className="text-sm">
                  <p className="font-medium">New buyer match found</p>
                  <p className="text-gray-500">123 Main St property matched with 2 buyers</p>
                  <p className="text-xs text-gray-400 mt-1">5 minutes ago</p>
                </div>
                <div className="text-sm">
                  <p className="font-medium">Contract generated</p>
                  <p className="text-gray-500">Purchase agreement ready for 456 Oak Ave</p>
                  <p className="text-xs text-gray-400 mt-1">1 hour ago</p>
                </div>
                <div className="text-sm">
                  <p className="font-medium">Lightning lead received</p>
                  <p className="text-gray-500">High-quality lead in Dallas, TX</p>
                  <p className="text-xs text-gray-400 mt-1">2 hours ago</p>
                </div>
              </div>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* User Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={session?.user?.image || ''} alt={session?.user?.name || ''} />
                  <AvatarFallback>
                    {session?.user?.name?.charAt(0) || session?.user?.email?.charAt(0) || 'U'}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end">
              <div className="flex items-center justify-start gap-2 p-2">
                <div className="flex flex-col space-y-1 leading-none">
                  {session?.user?.name && (
                    <p className="font-medium">{session.user.name}</p>
                  )}
                  {session?.user?.email && (
                    <p className="w-[200px] truncate text-sm text-muted-foreground">
                      {session.user.email}
                    </p>
                  )}
                </div>
              </div>
              <DropdownMenuSeparator />
              <DropdownMenuItem asChild>
                <Link href="/dashboard/profile" className="cursor-pointer">
                  <User className="mr-2 h-4 w-4" />
                  Profile
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem asChild>
                <Link href="/dashboard/settings" className="cursor-pointer">
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="cursor-pointer"
                onSelect={() => signOut({ callbackUrl: '/' })}
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sign out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}

// src/components/property/PropertySearch.tsx
'use client'

import { useState } from 'react'
import { Search, MapPin, Calculator, TrendingUp } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { motion } from 'framer-motion'

export function PropertySearch() {
  const [address, setAddress] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async () => {
    if (!address.trim()) return
    
    setIsLoading(true)
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false)
      // Navigate to property analysis page
      window.location.href = `/dashboard/properties/analyze?address=${encodeURIComponent(address)}`
    }, 2000)
  }

  return (
    <Card className="bg-gradient-to-r from-wtf-purple/10 to-wtf-green/10 border-wtf-purple/30">
      <CardHeader>
        <CardTitle className="text-2xl text-white flex items-center gap-2">
          <Search className="w-6 h-6" />
          Pop In Your Address
        </CardTitle>
        <CardDescription className="text-gray-300">
          Let's find you a buyer and analyze this deal
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Enter property address (e.g., 123 Main St, City, State)"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                className="pl-10 bg-gray-800 border-gray-600 text-white placeholder-gray-400"
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <Button 
              onClick={handleSearch}
              disabled={!address.trim() || isLoading}
              className="bg-wtf-gradient hover:opacity-90 px-6"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                'Find Buyers'
              )}
            </Button>
          </div>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-3 gap-4 pt-4">
            <motion.div 
              className="text-center p-3 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors cursor-pointer"
              whileHover={{ scale: 1.02 }}
            >
              <Calculator className="w-5 h-5 text-wtf-purple mx-auto mb-1" />
              <div className="text-sm text-gray-300">ARV Calculator</div>
            </motion.div>
            <motion.div 
              className="text-center p-3 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors cursor-pointer"
              whileHover={{ scale: 1.02 }}
            >
              <TrendingUp className="w-5 h-5 text-wtf-green mx-auto mb-1" />
              <div className="text-sm text-gray-300">Comps Analysis</div>
            </motion.div>
            <motion.div 
              className="text-center p-3 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors cursor-pointer"
              whileHover={{ scale: 1.02 }}
            >
              <Search className="w-5 h-5 text-wtf-blue mx-auto mb-1" />
              <div className="text-sm text-gray-300">Buyer Match</div>
            </motion.div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

// src/components/dashboard/QuickActions.tsx
'use client'

import { Plus, Upload, Zap, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import Link from 'next/link'

export function QuickActions() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button className="bg-wtf-gradient hover:opacity-90">
          <Plus className="w-4 h-4 mr-2" />
          Quick Actions
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuItem asChild>
          <Link href="/dashboard/properties/new" className="cursor-pointer">
            <Plus className="mr-2 h-4 w-4" />
            Add Property
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <Link href="/dashboard/leads/import" className="cursor-pointer">
            <Upload className="mr-2 h-4 w-4" />
            Import Leads
          </Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Link href="/dashboard/lightning-leads" className="cursor-pointer">
            <Zap className="mr-2 h-4 w-4" />
            Lightning Leads
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <Link href="/dashboard/buyers/new" className="cursor-pointer">
            <Users className="mr-2 h-4 w-4" />
            Add Buyer
          </Link>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

// src/components/property/PropertyCard.tsx
'use client'

import { useState } from 'react'
import Image from 'next/image'
import { 
  MapPin, 
  Bed, 
  Bath, 
  Square, 
  Calendar, 
  DollarSign, 
  TrendingUp,
  Users,
  Eye,
  Heart
} from 'lucide-react'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { formatCurrency, formatNumber } from '@/lib/utils'
import { PropertyData } from '@/types/property'
import { motion } from 'framer-motion'

interface PropertyCardProps {
  property: PropertyData
  onView?: (id: string) => void
  onFindBuyers?: (id: string) => void
}

export function PropertyCard({ property, onView, onFindBuyers }: PropertyCardProps) {
  const [isLiked, setIsLiked] = useState(false)
  const [imageError, setImageError] = useState(false)

  const profitPotential = property.arv && property.rehabCost 
    ? property.arv - (property.listPrice || 0) - property.rehabCost 
    : 0

  const roi = property.listPrice ? (profitPotential / property.listPrice) * 100 : 0

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <Card className="bg-gray-800 border-gray-700 overflow-hidden hover:border-wtf-purple/50 transition-all duration-300">
        {/* Image Section */}
        <div className="relative h-48 bg-gray-700">
          {property.photos && property.photos.length > 0 && !imageError ? (
            <Image
              src={property.photos[0]}
              alt={property.address}
              fill
              className="object-cover"
              onError={() => setImageError(true)}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <div className="text-center">
                <MapPin className="w-12 h-12 text-gray-500 mx-auto mb-2" />
                <p className="text-gray-500 text-sm">No Image</p>
              </div>
            </div>
          )}
          
          {/* Overlay Actions */}
          <div className="absolute top-3 right-3 flex gap-2">
            <Button
              size="sm"
              variant="secondary"
              className="w-8 h-8 p-0 bg-black/50 backdrop-blur-sm border-0"
              onClick={() => setIsLiked(!isLiked)}
            >
              <Heart className={`w-4 h-4 ${isLiked ? 'fill-red-500 text-red-500' : 'text-white'}`} />
            </Button>
          </div>

          {/* Property Type Badge */}
          <div className="absolute top-3 left-3">
            <Badge className="bg-wtf-purple">
              {property.propertyType.replace('_', ' ')}
            </Badge>
          </div>

          {/* ROI Badge */}
          {roi > 0 && (
            <div className="absolute bottom-3 left-3">
              <Badge className="bg-wtf-green">
                {roi.toFixed(1)}% ROI
              </Badge>
            </div>
          )}
        </div>

        <CardContent className="p-4">
          {/* Address */}
          <div className="mb-3">
            <h3 className="text-lg font-semibold text-white mb-1 line-clamp-1">
              {property.address}
            </h3>
            <p className="text-gray-400 text-sm flex items-center">
              <MapPin className="w-3 h-3 mr-1" />
              {property.city}, {property.state} {property.zipCode}
            </p>
          </div>

          {/* Property Details */}
          <div className="flex items-center gap-4 mb-3 text-sm text-gray-400">
            {property.bedrooms && (
              <div className="flex items-center">
                <Bed className="w-4 h-4 mr-1" />
                {property.bedrooms}
              </div>
            )}
            {property.bathrooms && (
              <div className="flex items-center">
                <Bath className="w-4 h-4 mr-1" />
                {property.bathrooms}
              </div>
            )}
            {property.squareFeet && (
              <div className="flex items-center">
                <Square className="w-4 h-4 mr-1" />
                {formatNumber(property.squareFeet)} sqft
              </div>
            )}
            {property.yearBuilt && (
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-1" />
                {property.yearBuilt}
              </div>
            )}
          </div>

          {/* Financial Info */}
          <div className="space-y-2">
            {property.listPrice && (
              <div className="flex justify-between items-center">
                <span className="text-gray-400">List Price:</span>
                <span className="text-white font-semibold">
                  {formatCurrency(property.listPrice)}
                </span>
              </div>
            )}
            {property.arv && (
              <div className="flex justify-between items-center">
                <span className="text-gray-400">ARV:</span>
                <span className="text-wtf-green font-semibold">
                  {formatCurrency(property.arv)}
                </span>
              </div>
            )}
            {profitPotential > 0 && (
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Profit Potential:</span>
                <span className="text-wtf-purple font-semibold">
                  {formatCurrency(profitPotential)}
                </span>
              </div>
            )}
          </div>
        </CardContent>

        <CardFooter className="p-4 pt-0 flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="flex-1 border-gray-600 text-gray-300 hover:bg-gray-700"
            onClick={() => onView?.(property.id)}
          >
            <Eye className="w-4 h-4 mr-2" />
            View Details
          </Button>
          <Button
            size="sm"
            className="flex-1 bg-wtf-gradient hover:opacity-90"
            onClick={() => onFindBuyers?.(property.id)}
          >
            <Users className="w-4 h-4 mr-2" />
            Find Buyers
          </Button>
        </CardFooter>
      </Card>
    </motion.div>
  )
}

// src/components/property/PropertyForm.tsx
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { PROPERTY_TYPES, PROPERTY_CONDITIONS } from '@/lib/constants'
import { PropertyType, PropertyCondition } from '@prisma/client'

const propertySchema = z.object({
  address: z.string().min(1, 'Address is required'),
  city: z.string().min(1, 'City is required'),
  state: z.string().min(2, 'State is required'),
  zipCode: z.string().min(5, 'ZIP code is required'),
  propertyType: z.nativeEnum(PropertyType),
  bedrooms: z.number().min(0).optional(),
  bathrooms: z.number().min(0).optional(),
  squareFeet: z.number().min(0).optional(),
  yearBuilt: z.number().min(1800).max(new Date().getFullYear()).optional(),
  condition: z.nativeEnum(PropertyCondition).optional(),
  listPrice: z.number().min(0).optional(),
  description: z.string().optional()
})

type PropertyFormData = z.infer<typeof propertySchema>

interface PropertyFormProps {
  onSubmit: (data: PropertyFormData) => Promise<void>
  defaultValues?: Partial<PropertyFormData>
  isLoading?: boolean
}

export function PropertyForm({ onSubmit, defaultValues, isLoading }: PropertyFormProps) {
  const [submitError, setSubmitError] = useState<string | null>(null)

  const form = useForm<PropertyFormData>({
    resolver: zodResolver(propertySchema),
    defaultValues
  })

  const handleSubmit = async (data: PropertyFormData) => {
    try {
      setSubmitError(null)
      await onSubmit(data)
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'An error occurred')
    }
  }

  return (
    <Card className="bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-white">Property Information</CardTitle>
        <CardDescription>
          Enter the property details to analyze and find buyers
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
          {/* Address Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Address</h3>
            <div className="grid gap-4">
              <div>
                <Label htmlFor="address" className="text-gray-300">Street Address</Label>
                <Input
                  id="address"
                  {...form.register('address')}
                  placeholder="123 Main Street"
                  className="bg-gray-700 border-gray-600 text-white"
                />
                {form.formState.errors.address && (
                  <p className="text-red-400 text-sm mt-1">{form.formState.errors.address.message}</p>
                )}
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="city" className="text-gray-300">City</Label>
                  <Input
                    id="city"
                    {...form.register('city')}
                    placeholder="City"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                  {form.formState.errors.city && (
                    <p className="text-red-400 text-sm mt-1">{form.formState.errors.city.message}</p>
                  )}
                </div>
                <div>
                  <Label htmlFor="state" className="text-gray-300">State</Label>
                  <Input
                    id="state"
                    {...form.register('state')}
                    placeholder="TX"
                    maxLength={2}
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                  {form.formState.errors.state && (
                    <p className="text-red-400 text-sm mt-1">{form.formState.errors.state.message}</p>
                  )}
                </div>
                <div>
                  <Label htmlFor="zipCode" className="text-gray-300">ZIP Code</Label>
                  <Input
                    id="zipCode"
                    {...form.register('zipCode')}
                    placeholder="12345"
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                  {form.formState.errors.zipCode && (
                    <p className="text-red-400 text-sm mt-1">{form.formState.errors.zipCode.message}</p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Property Details */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Property Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="propertyType" className="text-gray-300">Property Type</Label>
                <Select onValueChange={(value) => form.setValue('propertyType', value as PropertyType)}>
                  <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                    <SelectValue placeholder="Select property type" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(PROPERTY_TYPES).map(([key, value]) => (
                      <SelectItem key={key} value={key}>{value}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {form.formState.errors.propertyType && (
                  <p className="text-red-400 text-sm mt-1">{form.formState.errors.propertyType.message}</p>
                )}
              </div>
              <div>
                <Label htmlFor="condition" className="text-gray-300">Condition</Label>
                <Select onValueChange={(value) => form.setValue('condition', value as PropertyCondition)}>
                  <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                    <SelectValue placeholder="Select condition" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(PROPERTY_CONDITIONS).map(([key, value]) => (
                      <SelectItem key={key} value={key}>{value}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            <div className="grid grid-cols-4 gap-4">
              <div>
                <Label htmlFor="bedrooms" className="text-gray-300">Bedrooms</Label>
                <Input
                  id="bedrooms"
                  type="number"
                  {...form.register('bedrooms', { valueAsNumber: true })}
                  placeholder="3"
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <div>
                <Label htmlFor="bathrooms" className="text-gray-300">Bathrooms</Label>
                <Input
                  id="bathrooms"
                  type="number"
                  step="0.5"
                  {...form.register('bathrooms', { valueAsNumber: true })}
                  placeholder="2.5"
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <div>
                <Label htmlFor="squareFeet" className="text-gray-300">Square Feet</Label>
                <Input
                  id="squareFeet"
                  type="number"
                  {...form.register('squareFeet', { valueAsNumber: true })}
                  placeholder="2000"
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              <div>
                <Label htmlFor="yearBuilt" className="text-gray-300">Year Built</Label>
                <Input
                  id="yearBuilt"
                  type="number"
                  {...form.register('yearBuilt', { valueAsNumber: true })}
                  placeholder="1995"
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
            </div>
          </div>

          {/* Financial Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Financial Information</h3>
            <div>
              <Label htmlFor="listPrice" className="text-gray-300">List Price</Label>
              <Input
                id="listPrice"
                type="number"
                {...form.register('listPrice', { valueAsNumber: true })}
                placeholder="250000"
                className="bg-gray-700 border-gray-600 text-white"
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <Label htmlFor="description" className="text-gray-300">Description (Optional)</Label>
            <Textarea
              id="description"
              {...form.register('description')}
              placeholder="Additional property details..."
              className="bg-gray-700 border-gray-600 text-white"
              rows={3}
            />
          </div>

          {submitError && (
            <div className="bg-red-900/50 border border-red-500 rounded-lg p-3">
              <p className="text-red-200 text-sm">{submitError}</p>
            </div>
          )}

          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-wtf-gradient hover:opacity-90"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
            ) : null}
            {isLoading ? 'Saving...' : 'Save Property'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}