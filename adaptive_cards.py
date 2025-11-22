"""
Adaptive Card Builder - Creates rich UI cards for Teams interactions
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class AdaptiveCardBuilder:
    def __init__(self):
        """Initialize card builder with common styles"""
        self.colors = {
            'accent': '#0078D4',
            'good': '#107C10',
            'warning': '#FCE100',
            'attention': '#D13438',
            'light': '#F3F2F1',
            'dark': '#323130'
        }

    def create_welcome_card(self) -> Dict[str, Any]:
        """
        Create welcome card when bot is added to channel
        """
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "Container",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://img.icons8.com/color/96/000000/technical-support.png",
                            "size": "Medium",
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "TextBlock",
                            "text": "🎉 IT Support Bot is here!",
                            "weight": "Bolder",
                            "size": "Large",
                            "horizontalAlignment": "Center",
                            "spacing": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": "I'm your AI-powered IT assistant. I can help with common technical issues, create support tickets, and provide quick solutions.",
                            "wrap": True,
                            "horizontalAlignment": "Center",
                            "spacing": "Medium"
                        }
                    ]
                },
                {
                    "type": "Container",
                    "separator": True,
                    "spacing": "Large",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**Here's what I can do:**",
                            "wrap": True,
                            "size": "Medium",
                            "weight": "Bolder"
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "✅ Answer IT questions",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "✅ Troubleshoot issues",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "✅ Create support tickets",
                                            "wrap": True
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "✅ Check ticket status",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "✅ Provide solutions 24/7",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "✅ Escalate when needed",
                                            "wrap": True
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "Container",
                    "separator": True,
                    "spacing": "Large",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**Available Commands:**",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "/help",
                                    "value": "Show available commands"
                                },
                                {
                                    "title": "/ticket",
                                    "value": "Create a new support ticket"
                                },
                                {
                                    "title": "/status [ticket#]",
                                    "value": "Check ticket status"
                                },
                                {
                                    "title": "/stats",
                                    "value": "View IT dashboard (admin)"
                                }
                            ]
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Get Started",
                    "style": "positive",
                    "data": {
                        "action": "help"
                    }
                }
            ]
        }

    def create_help_card(self) -> Dict[str, Any]:
        """
        Create help card showing all available commands
        """
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "📚 IT Support Bot Help",
                    "weight": "Bolder",
                    "size": "Large"
                },
                {
                    "type": "TextBlock",
                    "text": "Here's how to use the IT Support Bot:",
                    "wrap": True,
                    "spacing": "Medium"
                },
                {
                    "type": "Container",
                    "separator": True,
                    "spacing": "Medium",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**Quick Actions**",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "💬",
                                            "size": "Large"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**Ask a question**",
                                            "weight": "Bolder"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Just type your IT question naturally",
                                            "wrap": True,
                                            "isSubtle": True
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "🎫",
                                            "size": "Large"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**/ticket**",
                                            "weight": "Bolder"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Create a new support ticket",
                                            "wrap": True,
                                            "isSubtle": True
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "📊",
                                            "size": "Large"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**/status**",
                                            "weight": "Bolder"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Check your ticket status",
                                            "wrap": True,
                                            "isSubtle": True
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "Container",
                    "separator": True,
                    "spacing": "Medium",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**Common Issues I Can Help With:**",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": "• Password resets and account lockouts\n• Software installation and updates\n• VPN and remote access issues\n• Email and calendar problems\n• Microsoft Teams troubleshooting\n• Printer and scanner issues\n• Slow computer performance\n• Network connectivity problems",
                            "wrap": True,
                            "spacing": "Small"
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Create Ticket",
                    "style": "positive",
                    "data": {
                        "action": "create_ticket_form"
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Check My Tickets",
                    "data": {
                        "action": "check_tickets"
                    }
                }
            ]
        }

    def create_ticket_form(self, subject: str = "", description: str = "", 
                          category: str = "", priority: str = "") -> Dict[str, Any]:
        """
        Create new ticket form
        """
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "🎫 Create Support Ticket",
                    "weight": "Bolder",
                    "size": "Large"
                },
                {
                    "type": "TextBlock",
                    "text": "Please provide details about your issue:",
                    "wrap": True,
                    "spacing": "Small",
                    "isSubtle": True
                },
                {
                    "type": "Container",
                    "separator": True,
                    "spacing": "Medium",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "**Subject** *",
                            "weight": "Bolder"
                        },
                        {
                            "type": "Input.Text",
                            "id": "subject",
                            "placeholder": "Brief description of the issue",
                            "maxLength": 100,
                            "isRequired": True,
                            "value": subject,
                            "errorMessage": "Subject is required"
                        },
                        {
                            "type": "TextBlock",
                            "text": "**Description** *",
                            "weight": "Bolder",
                            "spacing": "Medium"
                        },
                        {
                            "type": "Input.Text",
                            "id": "description",
                            "placeholder": "Detailed description of the issue, including any error messages",
                            "maxLength": 500,
                            "isMultiline": True,
                            "isRequired": True,
                            "value": description,
                            "errorMessage": "Description is required"
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**Category** *",
                                            "weight": "Bolder"
                                        },
                                        {
                                            "type": "Input.ChoiceSet",
                                            "id": "category",
                                            "style": "compact",
                                            "isRequired": True,
                                            "value": category if category else "General Support",
                                            "choices": [
                                                {"title": "Password Reset", "value": "Password Reset"},
                                                {"title": "Software Installation", "value": "Software Installation"},
                                                {"title": "Hardware Issue", "value": "Hardware Issue"},
                                                {"title": "Network Connectivity", "value": "Network Connectivity"},
                                                {"title": "Email Issues", "value": "Email Issues"},
                                                {"title": "Teams/Office 365", "value": "Teams/Office 365"},
                                                {"title": "VPN Access", "value": "VPN Access"},
                                                {"title": "Printer Problems", "value": "Printer Problems"},
                                                {"title": "File Access", "value": "File Access"},
                                                {"title": "Security Concern", "value": "Security Concern"},
                                                {"title": "New User Setup", "value": "New User Setup"},
                                                {"title": "General Support", "value": "General Support"},
                                                {"title": "Other", "value": "Other"}
                                            ],
                                            "errorMessage": "Please select a category"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "**Priority** *",
                                            "weight": "Bolder"
                                        },
                                        {
                                            "type": "Input.ChoiceSet",
                                            "id": "priority",
                                            "style": "compact",
                                            "isRequired": True,
                                            "value": priority if priority else "Medium",
                                            "choices": [
                                                {"title": "🔴 Critical", "value": "Critical"},
                                                {"title": "🟠 High", "value": "High"},
                                                {"title": "🟡 Medium", "value": "Medium"},
                                                {"title": "🟢 Low", "value": "Low"}
                                            ],
                                            "errorMessage": "Please select priority"
                                        }
                                    ]
                                }
                            ],
                            "spacing": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": "**Additional Information** (optional)",
                            "weight": "Bolder",
                            "spacing": "Medium"
                        },
                        {
                            "type": "Input.Text",
                            "id": "additional_info",
                            "placeholder": "Any additional details, affected systems, or when the issue started",
                            "maxLength": 300,
                            "isMultiline": True
                        },
                        {
                            "type": "Container",
                            "spacing": "Small",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "**Priority Guidelines:**",
                                    "weight": "Bolder",
                                    "size": "Small",
                                    "spacing": "Medium"
                                },
                                {
                                    "type": "FactSet",
                                    "facts": [
                                        {
                                            "title": "🔴 Critical:",
                                            "value": "System down, multiple users affected"
                                        },
                                        {
                                            "title": "🟠 High:",
                                            "value": "Can't work, single user affected"
                                        },
                                        {
                                            "title": "🟡 Medium:",
                                            "value": "Work impacted but have workaround"
                                        },
                                        {
                                            "title": "🟢 Low:",
                                            "value": "Questions or minor issues"
                                        }
                                    ],
                                    "spacing": "Small"
                                }
                            ]
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit Ticket",
                    "style": "positive",
                    "data": {
                        "action": "create_ticket"
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Cancel",
                    "data": {
                        "action": "cancel"
                    }
                }
            ]
        }

    def create_ticket_confirmation_card(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create ticket confirmation card
        """
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "Container",
                    "style": "emphasis",
                    "items": [
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "✅",
                                            "size": "ExtraLarge"
                                        }
                                    ]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "Ticket Created Successfully",
                                            "weight": "Bolder",
                                            "size": "Large",
                                            "color": "Good"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": f"Ticket #{ticket.get('ticket_number', 'N/A')}",
                                            "size": "Medium",
                                            "isSubtle": True
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "Container",
                    "separator": True,
                    "spacing": "Medium",
                    "items": [
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "Subject:",
                                    "value": ticket.get('subject', 'N/A')
                                },
                                {
                                    "title": "Priority:",
                                    "value": ticket.get('priority', 'Medium')
                                },
                                {
                                    "title": "Category:",
                                    "value": ticket.get('category', 'General Support')
                                },
                                {
                                    "title": "Status:",
                                    "value": ticket.get('status', 'New')
                                },
                                {
                                    "title": "Due Date:",
                                    "value": self.format_date(ticket.get('due_date'))
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "TextBlock",
                    "text": "**What happens next?**",
                    "weight": "Bolder",
                    "spacing": "Large"
                },
                {
                    "type": "TextBlock",
                    "text": "• IT has been notified of your request\n• You'll receive updates as we work on your ticket\n• Expected response time based on priority",
                    "wrap": True,
                    "spacing": "Small"
                }
            ],
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "View in QuickBase",
                    "url": ticket.get('quickbase_url', '#')
                },
                {
                    "type": "Action.Submit",
                    "title": "Check Status",
                    "data": {
                        "action": "check_status",
                        "ticket_number": ticket.get('ticket_number')
                    }
                }
            ]
        }

    # Continue with remaining methods...
    # [The rest of the methods continue as in the previous version]

    # Helper methods
    def get_status_color(self, status: str) -> str:
        """Get color for status display"""
        status_colors = {
            'New': 'Accent',
            'In Progress': 'Warning',
            'Awaiting User': 'Warning',
            'Awaiting IT': 'Warning',
            'Resolved': 'Good',
            'Closed': 'Good',
            'Cancelled': 'Default'
        }
        return status_colors.get(status, 'Default')

    def get_priority_icon(self, priority: str) -> str:
        """Get icon for priority display"""
        priority_icons = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        return priority_icons.get(priority, '⚪')

    def get_priority_color(self, priority: str) -> str:
        """Get color for priority display"""
        priority_colors = {
            'Critical': 'Attention',
            'High': 'Warning',
            'Medium': 'Default',
            'Low': 'Good'
        }
        return priority_colors.get(priority, 'Default')

    def format_date(self, date_string: str) -> str:
        """Format date for display"""
        try:
            if date_string:
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d %H:%M')
            return 'N/A'
        except:
            return date_string if date_string else 'N/A'

    def format_date_short(self, date_string: str) -> str:
        """Format date for short display"""
        try:
            if date_string:
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                return dt.strftime('%m/%d')
            return 'N/A'
        except:
            return 'N/A'