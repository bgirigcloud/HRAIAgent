"""
Demo Google ADK agent implementation for HR AI Assistant.
This module provides mock implementations of Google ADK agents for demonstration purposes.
"""

import os
from typing import Any, Dict, List, Optional, Union
import datetime

# Check if real google.adk exists, otherwise use our mock
try:
    import google.adk
    import google.adk.agents
    USING_REAL_ADK = True
except ImportError:
    USING_REAL_ADK = False

# Try to import the Onboarding Agent
try:
    from HR_root_agent.sub_agents.onboarding_agent.agent import OnboardingAgent
    HAS_ONBOARDING_AGENT = True
except ImportError:
    HAS_ONBOARDING_AGENT = False

# Try to import the Payroll Agent
try:
    from HR_root_agent.sub_agents.payroll_agent.agent import PayrollAgent
    HAS_PAYROLL_AGENT = True
except ImportError:
    HAS_PAYROLL_AGENT = False

# Try to import advanced agents
try:
    from HR_root_agent.sub_agents.neo4j_agent import neo4j_agent
    HAS_NEO4J_AGENT = True
except ImportError:
    HAS_NEO4J_AGENT = False

try:
    from HR_root_agent.sub_agents.pgvector_db_agent import pgvector_db_agent
    HAS_PGVECTOR_AGENT = True
except ImportError:
    HAS_PGVECTOR_AGENT = False

try:
    from HR_root_agent.sub_agents.rag_agent import rag_agent
    HAS_RAG_AGENT = True
except ImportError:
    HAS_RAG_AGENT = False

try:
    from HR_root_agent.sub_agents.mcp_server_agent import mcp_server_agent
    HAS_MCP_SERVER_AGENT = True
except ImportError:
    HAS_MCP_SERVER_AGENT = False

