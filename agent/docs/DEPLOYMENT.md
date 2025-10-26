# Deployment Guide

## Production Deployment

### Prerequisites
- Python 3.12+
- PostgreSQL (recommended) or SQLite
- Redis (for caching, optional)
- LiveKit server
- OpenAI API key

### Environment Setup

1. **Database Configuration:**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/drive_thru"
   ```

2. **API Keys:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export LIVEKIT_API_KEY="your-livekit-api-key"
   export LIVEKIT_API_SECRET="your-livekit-api-secret"
   ```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python scripts/init_database.py

EXPOSE 8000
CMD ["uvicorn", "drive_thru.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/drive_thru
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=drive_thru
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Scaling Considerations

1. **Database**: Use PostgreSQL for production
2. **Caching**: Implement Redis for session management
3. **Load Balancing**: Use multiple agent instances
4. **Monitoring**: Add health checks and metrics
5. **Security**: Implement authentication and rate limiting

### Monitoring

- Health checks: `GET /health`
- Metrics endpoint: `GET /metrics/summary`
- Database monitoring: Check connection pool status
- Agent performance: Monitor conversation success rates

### Security

- Use environment variables for secrets
- Implement API authentication
- Use HTTPS in production
- Regular security updates
- Database access controls
