"""
API endpoints for drive-thru data access
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database_config import get_database, get_db_session
from .data_pipeline import data_pipeline
from .models import ConversationResponse, OrderResponse, DailySummaryResponse

# Import CVE packages for individual vulnerability implementations
from .cve_packages.sql_injection import sql_injection_vulnerability
from .cve_packages.xss import xss_vulnerability
from .cve_packages.insecure_deserialization import insecure_deserialization_vulnerability
from .cve_packages.weak_crypto_md5 import md5_vulnerability
from .cve_packages.weak_crypto_des import des_vulnerability
from .cve_packages.missing_authentication import missing_authentication_vulnerability
from .cve_packages.idor import idor_vulnerability
from .cve_packages.command_injection import command_injection_vulnerability
from .cve_packages.unsafe_eval import unsafe_eval_vulnerability
from .cve_packages.hardcoded_secrets import hardcoded_secrets_vulnerability
from .cve_packages.secrets_exposure import secrets_exposure_vulnerability
from .cve_packages.missing_security_headers import missing_security_headers_vulnerability

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Drive-Thru Data API",
    description="API for accessing drive-thru conversation and order data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# VULNERABLE: Missing security headers middleware
# This should include CSP, X-Frame-Options, X-Content-Type-Options, etc.
@app.middleware("http")
async def add_security_headers(request, call_next):
    """VULNERABLE: Missing security headers"""
    response = await call_next(request)
    
    # Use the CVE package for missing security headers
    vulnerable_headers = missing_security_headers_vulnerability.vulnerable_add_security_headers(dict(response.headers))
    
    # Apply the vulnerable headers (which intentionally omit security headers)
    for key, value in vulnerable_headers.items():
        if key != "warning":
            response.headers[key] = value
    
    return response


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Drive-Thru Data API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db = get_database()
    health_status = db.test_connection()
    
    return {
        "status": "healthy" if health_status else "unhealthy",
        "database_connected": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/conversations/{session_id}", response_model=ConversationResponse)
async def get_conversation(session_id: str):
    """Get conversation data by session ID"""
    try:
        conversation = await data_pipeline.get_conversation_by_session_id(session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except Exception as e:
        logger.error(f"Failed to get conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all orders with pagination"""
    try:
        orders = await data_pipeline.get_orders(limit, offset)
        return orders
    except Exception as e:
        logger.error(f"Failed to get orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{session_id}/orders", response_model=List[OrderResponse])
