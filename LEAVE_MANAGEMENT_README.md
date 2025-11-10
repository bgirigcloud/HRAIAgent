# 🏖️ Leave Management System

## Overview

The Leave Management System is a comprehensive AI-powered solution for managing employee leave requests, approvals, and tracking. It provides self-service capabilities for employees and powerful management tools for supervisors.

## Features

### 👤 Employee Portal

#### 1. Leave Balance Tracking
- **Real-time Balance Display**: View current leave balance across all leave types
- **Tenure-based Allocation**: Automatic allocation based on years of service
  - 0-3 years: 15 vacation days
  - 4-7 years: 20 vacation days
  - 8+ years: 25 vacation days
- **Leave Type Breakdown**:
  - 🏖️ **Vacation**: Annual vacation leave (15-25 days based on tenure)
  - 🤒 **Sick Leave**: 12 days per year
  - 📅 **Personal**: 5 days per year
  - 🕊️ **Bereavement**: 5 days per occurrence
  - 👶 **Parental**: Configurable based on company policy
  - 💼 **Unpaid**: Unlimited (subject to approval)

#### 2. Leave Request Submission
- **Smart Date Selection**: Only weekdays counted (weekends excluded)
- **Half-Day Support**: Option to request half-day leave
- **Reason Documentation**: Text area for leave justification
- **Real-time Validation**: Checks for sufficient balance before submission
- **Request ID Generation**: Automatic unique ID generation (format: REQ-EMPXXX-YYYYMMDD)

#### 3. Leave History
- **Complete History View**: All submitted requests with status
- **Filter Options**: Filter by status (Pending/Approved/Rejected/Cancelled)
- **Status Tracking**: Real-time status updates
- **Audit Trail**: Full history of all leave transactions

### 👔 Manager Portal

#### 1. Pending Requests Dashboard
- **Centralized View**: All pending requests across the team
- **Employee Details**: Employee ID, name, and request details
- **Request Summary**: Leave type, dates, duration, and reason
- **Quick Actions**: Approve/Reject buttons with one-click actions

#### 2. Approval Workflow
- **Approve Requests**: Approve leave with automatic balance deduction
- **Reject Requests**: Reject with reason and restore pending count
- **Manager Notes**: Add comments or notes to decisions
- **Bulk Actions**: Handle multiple requests efficiently
- **Email Notifications**: Automatic notifications to employees (configured separately)

#### 3. Team Leave Overview
- **Team Calendar**: Visual representation of team leave
- **Availability Tracking**: See who's available on specific dates
- **Balance Summary**: View leave balances for all team members
- **Leave Patterns**: Identify leave trends and patterns

### 📊 Reports & Analytics

#### 1. Leave Statistics
- **Total Employees**: Count of all employees in system
- **Pending Requests**: Number of requests awaiting approval
- **Monthly Metrics**: Approved/rejected requests per month
- **Utilization Rates**: Percentage of leave used vs. allocated

#### 2. Leave Type Distribution
- **Allocation Overview**: See allocated days per leave type
- **Usage Tracking**: Track used vs. available days
- **Trend Analysis**: Identify most used leave types

#### 3. Export Capabilities
- **Leave Balances Export**: CSV/Excel export of all balances
- **History Export**: Complete leave history in CSV/Excel format
- **Custom Date Ranges**: Export data for specific periods
- **Compliance Reports**: Generate reports for audit purposes

#### 4. AI-Powered Insights
- **Natural Language Queries**: Ask questions in plain English
- **Trend Analysis**: Identify leave patterns and trends
- **Predictive Analytics**: Forecast leave utilization
- **Recommendations**: AI-suggested improvements for leave policies

## Usage Examples

### For Employees

#### Check Leave Balance
1. Navigate to **Leave Management** from the main menu
2. Go to **Employee Portal** tab
3. Click **Refresh Balance** button
4. View your current balance across all leave types

#### Submit Leave Request
1. In **Employee Portal** tab, locate **Submit Leave Request** section
2. Select **Leave Type** from dropdown
3. Choose **Start Date** and **End Date**
4. Check **Half Day Request** if applicable
5. Enter **Reason for Leave**
6. Click **Submit Request**
7. Receive confirmation with Request ID

#### View Leave History
1. In **Employee Portal** tab, scroll to **My Leave History** section
2. Click **Refresh History** button
3. View all your leave requests with status

### For Managers

#### View Pending Requests
1. Navigate to **Manager Portal** tab
2. Click **Refresh Pending** button
3. View all pending leave requests from your team

#### Approve a Request
1. Note the **Request ID** from pending requests list
2. In **Approve or Reject Requests** section, enter the **Request ID**
3. Add optional **Manager Notes**
4. Click **Approve** button
5. Employee balance automatically updated

#### Reject a Request
1. Enter **Request ID** in the approval form
2. Add **Manager Notes** with rejection reason
3. Click **Reject** button
4. Employee notified of rejection with reason

#### View Team Status
1. In **Manager Portal** tab, scroll to **Team Leave Overview**
2. Click **View Team Leave Status**
3. Expand individual employee sections to see details

