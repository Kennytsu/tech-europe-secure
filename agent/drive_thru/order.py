from __future__ import annotations

import secrets
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Literal, Union, Optional
from enum import Enum

from pydantic import BaseModel, Field


def order_uid() -> str:
    alphabet = string.ascii_uppercase + string.digits  # b36
    return "O_" + "".join(secrets.choice(alphabet) for _ in range(6))


def conversation_uid() -> str:
    alphabet = string.ascii_uppercase + string.digits  # b36
    return "C_" + "".join(secrets.choice(alphabet) for _ in range(8))


class OrderStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class ConversationMetrics(BaseModel):
    """Metrics and metadata for a conversation session"""
    conversation_id: str = Field(default_factory=conversation_uid)
    session_id: Optional[str] = None
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    total_turns: int = 0
    user_turns: int = 0
    agent_turns: int = 0
    transcript: str = ""
    summary: str = ""
    sentiment: Optional[SentimentType] = None
    sentiment_score: Optional[float] = None  # -1.0 to 1.0
    order_success: bool = False
    customer_satisfaction: Optional[int] = None  # 1-5 scale
    feedback: Optional[str] = None
    error_count: int = 0
    interruption_count: int = 0
    tool_calls_count: int = 0
    successful_tool_calls: int = 0


class OrderedCombo(BaseModel):
    type: Literal["combo_meal"] = "combo_meal"
    order_id: str = Field(default_factory=order_uid)
    meal_id: str
    drink_id: str
    drink_size: Literal["M", "L"] | None
    fries_size: Literal["M", "L"]
    sauce_id: str | None


class OrderedHappy(BaseModel):
    type: Literal["happy_meal"] = "happy_meal"
    order_id: str = Field(default_factory=order_uid)
    meal_id: str
    drink_id: str
    drink_size: Literal["S", "M", "L"] | None
    sauce_id: str | None


class OrderedRegular(BaseModel):
    type: Literal["regular"] = "regular"
    order_id: str = Field(default_factory=order_uid)
    item_id: str
    size: Literal["S", "M", "L"] | None = None


OrderedItem = Annotated[
    Union[OrderedCombo, OrderedHappy, OrderedRegular], Field(discriminator="type")
]


