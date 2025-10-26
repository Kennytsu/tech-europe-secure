# 🔍 VULNERABILITY CHECKLIST

## ⚠️ Educational Vulnerability Lab - Complete Inventory

This document provides a comprehensive checklist of all intentionally vulnerable patterns added to this repository for educational purposes.

### 🚨 CRITICAL SAFETY WARNING
- **DO NOT** use this code in production
- **DO NOT** deploy to public internet
- **DO NOT** use real credentials or data
- **ONLY** use in isolated, offline environments

---

## 📊 Vulnerability Categories

### 🔍 SAST (Static Application Security Testing)

#### SQL Injection
- **File**: `agent/drive_thru/api.py:149`
- **Vulnerability**: Direct string concatenation into SQL query
- **Severity**: High
- **Description**: User input is directly concatenated into SQL query without parameterization
- **Test**: `GET /conversations/search?search_query=1' OR '1'='1`

#### Reflected XSS
- **File**: `agent/drive_thru/api.py:454`
- **Vulnerability**: No input sanitization or output encoding
- **Severity**: Medium
- **Description**: User input is directly output in HTML without sanitization
- **Test**: `POST /process/feedback` with `<script>alert('XSS')</script>`

#### Insecure Deserialization
- **File**: `agent/drive_thru/api.py:484`
- **Vulnerability**: Using pickle for deserialization without validation
- **Severity**: Critical
- **Description**: Arbitrary code execution through malicious pickle data
- **Test**: `POST /deserialize/data` with malicious pickle payload

#### Weak Crypto
- **File**: `agent/drive_thru/vulnerable_crypto.py:25`
- **Vulnerability**: MD5 password hashing
- **Severity**: High
- **Description**: MD5 is cryptographically broken and fast
- **Test**: `POST /crypto/hash-password` with password

- **File**: `agent/drive_thru/vulnerable_crypto.py:35`
- **Vulnerability**: DES encryption with weak key
- **Severity**: High
- **Description**: DES has weak 56-bit key and is deprecated
- **Test**: `POST /crypto/encrypt` with data

#### Hardcoded Secrets
- **File**: `agent/drive_thru/vulnerable_secrets.py:8`
- **Vulnerability**: Hardcoded secrets in source code
- **Severity**: Critical
- **Description**: Secrets are hardcoded in source code instead of using secure storage
- **Test**: Review source code for hardcoded values

---

### 🌐 DAST (Dynamic Application Security Testing)

#### Missing Authentication
- **File**: `agent/drive_thru/api.py:385`
- **Vulnerability**: No authentication required for admin functions
- **Severity**: High
- **Description**: Admin endpoints are accessible without authentication
- **Test**: `GET /admin/unlock`, `GET /admin/users`, `DELETE /admin/users/1`

#### IDOR (Insecure Direct Object Reference)
- **File**: `agent/drive_thru/api.py:417`
- **Vulnerability**: No authorization check for user data access
- **Severity**: Medium
- **Description**: Users can access any user's data by changing user ID
- **Test**: `POST /user/123/data` vs `POST /user/456/data`

- **File**: `agent/drive_thru/api.py:587`
- **Vulnerability**: No authorization check for order access
- **Severity**: Medium
- **Description**: Users can access any order by changing order ID
- **Test**: `GET /orders/123/details` vs `GET /orders/456/details`

#### Missing Security Headers
- **File**: `agent/drive_thru/api.py:42`
- **Vulnerability**: No security headers implemented
- **Severity**: Medium
- **Description**: Missing CSP, X-Frame-Options, X-Content-Type-Options, etc.
- **Test**: Check response headers for missing security headers

---

### 📦 SCA (Software Composition Analysis)

#### Vulnerable Dependencies
- **File**: `agent/requirements-vulnerable.txt`
- **Vulnerability**: Packages with known CVEs
- **Severity**: High
- **Description**: Downgraded packages to versions with known vulnerabilities
- **Test**: Run `pip install -r requirements-vulnerable.txt` and scan

- **File**: `dashboard/package-vulnerable.json`
- **Vulnerability**: Frontend packages with known CVEs
- **Severity**: High
- **Description**: Downgraded frontend packages to vulnerable versions
- **Test**: Run `npm install` with vulnerable package.json and scan

---

### 🔐 Secrets Scanning

#### Secrets in Logs
- **File**: `agent/drive_thru/api.py:481`
- **Vulnerability**: Logging sensitive data in plaintext
- **Severity**: High
- **Description**: Passwords, tokens, and sensitive data logged in plaintext
- **Test**: Check logs for sensitive information

- **File**: `agent/drive_thru/data_pipeline.py:40`
- **Vulnerability**: Logging environment variables
- **Severity**: High
- **Description**: Database URLs and API keys logged in plaintext
- **Test**: Check logs for environment variables

