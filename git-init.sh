#!/bin/bash

# Git Repository Initialization Script for Teams IT Support Bot
# This script sets up a new git repository with proper structure and initial commit

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository configuration
REPO_NAME="jonny-tacos"
DEFAULT_BRANCH="main"
GIT_USER_NAME="${GIT_USER_NAME:-Your Name}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-your.email@company.com}"

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}   Teams IT Support Bot - Git Repository Setup    ${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

# Function to check if we're in a git repository
check_git_repo() {
    if [ -d .git ]; then
        echo -e "${YELLOW}Warning: Already in a git repository!${NC}"
        read -p "Do you want to reinitialize? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}Aborted.${NC}"
            exit 1
        fi
        rm -rf .git
    fi
}

# Function to create example environment file
create_env_example() {
    cat > .env.example << 'EOF'
# Teams Bot Configuration
TEAMS_APP_ID=your-teams-app-id-here
TEAMS_APP_SECRET=your-teams-app-secret-here
TEAMS_TENANT_ID=your-tenant-id-here

# QuickBase Configuration
QB_REALM=yourcompany.quickbase.com
QB_USER_TOKEN=your-quickbase-user-token
QB_APP_ID=your-quickbase-app-id
QB_TICKETS_TABLE_ID=your-tickets-table-id

# AI Configuration (GPT-5)
GPT5_ENDPOINT=your-internal-gpt5-endpoint
GPT5_API_KEY=your-gpt5-api-key
GPT5_MODEL=gpt-5

# Azure OpenAI (Fallback)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-azure-openai-key
AZURE_OPENAI_DEPLOYMENT=gpt-4

# IT Support Channel
IT_CHANNEL_ID=your-it-support-channel-id

# Application Insights (Optional)
APPLICATIONINSIGHTS_CONNECTION_STRING=your-connection-string
EOF
    echo -e "${GREEN}Created .env.example file${NC}"
}

# Function to create placeholder icon files
create_placeholder_icons() {
    # Create a simple color icon (base64 encoded 1x1 pixel PNG)
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" | base64 -d > color.png.example
    
    # Create a simple outline icon (base64 encoded 1x1 pixel PNG)
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" | base64 -d > outline.png.example
    
    echo -e "${GREEN}Created placeholder icon files${NC}"
}

# Function to create initial project structure
create_project_structure() {
    echo -e "${YELLOW}Creating project structure...${NC}"
    
    # Create directories
    mkdir -p tests
    mkdir -p docs
    mkdir -p scripts
    mkdir -p templates
    mkdir -p .github/workflows
    
    # Create basic test file
    cat > tests/__init__.py << 'EOF'
"""
Tests for Teams IT Support Bot
"""
EOF

    cat > tests/test_quickbase.py << 'EOF'
"""
Unit tests for QuickBase integration
"""
import unittest
from unittest.mock import Mock, patch

class TestQuickBaseManager(unittest.TestCase):
    """Test QuickBase manager functionality"""
    
    def test_create_ticket(self):
        """Test ticket creation"""
        # Add your tests here
        pass
    
    def test_get_ticket(self):
        """Test ticket retrieval"""
        # Add your tests here
        pass

if __name__ == '__main__':
    unittest.main()
EOF

    # Create GitHub Actions workflow
    cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to Azure Functions

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  AZURE_FUNCTIONAPP_NAME: teams-it-support-bot
  AZURE_FUNCTIONAPP_PACKAGE_PATH: '.'
  PYTHON_VERSION: '3.11'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Setup Python ${{ env.PYTHON_VERSION }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python -m pytest tests/

    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
        package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
EOF

    echo -e "${GREEN}Created project structure${NC}"
}

# Function to create comprehensive README for GitHub
create_github_readme() {
    cat > README_GITHUB.md << 'EOF'
<div align="center">
  
# 🤖 Teams IT Support Bot

### AI-Powered IT Service Desk Solution for Microsoft Teams

[![Azure Functions](https://img.shields.io/badge/Azure-Functions-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com/services/functions/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Teams](https://img.shields.io/badge/Microsoft-Teams-6264A7?style=for-the-badge&logo=microsoft-teams)](https://www.microsoft.com/teams)
[![QuickBase](https://img.shields.io/badge/QuickBase-Integration-4B9BFF?style=for-the-badge)](https://www.quickbase.com/)

</div>

---

## 🚀 Overview

An intelligent IT support bot that integrates Microsoft Teams with QuickBase, providing automated IT support through GPT-5 powered responses and streamlined ticket management.

## ✨ Features

- 🤖 **AI-Powered Support** - GPT-5 integration for intelligent responses
- 🎫 **Ticket Management** - Full QuickBase integration for ticket lifecycle
- 💳 **Rich UI** - Modern Adaptive Cards for Teams interactions
- 📊 **Analytics Dashboard** - Real-time IT metrics and reporting
- 🔔 **Smart Notifications** - Proactive alerts and updates
- 🔍 **Knowledge Base** - Built-in solutions for common issues

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Azure Functions
- **AI**: GPT-5 / Azure OpenAI
- **Database**: QuickBase
- **UI**: Teams Adaptive Cards
- **Infrastructure**: Azure

## 📦 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourorg/teams-it-support-bot.git
   cd teams-it-support-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Deploy to Azure**
   ```bash
   ./deploy.sh your-resource-group bot-name eastus2
   ```

## 📖 Documentation

See the [docs](./docs) folder for detailed documentation.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines.

## 📄 License

Proprietary - Internal Use Only

---

<div align="center">
Made with ❤️ by Your IT Team
</div>
EOF

    echo -e "${GREEN}Created GitHub README${NC}"
}

# Main execution
echo -e "${YELLOW}Starting Git repository initialization...${NC}"
echo ""

# Check if we're already in a git repo
check_git_repo

# Initialize git repository
echo -e "${YELLOW}Initializing new Git repository...${NC}"
git init -b $DEFAULT_BRANCH

# Configure git
echo -e "${YELLOW}Configuring Git...${NC}"
git config user.name "$GIT_USER_NAME"
git config user.email "$GIT_USER_EMAIL"

# Create necessary files and structure
create_env_example
create_placeholder_icons
create_project_structure
create_github_readme

# Create a comprehensive commit message template
cat > .gitmessage << 'EOF'
# <type>: <subject> (Max 50 chars)

# <body> (Explain why this change is being made)

# <footer> (References, links, ticket numbers)

# Type can be:
#   feat     (new feature)
#   fix      (bug fix)
#   docs     (documentation)
#   style    (formatting, missing semi colons, etc)
#   refactor (refactoring code)
#   test     (adding tests)
#   chore    (maintain)
#   deploy   (deployment related)
EOF

git config commit.template .gitmessage

# Stage all files
echo -e "${YELLOW}Staging files...${NC}"
git add .

# Create initial commit
echo -e "${YELLOW}Creating initial commit...${NC}"
git commit -m "feat: Initial commit - Teams IT Support Bot with QuickBase integration

- Azure Functions Python app for Teams bot
- QuickBase integration for ticket management
- GPT-5/Azure OpenAI for intelligent responses
- Adaptive Cards for rich Teams UI
- Comprehensive documentation and deployment scripts
- CI/CD pipeline configuration

Project includes:
- Complete bot implementation
- Deployment automation
- Testing framework
- Documentation"

# Create development branch
echo -e "${YELLOW}Creating development branch...${NC}"
git branch develop

# Show repository status
echo ""
echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}✅ Git Repository Successfully Initialized!${NC}"
echo -e "${GREEN}==================================================${NC}"
echo ""
echo -e "${BLUE}Repository Information:${NC}"
echo -e "  Branch: $(git branch --show-current)"
echo -e "  Commits: $(git rev-list --count HEAD)"
echo -e "  Files tracked: $(git ls-files | wc -l)"
echo ""
echo -e "${BLUE}Available branches:${NC}"
git branch
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Add your remote repository:"
echo "   ${GREEN}git remote add origin https://github.com/yourorg/$REPO_NAME.git${NC}"
echo ""
echo "2. Push to remote:"
echo "   ${GREEN}git push -u origin $DEFAULT_BRANCH${NC}"
echo ""
echo "3. Configure your credentials:"
echo "   ${GREEN}cp .env.example .env${NC}"
echo "   ${GREEN}# Edit .env with your actual values${NC}"
echo ""
echo "4. Set up Teams icons:"
echo "   ${GREEN}# Replace color.png.example and outline.png.example with actual 32x32 and 96x96 icons${NC}"
echo ""
echo -e "${BLUE}Repository Structure:${NC}"
tree -L 2 -a -I '.git' 2>/dev/null || ls -la

# Create a quick git command reference
cat > GIT_COMMANDS.md << 'EOF'
# Git Commands Quick Reference

## Daily Workflow

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: your feature description"

# Push changes
git push origin feature/your-feature-name

# Create pull request on GitHub/Azure DevOps
```

## Common Commands

```bash
# Check status
git status

# View commit history
git log --oneline --graph --all

# Stash changes
git stash
git stash pop

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Sync with remote
git fetch --all
git pull origin main

# Clean up branches
git branch -d feature/branch-name
git remote prune origin
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style
- refactor: Code refactoring
- test: Testing
- chore: Maintenance
- deploy: Deployment

Examples:
```
feat(quickbase): Add ticket priority auto-assignment
fix(teams): Resolve adaptive card rendering issue
docs(readme): Update deployment instructions
```
EOF

echo ""
echo -e "${GREEN}Created GIT_COMMANDS.md for reference${NC}"
echo ""
echo -e "${GREEN}Repository initialization complete! 🎉${NC}"