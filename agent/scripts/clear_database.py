#!/usr/bin/env python3
"""
Clear all data from the database
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from drive_thru.database_config import get_database
from drive_thru.models import Base, Conversation, Order, OrderItem, Transcript
from sqlalchemy.orm import sessionmaker

def clear_database():
    """Clear all data from the database"""
    db = get_database()
    engine = db.engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        print("🗑️  Clearing all data from database...")
        
        # Delete all data from tables in reverse order of dependency
        deleted_transcripts = session.query(Transcript).delete()
        print(f"   ✅ Deleted {deleted_transcripts} transcript entries")
        
        deleted_items = session.query(OrderItem).delete()
        print(f"   ✅ Deleted {deleted_items} order items")
        
        deleted_orders = session.query(Order).delete()
        print(f"   ✅ Deleted {deleted_orders} orders")
        
        deleted_conversations = session.query(Conversation).delete()
        print(f"   ✅ Deleted {deleted_conversations} conversations")
        
        session.commit()
        print("✅ Database cleared successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error clearing database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    clear_database()

