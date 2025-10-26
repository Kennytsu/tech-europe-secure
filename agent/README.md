# McDonald's Drive-Thru Voice Agent

A LiveKit-powered voice agent for McDonald's drive-thru operations with comprehensive data analytics and conversation tracking.

## 🏗️ Project Structure

```
agent/
├── drive_thru/              # Core application code
│   ├── __init__.py
│   ├── agent.py             # Main voice agent
│   ├── database.py          # Menu data and configuration
│   ├── order.py             # Order models and state management
│   ├── models.py            # Database models (SQLAlchemy)
│   ├── database_config.py   # Database connection and configuration
│   ├── data_pipeline.py     # Data processing and storage
│   ├── data_validator.py    # Data validation utilities
│   ├── conversation_analyzer.py  # Conversation analysis and sentiment
│   └── api.py               # FastAPI endpoints
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_agent_integration.py
│   ├── test_api.py
│   ├── test_complete_flow.py
│   ├── test_conversation_analysis.py
│   ├── test_natural_completion.py
│   ├── test_pipeline.py
│   └── test_simple_conversation.py
├── scripts/                 # Utility scripts
│   ├── __init__.py
│   ├── init_database.py     # Database initialization
│   └── inspect_database.py  # Database inspection utility
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   cd agent
   uv pip install -e .
   ```

2. **Initialize Database:**
   ```bash
   python scripts/init_database.py
   ```

3. **Run the Agent:**
   ```bash
   uv run python -m drive_thru.agent console
   ```

4. **Start API Server:**
   ```bash
   uv run python -m drive_thru.api
   ```

## 📊 Features

- **Voice Agent**: LiveKit-powered conversational AI
- **Order Management**: Complete order lifecycle tracking
- **Data Analytics**: Conversation summaries, sentiment analysis, metrics
- **Real-time API**: FastAPI endpoints for data access
- **Database Storage**: SQLite/PostgreSQL support
- **Conversation Analysis**: Automatic transcript generation and sentiment scoring

## 🧪 Testing

Run tests from the project root:
```bash
cd agent
python -m pytest tests/
```

## 📈 Data Pipeline

The system captures and analyzes:
- Order details and success rates
- Conversation transcripts
- Customer sentiment analysis
- Performance metrics
- Business intelligence data

## 🔧 Configuration

Environment variables:
- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key for voice processing

## 📝 License

This project is part of the AI Engineering Challenge.