async def get_conversation_orders(session_id: str):
    """Get orders for a specific conversation"""
    try:
        conversation = await data_pipeline.get_conversation_by_session_id(session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        orders = await data_pipeline.get_orders_by_conversation_id(conversation.id)
        return orders
    except Exception as e:
        logger.error(f"Failed to get conversation orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations")
async def get_conversations(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    location_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db_session)
):
    """Get list of conversations with filtering"""
    try:
        from .models import Conversation
        
        query = db.query(Conversation)
        
        # Apply filters
        if status:
            query = query.filter(Conversation.status == status)
        if location_id:
            query = query.filter(Conversation.location_id == location_id)
        if start_date:
            query = query.filter(Conversation.start_time >= start_date)
        if end_date:
            query = query.filter(Conversation.start_time <= end_date)
        
        # Apply pagination
        conversations = query.offset(offset).limit(limit).all()
        total_count = query.count()
        
        return {
            "conversations": [ConversationResponse.from_orm(c) for c in conversations],
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Failed to get conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/search")
async def search_conversations(
    search_query: str = Query(..., description="Search query for conversations"),
    db: Session = Depends(get_db_session)
):
    """Search conversations by query - VULNERABLE: SQL injection"""
    try:
        # Use the CVE package for SQL injection vulnerability
        conversations = sql_injection_vulnerability.vulnerable_search_conversations(search_query, db)
        
        return {
            "search_query": search_query,
            "conversations": conversations,
            "total_found": len(conversations),
            "warning": "VULNERABLE: SQL injection vulnerability detected"
        }
    except Exception as e:
        logger.error(f"Failed to search conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{conversation_id}/transcript")
async def get_conversation_transcript(
    conversation_id: str,
    db: Session = Depends(get_db_session)
):
    """Get transcript for a specific conversation"""
    try:
        from .models import Transcript, Conversation
        from uuid import UUID
        
        # Try to parse as UUID first, then fall back to string search
        conversation = None
        try:
            uuid_id = UUID(conversation_id)
            conversation = db.query(Conversation).filter(Conversation.id == uuid_id).first()
        except ValueError:
            # Not a valid UUID, search by conversation_id string
            conversation = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get all transcript entries for this conversation
        transcripts = db.query(Transcript).filter(
            Transcript.conversation_id == conversation.id
        ).order_by(Transcript.turn_number).all()
        
        # Format the transcript
        transcript_data = []
        for transcript in transcripts:
            transcript_data.append({
                "speaker": transcript.speaker,
                "content": transcript.content,
                "turn_number": transcript.turn_number,
                "timestamp": transcript.created_at.isoformat()
            })
        
        return {
            "conversation_id": conversation.conversation_id,
            "transcript": transcript_data
        }
    except Exception as e:
        logger.error(f"Failed to get transcript: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/summary")
async def get_metrics_summary(
    location_id: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db_session)
):
    """Get metrics summary for a date range"""
    try:
        from .models import Conversation, DailySummary
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get conversation metrics
        query = db.query(Conversation).filter(
            Conversation.start_time >= start_date,
            Conversation.start_time <= end_date
        )
        
        if location_id:
            query = query.filter(Conversation.location_id == location_id)
        
        conversations = query.all()
        
        if not conversations:
            return {
                "period": f"{start_date.date()} to {end_date.date()}",
                "total_conversations": 0,
                "success_rate": 0,
                "average_duration": 0,
                "total_revenue": 0,
                "average_order_value": 0
            }
        
        # Calculate metrics
        total_conversations = len(conversations)
        successful_conversations = len([c for c in conversations if c.success])
        success_rate = (successful_conversations / total_conversations) * 100 if total_conversations > 0 else 0
        
        durations = [c.duration_seconds for c in conversations if c.duration_seconds]
        average_duration = sum(durations) / len(durations) if durations else 0
        
        # Calculate revenue (simplified - would need to join with orders)
        total_revenue = 0  # This would need proper calculation with orders
        average_order_value = 0  # This would need proper calculation with orders
        
        return {
            "period": f"{start_date.date()} to {end_date.date()}",
            "total_conversations": total_conversations,
            "successful_conversations": successful_conversations,
            "success_rate": round(success_rate, 2),
            "average_duration": round(average_duration, 2),
            "total_revenue": total_revenue,
            "average_order_value": average_order_value,
            "total_errors": sum(c.error_count for c in conversations),
            "total_interruptions": sum(c.interruption_count for c in conversations)
        }
    except Exception as e:
        logger.error(f"Failed to get metrics summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/daily/{date}")
async def get_daily_metrics(
    date: datetime,
    location_id: Optional[str] = Query(None),
    db: Session = Depends(get_db_session)
):
    """Get daily metrics for a specific date"""
    try:
        from .models import DailySummary
        
        query = db.query(DailySummary).filter(DailySummary.date == date.date())
        
        if location_id:
            query = query.filter(DailySummary.location_id == location_id)
        
        summary = query.first()
        
        if not summary:
            raise HTTPException(status_code=404, detail="Daily summary not found")
        
        return DailySummaryResponse.from_orm(summary)
    except Exception as e:
        logger.error(f"Failed to get daily metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics/daily/{date}/generate")
async def generate_daily_metrics(
    date: datetime,
    location_id: Optional[str] = Query(None)
):
    """Generate daily metrics for a specific date"""
    try:
        await data_pipeline.generate_daily_summary(date, location_id)
        return {"message": f"Daily summary generated for {date.date()}"}
    except Exception as e:
        logger.error(f"Failed to generate daily metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/data/{session_id}")
async def get_dashboard_data(session_id: str):
    """Get dashboard data for a specific session"""
    try:
        data = await data_pipeline.export_metrics_for_dashboard(session_id)
        return data
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/popular")
async def get_popular_items(
    limit: int = Query(10, ge=1, le=50),
    item_type: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db_session)
):
    """Get popular items for a date range"""
    try:
        from .models import OrderItem, Order, Conversation
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query popular items
        query = db.query(
            OrderItem.item_id,
            OrderItem.item_name,
            OrderItem.item_type,
            func.count(OrderItem.id).label('order_count')
        ).join(Order).join(Conversation).filter(
            Conversation.start_time >= start_date,
            Conversation.start_time <= end_date
        )
        
        if item_type:
            query = query.filter(OrderItem.item_type == item_type)
        
        popular_items = query.group_by(
            OrderItem.item_id,
            OrderItem.item_name,
            OrderItem.item_type
        ).order_by(
            func.count(OrderItem.id).desc()
        ).limit(limit).all()
        
        return {
            "popular_items": [
                {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "item_type": item.item_type,
                    "order_count": item.order_count
                }
                for item in popular_items
            ],
            "period": f"{start_date.date()} to {end_date.date()}"
        }
    except Exception as e:
        logger.error(f"Failed to get popular items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/unlock")
