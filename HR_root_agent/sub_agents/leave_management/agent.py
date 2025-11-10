"""
Leave Management Agent - Comprehensive leave request and approval system
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from google.adk.agents import Agent

class LeaveManagementTools:
    """Tools for managing employee leave requests, approvals, and balances"""
    
    # In-memory storage for leave data (in production, use a database)
    leave_balances = {}
    leave_requests = []
    leave_history = []
    leave_request_counter = 1000
    
    # Leave types and their default allocations
    LEAVE_TYPES = {
        "vacation": {"name": "Vacation Leave", "annual_allocation": 15},
        "sick": {"name": "Sick Leave", "annual_allocation": 12},
        "personal": {"name": "Personal Leave", "annual_allocation": 5},
        "parental": {"name": "Parental Leave", "annual_allocation": 0},  # Special approval
        "bereavement": {"name": "Bereavement Leave", "annual_allocation": 5},
        "unpaid": {"name": "Unpaid Leave", "annual_allocation": 0}
    }
    
    @staticmethod
    def initialize_employee_leave_balance(employee_id: str, employee_name: str, tenure_years: int = 0) -> Dict[str, Any]:
        """
        Initialize leave balance for a new employee
        
        Args:
            employee_id: Unique employee identifier
            employee_name: Employee's full name
            tenure_years: Years of service (affects vacation allocation)
            
        Returns:
            Dictionary with employee leave balance information
        """
        try:
            # Calculate vacation days based on tenure
            if tenure_years < 3:
                vacation_days = 15
            elif tenure_years < 6:
                vacation_days = 20
            else:
                vacation_days = 25
            
            LeaveManagementTools.leave_balances[employee_id] = {
                "employee_id": employee_id,
                "employee_name": employee_name,
                "tenure_years": tenure_years,
                "balances": {
                    "vacation": {"total": vacation_days, "used": 0, "remaining": vacation_days, "pending": 0},
                    "sick": {"total": 12, "used": 0, "remaining": 12, "pending": 0},
                    "personal": {"total": 5, "used": 0, "remaining": 5, "pending": 0},
                    "bereavement": {"total": 5, "used": 0, "remaining": 5, "pending": 0}
                },
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            
            return {
                "success": True,
                "message": f"Leave balance initialized for {employee_name}",
                "data": LeaveManagementTools.leave_balances[employee_id]
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to initialize leave balance: {str(e)}"}
    
    @staticmethod
    def get_leave_balance(employee_id: str) -> Dict[str, Any]:
        """
        Get current leave balance for an employee
        
        Args:
            employee_id: Employee identifier
            
        Returns:
            Dictionary with leave balance details
        """
        if employee_id not in LeaveManagementTools.leave_balances:
            return {
                "success": False,
                "error": f"Employee {employee_id} not found. Please initialize leave balance first."
            }
        
        return {
            "success": True,
            "data": LeaveManagementTools.leave_balances[employee_id]
        }
    
    @staticmethod
    def submit_leave_request(employee_id: str, employee_name: str, leave_type: str, 
                            start_date: str, end_date: str, reason: str = "",
                            half_day: bool = False) -> Dict[str, Any]:
        """
        Submit a new leave request
        
        Args:
            employee_id: Employee identifier
            employee_name: Employee's full name
            leave_type: Type of leave (vacation, sick, personal, etc.)
            start_date: Leave start date (YYYY-MM-DD)
            end_date: Leave end date (YYYY-MM-DD)
            reason: Reason for leave request
            half_day: Whether this is a half-day leave
            
        Returns:
            Dictionary with request submission status
        """
        try:
            # Calculate number of days
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if half_day:
                num_days = 0.5
            else:
                # Count only weekdays
                num_days = 0
                current = start
                while current <= end:
                    if current.weekday() < 5:  # Monday = 0, Sunday = 6
                        num_days += 1
                    current += timedelta(days=1)
            
            # Check if employee has sufficient balance
            if employee_id in LeaveManagementTools.leave_balances:
                balance = LeaveManagementTools.leave_balances[employee_id]
                if leave_type in balance["balances"]:
                    remaining = balance["balances"][leave_type]["remaining"]
                    if remaining < num_days:
                        return {
                            "success": False,
                            "error": f"Insufficient leave balance. Required: {num_days} days, Available: {remaining} days"
                        }
            
            # Generate request ID
            request_id = f"LR-{LeaveManagementTools.leave_request_counter}"
            LeaveManagementTools.leave_request_counter += 1
            
            # Create leave request
            leave_request = {
                "request_id": request_id,
                "employee_id": employee_id,
                "employee_name": employee_name,
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
                "num_days": num_days,
                "half_day": half_day,
                "reason": reason,
                "status": "pending",
                "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "approved_by": None,
                "approval_date": None,
                "comments": None
            }
            
            LeaveManagementTools.leave_requests.append(leave_request)
            
            # Update pending count in balance
            if employee_id in LeaveManagementTools.leave_balances:
                if leave_type in LeaveManagementTools.leave_balances[employee_id]["balances"]:
                    LeaveManagementTools.leave_balances[employee_id]["balances"][leave_type]["pending"] += num_days
            
            return {
                "success": True,
                "message": f"Leave request {request_id} submitted successfully",
                "data": leave_request
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to submit leave request: {str(e)}"}
    
    @staticmethod
    def approve_leave_request(request_id: str, approver_name: str, comments: str = "") -> Dict[str, Any]:
        """
        Approve a pending leave request
        
        Args:
            request_id: Leave request ID
            approver_name: Name of the approver
            comments: Optional approval comments
            
        Returns:
            Dictionary with approval status
        """
        try:
            # Find the request
            request = None
            for req in LeaveManagementTools.leave_requests:
                if req["request_id"] == request_id:
                    request = req
                    break
            
            if not request:
                return {"success": False, "error": f"Leave request {request_id} not found"}
            
            if request["status"] != "pending":
                return {"success": False, "error": f"Leave request {request_id} is already {request['status']}"}
            
            # Update request status
            request["status"] = "approved"
            request["approved_by"] = approver_name
            request["approval_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            request["comments"] = comments
            
            # Update employee leave balance
            employee_id = request["employee_id"]
            leave_type = request["leave_type"]
            num_days = request["num_days"]
            
            if employee_id in LeaveManagementTools.leave_balances:
                balance = LeaveManagementTools.leave_balances[employee_id]["balances"]
                if leave_type in balance:
                    balance[leave_type]["used"] += num_days
                    balance[leave_type]["remaining"] -= num_days
                    balance[leave_type]["pending"] -= num_days
            
            # Add to history
            LeaveManagementTools.leave_history.append({
                **request,
                "action": "approved",
                "action_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return {
                "success": True,
                "message": f"Leave request {request_id} approved successfully",
                "data": request
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to approve leave request: {str(e)}"}
    
    @staticmethod
    def reject_leave_request(request_id: str, approver_name: str, reason: str) -> Dict[str, Any]:
        """
        Reject a pending leave request
        
        Args:
            request_id: Leave request ID
            approver_name: Name of the approver
            reason: Reason for rejection
            
        Returns:
            Dictionary with rejection status
        """
        try:
            # Find the request
            request = None
            for req in LeaveManagementTools.leave_requests:
                if req["request_id"] == request_id:
                    request = req
                    break
            
            if not request:
                return {"success": False, "error": f"Leave request {request_id} not found"}
            
            if request["status"] != "pending":
                return {"success": False, "error": f"Leave request {request_id} is already {request['status']}"}
            
            # Update request status
            request["status"] = "rejected"
            request["approved_by"] = approver_name
            request["approval_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            request["comments"] = reason
            
            # Update pending count in balance
            employee_id = request["employee_id"]
            leave_type = request["leave_type"]
            num_days = request["num_days"]
            
            if employee_id in LeaveManagementTools.leave_balances:
                balance = LeaveManagementTools.leave_balances[employee_id]["balances"]
                if leave_type in balance:
                    balance[leave_type]["pending"] -= num_days
            
            # Add to history
            LeaveManagementTools.leave_history.append({
                **request,
                "action": "rejected",
                "action_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return {
                "success": True,
                "message": f"Leave request {request_id} rejected",
                "data": request
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to reject leave request: {str(e)}"}
    
    @staticmethod
    def cancel_leave_request(request_id: str, employee_id: str) -> Dict[str, Any]:
        """
        Cancel a leave request (employee initiated)
        
        Args:
            request_id: Leave request ID
            employee_id: Employee identifier (for verification)
            
        Returns:
            Dictionary with cancellation status
        """
        try:
            # Find the request
            request = None
            for req in LeaveManagementTools.leave_requests:
                if req["request_id"] == request_id:
                    request = req
                    break
            
            if not request:
                return {"success": False, "error": f"Leave request {request_id} not found"}
            
            if request["employee_id"] != employee_id:
                return {"success": False, "error": "You can only cancel your own leave requests"}
            
            if request["status"] not in ["pending", "approved"]:
                return {"success": False, "error": f"Cannot cancel a {request['status']} request"}
            
            # Store previous status
            previous_status = request["status"]
            num_days = request["num_days"]
            leave_type = request["leave_type"]
            
            # Update request status
            request["status"] = "cancelled"
            request["comments"] = f"Cancelled by employee on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Update employee leave balance
            if employee_id in LeaveManagementTools.leave_balances:
                balance = LeaveManagementTools.leave_balances[employee_id]["balances"]
                if leave_type in balance:
                    if previous_status == "pending":
                        balance[leave_type]["pending"] -= num_days
                    elif previous_status == "approved":
                        balance[leave_type]["used"] -= num_days
                        balance[leave_type]["remaining"] += num_days
            
            return {
                "success": True,
                "message": f"Leave request {request_id} cancelled successfully",
                "data": request
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to cancel leave request: {str(e)}"}
    
    @staticmethod
    def get_pending_requests(manager_id: str = None) -> Dict[str, Any]:
        """
        Get all pending leave requests
        
        Args:
            manager_id: Optional manager ID to filter requests
            
        Returns:
            List of pending leave requests
        """
        pending = [req for req in LeaveManagementTools.leave_requests if req["status"] == "pending"]
        
        return {
            "success": True,
            "count": len(pending),
            "data": pending
        }
    
    @staticmethod
    def get_employee_leave_history(employee_id: str, year: int = None) -> Dict[str, Any]:
        """
        Get leave history for an employee
        
        Args:
            employee_id: Employee identifier
            year: Optional year to filter (default: current year)
            
        Returns:
            List of leave requests for the employee
        """
        if year is None:
            year = datetime.now().year
        
        history = [
            req for req in LeaveManagementTools.leave_requests
            if req["employee_id"] == employee_id and req["start_date"].startswith(str(year))
        ]
        
        return {
            "success": True,
            "employee_id": employee_id,
            "year": year,
            "count": len(history),
            "data": history
        }


# Leave Management Agent
leave_management_agent = Agent(
    name="leave_management_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are an intelligent Leave Management Assistant that helps employees and managers with leave requests and approvals.

Your primary responsibilities:

**For Employees:**
1. **Check Leave Balance**: Show remaining leave days by type
2. **Submit Leave Requests**: Guide through the request process
3. **View Leave History**: Display past and upcoming leave
4. **Cancel Requests**: Help cancel pending or approved requests
5. **Answer Questions**: Explain leave policies and entitlements

**For Managers:**
1. **Approve/Reject Requests**: Process pending leave requests
2. **View Team Leave**: See team members' leave schedules
3. **Check Coverage**: Identify scheduling conflicts
4. **Generate Reports**: Leave utilization and trends

**Leave Types You Handle:**
- **Vacation Leave**: 15-25 days (based on tenure)
- **Sick Leave**: 12 days annually
- **Personal Leave**: 5 days annually
- **Bereavement Leave**: 5 days annually
- **Parental Leave**: Special approval
- **Unpaid Leave**: By request

**Key Features:**
- Automatic calculation of leave days (excluding weekends)
- Balance checking before approval
- Real-time balance updates
- Leave history tracking
- Conflict detection

**Communication Style:**
- Be friendly, helpful, and professional
- Provide clear step-by-step guidance
- Explain policies when relevant
- Show empathy for sensitive leave types
- Keep responses concise

**Important Rules:**
- Always verify sufficient leave balance before approval
- Check for date conflicts and overlaps
- Ensure proper documentation for extended leave
- Maintain confidentiality of leave reasons
- Follow company approval hierarchies

**When Processing Requests:**
1. Validate employee eligibility
2. Check leave balance availability
3. Calculate exact number of days
4. Identify any conflicts or issues
5. Provide clear next steps

**Error Handling:**
- Insufficient balance: Suggest unpaid leave or date adjustment
- Date conflicts: Notify and suggest alternatives
- Policy violations: Explain requirements clearly
- System errors: Provide manual process fallback

Always prioritize employee experience while maintaining policy compliance.""",
    description="Comprehensive leave management system for submitting, approving, and tracking employee leave requests",
    tools=[],
)