# Define demo agents regardless of whether real ADK exists
class HRAgentBase:
    """Base class for all HR AI agents."""
    
    def __init__(self, name: str = "HR Agent", model: str = "gemini-1.5-pro"):
        self.name = name
        self.model = model
        self.history = []
    
    def ask(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Send a query to the agent and get a response."""
        if not context:
            context = {}
            
        # Record the interaction
        self.history.append({"role": "user", "content": query})
        
        # Generate mock response based on the query
        response = self._generate_mock_response(query, context)
        
        # Record the response
        self.history.append({"role": "assistant", "content": response})
        
        return response
    
    def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
        """Generate a mock response based on the query and context."""
        if "job description" in query.lower() or "jd" in query.lower():
            return "Here is my analysis of the job description. I've identified key skills including Python, data analysis, and communication. The job requires 3-5 years of experience and a bachelor's degree in Computer Science."
        elif "resume" in query.lower() or "cv" in query.lower():
            return "Based on my analysis of the resume, this candidate has 4 years of relevant experience, strong Python skills, and has worked with machine learning frameworks. They would be a good fit for the Senior Developer role."
        elif "interview" in query.lower():
            return "The candidate performed well in the technical interview, demonstrating strong problem-solving skills and good communication. I'd recommend moving forward with this candidate."
        elif "schedule" in query.lower() or "calendar" in query.lower():
            return "I've analyzed the calendar availability and recommend scheduling the interview on Tuesday at 2:00 PM when all team members are available."
        elif "help" in query.lower():
            return "I can help with job description analysis, resume screening, interview feedback, and scheduling. What would you like assistance with today?"
        else:
            return f"I understand you're asking about '{query}'. As your HR Assistant, I'm here to help with recruitment, candidate assessment, and HR processes. Could you provide more specific details about what you need?"

class JobDescriptionAgent(HRAgentBase):
    """Agent for analyzing and generating job descriptions."""
    
    def __init__(self):
        super().__init__(name="JD Analyzer")
        self.jd_templates = self._load_templates()
        self.skills_database = self._load_skills_database()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load JD templates."""
        return {
            "software_engineer": """
                # {title}
                
                ## About Us
                {company_description}
                
                ## Position Overview
                We are seeking an exceptional {title} to join our team{location_text}. In this role, you will design, develop, and maintain {focus_area} solutions while collaborating with cross-functional teams.
                
                ## Responsibilities
                {responsibilities}
                
                ## Required Skills & Qualifications
                {required_skills}
                
                ## Preferred Skills & Qualifications
                {preferred_skills}
                
                ## What We Offer
                {benefits}
                
                {salary_text}
                
                ## Experience Level
                {experience_level}
            """,
            "data_scientist": """
                # {title}
                
                ## About Us
                {company_description}
                
                ## Position Overview
                We are looking for a talented {title} to join our data science team{location_text}. You will work on extracting valuable insights from complex data sets and developing machine learning models.
                
                ## Responsibilities
                {responsibilities}
                
                ## Required Skills & Qualifications
                {required_skills}
                
                ## Preferred Skills & Qualifications
                {preferred_skills}
                
                ## What We Offer
                {benefits}
                
                {salary_text}
                
                ## Experience Level
                {experience_level}
            """,
            "product_manager": """
                # {title}
                
                ## About Us
                {company_description}
                
                ## Position Overview
                We are seeking an experienced {title} to lead product development initiatives{location_text}. You will be responsible for the product roadmap, user requirements, and coordinating with engineering teams.
                
                ## Responsibilities
                {responsibilities}
                
                ## Required Skills & Qualifications
                {required_skills}
                
                ## Preferred Skills & Qualifications
                {preferred_skills}
                
                ## What We Offer
                {benefits}
                
                {salary_text}
                
                ## Experience Level
                {experience_level}
            """
        }
    
    def _load_skills_database(self) -> Dict[str, List[str]]:
        """Load skills database for different job categories."""
        return {
            "software_engineering": [
                "Python", "JavaScript", "React", "Node.js", "TypeScript", 
                "AWS", "Docker", "Kubernetes", "CI/CD", "REST APIs", 
                "GraphQL", "SQL", "NoSQL", "Git", "Microservices",
                "System Design", "Algorithms", "Data Structures", "Testing"
            ],
            "data_science": [
                "Python", "R", "SQL", "Data Analysis", "Machine Learning",
                "Deep Learning", "NLP", "Computer Vision", "Statistics",
                "Data Visualization", "TensorFlow", "PyTorch", "scikit-learn",
                "Pandas", "NumPy", "Big Data", "Spark", "Hadoop", "ETL"
            ],
            "product_management": [
                "Product Strategy", "User Research", "Market Analysis",
                "Roadmapping", "Agile", "Scrum", "Jira", "Wireframing",
                "Prototyping", "A/B Testing", "User Stories", "Prioritization",
                "Stakeholder Management", "Go-to-market", "KPIs", "Analytics"
            ]
        }
    
    def analyze_job_description(self, jd_text: str) -> Dict[str, Any]:
        """Analyze a job description text."""
        # Detect job category
        job_category = "software_engineering"  # Default category
        
        for category, skills in self.skills_database.items():
            matches = sum(1 for skill in skills if skill.lower() in jd_text.lower())
            if matches > 3:  # If more than 3 skills from a category are found
                job_category = category
                break
        
        # Extract skills based on the identified category
        skills_found = [
            skill for skill in self.skills_database[job_category] 
            if skill.lower() in jd_text.lower()
        ]
        
        # Mock experience detection
        experience_terms = {
            "entry level": "0-2 years",
            "junior": "1-3 years",
            "mid-level": "3-5 years",
            "senior": "5+ years",
            "lead": "7+ years",
            "manager": "5+ years with management experience",
            "principal": "8+ years",
            "architect": "8+ years"
        }
        
        detected_experience = "3-5 years"  # Default
        for term, exp in experience_terms.items():
            if term in jd_text.lower():
                detected_experience = exp
                break
        
        # Mock education detection
        education_terms = {
            "bachelor": "Bachelor's degree",
            "master": "Master's degree",
            "phd": "Ph.D.",
            "doctorate": "Ph.D.",
            "high school": "High school diploma",
            "associate": "Associate's degree"
        }
        
        detected_education = "Bachelor's degree in relevant field"  # Default
        for term, edu in education_terms.items():
            if term in jd_text.lower():
                detected_education = edu
                if "computer" in jd_text.lower() or "cs" in jd_text.lower():
                    detected_education += " in Computer Science or related field"
                elif "business" in jd_text.lower():
                    detected_education += " in Business, Finance or related field"
                break
        
        # Generate recommendations
        recommendations = [
            "Consider adding more details about the team structure",
            "Specify which frameworks or tools are required",
            "Add information about remote work options or flexibility",
            "Include details about company culture and values"
        ]
        
        # Check for potential bias
        bias_terms = [
            "young", "energetic", "ninja", "rockstar", "guru", 
            "he", "she", "his", "her", "mankind", "manpower",
            "chairman", "manmade", "salesman", "fireman"
        ]
        
        bias_found = [term for term in bias_terms if term in jd_text.lower()]
        bias_check = "No major biases detected in language."
        if bias_found:
            bias_check = f"Potential bias found in terms: {', '.join(bias_found)}. Consider using more inclusive language."
        
        # Return analysis results
        return {
            "skills": skills_found if skills_found else ["Python", "Data Analysis", "Communication"],
            "experience": detected_experience,
            "education": detected_education,
            "recommendations": recommendations,
            "bias_check": bias_check,
            "market_fit": "The described position aligns with current market expectations and standards.",
            "sentiment": "Professional and clear"
        }
    
    def generate_job_description(self, role: str, requirements: List[str]) -> str:
        """Generate a job description based on role and requirements."""
        # Determine template to use based on role
        template_key = "software_engineer"  # Default
        
        if "data" in role.lower() or "machine" in role.lower() or "ai" in role.lower():
            template_key = "data_scientist"
        elif "product" in role.lower() or "manager" in role.lower():
            template_key = "product_manager"
        
        # Extract job title
        title = role
        
        # Format requirements and responsibilities
        required_skills_text = "\n".join([f"- {req}" for req in requirements]) if requirements else "- Proficiency in required technologies\n- Problem-solving skills\n- Good communication"
        
        # Generate default responsibilities based on role
        if "developer" in role.lower() or "engineer" in role.lower():
            responsibilities = """
            - Design, develop and maintain high-quality software solutions
            - Collaborate with cross-functional teams to define and implement features
            - Write clean, efficient, and well-documented code
            - Participate in code reviews and provide constructive feedback
            - Troubleshoot and debug issues as they arise
            """
        elif "data" in role.lower():
            responsibilities = """
            - Analyze large datasets to extract actionable insights
            - Develop and implement machine learning models
            - Collaborate with stakeholders to understand business requirements
            - Create visualizations and reports to communicate findings
            - Optimize data collection procedures
            """
        else:
            responsibilities = """
            - Work with stakeholders to gather and prioritize requirements
            - Define and track key performance metrics
            - Coordinate with engineering teams on implementation
            - Manage the product lifecycle from conception to launch
            - Analyze market trends and competition
            """
        
        # Fill the template
        jd_text = self.jd_templates[template_key].format(
            title=title,
            company_description="CloudHero With AI is a leading provider of AI-powered solutions that help businesses transform their operations and achieve better results.",
            location_text=" in a remote-first environment" if "remote" in role.lower() else "",
            responsibilities=responsibilities,
            required_skills=required_skills_text,
            preferred_skills="- Experience with cloud platforms (AWS, GCP, Azure)\n- Knowledge of CI/CD practices\n- Experience with Agile development methodologies",
            benefits="- Competitive salary and benefits package\n- Remote work flexibility\n- Professional development opportunities\n- Collaborative and inclusive work environment",
            salary_text="## Compensation\nCompetitive salary based on experience and skills.",
            experience_level="3-5 years of relevant experience required"
        )
        
        return jd_text
        
    def check_jd_bias(self, jd_text: str) -> Dict[str, Any]:
        """Check a job description for potential bias in language."""
        # Lists of potentially biased terms by category
        gender_bias_terms = [
            "he", "his", "him", "himself", "she", "her", "hers", "herself",
            "chairman", "manpower", "manmade", "mankind", "salesman", "fireman",
            "policeman", "stewardess", "waitress", "businessman"
        ]
        
        age_bias_terms = [
            "young", "energetic", "fresh", "recent graduate", "digital native",
            "junior", "youthful", "vibrant", "dynamic", "modern"
        ]
        
        cultural_bias_terms = [
            "cultural fit", "team player", "like-minded", "work hard play hard",
            "ninja", "rockstar", "guru", "superstar", "wizard"
        ]
        
        # Check for biased terms
        gender_bias = [term for term in gender_bias_terms if term.lower() in jd_text.lower()]
        age_bias = [term for term in age_bias_terms if term.lower() in jd_text.lower()]
        cultural_bias = [term for term in cultural_bias_terms if term.lower() in jd_text.lower()]
        
        # Calculate bias score (100 = no bias, 0 = extreme bias)
        bias_count = len(gender_bias) + len(age_bias) + len(cultural_bias)
        bias_score = max(0, 100 - (bias_count * 5))
        
        # Generate recommendations
        recommendations = []
        
        if gender_bias:
            recommendations.append(f"Replace gender-specific terms ({', '.join(gender_bias)}) with gender-neutral alternatives")
        
        if age_bias:
            recommendations.append(f"Remove age-related terms ({', '.join(age_bias)}) to avoid age discrimination")
        
        if cultural_bias:
            recommendations.append(f"Replace subjective cultural terms ({', '.join(cultural_bias)}) with specific requirements")
            
        if not recommendations:
            recommendations.append("Job description uses inclusive language. Continue using neutral, specific, and objective terminology.")
        
        return {
            "bias_score": bias_score,
            "gender_bias": gender_bias,
            "age_bias": age_bias,
            "cultural_bias": cultural_bias,
            "recommendations": recommendations,
            "overall_assessment": "Low bias" if bias_score > 80 else "Moderate bias" if bias_score > 60 else "High bias"
        }
        
    def get_market_insights(self, role: str, location: str = None) -> Dict[str, Any]:
        """Get market insights for a specific role and location."""
        # Mock market data based on role
        market_data = {
            "developer": {
                "salary_range": {"low": 90000, "average": 115000, "high": 140000},
                "demand": "High",
                "growth": "+15% YoY",
                "key_skills": ["Python", "JavaScript", "Cloud", "Microservices"]
            },
            "engineer": {
                "salary_range": {"low": 95000, "average": 120000, "high": 145000},
                "demand": "Very High",
                "growth": "+18% YoY",
                "key_skills": ["Python", "AWS", "Kubernetes", "CI/CD"]
            },
            "scientist": {
                "salary_range": {"low": 100000, "average": 130000, "high": 160000},
                "demand": "Very High",
                "growth": "+22% YoY",
                "key_skills": ["Python", "Machine Learning", "SQL", "Statistics"]
            },
            "manager": {
                "salary_range": {"low": 110000, "average": 140000, "high": 170000},
                "demand": "Moderate",
                "growth": "+10% YoY",
                "key_skills": ["Agile", "Leadership", "Product Strategy", "Stakeholder Management"]
            },
            "designer": {
                "salary_range": {"low": 85000, "average": 105000, "high": 130000},
                "demand": "High",
                "growth": "+12% YoY",
                "key_skills": ["UI/UX", "Figma", "User Research", "Prototyping"]
            }
        }
        
        # Default market data
        default_data = {
            "salary_range": {"low": 80000, "average": 100000, "high": 120000},
            "demand": "Moderate",
            "growth": "+8% YoY",
            "key_skills": ["Communication", "Problem Solving", "Teamwork"]
        }
        
        # Find matching market data
        role_lower = role.lower()
        matched_data = None
        
        for key, data in market_data.items():
            if key in role_lower:
                matched_data = data
                break
        
        # Use default if no match
        if not matched_data:
            matched_data = default_data
        
        # Adjust based on location if provided
        location_adjustment = 1.0  # Default multiplier
        if location:
            location_lower = location.lower()
            if any(city in location_lower for city in ["san francisco", "new york", "seattle", "boston"]):
                location_adjustment = 1.25
            elif any(city in location_lower for city in ["austin", "denver", "chicago", "los angeles"]):
                location_adjustment = 1.15
            elif "remote" in location_lower:
                location_adjustment = 1.05
        
        # Apply location adjustment
        adjusted_data = {
            "salary_range": {
                key: int(value * location_adjustment) 
                for key, value in matched_data["salary_range"].items()
            },
            "demand": matched_data["demand"],
            "growth": matched_data["growth"],
            "key_skills": matched_data["key_skills"],
            "location_factor": f"{int((location_adjustment - 1) * 100)}% above national average" if location_adjustment > 1 else "national average"
        }
        
        return adjusted_data

class ResumeAnalyzerAgent(HRAgentBase):
    """Agent for analyzing resumes and matching with job descriptions."""
    
    def __init__(self):
        super().__init__(name="Resume Analyzer")
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze a resume text."""
        # This would typically call the actual model for analysis
        return {
            "skills": ["Python", "Django", "PostgreSQL", "AWS", "Docker"],
            "experience_years": 4,
            "education": "M.S. in Computer Science",
            "strengths": ["Backend Development", "Cloud Infrastructure", "Database Design"],
            "missing_skills": ["React", "TensorFlow"],
            "sentiment": "Professional and well-organized"
        }
    
    def match_with_job(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """Match a resume with a job description."""
        # This would typically call the actual model for matching
        return {
            "match_score": 85,
            "matching_skills": ["Python", "AWS", "Docker"],
            "missing_skills": ["React", "TensorFlow"],
            "experience_match": "Exceeds requirements",
            "education_match": "Meets requirements",
            "recommendation": "Strong candidate, proceed to interview"
        }

class ATSAgent(HRAgentBase):
    """Agent for ATS integration and candidate management."""
    
    def __init__(self):
        super().__init__(name="ATS Manager")
    
    def rank_candidates(self, candidates: List[Dict[str, Any]], job_text: str) -> List[Dict[str, Any]]:
        """Rank candidates based on a job description."""
        # Mock implementation
        return [
            {"name": "Jane Doe", "match_score": 92, "recommendation": "Interview"},
            {"name": "John Smith", "match_score": 85, "recommendation": "Interview"},
            {"name": "Alice Johnson", "match_score": 78, "recommendation": "Consider"},
            {"name": "Bob Brown", "match_score": 65, "recommendation": "Reject"}
        ]

class SchedulingAgent(HRAgentBase):
    """Agent for calendar management and interview scheduling."""
    
    def __init__(self):
        super().__init__(name="Scheduling Assistant")
    
    def suggest_times(self, participants: List[str], duration_minutes: int = 60) -> List[Dict[str, Any]]:
        """Suggest meeting times based on participant availability."""
        # Mock implementation
        return [
            {"start_time": "2025-09-10T14:00:00", "end_time": "2025-09-10T15:00:00", "available_participants": ["all"]},
            {"start_time": "2025-09-11T10:00:00", "end_time": "2025-09-11T11:00:00", "available_participants": ["all"]},
            {"start_time": "2025-09-12T16:00:00", "end_time": "2025-09-12T17:00:00", "available_participants": ["all"]}
        ]

class InterviewTranscriptAgent(HRAgentBase):
    """Agent for analyzing interview transcripts and recordings."""
    
    def __init__(self):
        super().__init__(name="Interview Analyzer")
    
    def analyze_transcript(self, transcript_text: str) -> Dict[str, Any]:
        """Analyze an interview transcript."""
        # Mock implementation
        return {
            "technical_assessment": {
                "overall_score": 8.5,
                "strengths": ["Problem solving", "System design", "Code quality"],
                "weaknesses": ["Testing strategies", "Performance optimization"]
            },
            "soft_skills_assessment": {
                "overall_score": 9.0,
                "strengths": ["Communication", "Teamwork", "Adaptability"],
                "weaknesses": ["Could improve on leadership examples"]
            },
            "key_insights": [
                "Candidate has strong technical fundamentals",
                "Demonstrates good real-world problem-solving approach",
                "Cultural fit appears strong based on values expressed"
            ],
            "recommendation": "Hire - Strong candidate who meets all key requirements"
        }

class HRRootAgent(HRAgentBase):
    """Main agent that coordinates all HR sub-agents."""
    
    def __init__(self):
        super().__init__(name="HR Assistant")
        self.jd_agent = JobDescriptionAgent()
        self.resume_agent = ResumeAnalyzerAgent()
        self.ats_agent = ATSAgent()
        self.scheduling_agent = SchedulingAgent()
        self.interview_agent = InterviewTranscriptAgent()
    
    def process_request(self, request_type: str, **kwargs) -> Dict[str, Any]:
        """Process a request by routing to the appropriate sub-agent."""
        if request_type == "analyze_job_description":
            return self.jd_agent.analyze_job_description(kwargs.get("text", ""))
        elif request_type == "analyze_resume":
            return self.resume_agent.analyze_resume(kwargs.get("text", ""))
        elif request_type == "match_resume_job":
            return self.resume_agent.match_with_job(
                kwargs.get("resume_text", ""), 
                kwargs.get("job_text", "")
            )
        elif request_type == "rank_candidates":
            return self.ats_agent.rank_candidates(
                kwargs.get("candidates", []), 
                kwargs.get("job_text", "")
            )
        elif request_type == "suggest_times":
            return self.scheduling_agent.suggest_times(
                kwargs.get("participants", []), 
                kwargs.get("duration_minutes", 60)
            )
        elif request_type == "analyze_transcript":
            return self.interview_agent.analyze_transcript(kwargs.get("text", ""))
        else:
            return {"error": f"Unknown request type: {request_type}"}


# Provide access to agents
def get_hr_agents():
    """Get all HR agents in a dictionary."""
    agents = {
        "root": HRRootAgent(),
        "jd": JobDescriptionAgent(),
        "resume": ResumeAnalyzerAgent(),
        "ats": ATSAgent(),
        "scheduling": SchedulingAgent(),
        "interview": InterviewTranscriptAgent()
    }
    
    # Add the Onboarding Agent if available
    if HAS_ONBOARDING_AGENT:
        agents["onboarding"] = OnboardingAgent()
    else:
        # Create a mock onboarding agent using HRAgentBase
        class MockOnboardingAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="Onboarding Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with employee onboarding. The onboarding agent module is not fully loaded, but I can still provide basic information."
        
        agents["onboarding"] = MockOnboardingAgent()
    
    # Add the Payroll Agent if available
    if HAS_PAYROLL_AGENT:
        agents["payroll"] = PayrollAgent()
    else:
        # Create a mock payroll agent using HRAgentBase
        class MockPayrollAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="Payroll Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with payroll processing, including calculating wages, taxes, and deductions, generating pay stubs, and creating payroll reports. The payroll agent module is not fully loaded, but I can still provide basic information."
        
        agents["payroll"] = MockPayrollAgent()
        
        # Mock implementation of the Neo4j Agent
        class MockNeo4jAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="Neo4j Graph Database Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with organizational graph database operations, including creating employee relationships, analyzing organizational structure, and finding connections between team members. The Neo4j agent module is not fully loaded, but I can still provide basic information."

        # Mock implementation of the PGVector DB Agent
        class MockPGVectorDBAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="Vector Database Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with vector similarity search for resumes and job descriptions, finding matching candidates for jobs, and storing embeddings for HR documents. The PGVector DB agent module is not fully loaded, but I can still provide basic information."

        # Mock implementation of the RAG Agent
        class MockRAGAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="RAG Knowledge Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with retrieval augmented generation for HR knowledge, enhancing responses with relevant context from resumes and job descriptions. The RAG agent module is not fully loaded, but I can still provide basic information."

        # Mock implementation of the MCP Server Agent
        class MockMCPServerAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="MCP Server Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with Model Context Protocol server operations, providing API endpoints for HR tools and services. The MCP Server agent module is not fully loaded, but I can still provide basic information."
        class MockPayrollAgent(HRAgentBase):
            def __init__(self):
                super().__init__(name="Payroll Assistant")
                
            def _generate_mock_response(self, query: str, context: Dict[str, Any]) -> str:
                return "I can help with payroll processing, including calculating wages, taxes, and deductions, generating pay stubs, and creating payroll reports. The payroll agent module is not fully loaded, but I can still provide basic information."
        
        agents["payroll"] = MockPayrollAgent()
    
    # Add the Neo4j Agent if available
    if HAS_NEO4J_AGENT:
        agents["neo4j"] = neo4j_agent
    else:
        agents["neo4j"] = MockNeo4jAgent()
    
    # Add the PGVector DB Agent if available
    if HAS_PGVECTOR_AGENT:
        agents["pgvector_db"] = pgvector_db_agent
    else:
        agents["pgvector_db"] = MockPGVectorDBAgent()
    
    # Add the RAG Agent if available
    if HAS_RAG_AGENT:
        agents["rag"] = rag_agent
    else:
        agents["rag"] = MockRAGAgent()
    
    # Add the MCP Server Agent if available
    if HAS_MCP_SERVER_AGENT:
        agents["mcp_server"] = mcp_server_agent
    else:
        agents["mcp_server"] = MockMCPServerAgent()
    
    return agents