async def admin_unlock():
    """Admin unlock endpoint - VULNERABLE: missing authentication"""
    # Use the CVE package for missing authentication vulnerability
    return missing_authentication_vulnerability.vulnerable_admin_unlock()


@app.get("/debug/secrets")
async def debug_all_secrets():
    """Debug endpoint to show all secrets - VULNERABLE: secrets exposure"""
    # Use the CVE package for secrets exposure vulnerability
    return secrets_exposure_vulnerability.vulnerable_debug_secrets_endpoint()


@app.post("/user/{user_id}/data")
async def get_user_data(user_id: int):
    """Get user data by ID - VULNERABLE: IDOR (Insecure Direct Object Reference)"""
    # Use the CVE package for IDOR vulnerability
    return idor_vulnerability.vulnerable_get_user_data(user_id)


@app.post("/process/feedback")
async def process_feedback(feedback_data: dict):
    """Process customer feedback - VULNERABLE: Reflected XSS"""
    # Use the CVE package for XSS vulnerability
    return xss_vulnerability.vulnerable_feedback_processing(feedback_data)


@app.post("/crypto/encrypt")
async def encrypt_data(data: dict):
    """Encrypt data - VULNERABLE: weak crypto"""
    plaintext = data.get("data", "")
    
    # Use the CVE package for DES encryption vulnerability
    encrypted_result = des_vulnerability.vulnerable_encrypt_data(plaintext)
    
    # VULNERABLE: Logging sensitive data
    logger.info(f"Encrypted data for user: {plaintext}")
    
    return encrypted_result


@app.post("/crypto/hash-password")
async def hash_password(password_data: dict):
    """Hash password - VULNERABLE: weak hashing"""
    password = password_data.get("password", "")
    
    # Use the CVE package for MD5 vulnerability
    hashed_result = md5_vulnerability.vulnerable_hash_password(password)
    
    # VULNERABLE: Logging passwords in plaintext
    logger.info(f"Password hash request for password: {password}")
    
    return hashed_result


@app.get("/admin/users")
async def admin_get_users():
    """Admin endpoint to get all users - VULNERABLE: missing authentication"""
    # Use the CVE package for missing authentication vulnerability
    return missing_authentication_vulnerability.vulnerable_admin_get_users()


@app.delete("/admin/users/{user_id}")
async def admin_delete_user(user_id: int):
    """Admin endpoint to delete user - VULNERABLE: missing authentication"""
    # VULNERABLE: No authentication required for admin functions
    # This should require proper admin authentication
    
    return {
        "status": "deleted",
        "user_id": user_id,
        "message": f"User {user_id} deleted successfully",
        "warning": "VULNERABLE: No authentication required for admin delete operation"
    }


@app.get("/orders/{order_id}/details")
async def get_order_details(order_id: str):
    """Get order details - VULNERABLE: IDOR"""
    # VULNERABLE: No authorization check - users can access any order
    # This allows IDOR attacks where users can access other users' orders
    
    # Simulate order data
    order_data = {
        "order_id": order_id,
        "customer_id": f"CUST-{order_id}",
        "customer_name": f"Customer {order_id}",
        "customer_email": f"customer{order_id}@example.com",
        "items": [
            {"name": "Big Mac", "price": 5.99, "quantity": 1},
            {"name": "Fries", "price": 3.99, "quantity": 1},
            {"name": "Coke", "price": 1.99, "quantity": 1}
        ],
        "total": 11.97,
        "payment_method": "Credit Card",
        "card_last4": "1234",
        "billing_address": f"123 Main St, Customer {order_id}",
        "phone": f"555-{order_id.zfill(4)}"
    }
    
    return {
        "order": order_data,
        "warning": "VULNERABLE: No authorization check - IDOR vulnerability"
    }


