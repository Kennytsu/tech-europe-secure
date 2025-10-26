# API Documentation

## FastAPI Endpoints

The drive-thru agent provides a REST API for accessing conversation data, orders, and analytics.

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```
Returns API health status.

#### Conversations
```http
GET /conversations
```
Get all conversations with optional filtering.

**Query Parameters:**
- `limit`: Number of conversations to return (default: 100)
- `offset`: Number of conversations to skip (default: 0)
- `status`: Filter by conversation status
- `success`: Filter by success status

#### Orders
```http
GET /orders
```
Get all orders with optional filtering.

**Query Parameters:**
- `limit`: Number of orders to return (default: 100)
- `offset`: Number of orders to skip (default: 0)
- `status`: Filter by order status

#### Metrics Summary
```http
GET /metrics/summary
```
Get overall business metrics and performance statistics.

#### Daily Metrics
```http
GET /metrics/daily
```
Get daily aggregated metrics.

#### Dashboard Data
```http
GET /dashboard/data
```
Get comprehensive dashboard data including conversations, orders, and metrics.

#### Popular Items
```http
GET /items/popular
```
Get most popular menu items and combos.

### Response Formats

All endpoints return JSON responses with the following structure:

```json
{
  "data": [...],
  "total": 100,
  "limit": 50,
  "offset": 0
}
```

### Error Responses

```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### Example Usage

```bash
# Get recent conversations
curl "http://localhost:8000/conversations?limit=10"

# Get business metrics
curl "http://localhost:8000/metrics/summary"

# Get popular items
curl "http://localhost:8000/items/popular"
```
