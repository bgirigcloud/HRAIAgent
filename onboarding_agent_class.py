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
        return {
            "employee": employee_info,
            "tasks": [
                {"task": "Complete employment paperwork", "timeline": "Before start date", "responsible": "Employee", "status": "Pending"},
                {"task": "Prepare workstation", "timeline": "1 day before", "responsible": "IT", "status": "Pending"},
                {"task": "Set up email account", "timeline": "1 day before", "responsible": "IT", "status": "Pending"},
                # Additional tasks would be included here
            ],
            "system_access": [
                "Email account",
                "Intranet access",
                "HR system access",
                # Additional system access would be included here
            ],
            "schedule": [
                {
                    "day": "Day 1",
                    "date": employee_info.get("start_date", ""),
                    "events": [
                        "9:00 AM - Welcome and Check-in with HR Representative (30 min)",
                        "9:30 AM - HR Paperwork & Overview with HR Representative (1 hour)",
                        # Additional events would be included here
                    ]
                },
                # Additional days would be included here
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
                # Additional meetings would be included here
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
                # Additional access requests would be included here
            ]
        }
    
    def complete_onboarding_process(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete onboarding process."""
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
                "schedule": [
                    {
                        "day": "Day 1",
                        "date": employee_info.get("start_date", ""),
                        "events": [
                            "9:00 AM - Welcome and Check-in with HR Representative (30 min)",
                            "9:30 AM - HR Paperwork & Overview with HR Representative (1 hour)",
                            # Additional events would be included here
                        ]
                    },
                    # Additional days would be included here
                ],
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
                    }
                }
            }
        }