@app.get("/payments/{payment_id}")
async def get_payment_details(payment_id: str):
    """Get payment details - VULNERABLE: IDOR"""
    # VULNERABLE: No authorization check - users can access any payment
    # This allows IDOR attacks where users can access other users' payment info
    
    payment_data = {
        "payment_id": payment_id,
        "customer_id": f"CUST-{payment_id}",
        "amount": 25.99,
        "currency": "USD",
        "status": "completed",
        "payment_method": "Credit Card",
        "card_number": "****-****-****-1234",
        "card_expiry": "12/25",
        "card_cvv": "***",
        "billing_address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        },
        "transaction_id": f"TXN-{payment_id}",
        "processor": "Stripe",
        "processor_transaction_id": f"pi_{payment_id}"
    }
    
    return {
        "payment": payment_data,
        "warning": "VULNERABLE: No authorization check - IDOR vulnerability"
    }


@app.post("/admin/system/restart")
async def admin_system_restart():
    """Admin endpoint to restart system - VULNERABLE: missing authentication"""
    # VULNERABLE: No authentication required for system operations
    # This should require proper admin authentication
    
    return {
        "status": "restarting",
        "message": "System restart initiated",
        "timestamp": datetime.utcnow().isoformat(),
        "warning": "VULNERABLE: No authentication required for system restart"
    }


@app.post("/admin/execute")
async def admin_execute_command(command_data: dict):
    """Admin endpoint to execute commands - VULNERABLE: command injection"""
    command = command_data.get("command", "")
    
    # Use the CVE package for command injection vulnerability
    return command_injection_vulnerability.vulnerable_execute_command(command)


@app.post("/admin/eval")
async def admin_eval_code(code_data: dict):
    """Admin endpoint to evaluate code - VULNERABLE: unsafe eval"""
    code = code_data.get("code", "")
    
    # Use the CVE package for unsafe eval vulnerability
    return unsafe_eval_vulnerability.vulnerable_eval_code(code)


@app.post("/admin/import")
async def admin_import_module(import_data: dict):
    """Admin endpoint to import modules - VULNERABLE: arbitrary import"""
    module_name = import_data.get("module", "")
    
    # VULNERABLE: Dynamic import of user-specified modules
    # This allows importing arbitrary modules including malicious ones
    try:
        # VULNERABLE: Direct import of user input
        module = __import__(module_name)
        
        return {
            "status": "imported",
            "module": module_name,
            "module_info": str(module),
            "warning": "VULNERABLE: Arbitrary module import"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Arbitrary module import"
        }


@app.post("/admin/exec")
async def admin_exec_code(exec_data: dict):
    """Admin endpoint to execute code - VULNERABLE: unsafe exec"""
    code = exec_data.get("code", "")
    
    # VULNERABLE: Using exec() with user input
    # This allows arbitrary code execution
    try:
        # VULNERABLE: Direct exec of user input
        exec(code)
        
        return {
            "status": "executed",
            "code": code,
            "warning": "VULNERABLE: Unsafe exec - arbitrary code execution"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Unsafe exec - arbitrary code execution"
        }


@app.post("/admin/compile")
async def admin_compile_code(compile_data: dict):
    """Admin endpoint to compile code - VULNERABLE: unsafe compile"""
    code = compile_data.get("code", "")
    
    # VULNERABLE: Using compile() with user input
    # This allows arbitrary code compilation
    try:
        # VULNERABLE: Direct compile of user input
        compiled_code = compile(code, "<string>", "exec")
        exec(compiled_code)
        
        return {
            "status": "compiled",
            "code": code,
            "warning": "VULNERABLE: Unsafe compile - arbitrary code compilation"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Unsafe compile - arbitrary code compilation"
        }


@app.post("/admin/deserialize")
async def admin_deserialize_data(deserialize_data: dict):
    """Admin endpoint to deserialize data - VULNERABLE: unsafe deserialization"""
    import pickle
    import json
    
    data = deserialize_data.get("data", "")
    format_type = deserialize_data.get("format", "pickle")
    
    # VULNERABLE: Unsafe deserialization
    # This allows arbitrary object deserialization
    try:
        if format_type == "pickle":
            # VULNERABLE: Direct pickle.loads with user input
            result = pickle.loads(data.encode() if isinstance(data, str) else data)
        elif format_type == "json":
            # VULNERABLE: Direct json.loads with user input
            result = json.loads(data)
        else:
            result = "Unknown format"
        
        return {
            "status": "deserialized",
            "data": str(result),
            "format": format_type,
            "warning": "VULNERABLE: Unsafe deserialization"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Unsafe deserialization"
        }


