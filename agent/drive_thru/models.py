"""
Database models for drive-thru data pipeline
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4, UUID
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, 
    ForeignKey, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy import JSON
from sqlalchemy.orm import relationship

Base = declarative_base()


class OrderStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ItemType(str, Enum):
    REGULAR = "regular"
    COMBO = "combo"
    HAPPY_MEAL = "happy_meal"
    DRINK = "drink"
    SAUCE = "sauce"


class Conversation(Base):
    """Core conversation tracking table"""
    __tablename__ = "conversations"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    conversation_id = Column(String(255), nullable=False, index=True)
    location_id = Column(String(255), nullable=True, index=True)  # For multi-location support
    
    # Timing
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Status and success
    status = Column(String(50), nullable=False, default=ConversationStatus.ACTIVE)
    success = Column(Boolean, nullable=False, default=False)
    
    # Interaction metrics
    total_turns = Column(Integer, nullable=False, default=0)
    user_turns = Column(Integer, nullable=False, default=0)
    agent_turns = Column(Integer, nullable=False, default=0)
    tool_calls_count = Column(Integer, nullable=False, default=0)
    successful_tool_calls = Column(Integer, nullable=False, default=0)
    error_count = Column(Integer, nullable=False, default=0)
    interruption_count = Column(Integer, nullable=False, default=0)
    
    # Quality metrics
    sentiment_score = Column(Float, nullable=True)
    customer_satisfaction = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)  # Conversation summary
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="conversation", cascade="all, delete-orphan")
    transcripts = relationship("Transcript", back_populates="conversation", cascade="all, delete-orphan")
    metrics = relationship("ConversationMetrics", back_populates="conversation", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_conversation_location_time', 'location_id', 'start_time'),
        Index('idx_conversation_status_time', 'status', 'start_time'),
    )


class Order(Base):
    """Order management table"""
    __tablename__ = "orders"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(PostgresUUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    order_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Order details
    status = Column(String(50), nullable=False, default=OrderStatus.IN_PROGRESS)
    total_price = Column(Float, nullable=False, default=0.0)
    item_count = Column(Integer, nullable=False, default=0)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_order_conversation', 'conversation_id'),
        Index('idx_order_status_time', 'status', 'created_at'),
    )


class OrderItem(Base):
    """Individual order items table"""
    __tablename__ = "order_items"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id = Column(PostgresUUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    
    # Item details
    item_id = Column(String(255), nullable=False, index=True)
    item_type = Column(String(50), nullable=False, index=True)
    item_name = Column(String(255), nullable=False)
    size = Column(String(10), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    # Additional item data
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    
    # Indexes
    __table_args__ = (
        Index('idx_order_item_order', 'order_id'),
        Index('idx_order_item_type', 'item_type'),
        Index('idx_order_item_id', 'item_id'),
    )


class Transcript(Base):
    """Conversation transcript storage"""
    __tablename__ = "transcripts"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(PostgresUUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    
    # Transcript content
    content = Column(Text, nullable=False)
    speaker = Column(String(50), nullable=False)  # 'user' or 'agent'
    turn_number = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="transcripts")
    
    # Indexes
    __table_args__ = (
        Index('idx_transcript_conversation', 'conversation_id'),
        Index('idx_transcript_turn', 'conversation_id', 'turn_number'),
    )


class ConversationMetrics(Base):
    """Detailed conversation metrics"""
    __tablename__ = "conversation_metrics"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(PostgresUUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    
    # Performance metrics
    average_response_time = Column(Float, nullable=True)
    tool_call_success_rate = Column(Float, nullable=True)
    conversation_success_rate = Column(Float, nullable=True)
    customer_satisfaction_rate = Column(Float, nullable=True)
    
    # Business metrics
    total_revenue = Column(Float, nullable=False, default=0.0)
    average_order_value = Column(Float, nullable=True)
    popular_items = Column(JSON, nullable=True)
    popular_combos = Column(JSON, nullable=True)
    popular_drinks = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="metrics")
    
    # Indexes
    __table_args__ = (
        Index('idx_metrics_conversation', 'conversation_id'),
    )


class DailySummary(Base):
    """Daily aggregated metrics for analytics"""
    __tablename__ = "daily_summaries"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    location_id = Column(String(255), nullable=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    # Daily totals
    total_conversations = Column(Integer, nullable=False, default=0)
    successful_conversations = Column(Integer, nullable=False, default=0)
    failed_conversations = Column(Integer, nullable=False, default=0)
    cancelled_conversations = Column(Integer, nullable=False, default=0)
    
    # Revenue metrics
    total_revenue = Column(Float, nullable=False, default=0.0)
    average_order_value = Column(Float, nullable=True)
    total_orders = Column(Integer, nullable=False, default=0)
    
    # Performance metrics
    average_conversation_duration = Column(Float, nullable=True)
    average_tool_call_success_rate = Column(Float, nullable=True)
    total_errors = Column(Integer, nullable=False, default=0)
    total_interruptions = Column(Integer, nullable=False, default=0)
    
    # Item popularity (stored as JSON)
    popular_items = Column(JSON, nullable=True)
    popular_combos = Column(JSON, nullable=True)
    popular_drinks = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('location_id', 'date', name='unique_daily_summary'),
        Index('idx_daily_summary_date', 'date'),
        Index('idx_daily_summary_location_date', 'location_id', 'date'),
    )


# Pydantic models for API responses
class ConversationResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    session_id: str
    conversation_id: str
    location_id: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: Optional[float]
    status: str
    success: bool
    total_turns: int
    user_turns: int
    agent_turns: int
    tool_calls_count: int
    successful_tool_calls: int
    error_count: int
    interruption_count: int
    sentiment_score: Optional[float]
    customer_satisfaction: Optional[int]
    feedback: Optional[str]
    created_at: datetime
    updated_at: datetime


class OrderResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    conversation_id: UUID
    order_id: str
    status: str
    total_price: float
    item_count: int
    created_at: datetime
    updated_at: datetime
    items: List[Dict[str, Any]] = []


class MetricsResponse(BaseModel):
    model_config = {"from_attributes": True}
    business_metrics: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    popular_items: Dict[str, int]
    popular_combos: Dict[str, int]
    popular_drinks: Dict[str, int]
    timestamp: datetime


class DailySummaryResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    location_id: Optional[str]
    date: datetime
    total_conversations: int
    successful_conversations: int
    failed_conversations: int
    cancelled_conversations: int
    total_revenue: float
    average_order_value: Optional[float]
    total_orders: int
    average_conversation_duration: Optional[float]
    average_tool_call_success_rate: Optional[float]
    total_errors: int
    total_interruptions: int
    popular_items: Optional[Dict[str, Any]]
    popular_combos: Optional[Dict[str, Any]]
    popular_drinks: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
