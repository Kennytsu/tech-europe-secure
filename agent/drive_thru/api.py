"""
API endpoints for drive-thru data access
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database_config import get_database, get_db_session
from .data_pipeline import data_pipeline
from .models import ConversationResponse, OrderResponse, DailySummaryResponse

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Drive-Thru Data API",
    description="API for accessing drive-thru conversation and order data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Drive-Thru Data API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db = get_database()
    health_status = db.test_connection()
    
    return {
        "status": "healthy" if health_status else "unhealthy",
        "database_connected": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/conversations/{session_id}", response_model=ConversationResponse)
async def get_conversation(session_id: str):
    """Get conversation data by session ID"""
    try:
        conversation = await data_pipeline.get_conversation_by_session_id(session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except Exception as e:
        logger.error(f"Failed to get conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all orders with pagination"""
    try:
        orders = await data_pipeline.get_orders(limit, offset)
        return orders
    except Exception as e:
        logger.error(f"Failed to get orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{session_id}/orders", response_model=List[OrderResponse])
async def get_conversation_orders(session_id: str):
    """Get orders for a specific conversation"""
    try:
        conversation = await data_pipeline.get_conversation_by_session_id(session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        orders = await data_pipeline.get_orders_by_conversation_id(conversation.id)
        return orders
    except Exception as e:
        logger.error(f"Failed to get conversation orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations")
async def get_conversations(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    location_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db_session)
):
    """Get list of conversations with filtering"""
    try:
        from .models import Conversation
        
        query = db.query(Conversation)
        
        # Apply filters
        if status:
            query = query.filter(Conversation.status == status)
        if location_id:
            query = query.filter(Conversation.location_id == location_id)
        if start_date:
            query = query.filter(Conversation.start_time >= start_date)
        if end_date:
            query = query.filter(Conversation.start_time <= end_date)
        
        # Apply pagination
        conversations = query.offset(offset).limit(limit).all()
        total_count = query.count()
        
        return {
            "conversations": [ConversationResponse.from_orm(c) for c in conversations],
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Failed to get conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{conversation_id}/transcript")
async def get_conversation_transcript(
    conversation_id: str,
    db: Session = Depends(get_db_session)
):
    """Get transcript for a specific conversation"""
    try:
        from .models import Transcript, Conversation
        from uuid import UUID
        
        # Try to parse as UUID first, then fall back to string search
        conversation = None
        try:
            uuid_id = UUID(conversation_id)
            conversation = db.query(Conversation).filter(Conversation.id == uuid_id).first()
        except ValueError:
            # Not a valid UUID, search by conversation_id string
            conversation = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get all transcript entries for this conversation
        transcripts = db.query(Transcript).filter(
            Transcript.conversation_id == conversation.id
        ).order_by(Transcript.turn_number).all()
        
        # Format the transcript
        transcript_data = []
        for transcript in transcripts:
            transcript_data.append({
                "speaker": transcript.speaker,
                "content": transcript.content,
                "turn_number": transcript.turn_number,
                "timestamp": transcript.created_at.isoformat()
            })
        
        return {
            "conversation_id": conversation.conversation_id,
            "transcript": transcript_data
        }
    except Exception as e:
        logger.error(f"Failed to get transcript: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/summary")
async def get_metrics_summary(
    location_id: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db_session)
):
    """Get metrics summary for a date range"""
    try:
        from .models import Conversation, DailySummary
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get conversation metrics
        query = db.query(Conversation).filter(
            Conversation.start_time >= start_date,
            Conversation.start_time <= end_date
        )
        
        if location_id:
            query = query.filter(Conversation.location_id == location_id)
        
        conversations = query.all()
        
        if not conversations:
            return {
                "period": f"{start_date.date()} to {end_date.date()}",
                "total_conversations": 0,
                "success_rate": 0,
                "average_duration": 0,
                "total_revenue": 0,
                "average_order_value": 0
            }
        
        # Calculate metrics
        total_conversations = len(conversations)
        successful_conversations = len([c for c in conversations if c.success])
        success_rate = (successful_conversations / total_conversations) * 100 if total_conversations > 0 else 0
        
        durations = [c.duration_seconds for c in conversations if c.duration_seconds]
        average_duration = sum(durations) / len(durations) if durations else 0
        
        # Calculate revenue (simplified - would need to join with orders)
        total_revenue = 0  # This would need proper calculation with orders
        average_order_value = 0  # This would need proper calculation with orders
        
        return {
            "period": f"{start_date.date()} to {end_date.date()}",
            "total_conversations": total_conversations,
            "successful_conversations": successful_conversations,
            "success_rate": round(success_rate, 2),
            "average_duration": round(average_duration, 2),
            "total_revenue": total_revenue,
            "average_order_value": average_order_value,
            "total_errors": sum(c.error_count for c in conversations),
            "total_interruptions": sum(c.interruption_count for c in conversations)
        }
    except Exception as e:
        logger.error(f"Failed to get metrics summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/daily/{date}")