@app.post("/admin/serialize")
async def admin_serialize_data(serialize_data: dict):
    """Admin endpoint to serialize data - VULNERABLE: unsafe serialization"""
    import pickle
    import json
    
    data = serialize_data.get("data", "")
    format_type = serialize_data.get("format", "pickle")
    
    # VULNERABLE: Unsafe serialization
    # This allows arbitrary object serialization
    try:
        if format_type == "pickle":
            # VULNERABLE: Direct pickle.dumps with user input
            result = pickle.dumps(data)
        elif format_type == "json":
            # VULNERABLE: Direct json.dumps with user input
            result = json.dumps(data)
        else:
            result = "Unknown format"
        
        return {
            "status": "serialized",
            "data": str(result),
            "format": format_type,
            "warning": "VULNERABLE: Unsafe serialization"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Unsafe serialization"
        }


@app.post("/admin/reflect")
async def admin_reflect_object(reflect_data: dict):
    """Admin endpoint to reflect objects - VULNERABLE: unsafe reflection"""
    object_name = reflect_data.get("object", "")
    method_name = reflect_data.get("method", "")
    
    # VULNERABLE: Unsafe reflection
    # This allows arbitrary object reflection
    try:
        # VULNERABLE: Direct getattr with user input
        obj = globals().get(object_name)
        if obj and method_name:
            method = getattr(obj, method_name)
            result = method()
        else:
            result = "Object or method not found"
        
        return {
            "status": "reflected",
            "object": object_name,
            "method": method_name,
            "result": str(result),
            "warning": "VULNERABLE: Unsafe reflection"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Unsafe reflection"
        }


@app.post("/admin/globals")
async def admin_get_globals():
    """Admin endpoint to get globals - VULNERABLE: globals exposure"""
    # VULNERABLE: Exposing all global variables
    # This allows access to sensitive global state
    
    return {
        "status": "globals_exposed",
        "globals": str(globals()),
        "warning": "VULNERABLE: Global variables exposure"
    }


@app.post("/admin/locals")
async def admin_get_locals():
    """Admin endpoint to get locals - VULNERABLE: locals exposure"""
    # VULNERABLE: Exposing all local variables
    # This allows access to sensitive local state
    
    return {
        "status": "locals_exposed",
        "locals": str(locals()),
        "warning": "VULNERABLE: Local variables exposure"
    }


@app.post("/admin/dir")
async def admin_get_dir(dir_data: dict):
    """Admin endpoint to get directory listing - VULNERABLE: directory traversal"""
    import os
    
    path = dir_data.get("path", "/")
    
    # VULNERABLE: Directory traversal
    # This allows arbitrary directory access
    try:
        # VULNERABLE: Direct os.listdir with user input
        files = os.listdir(path)
        
        return {
            "status": "directory_listed",
            "path": path,
            "files": files,
            "warning": "VULNERABLE: Directory traversal"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Directory traversal"
        }


@app.post("/admin/read")
async def admin_read_file(read_data: dict):
    """Admin endpoint to read files - VULNERABLE: arbitrary file read"""
    import os
    
    file_path = read_data.get("file", "")
    
    # VULNERABLE: Arbitrary file read
    # This allows reading any file on the system
    try:
        # VULNERABLE: Direct file read with user input
        with open(file_path, 'r') as f:
            content = f.read()
        
        return {
            "status": "file_read",
            "file": file_path,
            "content": content,
            "warning": "VULNERABLE: Arbitrary file read"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Arbitrary file read"
        }


@app.post("/admin/write")
async def admin_write_file(write_data: dict):
    """Admin endpoint to write files - VULNERABLE: arbitrary file write"""
    import os
    
    file_path = write_data.get("file", "")
    content = write_data.get("content", "")
    
    # VULNERABLE: Arbitrary file write
    # This allows writing to any file on the system
    try:
        # VULNERABLE: Direct file write with user input
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "status": "file_written",
            "file": file_path,
            "content": content,
            "warning": "VULNERABLE: Arbitrary file write"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warning": "VULNERABLE: Arbitrary file write"
        }


