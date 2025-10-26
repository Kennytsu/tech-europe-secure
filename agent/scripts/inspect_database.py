#!/usr/bin/env python3
"""
Database inspection script
"""
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from drive_thru.database_config import get_database
from drive_thru.models import Conversation, Order, OrderItem

def inspect_database():
    """Inspect database contents"""
    try:
        db = get_database()
        with db.get_session() as session:
            # Check conversations
            conversations = session.query(Conversation).all()
            print(f"📊 Database contains {len(conversations)} conversations")
            for conv in conversations:
                print(f"  - Session: {conv.session_id}")
                print(f"    Status: {conv.status}, Success: {conv.success}")
                print(f"    Duration: {conv.duration_seconds}s, Turns: {conv.total_turns}")
                print(f"    Tool calls: {conv.tool_calls_count}, Errors: {conv.error_count}")
                print()
            
            # Check orders
            orders = session.query(Order).all()
            print(f"📦 Database contains {len(orders)} orders")
            for order in orders:
                print(f"  - Order: {order.order_id}")
                print(f"    Status: {order.status}, Price: ${order.total_price}")
                print(f"    Items: {order.item_count}")
                print()
            
            # Check order items
            items = session.query(OrderItem).all()
            print(f"🍔 Database contains {len(items)} order items")
            for item in items:
                print(f"  - Item: {item.item_name} ({item.item_type})")
                print(f"    Price: ${item.price}, Quantity: {item.quantity}")
                print()
            
            return True
            
    except Exception as e:
        print(f"❌ Database inspection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Inspecting Database Contents")
    print("=" * 40)
    success = inspect_database()
    sys.exit(0 if success else 1)
