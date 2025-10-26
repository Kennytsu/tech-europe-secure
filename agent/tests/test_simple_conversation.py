#!/usr/bin/env python3
"""
Simple test for conversation analysis
"""
import asyncio
from datetime import datetime
from drive_thru.data_pipeline import data_pipeline
from drive_thru.order import OrderState, ConversationMetrics, OrderedRegular, OrderStatus

async def test_simple_conversation():
    """Test conversation analysis with a simple order"""
    print("🧪 Testing Simple Conversation Analysis")
    print("=" * 50)
    
    # Create conversation metrics
    conversation_metrics = ConversationMetrics(
        conversation_id="C_SIMPLE001",
        start_time=datetime.now(),
        end_time=datetime.now(),
        duration_seconds=30.0,
        total_turns=4,
        user_turns=2,
        agent_turns=2,
        tool_calls_count=2,
        successful_tool_calls=2,
        error_count=0,
        interruption_count=0,
        sentiment_score=0.0,
        customer_satisfaction=None,
        feedback=None,
        transcript=""
    )
    
    # Create order state
    order_state = OrderState(
        conversation_metrics=conversation_metrics,
        status=OrderStatus.COMPLETED,
        items={}
    )
    
    # Add a Big Mac order
    big_mac = OrderedRegular(
        item_id="big_mac",
        size=None
    )
    await order_state.add(big_mac)
    
    print(f"✅ Order created with {len(order_state.items)} items")
    
    # Test conversation analysis
    print("🔍 Testing Conversation Analysis...")
    analysis = await data_pipeline._analyze_conversation(order_state)
    
    print(f"📝 Summary: {analysis['summary']}")
    print(f"😊 Sentiment Score: {analysis['sentiment_score']:.2f}")
    print(f"😊 Sentiment Type: {analysis['sentiment_type']}")
    print(f"📝 Transcript Entries: {len(analysis['transcript'])}")
    print()
    
    # Show transcript
    print("📝 Generated Transcript:")
    for entry in analysis['transcript']:
        print(f"   {entry['speaker']}: {entry['text']}")
    print()
    
    print("✅ Conversation analysis test completed!")

if __name__ == "__main__":
    asyncio.run(test_simple_conversation())