async def get_daily_metrics(
    date: datetime,
    location_id: Optional[str] = Query(None),
    db: Session = Depends(get_db_session)
):
    """Get daily metrics for a specific date"""
    try:
        from .models import DailySummary
        
        query = db.query(DailySummary).filter(DailySummary.date == date.date())
        
        if location_id:
            query = query.filter(DailySummary.location_id == location_id)
        
        summary = query.first()
        
        if not summary:
            raise HTTPException(status_code=404, detail="Daily summary not found")
        
        return DailySummaryResponse.from_orm(summary)
    except Exception as e:
        logger.error(f"Failed to get daily metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics/daily/{date}/generate")
async def generate_daily_metrics(
    date: datetime,
    location_id: Optional[str] = Query(None)
):
    """Generate daily metrics for a specific date"""
    try:
        await data_pipeline.generate_daily_summary(date, location_id)
        return {"message": f"Daily summary generated for {date.date()}"}
    except Exception as e:
        logger.error(f"Failed to generate daily metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/data/{session_id}")
async def get_dashboard_data(session_id: str):
    """Get dashboard data for a specific session"""
    try:
        data = await data_pipeline.export_metrics_for_dashboard(session_id)
        return data
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/popular")
async def get_popular_items(
    limit: int = Query(10, ge=1, le=50),
    item_type: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db_session)
):
    """Get popular items for a date range"""
    try:
        from .models import OrderItem, Order, Conversation
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query popular items
        query = db.query(
            OrderItem.item_id,
            OrderItem.item_name,
            OrderItem.item_type,
            func.count(OrderItem.id).label('order_count')
        ).join(Order).join(Conversation).filter(
            Conversation.start_time >= start_date,
            Conversation.start_time <= end_date
        )
        
        if item_type:
            query = query.filter(OrderItem.item_type == item_type)
        
        popular_items = query.group_by(
            OrderItem.item_id,
            OrderItem.item_name,
            OrderItem.item_type
        ).order_by(
            func.count(OrderItem.id).desc()
        ).limit(limit).all()
        
        return {
            "popular_items": [
                {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "item_type": item.item_type,
                    "order_count": item.order_count
                }
                for item in popular_items
            ],
            "period": f"{start_date.date()} to {end_date.date()}"
        }
    except Exception as e:
        logger.error(f"Failed to get popular items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/daily")
async def get_daily_metrics(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db_session)
):
    """Get daily metrics for the last N days"""
    try:
        from .models import DailySummary
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get daily summaries
        summaries = db.query(DailySummary).filter(
            DailySummary.date >= start_date.date(),
            DailySummary.date <= end_date.date()
        ).order_by(DailySummary.date.desc()).all()
        
        # If no summaries exist, create mock data for demo
        if not summaries:
            summaries = []
            for i in range(days):
                date = (end_date - timedelta(days=i)).date()
                summaries.append({
                    "date": date.isoformat(),
                    "total_conversations": max(1, 3 - i),
                    "successful_orders": max(1, 3 - i),
                    "total_revenue": max(5.99, 17.97 - (i * 2.99)),
                    "average_duration": max(20, 30 - i),
                    "average_sentiment": max(0.1, 0.8 - (i * 0.1)),
                    "error_rate": max(0, i * 0.05)
                })
        
        return {"daily_summaries": summaries}
    except Exception as e:
        logger.error(f"Failed to get daily metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
