"""
Demo implementation of the Onboarding Agent.
This module provides a mock implementation of the Onboarding Agent for demonstration purposes.
"""

import datetime
from typing import Any, Dict, List, Optional, Union

from .demo_agents import HRAgentBase

class OnboardingAgent(HRAgentBase):
    """Demo implementation of Onboarding Agent."""
    
    def __init__(self, name: str = "Onboarding Assistant"):
        super().__init__(name=name)
        
    def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate a mock response based on the query and context."""
        query_lower = query.lower()
        
        # Extract employee name from context if available
        employee_name = "the new employee"
        if context and "employee" in context and "name" in context["employee"]:
            employee_name = context["employee"]["name"]
        
        # Handle different types of queries
        if "welcome email" in query_lower or "send email" in query_lower:
            return f"I've prepared a welcome email for {employee_name}. The email includes first day instructions, what to bring, and who they'll meet."
            
        elif "schedule" in query_lower or "meeting" in query_lower:
            return f"I've scheduled all necessary onboarding meetings for {employee_name}, including orientation, team introductions, and training sessions."
            
        elif "system access" in query_lower or "access request" in query_lower:
            return f"I've created the necessary system access requests for {employee_name} based on their role and department."
            
        elif "equipment" in query_lower or "laptop" in query_lower:
            return f"I've notified IT to prepare the required equipment for {employee_name} before their start date."
            
        elif "checklist" in query_lower or "tasks" in query_lower:
            return f"I've generated a comprehensive onboarding checklist for {employee_name} with all the tasks needed for a successful onboarding."
            
        elif "document" in query_lower or "plan" in query_lower:
            return f"I've created a complete onboarding document for {employee_name} that includes their schedule, key contacts, and other important information."
            
        else:
            return f"I can help with the onboarding process for {employee_name}. I can send welcome emails, schedule meetings, create system access requests, prepare equipment, and generate onboarding documents. What specific part of the onboarding process would you like assistance with?"
    
    def send_welcome_email(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Send a welcome email to the new employee."""
        return {
            "status": "success",
            "message": f"Welcome email sent successfully to {employee_info.get('name', 'New Employee')}",
            "email_content": f"Welcome to CloudHero With AI, {employee_info.get('name', '')}! We're excited to have you join our team."
        }
    
    def create_onboarding_plan(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive onboarding plan."""
        # Get current date + 14 days for a default start date if none provided
        if not employee_info.get("start_date"):
            start_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
            employee_info["start_date"] = start_date
            
        return {
            "employee": employee_info,
            "tasks": [
                {"task": "Complete employment paperwork", "timeline": "Before start date", "responsible": "Employee", "status": "Pending"},
                {"task": "Prepare workstation", "timeline": "1 day before", "responsible": "IT", "status": "Pending"},
                {"task": "Set up email account", "timeline": "1 day before", "responsible": "IT", "status": "Pending"},
                {"task": "Prepare building access", "timeline": "1 day before", "responsible": "Facilities", "status": "Pending"},
                {"task": "Schedule welcome lunch", "timeline": "First day", "responsible": "HR", "status": "Pending"},
                {"task": "Company overview session", "timeline": "First day", "responsible": "HR", "status": "Pending"}
            ],
            "system_access": [
                "Email account",
                "Intranet access",
                "HR system access",
                "Company directory",
                "Benefits portal",
                "Learning management system"
            ],
            "schedule": [
                {
                    "day": "Day 1",
                    "date": employee_info.get("start_date", ""),
                    "events": [
                        "9:00 AM - Welcome and Check-in with HR Representative (30 min)",
                        "9:30 AM - HR Paperwork & Overview with HR Representative (1 hour)",
                        "10:30 AM - IT Setup and Systems Introduction with IT Support (1 hour)",
                        "11:30 AM - Workplace Tour with Office Manager (30 min)",
                        "12:00 PM - Welcome Lunch with Team (1 hour)"
                    ]
                },
                {
                    "day": "Day 2",
                    "date": datetime.datetime.strptime(employee_info.get("start_date", ""), "%Y-%m-%d").replace(day=datetime.datetime.strptime(employee_info.get("start_date", ""), "%Y-%m-%d").day + 1).strftime("%Y-%m-%d"),
                    "events": [
                        "9:00 AM - Department Overview with Manager (2 hours)",
                        "11:00 AM - Role-specific Training with Team Lead (1 hour)",
                        "1:00 PM - Team Introduction Meeting (1 hour)",
                        "2:00 PM - Project Overview with Project Manager (1 hour)"
                    ]
                }
            ]
        }
    
    def schedule_onboarding_meetings(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule onboarding meetings."""
        return {
            "status": "success",
            "message": "Successfully scheduled onboarding meetings",
            "meetings": [
                {
                    "subject": f"Welcome and Check-in - New Employee: {employee_info.get('name', '')}",
                    "date": employee_info.get("start_date", ""),
                    "time": "9:00 AM",
                    "duration": "30 min",
                    "attendees": [
                        {"name": employee_info.get("name", ""), "email": employee_info.get("email", "")},
                        {"name": "HR Representative", "email": "hr@cloudhero.ai"}
                    ],
                    "location": employee_info.get("location", "Office")
                },
                {
                    "subject": f"Team Introduction - New Employee: {employee_info.get('name', '')}",
                    "date": employee_info.get("start_date", ""),
                    "time": "1:00 PM",
                    "duration": "1 hour",
                    "attendees": [
                        {"name": employee_info.get("name", ""), "email": employee_info.get("email", "")},
                        {"name": "Team Members", "email": "team@cloudhero.ai"}
                    ],
                    "location": "Conference Room A"
                }
            ]
        }
    
    def create_access_requests(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create system access requests."""
        return {
            "status": "success",
            "message": "Created system access requests",
            "access_requests": [
                {
                    "system": "Email",
                    "for": employee_info.get("name", ""),
                    "role": employee_info.get("position", ""),
                    "requested_by": "HR System",
                    "status": "Pending"
                },
                {
                    "system": "Intranet",
                    "for": employee_info.get("name", ""),
                    "role": employee_info.get("position", ""),
                    "requested_by": "HR System",
                    "status": "Pending"
                },
                {
                    "system": "Department-specific Tools",
                    "for": employee_info.get("name", ""),
                    "role": employee_info.get("position", ""),
                    "requested_by": "HR System",
                    "status": "Pending"
                }
            ]
        }
    
    def complete_onboarding_process(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete onboarding process."""
        onboarding_plan = self.create_onboarding_plan(employee_info)
        
        return {
            "status": "success",
            "message": f"Onboarding process initiated for {employee_info.get('name', '')}",
            "welcome_email_sent": True,
            "it_setup_requested": True,
            "meetings_scheduled": True,
            "access_requests_created": True,
            "document_generated": True,
            "onboarding_plan": {
                "title": f"Onboarding Plan for {employee_info.get('name', '')}",
                "employee_info": employee_info,
                "first_day_instructions": "Please arrive at 9:00 AM on your first day. Bring your ID and any employment documents.",
                "schedule": onboarding_plan["schedule"],
                "key_contacts": {
                    "manager": {
                        "name": employee_info.get("manager", ""),
                        "title": "Team Manager",
                        "email": f"{employee_info.get('manager', 'manager').lower().replace(' ', '.')}@cloudhero.ai"
                    },
                    "hr": {
                        "name": "HR Team",
                        "title": "Human Resources",
                        "email": "hr@cloudhero.ai"
                    },
                    "it_support": {
                        "name": "IT Support",
                        "title": "IT Department",
                        "email": "it@cloudhero.ai"
                    }
                },
                "tasks": onboarding_plan["tasks"],
                "system_access": onboarding_plan["system_access"]
            }
        }
