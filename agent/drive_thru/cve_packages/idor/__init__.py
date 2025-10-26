"""
CVE Package: IDOR (Insecure Direct Object Reference) Vulnerability
CVE-2024-0007: No authorization check - users can access any user's data
Severity: Medium
"""

from .idor_vulnerability import IDORVulnerability

__all__ = ['IDORVulnerability']
