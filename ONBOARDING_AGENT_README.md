# Onboarding Agent Documentation

The Onboarding Agent is a specialized component of the HR AI Multi-Agent system designed to automate the employee onboarding process. It streamlines the workflow of welcoming new employees, setting up their accounts, scheduling orientation meetings, and ensuring they have everything they need for a successful start.

## Features

- **Welcome Email Generation**: Create personalized welcome emails for new employees with all relevant first-day information.
- **Onboarding Plan Creation**: Generate comprehensive onboarding plans tailored to the employee's role and department.
- **Meeting Scheduling**: Automatically schedule all necessary onboarding meetings and send calendar invitations.
- **System Access Requests**: Create and track requests for email accounts, system access, and other IT resources.
- **Equipment Setup Coordination**: Coordinate with IT to ensure all necessary equipment is ready before the employee's start date.
- **Task Management**: Create and assign onboarding tasks to relevant departments (HR, IT, Facilities, etc.).
- **Documentation Generation**: Create personalized onboarding documents for new employees.

## Usage Examples

### Complete Onboarding Process

```python
from HR_root_agent.sub_agents.onboarding_agent import OnboardingAgent

# Initialize the agent
agent = OnboardingAgent()

# Define a new employee
new_employee = {
    "name": "Jane Smith",
    "position": "Senior Software Engineer",
    "department": "Engineering",
    "start_date": "2025-10-15",
    "manager": "John Manager",
    "team": "Backend Development",
    "location": "New York Office",
    "email": "jane.smith@cloudhero.ai"
}

# Execute the complete onboarding process
result = agent.complete_onboarding_process(new_employee)

# Check the results
print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print(f"Welcome Email Sent: {'✓' if result['welcome_email_sent'] else '✗'}")
print(f"IT Setup Requested: {'✓' if result['it_setup_requested'] else '✗'}")
print(f"Meetings Scheduled: {'✓' if result['meetings_scheduled'] else '✗'}")
```

### Individual Onboarding Tasks

You can also use the agent to perform specific onboarding tasks:

```python
# Send just the welcome email
welcome_result = agent.send_welcome_email(new_employee)

# Create system access requests
access_result = agent.create_access_requests(new_employee)

# Schedule onboarding meetings
meetings_result = agent.schedule_onboarding_meetings(new_employee)

# Generate an onboarding plan
plan = agent.create_onboarding_plan(new_employee)
```

### Natural Language Interaction

The Onboarding Agent supports natural language queries:

```python
# Ask the agent about onboarding a new employee
response = agent.ask("What kind of welcome email will be sent to Jane?", 
                    {"employee": {"name": "Jane Smith"}})
print(response)

# Ask about scheduling
response = agent.ask("Can you schedule all the necessary onboarding meetings?", 
                    {"employee": {"name": "Jane Smith"}})
print(response)
```

## Integration with HR Multi-Agent System

The Onboarding Agent is integrated with the HR Multi-Agent system and can be accessed through the root agent:

```python
from HR_root_agent.agent import root_agent

# Use the root agent to access the onboarding agent
response = root_agent.ask("Please help me onboard our new employee Jane Smith who's starting as a Software Engineer on October 15th.")
```

## Customization

The Onboarding Agent can be customized with company-specific templates and processes:

1. **Email Templates**: The agent uses a set of default email templates that can be customized.
2. **Onboarding Checklists**: The default onboarding checklists can be expanded or modified.
3. **System Access Templates**: The list of required system access can be customized by department.

## Demo Mode

For demonstration purposes, a demo version of the Onboarding Agent is provided that simulates the onboarding process without requiring actual integrations with email or calendar systems.

To try the demo:

```bash
python onboarding_agent_demo.py
```

This will simulate the onboarding process for a sample employee and display the results.

## Implementation Details

The Onboarding Agent is implemented as a Python class with the following key methods:

- `create_onboarding_plan()`: Creates a comprehensive onboarding plan
- `send_welcome_email()`: Generates and sends welcome emails
- `schedule_onboarding_meetings()`: Creates calendar invitations for meetings
- `create_access_requests()`: Generates system access requests
- `complete_onboarding_process()`: Executes the complete onboarding workflow
- `ask()`: Processes natural language queries about onboarding

In a production environment, the agent would integrate with:

- Email systems (e.g., Gmail, Outlook)
- Calendar systems (e.g., Google Calendar, Microsoft Exchange)
- IT ticketing systems
- HR management systems
- Learning management systems
