"""
Teams IT Service Desk Bot - Main Azure Function App
Handles Teams bot interactions, ticket creation, and AI-powered support
"""

import azure.functions as func
import logging
import json
import os
from datetime import datetime, timedelta
import requests
from typing import Dict, Any, Optional, List
import hashlib
import hmac
import base64

# Import our custom modules
from teams_handler import TeamsHandler
from quickbase_manager import QuickBaseManager
from ai_processor import AIProcessor
from adaptive_cards import AdaptiveCardBuilder

app = func.FunctionApp()

# Initialize managers
teams_handler = TeamsHandler()
qb_manager = QuickBaseManager()
ai_processor = AIProcessor()
card_builder = AdaptiveCardBuilder()

@app.route(route="messages", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
async def messages(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main endpoint for Teams bot messages
    Handles incoming messages, commands, and card actions
    """
    logging.info("Teams bot message received")
    
    try:
        # Verify the request is from Teams
        auth_header = req.headers.get('Authorization', '')
        if not verify_teams_request(req, auth_header):
            return func.HttpResponse("Unauthorized", status_code=401)
        
        # Parse the incoming activity
        body = req.get_json()
        activity_type = body.get('type')
        
        # Route based on activity type
        if activity_type == 'message':
            return await handle_message(body)
        elif activity_type == 'invoke':
            return await handle_invoke(body)
        elif activity_type == 'conversationUpdate':
            return await handle_conversation_update(body)
        else:
            logging.info(f"Unhandled activity type: {activity_type}")
            return func.HttpResponse(status_code=200)
            
    except Exception as e:
        logging.error(f"Error processing Teams message: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )

async def handle_message(activity: Dict[str, Any]) -> func.HttpResponse:
    """
    Handle text messages from users
    """
    try:
        user_message = activity.get('text', '').strip()
        user_info = activity.get('from', {})
        conversation = activity.get('conversation', {})
        
        # Remove bot mention if present
        user_message = teams_handler.remove_mentions(user_message)
        
        # Check for commands
        if user_message.lower().startswith('/'):
            return await handle_command(user_message, user_info, conversation, activity)
        
        # Check if this is a ticket status query
        if 'ticket' in user_message.lower() and any(word in user_message.lower() for word in ['status', 'check', 'update']):
            return await handle_ticket_query(user_message, user_info, conversation, activity)
        
        # Otherwise, treat as IT support question
        return await handle_support_question(user_message, user_info, conversation, activity)
        
    except Exception as e:
        logging.error(f"Error handling message: {str(e)}")
        # Send error card to user
        error_card = card_builder.create_error_card(
            "I encountered an error processing your message. Please try again or contact IT support directly."
        )
        await teams_handler.send_card(activity, error_card)
        return func.HttpResponse(status_code=200)

async def handle_command(command: str, user_info: Dict, conversation: Dict, activity: Dict) -> func.HttpResponse:
    """
    Handle bot commands like /help, /ticket, /status
    """
    command_parts = command.split()
    cmd = command_parts[0].lower()
    
    if cmd == '/help':
        # Send help card
        help_card = card_builder.create_help_card()
        await teams_handler.send_card(activity, help_card)
        
    elif cmd == '/ticket':
        # Send new ticket form
        ticket_form = card_builder.create_ticket_form()
        await teams_handler.send_card(activity, ticket_form)
        
    elif cmd == '/status':
        # Get user's open tickets
        if len(command_parts) > 1:
            # Specific ticket number
            ticket_num = command_parts[1]
            ticket = await qb_manager.get_ticket(ticket_num)
            if ticket:
                status_card = card_builder.create_ticket_status_card(ticket)
                await teams_handler.send_card(activity, status_card)
            else:
                await teams_handler.send_message(activity, f"Ticket {ticket_num} not found.")
        else:
            # All user's tickets
            user_email = user_info.get('email', user_info.get('userPrincipalName', ''))
            tickets = await qb_manager.get_user_tickets(user_email)
            if tickets:
                list_card = card_builder.create_ticket_list_card(tickets)
                await teams_handler.send_card(activity, list_card)
            else:
                await teams_handler.send_message(activity, "You have no open tickets.")
                
    elif cmd == '/resolve':
        # IT admin command to resolve ticket
        if len(command_parts) > 1:
            ticket_num = command_parts[1]
            resolution = ' '.join(command_parts[2:]) if len(command_parts) > 2 else "Resolved by IT"
            success = await qb_manager.resolve_ticket(ticket_num, resolution, user_info.get('name', 'IT Admin'))
            if success:
                await teams_handler.send_message(activity, f"Ticket {ticket_num} has been resolved.")
            else:
                await teams_handler.send_message(activity, f"Failed to resolve ticket {ticket_num}.")
    
    elif cmd == '/stats':
        # Show IT dashboard stats (admin only)
        stats = await qb_manager.get_ticket_statistics()
        stats_card = card_builder.create_statistics_card(stats)
        await teams_handler.send_card(activity, stats_card)
    
    else:
        await teams_handler.send_message(activity, f"Unknown command: {cmd}. Type /help for available commands.")
    
    return func.HttpResponse(status_code=200)

async def handle_support_question(question: str, user_info: Dict, conversation: Dict, activity: Dict) -> func.HttpResponse:
    """
    Handle IT support questions using AI
    """
    try:
        # Show typing indicator
        await teams_handler.send_typing_indicator(activity)
        
        # Get AI response for the question
        ai_response = await ai_processor.get_support_response(question)
        
        if ai_response.get('needs_ticket'):
            # Complex issue that needs a ticket
            prefilled_form = card_builder.create_ticket_form(
                subject=ai_response.get('suggested_subject', question[:50]),
                description=question,
                category=ai_response.get('suggested_category', 'General Support'),
                priority=ai_response.get('suggested_priority', 'Medium')
            )
            
            response_card = card_builder.create_ai_response_card(
                ai_response.get('solution', ''),
                show_create_ticket=True
            )
            
            await teams_handler.send_card(activity, response_card)
            await teams_handler.send_card(activity, prefilled_form)
        else:
            # AI provided a solution
            response_card = card_builder.create_ai_response_card(
                ai_response.get('solution', ''),
                show_feedback=True
            )
            await teams_handler.send_card(activity, response_card)
            
            # Log the interaction for analytics
            await log_ai_interaction(question, ai_response, user_info)
            
    except Exception as e:
        logging.error(f"Error handling support question: {str(e)}")
        fallback_card = card_builder.create_ticket_form(
            subject=question[:50],
            description=question
        )
        await teams_handler.send_message(activity, 
            "I'm having trouble processing your question. Please create a ticket for assistance.")
        await teams_handler.send_card(activity, fallback_card)
    
    return func.HttpResponse(status_code=200)

async def handle_invoke(activity: Dict[str, Any]) -> func.HttpResponse:
    """
    Handle Adaptive Card action invocations
    """
    try:
        action = activity.get('value', {})
        action_type = action.get('action')
        
        if action_type == 'create_ticket':
            # Create new ticket from form submission
            ticket_data = {
                'subject': action.get('subject'),
                'description': action.get('description'),
                'priority': action.get('priority', 'Medium'),
                'category': action.get('category', 'General Support'),
                'user_email': activity.get('from', {}).get('email', ''),
                'user_name': activity.get('from', {}).get('name', ''),
                'channel_id': activity.get('conversation', {}).get('id'),
                'teams_message_id': activity.get('id')
            }
            
            # Create ticket in QuickBase
            ticket = await qb_manager.create_ticket(ticket_data)
            
            if ticket:
                # Send confirmation card
                confirmation_card = card_builder.create_ticket_confirmation_card(ticket)
                await teams_handler.update_card(activity, confirmation_card)
                
                # Notify IT channel if configured
                await notify_it_channel(ticket)
                
                # Return invoke response
                return func.HttpResponse(
                    json.dumps({
                        "type": "application/vnd.microsoft.card.adaptive",
                        "value": confirmation_card
                    }),
                    mimetype="application/json",
                    status_code=200
                )
            else:
                error_response = {
                    "type": "application/vnd.microsoft.error",
                    "value": "Failed to create ticket. Please try again."
                }
                return func.HttpResponse(
                    json.dumps(error_response),
                    mimetype="application/json",
                    status_code=200
                )
                
        elif action_type == 'update_ticket':
            # Update ticket from IT admin
            ticket_update = {
                'ticket_id': action.get('ticket_id'),
                'status': action.get('status'),
                'resolution': action.get('resolution'),
                'time_spent': action.get('time_spent'),
                'updated_by': activity.get('from', {}).get('name', 'IT Admin')
            }
            
            success = await qb_manager.update_ticket(ticket_update)
            
            if success:
                updated_card = card_builder.create_ticket_updated_card(ticket_update)
                await teams_handler.update_card(activity, updated_card)
            
            return func.HttpResponse(
                json.dumps({"status": "success" if success else "failed"}),
                mimetype="application/json",
                status_code=200
            )
            
        elif action_type == 'feedback':
            # Handle solution feedback
            feedback_data = {
                'helpful': action.get('helpful'),
                'question': action.get('question'),
                'solution': action.get('solution'),
                'user': activity.get('from', {}).get('name', 'Unknown')
            }
            await log_feedback(feedback_data)
            
            # Update card to show feedback received
            feedback_card = card_builder.create_feedback_received_card()
            await teams_handler.update_card(activity, feedback_card)
            
            return func.HttpResponse(
                json.dumps({"status": "success"}),
                mimetype="application/json",
                status_code=200
            )
            
    except Exception as e:
        logging.error(f"Error handling invoke: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

async def handle_conversation_update(activity: Dict[str, Any]) -> func.HttpResponse:
    """
    Handle bot being added to team/channel or new members joining
    """
    try:
        members_added = activity.get('membersAdded', [])
        bot_id = activity.get('recipient', {}).get('id')
        
        for member in members_added:
            if member.get('id') == bot_id:
                # Bot was added to a team/channel
                welcome_card = card_builder.create_welcome_card()
                await teams_handler.send_card(activity, welcome_card)
                
                # Store channel info if it's an IT support channel
                channel_info = activity.get('conversation', {})
                if channel_info.get('conversationType') == 'channel':
                    await store_channel_info(channel_info)
                    
    except Exception as e:
        logging.error(f"Error handling conversation update: {str(e)}")
    
    return func.HttpResponse(status_code=200)

async def notify_it_channel(ticket: Dict[str, Any]) -> None:
    """
    Send notification to IT support channel about new ticket
    """
    try:
        it_channel_id = os.environ.get('IT_CHANNEL_ID')
        if it_channel_id:
            notification_card = card_builder.create_it_notification_card(ticket)
            await teams_handler.send_to_channel(it_channel_id, notification_card)
    except Exception as e:
        logging.error(f"Error notifying IT channel: {str(e)}")

def verify_teams_request(req: func.HttpRequest, auth_header: str) -> bool:
    """
    Verify the request is from Microsoft Teams
    """
    try:
        # In production, implement proper Teams authentication
        # This is a simplified version
        if not auth_header.startswith('Bearer '):
            return False
        
        # Verify with Teams App ID and secret
        app_id = os.environ.get('TEAMS_APP_ID')
        app_secret = os.environ.get('TEAMS_APP_SECRET')
        
        # Add proper JWT validation here
        # For now, basic validation
        return True
        
    except Exception as e:
        logging.error(f"Error verifying Teams request: {str(e)}")
        return False

async def log_ai_interaction(question: str, response: Dict, user_info: Dict) -> None:
    """
    Log AI interactions for analytics and improvement
    """
    try:
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'user': user_info.get('name', 'Unknown'),
            'question': question,
            'ai_response': response.get('solution', ''),
            'confidence': response.get('confidence', 0),
            'needs_ticket': response.get('needs_ticket', False)
        }
        
        # Store in Azure Table Storage or your preferred logging solution
        # For now, just log it
        logging.info(f"AI Interaction: {json.dumps(log_data)}")
        
    except Exception as e:
        logging.error(f"Error logging AI interaction: {str(e)}")

async def log_feedback(feedback_data: Dict) -> None:
    """
    Log user feedback on AI solutions
    """
    try:
        feedback_data['timestamp'] = datetime.utcnow().isoformat()
        logging.info(f"Solution Feedback: {json.dumps(feedback_data)}")
        
        # Store in database for analysis
        # This helps improve AI responses over time
        
    except Exception as e:
        logging.error(f"Error logging feedback: {str(e)}")

async def store_channel_info(channel_info: Dict) -> None:
    """
    Store Teams channel information for notifications
    """
    try:
        # Store in Azure Table Storage or configuration
        logging.info(f"Storing channel info: {channel_info.get('id')}")
    except Exception as e:
        logging.error(f"Error storing channel info: {str(e)}")

# Health check endpoint
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
async def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint for monitoring
    """
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }),
        mimetype="application/json",
        status_code=200
    )