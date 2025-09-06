"""
Current Date Time Tool
Provides current date, time, and timezone information for scheduling operations.
"""

from google.adk.tools import GoogleADKTool
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional, Any
import json

class CurrentDateTimeTool(GoogleADKTool):
    """Tool for getting current date and time information."""
    
    name = "get_current_datetime"
    description = "Get current date, time, and timezone information for scheduling purposes"
    
    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone to get current time for (e.g., 'America/New_York', 'UTC', 'Europe/London')",
                        "default": "UTC"
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format: 'iso', 'readable', 'both'",
                        "enum": ["iso", "readable", "both"],
                        "default": "both"
                    },
                    "include_future_dates": {
                        "type": "boolean",
                        "description": "Include common future dates (tomorrow, next week, etc.)",
                        "default": true
                    }
                },
                "required": []
            }
        )
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Get current date and time information."""
        try:
            timezone_str = kwargs.get('timezone', 'UTC')
            format_type = kwargs.get('format', 'both')
            include_future = kwargs.get('include_future_dates', True)
            
            # Get timezone object
            try:
                if timezone_str.upper() == 'UTC':
                    tz = pytz.UTC
                else:
                    tz = pytz.timezone(timezone_str)
            except pytz.exceptions.UnknownTimeZoneError:
                # Fallback to UTC if timezone is invalid
                tz = pytz.UTC
                timezone_str = 'UTC'
            
            # Get current time in specified timezone
            now = datetime.now(tz)
            
            # Prepare response
            result = {
                'success': True,
                'timezone': timezone_str,
                'current': {}
            }
            
            # Format current time
            if format_type in ['iso', 'both']:
                result['current']['iso'] = now.isoformat()
            
            if format_type in ['readable', 'both']:
                result['current']['readable'] = now.strftime('%A, %B %d, %Y at %I:%M %p %Z')
                result['current']['date'] = now.strftime('%Y-%m-%d')
                result['current']['time'] = now.strftime('%H:%M:%S')
                result['current']['day_of_week'] = now.strftime('%A')
            
            # Add additional time information
            result['current']['unix_timestamp'] = int(now.timestamp())
            result['current']['year'] = now.year
            result['current']['month'] = now.month
            result['current']['day'] = now.day
            result['current']['hour'] = now.hour
            result['current']['minute'] = now.minute
            result['current']['weekday'] = now.weekday()  # 0=Monday, 6=Sunday
            
            # Include future dates if requested
            if include_future:
                result['future_references'] = self._get_future_dates(now)
            
            # Business hours information
            result['business_info'] = self._get_business_hours_info(now)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get current date/time: {str(e)}"
            }
    
    def _get_future_dates(self, base_time: datetime) -> Dict[str, Any]:
        """Get common future date references."""
        future_dates = {}
        
        # Tomorrow
        tomorrow = base_time + timedelta(days=1)
        future_dates['tomorrow'] = {
            'iso': tomorrow.isoformat(),
            'readable': tomorrow.strftime('%A, %B %d, %Y'),
            'date': tomorrow.strftime('%Y-%m-%d')
        }
        
        # Next week (next Monday)
        days_until_monday = (7 - base_time.weekday()) % 7
        if days_until_monday == 0:  # If today is Monday, get next Monday
            days_until_monday = 7
        next_monday = base_time + timedelta(days=days_until_monday)
        future_dates['next_week'] = {
            'iso': next_monday.isoformat(),
            'readable': next_monday.strftime('%A, %B %d, %Y'),
            'date': next_monday.strftime('%Y-%m-%d')
        }
        
        # End of this week (Friday)
        days_until_friday = (4 - base_time.weekday()) % 7
        if days_until_friday == 0 and base_time.weekday() >= 4:  # If past Friday
            days_until_friday = 7
        this_friday = base_time + timedelta(days=days_until_friday)
        future_dates['this_friday'] = {
            'iso': this_friday.isoformat(),
            'readable': this_friday.strftime('%A, %B %d, %Y'),
            'date': this_friday.strftime('%Y-%m-%d')
        }
        
        # Next month
        if base_time.month == 12:
            next_month = base_time.replace(year=base_time.year + 1, month=1, day=1)
        else:
            next_month = base_time.replace(month=base_time.month + 1, day=1)
        future_dates['next_month'] = {
            'iso': next_month.isoformat(),
            'readable': next_month.strftime('%B %Y'),
            'date': next_month.strftime('%Y-%m-%d')
        }
        
        return future_dates
    
    def _get_business_hours_info(self, current_time: datetime) -> Dict[str, Any]:
        """Get business hours information."""
        # Standard business hours: 9 AM - 5 PM, Monday-Friday
        is_weekday = current_time.weekday() < 5  # 0-4 is Mon-Fri
        current_hour = current_time.hour
        is_business_hours = is_weekday and 9 <= current_hour < 17
        
        # Calculate next business day
        if current_time.weekday() >= 5:  # Weekend
            days_to_add = 7 - current_time.weekday()  # Days until Monday
        elif current_hour >= 17:  # After business hours
            days_to_add = 1 if current_time.weekday() < 4 else 3  # Next day or Monday
        else:
            days_to_add = 0  # Currently in business hours
        
        next_business_day = current_time + timedelta(days=days_to_add)
        if days_to_add > 0:
            next_business_day = next_business_day.replace(hour=9, minute=0, second=0)
        
        return {
            'is_business_hours': is_business_hours,
            'is_weekday': is_weekday,
            'business_hours': '9:00 AM - 5:00 PM (Monday-Friday)',
            'next_business_day': {
                'iso': next_business_day.isoformat(),
                'readable': next_business_day.strftime('%A, %B %d, %Y at 9:00 AM')
            }
        }

class TimezoneHelperTool(GoogleADKTool):
    """Tool for timezone operations and conversions."""
    
    name = "timezone_helper"
    description = "Get timezone information and convert times between timezones"
    
    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action to perform: 'list_common', 'convert', 'validate'",
                        "enum": ["list_common", "convert", "validate"],
                        "default": "list_common"
                    },
                    "from_timezone": {
                        "type": "string",
                        "description": "Source timezone for conversion (e.g., 'America/New_York')"
                    },
                    "to_timezone": {
                        "type": "string",
                        "description": "Target timezone for conversion (e.g., 'Europe/London')"
                    },
                    "datetime_string": {
                        "type": "string",
                        "description": "Datetime to convert in ISO format"
                    },
                    "timezone_name": {
                        "type": "string",
                        "description": "Timezone name to validate"
                    }
                },
                "required": []
            }
        )
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Perform timezone operations."""
        try:
            action = kwargs.get('action', 'list_common')
            
            if action == 'list_common':
                return self._list_common_timezones()
            elif action == 'convert':
                return self._convert_timezone(
                    kwargs.get('datetime_string'),
                    kwargs.get('from_timezone'),
                    kwargs.get('to_timezone')
                )
            elif action == 'validate':
                return self._validate_timezone(kwargs.get('timezone_name'))
            else:
                return {
                    'success': False,
                    'error': f"Unknown action: {action}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Timezone operation failed: {str(e)}"
            }
    
    def _list_common_timezones(self) -> Dict[str, Any]:
        """List commonly used timezones."""
        common_timezones = {
            'US': [
                'America/New_York',      # Eastern Time
                'America/Chicago',       # Central Time
                'America/Denver',        # Mountain Time
                'America/Los_Angeles',   # Pacific Time
                'America/Phoenix',       # Arizona (no DST)
                'America/Anchorage',     # Alaska Time
                'Pacific/Honolulu'       # Hawaii Time
            ],
            'Europe': [
                'Europe/London',         # GMT/BST
                'Europe/Paris',          # CET/CEST
                'Europe/Berlin',         # CET/CEST
                'Europe/Rome',           # CET/CEST
                'Europe/Madrid',         # CET/CEST
                'Europe/Moscow'          # MSK
            ],
            'Asia': [
                'Asia/Tokyo',           # JST
                'Asia/Shanghai',        # CST
                'Asia/Hong_Kong',       # HKT
                'Asia/Singapore',       # SGT
                'Asia/Kolkata',         # IST
                'Asia/Dubai'            # GST
            ],
            'Other': [
                'UTC',                  # Universal Coordinated Time
                'Australia/Sydney',     # AEST/AEDT
                'Australia/Melbourne',  # AEST/AEDT
                'America/Sao_Paulo'     # BRT/BRST
            ]
        }
        
        return {
            'success': True,
            'common_timezones': common_timezones,
            'message': 'Common timezones listed by region'
        }
    
    def _convert_timezone(self, datetime_str: str, from_tz: str, to_tz: str) -> Dict[str, Any]:
        """Convert datetime between timezones."""
        if not all([datetime_str, from_tz, to_tz]):
            return {
                'success': False,
                'error': 'Missing required parameters for timezone conversion'
            }
        
        try:
            # Parse the datetime
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            
            # Get timezone objects
            from_timezone = pytz.timezone(from_tz) if from_tz != 'UTC' else pytz.UTC
            to_timezone = pytz.timezone(to_tz) if to_tz != 'UTC' else pytz.UTC
            
            # Localize the datetime to source timezone
            if dt.tzinfo is None:
                dt_localized = from_timezone.localize(dt)
            else:
                dt_localized = dt.astimezone(from_timezone)
            
            # Convert to target timezone
            dt_converted = dt_localized.astimezone(to_timezone)
            
            return {
                'success': True,
                'original': {
                    'datetime': dt_localized.isoformat(),
                    'timezone': from_tz,
                    'readable': dt_localized.strftime('%A, %B %d, %Y at %I:%M %p %Z')
                },
                'converted': {
                    'datetime': dt_converted.isoformat(),
                    'timezone': to_tz,
                    'readable': dt_converted.strftime('%A, %B %d, %Y at %I:%M %p %Z')
                },
                'time_difference': str(dt_converted.utcoffset() - dt_localized.utcoffset())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _validate_timezone(self, timezone_name: str) -> Dict[str, Any]:
        """Validate if a timezone name is valid."""
        if not timezone_name:
            return {
                'success': False,
                'error': 'No timezone name provided'
            }
        
        try:
            tz = pytz.timezone(timezone_name)
            now = datetime.now(tz)
            
            return {
                'success': True,
                'valid': True,
                'timezone': timezone_name,
                'current_time': now.isoformat(),
                'current_offset': str(now.utcoffset()),
                'dst_active': bool(now.dst())
            }
            
        except pytz.exceptions.UnknownTimeZoneError:
            return {
                'success': True,
                'valid': False,
                'timezone': timezone_name,
                'error': f'Unknown timezone: {timezone_name}'
            }

# Create tool instances
current_datetime_tool = CurrentDateTimeTool()
timezone_helper_tool = TimezoneHelperTool()

# Export tools
date_time_tools = [
    current_datetime_tool,
    timezone_helper_tool
]
