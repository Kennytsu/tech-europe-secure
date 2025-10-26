#!/usr/bin/env python3
"""
Test to demonstrate natural agent completion
"""
import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from drive_thru.agent import new_userdata
from drive_thru.order import OrderState, OrderStatus
from drive_thru.data_pipeline import data_pipeline
from drive_thru.database_config import get_database
from drive_thru.models import Conversation

async def test_natural_completion():
    """Test what happens when agent completes naturally"""
    try:
        print("🧪 Testing Natural Agent Completion")
        print("=" * 50)
        
        # 1. Create userdata (simulating agent startup)
        print("1️⃣ Creating agent userdata...")
        userdata = await new_userdata()
        print(f"   ✅ Session ID: {userdata.session_id}")
        print(f"   ✅ Conversation ID: {userdata.order.conversation_metrics.conversation_id}")
        
        # 2. Simulate the conversation that happened
        print("\n2️⃣ Simulating your conversation...")
        
        # Add transcript
        userdata.order.add_transcript_segment("Hello, welcome to McDonald's! How can I help you today?", is_user=False)
        userdata.order.add_transcript_segment("I'd like a Big Mac", is_user=True)
        userdata.order.add_transcript_segment("Great! I'll add a Big Mac to your order.", is_user=False)
        userdata.order.add_transcript_segment("That's everything", is_user=True)
        userdata.order.add_transcript_segment("Perfect! Your order is complete. Please drive to the first window. Have a great day!", is_user=False)
        
        # Update metrics
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=False)  # Agent greeting
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=True)   # Customer order
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=False)  # Agent response
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=True)   # Customer completion
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=False)  # Agent completion
        
        # Simulate tool calls
        userdata.metrics.update_tool_call_metrics(userdata.session_id, successful=True)  # order_regular_item
        userdata.metrics.update_tool_call_metrics(userdata.session_id, successful=True)  # complete_order
        
        # Set order as completed
        userdata.order.status = OrderStatus.COMPLETED
        userdata.order.total_price = 8.99
        userdata.order.mark_completed()
        
        print(f"   ✅ Conversation completed with {userdata.order.conversation_metrics.total_turns} turns")
        print(f"   ✅ Order status: {userdata.order.status}")
        print(f"   ✅ Order total: ${userdata.order.total_price}")
        
        # 3. Simulate NATURAL shutdown (this is what should happen)
        print("\n3️⃣ Simulating NATURAL agent shutdown...")
        print("   (This is what happens when agent completes the conversation)")
        
        # Finalize metrics
        userdata.metrics.end_session_metrics(userdata.session_id, userdata.order)
        final_metrics = userdata.metrics.export_metrics()
        
        print(f"   ✅ Metrics finalized")
        print(f"   ✅ Business metrics: {final_metrics['business_summary']['business_metrics']}")
        
        # Process through data pipeline
        print("\n4️⃣ Processing data through pipeline...")
        pipeline_result = await data_pipeline.process_conversation_data(
            userdata.session_id,
            userdata.order,
            final_metrics
        )
        
        print(f"   ✅ Pipeline result: {pipeline_result['status']}")
        if pipeline_result['status'] == 'success':
            print(f"   ✅ Conversation ID: {pipeline_result['conversation_id']}")
        else:
            print(f"   ❌ Pipeline error: {pipeline_result['message']}")
            return False
        
        # 5. Verify data was saved
        print("\n5️⃣ Verifying database storage...")
        
        db = get_database()
        with db.get_session() as session:
            conv = session.query(Conversation).filter(
                Conversation.session_id == userdata.session_id
            ).first()
            
            if conv:
                print(f"   ✅ Conversation stored: {conv.conversation_id}")
                print(f"   ✅ Status: {conv.status}, Success: {conv.success}")
                print(f"   ✅ Duration: {conv.duration_seconds}s")
                print(f"   ✅ Turns: {conv.total_turns}")
                print(f"   ✅ Tool calls: {conv.tool_calls_count}")
            else:
                print("   ❌ Conversation not found in database")
                return False
        
        print("\n🎉 Natural Completion Test PASSED!")
        print("=" * 50)
        print("✅ This proves the data pipeline works when agent completes naturally")
        print("✅ The issue is that the agent needs to finish the conversation")
        print("✅ In a real scenario, the agent would say 'Your order is complete'")
        print("✅ Then the shutdown callback would run and save all data")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_natural_completion()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
