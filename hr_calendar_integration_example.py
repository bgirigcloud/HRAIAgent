#!/usr/bin/env python3
"""
HR Calendar Integration Example
Shows how to use the HR root agent with Google Calendar scheduling capabilities.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from HR_root_agent.agent import root_agent
from google_calendar_mcp_config import calendar_config

def setup_calendar_integration():
    """Setup Google Calendar integration."""
    print("🔧 Setting up Google Calendar integration...")
    
    # Test calendar connection
    if calendar_config.test_connection():
        print("✅ Google Calendar connection successful!")
        return True
    else:
        print("❌ Google Calendar connection failed!")
        print("Please ensure you have:")
        print("1. Created credentials.json from Google Cloud Console")
        print("2. Enabled Google Calendar API")
        print("3. Placed credentials.json in the project directory")
        return False

def demo_hr_scheduling_workflow():
    """Demonstrate HR scheduling workflow with Google Calendar."""
    print("\n🎯 HR Scheduling Workflow Demo")
    print("=" * 40)
    
    # Example scheduling requests
    scheduling_requests = [
        "Schedule a technical interview for Sarah Johnson tomorrow at 2 PM for the Senior Developer position",
        "List all upcoming interviews for this week",
        "Check availability for Friday at 3 PM for a final interview",
        "Schedule a behavioral interview for Mike Chen next Monday at 10 AM with the hiring manager"
    ]
    
    for i, request in enumerate(scheduling_requests, 1):
        print(f"\n{i}. Request: '{request}'")
        print("-" * 60)
        
        try:
            # In a real implementation, you would call the root agent
            # For demo purposes, we'll show how it would work
            print("🤖 HR Agent Processing...")
            print("   → Routing to scheduling_agent")
            print("   → Using Google Calendar MCP tools")
            print("   → Processing natural language request")
            
            # Simulate agent response
            if "schedule" in request.lower():
                if "technical interview" in request.lower():
                    print("✅ Technical interview scheduled successfully!")
                    print("   📅 Event created in Google Calendar")
                    print("   📧 Invitations sent to all attendees")
                    print("   🔔 Reminders set for 1 day and 10 minutes before")
                elif "behavioral interview" in request.lower():
                    print("✅ Behavioral interview scheduled successfully!")
                    print("   📅 Event created in Google Calendar")
                    print("   👥 Hiring manager and HR representative added")
            
            elif "list" in request.lower():
                print("✅ Retrieved upcoming interviews:")
                print("   📋 Found 3 scheduled interviews")
                print("   📅 All events displayed with details")
            
            elif "check availability" in request.lower():
                print("✅ Availability checked:")
                print("   ⚠️ Conflict found with existing meeting")
                print("   💡 Alternative times suggested")
            
        except Exception as e:
            print(f"❌ Error processing request: {str(e)}")
        
        print()

def demo_interview_scheduling_scenarios():
    """Demo various interview scheduling scenarios."""
    print("\n📅 Interview Scheduling Scenarios")
    print("=" * 40)
    
    scenarios = [
        {
            "scenario": "New Graduate Technical Interview",
            "request": "Schedule a 1-hour technical interview for Alex Kim next Tuesday at 11 AM for the Junior Developer position",
            "details": {
                "candidate": "Alex Kim",
                "position": "Junior Developer",
                "type": "Technical Interview",
                "duration": "1 hour",
                "focus": "Basic programming concepts and problem-solving"
            }
        },
        {
            "scenario": "Senior Role Panel Interview",
            "request": "Schedule a 90-minute panel interview for Jessica Brown on Friday at 2 PM for the Engineering Manager role",
            "details": {
                "candidate": "Jessica Brown",
                "position": "Engineering Manager",
                "type": "Panel Interview",
                "duration": "90 minutes",
                "panel": "Engineering Director, Team Lead, HR Manager"
            }
        },
        {
            "scenario": "Final Interview with CEO",
            "request": "Schedule final interview for David Lee with CEO next week Wednesday at 4 PM",
            "details": {
                "candidate": "David Lee",
                "type": "Final Interview",
                "interviewer": "CEO",
                "importance": "High priority - final hiring decision"
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['scenario']}")
        print(f"   Request: \"{scenario['request']}\"")
        print("   Expected Processing:")
        print("   → Parse candidate name, position, and timing")
        print("   → Check interviewer availability")
        print("   → Create formatted calendar event")
        print("   → Send appropriate invitations")
        print("   → Set interview-specific reminders")
        
        details = scenario['details']
        print("   Event Details:")
        for key, value in details.items():
            print(f"     • {key.capitalize()}: {value}")

def main():
    """Main function for the integration example."""
    print("🏢 HR Agent Google Calendar Integration Example")
    print("=" * 50)
    
    # Setup
    if not setup_calendar_integration():
        print("\n⚠️ Calendar integration not available for this demo.")
        print("   Demo will show expected behavior without actual calendar operations.")
    
    # Run demos
    demo_hr_scheduling_workflow()
    demo_interview_scheduling_scenarios()
    
    print("\n✨ Integration Example Complete!")
    print("\n📚 To use in production:")
    print("1. Ensure Google Calendar credentials are properly configured")
    print("2. Install required dependencies: pip install -r requirements.txt")
    print("3. Run: python main.py")
    print("4. Ask the HR agent to schedule interviews using natural language")
    
    print("\n💡 Example commands to try:")
    print("• 'Schedule a technical interview for John Doe tomorrow at 3 PM'")
    print("• 'What interviews do I have scheduled this week?'")
    print("• 'Reschedule the interview with Jane Smith to Friday at 2 PM'")
    print("• 'Check if Monday at 10 AM is available for an interview'")

if __name__ == "__main__":
    main()
