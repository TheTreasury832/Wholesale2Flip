// frontend/src/app/dashboard/PropertySearch.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, Loader2, MapPin } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { usePropertyStore } from '@/stores/propertyStore';
import toast from 'react-hot-toast';

interface PropertyData {
  address: string;
  city: string;
  state: string;
  zip: string;
  county: string;
  propertyType: string;
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
  yearBuilt: number;
  listPrice: number;
  daysOnMarket: number;
  lat: number;
  lng: number;
}

export default function PropertySearch() {
  const router = useRouter();
  const [searchAddress, setSearchAddress] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const { setCurrentProperty } = usePropertyStore();

  // Auto-complete address suggestions
  const handleAddressChange = async (value: string) => {
    setSearchAddress(value);
    
    if (value.length > 3) {
      try {
        const response = await axios.get(`/api/properties/autocomplete`, {
          params: { query: value }
        });
        setSuggestions(response.data.suggestions);
      } catch (error) {
        console.error('Autocomplete error:', error);
      }
    } else {
      setSuggestions([]);
    }
  };

  // Search for property and fetch data
  const handleSearch = async () => {
    if (!searchAddress.trim()) {
      toast.error('Please enter a property address');
      return;
    }

    setIsSearching(true);
    
    try {
      // Fetch property data from multiple sources
      const response = await axios.post('/api/properties/search', {
        address: searchAddress
      });

      const propertyData: PropertyData = response.data;
      
      // Store in global state
      setCurrentProperty(propertyData);
      
      // Navigate to offer type selection
      router.push('/dashboard/offer-type');
      
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Property not found');
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5" />
        
        {/* Gradient Orbs */}
        <div className="absolute top-20 left-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-green-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      {/* House Image with Neon Outline */}
      <div className="absolute inset-0 flex items-center justify-center opacity-30">
        <div className="relative">
          <img 
            src="/house-outline.png" 
            alt="House" 
            className="w-[600px] h-[400px] object-contain"
          />
          {/* Neon effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-green-400 via-yellow-400 to-green-400 blur-xl opacity-50 animate-pulse" />
        </div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-3xl"
        >
          {/* Title */}
          <h1 className="text-6xl font-bold text-center text-white mb-4">
            Pop In Your Address
          </h1>
          <p className="text-xl text-center text-gray-400 mb-12">
            Let's find you a buyer
          </p>

          {/* Search Box */}
          <div className="relative">
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-3 shadow-2xl">
              <div className="flex items-center gap-4">
                <MapPin className="w-6 h-6 text-purple-400 ml-4" />
                <input
                  type="text"
                  value={searchAddress}
                  onChange={(e) => handleAddressChange(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  placeholder="Enter address..."
                  className="flex-1 bg-transparent text-white text-lg placeholder-gray-400 py-4 outline-none"
                />
                <button
                  onClick={handleSearch}
                  disabled={isSearching}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-200 flex items-center gap-2"
                >
                  {isSearching ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Searching...
                    </>
                  ) : (
                    <>
                      <Search className="w-5 h-5" />
                      Find Buyers
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Address Suggestions */}
            <AnimatePresence>
              {suggestions.length > 0 && (
                <motion.div 
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="absolute top-full left-0 right-0 mt-2 bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl overflow-hidden shadow-2xl"
                >
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setSearchAddress(suggestion);
                        setSuggestions([]);
                      }}
                      className="w-full px-6 py-3 text-left text-white hover:bg-white/10 transition-colors flex items-center gap-3"
                    >
                      <MapPin className="w-4 h-4 text-gray-400" />
                      {suggestion}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-3 gap-6 mt-16">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="text-4xl font-bold text-green-400">2,847</div>
              <div className="text-gray-400 mt-2">Active Buyers</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-center"
            >
              <div className="text-4xl font-bold text-purple-400">14 min</div>
              <div className="text-gray-400 mt-2">Avg Match Time</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-center"
            >
              <div className="text-4xl font-bold text-blue-400">$23.5k</div>
              <div className="text-gray-400 mt-2">Avg Profit</div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

// frontend/src/app/dashboard/offer-type/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { DollarSign, FileText, TrendingUp, Home } from 'lucide-react';
import { usePropertyStore } from '@/stores/propertyStore';

const offerTypes = [
  {
    id: 'cash',
    title: 'Cash',
    subtitle: 'Fix & Flip or Section 8',
    icon: DollarSign,
    color: 'from-green-500 to-emerald-600',
    description: 'Best for properties needing repairs or Section 8 rentals'
  },
  {
    id: 'creative',
    title: 'Creative',
    subtitle: 'Seller Finance or Subject To',
    icon: FileText,
    color: 'from-purple-500 to-blue-600',
    description: 'Best for properties with existing mortgages or motivated sellers'
  }
];

export default function OfferTypePage() {
  const router = useRouter();
  const { currentProperty, setOfferType } = usePropertyStore();
  const [selectedType, setSelectedType] = useState<string | null>(null);

  const handleSelection = (type: string) => {
    setSelectedType(type);
    setOfferType(type);
    
    // Navigate to property details confirmation
    setTimeout(() => {
      router.push('/dashboard/property-details');
    }, 300);
  };

  if (!currentProperty) {
    router.push('/dashboard');
    return null;
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] py-20">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto"
        >
          {/* Property Summary */}
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl p-6 mb-12">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center">
                <Home className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-white">{currentProperty.address}</h2>
                <p className="text-gray-400">{currentProperty.city}, {currentProperty.state} {currentProperty.zip}</p>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-400">Type:</span>
                <span className="text-white ml-2">{currentProperty.propertyType}</span>
              </div>
              <div>
                <span className="text-gray-400">Beds:</span>
                <span className="text-white ml-2">{currentProperty.bedrooms}</span>
              </div>
              <div>
                <span className="text-gray-400">Baths:</span>
                <span className="text-white ml-2">{currentProperty.bathrooms}</span>
              </div>
              <div>
                <span className="text-gray-400">Sqft:</span>
                <span className="text-white ml-2">{currentProperty.squareFeet.toLocaleString()}</span>
              </div>
            </div>
          </div>

          {/* Offer Type Selection */}
          <h1 className="text-4xl font-bold text-white text-center mb-4">
            Select Offer Type
          </h1>
          <p className="text-gray-400 text-center mb-12">
            Choose the best strategy for this property
          </p>

          <div className="grid md:grid-cols-2 gap-8">
            {offerTypes.map((type) => {
              const Icon = type.icon;
              return (
                <motion.button
                  key={type.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleSelection(type.id)}
                  className={`relative overflow-hidden bg-[#1a1a1a] border-2 rounded-2xl p-8 text-left transition-all duration-300 ${
                    selectedType === type.id 
                      ? 'border-green-500 shadow-[0_0_30px_rgba(16,185,129,0.3)]' 
                      : 'border-[#2a2a2a] hover:border-[#3a3a3a]'
                  }`}
                >
                  {/* Background Gradient */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${type.color} opacity-10`} />
                  
                  {/* Content */}
                  <div className="relative z-10">
                    <div className={`w-16 h-16 bg-gradient-to-br ${type.color} rounded-2xl flex items-center justify-center mb-6`}>
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-white mb-2">{type.title}</h3>
                    <p className="text-lg text-gray-300 mb-4">{type.subtitle}</p>
                    <p className="text-sm text-gray-400">{type.description}</p>
                  </div>

                  {/* Selection Indicator */}
                  {selectedType === type.id && (
                    <motion.div 
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="absolute top-4 right-4 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center"
                    >
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </motion.div>
                  )}
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      </div>
    </div>
  );
}