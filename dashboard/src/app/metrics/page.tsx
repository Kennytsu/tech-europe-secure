'use client'

import { useEffect, useState } from 'react'
import { MetricsCard } from '@/components/metrics-card'
import { ConversationsChart, RevenueChart, SentimentChart, PopularItemsChart } from '@/components/analytics-chart'
import { apiClient, Conversation, Order, Metrics, DailySummary, TranscriptResponse, TranscriptEntry } from '@/lib/api'
import { 
  MessageSquare, 
  ShoppingCart, 
  DollarSign, 
  TrendingUp, 
  Clock, 
  Users,
  Activity,
  AlertCircle,
  Star,
  BarChart3,
  PieChart,
  LineChart,
  Target,
  Zap,
  CheckCircle,
  XCircle,
  RefreshCw
} from 'lucide-react'

export default function MetricsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [orders, setOrders] = useState<Order[]>([])
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [dailyData, setDailyData] = useState<DailySummary[]>([])
  const [popularItems, setPopularItems] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        setError(null)

        // Fetch all data in parallel
        const [
          conversationsData,
          ordersData,
          metricsData,
          dailyData,
          popularItemsData
        ] = await Promise.all([
          apiClient.getConversations(100), // Get more data for metrics
          apiClient.getOrders(100),
          apiClient.getMetricsSummary(),
          apiClient.getDailyMetrics(30), // Get 30 days of data
          apiClient.getPopularItems(20) // Get more popular items
        ])

        setConversations(conversationsData.conversations || [])
        setOrders(Array.isArray(ordersData) ? ordersData : [])
        setMetrics(metricsData)
        setDailyData(dailyData.daily_summaries || [])
        setPopularItems(popularItemsData.popular_items || [])
        setLastUpdated(new Date())
      } catch (err) {
        console.error('Error fetching metrics data:', err)
        setError('Failed to load metrics data. Please check if the API server is running.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()

    // Refresh data every 3 seconds for real-time updates
    const interval = setInterval(fetchData, 3000)
    return () => clearInterval(interval)
  }, [])

  const handleRefresh = async () => {
    setIsLoading(true)
    try {
      const [
        conversationsData,
        ordersData,
        metricsData,
        dailyData,
        popularItemsData
      ] = await Promise.all([
        apiClient.getConversations(100),
        apiClient.getOrders(100),
        apiClient.getMetricsSummary(),
        apiClient.getDailyMetrics(30),
        apiClient.getPopularItems(20)
      ])

      setConversations(conversationsData.conversations || [])
      setOrders(Array.isArray(ordersData) ? ordersData : [])
      setMetrics(metricsData)
      setDailyData(dailyData.daily_summaries || [])
      setPopularItems(popularItemsData.popular_items || [])
      setLastUpdated(new Date())
    } catch (err) {
      console.error('Error refreshing data:', err)
      setError('Failed to refresh data')
    } finally {
      setIsLoading(false)
    }
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Connection Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <p className="text-sm text-gray-500">
            Make sure the API server is running on http://localhost:8000
          </p>
        </div>
      </div>
    )
  }

  // Calculate additional metrics
  const totalConversations = conversations.length
  const totalOrders = orders.length
  const successfulOrders = orders.filter(order => order.status === 'completed').length
  const cancelledOrders = orders.filter(order => order.status === 'cancelled').length
  const failedOrders = orders.filter(order => order.status === 'failed').length
  
  const successRate = totalOrders > 0 ? (successfulOrders / totalOrders) * 100 : 0
  const cancellationRate = totalOrders > 0 ? (cancelledOrders / totalOrders) * 100 : 0
  const failureRate = totalOrders > 0 ? (failedOrders / totalOrders) * 100 : 0

  const totalRevenue = orders.reduce((sum, order) => sum + (order.total_amount || 0), 0)
  const averageOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0

  const averageConversationDuration = conversations.length > 0 
    ? conversations.reduce((sum, conv) => sum + (conv.duration_seconds || 0), 0) / conversations.length 
    : 0

  const averageSentiment = conversations.length > 0
    ? conversations.reduce((sum, conv) => sum + (conv.sentiment_score || 0), 0) / conversations.length
    : 0

  const positiveSentimentCount = conversations.filter(conv => conv.sentiment === 'positive').length
  const negativeSentimentCount = conversations.filter(conv => conv.sentiment === 'negative').length
  const neutralSentimentCount = conversations.filter(conv => conv.sentiment === 'neutral').length

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Drive-Thru Analytics</h1>
              <p className="text-gray-600 mt-1">Comprehensive metrics and performance insights</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-blue-500 animate-pulse' : 'bg-green-500'}`}></div>
                  <span>{isLoading ? 'Updating...' : 'Live'}</span>
                </div>
                <span>•</span>
                <span>Last updated: {lastUpdated.toLocaleTimeString()}</span>
              </div>
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <RefreshCw className="h-8 w-8 text-blue-500 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">Loading metrics...</p>
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Key Performance Indicators */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <Target className="h-6 w-6 mr-2 text-blue-500" />
                Key Performance Indicators
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <MessageSquare className="h-8 w-8 text-blue-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Total Conversations</p>
                      <p className="text-2xl font-semibold text-gray-900">{totalConversations}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <ShoppingCart className="h-8 w-8 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Total Orders</p>
                      <p className="text-2xl font-semibold text-gray-900">{totalOrders}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <CheckCircle className="h-8 w-8 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Success Rate</p>
                      <p className="text-2xl font-semibold text-gray-900">{successRate.toFixed(1)}%</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <DollarSign className="h-8 w-8 text-yellow-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Total Revenue</p>
                      <p className="text-2xl font-semibold text-gray-900">${totalRevenue.toFixed(2)}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Order Performance Metrics */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <BarChart3 className="h-6 w-6 mr-2 text-green-500" />
                Order Performance
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <CheckCircle className="h-8 w-8 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Successful Orders</p>
                      <p className="text-2xl font-semibold text-gray-900">{successfulOrders}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <XCircle className="h-8 w-8 text-red-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Cancelled Orders</p>
                      <p className="text-2xl font-semibold text-gray-900">{cancelledOrders}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <AlertCircle className="h-8 w-8 text-red-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Failed Orders</p>
                      <p className="text-2xl font-semibold text-gray-900">{failedOrders}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <DollarSign className="h-8 w-8 text-blue-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Avg Order Value</p>
                      <p className="text-2xl font-semibold text-gray-900">${averageOrderValue.toFixed(2)}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Conversation Quality Metrics */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <PieChart className="h-6 w-6 mr-2 text-purple-500" />
                Conversation Quality
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <Clock className="h-8 w-8 text-blue-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Avg Duration</p>
                      <p className="text-2xl font-semibold text-gray-900">{Math.round(averageConversationDuration)}s</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <Star className="h-8 w-8 text-yellow-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Avg Sentiment</p>
                      <p className="text-2xl font-semibold text-gray-900">{averageSentiment.toFixed(2)}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <TrendingUp className="h-8 w-8 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Positive Sentiment</p>
                      <p className="text-2xl font-semibold text-gray-900">{positiveSentimentCount}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <TrendingUp className="h-8 w-8 text-red-500 rotate-180" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Negative Sentiment</p>
                      <p className="text-2xl font-semibold text-gray-900">{negativeSentimentCount}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <LineChart className="h-5 w-5 mr-2 text-blue-500" />
                  Conversation Trends
                </h3>
                <ConversationsChart data={dailyData} />
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <DollarSign className="h-5 w-5 mr-2 text-green-500" />
                  Revenue Trends
                </h3>
                <RevenueChart data={dailyData} />
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Activity className="h-5 w-5 mr-2 text-purple-500" />
                  Sentiment Distribution
                </h3>
                <SentimentChart data={conversations} />
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <ShoppingCart className="h-5 w-5 mr-2 text-orange-500" />
                  Popular Items
                </h3>
                <PopularItemsChart data={popularItems} />
              </div>
            </div>

            {/* Performance Summary */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Zap className="h-5 w-5 mr-2 text-yellow-500" />
                Performance Summary
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-500 mb-2">{successRate.toFixed(1)}%</div>
                  <div className="text-sm text-gray-600">Order Success Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-500 mb-2">{Math.round(averageConversationDuration)}s</div>
                  <div className="text-sm text-gray-600">Average Conversation Time</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-500 mb-2">{averageSentiment.toFixed(2)}</div>
                  <div className="text-sm text-gray-600">Average Sentiment Score</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
