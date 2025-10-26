'use client'

import { useEffect, useState } from 'react'
import { MetricsCard } from '@/components/metrics-card'
import { OrdersTable } from '@/components/orders-table'
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
  Eye,
  Star,
  RefreshCw
} from 'lucide-react'

// McDonald's menu item mapping
const getMcDonaldsItemName = (itemId: string, itemName: string) => {
  const menuItems: { [key: string]: string } = {
    'combo_big_mac': 'Combo Big Mac',
    'big_mac': 'Big Mac',
    'quarter_pounder': 'Quarter Pounder',
    'mcdouble': 'McDouble',
    'cheeseburger': 'Cheeseburger',
    'hamburger': 'Hamburger',
    'filet_o_fish': 'Filet-O-Fish',
    'french_fries': 'French Fries',
    'nuggets': 'Chicken McNuggets',
    'mcnuggets': 'Chicken McNuggets',
    'coca_cola': 'Coca-Cola',
    'sprite': 'Sprite',
    'fanta': 'Fanta',
    'coffee': 'McCafé Coffee',
    'apple_pie': 'Apple Pie',
    'mcflurry': 'McFlurry',
    'sundae': 'Hot Fudge Sundae',
    'salad': 'Garden Salad',
    'wrap': 'Chicken Wrap',
    'muffin': 'English Muffin',
    'hash_browns': 'Hash Browns',
    'pancakes': 'Hotcakes'
  }
  
  return menuItems[itemId] || itemName || 'Menu Item'
}


