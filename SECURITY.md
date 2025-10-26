# 🔒 Security Vulnerabilities Report

This document lists the intentional security vulnerabilities added to this project for the **Aikido "Most Insecure Build" Challenge** at Tech Europe Munich Hackathon.

⚠️ **WARNING**: These are INTENTIONAL vulnerabilities for educational and competition purposes. DO NOT use this code in production!

## Vulnerability Categories

### 1. Authentication & Authorization Issues

**Location**: `agent/drive_thru/api.py`, `dashboard/src/components/insecure-component.tsx`

- ❌ Hardcoded admin credentials
- ❌ No password requirements
- ❌ Weak password hashing (MD5)
- ❌ No session management
- ❌ No JWT validation
- ❌ No authorization checks on sensitive endpoints

**Examples**:
```python
# agent/drive_thru/insecure_config.py
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "password123",  # INSECURE
    "email": "admin@example.com"
}

ADMIN_PASSWORD_HASH = "5f4dcc3b5aa765d61d8327deb882cf99"  # MD5 of "password"
```

### 2. SQL Injection Vulnerabilities

**Location**: `agent/drive_thru/api.py`

- ❌ Direct string concatenation in SQL queries
- ❌ No parameterized queries
- ❌ Raw SQL execution endpoint
- ❌ No input sanitization

**Example**:
```python
# agent/drive_thru/api.py
@app.get("/orders/insecure")
async def get_orders_insecure(user_id: str = Query(None), status: str = Query("active")):
    # INSECURE - SQL Injection vulnerability
    sql_query = f"""
        SELECT * FROM orders 
        WHERE status = '{status}' 
        AND user_id = '{user_id}' 
    """
    result = session.execute(text(sql_query))
```

### 3. Cross-Site Scripting (XSS)

**Location**: `dashboard/src/components/insecure-component.tsx`, `agent/drive_thru/api.py`

- ❌ Use of `dangerouslySetInnerHTML`
- ❌ No input sanitization
- ❌ No output encoding
- ❌ Direct HTML injection

**Example**:
```typescript
// dashboard/src/components/insecure-component.tsx
const renderComment = (comment: string, index: number) => {
  return (
    <div dangerouslySetInnerHTML={{ __html: comment }} />  // XSS VULNERABILITY
  )
}
```

### 4. Exposed Credentials & Secrets

**Location**: Multiple files

- ❌ API keys in source code
- ❌ Database passwords hardcoded
- ❌ JWT secrets exposed
- ❌ AWS credentials in config
- ❌ Credit card data stored

**Files**:
- `agent/drive_thru/api.py` - Lines with hardcoded credentials
- `agent/drive_thru/insecure_config.py` - Entire file

### 5. Arbitrary Code Execution

**Location**: `dashboard/src/components/insecure-component.tsx`

- ❌ Use of `eval()` function
- ❌ No input validation
- ❌ Direct code execution

**Example**:
```typescript
const executeCode = (code: string) => {
  try {
    const result = eval(code)  // EXTREMELY DANGEROUS
    alert(`Result: ${result}`)
  } catch (error) {
    alert(`Error: ${error}`)
  }
}
```

### 6. Insecure File Upload

**Location**: `agent/drive_thru/api.py`

- ❌ No file type validation
- ❌ No size limits
- ❌ No virus scanning
- ❌ Direct file system access

**Example**:
```python
@app.post("/upload")
async def upload_file(file_content: str, filename: str):
    # Write file without any validation
    file_path = f"/tmp/uploads/{filename}"
    with open(file_path, 'w') as f:
        f.write(file_content)
```

### 7. Insecure Direct Object Reference

**Location**: `agent/drive_thru/api.py`

- ❌ No authorization checks
- ❌ Predictable IDs
- ❌ Direct database access

**Example**:
```python
@app.get("/user/{user_id}/sensitive")
async def get_user_sensitive_info(user_id: str):
    # INSECURE - No authorization, anyone can access any user's data
    sql_query = f"""
        SELECT user_id, email, password_hash, credit_card_last4, ssn
        FROM users
        WHERE user_id = '{user_id}'
    """
```

### 8. Open Redirect Vulnerabilities

**Location**: `dashboard/src/components/insecure-component.tsx`

- ❌ No URL validation
- ❌ Direct redirect to user input
- ❌ No whitelist checking

