#!/usr/bin/env python3
"""
Test agent integration with data pipeline
"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from drive_thru.agent import new_userdata, DriveThruAgent
from drive_thru.order import OrderState, OrderStatus, ConversationMetrics
from drive_thru.data_pipeline import data_pipeline
from drive_thru.database_config import get_database
from drive_thru.models import Conversation, Order, OrderItem

async def test_agent_integration():
    """Test complete agent integration with data pipeline"""
    try:
        print("🤖 Testing Agent Integration with Data Pipeline")
        print("=" * 60)
        
        # 1. Create userdata (simulating agent startup)
        print("1️⃣ Creating agent userdata...")
        userdata = await new_userdata()
        print(f"   ✅ Session ID: {userdata.session_id}")
        print(f"   ✅ Conversation ID: {userdata.order.conversation_metrics.conversation_id}")
        
        # 2. Simulate agent conversation
        print("\n2️⃣ Simulating agent conversation...")
        
        # Add some transcript segments
        userdata.order.add_transcript_segment("Hello, I'd like to order a Big Mac combo", is_user=True)
        userdata.order.add_transcript_segment("I'd be happy to help you with that order. Let me add a Big Mac combo to your order.", is_user=False)
        userdata.order.add_transcript_segment("Yes, with a large Coke and large fries", is_user=True)
        userdata.order.add_transcript_segment("Perfect! I've added a Big Mac combo with large Coke and large fries to your order.", is_user=False)
        userdata.order.add_transcript_segment("That's everything, thank you", is_user=True)
        userdata.order.add_transcript_segment("Your order is complete! The total is $12.99. Please drive to the first window.", is_user=False)
        
        # Update metrics
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=True)
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=False)
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=True)
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=False)
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=True)
        userdata.metrics.update_turn_metrics(userdata.session_id, is_user=False)
        
        # Simulate tool calls
        userdata.metrics.update_tool_call_metrics(userdata.session_id, successful=True)
        userdata.metrics.update_tool_call_metrics(userdata.session_id, successful=True)
        userdata.metrics.update_tool_call_metrics(userdata.session_id, successful=True)
        
        # Set order as completed
        userdata.order.status = OrderStatus.COMPLETED
        userdata.order.total_price = 12.99
        userdata.order.mark_completed()
        
        print(f"   ✅ Conversation completed")
        print(f"   ✅ Total turns: {userdata.order.conversation_metrics.total_turns}")
        print(f"   ✅ Tool calls: {userdata.order.conversation_metrics.tool_calls_count}")
        print(f"   ✅ Order status: {userdata.order.status}")
        print(f"   ✅ Order total: ${userdata.order.total_price}")
        
        # 3. Test data pipeline processing
        print("\n3️⃣ Testing data pipeline processing...")
        
        # Finalize metrics
        userdata.metrics.end_session_metrics(userdata.session_id, userdata.order)
        final_metrics = userdata.metrics.export_metrics()
        
        # Process through data pipeline
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
        
        # 4. Verify data storage
        print("\n4️⃣ Verifying data storage...")
        
        db = get_database()
        with db.get_session() as session:
            # Check conversation
            conv = session.query(Conversation).filter(
                Conversation.session_id == userdata.session_id
            ).first()
            
            if conv:
                print(f"   ✅ Conversation stored: {conv.conversation_id}")
                print(f"   ✅ Status: {conv.status}, Success: {conv.success}")
                print(f"   ✅ Duration: {conv.duration_seconds}s")
                print(f"   ✅ Turns: {conv.total_turns}")
                print(f"   ✅ Tool calls: {conv.tool_calls_count}")
                
                # Check orders
                orders = session.query(Order).filter(
                    Order.conversation_id == conv.id
                ).all()
                print(f"   ✅ Orders stored: {len(orders)}")
                
                for order in orders:
                    print(f"      - Order: {order.order_id}, Status: {order.status}, Price: ${order.total_price}")
                    
                    # Check order items
                    items = session.query(OrderItem).filter(
                        OrderItem.order_id == order.id
                    ).all()
                    print(f"      - Items: {len(items)}")
                    for item in items:
                        print(f"        * {item.item_name} ({item.item_type}) - ${item.price}")
            else:
                print("   ❌ Conversation not found in database")
                return False
        
        # 5. Test API endpoints
        print("\n5️⃣ Testing API endpoints...")
        
        # Test conversation retrieval
        retrieved_conv = await data_pipeline.get_conversation_by_session_id(userdata.session_id)
        if retrieved_conv:
            print(f"   ✅ Retrieved conversation: {retrieved_conv.conversation_id}")
        else:
            print("   ❌ Failed to retrieve conversation")
            return False
        
        # Test dashboard data export
        dashboard_data = await data_pipeline.export_metrics_for_dashboard(userdata.session_id)
        if 'conversation' in dashboard_data:
            print(f"   ✅ Dashboard data exported successfully")
            print(f"   ✅ Data keys: {list(dashboard_data.keys())}")
        else:
            print("   ❌ Dashboard data export failed")
            return False
        
        print("\n🎉 Agent Integration Test Completed Successfully!")
        print("=" * 60)
        print("✅ Agent userdata creation")
        print("✅ Conversation simulation")
        print("✅ Metrics collection")
        print("✅ Data pipeline processing")
        print("✅ Database storage")
        print("✅ API data retrieval")
        print("✅ Dashboard data export")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_agent_integration()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
