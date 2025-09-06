# Google Calendar MCP Integration for HR Agent

This document provides comprehensive information about the Google Calendar MCP integration for the HR Agent system, enabling seamless scheduling and calendar management for interviews and HR processes.

## 🎯 Overview

The Google Calendar MCP integration adds powerful scheduling capabilities to the HR Agent system, allowing for:

- **Automated Interview Scheduling**: Create calendar events directly from natural language requests
- **Availability Checking**: Check for conflicts and suggest alternative times
- **Calendar Management**: List, update, and delete events programmatically
- **Multi-attendee Coordination**: Handle complex scheduling with multiple interviewers
- **Timezone Support**: Handle scheduling across different timezones
- **Smart Reminders**: Automatically set appropriate reminders for different event types

## 📋 Prerequisites

### 1. Google Cloud Setup

1. **Create or Select a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Google Calendar API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials JSON file
   - Save it as `credentials.json` in your project root directory

### 2. Python Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

The integration includes these new dependencies:
- `google-auth==2.23.4`
- `google-auth-oauthlib==1.1.0`
- `google-auth-httplib2==0.1.1`
- `google-api-python-client==2.108.0`
- `mcp==1.0.0`

## 🚀 Quick Start

### 1. Setup Authentication

Place your `credentials.json` file in the project root and run the demo:

```bash
python google_calendar_scheduling_demo.py
```

On first run, a browser window will open for authentication. After successful authentication, a `token.json` file will be created for future use.

### 2. Test the Integration

```bash
python hr_calendar_integration_example.py
```

### 3. Use with HR Agent

```python
from HR_root_agent.agent import root_agent

# The agent now has scheduling capabilities
response = root_agent.run("Schedule a technical interview for John Doe tomorrow at 2 PM")
```

## 🛠️ Architecture

### Components

1. **`google_calendar_mcp_config.py`**
   - Handles Google Calendar API authentication
   - Manages OAuth 2.0 flow and token refresh
   - Provides service object for API calls

2. **`google_calendar_mcp_tools.py`**
   - Defines Google ADK-compatible tools for calendar operations
   - Implements CRUD operations for calendar events
   - Provides structured interfaces for the agent system

3. **`calendar_utils.py`**
   - Helper functions for complex scheduling operations
   - Natural language time parsing
   - Availability checking and conflict resolution
   - Interview-specific event formatting

4. **Updated `scheduling_agent`**
   - Enhanced with Google Calendar MCP tools
   - Improved instructions for calendar-aware scheduling
   - Integration with availability checking

### Tool Inventory

| Tool Name | Description | Key Parameters |
|-----------|-------------|----------------|
| `create_calendar_event` | Create new calendar events | summary, start_datetime, end_datetime, attendees |
| `list_calendar_events` | List events in a time range | time_min, time_max, max_results |
| `update_calendar_event` | Update existing events | event_id, updated fields |
| `delete_calendar_event` | Delete calendar events | event_id |

## 📅 Usage Examples

### Basic Event Creation

```python
from google_calendar_mcp_tools import create_event_tool

result = create_event_tool.run(
    summary="Technical Interview - John Doe",
    description="Senior Developer position interview",
    start_datetime="2024-01-15T14:00:00",
    end_datetime="2024-01-15T15:00:00",
    timezone="America/New_York",
    attendees=["interviewer@company.com", "john.doe@email.com"],
    location="Conference Room A"
)
```

### Interview Scheduling with Helper

```python
from calendar_utils import calendar_helper

event_data = calendar_helper.create_interview_event(
    candidate_name="Jane Smith",
    position="Senior Software Engineer",
    interviewer_emails=["tech.lead@company.com", "hr@company.com"],
    start_time="2024-01-15T14:00:00",
    end_time="2024-01-15T15:00:00",
    interview_type="Technical Interview",
    location="Zoom Meeting Room"
)
```

### Availability Checking

```python
from calendar_utils import calendar_helper

availability = calendar_helper.check_availability(
    start_time="2024-01-15T14:00:00",
    end_time="2024-01-15T15:00:00",
    attendee_emails=["interviewer@company.com"]
)

if not availability['available']:
    alternatives = calendar_helper.suggest_alternative_times(
        start_time, end_time, attendee_emails, days_ahead=7
    )
```

## 🤖 Natural Language Processing

The enhanced scheduling agent can handle various natural language requests:

### Supported Request Patterns

- **"Schedule [interview type] for [candidate] [time] for [position]"**
  - Example: "Schedule a technical interview for John Doe tomorrow at 2 PM for the Senior Developer position"

- **"List interviews [time period]"**
  - Example: "List all interviews this week"

- **"Check availability [time]"**
  - Example: "Check if Friday at 3 PM is available"

