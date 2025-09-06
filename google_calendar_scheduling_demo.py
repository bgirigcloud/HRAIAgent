#!/usr/bin/env python3
"""
Google Calendar MCP Scheduling Demo
Demonstrates the integration of Google Calendar with the HR agent system.
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_calendar_mcp_config import calendar_config
from google_calendar_mcp_tools import (
    create_event_tool, 
    list_events_tool, 
    update_event_tool, 
    delete_event_tool
)
from calendar_utils import calendar_helper

class GoogleCalendarDemo:
    """Demo class for Google Calendar MCP integration."""
    
    def __init__(self):
        """Initialize the demo."""
        self.demo_events = []
        
    def setup(self) -> bool:
        """Setup and test the Google Calendar connection."""
        print("🔧 Setting up Google Calendar MCP Demo...")
        print("=" * 50)
        
        # Test authentication
        print("1. Testing Google Calendar authentication...")
        if calendar_config.test_connection():
            print("✅ Successfully connected to Google Calendar!")
            return True
        else:
            print("❌ Failed to connect to Google Calendar.")
            print("\n📋 Setup Instructions:")
            print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
            print("2. Create a new project or select existing one")
            print("3. Enable Google Calendar API")
            print("4. Create OAuth 2.0 credentials (Desktop app)")
            print("5. Download credentials.json to this directory")
            print("6. Run this demo again")
            return False
    
    def demo_create_interview_event(self) -> Dict[str, Any]:
        """Demo creating an interview calendar event."""
        print("\n📅 Demo: Creating Interview Calendar Event")
        print("-" * 40)
        
        # Calculate demo time (tomorrow at 2 PM)
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        # Create interview event data
        event_data = calendar_helper.create_interview_event(
            candidate_name="John Smith",
            position="Senior Software Engineer",
            interviewer_emails=["interviewer@company.com", "hr@company.com"],
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            interview_type="Technical Interview",
            timezone="America/New_York",
            location="Conference Room A / Zoom",
            additional_notes="Focus on system design and Python expertise"
        )
        
        print(f"Creating event: {event_data['summary']}")
        print(f"Time: {start_time.strftime('%A, %B %d at %I:%M %p')} - {end_time.strftime('%I:%M %p')}")
        print(f"Attendees: {len(event_data['attendees'])} people")
        
        # Create the event
        result = create_event_tool.run(**event_data)
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"🔗 Event Link: {result['event_link']}")
            self.demo_events.append(result['event_id'])
            return result
        else:
            print(f"❌ {result['message']}")
            return result
    
    def demo_list_events(self) -> Dict[str, Any]:
        """Demo listing calendar events."""
        print("\n📋 Demo: Listing Upcoming Calendar Events")
        print("-" * 40)
        
        # List events for the next 7 days
        now = datetime.now()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=7)).isoformat() + 'Z'
        
        result = list_events_tool.run(
            time_min=time_min,
            time_max=time_max,
            max_results=10
        )
        
        if result['success']:
            print(f"✅ {result['message']}")
            
            if result['events']:
                summary = calendar_helper.format_schedule_summary(result['events'])
                print(summary)
            else:
                print("📭 No events found in the next 7 days.")
            
            return result
        else:
            print(f"❌ {result['message']}")
            return result
    
    def demo_update_event(self, event_id: str) -> Dict[str, Any]:
        """Demo updating a calendar event."""
        print(f"\n✏️ Demo: Updating Calendar Event")
        print("-" * 40)
        
        # Update the event with new information
        result = update_event_tool.run(
            event_id=event_id,
            summary="Technical Interview - John Smith (Senior Software Engineer) - UPDATED",
            description="UPDATED: Technical interview focusing on system design, Python, and cloud architecture. Please prepare relevant coding challenges.",
            location="Conference Room B / Updated Zoom Link"
        )
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"🔗 Updated Event Link: {result['event_link']}")
            return result
        else:
            print(f"❌ {result['message']}")
            return result
    
    def demo_availability_check(self) -> Dict[str, Any]:
        """Demo checking availability for scheduling."""
        print("\n🔍 Demo: Checking Availability")
        print("-" * 40)
        
        # Check availability for tomorrow 3-4 PM
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        print(f"Checking availability for: {start_time.strftime('%A, %B %d at %I:%M %p')} - {end_time.strftime('%I:%M %p')}")
        
        availability = calendar_helper.check_availability(
            start_time.isoformat(),
            end_time.isoformat(),
            ["test@example.com"]
        )
        
        if availability['available']:
            print("✅ Time slot is available!")
        else:
            print(f"⚠️ Found {availability['conflict_count']} conflicts:")
            for conflict in availability['conflicts']:
                print(f"   - {conflict['summary']}: {conflict['start']} - {conflict['end']}")
            
            # Suggest alternatives
            print("\n💡 Suggesting alternative times...")
            alternatives = calendar_helper.suggest_alternative_times(
                start_time.isoformat(),
                end_time.isoformat(),
                ["test@example.com"],
                days_ahead=5
            )
            
            if alternatives:
                print("Alternative time slots:")
                for i, alt in enumerate(alternatives, 1):
                    print(f"   {i}. {alt['day']} at {alt['time']}")
            else:
                print("   No suitable alternatives found in the next 5 days.")
        
        return availability
    
    def demo_cleanup(self):
        """Clean up demo events."""
        print("\n🧹 Demo: Cleaning Up Test Events")
        print("-" * 40)
        
        for event_id in self.demo_events:
            result = delete_event_tool.run(event_id=event_id)
            if result['success']:
                print(f"✅ Deleted event: {event_id}")
            else:
                print(f"❌ Failed to delete event {event_id}: {result['message']}")
    
    def run_full_demo(self):
        """Run the complete demonstration."""
        print("🚀 Google Calendar MCP Integration Demo")
        print("=" * 50)
        
        # Setup
        if not self.setup():
            return
        
        try:
            # Demo 1: Create interview event
            create_result = self.demo_create_interview_event()
            
            # Demo 2: List events
            self.demo_list_events()
            
            # Demo 3: Update event (if creation was successful)
            if create_result.get('success') and self.demo_events:
                self.demo_update_event(self.demo_events[0])
            
            # Demo 4: Check availability
            self.demo_availability_check()
            
            # Demo 5: Clean up
            user_input = input("\n🗑️ Would you like to clean up the demo events? (y/n): ")
            if user_input.lower().startswith('y'):
                self.demo_cleanup()
            else:
                print("Demo events left in calendar for your review.")
        
        except KeyboardInterrupt:
            print("\n\n⏹️ Demo interrupted by user.")
        except Exception as e:
            print(f"\n❌ Demo failed with error: {str(e)}")
        
        print("\n✨ Demo completed!")
        print("\n📚 Next Steps:")
        print("1. Review the created events in Google Calendar")
        print("2. Test the HR agent with: 'Schedule an interview for Jane Doe tomorrow at 3 PM'")
        print("3. Integrate with your existing HR workflow")

def main():
    """Main function to run the demo."""
    demo = GoogleCalendarDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()
