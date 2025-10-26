# McDonald's Drive-Thru Analytics Dashboard

A modern, responsive dashboard for monitoring drive-thru performance in real-time.

## Features

- 📊 **Real-time Metrics** - Live conversation count, success rates, revenue tracking
- 📈 **Analytics Charts** - Visual trends for conversations, revenue, sentiment
- 💬 **Conversation Management** - View transcripts, summaries, and sentiment analysis
- 🛒 **Order Tracking** - Monitor orders, popular items, and revenue
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **Charts**: Recharts for data visualization
- **API**: Axios for backend communication
- **Icons**: Lucide React

## Getting Started

### Prerequisites

1. **API Server Running**: Make sure the FastAPI backend is running on `http://localhost:8000`
2. **Database**: Ensure the database is initialized with conversation data

### Installation

```bash
# Install dependencies
npm install

# Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

### Running the Dashboard

```bash
# Development mode
npm run dev

# Production build
npm run build
npm start
```

## API Integration

The dashboard connects to the FastAPI backend endpoints:

- `GET /health` - Health check
- `GET /conversations` - List conversations
- `GET /orders` - List orders  
- `GET /metrics/summary` - Overall metrics
- `GET /metrics/daily` - Daily metrics
- `GET /dashboard/data` - Dashboard data
- `GET /items/popular` - Popular items

## Dashboard Pages

### Overview Dashboard (`/`)
- Key metrics cards
- Real-time conversation and revenue charts
- Recent conversations and orders
- Popular items analysis

## Configuration

### Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
NEXT_PUBLIC_DASHBOARD_TITLE="Drive-Thru Analytics"  # Dashboard title
NEXT_PUBLIC_REFRESH_INTERVAL=30000  # Auto-refresh interval (ms)
```

### Customization

- **Colors**: Update `tailwind.config.js` for custom color schemes
- **Components**: Modify components in `src/components/`
- **API**: Update `src/lib/api.ts` for different backend endpoints

## Development

### Project Structure

```
dashboard/
├── src/
│   ├── app/                 # Next.js app router
│   │   ├── page.tsx        # Main dashboard page
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Global styles
│   ├── components/         # Reusable components
│   │   ├── ui/            # Base UI components
│   │   ├── metrics-card.tsx
│   │   ├── conversation-list.tsx
│   │   ├── orders-table.tsx
│   │   └── analytics-chart.tsx
│   └── lib/               # Utilities and API
│       ├── api.ts          # API client
│       └── utils.ts       # Helper functions
├── public/                # Static assets
└── package.json
```

### Adding New Features

1. **New Metrics**: Add to `src/lib/api.ts` and create components
2. **New Charts**: Extend `src/components/analytics-chart.tsx`
3. **New Pages**: Create in `src/app/` directory
4. **Styling**: Use Tailwind classes or extend the design system

## Troubleshooting

### Common Issues

1. **Connection Error**: Ensure API server is running on correct port
2. **No Data**: Check if database has conversation data
3. **Styling Issues**: Verify Tailwind configuration
4. **Build Errors**: Check TypeScript types and imports

### Debug Mode

```bash
# Enable debug logging
NEXT_PUBLIC_DEBUG=true npm run dev
```

## Deployment

### Production Build

```bash
npm run build
npm start
```

### Environment Setup

```bash
# Production environment
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_DASHBOARD_TITLE="Production Dashboard"
```

## Contributing

1. Follow TypeScript best practices
2. Use Tailwind for styling
3. Test components thoroughly
4. Update documentation for new features

## License

MIT License - See LICENSE file for details