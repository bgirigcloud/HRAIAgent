"""
Onboarding Agent for HR AI Assistant.

This agent automates the process of welcoming new employees,
sending welcome emails, providing access to necessary systems,
and scheduling introductory meetings with team members.
"""

import os
import datetime
from typing import Dict, List, Any, Optional, Union

class OnboardingAgent:
    """Agent for automating employee onboarding processes."""
    
    def __init__(self, name: str = "Onboarding Assistant"):
        self.name = name
        self.email_templates = self._load_email_templates()
        self.onboarding_checklists = self._load_onboarding_checklists()
        self.system_access_templates = self._load_system_access_templates()
        
    def _load_email_templates(self) -> Dict[str, str]:
        """Load email templates for different onboarding communications."""
        return {
            "welcome": """
                Subject: Welcome to CloudHero With AI, {employee_name}!
                
                Dear {employee_name},
                
                Welcome to CloudHero With AI! We are thrilled to have you join our team as {position}.
                
                Your journey with us begins on {start_date}. Here's some information to help you get started:
                
                Location: {office_location}
                Reporting Manager: {manager_name}
                Team: {team_name}
                
                What to expect on your first day:
                - Arrival time: {arrival_time}
                - Please bring your ID and any employment documents
                - You'll meet with {hr_contact} from HR who will guide you through the day
                - You'll receive your equipment and access credentials
                - We've scheduled a team lunch to welcome you!
                
                Before your first day, please complete the following:
                {pre_start_tasks}
                
                If you have any questions before your start date, please contact {hr_contact} at {hr_email}.
                
                We're looking forward to having you on board!
                
                Best regards,
                {sender_name}
                {sender_title}
                CloudHero With AI
            """,
            
            "it_setup": """
                Subject: IT Setup for {employee_name} - Starting {start_date}
                
                Hello IT Team,
                
                We have a new team member, {employee_name}, joining as {position} on {start_date}.
                
                Please prepare the following equipment and access:
                
                Equipment:
                {equipment_list}
                
                System Access:
                {system_access_list}
                
                Software Requirements:
                {software_list}
                
                Special Requirements:
                {special_requirements}
                
                Please ensure everything is ready by {setup_deadline}, one day before their start date.
                
                Thank you!
                
                Best regards,
                {sender_name}
                HR Department
            """,
            
            "team_introduction": """
                Subject: Introducing Our New Team Member: {employee_name}
                
                Hello {team_name} Team,
                
                I'm excited to announce that {employee_name} will be joining our team as {position} on {start_date}.
                
                About {employee_first_name}:
                {employee_background}
                
                Please join me in welcoming {employee_first_name} to the team! We've scheduled a team lunch on {lunch_date} to give everyone a chance to meet.
                
                Best regards,
                {manager_name}
                {manager_title}
            """,
            
            "first_week": """
                Subject: Your First Week at CloudHero With AI
                
                Dear {employee_name},
                
                Congratulations on completing your first day at CloudHero With AI! We're excited to have you with us.
                
                Here's your schedule for the rest of the week:
                
                {weekly_schedule}
                
                Key People to Meet:
                {key_people}
                
                Resources to Review:
                {resources_list}
                
                Please let me know if you have any questions or need any assistance.
                
                Best regards,
                {hr_contact}
                HR Department
                CloudHero With AI
            """
        }
    
    def _load_onboarding_checklists(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load onboarding checklists for different roles and departments."""
        return {
            "general": [
                {"task": "Complete employment paperwork", "timeline": "Before start date", "responsible": "Employee", "status": "Pending"},
                {"task": "Prepare workstation", "timeline": "1 day before", "responsible": "IT", "status": "Pending"},
                {"task": "Set up email account", "timeline": "1 day before", "responsible": "IT", "status": "Pending"},
                {"task": "Prepare building access", "timeline": "1 day before", "responsible": "Facilities", "status": "Pending"},
                {"task": "Schedule welcome lunch", "timeline": "First day", "responsible": "HR", "status": "Pending"},
                {"task": "Company overview session", "timeline": "First day", "responsible": "HR", "status": "Pending"},
                {"task": "IT systems training", "timeline": "First day", "responsible": "IT", "status": "Pending"},
                {"task": "Meet with direct manager", "timeline": "First day", "responsible": "Manager", "status": "Pending"},
                {"task": "Team introductions", "timeline": "First day", "responsible": "Manager", "status": "Pending"},
                {"task": "Review job responsibilities", "timeline": "First week", "responsible": "Manager", "status": "Pending"},
                {"task": "Set initial goals", "timeline": "First week", "responsible": "Manager", "status": "Pending"},
                {"task": "Benefits enrollment", "timeline": "First week", "responsible": "HR", "status": "Pending"},
                {"task": "Security training", "timeline": "First week", "responsible": "Security", "status": "Pending"},
                {"task": "First-week check-in", "timeline": "End of first week", "responsible": "HR", "status": "Pending"},
                {"task": "30-day review scheduling", "timeline": "End of first week", "responsible": "Manager", "status": "Pending"}
            ],
            
            "engineering": [
                {"task": "Code repository access", "timeline": "First day", "responsible": "IT", "status": "Pending"},
                {"task": "Development environment setup", "timeline": "First day", "responsible": "IT", "status": "Pending"},
                {"task": "Architecture overview", "timeline": "First week", "responsible": "Tech Lead", "status": "Pending"},
                {"task": "Codebase walkthrough", "timeline": "First week", "responsible": "Team Lead", "status": "Pending"},
                {"task": "CI/CD process training", "timeline": "First week", "responsible": "DevOps", "status": "Pending"},
                {"task": "Assign first task", "timeline": "By end of first week", "responsible": "Manager", "status": "Pending"}
            ],
            
            "marketing": [
                {"task": "Brand guidelines review", "timeline": "First week", "responsible": "Creative Director", "status": "Pending"},
                {"task": "Marketing tools access", "timeline": "First day", "responsible": "IT", "status": "Pending"},
                {"task": "Campaign overview", "timeline": "First week", "responsible": "Marketing Manager", "status": "Pending"},
                {"task": "Social media access", "timeline": "First week", "responsible": "Social Media Manager", "status": "Pending"}
            ],
            
            "sales": [
                {"task": "CRM access", "timeline": "First day", "responsible": "IT", "status": "Pending"},
                {"task": "Product training", "timeline": "First week", "responsible": "Product Manager", "status": "Pending"},
                {"task": "Sales process overview", "timeline": "First week", "responsible": "Sales Manager", "status": "Pending"},
                {"task": "Client introductions", "timeline": "Second week", "responsible": "Sales Manager", "status": "Pending"}
            ],
            
            "leadership": [
                {"task": "Executive team meeting", "timeline": "First week", "responsible": "CEO", "status": "Pending"},
                {"task": "Company strategy review", "timeline": "First week", "responsible": "CEO", "status": "Pending"},
                {"task": "Department KPIs review", "timeline": "First week", "responsible": "CFO", "status": "Pending"},
                {"task": "Leadership philosophy session", "timeline": "Second week", "responsible": "CEO", "status": "Pending"}
            ]
        }
    
    def _load_system_access_templates(self) -> Dict[str, List[str]]:
        """Load templates for system access requirements by department."""
        return {
            "general": [
                "Email account",
                "Intranet access",
                "HR system access",
                "Company directory",
                "Benefits portal",
                "Learning management system",
                "Time tracking system"
            ],
            
            "engineering": [
                "GitHub/GitLab access",
                "AWS/Cloud platform access",
                "CI/CD pipeline access",
                "Project management tools (Jira/Asana)",
                "Database access (as needed)",
                "Development environments",
                "Testing environments",
                "Documentation wikis"
            ],
            
            "marketing": [
                "Marketing automation platform",
                "Analytics tools",
                "Social media accounts",
                "Content management system",
                "Design software licenses",
                "Digital asset management system",
                "Campaign tracking tools"
            ],
            
            "sales": [
                "CRM system",
                "Sales enablement platform",
                "Quote generation tools",
                "Contract management system",
                "Commission tracking system",
                "Expense reporting system"
            ],
            
            "leadership": [
                "Business intelligence dashboard",
                "Financial reporting systems",
                "Strategic planning tools",
                "Executive dashboard access",
                "Board meeting materials"
            ]
        }
        
    def create_onboarding_plan(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive onboarding plan for a new employee.
        
        Args:
            employee_info: Dictionary containing employee information including:
                - name: Employee's full name
                - position: Job title
                - department: Department they're joining
                - start_date: First day of employment
                - manager: Manager's name
                - team: Team name
                - location: Office location
                
        Returns:
            Dictionary containing the complete onboarding plan
        """
        department = employee_info.get("department", "").lower()
        
        # Determine which checklists to include
        checklists = ["general"]
        if department in ["engineering", "development", "qa", "devops"]:
            checklists.append("engineering")
        elif department in ["marketing", "communications", "pr"]:
            checklists.append("marketing")
        elif department in ["sales", "business development"]:
            checklists.append("sales")
        elif department in ["executive", "director", "vp"]:
            checklists.append("leadership")
            
        # Combine appropriate checklists
        tasks = []
        for checklist_name in checklists:
            if checklist_name in self.onboarding_checklists:
                tasks.extend(self.onboarding_checklists[checklist_name])
        
        # Determine system access requirements
        system_access = self.system_access_templates.get("general", []).copy()
        for checklist_name in checklists:
            if checklist_name != "general" and checklist_name in self.system_access_templates:
                system_access.extend(self.system_access_templates[checklist_name])
        
        # Create schedule
        start_date = datetime.datetime.strptime(employee_info.get("start_date", ""), "%Y-%m-%d")
        schedule = self._generate_first_week_schedule(start_date, department, employee_info)
        
        # Create onboarding plan
        return {
            "employee": employee_info,
            "tasks": tasks,
            "system_access": system_access,
            "schedule": schedule,
            "email_templates": self._prepare_email_templates(employee_info),
            "key_contacts": self._identify_key_contacts(employee_info)
        }
    
    def _generate_first_week_schedule(self, start_date: datetime.datetime, 
                                     department: str, employee_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate a schedule for the employee's first week."""
        schedule = []
        
        # Day 1 - Orientation
        day1 = start_date
        schedule.append({
            "day": "Day 1",
            "date": day1.strftime("%Y-%m-%d"),
            "events": [
                {"time": "09:00 AM", "duration": "30 min", "activity": "Welcome and Check-in", "with": "HR Representative"},
                {"time": "09:30 AM", "duration": "1 hour", "activity": "HR Paperwork & Overview", "with": "HR Representative"},
                {"time": "10:30 AM", "duration": "1 hour", "activity": "IT Setup and Systems Introduction", "with": "IT Support"},
                {"time": "11:30 AM", "duration": "30 min", "activity": "Workplace Tour", "with": "Office Manager"},
                {"time": "12:00 PM", "duration": "1 hour", "activity": "Welcome Lunch", "with": f"Team and {employee_info.get('manager', 'Manager')}"},
                {"time": "01:00 PM", "duration": "1 hour", "activity": "Meeting with Manager", "with": employee_info.get("manager", "Manager")},
                {"time": "02:00 PM", "duration": "1 hour", "activity": "Company Overview", "with": "HR Representative"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Team Introductions", "with": "Team Members"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Setup Workspace & Review Materials", "with": "Self-guided"}
            ]
        })
        
        # Day 2 - Department specific
        day2 = start_date + datetime.timedelta(days=1)
        
        if department in ["engineering", "development", "qa", "devops"]:
            day2_events = [
                {"time": "09:00 AM", "duration": "1 hour", "activity": "Development Environment Setup", "with": "IT Support"},
                {"time": "10:00 AM", "duration": "2 hours", "activity": "Technical Overview", "with": "Tech Lead"},
                {"time": "01:00 PM", "duration": "2 hours", "activity": "Codebase Introduction", "with": "Senior Developer"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Development Processes", "with": "Project Manager"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Day 2 Check-in", "with": employee_info.get("manager", "Manager")}
            ]
        elif department in ["marketing", "communications", "pr"]:
            day2_events = [
                {"time": "09:00 AM", "duration": "2 hours", "activity": "Marketing Strategy Overview", "with": "Marketing Director"},
                {"time": "11:00 AM", "duration": "1 hour", "activity": "Brand Guidelines", "with": "Brand Manager"},
                {"time": "01:00 PM", "duration": "2 hours", "activity": "Marketing Tools Training", "with": "Marketing Operations"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Current Campaigns Review", "with": "Campaign Manager"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Day 2 Check-in", "with": employee_info.get("manager", "Manager")}
            ]
        elif department in ["sales", "business development"]:
            day2_events = [
                {"time": "09:00 AM", "duration": "2 hours", "activity": "Sales Process Overview", "with": "Sales Director"},
                {"time": "11:00 AM", "duration": "1 hour", "activity": "CRM Training", "with": "Sales Operations"},
                {"time": "01:00 PM", "duration": "2 hours", "activity": "Product Training", "with": "Product Manager"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Sales Targets & Commissions", "with": "Sales Manager"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Day 2 Check-in", "with": employee_info.get("manager", "Manager")}
            ]
        else:
            # General schedule for other departments
            day2_events = [
                {"time": "09:00 AM", "duration": "2 hours", "activity": "Department Overview", "with": "Department Head"},
                {"time": "11:00 AM", "duration": "1 hour", "activity": "Tools & Systems Training", "with": "Team Lead"},
                {"time": "01:00 PM", "duration": "2 hours", "activity": "Role-specific Training", "with": "Senior Team Member"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Process Overview", "with": "Process Manager"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Day 2 Check-in", "with": employee_info.get("manager", "Manager")}
            ]
        
        schedule.append({
            "day": "Day 2",
            "date": day2.strftime("%Y-%m-%d"),
            "events": day2_events
        })
        
        # Day 3 - Training and Projects
        day3 = start_date + datetime.timedelta(days=2)
        schedule.append({
            "day": "Day 3",
            "date": day3.strftime("%Y-%m-%d"),
            "events": [
                {"time": "09:00 AM", "duration": "2 hours", "activity": "In-depth Training", "with": "Senior Team Member"},
                {"time": "11:00 AM", "duration": "1 hour", "activity": "Project Introduction", "with": "Project Manager"},
                {"time": "01:00 PM", "duration": "2 hours", "activity": "Role-specific Work", "with": "Self-guided"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Company Policies Review", "with": "HR Representative"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Day 3 Check-in", "with": employee_info.get("manager", "Manager")}
            ]
        })
        
        # Day 4 - Team Integration
        day4 = start_date + datetime.timedelta(days=3)
        schedule.append({
            "day": "Day 4",
            "date": day4.strftime("%Y-%m-%d"),
            "events": [
                {"time": "09:00 AM", "duration": "1 hour", "activity": "Team Meeting", "with": "Entire Team"},
                {"time": "10:00 AM", "duration": "2 hours", "activity": "Shadowing Colleague", "with": "Peer"},
                {"time": "01:00 PM", "duration": "2 hours", "activity": "First Assignment Work", "with": "Self-guided"},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "Cross-department Introduction", "with": "Partner Teams"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Day 4 Check-in", "with": employee_info.get("manager", "Manager")}
            ]
        })
        
        # Day 5 - Wrap up First Week
        day5 = start_date + datetime.timedelta(days=4)
        schedule.append({
            "day": "Day 5",
            "date": day5.strftime("%Y-%m-%d"),
            "events": [
                {"time": "09:00 AM", "duration": "2 hours", "activity": "Continue Assignment", "with": "Self-guided"},
                {"time": "11:00 AM", "duration": "1 hour", "activity": "Benefits Enrollment Session", "with": "HR Representative"},
                {"time": "01:00 PM", "duration": "1 hour", "activity": "Security Training", "with": "Security Officer"},
                {"time": "02:00 PM", "duration": "1 hour", "activity": "First Week Review", "with": employee_info.get("manager", "Manager")},
                {"time": "03:00 PM", "duration": "1 hour", "activity": "HR Check-in", "with": "HR Representative"},
                {"time": "04:00 PM", "duration": "1 hour", "activity": "Team Social (optional)", "with": "Team"}
            ]
        })
        
        return schedule
    
    def _prepare_email_templates(self, employee_info: Dict[str, Any]) -> Dict[str, str]:
        """Prepare email templates with employee information."""
        emails = {}
        
        # Employee's first name
        first_name = employee_info.get("name", "").split()[0] if employee_info.get("name") else ""
        
        # Welcome email
        welcome_email = self.email_templates["welcome"].format(
            employee_name=employee_info.get("name", ""),
            position=employee_info.get("position", ""),
            start_date=employee_info.get("start_date", ""),
            office_location=employee_info.get("location", "Our office"),
            manager_name=employee_info.get("manager", "Your Manager"),
            team_name=employee_info.get("team", "Our Team"),
            arrival_time="9:00 AM",
            hr_contact="HR Team",
            hr_email="hr@cloudhero.ai",
            pre_start_tasks="- Complete the onboarding forms sent to your email\n- Review the company handbook\n- Prepare any questions you might have",
            sender_name="HR Team",
            sender_title="Human Resources"
        )
        emails["welcome"] = welcome_email
        
        # IT Setup email
        it_email = self.email_templates["it_setup"].format(
            employee_name=employee_info.get("name", ""),
            position=employee_info.get("position", ""),
            start_date=employee_info.get("start_date", ""),
            equipment_list="- Laptop (Standard dev configuration)\n- Monitor\n- Keyboard and mouse\n- Headset",
            system_access_list="- Email account\n- VPN access\n- Project management tools\n- Code repositories",
            software_list="- Development tools\n- Communication tools\n- Project management software",
            special_requirements="None",
            setup_deadline="[Setup deadline]",
            sender_name="HR Team"
        )
        emails["it_setup"] = it_email
        
        # Team introduction email
        team_intro = self.email_templates["team_introduction"].format(
            employee_name=employee_info.get("name", ""),
            employee_first_name=first_name,
            position=employee_info.get("position", ""),
            start_date=employee_info.get("start_date", ""),
            team_name=employee_info.get("team", ""),
            employee_background=f"{first_name} comes to us with experience in [background details]. They'll be focusing on [responsibilities].",
            lunch_date="[Lunch date]",
            manager_name=employee_info.get("manager", ""),
            manager_title="Team Manager"
        )
        emails["team_introduction"] = team_intro
        
        # First week email
        first_week = self.email_templates["first_week"].format(
            employee_name=employee_info.get("name", ""),
            weekly_schedule="Monday: Orientation and Team Introductions\nTuesday: Systems Training\nWednesday: Role-specific Training\nThursday: Project Introduction\nFriday: First Week Review",
            key_people="- Your Manager: [Manager Name], [Manager Title]\n- Your Buddy: [Buddy Name], [Buddy Title]\n- HR Contact: [HR Contact], Human Resources",
            resources_list="- Company Handbook\n- Department Documentation\n- Training Materials",
            hr_contact="HR Team"
        )
        emails["first_week"] = first_week
        
        return emails
    
    def _identify_key_contacts(self, employee_info: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Identify key contacts for the new employee."""
        department = employee_info.get("department", "").lower()
        
        contacts = {
            "manager": {
                "name": employee_info.get("manager", ""),
                "title": "Team Manager",
                "email": f"{employee_info.get('manager', 'manager').lower().replace(' ', '.')}@cloudhero.ai",
                "phone": "123-456-7890"
            },
            "hr": {
                "name": "HR Team",
                "title": "Human Resources",
                "email": "hr@cloudhero.ai",
                "phone": "123-456-7891"
            },
            "it_support": {
                "name": "IT Support",
                "title": "IT Department",
                "email": "it@cloudhero.ai",
                "phone": "123-456-7892"
            }
        }
        
        # Add department-specific contacts
        if department in ["engineering", "development", "qa", "devops"]:
            contacts["tech_lead"] = {
                "name": "Tech Lead",
                "title": "Technical Lead",
                "email": "techlead@cloudhero.ai",
                "phone": "123-456-7893"
            }
        elif department in ["marketing", "communications", "pr"]:
            contacts["creative_director"] = {
                "name": "Creative Director",
                "title": "Creative Director",
                "email": "creative@cloudhero.ai",
                "phone": "123-456-7894"
            }
        elif department in ["sales", "business development"]:
            contacts["sales_director"] = {
                "name": "Sales Director",
                "title": "Sales Director",
                "email": "sales.director@cloudhero.ai",
                "phone": "123-456-7895"
            }
        
        # Add onboarding buddy
        contacts["buddy"] = {
            "name": "Onboarding Buddy",
            "title": "Team Member",
            "email": "buddy@cloudhero.ai",
            "phone": "123-456-7896"
        }
        
        return contacts
    
    def send_welcome_email(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a welcome email to the new employee.
        
        In a real implementation, this would connect to an email service.
        For demo purposes, it returns the email content.
        """
        onboarding_plan = self.create_onboarding_plan(employee_info)
        
        # In a real implementation, this would send the actual email
        return {
            "status": "success",
            "message": "Welcome email sent successfully",
            "email_content": onboarding_plan["email_templates"]["welcome"]
        }
    
    def send_it_setup_request(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send IT setup request for the new employee.
        
        In a real implementation, this would create tickets or send emails to IT.
        For demo purposes, it returns the email content.
        """
        onboarding_plan = self.create_onboarding_plan(employee_info)
        
        # In a real implementation, this would create IT tickets
        return {
            "status": "success",
            "message": "IT setup request created successfully",
            "email_content": onboarding_plan["email_templates"]["it_setup"]
        }
    
    def schedule_onboarding_meetings(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule onboarding meetings for the new employee.
        
        In a real implementation, this would interact with a calendar system.
        For demo purposes, it returns the meeting schedule.
        """
        onboarding_plan = self.create_onboarding_plan(employee_info)
        
        # Extract meetings from the schedule
        meetings = []
        for day in onboarding_plan["schedule"]:
            for event in day["events"]:
                if "with" in event and event["with"] not in ["Self-guided"]:
                    meetings.append({
                        "subject": f"{event['activity']} - New Employee: {employee_info.get('name', '')}",
                        "date": day["date"],
                        "time": event["time"],
                        "duration": event["duration"],
                        "attendees": [
                            {"name": employee_info.get("name", ""), "email": employee_info.get("email", "")},
                            {"name": event["with"], "email": f"{event['with'].replace(' ', '.').lower()}@cloudhero.ai"}
                        ],
                        "location": employee_info.get("location", "Office") if "lunch" not in event["activity"].lower() else "Company Cafeteria"
                    })
        
        # In a real implementation, this would create calendar events
        return {
            "status": "success",
            "message": f"Successfully scheduled {len(meetings)} onboarding meetings",
            "meetings": meetings
        }
    
    def create_access_requests(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create access requests for required systems.
        
        In a real implementation, this would create tickets for system access.
        For demo purposes, it returns the access requests.
        """
        onboarding_plan = self.create_onboarding_plan(employee_info)
        
        # In a real implementation, this would create access request tickets
        return {
            "status": "success",
            "message": f"Created {len(onboarding_plan['system_access'])} system access requests",
            "access_requests": [
                {
                    "system": system,
                    "for": employee_info.get("name", ""),
                    "role": employee_info.get("position", ""),
                    "requested_by": "HR System",
                    "status": "Pending"
                }
                for system in onboarding_plan["system_access"]
            ]
        }
    
    def generate_onboarding_document(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive onboarding document for the employee.
        
        This would typically be a PDF or Word document with all relevant information.
        For demo purposes, it returns structured data.
        """
        onboarding_plan = self.create_onboarding_plan(employee_info)
        
        # Format the first week schedule for display
        formatted_schedule = []
        for day in onboarding_plan["schedule"]:
            day_schedule = {
                "day": day["day"],
                "date": day["date"],
                "events": []
            }
            
            for event in day["events"]:
                day_schedule["events"].append(
                    f"{event['time']} - {event['activity']} with {event['with']} ({event['duration']})"
                )
            
            formatted_schedule.append(day_schedule)
        
        # Format the onboarding checklist for display
        formatted_checklist = []
        for task in onboarding_plan["tasks"]:
            formatted_checklist.append({
                "task": task["task"],
                "timeline": task["timeline"],
                "responsible": task["responsible"]
            })
        
        # Prepare the document content
        document = {
            "title": f"Onboarding Plan for {employee_info.get('name', '')}",
            "employee_info": {
                "name": employee_info.get("name", ""),
                "position": employee_info.get("position", ""),
                "department": employee_info.get("department", ""),
                "start_date": employee_info.get("start_date", ""),
                "manager": employee_info.get("manager", ""),
                "location": employee_info.get("location", "")
            },
            "welcome_message": f"Welcome to CloudHero With AI, {employee_info.get('name', '')}! We're excited to have you join us as our new {employee_info.get('position', '')}. This document contains all the information you need for a successful onboarding experience.",
            "first_day_instructions": "Please arrive at 9:00 AM on your first day. Bring your ID and any employment documents. You'll be greeted by a member of our HR team who will guide you through the day.",
            "schedule": formatted_schedule,
            "key_contacts": onboarding_plan["key_contacts"],
            "onboarding_checklist": formatted_checklist,
            "systems_access": onboarding_plan["system_access"]
        }
        
        # In a real implementation, this would generate a PDF or Word document
        return {
            "status": "success",
            "message": "Onboarding document generated successfully",
            "document": document
        }
    
    def complete_onboarding_process(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete onboarding process for a new employee.
        
        This combines all the onboarding steps into a single operation.
        """
        try:
            welcome_email = self.send_welcome_email(employee_info)
            it_setup = self.send_it_setup_request(employee_info)
            meetings = self.schedule_onboarding_meetings(employee_info)
            access = self.create_access_requests(employee_info)
            document = self.generate_onboarding_document(employee_info)
            
            return {
                "status": "success",
                "message": f"Onboarding process initiated for {employee_info.get('name', '')}",
                "welcome_email_sent": welcome_email["status"] == "success",
                "it_setup_requested": it_setup["status"] == "success",
                "meetings_scheduled": meetings["status"] == "success",
                "access_requests_created": access["status"] == "success",
                "document_generated": document["status"] == "success",
                "onboarding_plan": document["document"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error in onboarding process: {str(e)}"
            }
    
    def ask(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a natural language query about onboarding.
        
        Args:
            query: The query text
            context: Additional context like employee information
            
        Returns:
            Response to the query
        """
        query_lower = query.lower()
        
        # Extract employee name from context if available
        employee_name = "the new employee"
        if context and "employee" in context and "name" in context["employee"]:
            employee_name = context["employee"]["name"]
        
        # Handle different types of queries
        if "welcome email" in query_lower or "send email" in query_lower:
            return f"I can prepare a welcome email for {employee_name}. The email will include first day instructions, what to bring, and who they'll meet."
            
        elif "schedule" in query_lower or "meeting" in query_lower:
            return f"I can schedule all necessary onboarding meetings for {employee_name}, including orientation, team introductions, and training sessions."
            
        elif "system access" in query_lower or "access request" in query_lower:
            return f"I'll create the necessary system access requests for {employee_name} based on their role and department."
            
        elif "equipment" in query_lower or "laptop" in query_lower:
            return f"I'll make sure IT prepares the required equipment for {employee_name} before their start date."
            
        elif "checklist" in query_lower or "tasks" in query_lower:
            return f"I can generate a comprehensive onboarding checklist for {employee_name} with all the tasks needed for a successful onboarding."
            
        elif "document" in query_lower or "plan" in query_lower:
            return f"I'll create a complete onboarding document for {employee_name} that includes their schedule, key contacts, and other important information."
            
        else:
            return f"I can help with the onboarding process for {employee_name}. I can send welcome emails, schedule meetings, create system access requests, prepare equipment, and generate onboarding documents. What specific part of the onboarding process would you like assistance with?"

# Example usage:
# agent = OnboardingAgent()
# 
# new_employee = {
#     "name": "Jane Smith",
#     "position": "Senior Software Engineer",
#     "department": "Engineering",
#     "start_date": "2025-09-15",
#     "manager": "John Manager",
#     "team": "Backend Development",
#     "location": "New York Office",
#     "email": "jane.smith@example.com"
# }
# 
# onboarding_result = agent.complete_onboarding_process(new_employee)
