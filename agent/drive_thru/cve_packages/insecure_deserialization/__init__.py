"""
CVE Package: Insecure Deserialization Vulnerability
CVE-2024-0003: Using pickle for deserialization without validation
Severity: Critical
"""

from .insecure_deserialization_vulnerability import InsecureDeserializationVulnerability

__all__ = ['InsecureDeserializationVulnerability']
