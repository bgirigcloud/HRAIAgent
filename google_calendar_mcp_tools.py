"""
Google Calendar MCP Tools
MCP-compatible tools for Google Calendar operations using Google ADK framework.
"""

from google.adk.tools import GoogleADKTool
from google_calendar_mcp_config import calendar_config
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

class GoogleCalendarCreateEventTool(GoogleADKTool):
    """Tool for creating Google Calendar events."""
    
    name = "create_calendar_event"
    description = "Create a new event in Google Calendar"
    
    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "The title/summary of the event"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the event"
                    },
                    "start_datetime": {
                        "type": "string",
                        "description": "Start date and time in ISO format (e.g., '2024-01-15T14:00:00')"
                    },
                    "end_datetime": {
                        "type": "string",
                        "description": "End date and time in ISO format (e.g., '2024-01-15T15:00:00')"
                    },
                    "timezone": {
                        "type": "string",
                        "description": "Timezone for the event (e.g., 'America/New_York')",
                        "default": "UTC"
                    },
                    "attendees": {
                        "type": "array",
                        "description": "List of attendee email addresses",
                        "items": {"type": "string"},
                        "default": []
                    },
                    "location": {
                        "type": "string",
                        "description": "Location of the event",
                        "default": ""
                    },
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID (defaults to primary calendar)",
                        "default": "primary"
                    }
                },
                "required": ["summary", "start_datetime", "end_datetime"]
            }
        )
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Create a calendar event."""
        try:
            service = calendar_config.get_service()
            
            # Prepare attendees list
            attendees_list = []
            if kwargs.get('attendees'):
                attendees_list = [{'email': email} for email in kwargs['attendees']]
            
            # Create event object
            event = {
                'summary': kwargs['summary'],
                'description': kwargs.get('description', ''),
                'location': kwargs.get('location', ''),
                'start': {
                    'dateTime': kwargs['start_datetime'],
                    'timeZone': kwargs.get('timezone', 'UTC'),
                },
                'end': {
                    'dateTime': kwargs['end_datetime'],
                    'timeZone': kwargs.get('timezone', 'UTC'),
                },
                'attendees': attendees_list,
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 10},       # 10 minutes before
                    ],
                },
            }
            
            # Create the event
            calendar_id = kwargs.get('calendar_id', 'primary')
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_link': created_event.get('htmlLink', ''),
                'message': f"Event '{kwargs['summary']}' created successfully",
                'event_details': {
                    'summary': created_event['summary'],
                    'start': created_event['start'],
                    'end': created_event['end'],
                    'attendees': len(attendees_list),
                    'location': created_event.get('location', ''),
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create calendar event: {str(e)}"
            }

class GoogleCalendarListEventsTool(GoogleADKTool):
    """Tool for listing Google Calendar events."""
    
    name = "list_calendar_events"
    description = "List events from Google Calendar within a specified time range"
    
    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "time_min": {
                        "type": "string",
                        "description": "Start time in ISO format (defaults to now)"
                    },
                    "time_max": {
                        "type": "string",
                        "description": "End time in ISO format (defaults to 7 days from now)"
                    },
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID (defaults to primary calendar)",
                        "default": "primary"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of events to return",
                        "default": 10
                    }
                },
                "required": []
            }
        )
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """List calendar events."""
        try:
            service = calendar_config.get_service()
            
            # Set default time range if not provided
            now = datetime.utcnow()
            time_min = kwargs.get('time_min', now.isoformat() + 'Z')
            time_max = kwargs.get('time_max', (now + timedelta(days=7)).isoformat() + 'Z')
            
            # Call the Calendar API
            calendar_id = kwargs.get('calendar_id', 'primary')
            max_results = kwargs.get('max_results', 10)
            
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format events
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                formatted_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No Title'),
                    'description': event.get('description', ''),
                    'start': start,
                    'end': end,
                    'location': event.get('location', ''),
                    'attendees': len(event.get('attendees', [])),
                    'link': event.get('htmlLink', '')
                })
            
            return {
                'success': True,
                'events_count': len(formatted_events),
                'events': formatted_events,
                'message': f"Found {len(formatted_events)} events"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list calendar events: {str(e)}"
            }

class GoogleCalendarUpdateEventTool(GoogleADKTool):
    """Tool for updating Google Calendar events."""
    
    name = "update_calendar_event"
    description = "Update an existing event in Google Calendar"
    
    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to update"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Updated title/summary of the event"
                    },
                    "description": {
                        "type": "string",
                        "description": "Updated description of the event"
                    },
                    "start_datetime": {
                        "type": "string",
                        "description": "Updated start date and time in ISO format"
                    },
                    "end_datetime": {
                        "type": "string",
                        "description": "Updated end date and time in ISO format"
                    },
                    "timezone": {
                        "type": "string",
                        "description": "Timezone for the event",
                        "default": "UTC"
                    },
                    "location": {
                        "type": "string",
                        "description": "Updated location of the event"
                    },
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID",
                        "default": "primary"
                    }
                },
                "required": ["event_id"]
            }
        )
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Update a calendar event."""
        try:
            service = calendar_config.get_service()
            
            # Get the existing event
            calendar_id = kwargs.get('calendar_id', 'primary')
            event_id = kwargs['event_id']
            
            event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
            
            # Update only provided fields
            if 'summary' in kwargs:
                event['summary'] = kwargs['summary']
            if 'description' in kwargs:
                event['description'] = kwargs['description']
            if 'location' in kwargs:
                event['location'] = kwargs['location']
            if 'start_datetime' in kwargs:
                event['start']['dateTime'] = kwargs['start_datetime']
                event['start']['timeZone'] = kwargs.get('timezone', 'UTC')
            if 'end_datetime' in kwargs:
                event['end']['dateTime'] = kwargs['end_datetime']
                event['end']['timeZone'] = kwargs.get('timezone', 'UTC')
            
            # Update the event
            updated_event = service.events().update(
                calendarId=calendar_id, 
                eventId=event_id, 
                body=event
            ).execute()
            
            return {
                'success': True,
                'event_id': updated_event['id'],
                'event_link': updated_event.get('htmlLink', ''),
                'message': f"Event '{updated_event['summary']}' updated successfully",
                'event_details': {
                    'summary': updated_event['summary'],
                    'start': updated_event['start'],
                    'end': updated_event['end'],
                    'location': updated_event.get('location', ''),
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to update calendar event: {str(e)}"
            }

class GoogleCalendarDeleteEventTool(GoogleADKTool):
    """Tool for deleting Google Calendar events."""
    
    name = "delete_calendar_event"
    description = "Delete an event from Google Calendar"
    
    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to delete"
                    },
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID",
                        "default": "primary"
                    }
                },
                "required": ["event_id"]
            }
        )
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Delete a calendar event."""
        try:
            service = calendar_config.get_service()
            
            calendar_id = kwargs.get('calendar_id', 'primary')
            event_id = kwargs['event_id']
            
            # Delete the event
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            
            return {
                'success': True,
                'event_id': event_id,
                'message': "Event deleted successfully"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to delete calendar event: {str(e)}"
            }

# Create tool instances
create_event_tool = GoogleCalendarCreateEventTool()
list_events_tool = GoogleCalendarListEventsTool()
update_event_tool = GoogleCalendarUpdateEventTool()
delete_event_tool = GoogleCalendarDeleteEventTool()

# Export all tools
all_calendar_tools = [
    create_event_tool,
    list_events_tool,
    update_event_tool,
    delete_event_tool
]
