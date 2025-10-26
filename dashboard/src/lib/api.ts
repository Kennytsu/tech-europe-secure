import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

// Types
export interface Conversation {
  id: string
  session_id: string
  conversation_id: string
  start_time: string
  end_time: string
  duration_seconds: number
  status: string
  success: boolean
  total_turns: number
  user_turns: number
  agent_turns: number
  tool_calls_count: number
  successful_tool_calls: number
  error_count: number
  interruption_count: number
  sentiment_score: number
  customer_satisfaction?: number
  feedback?: string
  summary?: string
  created_at: string
  updated_at: string
}

export interface Order {
  id: string
  conversation_id: string
  order_id: string
  status: string
  total_price: number
  item_count: number
  created_at: string
  updated_at: string
  items?: OrderItem[]
}

export interface OrderItem {
  id: string
  order_id: string
  item_id: string
  item_type: string
  item_name: string
  size?: string
  price: number
  quantity: number
  created_at: string
}

export interface Metrics {
  total_conversations: number
  successful_orders: number
  total_revenue: number
  average_duration: number
  average_sentiment: number
  error_rate: number
  popular_items: Array<{
    item_name: string
    count: number
    revenue: number
  }>
}

export interface DailySummary {
  date: string
  total_conversations: number
  successful_orders: number
  total_revenue: number
  average_duration: number
  average_sentiment: number
  error_rate: number
}

export interface TranscriptEntry {
  speaker: string
  content: string
  turn_number: number
  timestamp: string
}

export interface TranscriptResponse {
  conversation_id: string
  transcript: TranscriptEntry[]
}

// API Functions
export const apiClient = {
  // Health check
  async getHealth() {
    const response = await api.get('/health')
    return response.data
  },

  // Conversations
  async getConversations(limit = 50, offset = 0) {
    const response = await api.get(`/conversations?limit=${limit}&offset=${offset}`)
    return response.data
  },

  async getConversation(id: string) {
    const response = await api.get(`/conversations/${id}`)
    return response.data
  },

  // Orders
  async getOrders(limit = 50, offset = 0) {
    const response = await api.get(`/orders?limit=${limit}&offset=${offset}`)
    return response.data
  },

  async getOrder(id: string) {
    const response = await api.get(`/orders/${id}`)
    return response.data
  },

  // Metrics
  async getMetricsSummary() {
    const response = await api.get('/metrics/summary')
    return response.data
  },

  async getDailyMetrics(days = 7) {
    const response = await api.get(`/metrics/daily?days=${days}`)
    return response.data
  },

  // Dashboard data
  async getDashboardData() {
    const response = await api.get('/dashboard/data')
    return response.data
  },

  // Popular items
  async getPopularItems(limit = 10) {
    const response = await api.get(`/items/popular?limit=${limit}`)
    return response.data
  },

  // Transcript
  async getConversationTranscript(conversationId: string) {
    const response = await api.get(`/conversations/${conversationId}/transcript`)
    return response.data
  },
}

export default api
