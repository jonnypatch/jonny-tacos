# Teams IT Support Bot with QuickBase Integration

A comprehensive Microsoft Teams bot that serves as an IT Service Desk solution, featuring AI-powered support responses, QuickBase ticket management, and rich Teams UI interactions using Adaptive Cards.

## 🚀 Features

- **AI-Powered Support**: Uses GPT-5 (with Azure OpenAI fallback) to provide intelligent IT support responses
- **QuickBase Integration**: Full ticket lifecycle management with your existing QuickBase app
- **Rich Teams UI**: Modern Adaptive Cards for intuitive user interactions
- **Automated Ticket Creation**: Smart categorization and priority assignment
- **Real-time Status Updates**: Check ticket status directly in Teams
- **IT Dashboard**: Administrative statistics and monitoring
- **Knowledge Base**: Built-in solutions for common IT issues

## 📋 Prerequisites

- Azure subscription with Function App capabilities
- Microsoft Teams admin access
- QuickBase account with API access
- GPT-5 endpoint or Azure OpenAI resource
- Python 3.11+
- Azure CLI
- Azure Functions Core Tools

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4
```

### 2. Configure Environment Variables

Update `local.settings.json` with your actual values:

```json
{
  "Values": {
    "TEAMS_APP_ID": "your-teams-app-id",
    "TEAMS_APP_SECRET": "your-teams-app-secret",
    "TEAMS_TENANT_ID": "your-tenant-id",
    "QB_REALM": "yourcompany.quickbase.com",
    "QB_USER_TOKEN": "your-quickbase-token",
    "QB_APP_ID": "your-quickbase-app-id",
    "QB_TICKETS_TABLE_ID": "your-table-id",
    "GPT5_ENDPOINT": "your-gpt5-endpoint",
    "GPT5_API_KEY": "your-gpt5-key"
  }
}
```

### 3. QuickBase Configuration

Ensure your QuickBase table has the following fields with corresponding field IDs:

| Field Name | Field ID | Type |
|------------|----------|------|
| Ticket Number | 6 | Text |
| Subject | 7 | Text |
| Description | 8 | Text - Multi-line |
| Priority | 9 | Text - Multiple Choice |
| Category | 10 | Text - Multiple Choice |
| Status | 11 | Text - Multiple Choice |
| Submitted Date | 12 | Date/Time |
| Due Date | 13 | Date |
| Resolved Date | 14 | Date/Time |
| Resolution | 15 | Text - Multi-line |
| Time Spent | 16 | Numeric |

### 4. Deploy to Azure

```bash
# Make deployment script executable
chmod +x deploy.sh

# Set environment variables
export TEAMS_APP_ID="your-app-id"
export TEAMS_APP_SECRET="your-secret"
# ... set all other required variables

# Run deployment
./deploy.sh cabbagepatchkids teams-it-bot eastus2
```

### 5. Teams App Setup

1. Update `manifest.json` with your App ID and endpoints
2. Create app package:
   ```bash
   zip -r teams-app.zip manifest.json color.png outline.png
   ```
3. Upload to Teams Admin Center
4. Install in your Teams environment

## 💬 Bot Commands

### User Commands
- `/help` - Show available commands and features
- `/ticket` - Create a new support ticket
- `/status [ticket#]` - Check ticket status
- Ask any IT question naturally (no command needed)

### Admin Commands
- `/resolve [ticket#] [resolution]` - Resolve a ticket
- `/stats` - View IT dashboard statistics

## 🎯 Usage Examples

### Natural Language Support
```
User: "My Outlook won't sync emails"
Bot: [Provides troubleshooting steps via AI]
     [Offers to create ticket if needed]
```

### Ticket Creation
```
User: "/ticket"
Bot: [Shows ticket form with fields]
User: [Fills form and submits]
Bot: [Creates ticket in QuickBase, shows confirmation]
```

### Status Check
```
User: "/status IT-0042"
Bot: [Shows ticket details and current status]
```

## 🏗️ Architecture

```
Teams Client
    ↓
Azure Function App (Python)
    ├── Teams Handler (Bot Framework)
    ├── Adaptive Cards Builder
    ├── AI Processor (GPT-5/Azure OpenAI)
    └── QuickBase Manager
         ↓
    QuickBase Database
```

## 🔧 Customization

### Adding New IT Categories

Edit `quickbase_manager.py`:
```python
self.categories = [
    'Password Reset',
    'Software Installation',
    # Add your categories here
]
```

### Modifying AI Responses

Edit `ai_processor.py` knowledge base:
```python
self.knowledge_base = {
    "your_issue": {
        "keywords": ["keyword1", "keyword2"],
        "solution": "Your solution text",
        "category": "Category Name",
        "needs_ticket": False
    }
}
```

### Customizing Cards

Edit `adaptive_cards.py` to modify the UI appearance and layout.

## 📊 Monitoring

- **Application Insights**: Monitor function performance and errors
- **Teams Analytics**: Track bot usage in Teams Admin Center
- **QuickBase Reports**: Create custom reports for ticket metrics

## 🔒 Security Considerations

1. Store secrets in Azure Key Vault
2. Enable managed identity for Function App
3. Implement rate limiting
4. Validate all user inputs
5. Use HTTPS for all communications
6. Regular security audits

## 🐛 Troubleshooting

### Bot Not Responding
1. Check Azure Function logs
2. Verify Teams app permissions
3. Confirm webhook URLs are correct

### QuickBase Integration Issues
1. Verify API token permissions
2. Check field mapping IDs
3. Confirm realm hostname

### AI Responses Not Working
1. Check GPT-5/Azure OpenAI endpoints
2. Verify API keys
3. Review rate limits

## 📝 Development

### Local Testing
```bash
func start
```

### Running Tests
```bash
python -m pytest tests/
```

### Updating Dependencies
```bash
pip freeze > requirements.txt
```

## 🤝 Support

For issues or questions:
1. Check the bot logs in Azure Portal
2. Review QuickBase audit logs
3. Contact your IT administrator

## 📄 License

Internal use only - Proprietary

## 🔄 Updates

### Version 1.0.0 (Current)
- Initial release with core functionality
- GPT-5 integration
- QuickBase ticket management
- Adaptive Cards UI

### Planned Features
- Voice command support
- Mobile app integration
- Advanced analytics dashboard
- Auto-ticket routing
- SLA tracking and alerts

## 🎉 Quick Start Checklist

- [ ] Azure Function App created
- [ ] Teams App registered
- [ ] QuickBase API configured
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Bot installed in Teams
- [ ] Test ticket created
- [ ] AI responses working
- [ ] IT channel notifications active
- [ ] Admin commands verified

---

Built with ❤️ for efficient IT support