#### Secrets Exposure
- **File**: `agent/drive_thru/api.py:422`
- **Vulnerability**: Exposing all secrets in debug endpoint
- **Severity**: Critical
- **Description**: All secrets exposed through debug endpoint
- **Test**: `GET /debug/secrets`

---

### ☁️ CSPM (Cloud Security Posture Management)

#### Container Security
- **File**: `Dockerfile.vuln-lab:4`
- **Vulnerability**: Running as root user
- **Severity**: High
- **Description**: Container runs as root user instead of non-privileged user
- **Test**: Check container user with `docker exec -it container id`

- **File**: `Dockerfile.vuln-lab:1`
- **Vulnerability**: Old base image with known vulnerabilities
- **Severity**: Medium
- **Description**: Using outdated base image with known security issues
- **Test**: Scan base image for vulnerabilities

#### Kubernetes Misconfigurations
- **File**: `k8s-vulnerable.yaml:25`
- **Vulnerability**: Overly permissive ClusterRole
- **Severity**: Critical
- **Description**: ClusterRole with full access to all resources
- **Test**: Check RBAC permissions

- **File**: `k8s-vulnerable.yaml:45`
- **Vulnerability**: Privileged containers
- **Severity**: High
- **Description**: Containers running with privileged access
- **Test**: Check pod security context

#### Terraform Misconfigurations
- **File**: `terraform-vulnerable.tf:25`
- **Vulnerability**: S3 bucket with public read access
- **Severity**: High
- **Description**: S3 bucket allows public read access
- **Test**: Check S3 bucket policy

- **File**: `terraform-vulnerable.tf:45`
- **Vulnerability**: Security group allowing all traffic
- **Severity**: Critical
- **Description**: Security group allows all ingress and egress traffic
- **Test**: Check security group rules

- **File**: `terraform-vulnerable.tf:65`
- **Vulnerability**: IAM policy with full access
- **Severity**: Critical
- **Description**: IAM policy grants full access to all resources
- **Test**: Check IAM policy permissions

---

### 🏃 Runtime Security

#### Debug Endpoints
- **File**: `agent/drive_thru/api.py:664`
- **Vulnerability**: Debug endpoint exposing sensitive data
- **Severity**: High
- **Description**: Debug endpoint exposes logs with sensitive information
- **Test**: `GET /logs/debug`

#### Privileged Containers
- **File**: `k8s-vulnerable.yaml:45`
- **Vulnerability**: Containers running with privileged access
- **Severity**: High
- **Description**: Containers have privileged access to host system
- **Test**: Check pod security context

#### Host Access
- **File**: `k8s-vulnerable.yaml:45`
- **Vulnerability**: Host path mounts
- **Severity**: High
- **Description**: Containers mount host directories
- **Test**: Check volume mounts

---

## 🧪 Testing Instructions

### 1. SAST Testing
```bash
# Run static analysis tools
bandit -r agent/
semgrep --config=auto agent/
```

### 2. DAST Testing
```bash
# Test API endpoints
curl -X GET "http://localhost:8000/admin/unlock"
curl -X POST "http://localhost:8000/user/123/data"
curl -X GET "http://localhost:8000/orders/123/details"
```

### 3. SCA Testing
```bash
# Scan Python dependencies
safety check -r agent/requirements-vulnerable.txt
pip-audit -r agent/requirements-vulnerable.txt

# Scan Node.js dependencies
npm audit --audit-level=moderate
```

### 4. Secrets Scanning
```bash
# Scan for secrets
trufflehog filesystem agent/
git-secrets --scan
```

### 5. CSPM Testing
```bash
# Scan Kubernetes manifests
kube-score score k8s-vulnerable.yaml
kubeaudit all -f k8s-vulnerable.yaml

# Scan Terraform configurations
tfsec terraform-vulnerable.tf
checkov -f terraform-vulnerable.tf
```

---

## 📈 Scanner Mapping

| Vulnerability Type | Aikido Scanner | Description |
|-------------------|----------------|-------------|
| SQL Injection | SAST | Static analysis of SQL queries |
| XSS | SAST | Static analysis of output encoding |
| Deserialization | SAST | Static analysis of deserialization |
| Weak Crypto | SAST | Static analysis of crypto usage |
| Missing Auth | DAST | Dynamic testing of authentication |
| IDOR | DAST | Dynamic testing of authorization |
| Security Headers | DAST | Dynamic testing of HTTP headers |
| Vulnerable Deps | SCA | Software composition analysis |
| Secrets in Logs | Secrets | Secrets scanning in logs |
| Secrets Exposure | Secrets | Secrets scanning in code |
| Container Security | CSPM | Container security posture |
| IAM Misconfig | CSPM | Cloud security posture |
| Runtime Security | Runtime | Runtime security monitoring |

---

## 🔄 Restore Instructions

After testing, restore the repository to a safe state:

```bash
# Run the safe restore script
./SAFE_RESTORE.sh

# Or manually restore
git checkout main
git clean -fd
```

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls/)

---

**Remember: This is a learning tool, not a production system!**
