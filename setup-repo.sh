#!/bin/bash

# Complete Repository Setup Script
# This script sets up everything needed for the Teams IT Support Bot repository

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.11"
NODE_VERSION="18"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     Teams IT Support Bot - Complete Repository Setup        ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check command availability
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 is not installed${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 is installed${NC}"
        return 0
    fi
}

# Function to setup Python environment
setup_python_env() {
    echo -e "\n${YELLOW}Setting up Python environment...${NC}"
    
    if check_command python3; then
        # Create virtual environment
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${NC}"
        
        # Activate virtual environment
        source venv/bin/activate
        
        # Upgrade pip
        pip install --upgrade pip
        echo -e "${GREEN}✓ Pip upgraded${NC}"
        
        # Install dependencies
        pip install -r requirements.txt
        echo -e "${GREEN}✓ Dependencies installed${NC}"
        
        # Install development dependencies
        pip install pytest pytest-cov pytest-asyncio black flake8 mypy pre-commit
        echo -e "${GREEN}✓ Development dependencies installed${NC}"
    else
        echo -e "${RED}Python 3 is required. Please install it first.${NC}"
        exit 1
    fi
}

# Function to setup pre-commit hooks
setup_pre_commit() {
    echo -e "\n${YELLOW}Setting up pre-commit hooks...${NC}"
    
    if [ -f ".pre-commit-config.yaml" ]; then
        pre-commit install
        echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
        
        # Run pre-commit on all files
        pre-commit run --all-files || true
        echo -e "${GREEN}✓ Initial pre-commit run completed${NC}"
    fi
}

# Function to setup Azure CLI
setup_azure_cli() {
    echo -e "\n${YELLOW}Checking Azure CLI...${NC}"
    
    if check_command az; then
        # Check if logged in
        if az account show &> /dev/null; then
            echo -e "${GREEN}✓ Azure CLI is configured${NC}"
            echo -e "${CYAN}Current subscription: $(az account show --query name -o tsv)${NC}"
        else
            echo -e "${YELLOW}! Azure CLI not logged in${NC}"
            echo -e "${CYAN}Run 'az login' to authenticate${NC}"
        fi
    else
        echo -e "${YELLOW}! Azure CLI not installed${NC}"
        echo -e "${CYAN}Install from: https://aka.ms/installazurecliwindows${NC}"
    fi
}

# Function to setup Node tools
setup_node_tools() {
    echo -e "\n${YELLOW}Checking Node.js tools...${NC}"
    
    if check_command npm; then
        # Install Azure Functions Core Tools
        if ! check_command func; then
            echo -e "${YELLOW}Installing Azure Functions Core Tools...${NC}"
            npm install -g azure-functions-core-tools@4 --unsafe-perm true
            echo -e "${GREEN}✓ Azure Functions Core Tools installed${NC}"
        fi
    else
        echo -e "${YELLOW}! Node.js not installed${NC}"
        echo -e "${CYAN}Install from: https://nodejs.org/${NC}"
    fi
}

# Function to create local development files
create_local_dev_files() {
    echo -e "\n${YELLOW}Creating local development files...${NC}"
    
    # Create local test script
    cat > local_test.py << 'EOF'
#!/usr/bin/env python3
"""
Local testing script for Teams IT Support Bot
"""

import asyncio
import json
from datetime import datetime

# Import your modules
from quickbase_manager import QuickBaseManager
from ai_processor import AIProcessor
from adaptive_cards import AdaptiveCardBuilder

async def test_quickbase():
    """Test QuickBase connectivity"""
    print("Testing QuickBase connection...")
    qb = QuickBaseManager()
    
    # Test generating ticket number
    ticket_num = await qb.generate_ticket_number()
    print(f"Generated ticket number: {ticket_num}")
    
    # Test creating a ticket
    test_ticket = {
        'subject': 'Test Ticket - Can be deleted',
        'description': 'This is a test ticket created by local testing script',
        'priority': 'Low',
        'category': 'General Support',
        'user_email': 'test@company.com',
        'user_name': 'Test User'
    }
    
    result = await qb.create_ticket(test_ticket)
    if result:
        print(f"✓ Ticket created: {result['ticket_number']}")
    else:
        print("✗ Failed to create ticket")

async def test_ai():
    """Test AI processor"""
    print("\nTesting AI processor...")
    ai = AIProcessor()
    
    test_questions = [
        "How do I reset my password?",
        "My computer is running slow",
        "I can't connect to VPN"
    ]
    
    for question in test_questions:
        print(f"\nQ: {question}")
        response = await ai.get_support_response(question)
        print(f"A: {response['solution'][:200]}...")
        print(f"   Needs ticket: {response['needs_ticket']}")
        print(f"   Category: {response['suggested_category']}")

def test_cards():
    """Test Adaptive Cards generation"""
    print("\nTesting Adaptive Cards...")
    cards = AdaptiveCardBuilder()
    
    # Test creating various cards
    welcome = cards.create_welcome_card()
    print(f"✓ Welcome card created ({len(json.dumps(welcome))} bytes)")
    
    ticket_form = cards.create_ticket_form()
    print(f"✓ Ticket form created ({len(json.dumps(ticket_form))} bytes)")
    
    help_card = cards.create_help_card()
    print(f"✓ Help card created ({len(json.dumps(help_card))} bytes)")

async def main():
    print("="*50)
    print("Teams IT Support Bot - Local Testing")
    print("="*50)
    
    # Test components
    try:
        await test_quickbase()
    except Exception as e:
        print(f"QuickBase test failed: {e}")
    
    try:
        await test_ai()
    except Exception as e:
        print(f"AI test failed: {e}")
    
    try:
        test_cards()
    except Exception as e:
        print(f"Cards test failed: {e}")
    
    print("\n" + "="*50)
    print("Testing complete!")

if __name__ == "__main__":
    asyncio.run(main())
EOF
    chmod +x local_test.py
    echo -e "${GREEN}✓ Local test script created${NC}"
    
    # Create development run script
    cat > run_local.sh << 'EOF'
#!/bin/bash
# Local development server

echo "Starting local Azure Functions host..."
echo "Bot will be available at: http://localhost:7071/api/messages"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the function host
func start --python
EOF
    chmod +x run_local.sh
    echo -e "${GREEN}✓ Local run script created${NC}"
}

