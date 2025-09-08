"""
Demo script for the Onboarding Agent.

This script demonstrates how to use the Onboarding Agent to automate
the process of onboarding new employees.
"""

import json
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import HR_root_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from HR_root_agent.sub_agents.onboarding_agent import OnboardingAgent
except ImportError:
    print("Creating mock OnboardingAgent for demonstration purposes...")
    
    # If import fails, create a mock version of the OnboardingAgent
    class OnboardingAgent:
        def __init__(self, name="Onboarding Assistant"):
            self.name = name
            print(f"Initialized {self.name}")
            
        def complete_onboarding_process(self, employee_info):
            print(f"Simulating onboarding process for {employee_info.get('name', 'New Employee')}")
            return {
                "status": "success",
                "message": f"Mock onboarding process initiated for {employee_info.get('name', '')}",
                "welcome_email_sent": True,
                "it_setup_requested": True,
                "meetings_scheduled": True,
                "access_requests_created": True,
                "document_generated": True,
                "onboarding_plan": {
                    "title": f"Mock Onboarding Plan for {employee_info.get('name', '')}",
                    "employee_info": employee_info
                }
            }

def print_section(title):
    """Print a formatted section title."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_json(data):
    """Print formatted JSON data."""
    print(json.dumps(data, indent=2))

def main():
    print_section("ONBOARDING AGENT DEMONSTRATION")
    
    # Initialize the agent
    agent = OnboardingAgent()
    
    # Create a sample new employee
    start_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    new_employee = {
        "name": "Jane Smith",
        "position": "Senior Software Engineer",
        "department": "Engineering",
        "start_date": start_date,
        "manager": "John Manager",
        "team": "Backend Development",
        "location": "New York Office",
        "email": "jane.smith@example.com"
    }
    
    print_section("NEW EMPLOYEE INFORMATION")
    print_json(new_employee)
    
    # Complete onboarding process
    print_section("INITIATING COMPLETE ONBOARDING PROCESS")
    result = agent.complete_onboarding_process(new_employee)
    
    # Display status
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print()
    print(f"Welcome Email Sent: {'✓' if result['welcome_email_sent'] else '✗'}")
    print(f"IT Setup Requested: {'✓' if result['it_setup_requested'] else '✗'}")
    print(f"Meetings Scheduled: {'✓' if result['meetings_scheduled'] else '✗'}")
    print(f"Access Requests Created: {'✓' if result['access_requests_created'] else '✗'}")
    print(f"Document Generated: {'✓' if result['document_generated'] else '✗'}")
    
    # Display the onboarding plan summary
    print_section("ONBOARDING PLAN SUMMARY")
    plan = result.get("onboarding_plan", {})
    
    if "title" in plan:
        print(f"Title: {plan['title']}")
    
    if "employee_info" in plan:
        print("\nEmployee Information:")
        for key, value in plan['employee_info'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    if "first_day_instructions" in plan:
        print(f"\nFirst Day Instructions: {plan['first_day_instructions']}")
    
    if "schedule" in plan:
        print("\nFirst Week Schedule:")
        for day in plan["schedule"]:
            print(f"\n  {day['day']} ({day['date']}):")
            for event in day.get("events", []):
                print(f"    • {event}")
    
    if "key_contacts" in plan:
        print("\nKey Contacts:")
        for role, contact in plan.get("key_contacts", {}).items():
            print(f"  {role.replace('_', ' ').title()}: {contact.get('name', '')} - {contact.get('email', '')}")
    
    # Demonstrate asking the agent natural language questions
    print_section("NATURAL LANGUAGE INTERACTION WITH AGENT")
    
    questions = [
        "What kind of welcome email will be sent?",
        "Can you schedule all the onboarding meetings?",
        "What system access will be set up?",
        "What equipment will be prepared?",
        "Can you show me the onboarding checklist?",
    ]
    
    context = {"employee": new_employee}
    
    for question in questions:
        print(f"\nQuestion: {question}")
        answer = agent.ask(question, context)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