### Analytics and Reporting

#### Generate Reports
1. Navigate to **Reports & Analytics** tab
2. View current **Leave Statistics** metrics
3. Review **Leave Type Distribution** table
4. Click **Export Leave Balances** or **Export Leave History** for CSV/Excel downloads

#### Get AI Insights
1. In **Reports & Analytics** tab, scroll to **AI-Powered Insights**
2. Enter your question, for example:
   - "What are the leave patterns this quarter?"
   - "Which team has highest leave utilization?"
   - "When is the best time to schedule team meetings?"
3. Click **Get Insights**
4. Review AI-generated analysis and recommendations

## Leave Types and Policies

### Vacation Leave
- **Allocation**: Tenure-based (15/20/25 days)
- **Carry Over**: Up to 5 days to next year
- **Usage**: Must provide 2 weeks notice for requests over 5 days
- **Blackout Dates**: Company-defined busy periods

### Sick Leave
- **Allocation**: 12 days per year
- **Carry Over**: Up to 10 days
- **Documentation**: Medical certificate required for 3+ consecutive days
- **Emergency**: Can be taken without prior notice

### Personal Leave
- **Allocation**: 5 days per year
- **Carry Over**: No carry over
- **Usage**: Short notice acceptable (24 hours)
- **Purpose**: Personal matters, appointments, errands

### Bereavement Leave
- **Allocation**: 5 days per occurrence
- **Family Definition**: Immediate family members
- **Extended Family**: 3 days for extended family
- **Documentation**: Death certificate may be required

### Parental Leave
- **Maternity**: 12 weeks paid
- **Paternity**: 2 weeks paid
- **Adoption**: 12 weeks paid
- **Extension**: Unpaid extension available

### Unpaid Leave
- **Approval**: Manager and HR approval required
- **Duration**: Maximum 30 days per request
- **Benefits**: Benefits may be affected for extended periods
- **Documentation**: Detailed justification required

## Technical Details

### Backend Architecture

#### LeaveManagementTools Class
Located in: `HR_root_agent/sub_agents/leave_management/agent.py`

**Core Methods:**
1. `initialize_employee_balance(employee_id, tenure_years)`: Set up initial leave balance
2. `submit_leave_request(employee_id, start_date, end_date, leave_type, reason, is_half_day)`: Create new request
3. `approve_leave_request(request_id, manager_id)`: Approve pending request
4. `reject_leave_request(request_id, manager_id, reason)`: Reject pending request
5. `cancel_leave_request(request_id, employee_id)`: Employee-initiated cancellation
6. `get_pending_requests(manager_id)`: Fetch all pending requests
7. `get_employee_leave_history(employee_id)`: Fetch employee's complete history
8. `calculate_leave_days(start_date, end_date, is_half_day)`: Calculate weekdays only
9. `get_employee_balance(employee_id)`: Fetch current leave balance
10. `update_leave_balance(employee_id, leave_type, days)`: Modify balance

#### Data Storage
- **In-Memory Storage**: Uses Python dictionaries for demo
- **Production Recommendation**: Migrate to database (PostgreSQL/MongoDB)
- **Data Structures**:
  - `leave_balances`: {employee_id: {leave_type: days}}
  - `leave_requests`: {request_id: {employee_id, start_date, end_date, ...}}
  - `leave_history`: {employee_id: [request_list]}

#### Request ID Format
- Pattern: `REQ-{employee_id}-{start_date_YYYYMMDD}`
- Example: `REQ-EMP001-20241225`
- Ensures uniqueness per employee per start date

### Frontend Integration

#### Streamlit Components
Located in: `streamlit_app.py` - `display_leave_management()` function

**UI Components:**
- **Employee Selector**: Dropdown to switch between employee profiles
- **Balance Cards**: Metric widgets showing leave balances
- **Request Form**: Multi-field form with validation
- **History Table**: Expandable sections for past requests
- **Approval Interface**: Manager-specific controls
- **Analytics Dashboard**: Charts and metrics

#### Session State Management
- `current_employee_id`: Currently selected employee
- `leave_demo_initialized`: Flag for sample data initialization
- `leave_balance_info`: Cached balance information
- `leave_history_info`: Cached history data
- `pending_requests_info`: Cached pending requests

### API Integration

#### Agent Communication
```python
# Submit leave request
response = leave_agent.send_message(
    f"Submit leave request for {employee_id} from {start_date} to {end_date} "
    f"for {leave_type} reason: {reason}"
)

# Approve request
response = leave_agent.send_message(f"Approve leave request {request_id}")

# Get balance
response = leave_agent.send_message(f"What is the leave balance for employee {employee_id}?")
```

#### Error Handling
- **Try-Catch Blocks**: All API calls wrapped in exception handling
- **User Feedback**: Clear error messages displayed in UI
- **Graceful Degradation**: Shows cached data if API fails
- **Retry Logic**: Automatic retry for transient failures

## Configuration