# Function to check all prerequisites
check_prerequisites() {
    echo -e "\n${BLUE}Checking prerequisites...${NC}"
    
    local all_good=true
    
    check_command git || all_good=false
    check_command python3 || all_good=false
    check_command pip || all_good=false
    
    if [ "$all_good" = false ]; then
        echo -e "\n${RED}Some prerequisites are missing. Please install them first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All required prerequisites are installed${NC}"
}

# Function to initialize git repository
init_git_repo() {
    echo -e "\n${YELLOW}Initializing Git repository...${NC}"
    
    if [ ! -d .git ]; then
        # Run the git initialization script
        chmod +x git-init.sh
        ./git-init.sh
    else
        echo -e "${GREEN}✓ Git repository already initialized${NC}"
    fi
}

# Function to create GitHub secrets file
create_github_secrets() {
    echo -e "\n${YELLOW}Creating GitHub secrets template...${NC}"
    
    cat > .github/SECRETS_TEMPLATE.md << 'EOF'
# GitHub Secrets Configuration

Add these secrets to your GitHub repository (Settings > Secrets > Actions):

## Required Secrets

### AZURE_CREDENTIALS
```json
{
  "clientId": "<your-service-principal-app-id>",
  "clientSecret": "<your-service-principal-password>",
  "subscriptionId": "<your-subscription-id>",
  "tenantId": "<your-tenant-id>"
}
```

To create this:
```bash
az ad sp create-for-rbac --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

### AZURE_FUNCTIONAPP_PUBLISH_PROFILE
Get from Azure Portal:
1. Go to your Function App
2. Click "Get publish profile"
3. Copy entire XML content

### Other Secrets
- `QB_USER_TOKEN`: Your QuickBase user token
- `GPT5_API_KEY`: Your GPT-5 API key
- `TEAMS_APP_SECRET`: Teams app secret

## Setting Secrets via CLI
```bash
gh secret set AZURE_CREDENTIALS < azure-creds.json
gh secret set QB_USER_TOKEN
```
EOF
    echo -e "${GREEN}✓ GitHub secrets template created${NC}"
}

# Function to display next steps
show_next_steps() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                    Setup Complete! 🎉                       ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Repository is ready for development!${NC}"
    echo ""
    echo -e "${BLUE}Quick Start Commands:${NC}"
    echo -e "  ${YELLOW}Activate environment:${NC}  source venv/bin/activate"
    echo -e "  ${YELLOW}Run local tests:${NC}       python local_test.py"
    echo -e "  ${YELLOW}Start local server:${NC}    ./run_local.sh"
    echo -e "  ${YELLOW}Deploy to Azure:${NC}       ./deploy.sh"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. ${CYAN}Configure credentials:${NC}"
    echo -e "     • Copy .env.example to .env"
    echo -e "     • Fill in your actual API keys and tokens"
    echo ""
    echo -e "  2. ${CYAN}Set up Teams app:${NC}"
    echo -e "     • Update manifest.json with your app ID"
    echo -e "     • Add bot icons (color.png, outline.png)"
    echo ""
    echo -e "  3. ${CYAN}Configure QuickBase:${NC}"
    echo -e "     • Verify table structure matches field mappings"
    echo -e "     • Test connectivity with local_test.py"
    echo ""
    echo -e "  4. ${CYAN}Add remote repository:${NC}"
    echo -e "     git remote add origin <your-repo-url>"
    echo -e "     git push -u origin main"
    echo ""
    echo -e "${MAGENTA}Documentation:${NC}"
    echo -e "  • README.md - Complete documentation"
    echo -e "  • GIT_COMMANDS.md - Git workflow reference"
    echo -e "  • .github/SECRETS_TEMPLATE.md - GitHub Actions setup"
    echo ""
    echo -e "${GREEN}Happy coding! 🚀${NC}"
}

# Main execution
main() {
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Initialize git repository
    init_git_repo
    
    # Setup Python environment
    setup_python_env
    
    # Setup pre-commit hooks
    setup_pre_commit
    
    # Check Azure CLI
    setup_azure_cli
    
    # Check Node tools
    setup_node_tools
    
    # Create local development files
    create_local_dev_files
    
    # Create GitHub secrets template
    create_github_secrets
    
    # Show completion message and next steps
    show_next_steps
}

# Run main function
main