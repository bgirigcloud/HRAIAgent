"""
Calendar Utilities
Helper functions for calendar operations and scheduling workflows.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import re
from google_calendar_mcp_config import calendar_config

class CalendarSchedulingHelper:
    """Helper class for complex scheduling operations."""
    
    @staticmethod
    def parse_natural_time(time_str: str, timezone: str = "UTC") -> Optional[str]:
        """
        Parse natural language time expressions into ISO format.
        
        Args:
            time_str: Natural language time (e.g., "tomorrow at 2 PM", "next Monday 10:00 AM")
            timezone: Timezone to use
            
        Returns:
            ISO formatted datetime string or None if parsing fails
        """
        try:
            # This is a simplified parser - in production, consider using libraries like dateutil
            now = datetime.now()
            
            # Handle "tomorrow" cases
            if "tomorrow" in time_str.lower():
                tomorrow = now + timedelta(days=1)
                time_part = re.search(r'(\d{1,2}):?(\d{0,2})\s*(am|pm)', time_str.lower())
                if time_part:
                    hour = int(time_part.group(1))
                    minute = int(time_part.group(2)) if time_part.group(2) else 0
                    if time_part.group(3) == 'pm' and hour != 12:
                        hour += 12
                    elif time_part.group(3) == 'am' and hour == 12:
                        hour = 0
                    
                    result = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    return result.isoformat()
            
            # Handle "today" cases
            if "today" in time_str.lower():
                time_part = re.search(r'(\d{1,2}):?(\d{0,2})\s*(am|pm)', time_str.lower())
                if time_part:
                    hour = int(time_part.group(1))
                    minute = int(time_part.group(2)) if time_part.group(2) else 0
                    if time_part.group(3) == 'pm' and hour != 12:
                        hour += 12
                    elif time_part.group(3) == 'am' and hour == 12:
                        hour = 0
                    
                    result = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    return result.isoformat()
            
            # Handle ISO format directly
            if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', time_str):
                return time_str
                
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def check_availability(start_time: str, end_time: str, attendee_emails: List[str], 
                          timezone: str = "UTC") -> Dict[str, Any]:
        """
        Check availability for all attendees during the specified time slot.
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            attendee_emails: List of attendee email addresses
            timezone: Timezone for the event
            
        Returns:
            Dictionary with availability information
        """
        try:
            service = calendar_config.get_service()
            
            # For simplicity, check the primary calendar only
            # In a full implementation, you'd check each attendee's calendar
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            conflicts = []
            
            for event in events:
                event_start = event['start'].get('dateTime', event['start'].get('date'))
                event_end = event['end'].get('dateTime', event['end'].get('date'))
                
                conflicts.append({
                    'summary': event.get('summary', 'Busy'),
                    'start': event_start,
                    'end': event_end
                })
            
            return {
                'available': len(conflicts) == 0,
                'conflicts': conflicts,
                'conflict_count': len(conflicts),
                'message': f"Found {len(conflicts)} conflicts" if conflicts else "Time slot is available"
            }
            
        except Exception as e:
            return {
                'available': False,
                'error': str(e),
                'message': f"Failed to check availability: {str(e)}"
            }
    
    @staticmethod
    def suggest_alternative_times(original_start: str, original_end: str, 
                                attendee_emails: List[str], days_ahead: int = 7) -> List[Dict[str, str]]:
        """
        Suggest alternative meeting times if the original time has conflicts.
        
        Args:
            original_start: Original start time in ISO format
            original_end: Original end time in ISO format
            attendee_emails: List of attendee email addresses
            days_ahead: Number of days to look ahead for alternatives
            
        Returns:
            List of alternative time slots
        """
        try:
            start_dt = datetime.fromisoformat(original_start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(original_end.replace('Z', '+00:00'))
            duration = end_dt - start_dt
            
            suggestions = []
            
            # Check next few days at the same time
            for day_offset in range(1, days_ahead + 1):
                new_start = start_dt + timedelta(days=day_offset)
                new_end = new_start + duration
                
                availability = CalendarSchedulingHelper.check_availability(
                    new_start.isoformat(),
                    new_end.isoformat(),
                    attendee_emails
                )
                
                if availability['available']:
                    suggestions.append({
                        'start_datetime': new_start.isoformat(),
                        'end_datetime': new_end.isoformat(),
                        'day': new_start.strftime('%A, %B %d, %Y'),
                        'time': f"{new_start.strftime('%I:%M %p')} - {new_end.strftime('%I:%M %p')}"
                    })
                    
                    # Stop after finding 3 alternatives
                    if len(suggestions) >= 3:
                        break
            
            return suggestions
            
        except Exception:
            return []
    
    @staticmethod
    def create_interview_event(candidate_name: str, position: str, interviewer_emails: List[str],
                             start_time: str, end_time: str, interview_type: str = "Technical Interview",
                             timezone: str = "UTC", location: str = "", additional_notes: str = "") -> Dict[str, Any]:
        """
        Create a formatted interview calendar event.
        
        Args:
            candidate_name: Name of the candidate
            position: Position being interviewed for
            interviewer_emails: List of interviewer email addresses
            start_time: Start time in ISO format
            end_time: End time in ISO format
            interview_type: Type of interview (Technical, Behavioral, etc.)
            timezone: Timezone for the event
            location: Meeting location or video link
            additional_notes: Additional notes for the interview
            
        Returns:
            Dictionary with event creation parameters
        """
        summary = f"{interview_type} - {candidate_name} ({position})"
        
        description = f"""
Interview Details:
• Candidate: {candidate_name}
• Position: {position}
• Interview Type: {interview_type}
• Duration: {start_time} - {end_time}

{additional_notes}

Please ensure you have reviewed the candidate's resume and prepared relevant questions.
""".strip()
        
        return {
            'summary': summary,
            'description': description,
            'start_datetime': start_time,
            'end_datetime': end_time,
            'timezone': timezone,
            'attendees': interviewer_emails,
            'location': location
        }
    
    @staticmethod
    def format_schedule_summary(events: List[Dict[str, Any]]) -> str:
        """
        Format a list of events into a readable schedule summary.
        
        Args:
            events: List of calendar events
            
        Returns:
            Formatted schedule summary string
        """
        if not events:
            return "No scheduled events found."
        
        summary_lines = ["📅 **Schedule Summary**\n"]
        
        for i, event in enumerate(events, 1):
            start_time = event.get('start', '')
            summary = event.get('summary', 'No Title')
            location = event.get('location', '')
            attendees_count = event.get('attendees', 0)
            
            # Format the datetime
            try:
                if 'T' in start_time:
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%A, %B %d at %I:%M %p')
                else:
                    formatted_time = start_time
            except:
                formatted_time = start_time
            
            summary_lines.append(f"{i}. **{summary}**")
            summary_lines.append(f"   📍 {formatted_time}")
            if location:
                summary_lines.append(f"   🏢 {location}")
            if attendees_count > 0:
                summary_lines.append(f"   👥 {attendees_count} attendees")
            summary_lines.append("")
        
        return "\n".join(summary_lines)

# Create helper instance
calendar_helper = CalendarSchedulingHelper()
