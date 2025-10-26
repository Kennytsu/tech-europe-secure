#!/usr/bin/env python3
"""
Test script for drive-thru data pipeline
"""
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from drive_thru.database_config import get_database
from drive_thru.data_pipeline import data_pipeline
from drive_thru.order import OrderState, ConversationMetrics, OrderStatus
from drive_thru.order import OrderedCombo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_data_pipeline():
    """Test the data pipeline with sample data"""
    try:
        # Initialize database
        db = get_database()
        if not db.test_connection():
            logger.error("Database connection failed")
            return False
        
        # Create sample order state
        conversation_metrics = ConversationMetrics(
            conversation_id="C_TEST123",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            duration_seconds=120.5,
            total_turns=8,
            user_turns=4,
            agent_turns=4,
            tool_calls_count=3,
            successful_tool_calls=3,
            error_count=0,
            interruption_count=1,
            order_success=True,
            sentiment_score=0.8,
            customer_satisfaction=4,
            feedback="Great service!"
        )
        
        order_state = OrderState(items={})
        order_state.conversation_metrics = conversation_metrics
        order_state.status = OrderStatus.COMPLETED
        order_state.total_price = 12.99
        
        # Add sample order items
        combo_item = OrderedCombo(
            meal_id="combo_big_mac",
            drink_id="coca_cola",
            drink_size="L",
            sauce_id="ketchup",
            fries_size="L"
        )
        order_state.items[combo_item.order_id] = combo_item
        
        # Sample metrics data
        metrics_data = {
            "performance_metrics": {
                "average_response_time": 1.5,
                "tool_call_success_rate": 100.0,
                "conversation_success_rate": 100.0,
                "customer_satisfaction_rate": 80.0
            },
            "business_metrics": {
                "total_revenue": 12.99,
                "average_order_value": 12.99
            },
            "popular_items": {"combo_big_mac": 1},
            "popular_combos": {"combo_big_mac": 1},
            "popular_drinks": {"coca_cola": 1}
        }
        
        # Test data pipeline
        session_id = "session_1735005575_123456"
        result = await data_pipeline.process_conversation_data(
            session_id, order_state, metrics_data
        )
        
        logger.info(f"Pipeline result: {result}")
        
        # Test data retrieval
        conversation = await data_pipeline.get_conversation_by_session_id(session_id)
        if conversation:
            logger.info(f"Retrieved conversation: {conversation.conversation_id}")
        else:
            logger.error("Failed to retrieve conversation")
            return False
        
        # Test orders retrieval
        orders = await data_pipeline.get_orders_by_conversation_id(conversation.id)
        logger.info(f"Retrieved {len(orders)} orders")
        
        # Test dashboard data export
        dashboard_data = await data_pipeline.export_metrics_for_dashboard(session_id)
        logger.info(f"Dashboard data keys: {list(dashboard_data.keys())}")
        
        logger.info("Data pipeline test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Data pipeline test failed: {e}")
        return False


async def main():
    """Main test function"""
    logger.info("Starting data pipeline test...")
    
    success = await test_data_pipeline()
    
    if success:
        logger.info("All tests passed!")
        sys.exit(0)
    else:
        logger.error("Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
