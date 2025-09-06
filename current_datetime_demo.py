#!/usr/bin/env python3
"""
Current Date/Time Tool Demo
Demonstrates the current date/time tools for scheduling operations.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from current_date_time_tool import current_datetime_tool, timezone_helper_tool

class CurrentDateTimeDemo:
    """Demo class for current date/time tools."""
    
    def demo_current_datetime(self):
        """Demo getting current date and time."""
        print("📅 Demo: Getting Current Date and Time")
        print("=" * 50)
        
        # Test different timezone and format combinations
        test_cases = [
            {"timezone": "UTC", "format": "both"},
            {"timezone": "America/New_York", "format": "both"},
            {"timezone": "Europe/London", "format": "readable"},
            {"timezone": "Asia/Tokyo", "format": "iso"}
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n{i}. Getting current time for {case['timezone']} in {case['format']} format:")
            
            result = current_datetime_tool.run(**case)
            
            if result['success']:
                print(f"✅ Success!")
                print(f"   Timezone: {result['timezone']}")
                
                current_info = result['current']
                if 'readable' in current_info:
                    print(f"   Current Time: {current_info['readable']}")
                if 'iso' in current_info:
                    print(f"   ISO Format: {current_info['iso']}")
                
                # Show business hours info
                business = result.get('business_info', {})
                if business:
                    print(f"   Business Hours: {'Yes' if business.get('is_business_hours') else 'No'}")
                    print(f"   Weekday: {'Yes' if business.get('is_weekday') else 'No'}")
                
                # Show future references
                if 'future_references' in result:
                    future = result['future_references']
                    print(f"   Tomorrow: {future['tomorrow']['readable']}")
                    print(f"   Next Friday: {future['this_friday']['readable']}")
                
            else:
                print(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    def demo_timezone_operations(self):
        """Demo timezone helper operations."""
        print("\n🌍 Demo: Timezone Operations")
        print("=" * 50)
        
        # 1. List common timezones
        print("\n1. Listing Common Timezones:")
        result = timezone_helper_tool.run(action="list_common")
        
        if result['success']:
            timezones = result['common_timezones']
            print("✅ Common timezones by region:")
            for region, tz_list in timezones.items():
                print(f"   {region}: {', '.join(tz_list[:3])}...")  # Show first 3
        
        # 2. Validate timezone
        print("\n2. Validating Timezones:")
        test_timezones = ["America/New_York", "Invalid/Timezone", "UTC", "Europe/London"]
        
        for tz in test_timezones:
            result = timezone_helper_tool.run(action="validate", timezone_name=tz)
            if result['success']:
                if result['valid']:
                    print(f"   ✅ {tz}: Valid (Current time: {result['current_time'][:19]})")
                else:
                    print(f"   ❌ {tz}: Invalid")
        
        # 3. Convert between timezones
        print("\n3. Converting Between Timezones:")
        
        # Get current time for conversion
        current_utc = datetime.utcnow().isoformat()
        
        conversions = [
            {"from": "UTC", "to": "America/New_York", "time": current_utc},
            {"from": "America/New_York", "to": "Europe/London", "time": "2024-01-15T14:00:00"},
            {"from": "Asia/Tokyo", "to": "America/Los_Angeles", "time": "2024-01-15T09:00:00"}
        ]
        
        for conv in conversions:
            result = timezone_helper_tool.run(
                action="convert",
                datetime_string=conv["time"],
                from_timezone=conv["from"],
                to_timezone=conv["to"]
            )
            
            if result['success']:
                orig = result['original']
                converted = result['converted']
                print(f"   🔄 {conv['from']} → {conv['to']}:")
                print(f"      From: {orig['readable']}")
                print(f"      To:   {converted['readable']}")
            else:
                print(f"   ❌ Conversion failed: {result.get('error')}")
    
    def demo_scheduling_scenarios(self):
        """Demo practical scheduling scenarios."""
        print("\n📋 Demo: Practical Scheduling Scenarios")
        print("=" * 50)
        
        # Get current datetime for scheduling
        current_result = current_datetime_tool.run(
            timezone="America/New_York",
            include_future_dates=True
        )
        
        if not current_result['success']:
            print("❌ Failed to get current time for demo")
            return
        
        current_info = current_result['current']
        future_refs = current_result['future_references']
        business_info = current_result['business_info']
        
        print(f"Current Time: {current_info['readable']}")
        print(f"Business Hours: {'Active' if business_info['is_business_hours'] else 'Inactive'}")
        
        # Scenario 1: Schedule for tomorrow
        print(f"\n1. 📅 Scheduling for Tomorrow:")
        tomorrow = future_refs['tomorrow']
        print(f"   Date: {tomorrow['readable']}")
        print(f"   Suggested Time: 2:00 PM - 3:00 PM")
        print(f"   ISO Format: {tomorrow['date']}T14:00:00")
        
        # Scenario 2: Schedule for next week
        print(f"\n2. 📅 Scheduling for Next Week:")
        next_week = future_refs['next_week']
        print(f"   Date: {next_week['readable']}")
        print(f"   Suggested Time: 10:00 AM - 11:00 AM")
        print(f"   ISO Format: {next_week['date']}T10:00:00")
        
        # Scenario 3: End of week scheduling
        print(f"\n3. 📅 End of Week Scheduling:")
        friday = future_refs['this_friday']
        print(f"   Date: {friday['readable']}")
        print(f"   Suggested Time: 3:00 PM - 4:00 PM (end of week wrap-up)")
        print(f"   ISO Format: {friday['date']}T15:00:00")
        
        # Scenario 4: Business hours consideration
        print(f"\n4. 🕐 Business Hours Consideration:")
        if business_info['is_business_hours']:
            print("   ✅ Currently in business hours - can schedule immediately")
        else:
            next_business = business_info['next_business_day']
            print(f"   ⏰ Outside business hours")
            print(f"   Next business day: {next_business['readable']}")
        
        # Scenario 5: International scheduling
        print(f"\n5. 🌍 International Scheduling Example:")
        
        # Convert current NY time to other timezones
        ny_time = current_info['iso']
        
        for tz in ["Europe/London", "Asia/Tokyo", "Australia/Sydney"]:
            conversion = timezone_helper_tool.run(
                action="convert",
                datetime_string=ny_time,
                from_timezone="America/New_York",
                to_timezone=tz
            )
            
            if conversion['success']:
                converted = conversion['converted']
                print(f"   {tz}: {converted['readable']}")
    
    def demo_integration_example(self):
        """Demo how these tools integrate with calendar scheduling."""
        print("\n🔗 Demo: Integration with Calendar Scheduling")
        print("=" * 50)
        
        print("Example HR Agent Workflow:")
        print("\n1. User Request: 'Schedule a technical interview for John Doe tomorrow at 2 PM'")
        
        # Step 1: Get current datetime
        print("\n   Step 1: Get current date/time information")
        current_result = current_datetime_tool.run(timezone="America/New_York")
        
        if current_result['success']:
            print(f"   ✅ Current time: {current_result['current']['readable']}")
            tomorrow = current_result['future_references']['tomorrow']
            interview_time = f"{tomorrow['date']}T14:00:00"
            print(f"   📅 Calculated interview time: {interview_time}")
        
        # Step 2: Timezone consideration
        print("\n   Step 2: Handle timezone requirements")
        if "international" in "technical interview".lower():  # Simulated check
            print("   🌍 International participant detected - checking timezones")
            
            # Convert to other timezones
            conversion = timezone_helper_tool.run(
                action="convert",
                datetime_string=interview_time,
                from_timezone="America/New_York",
                to_timezone="Europe/London"
            )
            
            if conversion['success']:
                print(f"   🇬🇧 London time: {conversion['converted']['readable']}")
        
        # Step 3: Business hours check
        print("\n   Step 3: Business hours validation")
        business_info = current_result.get('business_info', {})
        
        # Parse hour from interview time
        interview_hour = int(interview_time.split('T')[1].split(':')[0])
        
        if 9 <= interview_hour <= 17:
            print("   ✅ Interview time is within business hours")
        else:
            print("   ⚠️ Interview time is outside standard business hours")
            print("   💡 Suggesting alternative: 10:00 AM - 11:00 AM")
        
        # Step 4: Calendar integration
        print("\n   Step 4: Create calendar event (simulated)")
        print("   📧 Would create Google Calendar event with:")
        print(f"      Title: Technical Interview - John Doe (Senior Developer)")
        print(f"      Time: {interview_time}")
        print(f"      Attendees: hr@company.com, interviewer@company.com")
        print(f"      Description: Technical interview for Senior Developer position")
        
        print("\n   ✅ Complete workflow demonstrated!")
    
    def run_full_demo(self):
        """Run the complete demonstration."""
        print("🕐 Current Date/Time Tools Demo")
        print("=" * 60)
        
        try:
            # Run all demo sections
            self.demo_current_datetime()
            self.demo_timezone_operations()
            self.demo_scheduling_scenarios()
            self.demo_integration_example()
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Demo interrupted by user.")
        except Exception as e:
            print(f"\n❌ Demo failed with error: {str(e)}")
        
        print("\n✨ Demo completed!")
        print("\n📚 Available Tools:")
        print("1. get_current_datetime - Get current date/time with timezone support")
        print("2. timezone_helper - Validate, list, and convert between timezones")
        print("\n💡 Usage in HR Agent:")
        print("- 'What time is it now?'")
        print("- 'Schedule interview for tomorrow at 2 PM'")
        print("- 'Convert 3 PM EST to London time'")
        print("- 'Is Friday a business day?'")

def main():
    """Main function to run the demo."""
    demo = CurrentDateTimeDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()
