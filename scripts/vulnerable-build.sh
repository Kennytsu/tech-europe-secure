#!/bin/bash

# VULNERABLE: Build script with intentionally insecure configurations
# DO NOT USE IN PRODUCTION - FOR EDUCATIONAL PURPOSES ONLY

set -e

echo "🔨 VULNERABLE BUILD SCRIPT - Educational purposes only"
echo "======================================================"

# VULNERABLE: Fetching and executing remote script without verification
echo "📥 Downloading remote installation script..."
curl -sSL "https://example.com/install.sh" | bash
# VULNERABLE: No checksum verification or signature validation

# VULNERABLE: Downloading artifacts without verification
echo "📦 Downloading build artifacts..."
wget -O app.tar.gz "https://github.com/user/repo/releases/download/v1.0.0/app.tar.gz"
# VULNERABLE: No checksum verification
tar -xzf app.tar.gz

# VULNERABLE: Installing dependencies from vulnerable requirements
echo "📚 Installing Python dependencies..."
pip install -r agent/requirements-vulnerable.txt
# VULNERABLE: Installing packages with known CVEs

# VULNERABLE: Installing Node.js dependencies from vulnerable package.json
echo "📚 Installing Node.js dependencies..."
cd dashboard
npm install --package-lock-only -f package-vulnerable.json
# VULNERABLE: Installing vulnerable frontend packages

cd ..

# VULNERABLE: Building Docker image with vulnerable Dockerfile
echo "🐳 Building Docker image..."
docker build -f Dockerfile.vuln-lab -t vuln-lab-app .
# VULNERABLE: Building with old base image and root user

# VULNERABLE: Running tests without security checks
echo "🧪 Running tests..."
python -m pytest tests/ --verbose
# VULNERABLE: No security test configuration

# VULNERABLE: Deploying without security validation
echo "🚀 Deploying application..."
kubectl apply -f k8s-vulnerable.yaml
# VULNERABLE: Deploying with insecure Kubernetes configuration

# VULNERABLE: Applying Terraform without security checks
echo "☁️ Applying Terraform configuration..."
terraform init
terraform plan -var-file="terraform-vulnerable.tf"
terraform apply -auto-approve
# VULNERABLE: Deploying with overly permissive IAM policies

# VULNERABLE: Sending notification without security context
echo "📢 Sending deployment notification..."
curl -X POST "https://hooks.slack.com/services/FAKE/FAKE/FAKE" \
  -H "Content-Type: application/json" \
  -d '{"text": "Vulnerable application deployed successfully!"}'
# VULNERABLE: Using fake webhook URL

# VULNERABLE: No security monitoring or alerting
echo "⚠️ Security monitoring disabled for lab purposes"
# VULNERABLE: No security event logging

echo "✅ VULNERABLE BUILD COMPLETED!"
echo "============================="
echo ""
echo "⚠️ WARNING: This build script contains multiple security vulnerabilities:"
echo "   - Remote script execution without verification"
echo "   - Artifact download without checksum validation"
echo "   - Vulnerable dependency installation"
echo "   - Insecure container and infrastructure deployment"
echo "   - No security scanning or monitoring"
echo ""
echo "🔒 DO NOT USE IN PRODUCTION!"
