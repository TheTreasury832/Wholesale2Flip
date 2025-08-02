// frontend/src/app/buyboxes/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Map, List, Home, DollarSign, Building2 } from 'lucide-react';
import axios from 'axios';

const buyerCategories = [
  { id: 'fix-flip', label: 'Fix & Flip Buyers', icon: Home, color: 'purple' },
  { id: 'creative', label: 'Creative Buyers', icon: DollarSign, color: 'blue' },
  { id: 'section8', label: 'Section 8 Buyers', icon: Building2, color: 'green' }
];

const states = [
  'ALABAMA', 'ARIZONA', 'COLORADO', 'DELAWARE', 'FLORIDA', 
  'GEORGIA', 'IDAHO', 'INDIANA', 'KANSAS', 'KENTUCKY',
  'LOUISIANA', 'MARYLAND', 'MICHIGAN', 'MISSISSIPPI', 'MISSOURI',
  'NEBRASKA', 'NEVADA', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',
  'NORTH CAROLINA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA',
  'SOUTH CAROLINA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VIRGINIA',
  'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN'
];

interface BuyerData {
  state: string;
  fixFlipCount: number;
  creativeCount: number;
  section8Count: number;
}

export default function BuyBoxesPage() {
  const [viewMode, setViewMode] = useState<'map' | 'list'>('list');
  const [selectedCategory, setSelectedCategory] = useState('fix-flip');
  const [buyerData, setBuyerData] = useState<BuyerData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBuyerData();
  }, []);

  const fetchBuyerData = async () => {
    try {
      const response = await axios.get('/api/buyers/by-state');
      setBuyerData(response.data);
    } catch (error) {
      console.error('Error fetching buyer data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'fix-flip': return 'from-purple-500 to-purple-600';
      case 'creative': return 'from-blue-500 to-blue-600';
      case 'section8': return 'from-green-500 to-green-600';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a]">
      {/* Header */}
      <div className="bg-[#1a1a1a] border-b border-[#2a2a2a]">
        <div className="container mx-auto px-6 py-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-white">Buyer Network</h1>
            <div className="flex gap-2 bg-[#0a0a0a] p-1 rounded-lg">
              <button
                onClick={() => setViewMode('map')}
                className={`px-4 py-2 rounded-md flex items-center gap-2 transition-all ${
                  viewMode === 'map' 
                    ? 'bg-purple-600 text-white' 
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <Map className="w-4 h-4" /> Map View
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-4 py-2 rounded-md flex items-center gap-2 transition-all ${
                  viewMode === 'list' 
                    ? 'bg-purple-600 text-white' 
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <List className="w-4 h-4" /> List View
              </button>
            </div>
          </div>

          {/* Category Tabs */}
          <div className="flex gap-2">
            {buyerCategories.map((category) => {
              const Icon = category.icon;
              return (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                    selectedCategory === category.id
                      ? `bg-gradient-to-r ${getCategoryColor(category.id)} text-white`
                      : 'bg-[#0a0a0a] text-gray-400 hover:text-white border border-[#2a2a2a]'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {category.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-8">
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
          </div>
        ) : viewMode === 'list' ? (
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl overflow-hidden">
            {states.map((state, index) => (
              <motion.div
                key={state}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.02 }}
                className="border-b border-[#2a2a2a] last:border-b-0 hover:bg-white/5 transition-colors"
              >
                <div className="px-8 py-6 flex justify-between items-center">
                  <h3 className="text-xl font-semibold text-white">{state}</h3>
                  <div className="flex gap-8">
                    {selectedCategory === 'fix-flip' && (
                      <span className="text-purple-400 font-semibold">
                        {Math.floor(Math.random() * 50 + 10)} buyers
                      </span>
                    )}
                    {selectedCategory === 'creative' && (
                      <span className="text-blue-400 font-semibold">
                        {Math.floor(Math.random() * 30 + 5)} buyers
                      </span>
                    )}
                    {selectedCategory === 'section8' && (
                      <span className="text-green-400 font-semibold">
                        {Math.floor(Math.random() * 20 + 3)} buyers
                      </span>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl p-8">
            <div className="text-center text-gray-400">
              <Map className="w-24 h-24 mx-auto mb-4 opacity-20" />
              <p>Interactive map view coming soon</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// frontend/src/app/dashboard/contract-generator/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Calendar, DollarSign, FileText, User, Home, CheckCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface ContractFormData {
  purchasePrice: number;
  earnestMoney: number;
  closingDate: string;
  closingPeriod: 'specific' | 'days';
  closingDays: number;
  inspectionPeriod: number;
  closingCosts: 'buyer' | 'seller' | 'split';
  hasLiens: boolean;
  lienDetails: string;
  hasBalloon: boolean;
  balloonYears: number;
  hasAgent: boolean;
  agentName: string;
  agentCommission: number;
  agentEmail: string;
  sellerName: string;
  sellerAddress: string;
}

const steps = [
  { id: 1, title: 'Purchase Terms', icon: DollarSign },
  { id: 2, title: 'Closing Details', icon: Calendar },
  { id: 3, title: 'Property Info', icon: Home },
  { id: 4, title: 'Parties', icon: User },
  { id: 5, title: 'Review', icon: CheckCircle }
];

export default function ContractGeneratorPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<ContractFormData>({
    purchasePrice: 0,
    earnestMoney: 1000,
    closingDate: '',
    closingPeriod: 'days',
    closingDays: 30,
    inspectionPeriod: 10,
    closingCosts: 'buyer',
    hasLiens: false,
    lienDetails: '',
    hasBalloon: false,
    balloonYears: 0,
    hasAgent: false,
    agentName: '',
    agentCommission: 3,
    agentEmail: '',
    sellerName: '',
    sellerAddress: ''
  });

  const updateFormData = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('/api/contracts/generate', formData);
      
      toast.success('Contract generated and sent to TC!');
      
      // Navigate to success page
      router.push('/dashboard/contract-success');
    } catch (error) {
      toast.error('Error generating contract. Please try again.');
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Purchase Price
              </label>
              <div className="relative">
                <DollarSign className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="number"
                  value={formData.purchasePrice}
                  onChange={(e) => updateFormData('purchasePrice', Number(e.target.value))}
                  className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg pl-12 pr-4 py-4 text-white focus:border-purple-500 outline-none"
                  placeholder="Enter purchase price"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Earnest Money Deposit
              </label>
              <div className="relative">
                <DollarSign className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="number"
                  value={formData.earnestMoney}
                  onChange={(e) => updateFormData('earnestMoney', Number(e.target.value))}
                  className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg pl-12 pr-4 py-4 text-white focus:border-purple-500 outline-none"
                  placeholder="Enter EMD amount"
                />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Closing Period
              </label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => updateFormData('closingPeriod', 'specific')}
                  className={`p-4 rounded-lg border transition-all ${
                    formData.closingPeriod === 'specific'
                      ? 'bg-purple-600 border-purple-600 text-white'
                      : 'bg-[#0a0a0a] border-[#2a2a2a] text-gray-400'
                  }`}
                >
                  Specific Date
                </button>
                <button
                  onClick={() => updateFormData('closingPeriod', 'days')}
                  className={`p-4 rounded-lg border transition-all ${
                    formData.closingPeriod === 'days'
                      ? 'bg-purple-600 border-purple-600 text-white'
                      : 'bg-[#0a0a0a] border-[#2a2a2a] text-gray-400'
                  }`}
                >
                  Days from Contract
                </button>
              </div>
            </div>

            {formData.closingPeriod === 'specific' ? (
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Closing Date
                </label>
                <input
                  type="date"
                  value={formData.closingDate}
                  onChange={(e) => updateFormData('closingDate', e.target.value)}
                  className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                />
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Days to Closing
                </label>
                <input
                  type="number"
                  value={formData.closingDays}
                  onChange={(e) => updateFormData('closingDays', Number(e.target.value))}
                  className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                  placeholder="30"
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Inspection Period (Business Days)
              </label>
              <input
                type="number"
                value={formData.inspectionPeriod}
                onChange={(e) => updateFormData('inspectionPeriod', Number(e.target.value))}
                className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                placeholder="10"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Closing Costs Paid By
              </label>
              <div className="grid grid-cols-3 gap-4">
                {['buyer', 'seller', 'split'].map((option) => (
                  <button
                    key={option}
                    onClick={() => updateFormData('closingCosts', option)}
                    className={`p-4 rounded-lg border transition-all capitalize ${
                      formData.closingCosts === option
                        ? 'bg-purple-600 border-purple-600 text-white'
                        : 'bg-[#0a0a0a] border-[#2a2a2a] text-gray-400'
                    }`}
                  >
                    {option === 'split' ? 'Split 50/50' : option}
                  </button>
                ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div>
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={formData.hasLiens}
                  onChange={(e) => updateFormData('hasLiens', e.target.checked)}
                  className="w-5 h-5 bg-[#0a0a0a] border-[#2a2a2a] rounded text-purple-600"
                />
                <span className="text-white">Property has liens (Solar, HOA, etc.)</span>
              </label>
              
              {formData.hasLiens && (
                <textarea
                  value={formData.lienDetails}
                  onChange={(e) => updateFormData('lienDetails', e.target.value)}
                  className="w-full mt-4 bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                  placeholder="Describe the liens..."
                  rows={3}
                />
              )}
            </div>

            <div>
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={formData.hasBalloon}
                  onChange={(e) => updateFormData('hasBalloon', e.target.checked)}
                  className="w-5 h-5 bg-[#0a0a0a] border-[#2a2a2a] rounded text-purple-600"
                />
                <span className="text-white">Include balloon payment</span>
              </label>
              
              {formData.hasBalloon && (
                <input
                  type="number"
                  value={formData.balloonYears}
                  onChange={(e) => updateFormData('balloonYears', Number(e.target.value))}
                  className="w-full mt-4 bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                  placeholder="Years until balloon payment"
                />
              )}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Seller Name(s)
              </label>
              <input
                type="text"
                value={formData.sellerName}
                onChange={(e) => updateFormData('sellerName', e.target.value)}
                className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                placeholder="John and Jane Doe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Seller Mailing Address
              </label>
              <textarea
                value={formData.sellerAddress}
                onChange={(e) => updateFormData('sellerAddress', e.target.value)}
                className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                placeholder="123 Main St, City, State ZIP"
                rows={2}
              />
            </div>

            <div>
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={formData.hasAgent}
                  onChange={(e) => updateFormData('hasAgent', e.target.checked)}
                  className="w-5 h-5 bg-[#0a0a0a] border-[#2a2a2a] rounded text-purple-600"
                />
                <span className="text-white">Real estate agent involved</span>
              </label>
              
              {formData.hasAgent && (
                <div className="mt-4 space-y-4">
                  <input
                    type="text"
                    value={formData.agentName}
                    onChange={(e) => updateFormData('agentName', e.target.value)}
                    className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                    placeholder="Agent name"
                  />
                  <input
                    type="email"
                    value={formData.agentEmail}
                    onChange={(e) => updateFormData('agentEmail', e.target.value)}
                    className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                    placeholder="Agent email"
                  />
                  <input
                    type="number"
                    value={formData.agentCommission}
                    onChange={(e) => updateFormData('agentCommission', Number(e.target.value))}
                    className="w-full bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg px-4 py-4 text-white focus:border-purple-500 outline-none"
                    placeholder="Commission %"
                  />
                </div>
              )}
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-white mb-6">Review Contract Details</h3>
            
            <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded-lg p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-gray-400">Purchase Price:</span>
                  <p className="text-white font-semibold">${formData.purchasePrice.toLocaleString()}</p>
                </div>
                <div>
                  <span className="text-gray-400">EMD:</span>
                  <p className="text-white font-semibold">${formData.earnestMoney.toLocaleString()}</p>
                </div>
                <div>
                  <span className="text-gray-400">Closing:</span>
                  <p className="text-white font-semibold">
                    {formData.closingPeriod === 'specific' 
                      ? formData.closingDate 
                      : `${formData.closingDays} days`}
                  </p>
                </div>
                <div>
                  <span className="text-gray-400">Inspection Period:</span>
                  <p className="text-white font-semibold">{formData.inspectionPeriod} days</p>
                </div>
              </div>
              
              <div className="pt-4 border-t border-[#2a2a2a]">
                <span className="text-gray-400">Seller:</span>
                <p className="text-white font-semibold">{formData.sellerName}</p>
                <p className="text-gray-300 text-sm">{formData.sellerAddress}</p>
              </div>
              
              {formData.hasAgent && (
                <div className="pt-4 border-t border-[#2a2a2a]">
                  <span className="text-gray-400">Agent:</span>
                  <p className="text-white font-semibold">{formData.agentName}</p>
                  <p className="text-gray-300 text-sm">{formData.agentCommission}% commission</p>
                </div>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] py-12">
      <div className="container mx-auto px-6 max-w-3xl">
        {/* Progress Steps */}
        <div className="flex justify-between mb-12">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={step.id} className="flex items-center">
                <div className="flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
                      currentStep >= step.id
                        ? 'bg-purple-600 text-white'
                        : 'bg-[#1a1a1a] text-gray-400'
                    }`}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <span className="text-xs text-gray-400 mt-2">{step.title}</span>
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`w-full h-1 mx-2 transition-all ${
                      currentStep > step.id ? 'bg-purple-600' : 'bg-[#2a2a2a]'
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>

        {/* Form Content */}
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl p-8"
        >
          <h2 className="text-2xl font-bold text-white mb-6">
            {steps[currentStep - 1].title}
          </h2>
          
          {renderStepContent()}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8">
            <button
              onClick={handlePrevious}
              disabled={currentStep === 1}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                currentStep === 1
                  ? 'bg-[#0a0a0a] text-gray-600 cursor-not-allowed'
                  : 'bg-[#0a0a0a] text-white hover:bg-[#2a2a2a]'
              }`}
            >
              Previous
            </button>
            
            {currentStep === steps.length ? (
              <button
                onClick={handleSubmit}
                className="px-8 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-semibold hover:from-green-600 hover:to-green-700 transition-all"
              >
                Submit to TC for Signatures
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all"
              >
                Next
              </button>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}