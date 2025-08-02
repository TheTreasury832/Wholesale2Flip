// src/app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from '@/components/providers'
import { Toaster } from 'react-hot-toast'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Wholesale2Flip (WTF) - Advanced Real Estate Wholesaling Platform',
  description: 'The most powerful real estate wholesaling platform with AI-powered lead generation, buyer matching, and contract automation.',
  keywords: 'real estate, wholesaling, investment, property, buyers, leads, contracts',
  authors: [{ name: 'WTF Team' }],
  creator: 'WTF Team',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://wholesale2flip.com',
    title: 'Wholesale2Flip (WTF) - Advanced Real Estate Wholesaling Platform',
    description: 'The most powerful real estate wholesaling platform with AI-powered lead generation, buyer matching, and contract automation.',
    siteName: 'Wholesale2Flip',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Wholesale2Flip Platform'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Wholesale2Flip (WTF) - Advanced Real Estate Wholesaling Platform',
    description: 'The most powerful real estate wholesaling platform with AI-powered lead generation, buyer matching, and contract automation.',
    images: ['/og-image.png']
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1
    }
  }
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#1F2937',
                color: '#F9FAFB',
                border: '1px solid #374151'
              },
              success: {
                iconTheme: {
                  primary: '#10B981',
                  secondary: '#F9FAFB'
                }
              },
              error: {
                iconTheme: {
                  primary: '#EF4444',
                  secondary: '#F9FAFB'
                }
              }
            }}
          />
        </Providers>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}

// src/app/globals.css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 262.1 83.3% 57.8%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 262.1 83.3% 57.8%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 262.1 83.3% 57.8%;
    --primary-foreground: 210 40% 98%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 262.1 83.3% 57.8%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

@layer utilities {
  .gradient-text {
    @apply bg-gradient-to-r from-wtf-purple to-wtf-green bg-clip-text text-transparent;
  }
  
  .glass-effect {
    @apply backdrop-blur-sm bg-white/10 border border-white/20;
  }
  
  .neon-glow {
    box-shadow: 0 0 5px theme('colors.wtf.purple'), 0 0 10px theme('colors.wtf.purple'), 0 0 15px theme('colors.wtf.purple');
  }
  
  .hover-lift {
    @apply transition-transform duration-200 hover:-translate-y-1;
  }
}

// src/app/page.tsx
import { Hero } from '@/components/marketing/Hero'
import { Features } from '@/components/marketing/Features'
import { Testimonials } from '@/components/marketing/Testimonials'
import { Pricing } from '@/components/marketing/Pricing'
import { CallToAction } from '@/components/marketing/CallToAction'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Header />
      <main>
        <Hero />
        <Features />
        <Testimonials />
        <Pricing />
        <CallToAction />
      </main>
      <Footer />
    </div>
  )
}

// src/components/providers.tsx
'use client'

import { SessionProvider } from 'next-auth/react'
import { ThemeProvider } from 'next-themes'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () => new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 60 * 1000, // 1 minute
          refetchOnWindowFocus: false
        }
      }
    })
  )

  return (
    <SessionProvider>
      <ThemeProvider
        attribute="class"
        defaultTheme="dark"
        enableSystem
        disableTransitionOnChange
      >
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      </ThemeProvider>
    </SessionProvider>
  )
}