- **"Reschedule [event] to [new time]"**
  - Example: "Reschedule the interview with Jane Smith to Monday at 10 AM"

### Time Expression Parsing

The system can parse various time expressions:
- Relative: "tomorrow", "next Monday", "this Friday"
- Absolute: "January 15th at 2 PM", "2024-01-15T14:00:00"
- Time ranges: "2-3 PM", "10:30 AM to 11:30 AM"

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with required configurations:

```env
GOOGLE_API_KEY=your_google_api_key
DEFAULT_TIMEZONE=America/New_York
DEFAULT_INTERVIEW_DURATION=60  # minutes
```

### Calendar Settings

Modify `google_calendar_mcp_config.py` for custom settings:

```python
# Custom scopes if needed
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Custom credential files
calendar_config = GoogleCalendarMCPConfig(
    credentials_file='path/to/credentials.json',
    token_file='path/to/token.json'
)
```

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```
   Error: Failed to authenticate with Google Calendar API
   ```
   - Ensure `credentials.json` is in the correct location
   - Check that Google Calendar API is enabled
   - Verify OAuth 2.0 credentials are for "Desktop app"

2. **Permission Denied**
   ```
   Error: Permission denied for calendar access
   ```
   - Ensure OAuth scopes include calendar permissions
   - Re-authenticate by deleting `token.json` and running again

3. **Event Creation Failures**
   ```
   Error: Failed to create calendar event
   ```
   - Check that attendee emails are valid
   - Verify datetime format is ISO 8601
   - Ensure timezone is valid

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run your calendar operations
```

## 🧪 Testing

### Running Tests

```bash
# Run the full demo
python google_calendar_scheduling_demo.py

# Test individual components
python -c "from google_calendar_mcp_config import calendar_config; print(calendar_config.test_connection())"
```

### Test Scenarios

The demo includes these test scenarios:
1. Basic event creation and verification
2. Event listing and formatting
3. Event updating and modification
4. Availability checking with conflicts
5. Alternative time suggestions
6. Event cleanup and deletion

## 📈 Advanced Features

### Batch Operations

```python
# Schedule multiple interviews
interview_batch = [
    {
        "candidate": "Alice Johnson",
        "position": "Frontend Developer",
        "time": "2024-01-15T10:00:00"
    },
    {
        "candidate": "Bob Wilson",
        "position": "Backend Developer", 
        "time": "2024-01-15T14:00:00"
    }
]

for interview in interview_batch:
    # Create events with conflict checking
    pass
```

### Custom Event Templates

```python
class InterviewEventTemplate:
    def technical_interview(self, candidate, position):
        return {
            'summary': f'Technical Interview - {candidate} ({position})',
            'description': self._get_technical_description(position),
            'duration': 60,  # minutes
            'reminders': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 15}
            ]
        }
```

### Integration with Other Systems

```python
# Integration with ATS system
from HR_root_agent.sub_agents.ats_tool.agent import ats_agent

def schedule_from_ats_candidate(candidate_id):
    candidate_info = ats_agent.get_candidate(candidate_id)
    
    # Schedule interview based on ATS data
    schedule_result = create_event_tool.run(
        summary=f"Interview - {candidate_info['name']}",
        # ... other parameters from ATS
    )
```

## 🚀 Production Deployment

### Security Considerations

1. **Credential Management**
   - Store `credentials.json` securely
   - Use environment variables for sensitive data
   - Implement credential rotation

2. **Access Control**
   - Limit calendar scopes to minimum required
   - Implement role-based access for different user types
   - Log all calendar operations for audit trails

3. **Rate Limiting**
   - Implement appropriate rate limiting for API calls
   - Handle quota exceeded errors gracefully
   - Use exponential backoff for retries

### Monitoring

```python
# Add monitoring for calendar operations
import logging

logger = logging.getLogger('calendar_operations')

def monitored_event_creation(**kwargs):
    logger.info(f"Creating event: {kwargs['summary']}")
    result = create_event_tool.run(**kwargs)
    
    if result['success']:
        logger.info(f"Event created successfully: {result['event_id']}")
    else:
        logger.error(f"Event creation failed: {result['error']}")
    
    return result
```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review Google Calendar API documentation
3. Verify your Google Cloud project configuration
4. Test with the provided demo scripts

## 🔄 Updates and Maintenance

### Keeping Up to Date

1. **Google API Updates**
   - Monitor Google Calendar API changelog
   - Update client libraries regularly
   - Test integration after updates

2. **Token Refresh**
   - Implement automatic token refresh
   - Handle expired credentials gracefully
   - Set up monitoring for authentication issues

3. **Feature Enhancements**
   - Add new natural language patterns
   - Implement additional calendar features
   - Enhance error handling and recovery

## 📄 License

This integration is part of the HR Agent system and follows the same licensing terms.

---

*Last updated: January 2024*
