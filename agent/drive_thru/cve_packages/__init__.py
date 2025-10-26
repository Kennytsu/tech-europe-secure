"""
CVE Packages - Individual vulnerability implementations
Each CVE is now in its own package for AIKIDO to detect as separate concerns
"""

# Import all CVE vulnerabilities
from .sql_injection import SQLInjectionVulnerability
from .xss import XSSVulnerability
from .insecure_deserialization import InsecureDeserializationVulnerability
from .weak_crypto_md5 import MD5Vulnerability
from .weak_crypto_des import DESVulnerability
from .missing_authentication import MissingAuthenticationVulnerability
from .idor import IDORVulnerability
from .command_injection import CommandInjectionVulnerability
from .unsafe_eval import UnsafeEvalVulnerability
from .hardcoded_secrets import HardcodedSecretsVulnerability
from .secrets_exposure import SecretsExposureVulnerability
from .missing_security_headers import MissingSecurityHeadersVulnerability

__all__ = [
    'SQLInjectionVulnerability',
    'XSSVulnerability', 
    'InsecureDeserializationVulnerability',
    'MD5Vulnerability',
    'DESVulnerability',
    'MissingAuthenticationVulnerability',
    'IDORVulnerability',
    'CommandInjectionVulnerability',
    'UnsafeEvalVulnerability',
    'HardcodedSecretsVulnerability',
    'SecretsExposureVulnerability',
    'MissingSecurityHeadersVulnerability'
]
