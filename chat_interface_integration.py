#!/usr/bin/env python3
"""
Integration solution for chat interface with job description agent
This fixes the "transfer_to_agent" issue and enables direct JD generation
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class JobDescriptionChatHandler:
    """Handler for job description requests in chat interface"""
    
    def __init__(self):
        try:
            from HR_root_agent.sub_agents.job_description.agent import job_description_agent, research_role_skills_and_generate_jd
            self.agent = job_description_agent
            self.direct_function = research_role_skills_and_generate_jd
        except ImportError as e:
            print(f"⚠️ Warning: Could not import agent: {e}")
            self.agent = None
            self.direct_function = None
    
    def handle_jd_request(self, user_message: str) -> str:
        """
        Handle job description requests from chat interface
        
        Args:
            user_message: User's request (e.g., "Create a job description for a Senior Java Developer with 5 years of experience")
            
        Returns:
            Generated job description or error message
        """
        
        try:
            # Parse the user request
            role, years = self._parse_jd_request(user_message)
            
            if not role or not years:
                return "❌ Could not parse job role and years from your request. Please specify both the role and years of experience."
            
            # Try multiple methods to generate the JD
            return self._generate_job_description(role, years, user_message)
            
        except Exception as e:
            return f"❌ Error generating job description: {str(e)}"
    
    def _parse_jd_request(self, message: str):
        """Parse job role and years from user message"""
        
        import re
        
        message_lower = message.lower()
        
        # Extract years
        year_patterns = [
            r'(\d+)\s*years?',
            r'with\s+(\d+)\s*years?',
            r'(\d+)\s*year\s+experience',
            r'(\d+)y\b'  # shorthand like "5y"
        ]
        
        years = None
        for pattern in year_patterns:
            match = re.search(pattern, message_lower)
            if match:
                years = int(match.group(1))
                break
        
        # Extract role
        role = None
        role_patterns = [
            r'(java\s+developer)',
            r'(python\s+developer)', 
            r'(data\s+scientist)',
            r'(qa\s+tester)',
            r'(qa\s+engineer)',
            r'(devops\s+engineer)',
            r'(frontend\s+developer)',
            r'(backend\s+developer)',
            r'(full\s+stack\s+developer)',
            r'(software\s+engineer)',
            r'(product\s+manager)'
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, message_lower)
            if match:
                role = match.group(1).title()
                break
        
        return role, years
    
    def _generate_job_description(self, role: str, years: int, original_message: str) -> str:
        """Generate job description using available methods"""
        
        # Method 1: Try direct function call (most reliable)
        if self.direct_function:
            try:
                return self.direct_function(role, years)
            except Exception as e:
                print(f"⚠️ Direct function failed: {e}")
        
        # Method 2: Try agent with different methods
        if self.agent:
            agent_methods = ['send_message', 'run', 'chat', 'generate']
            
            for method_name in agent_methods:
                if hasattr(self.agent, method_name):
                    try:
                        method = getattr(self.agent, method_name)
                        response = method(original_message)
                        
                        # Handle different response types
                        if hasattr(response, 'content'):
                            return response.content
                        elif isinstance(response, str):
                            return response
                        else:
                            return str(response)
                            
                    except Exception as e:
                        print(f"⚠️ Agent method {method_name} failed: {e}")
                        continue
        
        # Method 3: Generate using built-in knowledge (fallback)
        return self._generate_fallback_jd(role, years)
    
    def _generate_fallback_jd(self, role: str, years: int) -> str:
        """Fallback job description generation"""
        
        level = "Junior" if years <= 2 else "Mid-Level" if years <= 5 else "Senior" if years <= 8 else "Lead"
        
        if "java" in role.lower():
            return f"""### {level} {role}

We're looking for a highly skilled and experienced {level} {role} with a minimum of {years} years of professional experience to join our team. The ideal candidate will be a leader in the full software development lifecycle, from concept and design to testing and deployment. You'll be responsible for building high-volume, low-latency, and high-performance applications, and will also provide guidance and mentorship to junior developers.

***

