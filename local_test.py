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