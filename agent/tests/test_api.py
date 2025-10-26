#!/usr/bin/env python3
"""
Test script for API functionality
"""
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_api_imports():
    """Test API imports and basic functionality"""
    try:
        from drive_thru.api import app
        print("✅ API app imported successfully")
        
        # Test route registration
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(f"{route.path} - {getattr(route, 'methods', 'N/A')}")
        
        print(f"✅ Found {len(routes)} API routes:")
        for route in routes:
            print(f"  - {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False

def test_database_health():
    """Test database health check"""
    try:
        from drive_thru.database_config import check_database_health
        health = check_database_health()
        
        print(f"✅ Database health: {health['status']}")
        print(f"   Connected: {health['connected']}")
        
        return health['connected']
        
    except Exception as e:
        print(f"❌ Database health check failed: {e}")
        return False

def test_data_pipeline():
    """Test data pipeline basic functionality"""
    try:
        from drive_thru.data_pipeline import data_pipeline
        print("✅ Data pipeline imported successfully")
        
        # Test pipeline methods exist
        methods = ['process_conversation_data', 'get_conversation_by_session_id', 
                  'get_orders_by_conversation_id', 'export_metrics_for_dashboard']
        
        for method in methods:
            if hasattr(data_pipeline, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Data pipeline test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Step 3: Data Pipeline & Storage")
    print("=" * 50)
    
    tests = [
        ("Database Health", test_database_health),
        ("API Imports", test_api_imports),
        ("Data Pipeline", test_data_pipeline),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Step 3 is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
