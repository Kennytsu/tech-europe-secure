'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { TrendingUp, Activity, DollarSign, Users } from 'lucide-react'

interface AnalyticsChartProps {
  title: string
  data: any[]
  type: 'line' | 'bar'
  dataKey: string
  color?: string
  icon?: React.ComponentType<{ className?: string }>
}

export function AnalyticsChart({ 
  title, 
  data, 
  type, 
  dataKey, 
  color = '#8884d8',
  icon: Icon
}: AnalyticsChartProps) {
  const renderChart = () => {
    if (type === 'line') {
      return (
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2} />
        </LineChart>
      )
    }
    
    return (
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey={dataKey} fill={color} />
      </BarChart>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {Icon && <Icon className="h-5 w-5" />}
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}

// Pre-configured chart components
export function ConversationsChart({ data }: { data: any[] }) {
  return (
    <AnalyticsChart
      title="Conversations Over Time"
      data={data}
      type="line"
      dataKey="conversations"
      color="#3b82f6"
      icon={Users}
    />
  )
}

export function RevenueChart({ data }: { data: any[] }) {
  return (
    <AnalyticsChart
      title="Revenue Over Time"
      data={data}
      type="line"
      dataKey="revenue"
      color="#10b981"
      icon={DollarSign}
    />
  )
}

export function SentimentChart({ data }: { data: any[] }) {
  return (
    <AnalyticsChart
      title="Average Sentiment"
      data={data}
      type="line"
      dataKey="sentiment"
      color="#f59e0b"
      icon={Activity}
    />
  )
}

export function PopularItemsChart({ data }: { data: any[] }) {
  return (
    <AnalyticsChart
      title="Popular Items"
      data={data}
      type="bar"
      dataKey="count"
      color="#8b5cf6"
      icon={TrendingUp}
    />
  )
}