### Key Responsibilities ✍️

* **Design and Development:** Lead the design, development, and maintenance of robust, scalable, and secure Java-based applications and services.
* **Coding and Best Practices:** Write clean, efficient, well-documented, and testable code. Ensure all code meets high-quality standards and aligns with software development best practices.
* **Troubleshooting and Optimization:** Identify and resolve complex technical issues, and optimize application performance and scalability.
* **Collaboration:** Work closely with cross-functional teams, including product managers, architects, and QA engineers, to define, design, and ship new features.
* **Mentorship:** Provide technical guidance and mentorship to junior developers, and participate in code reviews to maintain code quality.
* **System Architecture:** Propose and implement changes to the existing Java infrastructure, and contribute to architectural reviews.

***

### Required Skills & Qualifications 💻

* **Experience:** At least {years} years of hands-on experience in Java development.
* **Core Java:** Deep knowledge of Core Java, including Object-Oriented Programming (OOP) principles, data structures, algorithms, and multithreading.
* **Frameworks & Libraries:** Extensive experience with popular Java frameworks, such as **Spring Boot** and **Spring**, for building microservices and enterprise applications.
* **APIs and Web Services:** Proven ability to design and develop **RESTful APIs** and other web services.
* **Databases:** Proficiency with both relational (e.g., MySQL, PostgreSQL) and NoSQL (e.g., MongoDB) databases, including strong SQL skills.
* **Tools & Methodologies:** Expertise with build tools like **Maven** or **Gradle**, version control systems like **Git**, and a solid understanding of **Agile/Scrum** methodologies.
* **Testing:** Experience with testing frameworks like **JUnit** and **Mockito** for writing unit and integration tests.
* **Problem-Solving:** Strong analytical and problem-solving skills, with the ability to tackle complex technical challenges.

***

### Preferred Qualifications ✅

* Experience with **CI/CD** pipelines and tools (e.g., Jenkins, GitLab CI).
* Familiarity with cloud platforms (e.g., AWS, Azure, Google Cloud).
* Experience with containerization technologies like **Docker** and orchestration tools like **Kubernetes**.
* A Bachelor's or Master's degree in Computer Science, Software Engineering, or a related field."""
        
        else:
            return f"""### {level} {role}

We're looking for a skilled {level} {role} with {years} years of experience to join our team.

***

### Key Responsibilities ✍️

* **Development:** Design, develop, and maintain software applications and systems.
* **Code Quality:** Write clean, maintainable, and well-documented code.
* **Collaboration:** Work with cross-functional teams to deliver high-quality solutions.
* **Problem Solving:** Identify and resolve technical issues and challenges.
* **Best Practices:** Follow industry best practices and coding standards.
* **Continuous Learning:** Stay updated with latest technologies and trends.

***

### Required Skills & Qualifications 💻

* **Experience:** {years}+ years of professional experience in relevant technologies.
* **Technical Skills:** Strong programming and development skills.
* **Problem Solving:** Analytical and debugging capabilities.
* **Communication:** Good communication and teamwork abilities.
* **Tools:** Experience with version control and development tools.

***

### Preferred Qualifications ✅

* Experience with cloud platforms and modern technologies.
* Knowledge of agile development methodologies.
* Relevant certifications or advanced degrees."""

# Global handler instance
jd_handler = JobDescriptionChatHandler()

def handle_chat_message(message: str) -> str:
    """
    Main function to handle chat messages for job descriptions
    Use this in your chat interface to process JD requests
    """
    return jd_handler.handle_jd_request(message)

# Example usage for chat interface
if __name__ == "__main__":
    print("🤖 Job Description Chat Interface - Integration Test")
    print("=" * 70)
    
    # Test messages like in your screenshot
    test_messages = [
        "Create a job description for a Senior Java Developer with 5 years of experience",
        "create the jd 5 years java developer", 
        "Generate JD for Python Developer 3 years",
        "Job description for Data Scientist with 4 years experience"
    ]
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        print("🤖 Bot:")
        response = handle_chat_message(message)
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 70)
