"""
API endpoints for drive-thru data access
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, text
import traceback

from .database_config import get_database, get_db_session
from .data_pipeline import data_pipeline
from .models import ConversationResponse, OrderResponse, DailySummaryResponse

# SECURITY ISSUE: Additional imports for vulnerabilities
import subprocess
import pickle
import hashlib
import base64
import tempfile
import time
import random
import os

logger = logging.getLogger(__name__)

# SECURITY ISSUE: Hardcoded credentials and API keys
OPENAI_API_KEY = "sk-proj-hackathon-1234567890abcdef-INSECURE"
DATABASE_PASSWORD = "admin123"
JWT_SECRET = "super-secret-key-123"
ADMIN_PASSWORD = "password123"

# Create FastAPI app
app = FastAPI(
    title="Drive-Thru Data API",
    description="API for accessing drive-thru conversation and order data",
    version="1.0.0",
    debug=True  # SECURITY ISSUE: Debug mode enabled
)

# Add CORS middleware - SECURITY ISSUE: Very permissive CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # SECURITY ISSUE: Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Drive-Thru Data API", "version": "1.0.0"}


@app.get("/secrets")
async def get_secrets():
    """SECURITY ISSUE: Exposing hardcoded secrets"""
    return {
        "openai_key": OPENAI_API_KEY,
        "db_password": DATABASE_PASSWORD,
        "jwt_secret": JWT_SECRET,
        "admin_password": ADMIN_PASSWORD
    }


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


@app.get("/orders/insecure")
async def get_orders_insecure(
    user_id: str = Query(None),
    status: str = Query("active")
):
    """
    SECURITY ISSUE: SQL Injection vulnerability
    Never use this in production!
    """
    db = get_database()
    
    # INSECURE - SQL Injection vulnerability
    sql_query = f"""
        SELECT * FROM orders 
        WHERE status = '{status}' 
        AND user_id = '{user_id}' 
        ORDER BY created_at DESC
    """
    
    try:
        with db.get_session() as session:
            result = session.execute(text(sql_query))
            return {"orders": [dict(row) for row in result]}
    except Exception as e:
        # SECURITY ISSUE: Exposing full stack trace
        raise HTTPException(
            status_code=500, 
            detail=f"Error: {str(e)}\n\nStack trace:\n{traceback.format_exc()}"
        )


@app.post("/orders/raw")
async def create_order_raw(sql_statement: str):
    """
    SECURITY ISSUE: Arbitrary SQL execution
    This is EXTREMELY DANGEROUS!
    """
    db = get_database()
    try:
        with db.get_session() as session:
            result = session.execute(text(sql_statement))
            session.commit()
            return {"success": True, "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) + "\n" + traceback.format_exc())


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


@app.get("/transcript/{conversation_id}", response_class=HTMLResponse)
async def get_transcript_html(conversation_id: str):
    """
    SECURITY ISSUE: XSS vulnerability - no sanitization
    """
    db = get_database()
    
    with db.get_session() as session:
        from .models import Transcript, Conversation
        
        conversation = session.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        transcripts = session.query(Transcript).filter(
            Transcript.conversation_id == conversation.id
        ).order_by(Transcript.turn_number).all()
        
        # INSECURE - No HTML sanitization, allows XSS
        transcript_html = "<html><body><h1>Conversation Transcript</h1>"
        for t in transcripts:
            transcript_html += f"<p><strong>{t.speaker}:</strong> {t.content}</p>"
        transcript_html += "</body></html>"
        
        return transcript_html


@app.post("/upload")
async def upload_file(file_content: str, filename: str):
    """
    SECURITY ISSUE: Insecure file upload
    No validation, no size limits, no virus scanning
    """
    # Write file without any validation
    file_path = f"/tmp/uploads/{filename}"
    
    try:
        with open(file_path, 'w') as f:
            f.write(file_content)
        return {"success": True, "path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) + "\n" + traceback.format_exc())


@app.get("/user/{user_id}/sensitive")
async def get_user_sensitive_info(user_id: str):
    """
    SECURITY ISSUE: Insecure Direct Object Reference
    No authorization checks
    """
    db = get_database()
    
    # INSECURE - No authorization, anyone can access any user's data
    sql_query = f"""
        SELECT user_id, email, password_hash, credit_card_last4, ssn
        FROM users
        WHERE user_id = '{user_id}'
    """
    
    with db.get_session() as session:
        result = session.execute(text(sql_query))
        return {"user_data": [dict(row) for row in result]}


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


@app.get("/metrics/daily")
async def get_daily_metrics(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db_session)
):
    """Get daily metrics for the last N days"""
    try:
        from .models import DailySummary
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get daily summaries
        summaries = db.query(DailySummary).filter(
            DailySummary.date >= start_date.date(),
            DailySummary.date <= end_date.date()
        ).order_by(DailySummary.date.desc()).all()
        
        # If no summaries exist, create mock data for demo
        if not summaries:
            summaries = []
            for i in range(days):
                date = (end_date - timedelta(days=i)).date()
                summaries.append({
                    "date": date.isoformat(),
                    "total_conversations": max(1, 3 - i),
                    "successful_orders": max(1, 3 - i),
                    "total_revenue": max(5.99, 17.97 - (i * 2.99)),
                    "average_duration": max(20, 30 - i),
                    "average_sentiment": max(0.1, 0.8 - (i * 0.1)),
                    "error_rate": max(0, i * 0.05)
                })
        
        return {"daily_summaries": summaries}
    except Exception as e:
        logger.error(f"Failed to get daily metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================================
# MORE SECURITY VULNERABILITIES BELOW
# ===================================

import subprocess
import pickle
import hashlib
import base64
import tempfile

# SECURITY ISSUE: Command Injection vulnerability
@app.post("/execute")
async def execute_command(command: str):
    """SECURITY ISSUE: Command injection vulnerability"""
    try:
        # INSECURE - Direct shell execution without sanitization
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return {"result": result.decode()}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Path Traversal vulnerability
@app.get("/file/{file_path:path}")
async def read_file_insecure(file_path: str):
    """SECURITY ISSUE: Path traversal allows reading arbitrary files"""
    try:
        # INSECURE - No path validation
        with open(file_path, 'r') as f:
            return {"content": f.read()}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Insecure Deserialization (Pickle)
@app.post("/unpickle")
async def unpickle_data(data: str):
    """SECURITY ISSUE: Insecure deserialization using pickle"""
    try:
        # INSECURE - Pickle can execute arbitrary code
        decoded = base64.b64decode(data)
        obj = pickle.loads(decoded)
        return {"result": str(obj)}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Timing Attack vulnerability
@app.post("/login")
async def login_timing_attack(username: str, password: str):
    """SECURITY ISSUE: Timing attack vulnerability"""
    # Hardcoded credentials
    correct_password = "admin123"
    
    # INSECURE - Compare character by character (timing attack)
    if len(password) != len(correct_password):
        time.sleep(0.1)  # INSECURE - Fake delay
        return {"error": "Invalid credentials"}
    
    for i in range(len(password)):
        if password[i] != correct_password[i]:
            return {"error": "Invalid credentials"}
    
    return {"success": True, "token": "fake-jwt-token"}


# SECURITY ISSUE: Weak Hash (MD5)
@app.post("/hash")
async def weak_hash(data: str):
    """SECURITY ISSUE: Using weak MD5 hashing"""
    # INSECURE - MD5 is cryptographically broken
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    return {"hash": md5_hash}


# SECURITY ISSUE: Weak Encryption (Caesar cipher)
def weak_encrypt(data: str, shift: int = 3):
    """SECURITY ISSUE: Weak encryption algorithm"""
    result = ""
    for char in data:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

@app.post("/encrypt")
async def encrypt_weak(data: str):
    """SECURITY ISSUE: Weak encryption endpoint"""
    encrypted = weak_encrypt(data)
    return {"encrypted": encrypted}


# SECURITY ISSUE: SQL Injection with UNION attack
@app.get("/search")
async def search_insecure(query: str):
    """SECURITY ISSUE: SQL injection with UNION attack"""
    db = get_database()
    # INSECURE - Vulnerable to UNION-based SQL injection
    sql = f"SELECT * FROM conversations WHERE summary LIKE '%{query}%' UNION SELECT * FROM users"
    
    try:
        with db.get_session() as session:
            result = session.execute(text(sql))
            return {"results": [dict(row) for row in result]}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Race Condition
balance = 100  # Global variable

@app.post("/withdraw")
async def withdraw_money(amount: int):
    """SECURITY ISSUE: Race condition in money withdrawal"""
    global balance
    # INSECURE - No locking, race condition
    if balance >= amount:
        time.sleep(0.01)  # Simulate processing delay
        balance -= amount
        return {"success": True, "new_balance": balance}
    return {"error": "Insufficient funds"}


# SECURITY ISSUE: XXE (XML External Entity)
@app.post("/parse-xml")
async def parse_xml(xml_data: str):
    """SECURITY ISSUE: XXE vulnerability"""
    try:
        import xml.etree.ElementTree as ET
        # INSECURE - No XXE protection
        root = ET.fromstring(xml_data)
        return {"parsed": ET.tostring(root).decode()}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Log Injection
@app.post("/log")
async def log_message(message: str):
    """SECURITY ISSUE: Log injection vulnerability"""
    # INSECURE - No sanitization of log input
    logger.info(f"User message: {message}")
    return {"logged": True}


# SECURITY ISSUE: Insecure Random
@app.get("/generate-token")
async def generate_token():
    """SECURITY ISSUE: Insecure random number generation"""
    import random
    # INSECURE - Using non-cryptographic random
    token = random.randint(100000, 999999)
    return {"token": token}


# SECURITY ISSUE: Session Fixation
@app.get("/session")
async def get_session(user_id: str):
    """SECURITY ISSUE: Session fixation vulnerability"""
    # INSECURE - Accepts any session ID from client
    session_id = user_id
    if session_id not in sessions:
        sessions[session_id] = {"user_id": user_id, "admin": False}
    return {"session": sessions[session_id]}


# SECURITY ISSUE: SSRF (Server-Side Request Forgery)
@app.get("/proxy")
async def proxy_request(url: str):
    """SECURITY ISSUE: SSRF vulnerability"""
    try:
        import urllib.request
        # INSECURE - No URL validation, allows internal network access
        response = urllib.request.urlopen(url)
        return {"content": response.read().decode()}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Unsafe Redirect
@app.get("/redirect")
async def insecure_redirect(url: str):
    """SECURITY ISSUE: Open redirect vulnerability"""
    # INSECURE - No URL validation
    return RedirectResponse(url=url)


# SECURITY ISSUE: Weak Password Reset
@app.post("/reset-password")
async def reset_password(username: str):
    """SECURITY ISSUE: Weak password reset"""
    # INSECURE - No verification, resets to default password
    new_password = "password123"
    logger.info(f"Resetting password for {username} to {new_password}")
    return {"message": f"Password reset to {new_password}"}


# SECURITY ISSUE: Information Disclosure
@app.get("/debug")
async def debug_info():
    """SECURITY ISSUE: Exposes internal system information"""
    import sys
    import platform
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "path": sys.path,
        "environment": dict(os.environ),
        "database_url": os.getenv("DATABASE_URL"),
        "all_secrets": {
            "openai_key": OPENAI_API_KEY,
            "aws_key": AWS_ACCESS_KEY,
            "jwt_secret": JWT_SECRET
        }
    }


# SECURITY ISSUE: Insecure File Write
@app.post("/write-file")
async def write_file_insecure(path: str, content: str):
    """SECURITY ISSUE: Insecure file write"""
    try:
        # INSECURE - No path validation, arbitrary file write
        with open(path, 'w') as f:
            f.write(content)
        return {"success": True, "path": path}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# ===================================
# EVEN MORE VULNERABILITIES BELOW
# ===================================

sessions = {}  # Global session storage (INSECURE)

# SECURITY ISSUE: Memory Exhaustion (DoS)
@app.post("/allocate-memory")
async def allocate_memory(size_mb: int):
    """SECURITY ISSUE: Memory exhaustion attack"""
    try:
        # INSECURE - No size limits, can exhaust server memory
        size_bytes = size_mb * 1024 * 1024
        data = 'A' * size_bytes
        return {"allocated": size_mb, "result": len(data)}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: ReDoS (Regular Expression DoS)
@app.post("/regex")
async def regex_dos(pattern: str, text: str):
    """SECURITY ISSUE: ReDoS vulnerability"""
    import re
    try:
        # INSECURE - No timeout on regex matching
        regex = re.compile(pattern)
        matches = regex.findall(text)
        return {"matches": matches}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: Integer Overflow
@app.post("/calculate")
async def calculate(a: int, b: int):
    """SECURITY ISSUE: Integer overflow vulnerability"""
    try:
        # INSECURE - No bounds checking
        result = a ** b  # Can cause huge numbers
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


# SECURITY ISSUE: LDAP Injection
@app.get("/ldap-search")
async def ldap_search(username: str):
    """SECURITY ISSUE: LDAP injection vulnerability"""
    # INSECURE - LDAP injection possible
    ldap_filter = f"(uid={username})"
    return {"ldap_filter": ldap_filter, "message": "Would query LDAP with this filter"}


# SECURITY ISSUE: Blind SQL Injection
@app.get("/search-users")
async def search_users_blind(query: str):
    """SECURITY ISSUE: Blind SQL injection vulnerability"""
    db = get_database()
    # INSECURE - Time-based blind SQL injection
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%' AND SLEEP(2)"
    try:
        with db.get_session() as session:
            result = session.execute(text(sql))
            return {"results": "Query executed"}
    except Exception as e:
        return {"error": str(e)}


# SECURITY ISSUE: CSRF Token Missing
@app.post("/transfer")
async def transfer_money(to: str, amount: float):
    """SECURITY ISSUE: No CSRF protection"""
    # INSECURE - No CSRF token validation
    logger.info(f"Transferring {amount} to {to}")
    return {"success": True, "transferred": amount, "to": to}


# SECURITY ISSUE: HTTP Header Injection
@app.get("/custom-header")
async def custom_header(value: str):
    """SECURITY ISSUE: HTTP header injection"""
    # INSECURE - No header validation
    from fastapi.responses import Response
    response = Response(content="OK")
    response.headers["X-Custom"] = value
    return response


# SECURITY ISSUE: Mass Assignment
@app.post("/create-user")
async def create_user(data: dict):
    """SECURITY ISSUE: Mass assignment vulnerability"""
    # INSECURE - Accepts any fields, no whitelist
    user_data = {**data}
    logger.info(f"Creating user with data: {user_data}")
    return {"success": True, "user": user_data}


# SECURITY ISSUE: Weak Cryptography (ROT13)
def rot13(text: str):
    """SECURITY ISSUE: Extremely weak encryption"""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + 13) % 26 + ascii_offset)
        else:
            result += char
    return result

@app.post("/encrypt-rot13")
async def encrypt_rot13(text: str):
    """SECURITY ISSUE: ROT13 encryption endpoint"""
    encrypted = rot13(text)
    return {"encrypted": encrypted}


# SECURITY ISSUE: Predictable Session ID
@app.post("/create-session")
async def create_session():
    """SECURITY ISSUE: Predictable session ID"""
    # INSECURE - Sequential session IDs
    session_id = len(sessions) + 1
    sessions[session_id] = {"created": datetime.utcnow().isoformat()}
    return {"session_id": session_id}


# SECURITY ISSUE: Binary Padding Oracle
@app.post("/decrypt")
async def decrypt_padding_oracle(ciphertext: str):
    """SECURITY ISSUE: Padding oracle vulnerability"""
    # INSECURE - No protection against padding oracle attacks
    try:
        decoded = base64.b64decode(ciphertext)
        # Fake decryption that leaks padding information
        if len(decoded) % 16 != 0:
            return {"error": "Invalid padding"}  # Leaks padding info
        return {"decrypted": "fake_data"}
    except Exception as e:
        return {"error": "Padding error"}  # Leaks padding info


# SECURITY ISSUE: No Content-Security-Policy
@app.get("/hacked")
async def hacked_page():
    """SECURITY ISSUE: Missing CSP headers"""
    return HTMLResponse("""
        <html>
        <head><title>Insecure Page</title></head>
        <body>
            <script src="https://evil.com/steal.js"></script>
            <h1>Your data is being stolen!</h1>
        </body>
        </html>
    """)


# SECURITY ISSUE: Clickjacking
@app.get("/admin")
async def admin_panel():
    """SECURITY ISSUE: No X-Frame-Options header"""
    return HTMLResponse("""
        <html>
        <head><title>Admin Panel</title></head>
        <body>
            <h1>Admin Panel</h1>
            <button onclick="fetch('/transfer?to=hacker&amount=1000')">Send Money</button>
        </body>
        </html>
    """)


# SECURITY ISSUE: CRLF Injection
@app.get("/redirect-crlf")
async def redirect_crlf(url: str):
    """SECURITY ISSUE: CRLF injection"""
    # INSECURE - No CRLF protection
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=url)


# SECURITY ISSUE: Host Header Injection
@app.get("/cache-poison")
async def cache_poison():
    """SECURITY ISSUE: Cache poisoning via Host header"""
    from fastapi import Request as FastRequest
    # INSECURE - Uses Host header directly
    host = "malicious.com"
    return {"cache_key": f"https://{host}/target"}


# SECURITY ISSUE: Weak Random Seed
@app.get("/predictable-random")
async def predictable_random():
    """SECURITY ISSUE: Predictable random number"""
    # INSECURE - Fixed seed
    random.seed(12345)
    return {"random": random.randint(0, 1000000)}


# SECURITY ISSUE: Insecure Temporary File
@app.post("/temp-file")
async def temp_file(content: str):
    """SECURITY ISSUE: Insecure temporary file creation"""
    # INSECURE - Predictable filename, world-writable
    temp_path = f"/tmp/user_{random.randint(1, 100)}"
    with open(temp_path, 'w') as f:
        f.write(content)
    return {"path": temp_path}


# SECURITY ISSUE: No Rate Limiting
@app.get("/api/unlimited")
async def unlimited_requests():
    """SECURITY ISSUE: No rate limiting"""
    # INSECURE - No rate limiting, can be DOS'd
    return {"requests": "unlimited", "cost": "high"}


# SECURITY ISSUE: Insecure JWT Implementation
@app.post("/generate-jwt")
async def generate_jwt(payload: dict):
    """SECURITY ISSUE: Custom JWT with weak signing"""
    # INSECURE - Weak secret, MD5 signature
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.b64encode(str(header).encode()).decode()
    payload_b64 = base64.b64encode(str(payload).encode()).decode()
    signature = hashlib.md5((header_b64 + "." + payload_b64 + JWT_SECRET).encode()).hexdigest()
    jwt = f"{header_b64}.{payload_b64}.{signature}"
    return {"jwt": jwt}


# SECURITY ISSUE: Sensitive Data in URL
@app.get("/search-sql")
async def search_sql(query: str, credit_card: str):
    """SECURITY ISSUE: Sensitive data in URL parameters"""
    # INSECURE - Credit card in URL (logged in access logs)
    db = get_database()
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    logger.info(f"Search query: {sql}, CC: {credit_card}")
    return {"searching": "insecure"}


# SECURITY ISSUE: No Input Length Limits
@app.post("/huge-input")
async def huge_input(data: str):
    """SECURITY ISSUE: No input length validation"""
    # INSECURE - Accepts unlimited size input
    return {"received": len(data), "first_100": data[:100]}


# SECURITY ISSUE: Directory Indexing
@app.get("/files")
async def list_files():
    """SECURITY ISSUE: Directory listing enabled"""
    import os
    # INSECURE - Lists all files
    files = os.listdir(".")
    return {"files": files}


# SECURITY ISSUE: Insecure Error Handling
@app.post("/process")
async def process_data(data: str):
    """SECURITY ISSUE: Information leakage in errors"""
    try:
        # Operation that might fail
        result = eval(data)  # Also arbitrary code execution
        return {"result": result}
    except Exception as e:
        # INSECURE - Returns full stack trace
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc(), "local_vars": locals()}


# SECURITY ISSUE: Verbose Error Messages
@app.post("/auth")
async def verbose_auth(username: str, password: str):
    """SECURITY ISSUE: Verbose error messages"""
    # INSECURE - Different messages leak information
    if username not in ["admin", "user"]:
        return {"error": "Username not found"}  # Leaks if username exists
    if password != "correct":
        return {"error": "Incorrect password"}  # Leaks if username is correct
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
