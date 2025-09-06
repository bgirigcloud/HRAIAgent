# Current Data Tools Summary

This document provides a comprehensive overview of the current date/time tools available in the HR Agent system for enhanced scheduling capabilities.

## 🛠️ Available Tools

### 1. `get_current_datetime` Tool

**Purpose**: Get current date, time, and timezone information for scheduling operations.

**Key Features**:
- ✅ Multi-timezone support
- ✅ Multiple output formats (ISO, readable, both)
- ✅ Business hours detection
- ✅ Future date references (tomorrow, next week, etc.)
- ✅ Comprehensive time information

**Parameters**:
```json
{
  "timezone": "America/New_York",     // Target timezone
  "format": "both",                   // Output format: iso, readable, both
  "include_future_dates": true        // Include common future references
}
```

**Example Output**:
```json
{
  "success": true,
  "timezone": "America/New_York",
  "current": {
    "iso": "2024-01-15T14:30:00-05:00",
    "readable": "Monday, January 15, 2024 at 02:30 PM EST",
    "date": "2024-01-15",
    "time": "14:30:00",
    "day_of_week": "Monday",
    "unix_timestamp": 1705339800,
    "year": 2024,
    "month": 1,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "weekday": 0
  },
  "future_references": {
    "tomorrow": {
      "iso": "2024-01-16T14:30:00-05:00",
      "readable": "Tuesday, January 16, 2024",
      "date": "2024-01-16"
    },
    "next_week": {
      "iso": "2024-01-22T14:30:00-05:00",
      "readable": "Monday, January 22, 2024",
      "date": "2024-01-22"
    },
    "this_friday": {
      "iso": "2024-01-19T14:30:00-05:00",
      "readable": "Friday, January 19, 2024",
      "date": "2024-01-19"
    },
    "next_month": {
      "iso": "2024-02-01T14:30:00-05:00",
      "readable": "February 2024",
      "date": "2024-02-01"
    }
  },
  "business_info": {
    "is_business_hours": true,
    "is_weekday": true,
    "business_hours": "9:00 AM - 5:00 PM (Monday-Friday)",
    "next_business_day": {
      "iso": "2024-01-16T09:00:00-05:00",
      "readable": "Tuesday, January 16, 2024 at 9:00 AM"
    }
  }
}
```

### 2. `timezone_helper` Tool

**Purpose**: Handle timezone operations including validation, listing, and conversions.

**Key Features**:
- ✅ List common timezones by region
- ✅ Validate timezone names
- ✅ Convert times between timezones
- ✅ Handle DST automatically
- ✅ Calculate time differences

**Actions Available**:

#### `list_common` - List Common Timezones
```json
{
  "action": "list_common"
}
```

**Output**: Organized list of timezones by region (US, Europe, Asia, Other).

#### `validate` - Validate Timezone
```json
{
  "action": "validate",
  "timezone_name": "America/New_York"
}
```

**Output**: Validation result with current time if valid.

#### `convert` - Convert Between Timezones
```json
{
  "action": "convert",
  "datetime_string": "2024-01-15T14:00:00",
  "from_timezone": "America/New_York",
  "to_timezone": "Europe/London"
}
```

**Output**: Original and converted times with time difference.

## 🎯 Integration with HR Agent

### Current Tools in Scheduling Agent

The scheduling agent now has access to:
1. **Google Calendar Tools** (4 tools):
   - `create_calendar_event` - Create new events
   - `list_calendar_events` - List existing events
   - `update_calendar_event` - Update events
   - `delete_calendar_event` - Delete events

2. **Date/Time Tools** (2 tools):
   - `get_current_datetime` - Current time information
   - `timezone_helper` - Timezone operations

### Enhanced Capabilities

With these tools, the HR Agent can now:
- ✅ Get accurate current time for any timezone
- ✅ Handle natural language time expressions
- ✅ Validate business hours
- ✅ Convert between timezones for international interviews
- ✅ Calculate future dates (tomorrow, next week, etc.)
- ✅ Provide comprehensive scheduling information