// src/components/layout/Header.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useSession, signOut } from 'next-auth/react'
import { Menu, X, Zap, User, Settings, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { data: session, status } = useSession()

  const navigation = [
    { name: 'Features', href: '#features' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'About', href: '/about' },
    { name: 'Support', href: '/support' }
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-wtf-gradient rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold gradient-text">WTF</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-gray-300 hover:text-white transition-colors duration-200"
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Auth Section */}
          <div className="hidden md:flex items-center space-x-4">
            {status === 'loading' ? (
              <div className="w-8 h-8 bg-gray-700 rounded-full animate-pulse" />
            ) : session ? (
              <div className="flex items-center space-x-4">
                <Button asChild variant="outline">
                  <Link href="/dashboard">Dashboard</Link>
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src={session.user?.image || ''} alt={session.user?.name || ''} />
                        <AvatarFallback>
                          {session.user?.name?.charAt(0) || session.user?.email?.charAt(0) || 'U'}
                        </AvatarFallback>
                      </Avatar>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-56" align="end">
                    <div className="flex items-center justify-start gap-2 p-2">
                      <div className="flex flex-col space-y-1 leading-none">
                        {session.user?.name && (
                          <p className="font-medium">{session.user.name}</p>
                        )}
                        {session.user?.email && (
                          <p className="w-[200px] truncate text-sm text-muted-foreground">
                            {session.user.email}
                          </p>
                        )}
                      </div>
                    </div>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem asChild>
                      <Link href="/dashboard" className="cursor-pointer">
                        <User className="mr-2 h-4 w-4" />
                        Dashboard
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem asChild>
                      <Link href="/dashboard/profile" className="cursor-pointer">
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
            ) : (
              <div className="flex items-center space-x-4">
                <Button asChild variant="ghost">
                  <Link href="/auth/signin">Sign In</Link>
                </Button>
                <Button asChild className="bg-wtf-gradient hover:opacity-90">
                  <Link href="/auth/signup">Get Started</Link>
                </Button>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-800 rounded-lg mt-2">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="block px-3 py-2 text-gray-300 hover:text-white transition-colors duration-200"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              <div className="border-t border-gray-700 pt-2 mt-2">
                {session ? (
                  <div className="space-y-2">
                    <Link
                      href="/dashboard"
                      className="block px-3 py-2 text-gray-300 hover:text-white transition-colors duration-200"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Dashboard
                    </Link>
                    <button
                      onClick={() => {
                        signOut({ callbackUrl: '/' })
                        setIsMenuOpen(false)
                      }}
                      className="block w-full text-left px-3 py-2 text-gray-300 hover:text-white transition-colors duration-200"
                    >
                      Sign Out
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Link
                      href="/auth/signin"
                      className="block px-3 py-2 text-gray-300 hover:text-white transition-colors duration-200"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Sign In
                    </Link>
                    <Link
                      href="/auth/signup"
                      className="block px-3 py-2 text-wtf-purple hover:text-wtf-purple-light transition-colors duration-200"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Get Started
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

// src/components/marketing/Hero.tsx
'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Play, Zap, TrendingUp, Users, DollarSign } from 'lucide-react'
import { motion } from 'framer-motion'

export function Hero() {
  const [typedText, setTypedText] = useState('')
  const fullText = "Wholesaling on Steroids"
  
  useEffect(() => {
    let i = 0
    const timer = setInterval(() => {
      if (i < fullText.length) {
        setTypedText(fullText.slice(0, i + 1))
        i++
      } else {
        clearInterval(timer)
      }
    }, 100)
    
    return () => clearInterval(timer)
  }, [])

  const stats = [
    { icon: DollarSign, value: "$2.5M+", label: "Deals Closed" },
    { icon: Users, value: "10K+", label: "Active Buyers" },
    { icon: TrendingUp, value: "98%", label: "Success Rate" },
    { icon: Zap, value: "24/7", label: "AI Powered" }
  ]

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-hero-pattern opacity-10" />
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-wtf-purple/20 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-wtf-green/20 rounded-full blur-3xl animate-pulse delay-1000" />
      
      <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 pt-20">
        <div className="text-center">
          {/* Hero Text */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-6"
          >
            <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight">
              <span className="gradient-text">{typedText}</span>
              <span className="animate-pulse">|</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              The most advanced real estate wholesaling platform with 
              <span className="text-wtf-green font-semibold"> AI-powered matching</span>, 
              <span className="text-wtf-purple font-semibold"> instant buyer connections</span>, and 
              <span className="text-wtf-blue font-semibold"> automated contract generation</span>.
            </p>
          </motion.div>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-10"
          >
            <Button
              asChild
              size="lg"
              className="bg-wtf-gradient hover:opacity-90 text-white font-semibold px-8 py-4 text-lg rounded-full shadow-2xl hover-lift group"
            >
              <Link href="/auth/signup">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </Button>
            
            <Button
              variant="outline"
              size="lg"
              className="border-wtf-purple text-wtf-purple hover:bg-wtf-purple/10 px-8 py-4 text-lg rounded-full group"
            >
              <Play className="mr-2 h-5 w-5" />
              Watch Demo
            </Button>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 max-w-4xl mx-auto"
          >
            {stats.map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="flex justify-center mb-3">
                  <div className="w-12 h-12 bg-wtf-gradient rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                    <stat.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <div className="text-2xl md:text-3xl font-bold text-white mb-1">
                  {stat.value}
                </div>
                <div className="text-gray-400 text-sm">
                  {stat.label}
                </div>
              </div>
            ))}
          </motion.div>

          {/* Address Search Preview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="mt-16 max-w-2xl mx-auto"
          >
            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-8 shadow-2xl">
              <h3 className="text-2xl font-semibold text-white mb-4">
                Find Buyers Instantly
              </h3>
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Enter property address..."
                    className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-wtf-purple focus:border-transparent"
                  />
                </div>
                <Button className="bg-wtf-gradient hover:opacity-90 px-6 py-3 rounded-lg font-semibold">
                  Find Buyers
                </Button>
              </div>
              <p className="text-gray-400 text-sm mt-3 text-center">
                Get matched with verified cash buyers in seconds
              </p>
            </div>
          </motion.div>
        </div>
      </div>
      
      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
      >
        <div className="w-6 h-10 border-2 border-gray-400 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-gray-400 rounded-full mt-2 animate-bounce" />
        </div>
      </motion.div>
    </section>
  )
}

// src/components/marketing/Features.tsx
'use client'

import { motion } from 'framer-motion'
import { 
  Zap, 
  Users, 
  FileText, 
  TrendingUp, 
  Brain, 
  MessageSquare,
  Search,
  DollarSign,
  Clock,
  Shield,
  Smartphone,
  Globe
} from 'lucide-react'

export function Features() {
  const features = [
    {
      icon: Search,
      title: "Instant Property Analysis",
      description: "Get ARV, rehab costs, and profit potential in seconds with our AI-powered property analyzer.",
      color: "text-wtf-purple"
    },
    {
      icon: Users,
      title: "Smart Buyer Matching",
      description: "Connect with verified cash buyers whose criteria perfectly match your deals.",
      color: "text-wtf-green"
    },
    {
      icon: FileText,
      title: "Auto Contract Generation",
      description: "Generate professional contracts with e-signature capabilities in minutes, not hours.",
      color: "text-wtf-blue"
    },
    {
      icon: Brain,
      title: "AI-Powered Insights",
      description: "ScriptMaster AI and Multifamily Underwriter GPT provide expert guidance for every deal.",
      color: "text-wtf-orange"
    },
    {
      icon: TrendingUp,
      title: "Lightning Leads",
      description: "Access premium motivated seller leads with 98% accuracy and instant notifications.",
      color: "text-wtf-purple"
    },
    {
      icon: MessageSquare,
      title: "Discord Integration",
      description: "Get deal alerts, training updates, and community support directly in Discord.",
      color: "text-wtf-green"
    },
    {
      icon: DollarSign,
      title: "Profit Tracking",
      description: "Track your deals, revenue, and ROI with comprehensive analytics and reporting.",
      color: "text-wtf-blue"
    },
    {
      icon: Clock,
      title: "24/7 Automation",
      description: "Automated follow-ups, lead scoring, and buyer notifications work around the clock.",
      color: "text-wtf-orange"
    },
    {
      icon: Shield,
      title: "Verified Buyers Only",
      description: "All buyers are proof-of-funds verified to ensure serious, qualified investors.",
      color: "text-wtf-purple"
    },
    {
      icon: Smartphone,
      title: "Mobile Optimized",
      description: "Access all features on any device with our responsive PWA design.",
      color: "text-wtf-green"
    },
    {
      icon: Globe,
      title: "Nationwide Coverage",
      description: "Active buyer network and market data covering all 50 states.",
      color: "text-wtf-blue"
    },
    {
      icon: Zap,
      title: "One-Click Disposition",
      description: "Send deals to matched buyers with one click and track engagement in real-time.",
      color: "text-wtf-orange"
    }
  ]

  return (
    <section id="features" className="py-20 bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Why Choose <span className="gradient-text">WTF</span>?
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Everything you need to dominate real estate wholesaling in one powerful platform.
            Built by wholesalers, for wholesalers.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6 hover:border-wtf-purple/50 transition-all duration-300 hover-lift group"
            >
              <div className="flex items-center mb-4">
                <div className={`w-12 h-12 rounded-lg bg-gray-700 flex items-center justify-center group-hover:scale-110 transition-transform ${feature.color}`}>
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold text-white ml-4">
                  {feature.title}
                </h3>
              </div>
              <p className="text-gray-300 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Feature Highlight */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-20 bg-wtf-gradient rounded-2xl p-8 md:p-12 text-center"
        >
          <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
            The Treasury Vault Integration
          </h3>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Access Mike K's proven scripts, objection handlers, and training materials 
            directly in the platform with AI-powered guidance for every conversation.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <div className="bg-white/20 rounded-lg px-6 py-3">
              <span className="text-white font-semibold">Cold Calling Scripts</span>
            </div>
            <div className="bg-white/20 rounded-lg px-6 py-3">
              <span className="text-white font-semibold">Objection Handling</span>
            </div>
            <div className="bg-white/20 rounded-lg px-6 py-3">
              <span className="text-white font-semibold">Follow-up Sequences</span>
            </div>
            <div className="bg-white/20 rounded-lg px-6 py-3">
              <span className="text-white font-semibold">AI Coaching</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}