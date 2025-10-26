'use client'

import { Badge } from '@/components/ui/badge'
import { formatDate, formatDuration, getSentimentColor, getStatusColor } from '@/lib/utils'
import { Conversation } from '@/lib/api'
import { MessageSquare, Clock, User, Bot } from 'lucide-react'

interface ConversationListProps {
  conversations: Conversation[]
  isLoading?: boolean
}

export function ConversationList({ conversations, isLoading }: ConversationListProps) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded-lg"></div>
          </div>
        ))}
      </div>
    )
  }

  if (conversations.length === 0) {
    return (
      <div className="text-center py-6">
        <MessageSquare className="h-8 w-8 text-gray-400 mx-auto mb-2" />
        <p className="text-gray-500 text-sm">No conversations yet</p>
        <p className="text-gray-400 text-xs">Conversations will appear here</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {conversations.map((conversation) => (
        <div
          key={conversation.id}
          className="bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors border border-gray-200"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                conversation.success 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {conversation.success ? 'Success' : 'Failed'}
              </span>
              <span className="text-xs text-gray-500">
                {formatDuration(conversation.duration_seconds)}
              </span>
            </div>
            <span className={`text-sm ${
              conversation.sentiment_score > 0.1 ? 'text-green-600' : 
              conversation.sentiment_score < -0.1 ? 'text-red-600' : 'text-gray-600'
            }`}>
              {conversation.sentiment_score > 0.1 ? '😊' : 
               conversation.sentiment_score < -0.1 ? '😞' : '😐'}
            </span>
          </div>
          
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>ID: {conversation.conversation_id.slice(-8)}</span>
            <span>{formatDate(conversation.created_at)}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
