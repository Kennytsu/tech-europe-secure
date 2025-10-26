#!/usr/bin/env python3
"""
Test conversation analysis features
"""
import asyncio
from datetime import datetime
from drive_thru.data_pipeline import data_pipeline
from drive_thru.order import OrderState, ConversationMetrics, OrderedRegular, OrderStatus
from drive_thru.conversation_analyzer import conversation_analyzer, ConversationTurn

async def test_conversation_analysis():
    """Test the conversation analysis features"""
    print("🧪 Testing Conversation Analysis Features")
    print("=" * 50)
    
    # Create a test order state
    conversation_metrics = ConversationMetrics(
        conversation_id="C_TEST001",
        start_time=datetime.now(),
        end_time=datetime.now(),
        duration_seconds=25.5,
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
        name="Big Mac",
        price=5.99,
        size=None
    )
    await order_state.add(big_mac)
    
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
    
    # Test data pipeline processing
    print("🚀 Testing Data Pipeline Processing...")
    session_id = f"session_{int(datetime.now().timestamp())}_{int(datetime.now().timestamp() * 1000) % 10000000}"
    
    # Mock metrics data
    metrics_data = {
        'business_summary': {
            'business_metrics': {
                'total_orders': 1,
                'successful_orders': 1,
                'total_revenue': 5.99,
                'average_order_value': 5.99
            }
        }
    }
    
    result = await data_pipeline.process_conversation_data(
        session_id, order_state, metrics_data
    )
    
    print(f"✅ Pipeline Result: {result}")
    print()
    
    # Check what was saved
    print("📊 Checking Saved Data...")
    from drive_thru.database_config import get_database
    from drive_thru.models import Conversation, Transcript
    
    db = get_database()
    with db.get_session() as session:
        # Find the conversation
        conv = session.query(Conversation).filter(Conversation.session_id == session_id).first()
        if conv:
            print(f"✅ Conversation saved: {conv.session_id}")
            print(f"   Summary: {conv.summary}")
            print(f"   Sentiment: {conv.sentiment_score}")
            print(f"   Status: {conv.status}")
            print()
            
            # Check transcripts
            transcripts = session.query(Transcript).filter(Transcript.conversation_id == conv.id).all()
            print(f"📝 Transcripts saved: {len(transcripts)}")
            for transcript in transcripts:
                print(f"   {transcript.speaker}: {transcript.text}")
        else:
            print("❌ Conversation not found")

if __name__ == "__main__":
    asyncio.run(test_conversation_analysis())