@dataclass
class OrderState:
    items: dict[str, OrderedItem]
    status: OrderStatus = OrderStatus.IN_PROGRESS
    conversation_metrics: ConversationMetrics = None
    total_price: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.conversation_metrics is None:
            self.conversation_metrics = ConversationMetrics()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    async def add(self, item: OrderedItem) -> None:
        self.items[item.order_id] = item
        self.updated_at = datetime.utcnow()
        await self._update_total_price()

    async def remove(self, order_id: str) -> OrderedItem:
        item = self.items.pop(order_id)
        self.updated_at = datetime.utcnow()
        await self._update_total_price()
        return item

    def get(self, order_id: str) -> OrderedItem | None:
        return self.items.get(order_id)

    async def _update_total_price(self) -> None:
        """Calculate total price from all items in the order"""
        total = 0.0
        for item in self.items.values():
            # Calculate price based on item type and size
            price = self._calculate_item_price(item)
            total += price
        self.total_price = total

    def _calculate_item_price(self, item: OrderedItem) -> float:
        """Calculate item price based on McDonald's menu pricing"""
        # McDonald's menu pricing (approximate US prices)
        pricing = {
            # Combo Meals
            'combo_meal': {
                'big_mac': {'M': 8.99, 'L': 9.99},
                'quarter_pounder': {'M': 8.99, 'L': 9.99},
                'mcnuggets_10': {'M': 8.99, 'L': 9.99},
                'mcnuggets_20': {'M': 8.99, 'L': 9.99},
                'filet_o_fish': {'M': 7.99, 'L': 8.99},
                'mchicken': {'M': 7.99, 'L': 8.99},
                'crispy_chicken': {'M': 7.99, 'L': 8.99},
                'spicy_mchicken': {'M': 7.99, 'L': 8.99},
                'default': {'M': 7.99, 'L': 8.99}
            },
            # Happy Meals
            'happy_meal': {
                'big_mac': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'mcnuggets_4': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'hamburger': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'cheeseburger': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'default': {'S': 4.99, 'M': 5.99, 'L': 6.99}
            },
            # Regular Items
            'regular': {
                'big_mac': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'quarter_pounder': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'mcnuggets_4': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'mcnuggets_6': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'mcnuggets_10': {'S': 6.99, 'M': 7.99, 'L': 8.99},
                'mcnuggets_20': {'S': 9.99, 'M': 10.99, 'L': 11.99},
                'filet_o_fish': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'mchicken': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'crispy_chicken': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'spicy_mchicken': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'hamburger': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'cheeseburger': {'S': 2.99, 'M': 3.99, 'L': 4.99},
                'fries': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'coca_cola': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'sprite': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'fanta': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'coffee': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'ice_cream': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'apple_pie': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'default': {'S': 2.99, 'M': 3.99, 'L': 4.99}
            }
        }
        
        try:
            item_type = item.type
            item_id = getattr(item, 'meal_id', getattr(item, 'item_id', 'default'))
            size = getattr(item, 'drink_size', getattr(item, 'fries_size', getattr(item, 'size', 'M')))
            
            # Get the appropriate size (default to M if not found)
            if size not in ['S', 'M', 'L']:
                size = 'M'
            
            # Get price based on item type and ID
            if item_type in pricing:
                if item_id in pricing[item_type]:
                    return pricing[item_type][item_id].get(size, pricing[item_type]['default'].get(size, 4.99))
                else:
                    return pricing[item_type]['default'].get(size, 4.99)
            else:
                return 4.99  # Default fallback price
                
        except Exception:
            return 4.99  # Safe fallback

    def mark_completed(self) -> None:
        """Mark the order as completed"""
        self.status = OrderStatus.COMPLETED
        self.updated_at = datetime.utcnow()
        if self.conversation_metrics:
            self.conversation_metrics.order_success = True
            self.conversation_metrics.end_time = datetime.utcnow()
            if self.conversation_metrics.start_time:
                duration = self.conversation_metrics.end_time - self.conversation_metrics.start_time
                self.conversation_metrics.duration_seconds = duration.total_seconds()

    def mark_cancelled(self) -> None:
        """Mark the order as cancelled"""
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.utcnow()
        if self.conversation_metrics:
            self.conversation_metrics.end_time = datetime.utcnow()
            if self.conversation_metrics.start_time:
                duration = self.conversation_metrics.end_time - self.conversation_metrics.start_time
                self.conversation_metrics.duration_seconds = duration.total_seconds()

    def mark_failed(self) -> None:
        """Mark the order as failed"""
        self.status = OrderStatus.FAILED
        self.updated_at = datetime.utcnow()
        if self.conversation_metrics:
            self.conversation_metrics.end_time = datetime.utcnow()
            if self.conversation_metrics.start_time:
                duration = self.conversation_metrics.end_time - self.conversation_metrics.start_time
                self.conversation_metrics.duration_seconds = duration.total_seconds()

    def add_transcript_segment(self, segment: str, is_user: bool = True) -> None:
        """Add a transcript segment to the conversation"""
        if self.conversation_metrics:
            if is_user:
                self.conversation_metrics.user_turns += 1
            else:
                self.conversation_metrics.agent_turns += 1
            
            self.conversation_metrics.total_turns += 1
            self.conversation_metrics.transcript += f"{'User' if is_user else 'Agent'}: {segment}\n"
            self.updated_at = datetime.utcnow()

    def increment_error_count(self) -> None:
        """Increment the error count in conversation metrics"""
        if self.conversation_metrics:
            self.conversation_metrics.error_count += 1

    def increment_interruption_count(self) -> None:
        """Increment the interruption count in conversation metrics"""
        if self.conversation_metrics:
            self.conversation_metrics.interruption_count += 1

    def increment_tool_calls(self, successful: bool = True) -> None:
        """Increment tool call counts in conversation metrics"""
        if self.conversation_metrics:
            self.conversation_metrics.tool_calls_count += 1
            if successful:
                self.conversation_metrics.successful_tool_calls += 1