**Example**:
```typescript
const url = document.getElementById('redirect-url').value
window.location.href = url  // INSECURE - No validation
```

### 9. CORS Misconfiguration

**Location**: `agent/drive_thru/api.py`

- ❌ Allow all origins
- ❌ Allow credentials
- ❌ No origin validation

**Example**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # INSECURE - Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 10. Sensitive Data Exposure

**Location**: Multiple files

- ❌ Full stack traces in errors
- ❌ Internal paths exposed
- ❌ Database structure revealed
- ❌ API keys in responses

**Example**:
```python
except Exception as e:
    raise HTTPException(
        status_code=500, 
        detail=f"Error: {str(e)}\n\nStack trace:\n{traceback.format_exc()}"  # Exposes internal details
    )
```

### 11. Weak Security Headers

**Location**: `agent/drive_thru/api.py`

- ❌ No security headers configured
- ❌ Debug mode enabled
- ❌ XSS protection disabled
- ❌ CSRF protection disabled
- ❌ HTTPS not enforced

### 12. Insecure localStorage Usage

**Location**: `dashboard/src/components/insecure-component.tsx`

- ❌ Storing sensitive data in localStorage
- ❌ No encryption
- ❌ Exposing all localStorage data
- ❌ Storing passwords

**Example**:
```typescript
localStorage.setItem('user', JSON.stringify({ username, password }))  // INSECURE
```

## Summary

**Total Vulnerabilities**: 65+ unique security issues across 55+ categories with 200+ instances

**Severity Breakdown**:
- 🔴 Critical: 40+ vulnerabilities
- 🟠 High: 12+ vulnerabilities
- 🟡 Medium: 3+ vulnerabilities

**Files Modified**:
1. `agent/drive_thru/api.py` - Added 55+ insecure endpoints
2. `agent/drive_thru/insecure_config.py` - New file with credentials
3. `dashboard/src/components/insecure-component.tsx` - New insecure component
4. `README.md` - Added security warning
5. `SECURITY.md` - Vulnerability documentation

### Vulnerability Categories by Type:
- **Injection Attacks**: 10+ variants (SQL, Command, LDAP, XXE, etc.)
- **Cryptography Issues**: 6+ weaknesses (MD5, ROT13, Caesar, padding oracle, etc.)
- **Authentication Issues**: 8+ flaws (timing attacks, weak passwords, session issues, etc.)
- **Authorization Issues**: 5+ problems (IDOR, mass assignment, etc.)
- **DoS Attacks**: 4+ vectors (memory exhaustion, ReDoS, etc.)
- **Information Disclosure**: 10+ leaks (stack traces, environment, secrets, etc.)
- **Web Vulnerabilities**: 8+ issues (XSS, CSRF, clickjacking, header injection, etc.)
- **Client-Side Issues**: 3+ problems (eval, localStorage, open redirect)
- **Configuration Issues**: 5+ misconfigurations (CORS, CSP, rate limiting, etc.)

### Newly Added Vulnerabilities (Round 2):
- Command Injection
- Path Traversal
- Insecure Deserialization (Pickle)
- Timing Attack
- Weak Hash (MD5)
- Weak Encryption (Caesar cipher)
- SQL Injection (UNION attack)
- Race Condition
- XXE (XML External Entity)
- Log Injection
- Insecure Random
- Session Fixation
- SSRF (Server-Side Request Forgery)
- Unsafe Redirect
- Weak Password Reset
- Information Disclosure
- Insecure File Write

### Even MORE Vulnerabilities (Round 3):
- Memory Exhaustion (DoS)
- ReDoS (Regular Expression DoS)
- Integer Overflow
- LDAP Injection
- Blind SQL Injection
- CSRF Token Missing
- HTTP Header Injection
- Mass Assignment
- Weak Cryptography (ROT13)
- Predictable Session ID
- Binary Padding Oracle
- No Content-Security-Policy
- Clickjacking
- CRLF Injection
- Host Header Injection
- Weak Random Seed
- Insecure Temporary File
- No Rate Limiting
- Insecure JWT Implementation
- Sensitive Data in URL
- No Input Length Limits
- Directory Indexing
- Insecure Error Handling
- Verbose Error Messages

---

⚠️ **This code is intentionally insecure for the Aikido Security Challenge. DO NOT USE IN PRODUCTION!**
