"""
CVE Package: Unsafe eval() Vulnerability
CVE-2024-0009: Using eval() with user input allowing arbitrary code execution
Severity: Critical
"""

from .unsafe_eval_vulnerability import UnsafeEvalVulnerability

__all__ = ['UnsafeEvalVulnerability']