## 🚀 Usage Examples

### 1. Basic Current Time
```python
# Get current time in EST
result = current_datetime_tool.run(
    timezone="America/New_York",
    format="both"
)
```

### 2. Business Hours Check
```python
# Check if it's currently business hours
result = current_datetime_tool.run(timezone="UTC")
is_business_hours = result['business_info']['is_business_hours']
```

### 3. Timezone Conversion
```python
# Convert interview time from NY to London
result = timezone_helper_tool.run(
    action="convert",
    datetime_string="2024-01-15T14:00:00",
    from_timezone="America/New_York",
    to_timezone="Europe/London"
)
```

### 4. Validate Timezone
```python
# Check if timezone is valid
result = timezone_helper_tool.run(
    action="validate",
    timezone_name="Asia/Tokyo"
)
```

## 📋 Natural Language Processing

The enhanced scheduling agent can now handle:

### Time-Related Queries
- **"What time is it now?"**
- **"What time is it in London?"**
- **"Is it business hours?"**
- **"When is tomorrow?"**
- **"What's the date next Monday?"**

### Scheduling with Time Context
- **"Schedule interview tomorrow at 2 PM"** → Uses current time to calculate tomorrow
- **"Schedule meeting next week"** → Uses future date references
- **"Convert 3 PM EST to Tokyo time"** → Uses timezone conversion
- **"Is Friday a business day?"** → Uses business hours detection

### International Scheduling
- **"Schedule interview with London candidate at 3 PM their time"**
- **"What time is 10 AM Tokyo time in New York?"**
- **"Schedule call with Sydney office next Tuesday"**

## 🔧 Technical Implementation

### Dependencies Added
```txt
pytz==2023.3  # Timezone handling
```

### File Structure
```
HR_agent/
├── current_date_time_tool.py          # Main date/time tools
├── current_datetime_demo.py           # Demo script
├── CURRENT_DATA_TOOLS_SUMMARY.md     # This documentation
└── HR_root_agent/
    └── sub_agents/
        └── scheduling_agent/
            └── agent.py               # Updated with new tools
```

### Integration Pattern
```python
# Import tools
from current_date_time_tool import date_time_tools

# Add to agent
scheduling_agent = Agent(
    tools=all_calendar_tools + date_time_tools,
    # ... other configuration
)
```

## 🧪 Testing

### Run the Demo
```bash
python current_datetime_demo.py
```

The demo includes:
1. ✅ Current datetime in multiple timezones
2. ✅ Timezone operations (list, validate, convert)
3. ✅ Practical scheduling scenarios
4. ✅ Integration workflow examples

### Test Individual Tools
```python
from current_date_time_tool import current_datetime_tool, timezone_helper_tool

# Test current time
result = current_datetime_tool.run()
print(result)

# Test timezone conversion
result = timezone_helper_tool.run(action="list_common")
print(result)
```

## 🎯 Benefits for HR Workflows

### 1. Accurate Scheduling
- Always use current time for scheduling calculations
- Handle timezone conversions automatically
- Respect business hours

### 2. Natural Language Support
- Parse "tomorrow", "next week" expressions
- Convert relative time to absolute time
- Handle international time references

### 3. Comprehensive Time Information
- Provide multiple date formats
- Include business hours context
- Calculate future date references

### 4. International Support
- List common timezones by region
- Validate timezone names
- Convert between any timezones

## 🔮 Future Enhancements

Potential improvements:
- ⏰ Holiday calendar integration
- 📍 Location-based timezone detection
- 🔄 Recurring event support
- 📊 Scheduling analytics
- 🎯 Smart time slot suggestions
- 📱 Mobile timezone handling

## 📞 Support

For questions about the current data tools:
1. Run the demo script for examples
2. Check tool parameters and outputs
3. Review timezone validation results
4. Test with different timezone combinations

---

*The current data tools provide essential time and timezone functionality for the HR Agent's scheduling capabilities, enabling accurate and intelligent scheduling across global teams.*
