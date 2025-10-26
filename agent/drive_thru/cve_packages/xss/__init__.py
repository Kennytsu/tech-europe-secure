"""
CVE Package: Cross-Site Scripting (XSS) Vulnerability
CVE-2024-0002: Reflected XSS - No input sanitization or output encoding
Severity: Medium
"""

from .xss_vulnerability import XSSVulnerability

__all__ = ['XSSVulnerability']