### Environment Variables
```bash
# Required for AI features
GOOGLE_API_KEY=your_api_key_here
PROJECT_ID=your_gcp_project_id

# Optional: Email notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Leave Policy Configuration
Edit in `HR_root_agent/sub_agents/leave_management/agent.py`:

```python
# Vacation allocation by tenure
VACATION_BY_TENURE = {
    (0, 3): 15,    # 0-3 years: 15 days
    (4, 7): 20,    # 4-7 years: 20 days
    (8, 100): 25   # 8+ years: 25 days
}

# Standard leave types
LEAVE_TYPES = {
    "Vacation": {"annual": True, "carry_over": 5},
    "Sick": {"annual": True, "carry_over": 10, "default": 12},
    "Personal": {"annual": True, "carry_over": 0, "default": 5},
    "Bereavement": {"annual": False, "default": 5},
    "Parental": {"annual": False, "configurable": True},
    "Unpaid": {"annual": False, "unlimited": True}
}
```

## Best Practices

### For Employees
1. **Plan Ahead**: Submit vacation requests at least 2 weeks in advance
2. **Check Balance**: Verify balance before submitting to avoid rejection
3. **Provide Details**: Clear reasons help managers approve faster
4. **Update Calendar**: Add approved leave to your work calendar
5. **Emergency Protocol**: For sick leave, notify manager ASAP even if after starting leave

### For Managers
1. **Timely Review**: Review pending requests within 2 business days
2. **Fair Decisions**: Apply leave policies consistently across team
3. **Communication**: Discuss concerns with employee before rejecting
4. **Team Coverage**: Ensure adequate coverage before approving multiple simultaneous requests
5. **Documentation**: Add notes to decisions for future reference

### For HR Administrators
1. **Regular Audits**: Review leave patterns quarterly
2. **Policy Updates**: Update leave policies based on analytics insights
3. **Balance Resets**: Reset annual leave balances at year-end
4. **Compliance**: Ensure policies comply with local labor laws
5. **Training**: Train managers on fair leave approval practices

## Troubleshooting

### Common Issues

#### Issue: "Insufficient leave balance"
**Cause**: Employee doesn't have enough days for requested leave type
**Solution**: 
- Check current balance with "Refresh Balance"
- Request fewer days or different leave type
- Contact HR if balance seems incorrect

#### Issue: Request not appearing in pending list
**Cause**: Request may have been auto-rejected due to validation failure
**Solution**:
- Check leave history for request status
- Verify dates are valid (not weekends/holidays)
- Ensure sufficient balance before submission

#### Issue: Cannot approve request
**Cause**: Request ID may be incorrect or already processed
**Solution**:
- Refresh pending requests list
- Verify exact Request ID (copy-paste to avoid typos)
- Check if request was already approved/rejected

#### Issue: Balance not updating after approval
**Cause**: System delay or cache issue
**Solution**:
- Click "Refresh Balance" button
- Wait a few seconds and try again
- Check leave history to confirm approval

### Support

For technical issues or questions:
1. **Employee Questions**: Contact your manager or HR department
2. **Manager Questions**: Contact HR or system administrator
3. **Technical Issues**: Create a ticket with IT support
4. **Feature Requests**: Submit via internal feedback form

## Future Enhancements

### Planned Features
1. **Email Notifications**: Automatic emails for all leave status changes
2. **Calendar Integration**: Sync with Google Calendar/Outlook
3. **Mobile App**: iOS/Android app for on-the-go access
4. **Public Holidays**: Auto-exclude company holidays from calculations
5. **Team Calendar View**: Visual calendar showing team availability
6. **Delegation**: Allow managers to delegate approval authority
7. **Recurring Leave**: Support for regular leave patterns (e.g., every Friday)
8. **Leave Swap**: Allow employees to swap leave days
9. **Approval Chain**: Multi-level approval for extended leave
10. **Compliance Alerts**: Notify HR of potential policy violations

### Integration Roadmap
- **Payroll System**: Auto-sync leave data with payroll
- **HRIS**: Bi-directional sync with HR Information System
- **Time Tracking**: Integration with time and attendance systems
- **Slack/Teams**: Chat bot for leave requests
- **SSO**: Single sign-on with corporate identity provider

## Compliance and Legal

### Data Privacy
- **GDPR Compliance**: Personal data handled per GDPR requirements
- **Data Retention**: Leave history retained for 7 years
- **Access Control**: Role-based access (Employee/Manager/HR/Admin)
- **Audit Logs**: All actions logged for compliance

### Legal Considerations
- **Labor Laws**: Policies comply with local labor regulations
- **FMLA**: US Family and Medical Leave Act compliant
- **FLSA**: Fair Labor Standards Act compliant
- **State Laws**: Configurable for state-specific requirements

## License and Support

### License
Copyright © 2024 HR Multi-Agent System. All rights reserved.

### Support Resources
- **Documentation**: This README and other guides in repository
- **API Reference**: `HR_root_agent/sub_agents/leave_management/agent.py`
- **UI Reference**: `streamlit_app.py` - `display_leave_management()` function
- **Sample Data**: Pre-loaded demo employees and requests

### Contributing
To contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit pull request with description
5. Wait for review and feedback

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Author**: HR Multi-Agent Development Team