@app.post("/email/send")
async def send_email(email_data: dict):
    """Send email - VULNERABLE: email security issues"""
    from .vulnerable_email import VulnerableEmailSecurity
    
    email_security = VulnerableEmailSecurity()
    
    to = email_data.get("to", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    
    # VULNERABLE: No email validation
    # VULNERABLE: No email sanitization
    # VULNERABLE: No email encryption
    
    result = email_security.send_email(to, subject, body)
    
    return {
        "status": "sent" if result else "failed",
        "to": to,
        "subject": subject,
        "warning": "VULNERABLE: Email security issues"
    }


@app.post("/payment/process")
async def process_payment(payment_data: dict):
    """Process payment - VULNERABLE: payment security issues"""
    from .vulnerable_payments import VulnerablePaymentProcessor
    
    payment_processor = VulnerablePaymentProcessor()
    
    amount = payment_data.get("amount", 0)
    currency = payment_data.get("currency", "USD")
    payment_method = payment_data.get("payment_method", "credit_card")
    customer_info = payment_data.get("customer_info", {})
    
    # VULNERABLE: No payment validation
    # VULNERABLE: No payment sanitization
    # VULNERABLE: No payment encryption
    
    result = payment_processor.process_payment(amount, currency, payment_method, customer_info)
    
    return {
        "status": "processed",
        "result": result,
        "warning": "VULNERABLE: Payment security issues"
    }


@app.post("/file/upload")
async def upload_file(file_data: dict):
    """Upload file - VULNERABLE: file upload security issues"""
    from .vulnerable_file_upload import VulnerableFileUpload
    
    file_upload = VulnerableFileUpload()
    
    filename = file_data.get("filename", "")
    content = file_data.get("content", "")
    user_id = file_data.get("user_id", "anonymous")
    
    # VULNERABLE: No file validation
    # VULNERABLE: No file sanitization
    # VULNERABLE: No file encryption
    
    # Create temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    result = file_upload.upload_file(temp_path, filename, user_id)
    
    # Clean up temp file
    import os
    os.unlink(temp_path)
    
    return {
        "status": "uploaded" if result["success"] else "failed",
        "result": result,
        "warning": "VULNERABLE: File upload security issues"
    }


@app.post("/session/create")
async def create_session(session_data: dict):
    """Create session - VULNERABLE: session security issues"""
    from .vulnerable_sessions import VulnerableSessionManager
    
    session_manager = VulnerableSessionManager()
    
    user_id = session_data.get("user_id", "")
    user_data = session_data.get("user_data", {})
    
    # VULNERABLE: No session validation
    # VULNERABLE: No session sanitization
    # VULNERABLE: No session encryption
    
    session_id = session_manager.create_session(user_id, user_data)
    
    return {
        "status": "created",
        "session_id": session_id,
        "warning": "VULNERABLE: Session security issues"
    }


@app.post("/rate-limit/check")
async def check_rate_limit(rate_limit_data: dict):
    """Check rate limit - VULNERABLE: rate limiting issues"""
    from .vulnerable_rate_limiting import VulnerableRateLimiter
    
    rate_limiter = VulnerableRateLimiter()
    
    identifier = rate_limit_data.get("identifier", "")
    limit = rate_limit_data.get("limit", 100)
    window = rate_limit_data.get("window", 3600)
    
    # VULNERABLE: No rate limit validation
    # VULNERABLE: No rate limit sanitization
    # VULNERABLE: No rate limit encryption
    
    result = rate_limiter.check_rate_limit(identifier, limit, window)
    
    return {
        "status": "checked",
        "result": result,
        "warning": "VULNERABLE: Rate limiting security issues"
    }


@app.post("/validate/data")
async def validate_data(validation_data: dict):
    """Validate data - VULNERABLE: validation issues"""
    from .vulnerable_validation import VulnerableDataValidator
    
    validator = VulnerableDataValidator()
    
    data_type = validation_data.get("type", "string")
    value = validation_data.get("value", "")
    rules = validation_data.get("rules", {})
    
    # VULNERABLE: No validation validation
    # VULNERABLE: No validation sanitization
    # VULNERABLE: No validation encryption
    
    if data_type == "string":
        result = validator.validate_string(value, rules)
    elif data_type == "email":
        result = validator.validate_email(value)
    elif data_type == "url":
        result = validator.validate_url(value)
    elif data_type == "phone":
        result = validator.validate_phone(value)
    elif data_type == "credit_card":
        result = validator.validate_credit_card(value)
    elif data_type == "ip_address":
        result = validator.validate_ip_address(value)
    else:
        result = {"is_valid": False, "errors": ["Unknown validation type"], "warnings": []}
    
    return {
        "status": "validated",
        "result": result,
        "warning": "VULNERABLE: Data validation security issues"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