export default function Dashboard() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [orders, setOrders] = useState<Order[]>([])
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [dailyData, setDailyData] = useState<DailySummary[]>([])
  const [popularItems, setPopularItems] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null)
  const [showOrderDetails, setShowOrderDetails] = useState(false)
  const [activeTab, setActiveTab] = useState<'order' | 'conversation'>('order')
  const [transcriptData, setTranscriptData] = useState<TranscriptEntry[]>([])
  const [loadingTranscript, setLoadingTranscript] = useState(false)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

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
          apiClient.getConversations(10),
          apiClient.getOrders(10),
          apiClient.getMetricsSummary(),
          apiClient.getDailyMetrics(7),
          apiClient.getPopularItems(5)
        ])

        setConversations(conversationsData.conversations || [])
        setOrders(Array.isArray(ordersData) ? ordersData : [])
        setMetrics(metricsData)
        setDailyData(dailyData.daily_summaries || [])
        setPopularItems(popularItemsData.popular_items || [])
        setLastUpdated(new Date())
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        setError('Failed to load dashboard data. Please check if the API server is running.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()

    // Refresh data every 3 seconds for real-time updates
    const interval = setInterval(fetchData, 3000)
    return () => clearInterval(interval)
  }, [])

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

  const handleOrderClick = (order: Order) => {
    setSelectedOrder(order)
    setShowOrderDetails(true)
    setActiveTab('order')
  }

  const closeOrderDetails = () => {
    setShowOrderDetails(false)
    setSelectedOrder(null)
    setActiveTab('order')
    setTranscriptData([]) // Clear transcript data on close
  }

  const fetchTranscript = async (conversationId: string) => {
    try {
      setLoadingTranscript(true)
      const response = await apiClient.getConversationTranscript(conversationId)
      setTranscriptData(response.transcript || [])
    } catch (error) {
      console.error('Failed to fetch transcript:', error)
      setTranscriptData([])
    } finally {
      setLoadingTranscript(false)
    }
  }

  const handleConversationTabClick = () => {
    setActiveTab('conversation')
    if (selectedOrder && transcriptData.length === 0) { // Only fetch if not already fetched
      fetchTranscript(selectedOrder.conversation_id)
    }
  }

  const handleRefresh = async () => {
    setIsLoading(true)
    try {
      setError(null)

      // Fetch all data in parallel
      const [
        conversationsData,
        ordersData,
        metricsData,
        dailyData,
        popularItemsData
      ] = await Promise.all([
        apiClient.getConversations(10),
        apiClient.getOrders(10),
        apiClient.getMetricsSummary(),
        apiClient.getDailyMetrics(7),
        apiClient.getPopularItems(5)
      ])

      setConversations(conversationsData.conversations || [])
      setOrders(Array.isArray(ordersData) ? ordersData : [])
      setMetrics(metricsData)
      setDailyData(dailyData.daily_summaries || [])
      setPopularItems(popularItemsData.popular_items || [])
      setLastUpdated(new Date())
    } catch (err) {
      console.error('Error refreshing dashboard data:', err)
      setError('Failed to refresh dashboard data')
    } finally {
      setIsLoading(false)
    }
  }



  return (
    <div className="min-h-screen bg-gray-50">
      {/* Dashboard Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard Overview</h1>
              <p className="text-gray-600 mt-1">Real-time monitoring and insights for McDonald's drive-thru operations</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-blue-500 animate-pulse' : 'bg-green-500'}`}></div>
                  <span>{isLoading ? 'Updating...' : 'Live'}</span>
                </div>
                <span>•</span>
                <span>Last updated: {isClient ? lastUpdated.toLocaleTimeString() : '--:--:--'}</span>
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
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-red-500">
            <div className="flex items-center">
              <ShoppingCart className="h-8 w-8 text-red-500 mr-3" />
              <div>
                <div className="text-2xl font-bold text-gray-900">{orders.length}</div>
                <div className="text-sm text-gray-600">Active Orders</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-green-500">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-green-500 mr-3" />
              <div>
                <div className="text-2xl font-bold text-gray-900">${metrics?.total_revenue?.toFixed(2) || '0.00'}</div>
                <div className="text-sm text-gray-600">Today's Revenue</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-blue-500">
            <div className="flex items-center">
              <Clock className="h-8 w-8 text-blue-500 mr-3" />
              <div>
                <div className="text-2xl font-bold text-gray-900">{Math.round(metrics?.average_duration || 0)}s</div>
                <div className="text-sm text-gray-600">Avg Order Time</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-yellow-500">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-yellow-500 mr-3" />
              <div>
                <div className="text-2xl font-bold text-gray-900">{metrics?.successful_orders || 0}</div>
                <div className="text-sm text-gray-600">Completed Today</div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content - Orders Only */}
        <div className="grid grid-cols-1 gap-8">
          {/* Incoming Orders - Full Width */}
          <div>
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="bg-red-600 px-6 py-4">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <ShoppingCart className="h-6 w-6 mr-2" />
                  Incoming Orders
                </h2>
                <p className="text-red-100 text-sm">Click on any order to view details</p>
              </div>
              <div className="p-6">
                {isLoading ? (
                  <div className="space-y-4">
                    {[...Array(3)].map((_, i) => (
                      <div key={i} className="animate-pulse">
                        <div className="h-20 bg-gray-200 rounded-lg"></div>
                      </div>
                    ))}
                  </div>
                ) : orders.length === 0 ? (
                  <div className="text-center py-12">
                    <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 text-lg">No orders yet</p>
                    <p className="text-gray-400 text-sm">Orders will appear here when customers place them</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {orders.map((order, index) => (
                      <div
                        key={order.id}
                        onClick={() => handleOrderClick(order)}
                        className="border-2 border-gray-200 rounded-lg p-4 hover:border-red-300 hover:shadow-md transition-all cursor-pointer group"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="mb-3">
                              <h3 className="text-lg font-bold text-gray-900 mb-1">
                                Order {index + 1}
                              </h3>
                              <p className={`text-sm font-medium ${
                                order.status === 'completed' 
                                  ? 'text-green-600' 
                                  : 'text-yellow-600'
                              }`}>
                                {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                              </p>
                            </div>
                            {/* Order Items Preview */}
                            {order.items && order.items.length > 0 && (
                              <div className="mb-3">
                                <div className="text-sm text-gray-700 font-medium mb-1">Order Items:</div>
                                <div className="flex flex-wrap gap-1">
                                  {(() => {
                                    // Group items by item_id and size for preview
                                    const groupedItems = order.items.reduce((acc, item) => {
                                      const key = `${item.item_id}-${item.size || 'regular'}`
                                      if (!acc[key]) {
                                        acc[key] = {
                                          ...item,
                                          totalQuantity: 0
                                        }
                                      }
                                      acc[key].totalQuantity += item.quantity
                                      return acc
                                    }, {} as any)

                                    const previewItems = Object.values(groupedItems).slice(0, 3)
                                    const remainingCount = Object.values(groupedItems).length - 3

                                    return (
                                      <>
                                        {previewItems.map((item: any, index) => (
                                          <span key={index} className="bg-red-50 text-red-700 text-xs px-2 py-1 rounded-full border border-red-200">
                                            {item.totalQuantity}x {getMcDonaldsItemName(item.item_id, item.item_name)}
                                          </span>
                                        ))}
                                        {remainingCount > 0 && (
                                          <span className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                                            +{remainingCount} more
                                          </span>
                                        )}
                                      </>
                                    )
                                  })()}
                                </div>
                              </div>
                            )}
                            
                            <div className="flex items-center space-x-4 text-sm text-gray-600">
                              <span className="flex items-center">
                                <DollarSign className="h-4 w-4 mr-1" />
                                ${order.total_price.toFixed(2)}
                              </span>
                              <span className="flex items-center">
                                <Clock className="h-4 w-4 mr-1" />
                                {isClient ? new Date(order.created_at).toLocaleTimeString() : '--:--:--'}
                              </span>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Eye className="h-5 w-5 text-gray-400 group-hover:text-red-500 transition-colors" />
                            <span className="text-sm text-gray-500 group-hover:text-red-600">View Details</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Order Details Modal with Tabs */}
        {showOrderDetails && selectedOrder && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="bg-red-600 px-6 py-4 rounded-t-lg">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold text-white">🍟 Order Details</h3>
                  <button
                    onClick={closeOrderDetails}
                    className="text-white hover:text-red-200 transition-colors"
                  >
                    <span className="text-2xl">&times;</span>
                  </button>
                </div>
              </div>
              
              {/* Tab Navigation */}
              <div className="border-b border-gray-200">
                <nav className="flex space-x-8 px-6">
                  <button
                    onClick={() => setActiveTab('order')}
                    className={`py-4 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'order'
                        ? 'border-red-500 text-red-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <ShoppingCart className="h-4 w-4 inline mr-2" />
                    Order Details
                  </button>
                  <button
                    onClick={handleConversationTabClick}
                    className={`py-4 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'conversation'
                        ? 'border-red-500 text-red-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <MessageSquare className="h-4 w-4 inline mr-2" />
                    Conversation
                  </button>
                </nav>
              </div>

              <div className="p-6">
                {/* Order Details Tab */}
                {activeTab === 'order' && (
                  <>
                    {selectedOrder.items && selectedOrder.items.length > 0 && (
                  <div>
                    <h4 className="text-lg font-semibold mb-4 flex items-center text-black">
                      <ShoppingCart className="h-5 w-5 mr-2 text-red-600" />
                      Order Items ({selectedOrder.items.length})
                    </h4>
                    <div className="space-y-3">
                      {(() => {
                        // Group items by item_id and size
                        const groupedItems = selectedOrder.items.reduce((acc, item) => {
                          const key = `${item.item_id}-${item.size || 'regular'}`
                          if (!acc[key]) {
                            acc[key] = {
                              ...item,
                              totalQuantity: 0,
                              totalPrice: 0
                            }
                          }
                          acc[key].totalQuantity += item.quantity
                          acc[key].totalPrice += item.price * item.quantity
                          return acc
                        }, {} as any)

                        return Object.values(groupedItems).map((item: any, index) => (
                          <div key={index} className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-100">
                            <div className="flex-1">
                              <div className="flex items-center space-x-3">
                                <span className="bg-red-600 text-white text-sm font-bold px-2 py-1 rounded-full">
                                  {item.totalQuantity}x
                                </span>
                                <div>
                                  <p className="font-semibold text-gray-900">
                                    {getMcDonaldsItemName(item.item_id, item.item_name)}
                                  </p>
                                  <p className="text-sm text-gray-600">
                                    {item.size ? `Size: ${item.size}` : 'Regular'}
                                  </p>
                                </div>
                              </div>
                            </div>
                            <div className="text-right">
                              <p className="font-bold text-lg text-red-600">${item.price.toFixed(2)} each</p>
                              <p className="text-sm text-gray-500">
                                ${item.totalPrice.toFixed(2)} total
                              </p>
                            </div>
                          </div>
                        ))
                      })()}
                    </div>

                    {/* Order Summary */}
                    <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-center text-lg font-semibold">
                        <span className="text-gray-900">Order Total:</span>
                        <span className="text-red-600">${selectedOrder.total_price.toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                )}

                    <div className="mt-6 pt-4 border-t">
                      <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                        <div>
                          <span className="font-medium">Created:</span> {isClient ? new Date(selectedOrder.created_at).toLocaleString() : '--/--/----, --:--:--'}
                        </div>
                        <div>
                          <span className="font-medium">Updated:</span> {isClient ? new Date(selectedOrder.updated_at).toLocaleString() : '--/--/----, --:--:--'}
                        </div>
                      </div>
                    </div>
                  </>
                )}

                {/* Conversation Tab */}
                {activeTab === 'conversation' && (
                  <div className="space-y-6">
                    {/* Find the conversation for this order */}
                    {(() => {
                      const relatedConversation = conversations.find(conv => 
                        conv.id === selectedOrder.conversation_id
                      )
                      
                      if (!relatedConversation) {
                        return (
                          <div className="text-center py-8">
                            <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <p className="text-gray-500">No conversation data available for this order</p>
                          </div>
                        )
                      }

                      return (
                        <>


                          {/* Conversation Transcript */}
                          <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                            <h4 className="text-lg font-semibold text-yellow-900 mb-3 flex items-center">
                              <MessageSquare className="h-5 w-5 mr-2" />
                              Conversation Transcript
                            </h4>
                            {loadingTranscript ? (
                              <div className="bg-white rounded border p-4 text-center">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-600 mx-auto"></div>
                                <p className="mt-2 text-sm text-gray-600">Loading conversation...</p>
                              </div>
                            ) : transcriptData.length > 0 ? (
                              <div className="bg-white rounded border p-4 max-h-96 overflow-y-auto space-y-3">
                                {transcriptData.map((entry, index) => (
                                  <div key={index} className={`p-3 rounded-lg ${
                                    entry.speaker === 'user' 
                                      ? 'bg-blue-50 border-l-4 border-blue-400' 
                                      : 'bg-green-50 border-l-4 border-green-400'
                                  }`}>
                                    <div className="flex items-center justify-between mb-1">
                                      <span className={`text-sm font-semibold ${
                                        entry.speaker === 'user' ? 'text-blue-700' : 'text-green-700'
                                      }`}>
                                        {entry.speaker === 'user' ? '👤 Customer' : '🤖 Agent'}
                                      </span>
                                      <span className="text-xs text-gray-500">
                                        Turn {entry.turn_number}
                                      </span>
                                    </div>
                                    <p className="text-sm text-gray-700 leading-relaxed">
                                      {entry.content}
                                    </p>
                                    <p className="text-xs text-gray-500 mt-1">
                                      {isClient ? new Date(entry.timestamp).toLocaleTimeString() : '--:--:--'}
                                    </p>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <div className="bg-white rounded border p-4 text-center">
                                <MessageSquare className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                                <p className="text-gray-500 text-sm">No transcript available for this conversation</p>
                              </div>
                            )}
                          </div>

                          {/* Combined Summary and Metrics */}
                          <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                            <h4 className="text-lg font-semibold text-purple-900 mb-3 flex items-center">
                              <MessageSquare className="h-5 w-5 mr-2" />
                              Conversation Analysis
                            </h4>
                            <div className="bg-white rounded border p-4 space-y-4">
                              {/* Summary */}
                              <div>
                                <h5 className="text-sm font-semibold text-gray-800 mb-2">Summary:</h5>
                                <p className="text-sm text-gray-700 leading-relaxed">
                                  {relatedConversation.summary || 
                                    `This conversation resulted in a ${relatedConversation.success ? 'successful' : 'failed'} order with ${relatedConversation.total_turns} total turns. ` +
                                    `The customer ${relatedConversation.sentiment_score > 0.1 ? 'seemed satisfied' : relatedConversation.sentiment_score < -0.1 ? 'appeared frustrated' : 'had a neutral experience'} ` +
                                    `during the ${Math.round(relatedConversation.duration_seconds)}-second interaction. ` +
                                    `The agent made ${relatedConversation.tool_calls_count} tool calls with ${relatedConversation.error_count} errors.`
                                  }
                                </p>
        </div>

                              {/* Metrics Grid */}
                              <div className="grid grid-cols-2 gap-4 pt-3 border-t border-gray-200">
                                <div>
                                  <span className="text-sm font-medium text-gray-700">Success Rate:</span>
                                  <span className={`ml-2 text-sm font-semibold ${
                                    relatedConversation.success ? 'text-green-600' : 'text-red-600'
                                  }`}>
                                    {relatedConversation.success ? '100%' : '0%'}
                                  </span>
                                </div>
                                <div>
                                  <span className="text-sm font-medium text-gray-700">Sentiment Score:</span>
                                  <span className={`ml-2 text-sm font-semibold ${
                                    relatedConversation.sentiment_score > 0.1 ? 'text-green-600' : 
                                    relatedConversation.sentiment_score < -0.1 ? 'text-red-600' : 'text-gray-600'
                                  }`}>
                                    {(relatedConversation.sentiment_score * 100).toFixed(1)}%
                                  </span>
                                </div>
                                <div>
                                  <span className="text-sm font-medium text-gray-700">Duration:</span>
                                  <span className="ml-2 text-sm font-semibold text-gray-600">
                                    {Math.round(relatedConversation.duration_seconds)}s
                                  </span>
                                </div>
                                <div>
                                  <span className="text-sm font-medium text-gray-700">Tool Calls:</span>
                                  <span className="ml-2 text-sm font-semibold text-gray-600">
                                    {relatedConversation.tool_calls_count}
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>

                          {/* Conversation Summary */}
                          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                            <h4 className="text-lg font-semibold text-blue-900 mb-3 flex items-center">
                              <MessageSquare className="h-5 w-5 mr-2" />
                              Conversation Summary
                            </h4>
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <span className="text-sm font-medium text-blue-700">Status:</span>
                                <span className={`ml-2 px-2 py-1 text-xs font-medium rounded-full ${
                                  relatedConversation.success 
                                    ? 'bg-green-100 text-green-800' 
                                    : 'bg-red-100 text-red-800'
                                }`}>
                                  {relatedConversation.success ? 'Success' : 'Failed'}
                                </span>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-blue-700">Duration:</span>
                                <span className="ml-2 text-sm text-blue-600">
                                  {Math.round(relatedConversation.duration_seconds)}s
                                </span>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-blue-700">Sentiment:</span>
                                <span className={`ml-2 text-sm ${
                                  relatedConversation.sentiment_score > 0.1 ? 'text-green-600' : 
                                  relatedConversation.sentiment_score < -0.1 ? 'text-red-600' : 'text-gray-600'
                                }`}>
                                  {relatedConversation.sentiment_score > 0.1 ? '😊 Positive' : 
                                   relatedConversation.sentiment_score < -0.1 ? '😞 Negative' : '😐 Neutral'}
                                </span>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-blue-700">Date:</span>
                                <span className="ml-2 text-sm text-blue-600">
                                  {isClient ? new Date(relatedConversation.created_at).toLocaleString() : '--/--/----, --:--:--'}
                                </span>
                              </div>
                            </div>
                          </div>
                        </>
                      )
                    })()}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}