import streamlit as st
import datetime

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="CloudHero With AI - HR Assistant",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import sys
from pathlib import Path

# Add project root to path to ensure imports work correctly
sys.path.append(str(Path(__file__).parent))

# Import dependency manager
from dependency_manager import DependencyManager

# Setup required packages
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    DependencyManager.ensure_package_installed("python-dotenv", "dotenv")
    import dotenv
    dotenv.load_dotenv()

# Import option_menu with fallback to basic navigation
try:
    import streamlit_option_menu
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    # Try to install it
    success = DependencyManager.ensure_package_installed("streamlit-option-menu", "streamlit_option_menu")
    if success:
        from streamlit_option_menu import option_menu
        HAS_OPTION_MENU = True
    else:
        HAS_OPTION_MENU = False
        st.warning("Using basic navigation because streamlit-option-menu is not available.")

try:
    import dotenv
    dotenv.load_dotenv()  # Load environment variables from .env file
except ImportError:
    st.error("Failed to import dotenv. Please install it with: pip install python-dotenv")
    dotenv = None

# Create comprehensive mock modules for optional dependencies
class MockAgent:
    """Mock implementation of a Google ADK agent"""
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get('config', {})
        self.name = kwargs.get('name', 'MockAgent')
    
    def run(self, *args, **kwargs):
        return {"result": "This is a mock response from the agent", "status": "success"}
    
    def ask(self, query, *args, **kwargs):
        return f"Mock response to: {query}"
    
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

class MockAgents:
    """Mock implementation of google.adk.agents module"""
    def __init__(self):
        self.Agent = MockAgent
        self.Config = type('Config', (), {})
    
    def create_agent(self, *args, **kwargs):
        return MockAgent(*args, **kwargs)

class MockGoogleADK:
    """Mock class for google.adk to prevent import errors"""
    def __init__(self):
        self.agents = MockAgents()
        self.Database = type('Database', (), {
            '__init__': lambda self, *args, **kwargs: None,
            'connect': lambda self, *args, **kwargs: self,
            'execute': lambda self, *args, **kwargs: [],
            'close': lambda self: None,
        })

# Apply mocks for missing modules
mock_google_adk = MockGoogleADK()
DependencyManager.mock_module('google.adk', mock_google_adk)
DependencyManager.mock_module('google.adk.agents', mock_google_adk.agents)

# Define mock agent classes for demonstration
class MockAgent:
    """Mock agent class for demonstration purposes"""
    def __init__(self, agent_type="generic"):
        self.agent_type = agent_type
    
    def analyze_job_description(self, text):
        return {
            "skills": ["Python", "Machine Learning", "Communication"],
            "recommendations": ["Add team details", "Specify experience requirements"],
            "bias_check": "Inclusive language used",
            "market_fit": "Salary within market expectations"
        }
    
    def analyze_resumes(self, files, job_title):
        return [
            {"name": "John Smith", "match": 92, "skills": ["Python", "Django", "AWS"]},
            {"name": "Sarah Johnson", "match": 85, "skills": ["Python", "Flask", "SQL"]}
        ]
    
    def analyze_interview(self, file, candidate, position):
        return {
            "technical_score": 8.5,
            "soft_skills": 9.0,
            "recommendation": "Hire"
        }

# Import HR agent modules or use demo agents if not available
try:
    # First try to import real agents
    from HR_root_agent.agent import HRRootAgent
    from HR_root_agent.sub_agents.job_description.agent import JobDescriptionAgent
    from HR_root_agent.sub_agents.resume_analyzer.agent import ResumeAnalyzerAgent
    from HR_root_agent.sub_agents.ats_tool.agent import ATSAgent
    from HR_root_agent.sub_agents.scheduling_agent.agent import SchedulingAgent
    from HR_root_agent.sub_agents.interview_transcript_agent.agent import InterviewTranscriptAgent
    USING_MOCK = False
    st.sidebar.success("Using real HR agents")
except ImportError:
    try:
        # Try to use our comprehensive demo agents
        from demo_agents import (
            HRRootAgent, 
            JobDescriptionAgent, 
            ResumeAnalyzerAgent, 
            ATSAgent, 
            SchedulingAgent, 
            InterviewTranscriptAgent,
            get_hr_agents
        )
        USING_MOCK = True
        st.sidebar.info("Using demo HR agents")
    except ImportError as e:
        # Fallback to very basic mock agents
        st.warning(f"Using basic mock agents for demonstration: {e}")
        HRRootAgent = lambda: MockAgent("root")
        JobDescriptionAgent = lambda: MockAgent("jd")
        ResumeAnalyzerAgent = lambda: MockAgent("resume")
        ATSAgent = lambda: MockAgent("ats")
        SchedulingAgent = lambda: MockAgent("scheduling")
        InterviewTranscriptAgent = lambda: MockAgent("interview")
        USING_MOCK = True

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Product+Sans:wght@400;700&display=swap');
    
    * {
        font-family: 'Product Sans', sans-serif;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    .main-header {
        color: #1570A5;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-top: 0.5rem;
    }
    
    .sub-header {
        color: #1570A5;
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-top: 4px solid #50B4E0;
    }
    
    .info-text {
        color: #424242;
        font-size: 1rem;
    }
    
    .blue-btn {
        background-color: #1570A5;
        color: white;
    }
    
    .blue-btn:hover {
        background-color: #0F5B8B;
        color: white;
    }
    
    /* CloudHero brand colors */
    .primary-color {
        color: #1570A5;
    }
    
    .secondary-color {
        color: #50B4E0;
    }
    
    .accent-color {
        color: #7FD3F7;
    }
    
    /* Custom styling for option menu */
    .nav-link {
        color: #1570A5 !important;
        font-weight: 500;
    }
    
    .nav-link.active {
        background-color: #1570A5 !important;
        color: white !important;
    }
    
    /* Custom styling for sidebar */
    .css-1d391kg {
        background-color: #f1f7fb;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #1570A5;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #0F5B8B;
        color: white;
    }
    
    /* Make primary buttons match brand color */
    .stButton>button[kind="primary"] {
        background-color: #1570A5;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize HR Agents
@st.cache_resource
def load_agents():
    try:
        # If using demo_agents module with get_hr_agents function
        if USING_MOCK and 'get_hr_agents' in globals():
            return get_hr_agents()
        
        # Otherwise initialize root agent and get all sub-agents from it
        try:
            from HR_root_agent.agent import root_agent
            
            # Return all agents through the root agent
            return {
                "root": root_agent,
                "jd": root_agent.sub_agents[0],  # job_description_agent
                "resume": root_agent.sub_agents[2],  # resume_analyzer_agent
                "ats": root_agent.sub_agents[5],  # ats_agent
                "scheduling": root_agent.sub_agents[4],  # scheduling_agent
                "interview": root_agent.sub_agents[2],  # interview_transcript_agent
                "onboarding": root_agent.sub_agents[6] if len(root_agent.sub_agents) > 6 else None,  # onboarding_agent
                "payroll": root_agent.sub_agents[7] if len(root_agent.sub_agents) > 7 else None,  # payroll_agent
                "neo4j": root_agent.sub_agents[8] if len(root_agent.sub_agents) > 8 else None,  # neo4j_agent
                "pgvector_db": root_agent.sub_agents[9] if len(root_agent.sub_agents) > 9 else None,  # pgvector_db_agent
                "rag": root_agent.sub_agents[10] if len(root_agent.sub_agents) > 10 else None,  # rag_agent
                "mcp_server": root_agent.sub_agents[11] if len(root_agent.sub_agents) > 11 else None  # mcp_server_agent
            }
        except Exception as e:
            st.error(f"Error initializing root agent: {e}")
            raise
    except Exception as e:
        if not USING_MOCK:
            st.error(f"Error loading agents: {e}")
        # Even on error, return mock agents so the UI still works
        return {
            "root": MockAgent("root"),
            "jd": MockAgent("jd"),
            "resume": MockAgent("resume"),
            "ats": MockAgent("ats"),
            "scheduling": MockAgent("scheduling"),
            "interview": MockAgent("interview"),
            "onboarding": MockAgent("onboarding"),
            "payroll": MockAgent("payroll"),
            "neo4j": MockAgent("neo4j"),
            "pgvector_db": MockAgent("pgvector_db"),
            "rag": MockAgent("rag"),
            "mcp_server": MockAgent("mcp_server")
        }

# Main application
def main():
    # Page config moved to top of file
    
    load_css()
    
    # Header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            st.image("D:/CloudHeroWithAI/HrMultiAgent/HRAIAgent/CompanyLogo.png", width=150)
        except:
            st.write("☁️")
    with col2:
        st.markdown('<h1 class="main-header">HR AI Assistant</h1>', unsafe_allow_html=True)
    
    # Display demo mode notice if using mock agents
    if USING_MOCK:
        st.info("""
        ℹ️ **DEMO MODE ACTIVE**: The application is running with simulated data and mock agents.
        Real agent functionality is not available, but you can explore the UI and features.
        """)
    
    
    # Navigation
    with st.sidebar:
        # Use the company logo instead of the generic icon
        try:
            st.image("D:/CloudHeroWithAI/HrMultiAgent/HRAIAgent/CompanyLogo.png", width=250)
        except:
            st.image("https://img.icons8.com/color/96/000000/human-resources.png", width=80)
            
        st.markdown('<h2 class="sub-header">HR Multi-Agent System</h2>', unsafe_allow_html=True)
        
        # Define navigation options
        nav_options = [
            "Dashboard", 
            "Job Description Analysis", 
            "Resume Screening", 
            "ATS Integration",
            "Calendar Management",
            "Interview Analysis",
            "Employee Onboarding",
            "Payroll Management"
        ]
        
        if HAS_OPTION_MENU:
            # Use streamlit-option-menu if available
            selected = option_menu(
                menu_title=None,
                options=nav_options,
                icons=[
                    "house", 
                    "file-text", 
                    "person-badge", 
                    "filter-circle",
                    "calendar-date",
                    "chat-dots",
                    "person-plus",
                    "cash-coin"
                ],
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#1570A5", "font-size": "18px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e6f2f7"},
                    "nav-link-selected": {"background-color": "#1570A5"},
                }
            )
        else:
            # Fallback to basic radio buttons for navigation
            selected = st.radio("Navigation", nav_options)
    
    # Load agents
    agents = load_agents()
    
    # Content based on selection
    if selected == "Dashboard":
        display_dashboard()
    
    elif selected == "Job Description Analysis":
        display_jd_analysis(agents["jd"] if agents else None)
    
    elif selected == "Resume Screening":
        display_resume_screening(agents["resume"] if agents else None)
    
    elif selected == "ATS Integration":
        display_ats_integration(agents["ats"] if agents else None)
    
    elif selected == "Calendar Management":
        display_calendar_management(agents["scheduling"] if agents else None)
    
    elif selected == "Interview Analysis":
        display_interview_analysis(agents["interview"] if agents else None)
        
    elif selected == "Employee Onboarding":
        display_employee_onboarding(agents["onboarding"] if agents else None)
        
    elif selected == "Payroll Management":
        display_payroll_management(agents["payroll"] if agents else None)

# Dashboard page
def display_dashboard():
    st.markdown('<h2 class="sub-header">Dashboard</h2>', unsafe_allow_html=True)
    
    # Overview cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: #1570A5;">Job Descriptions</h3>
            <h2 style="color: #333;">5</h2>
            <p class="info-text">Active job listings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color: #1570A5;">Resumes</h3>
            <h2 style="color: #333;">24</h2>
            <p class="info-text">Candidates evaluated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3 style="color: #1570A5;">Interviews</h3>
            <h2 style="color: #333;">8</h2>
            <p class="info-text">Scheduled this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activities
    st.markdown('<h3 class="sub-header">Recent Activities</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <p><strong>Today</strong> - 3 new resumes analyzed for Senior Developer position</p>
        <p><strong>Yesterday</strong> - Interview feedback processed for Marketing Manager candidates</p>
        <p><strong>Sep 5, 2025</strong> - New job description created for Data Scientist position</p>
        <p><strong>Sep 3, 2025</strong> - 5 interviews scheduled with Product Manager candidates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<h3 class="sub-header">Quick Actions</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Create New Job Description", type="primary", use_container_width=True)
        st.button("Schedule Interview", type="primary", use_container_width=True)
    
    with col2:
        st.button("Upload Resumes", type="primary", use_container_width=True)
        st.button("Generate Reports", type="primary", use_container_width=True)

# Job Description Analysis page
def display_jd_analysis(agent):
    st.markdown('<h2 class="sub-header">Job Description Analysis</h2>', unsafe_allow_html=True)
    
    # Tabs for different JD functions
    jd_tabs = st.tabs(["Analyze JD", "Generate JD", "JD Templates", "JD History"])
    
    # Tab 1: Analyze Job Description
    with jd_tabs[0]:
        st.markdown("""
        <div class="card">
            <p class="info-text">
                Upload a job description or paste text to analyze key requirements, 
                skills, and qualifications. Our AI will help optimize your job posting to 
                attract the right candidates.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Input methods: File upload or text input
        input_method = st.radio("Select input method", ["Upload File", "Paste Text"], horizontal=True)
        
        jd_text = ""
        if input_method == "Upload File":
            uploaded_file = st.file_uploader("Upload a job description document", type=["txt", "pdf", "docx"])
            if uploaded_file:
                # In a real implementation, we would use libraries to extract text from various file formats
                try:
                    # For demonstration, assume it's a text file
                    jd_text = uploaded_file.getvalue().decode("utf-8")
                    with st.expander("Preview uploaded content"):
                        st.text(jd_text[:500] + ("..." if len(jd_text) > 500 else ""))
                except:
                    st.error("Could not read file. Please ensure it's a valid text document.")
        else:
            jd_text = st.text_area(
                "Paste job description text",
                height=250,
                placeholder="Paste the full job description text here...",
                help="Include the complete job description including title, responsibilities, requirements, etc."
            )
        
        # Analysis options
        with st.expander("Analysis Options"):
            col1, col2 = st.columns(2)
            with col1:
                analyze_for_bias = st.checkbox("Check for bias in language", value=True)
                extract_skills = st.checkbox("Extract key skills", value=True)
            with col2:
                competitive_analysis = st.checkbox("Compare to market standards", value=True)
                improvement_suggestions = st.checkbox("Get improvement suggestions", value=True)
        
        analyze_btn = st.button("Analyze Job Description", type="primary", use_container_width=True, disabled=not jd_text)
        
        # Analysis results (shown when analyze button is clicked)
        if analyze_btn and jd_text:
            st.markdown('<h3 class="sub-header">Analysis Results</h3>', unsafe_allow_html=True)
            
            with st.spinner("Analyzing job description..."):
                # Use the demo agent to analyze
                if agent:
                    try:
                        # Try to use the agent's analyze_job_description method
                        analysis = agent.analyze_job_description(jd_text)
                        
                        # Display the results in tabs
                        result_tabs = st.tabs(["Skills & Requirements", "Recommendations", "Bias Analysis", "Market Fit"])
                        
                        with result_tabs[0]:
                            st.markdown("""
                            <div class="card">
                                <h4 style="color: #1570A5;">Key Skills Identified</h4>
                            """, unsafe_allow_html=True)
                            
                            # Display skills from analysis or fallback to default
                            if 'skills' in analysis and analysis['skills']:
                                skills_html = "<ul>"
                                for skill in analysis['skills']:
                                    skills_html += f"<li>{skill}</li>"
                                skills_html += "</ul>"
                                st.markdown(skills_html, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <ul>
                                    <li>Python programming (Required)</li>
                                    <li>Data analysis (Required)</li>
                                    <li>Machine learning (Preferred)</li>
                                    <li>Communication skills (Required)</li>
                                    <li>Project management (Preferred)</li>
                                </ul>
                                """, unsafe_allow_html=True)
                            
                            # Experience and education
                            if 'experience' in analysis:
                                st.markdown(f"<p><strong>Experience Required:</strong> {analysis['experience']}</p>", unsafe_allow_html=True)
                            if 'education' in analysis:
                                st.markdown(f"<p><strong>Education:</strong> {analysis['education']}</p>", unsafe_allow_html=True)
                                
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with result_tabs[1]:
                            st.markdown("""
                            <div class="card">
                                <h4 style="color: #1570A5;">Recommendations</h4>
                            """, unsafe_allow_html=True)
                            
                            if 'recommendations' in analysis and analysis['recommendations']:
                                recs_html = "<ul>"
                                for rec in analysis['recommendations']:
                                    recs_html += f"<li>{rec}</li>"
                                recs_html += "</ul>"
                                st.markdown(recs_html, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <ul>
                                    <li>Consider adding specific details about team size and structure</li>
                                    <li>The experience requirement could be more specific</li>
                                    <li>Add information about tech stack and tools used</li>
                                    <li>Include details about company culture and benefits</li>
                                </ul>
                                """, unsafe_allow_html=True)
                                
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with result_tabs[2]:
                            st.markdown("""
                            <div class="card">
                                <h4 style="color: #1570A5;">Bias Check</h4>
                            """, unsafe_allow_html=True)
                            
                            if 'bias_check' in analysis:
                                st.markdown(f"<p>{analysis['bias_check']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown("<p>Job description uses inclusive language and avoids gender bias.</p>", unsafe_allow_html=True)
                                
                            # Visual indicator of bias level
                            bias_score = 92  # Example score (higher is better/less biased)
                            st.progress(bias_score/100)
                            st.markdown(f"<p style='text-align:center;'><strong>Bias Score:</strong> {bias_score}/100</p>", unsafe_allow_html=True)
                            
                            # Example bias findings
                            st.markdown("""
                            <h5 style='color: #1570A5;'>Gender-neutral language</h5>
                            <p>The job description uses gender-neutral language throughout. Continued use of inclusive terms like "candidate", "professional", and "team member" is recommended.</p>
                            
                            <h5 style='color: #1570A5;'>Age-inclusive language</h5>
                            <p>The text avoids terms that might signal age bias (like "digital native", "young and energetic").</p>
                                
                            <h5 style='color: #1570A5;'>Suggestions</h5>
                            <p>Consider reviewing phrases like "fast-paced environment" which may unintentionally exclude people with certain disabilities.</p>
                            """, unsafe_allow_html=True)
                                
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        with result_tabs[3]:
                            st.markdown("""
                            <div class="card">
                                <h4 style="color: #1570A5;">Market Competitiveness</h4>
                            """, unsafe_allow_html=True)
                            
                            if 'market_fit' in analysis:
                                st.markdown(f"<p>{analysis['market_fit']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown("<p>The salary range is within market expectations for this role and location.</p>", unsafe_allow_html=True)
                                
                            # Visual representation of market competitiveness
                            market_data = {
                                "Your Offering": 120000,
                                "Market Low": 95000,
                                "Market Average": 115000,
                                "Market High": 135000
                            }
                            
                            # Simple market comparison chart
                            st.markdown("<h5 style='color: #1570A5;'>Salary Comparison</h5>", unsafe_allow_html=True)
                            
                            # Using st.metric to show comparisons
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Your Offering", f"${market_data['Your Offering']:,}")
                            with col2:
                                st.metric("Market Average", f"${market_data['Market Average']:,}", 
                                         f"{((market_data['Your Offering'] - market_data['Market Average'])/market_data['Market Average'])*100:.1f}%")
                            with col3:
                                st.metric("Market Range", f"${market_data['Market Low']:,} - ${market_data['Market High']:,}")
                                
                            # Benefits comparison
                            st.markdown("""
                            <h5 style='color: #1570A5;'>Benefits Assessment</h5>
                            <p>Your benefits package appears to be <strong>highly competitive</strong> compared to similar positions. The remote work option and professional development budget are particularly strong offerings.</p>
                            """, unsafe_allow_html=True)
                                
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        
                        # Fallback to static content
                        st.markdown("""
                        <div class="card">
                            <h4 style="color: #1570A5;">Key Skills Identified</h4>
                            <ul>
                                <li>Python programming (Required)</li>
                                <li>Data analysis (Required)</li>
                                <li>Machine learning (Preferred)</li>
                                <li>Communication skills (Required)</li>
                                <li>Project management (Preferred)</li>
                            </ul>
                            
                            <h4 style="color: #1570A5;">Recommendations</h4>
                            <ul>
                                <li>Consider adding specific details about team size and structure</li>
                                <li>The experience requirement could be more specific</li>
                                <li>Add information about tech stack and tools used</li>
                                <li>Include details about company culture and benefits</li>
                            </ul>
                            
                            <h4 style="color: #1570A5;">Bias Check</h4>
                            <p>Job description uses inclusive language and avoids gender bias.</p>
                            
                            <h4 style="color: #1570A5;">Market Competitiveness</h4>
                            <p>The salary range is within market expectations for this role and location.</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Actions after analysis
            st.markdown('<h3 class="sub-header">Actions</h3>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Save Analysis Results", use_container_width=True)
            with col2:
                st.button("Export as PDF", use_container_width=True)
            with col3:
                st.button("Share with Team", use_container_width=True)
    
    # Tab 2: Generate Job Description
    with jd_tabs[1]:
        st.markdown("""
        <div class="card">
            <p class="info-text">
                Generate a professional job description by providing key information.
                Our AI will create a comprehensive and attractive job posting.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title", placeholder="e.g., Senior Python Developer")
            department = st.text_input("Department", placeholder="e.g., Engineering")
            location = st.text_input("Location", placeholder="e.g., Remote, New York, NY")
            employment_type = st.selectbox("Employment Type", 
                ["Full-time", "Part-time", "Contract", "Internship", "Freelance", "Temporary"])
        
        with col2:
            experience_level = st.selectbox("Experience Level", 
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior (5-8 years)", "Lead/Principal (8+ years)", "Executive"])
            salary_range = st.text_input("Salary Range (optional)", placeholder="e.g., $120,000 - $150,000")
            reporting_to = st.text_input("Reporting To", placeholder="e.g., CTO, Engineering Manager")
            team_size = st.text_input("Team Size", placeholder="e.g., 5-7 team members")
        
        # Key responsibilities and requirements
        st.subheader("Key Responsibilities")
        responsibilities = st.text_area("Enter one responsibility per line", height=150, 
            placeholder="Design and develop high-quality software solutions\nCollaborate with cross-functional teams\nParticipate in code reviews")
        
        st.subheader("Skills & Qualifications")
        required_skills = st.text_area("Required Skills (one per line)", height=100,
            placeholder="Python\nDjango\nSQL\nRESTful APIs")
        preferred_skills = st.text_area("Preferred Skills (one per line)", height=100,
            placeholder="Docker\nKubernetes\nAWS\nMachine Learning")
        
        # Company and benefits
        st.subheader("Company & Benefits")
        company_description = st.text_area("Company Description", height=100,
            placeholder="CloudHero With AI is a leading provider of AI-powered solutions...")
        benefits = st.text_area("Benefits & Perks (one per line)", height=100,
            placeholder="Competitive salary\nRemote work options\nFlexible hours\nHealth insurance")
        
        # Generate button
        generate_btn = st.button("Generate Job Description", type="primary", use_container_width=True)
        
        if generate_btn and job_title:
            with st.spinner("Generating job description..."):
                if agent and hasattr(agent, 'generate_job_description'):
                    try:
                        # Convert responsibilities and skills to lists
                        resp_list = [r.strip() for r in responsibilities.split('\n') if r.strip()]
                        req_skills = [s.strip() for s in required_skills.split('\n') if s.strip()]
                        pref_skills = [s.strip() for s in preferred_skills.split('\n') if s.strip()]
                        benefit_list = [b.strip() for b in benefits.split('\n') if b.strip()]
                        
                        # Call the agent's method
                        generated_jd = agent.generate_job_description(job_title, req_skills)
                    except:
                        # Fallback to template-based generation
                        generated_jd = f"""
                        # {job_title}

                        ## About the Role
                        We are seeking an experienced {job_title} to join our {department} team{f" in {location}" if location else ""}. This is a {employment_type.lower()} position{f" reporting to the {reporting_to}" if reporting_to else ""}.

                        ## Responsibilities
                        {"".join(f"- {resp}\n" for resp in responsibilities.split('\n') if resp.strip())}

                        ## Required Skills & Qualifications
                        {"".join(f"- {skill}\n" for skill in required_skills.split('\n') if skill.strip())}

                        ## Preferred Skills
                        {"".join(f"- {skill}\n" for skill in preferred_skills.split('\n') if skill.strip())}

                        ## About {company_description.split()[0] if company_description else "Our Company"}
                        {company_description}

                        ## What We Offer
                        {"".join(f"- {benefit}\n" for benefit in benefits.split('\n') if benefit.strip())}
                        
                        ## Experience Level
                        {experience_level}
                        
                        {f"## Salary Range\n{salary_range}" if salary_range else ""}
                        """
                
                # Display the generated JD
                st.markdown('<h3 class="sub-header">Generated Job Description</h3>', unsafe_allow_html=True)
                
                # Show the JD in a card with options to edit
                st.markdown("""
                <div class="card">
                    <h4 style="color: #1570A5;">Preview</h4>
                """, unsafe_allow_html=True)
                
                # Display the generated JD in a text area for editing
                edited_jd = st.text_area("Edit if needed:", value=generated_jd, height=400)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("Save Job Description", use_container_width=True)
                with col2:
                    st.button("Export as Word", use_container_width=True)
                with col3:
                    st.button("Publish to Job Boards", use_container_width=True)

    # Tab 3: JD Templates
    with jd_tabs[2]:
        st.markdown("""
        <div class="card">
            <p class="info-text">
                Browse and use our library of job description templates for various roles and industries.
                Select a template to use as a starting point for your job posting.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Template categories
        template_category = st.selectbox("Select Category", 
            ["Engineering & Development", "Data Science & Analytics", "Marketing & Sales", 
             "Design & Creative", "Management & Leadership", "Customer Support", "HR & Recruitment"])
        
        # Display templates based on category
        if template_category == "Engineering & Development":
            templates = {
                "Software Engineer": "Template for general software engineering roles",
                "Frontend Developer": "Specialized for UI/UX focused developers",
                "Backend Developer": "For server-side and API development roles",
                "Full Stack Developer": "For developers who work on both frontend and backend",
                "DevOps Engineer": "For CI/CD and infrastructure automation specialists",
                "Mobile App Developer": "For iOS/Android development positions"
            }
        elif template_category == "Data Science & Analytics":
            templates = {
                "Data Scientist": "For professionals who analyze and interpret complex data",
                "Data Analyst": "For roles focused on data processing and visualization",
                "Machine Learning Engineer": "For specialists building ML models and systems",
                "Data Engineer": "For data pipeline and infrastructure specialists",
                "Business Intelligence Analyst": "For reporting and dashboard specialists"
            }
        else:
            templates = {
                "Sample Template 1": "Description of the template",
                "Sample Template 2": "Description of the template",
                "Sample Template 3": "Description of the template"
            }
        
        # Display template cards
        st.markdown('<div class="template-container">', unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, (template_name, template_desc) in enumerate(templates.items()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="card">
                    <h4 style="color: #1570A5;">{template_name}</h4>
                    <p>{template_desc}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                        <span>⭐⭐⭐⭐⭐</span>
                        <span>Used 245 times</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.button(f"Use Template: {template_name}", key=f"use_{template_name}", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 4: JD History
    with jd_tabs[3]:
        st.markdown("""
        <div class="card">
            <p class="info-text">
                View and manage your previously created and analyzed job descriptions.
                You can edit, duplicate, or archive past job descriptions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mock job description history data
        jd_history = [
            {"id": 1, "title": "Senior Python Developer", "created": "2025-09-01", "status": "Published", "views": 145},
            {"id": 2, "title": "Data Scientist", "created": "2025-08-25", "status": "Draft", "views": 0},
            {"id": 3, "title": "Product Manager", "created": "2025-08-10", "status": "Published", "views": 287},
            {"id": 4, "title": "UX Designer", "created": "2025-07-22", "status": "Archived", "views": 112},
            {"id": 5, "title": "Cloud Architect", "created": "2025-07-15", "status": "Published", "views": 203}
        ]
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Filter by Status", ["Published", "Draft", "Archived"], default=["Published", "Draft"])
        with col2:
            date_range = st.date_input("Date Range", value=[], key="jd_date_range")
        with col3:
            search_term = st.text_input("Search by Title", placeholder="Enter keywords...")
        
        # Display job description history
        for jd in jd_history:
            if jd["status"] in status_filter:
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="color: #1570A5; margin: 0;">{jd["title"]}</h4>
                        <span class="badge" style="background-color: {'#4CAF50' if jd['status'] == 'Published' else '#FFA000' if jd['status'] == 'Draft' else '#9E9E9E'}; color: white; padding: 5px 10px; border-radius: 4px;">
                            {jd["status"]}
                        </span>
                    </div>
                    <p style="margin-top: 10px;">Created on: {jd["created"]} | Views: {jd["views"]}</p>
                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                        <button style="background-color: #1570A5; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">View</button>
                        <button style="background-color: #616161; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Edit</button>
                        <button style="background-color: #616161; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Duplicate</button>
                        <button style="background-color: {'#9E9E9E' if jd['status'] == 'Archived' else '#F44336'}; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">{'Restore' if jd['status'] == 'Archived' else 'Archive'}</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Resume Screening page
def display_resume_screening(agent):
    st.markdown('<h2 class="sub-header">Resume Screening</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="info-text">
            Upload candidate resumes to automatically extract information, match skills with job requirements,
            and get AI-powered recommendations on candidate suitability.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Job selection
    job_listing = st.selectbox(
        "Select Job Position", 
        ["Senior Python Developer", "Data Scientist", "Product Manager", "UX Designer", "DevOps Engineer"]
    )
    
    # File upload for resumes
    uploaded_files = st.file_uploader(
        "Upload candidate resumes", 
        type=["pdf", "docx", "txt"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.markdown(f"<h3 class='sub-header'>{len(uploaded_files)} Resume(s) Uploaded</h3>", unsafe_allow_html=True)
        
        for file in uploaded_files:
            st.markdown(f"<p>{file.name}</p>", unsafe_allow_html=True)
        
        analyze_resumes = st.button("Analyze Resumes", type="primary")
        
        if analyze_resumes:
            with st.spinner("Analyzing resumes..."):
                # Placeholder for actual agent analysis
                if agent:
                    # This would be replaced with actual agent call
                    # results = agent.analyze_resumes(uploaded_files, job_listing)
                    pass
                
                # Mock results
                st.markdown('<h3 class="sub-header">Analysis Results</h3>', unsafe_allow_html=True)
                
                candidates = [
                    {"name": "John Smith", "match": 92, "skills": ["Python", "Django", "AWS", "Docker"]},
                    {"name": "Sarah Johnson", "match": 85, "skills": ["Python", "Flask", "SQL", "Git"]},
                    {"name": "Michael Wong", "match": 78, "skills": ["Java", "Python", "REST APIs", "MongoDB"]}
                ]
                
                for candidate in candidates:
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="card">
                            <h4 style="color: #1E88E5;">{candidate['name']}</h4>
                            <p><strong>Skills:</strong> {', '.join(candidate['skills'])}</p>
                            <p><strong>Match Score:</strong> {candidate['match']}%</p>
                            <p><strong>AI Recommendation:</strong> {
                                "Strong match, proceed to interview" if candidate['match'] > 85 
                                else "Potential match, consider technical assessment first"
                            }</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.button(f"View Details", key=f"view_{candidate['name']}")
                        st.button(f"Shortlist", key=f"shortlist_{candidate['name']}")

# ATS Integration page
def display_ats_integration(agent):
    st.markdown('<h2 class="sub-header">ATS Integration</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="info-text">
            Connect with your Applicant Tracking System to streamline candidate management.
            Import candidates, sync job postings, and track applicant status across platforms.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ATS Connection
    col1, col2 = st.columns(2)
    
    with col1:
        ats_provider = st.selectbox(
            "ATS Provider", 
            ["Workday", "Greenhouse", "Lever", "BambooHR", "Taleo", "Other"]
        )
    
    with col2:
        connection_status = st.selectbox(
            "Connection Status", 
            ["Connected", "Not Connected"], 
            index=1
        )
    
    # If not connected
    if connection_status == "Not Connected":
        st.markdown('<h3 class="sub-header">Connect to ATS</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            api_key = st.text_input("API Key", type="password")
        with col2:
            api_endpoint = st.text_input("API Endpoint URL")
        
        connect_btn = st.button("Connect to ATS", type="primary")
    
    # If connected
    else:
        st.markdown('<h3 class="sub-header">ATS Operations</h3>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Import Candidates", "Sync Job Postings", "Candidate Status"])
        
        with tab1:
            st.markdown("""
            <div class="card">
                <h4 style="color: #1E88E5;">Import Candidates from ATS</h4>
                <p>Select job positions to import candidates for review and processing.</p>
            </div>
            """, unsafe_allow_html=True)
            
            positions = st.multiselect(
                "Select Job Positions", 
                ["Senior Python Developer", "Data Scientist", "Product Manager", "UX Designer"]
            )
            
            import_btn = st.button("Import Candidates", type="primary")
        
        with tab2:
            st.markdown("""
            <div class="card">
                <h4 style="color: #1E88E5;">Sync Job Postings</h4>
                <p>Synchronize job descriptions between HR AI Assistant and your ATS.</p>
            </div>
            """, unsafe_allow_html=True)
            
            sync_direction = st.radio(
                "Sync Direction", 
                ["Import from ATS", "Export to ATS", "Two-way Sync"]
            )
            
            sync_btn = st.button("Start Sync", type="primary")
        
        with tab3:
            st.markdown("""
            <div class="card">
                <h4 style="color: #1E88E5;">Update Candidate Status</h4>
                <p>Update candidate application status and sync with your ATS.</p>
            </div>
            """, unsafe_allow_html=True)
            
            candidate = st.selectbox(
                "Select Candidate", 
                ["John Smith", "Sarah Johnson", "Michael Wong", "Emma Davis"]
            )
            
            status = st.selectbox(
                "Application Status", 
                ["New", "Screening", "Interview", "Technical Assessment", "Offer", "Hired", "Rejected"]
            )
            
            update_btn = st.button("Update Status", type="primary")

# Calendar Management page
def display_calendar_management(agent):
    st.markdown('<h2 class="sub-header">Calendar Management</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="info-text">
            Manage interview scheduling, coordinate with hiring teams, and send automated
            calendar invites to candidates.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calendar Connection Status
    col1, col2 = st.columns(2)
    
    with col1:
        calendar_provider = st.selectbox(
            "Calendar Provider", 
            ["Google Calendar", "Microsoft Outlook", "Apple Calendar", "Other"]
        )
    
    with col2:
        connection_status = st.selectbox(
            "Connection Status", 
            ["Connected", "Not Connected"], 
            index=1
        )
    
    # If not connected
    if connection_status == "Not Connected":
        st.markdown('<h3 class="sub-header">Connect Calendar</h3>', unsafe_allow_html=True)
        
        auth_btn = st.button("Authorize Calendar Access", type="primary")
        
        if auth_btn:
            st.info("Redirecting to authorization page...")
    
    # If connected
    else:
        tab1, tab2, tab3 = st.tabs(["Schedule Interview", "View Calendar", "Settings"])
        
        with tab1:
            st.markdown('<h3 class="sub-header">Schedule New Interview</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                candidate = st.selectbox(
                    "Candidate", 
                    ["John Smith", "Sarah Johnson", "Michael Wong", "Emma Davis"]
                )
                candidate_email = st.text_input("Candidate Email")
                position = st.selectbox(
                    "Position", 
                    ["Senior Python Developer", "Data Scientist", "Product Manager", "UX Designer"]
                )
            
            with col2:
                interview_type = st.selectbox(
                    "Interview Type", 
                    ["Technical", "Behavioral", "HR Round", "Final Round"]
                )
                interview_date = st.date_input("Interview Date", key="schedule_interview_date")
                interview_time = st.time_input("Interview Time")
            
            interviewers = st.multiselect(
                "Interviewers", 
                ["Alex Manager", "Taylor Tech Lead", "Jordan HR", "Casey Director"]
            )
            
            location = st.radio(
                "Interview Location", 
                ["Zoom/Teams Meeting", "Phone Call", "In-person"]
            )
            
            if location == "Zoom/Teams Meeting":
                meeting_link = st.text_input("Meeting Link")
            elif location == "In-person":
                office_location = st.text_input("Office Address")
            
            notes = st.text_area("Additional Notes")
            
            schedule_btn = st.button("Schedule Interview", type="primary")
        
        with tab2:
            st.markdown('<h3 class="sub-header">Upcoming Interviews</h3>', unsafe_allow_html=True)
            
            # Mock calendar data
            interviews = [
                {"candidate": "John Smith", "position": "Senior Python Developer", "date": "Sep 10, 2025", "time": "10:00 AM"},
                {"candidate": "Sarah Johnson", "position": "Data Scientist", "date": "Sep 11, 2025", "time": "2:30 PM"},
                {"candidate": "Michael Wong", "position": "Senior Python Developer", "date": "Sep 12, 2025", "time": "11:15 AM"},
            ]
            
            for interview in interviews:
                st.markdown(f"""
                <div class="card">
                    <h4 style="color: #1E88E5;">{interview['candidate']} - {interview['position']}</h4>
                    <p><strong>Date & Time:</strong> {interview['date']} at {interview['time']}</p>
                    <p><strong>Interviewers:</strong> Alex Manager, Taylor Tech Lead</p>
                    <p><strong>Location:</strong> Zoom Meeting</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<h3 class="sub-header">Calendar Settings</h3>', unsafe_allow_html=True)
            
            st.checkbox("Send automatic reminders to candidates (24h before)")
            st.checkbox("Send automatic reminders to interviewers (1h before)")
            st.checkbox("Add buffer time between interviews (15 minutes)")
            
            working_hours = st.slider("Working Hours for Scheduling", 8, 18, (9, 17))
            st.write(f"Available for scheduling: {working_hours[0]}:00 AM to {working_hours[1]}:00 PM")
            
            save_settings = st.button("Save Settings", type="primary")

# Interview Analysis page
def display_interview_analysis(agent):
    st.markdown('<h2 class="sub-header">Interview Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="info-text">
            Upload interview transcripts or recordings to analyze candidate responses,
            extract key insights, and get AI-powered evaluation of technical and soft skills.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    upload_type = st.radio("Upload Type", ["Transcript", "Audio Recording"])
    
    if upload_type == "Transcript":
        uploaded_file = st.file_uploader("Upload interview transcript", type=["txt", "docx", "pdf"])
    else:
        uploaded_file = st.file_uploader("Upload interview recording", type=["mp3", "wav", "m4a"])
    
    # Interview details
    if uploaded_file:
        st.markdown('<h3 class="sub-header">Interview Details</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            candidate_name = st.text_input("Candidate Name")
            position = st.selectbox(
                "Position", 
                ["Senior Python Developer", "Data Scientist", "Product Manager", "UX Designer"]
            )
        
        with col2:
            interview_type = st.selectbox(
                "Interview Type", 
                ["Technical", "Behavioral", "HR Round", "Final Round"]
            )
            interviewer = st.text_input("Interviewer Name")
        
        analyze_btn = st.button("Analyze Interview", type="primary")
        
        if analyze_btn:
            with st.spinner("Analyzing interview..."):
                # Placeholder for actual agent analysis
                if agent:
                    # This would be replaced with actual agent call
                    # analysis = agent.analyze_interview(uploaded_file, candidate_name, position)
                    pass
                
                # Mock analysis results
                st.markdown('<h3 class="sub-header">Analysis Results</h3>', unsafe_allow_html=True)
                
                # Technical skills assessment
                st.markdown("""
                <div class="card">
                    <h4 style="color: #1E88E5;">Technical Skills Assessment</h4>
                    <ul>
                        <li><strong>Python Knowledge:</strong> Advanced (Confident responses on decorators, generators, and concurrency)</li>
                        <li><strong>Database Experience:</strong> Intermediate (Good understanding of SQL but limited NoSQL knowledge)</li>
                        <li><strong>System Design:</strong> Advanced (Provided detailed architecture explanations)</li>
                        <li><strong>Problem Solving:</strong> Strong (Solved coding challenge efficiently)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Soft skills assessment
                st.markdown("""
                <div class="card">
                    <h4 style="color: #1E88E5;">Soft Skills Assessment</h4>
                    <ul>
                        <li><strong>Communication:</strong> Excellent (Clear, concise explanations)</li>
                        <li><strong>Teamwork:</strong> Strong (Shared positive examples of collaboration)</li>
                        <li><strong>Leadership:</strong> Moderate (Limited experience but shows potential)</li>
                        <li><strong>Culture Fit:</strong> Strong (Values align with company culture)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Key insights
                st.markdown("""
                <div class="card">
                    <h4 style="color: #1E88E5;">Key Insights</h4>
                    <ul>
                        <li>Candidate demonstrated strong problem-solving skills when discussing previous projects</li>
                        <li>Shows enthusiasm about company's mission and values</li>
                        <li>Has experience with most required technologies but needs training on cloud infrastructure</li>
                        <li>Strong communicator who explains complex concepts clearly</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Overall recommendation
                st.markdown("""
                <div class="card">
                    <h4 style="color: #1E88E5;">Overall Recommendation</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #4CAF50;">Recommended for Hire (Score: 8.5/10)</p>
                    <p>Candidate demonstrates strong technical skills and cultural alignment. Consider additional technical assessment in cloud technologies before making final offer.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("Save Analysis", use_container_width=True)
                with col2:
                    st.button("Share with Team", use_container_width=True)
                with col3:
                    st.button("Proceed to Offer", type="primary", use_container_width=True)


def display_employee_onboarding(agent):
    st.markdown('<h2 class="sub-header">Employee Onboarding</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="info-text">
            Automate the process of welcoming new employees. Create onboarding plans, 
            send welcome emails, schedule introductory meetings, and coordinate system access.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different onboarding functions
    tab1, tab2, tab3, tab4 = st.tabs(["Create Onboarding Plan", "Email Templates", "Access Requests", "Dashboard"])
    
    with tab1:
        st.subheader("New Employee Information")
        
        col1, col2 = st.columns(2)
        with col1:
            employee_name = st.text_input("Full Name", placeholder="Jane Smith")
            position = st.text_input("Position", placeholder="Senior Software Engineer")
            department = st.selectbox("Department", 
                                     ["Engineering", "Marketing", "Sales", "Finance", "Human Resources", "Product", "Design", "Operations"])
            start_date = st.date_input("Start Date", key="onboarding_start_date")
        
        with col2:
            manager = st.text_input("Reporting Manager", placeholder="John Manager")
            team = st.text_input("Team", placeholder="Backend Development")
            location = st.text_input("Office Location", placeholder="New York Office")
            email = st.text_input("Email", placeholder="jane.smith@example.com")
        
        if st.button("Generate Onboarding Plan", type="primary", use_container_width=True):
            if not employee_name:
                st.error("Please enter the employee's name")
            else:
                with st.spinner("Generating comprehensive onboarding plan..."):
                    # Convert start date to string format
                    start_date_str = start_date.strftime("%Y-%m-%d") if start_date else ""
                    
                    # Prepare employee data
                    employee_info = {
                        "name": employee_name,
                        "position": position,
                        "department": department,
                        "start_date": start_date_str,
                        "manager": manager,
                        "team": team,
                        "location": location,
                        "email": email
                    }
                    
                    if agent:
                        try:
                            # Call the onboarding agent to create the plan
                            result = agent.complete_onboarding_process(employee_info)
                            
                            # Store the result in session state for use across tabs
                            st.session_state.onboarding_plan = result.get("onboarding_plan", {})
                            st.session_state.employee_info = employee_info
                            
                            # Display success message
                            st.success(f"Onboarding plan for {employee_name} created successfully!")
                            
                            # Display the plan details
                            with st.expander("Onboarding Plan Details", expanded=True):
                                plan = st.session_state.onboarding_plan
                                
                                # First day instructions
                                if "first_day_instructions" in plan:
                                    st.markdown(f"**First Day Instructions:**  \n{plan['first_day_instructions']}")
                                
                                # Schedule
                                if "schedule" in plan:
                                    st.markdown("**First Week Schedule:**")
                                    for day in plan["schedule"]:
                                        st.markdown(f"**{day['day']} ({day['date']}):**")
                                        for event in day.get("events", []):
                                            st.markdown(f"- {event}")
                                
                                # Key contacts
                                if "key_contacts" in plan:
                                    st.markdown("**Key Contacts:**")
                                    contacts_md = ""
                                    for role, contact in plan.get("key_contacts", {}).items():
                                        contacts_md += f"- **{role.replace('_', ' ').title()}:** {contact.get('name', '')} - {contact.get('email', '')}\n"
                                    st.markdown(contacts_md)
                                
                                # Tasks
                                if "tasks" in plan:
                                    st.markdown("**Onboarding Tasks:**")
                                    for task in plan.get("tasks", []):
                                        st.markdown(f"- **{task.get('task', '')}** ({task.get('timeline', '')}) - *Responsible:* {task.get('responsible', '')}")
                                
                                # System access
                                if "system_access" in plan:
                                    st.markdown("**System Access Required:**")
                                    access_md = ""
                                    for system in plan.get("system_access", []):
                                        access_md += f"- {system}\n"
                                    st.markdown(access_md)
                        except Exception as e:
                            st.error(f"Error generating onboarding plan: {str(e)}")
                    else:
                        # If no agent is available, show a mock plan
                        mock_plan = {
                            "title": f"Onboarding Plan for {employee_name}",
                            "employee_info": employee_info,
                            "first_day_instructions": "Please arrive at 9:00 AM on your first day. Bring your ID and any employment documents.",
                            "schedule": [
                                {
                                    "day": "Day 1",
                                    "date": start_date_str,
                                    "events": [
                                        "9:00 AM - Welcome and Check-in with HR Representative (30 min)",
                                        "9:30 AM - HR Paperwork & Overview with HR Representative (1 hour)",
                                        "10:30 AM - IT Setup and Systems Introduction with IT Support (1 hour)",
                                        "11:30 AM - Workplace Tour with Office Manager (30 min)",
                                        "12:00 PM - Welcome Lunch with Team (1 hour)"
                                    ]
                                }
                            ],
                            "key_contacts": {
                                "manager": {
                                    "name": manager,
                                    "title": "Team Manager",
                                    "email": f"{manager.lower().replace(' ', '.')}@cloudhero.ai"
                                },
                                "hr": {
                                    "name": "HR Team",
                                    "title": "Human Resources",
                                    "email": "hr@cloudhero.ai"
                                }
                            },
                            "tasks": [
                                {"task": "Complete employment paperwork", "timeline": "Before start date", "responsible": "Employee"},
                                {"task": "Prepare workstation", "timeline": "1 day before", "responsible": "IT"},
                                {"task": "Set up email account", "timeline": "1 day before", "responsible": "IT"}
                            ],
                            "system_access": [
                                "Email account",
                                "Intranet access",
                                "HR system access"
                            ]
                        }
                        
                        # Store in session state
                        st.session_state.onboarding_plan = mock_plan
                        st.session_state.employee_info = employee_info
                        
                        # Display mock plan
                        st.success(f"Mock onboarding plan for {employee_name} created!")
                        with st.expander("Onboarding Plan Details", expanded=True):
                            st.markdown(f"**First Day Instructions:**  \n{mock_plan['first_day_instructions']}")
                            
                            st.markdown("**First Week Schedule:**")
                            for day in mock_plan["schedule"]:
                                st.markdown(f"**{day['day']} ({day['date']}):**")
                                for event in day.get("events", []):
                                    st.markdown(f"- {event}")
                            
                            st.markdown("**Key Contacts:**")
                            contacts_md = ""
                            for role, contact in mock_plan.get("key_contacts", {}).items():
                                contacts_md += f"- **{role.replace('_', ' ').title()}:** {contact.get('name', '')} - {contact.get('email', '')}\n"
                            st.markdown(contacts_md)
                            
                            st.markdown("**Onboarding Tasks:**")
                            for task in mock_plan.get("tasks", []):
                                st.markdown(f"- **{task.get('task', '')}** ({task.get('timeline', '')}) - *Responsible:* {task.get('responsible', '')}")
                            
                            st.markdown("**System Access Required:**")
                            access_md = ""
                            for system in mock_plan.get("system_access", []):
                                access_md += f"- {system}\n"
                            st.markdown(access_md)
    
    with tab2:
        st.subheader("Welcome Email Templates")
        
        if 'employee_info' not in st.session_state:
            st.info("Create an onboarding plan first to use email templates")
        else:
            email_type = st.selectbox("Select Email Type", 
                                    ["Welcome Email", "IT Setup Request", "Team Introduction", "First Week Information"])
            
            # Display the appropriate email template based on selection
            if email_type == "Welcome Email":
                template = f"""
                Subject: Welcome to CloudHero With AI, {st.session_state.employee_info.get('name', '')}!
                
                Dear {st.session_state.employee_info.get('name', '')},
                
                Welcome to CloudHero With AI! We are thrilled to have you join our team as {st.session_state.employee_info.get('position', '')}.
                
                Your journey with us begins on {st.session_state.employee_info.get('start_date', '')}. Here's some information to help you get started:
                
                Location: {st.session_state.employee_info.get('location', '')}
                Reporting Manager: {st.session_state.employee_info.get('manager', '')}
                Team: {st.session_state.employee_info.get('team', '')}
                
                What to expect on your first day:
                - Arrival time: 9:00 AM
                - Please bring your ID and any employment documents
                - You'll meet with HR who will guide you through the day
                - You'll receive your equipment and access credentials
                - We've scheduled a team lunch to welcome you!
                
                We're looking forward to having you on board!
                
                Best regards,
                HR Team
                CloudHero With AI
                """
            elif email_type == "IT Setup Request":
                template = f"""
                Subject: IT Setup for {st.session_state.employee_info.get('name', '')} - Starting {st.session_state.employee_info.get('start_date', '')}
                
                Hello IT Team,
                
                We have a new team member, {st.session_state.employee_info.get('name', '')}, joining as {st.session_state.employee_info.get('position', '')} on {st.session_state.employee_info.get('start_date', '')}.
                
                Please prepare the following equipment and access:
                
                Equipment:
                - Laptop (Standard dev configuration)
                - Monitor
                - Keyboard and mouse
                - Headset
                
                System Access:
                - Email account
                - VPN access
                - Project management tools
                - Code repositories
                
                Please ensure everything is ready by {st.session_state.employee_info.get('start_date', '')}, one day before their start date.
                
                Thank you!
                
                Best regards,
                HR Department
                """
            elif email_type == "Team Introduction":
                employee_first_name = st.session_state.employee_info.get('name', '').split()[0] if st.session_state.employee_info.get('name') else ""
                template = f"""
                Subject: Introducing Our New Team Member: {st.session_state.employee_info.get('name', '')}
                
                Hello {st.session_state.employee_info.get('team', '')} Team,
                
                I'm excited to announce that {st.session_state.employee_info.get('name', '')} will be joining our team as {st.session_state.employee_info.get('position', '')} on {st.session_state.employee_info.get('start_date', '')}.
                
                About {employee_first_name}:
                {employee_first_name} comes to us with experience in [background details]. They'll be focusing on [responsibilities].
                
                Please join me in welcoming {employee_first_name} to the team! We've scheduled a team lunch on their first day to give everyone a chance to meet.
                
                Best regards,
                {st.session_state.employee_info.get('manager', '')}
                Team Manager
                """
            else:  # First Week Information
                template = f"""
                Subject: Your First Week at CloudHero With AI
                
                Dear {st.session_state.employee_info.get('name', '')},
                
                Congratulations on completing your first day at CloudHero With AI! We're excited to have you with us.
                
                Here's your schedule for the rest of the week:
                
                Tuesday: Systems Training
                Wednesday: Role-specific Training
                Thursday: Project Introduction
                Friday: First Week Review
                
                Key People to Meet:
                - Your Manager: {st.session_state.employee_info.get('manager', '')}, Team Manager
                - Your Buddy: [Buddy Name], Team Member
                - HR Contact: HR Team, Human Resources
                
                Please let me know if you have any questions or need any assistance.
                
                Best regards,
                HR Team
                CloudHero With AI
                """
            
            # Display the template in a text area that can be edited
            edited_email = st.text_area("Email Content", value=template, height=400)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Copy to Clipboard", use_container_width=True):
                    st.success("Email content copied to clipboard!")
            with col2:
                if st.button("Send Email", type="primary", use_container_width=True):
                    if agent:
                        with st.spinner("Sending email..."):
                            try:
                                # Call the agent to send the email (in a real implementation)
                                result = agent.send_welcome_email(st.session_state.employee_info)
                                st.success("Email sent successfully!")
                            except Exception as e:
                                st.error(f"Error sending email: {str(e)}")
                    else:
                        st.success("Mock email sent successfully!")
    
    with tab3:
        st.subheader("System Access Requests")
        
        if 'employee_info' not in st.session_state:
            st.info("Create an onboarding plan first to manage system access requests")
        else:
            # Display access requirements from the onboarding plan
            if 'onboarding_plan' in st.session_state and 'system_access' in st.session_state.onboarding_plan:
                system_access_list = st.session_state.onboarding_plan.get('system_access', [])
                
                st.markdown("**Required System Access:**")
                for i, system in enumerate(system_access_list):
                    st.checkbox(system, value=True, key=f"access_{i}")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_system = st.text_input("Add Additional System")
                    if st.button("Add System"):
                        if new_system:
                            if 'system_access' not in st.session_state.onboarding_plan:
                                st.session_state.onboarding_plan['system_access'] = []
                            st.session_state.onboarding_plan['system_access'].append(new_system)
                            st.experimental_rerun()
                
                with col2:
                    if st.button("Submit Access Requests", type="primary", use_container_width=True):
                        if agent:
                            with st.spinner("Creating access requests..."):
                                try:
                                    result = agent.create_access_requests(st.session_state.employee_info)
                                    st.success(f"Successfully created {len(system_access_list)} system access requests!")
                                except Exception as e:
                                    st.error(f"Error creating access requests: {str(e)}")
                        else:
                            st.success(f"Mock creation of {len(system_access_list)} system access requests completed!")
            else:
                st.warning("No system access requirements found in the onboarding plan")
    
    with tab4:
        st.subheader("Onboarding Dashboard")
        
        # Create an onboarding status overview
        st.markdown("### Recent Onboarding Activity")
        
        # Create mock data for demonstration
        if 'employee_info' in st.session_state:
            current_employee = st.session_state.employee_info.get('name', 'New Employee')
        else:
            current_employee = "Jane Smith"
            
        onboarding_data = [
            {"name": current_employee, "position": "Senior Software Engineer", "start_date": "2025-09-22", "status": "In Progress", "completion": 0},
            {"name": "John Williams", "position": "Marketing Manager", "start_date": "2025-09-15", "status": "In Progress", "completion": 60},
            {"name": "Emily Chen", "position": "Product Designer", "start_date": "2025-09-08", "status": "Completed", "completion": 100},
            {"name": "Michael Rodriguez", "position": "Sales Representative", "start_date": "2025-09-01", "status": "Completed", "completion": 100}
        ]
        
        # Display as a table
        st.dataframe(
            {
                "Employee": [item["name"] for item in onboarding_data],
                "Position": [item["position"] for item in onboarding_data],
                "Start Date": [item["start_date"] for item in onboarding_data],
                "Status": [item["status"] for item in onboarding_data],
                "Completion": [f"{item['completion']}%" for item in onboarding_data]
            },
            use_container_width=True
        )
        
        # Add statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Onboardings", "2")
        with col2:
            st.metric("Completed This Month", "2")
        with col3:
            st.metric("Avg. Satisfaction Score", "4.8/5")
        
        # Show upcoming start dates
        st.markdown("### Upcoming Start Dates")
        st.markdown("""
        - **Sep 22, 2025**: Jane Smith, Senior Software Engineer
        - **Oct 1, 2025**: Robert Johnson, DevOps Engineer
        - **Oct 15, 2025**: Sarah Miller, UX Researcher
        """)
        
        # Show recent actions
        st.markdown("### Recent Actions")
        st.markdown("""
        - Welcome email sent to Jane Smith
        - IT setup completed for John Williams
        - Onboarding completed for Emily Chen
        - System access granted for Michael Rodriguez
        """)


def display_payroll_management(agent):
    st.markdown('<h2 class="sub-header">Payroll Management</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p class="info-text">
            Manage employee payroll processing, including calculating salaries, handling taxes and deductions,
            generating pay stubs, and creating payroll reports.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different payroll functions
    tab1, tab2, tab3, tab4 = st.tabs(["Process Payroll", "Employee Management", "Tax Management", "Reports"])
    
    with tab1:
        st.subheader("Process Payroll")
        
        # Pay period selection
        col1, col2 = st.columns(2)
        with col1:
            pay_period_type = st.selectbox("Pay Period Type", 
                                          ["Weekly", "Biweekly", "Semi-monthly", "Monthly"])
            
            today = datetime.datetime.now()
            if pay_period_type == "Weekly":
                start_date = today - datetime.timedelta(days=7)
                end_date = today
            elif pay_period_type == "Biweekly":
                start_date = today - datetime.timedelta(days=14)
                end_date = today
            elif pay_period_type == "Semi-monthly":
                # Simplified logic for demo
                if today.day <= 15:
                    start_date = today.replace(day=1)
                    end_date = today.replace(day=15)
                else:
                    start_date = today.replace(day=16)
                    last_day = 28 if today.month == 2 else 30 if today.month in [4, 6, 9, 11] else 31
                    end_date = today.replace(day=last_day)
            else:  # Monthly
                start_date = today.replace(day=1)
                last_day = 28 if today.month == 2 else 30 if today.month in [4, 6, 9, 11] else 31
                end_date = today.replace(day=last_day)
                
            start_date_input = st.date_input("Start Date", value=start_date, key="payroll_start_date")
            end_date_input = st.date_input("End Date", value=end_date, key="payroll_end_date")
            
        with col2:
            pay_date = st.date_input("Pay Date", value=today + datetime.timedelta(days=5), key="payroll_pay_date")
            payment_method = st.selectbox("Payment Method", ["Direct Deposit", "Check", "Cash"])
            include_terminated = st.checkbox("Include Terminated Employees", value=False)
    
        # Employee selection
        st.subheader("Employees")
        
        # Mock employee data
        employees = [
            {"id": "EMP001", "name": "John Smith", "department": "Engineering", "status": "Active", "pay_type": "Salary", "amount": "$75,000/year"},
            {"id": "EMP002", "name": "Jane Doe", "department": "Marketing", "status": "Active", "pay_type": "Hourly", "amount": "$25/hour"},
            {"id": "EMP003", "name": "Robert Johnson", "department": "Finance", "status": "Active", "pay_type": "Salary", "amount": "$85,000/year"},
            {"id": "EMP004", "name": "Emily Williams", "department": "HR", "status": "Active", "pay_type": "Salary", "amount": "$70,000/year"},
            {"id": "EMP005", "name": "Michael Brown", "department": "Engineering", "status": "Active", "pay_type": "Hourly", "amount": "$30/hour"}
        ]
        
        # Display employees in a dataframe with checkboxes
        st.markdown("Select employees to include in this payroll run:")
        
        for i, emp in enumerate(employees):
            col1, col2, col3, col4 = st.columns([0.2, 2, 1.5, 1.5])
            with col1:
                selected = st.checkbox("", value=True, key=f"emp_{i}")
            with col2:
                st.write(f"**{emp['name']}** ({emp['id']})")
            with col3:
                st.write(f"{emp['department']} - {emp['status']}")
            with col4:
                st.write(f"{emp['pay_type']}: {emp['amount']}")
            
        # Hours entry for hourly employees
        st.subheader("Hours Entry (Hourly Employees)")
        
        hourly_employees = [emp for emp in employees if emp['pay_type'] == 'Hourly']
        
        if hourly_employees:
            for i, emp in enumerate(hourly_employees):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{emp['name']}**")
                with col2:
                    st.number_input("Regular Hours", min_value=0.0, max_value=100.0, value=80.0, step=0.5, key=f"reg_hours_{i}")
                with col3:
                    st.number_input("Overtime Hours", min_value=0.0, max_value=40.0, value=0.0, step=0.5, key=f"ot_hours_{i}")
        else:
            st.info("No hourly employees selected")
        
        # Run payroll button
        if st.button("Process Payroll Run", type="primary", use_container_width=True):
            with st.spinner("Processing payroll..."):
                if agent:
                    try:
                        # Format the pay period
                        pay_period = {
                            "start_date": start_date_input.strftime("%Y-%m-%d"),
                            "end_date": end_date_input.strftime("%Y-%m-%d"),
                            "pay_date": pay_date.strftime("%Y-%m-%d"),
                            "period_type": pay_period_type.lower()
                        }
                        
                        # Format employee data
                        employee_data = []
                        for i, emp in enumerate(employees):
                            if st.session_state.get(f"emp_{i}", False):
                                emp_data = {
                                    "id": emp["id"],
                                    "name": emp["name"],
                                    "pay_type": emp["pay_type"].lower(),
                                    "salary": float(emp["amount"].replace("$", "").replace(",", "").replace("/year", "").replace("/hour", "")),
                                    "state": "CA",  # Default state for demo
                                    "allowances": 2,  # Default allowances for demo
                                    "deductions": {
                                        "401k": 0.05,
                                        "health_insurance": 120
                                    }
                                }
                                
                                # Add hours for hourly employees
                                if emp["pay_type"] == "Hourly":
                                    idx = next((j for j, e in enumerate(hourly_employees) if e["id"] == emp["id"]), None)
                                    if idx is not None:
                                        emp_data["hours_worked"] = st.session_state.get(f"reg_hours_{idx}", 80)
                                        emp_data["overtime_hours"] = st.session_state.get(f"ot_hours_{idx}", 0)
                                
                                employee_data.append(emp_data)
                        
                        # Process payroll using the agent
                        result = agent.calculate_payroll(employee_data, pay_period)
                        
                        # Show success message
                        st.success(f"Payroll processed successfully for {len(employee_data)} employees.")
                        
                        # Display summary
                        st.subheader("Payroll Summary")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Gross Pay", f"${result.get('total_gross', 0):.2f}")
                        with col2:
                            st.metric("Total Taxes", f"${result.get('total_taxes', 0):.2f}")
                        with col3:
                            st.metric("Total Deductions", f"${result.get('total_deductions', 0):.2f}")
                        with col4:
                            st.metric("Total Net Pay", f"${result.get('total_net', 0):.2f}")
                        
                        # Store result in session state for use in other tabs
                        st.session_state.payroll_result = result
                        
                    except Exception as e:
                        st.error(f"Error processing payroll: {str(e)}")
                        
                else:
                    # Show mock result if no agent is available
                    mock_result = {
                        "pay_period": {
                            "start_date": start_date_input.strftime("%Y-%m-%d"),
                            "end_date": end_date_input.strftime("%Y-%m-%d"),
                            "pay_date": pay_date.strftime("%Y-%m-%d"),
                            "period_type": pay_period_type.lower()
                        },
                        "total_gross": 14500.00,
                        "total_taxes": 3625.00,
                        "total_deductions": 870.00,
                        "total_net": 10005.00,
                        "employee_payments": [
                            {"employee_name": "John Smith", "gross_pay": 2884.62, "total_taxes": 721.15, "net_pay": 2019.23},
                            {"employee_name": "Jane Doe", "gross_pay": 2000.00, "total_taxes": 500.00, "net_pay": 1380.00},
                            {"employee_name": "Robert Johnson", "gross_pay": 3269.23, "total_taxes": 817.31, "net_pay": 2287.92},
                            {"employee_name": "Emily Williams", "gross_pay": 2692.31, "total_taxes": 673.08, "net_pay": 1884.62},
                            {"employee_name": "Michael Brown", "gross_pay": 2400.00, "total_taxes": 600.00, "net_pay": 1656.00}
                        ]
                    }
                    
                    # Show success message
                    st.success(f"Mock payroll processed successfully for {len(employees)} employees.")
                    
                    # Display summary
                    st.subheader("Payroll Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Gross Pay", f"${mock_result['total_gross']:.2f}")
                    with col2:
                        st.metric("Total Taxes", f"${mock_result['total_taxes']:.2f}")
                    with col3:
                        st.metric("Total Deductions", f"${mock_result['total_deductions']:.2f}")
                    with col4:
                        st.metric("Total Net Pay", f"${mock_result['total_net']:.2f}")
                    
                    # Store result in session state for use in other tabs
                    st.session_state.payroll_result = mock_result
                
                # Actions after processing
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("Download Pay Stubs", use_container_width=True)
                with col2:
                    st.button("Download Payroll Report", use_container_width=True)
                with col3:
                    st.button("Process Payments", use_container_width=True)
    
    with tab2:
        st.subheader("Employee Management")
        
        # Tabs for employee management functions
        employee_tabs = st.tabs(["Employee List", "Add Employee", "Modify Employee", "Deductions"])
        
        with employee_tabs[0]:
            # Show employee list
            st.markdown("**Employee List**")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                dept_filter = st.multiselect("Department", ["All", "Engineering", "Marketing", "Finance", "HR"], default=["All"])
            with col2:
                status_filter = st.multiselect("Status", ["All", "Active", "Terminated", "On Leave"], default=["All"])
            with col3:
                pay_filter = st.multiselect("Pay Type", ["All", "Salary", "Hourly"], default=["All"])
            
            # Display employee table
            st.dataframe(
                {
                    "ID": [emp["id"] for emp in employees],
                    "Name": [emp["name"] for emp in employees],
                    "Department": [emp["department"] for emp in employees],
                    "Status": [emp["status"] for emp in employees],
                    "Pay Type": [emp["pay_type"] for emp in employees],
                    "Pay Rate": [emp["amount"] for emp in employees]
                },
                use_container_width=True
            )
        
        with employee_tabs[1]:
            # Add new employee form
            st.markdown("**Add New Employee**")
            
            col1, col2 = st.columns(2)
            with col1:
                new_emp_name = st.text_input("Full Name", placeholder="John Doe")
                new_emp_email = st.text_input("Email", placeholder="john.doe@example.com")
                new_emp_phone = st.text_input("Phone", placeholder="(555) 123-4567")
                new_emp_address = st.text_area("Address", placeholder="123 Main St\nCity, State 12345", height=100)
            
            with col2:
                new_emp_department = st.selectbox("Department", ["Engineering", "Marketing", "Finance", "HR", "Sales", "Operations"])
                new_emp_paytype = st.selectbox("Pay Type", ["Salary", "Hourly"])
                
                if new_emp_paytype == "Salary":
                    new_emp_pay = st.number_input("Annual Salary ($)", min_value=0, value=75000)
                else:
                    new_emp_pay = st.number_input("Hourly Rate ($)", min_value=0.0, value=25.0, step=0.5)
                
                new_emp_start_date = st.date_input("Start Date", key="emp_start_date")
            
            # Add employee button
            if st.button("Add Employee", type="primary", use_container_width=True):
                if not new_emp_name:
                    st.error("Employee name is required")
                else:
                    st.success(f"Employee {new_emp_name} added successfully!")
        
        with employee_tabs[2]:
            # Modify existing employee
            st.markdown("**Modify Employee**")
            
            # Select employee to modify
            selected_emp_id = st.selectbox("Select Employee", 
                                          [f"{emp['name']} ({emp['id']})" for emp in employees])
            
            if selected_emp_id:
                selected_emp = next((emp for emp in employees if f"{emp['name']} ({emp['id']})" == selected_emp_id), None)
                
                if selected_emp:
                    col1, col2 = st.columns(2)
                    with col1:
                        mod_emp_name = st.text_input("Full Name", value=selected_emp["name"], key="mod_name")
                        mod_emp_department = st.selectbox("Department", ["Engineering", "Marketing", "Finance", "HR", "Sales", "Operations"], 
                                                        index=["Engineering", "Marketing", "Finance", "HR", "Sales", "Operations"].index(selected_emp["department"]),
                                                        key="mod_dept")
                    
                    with col2:
                        mod_emp_status = st.selectbox("Status", ["Active", "Terminated", "On Leave"], 
                                                     index=["Active", "Terminated", "On Leave"].index(selected_emp["status"]),
                                                     key="mod_status")
                        
                        mod_emp_paytype = st.selectbox("Pay Type", ["Salary", "Hourly"], 
                                                      index=["Salary", "Hourly"].index(selected_emp["pay_type"]),
                                                      key="mod_paytype")
                        
                        if mod_emp_paytype == "Salary":
                            current_pay = int(selected_emp["amount"].replace("$", "").replace(",", "").replace("/year", ""))
                            mod_emp_pay = st.number_input("Annual Salary ($)", min_value=0, value=current_pay, key="mod_pay_salary")
                        else:
                            current_pay = float(selected_emp["amount"].replace("$", "").replace("/hour", ""))
                            mod_emp_pay = st.number_input("Hourly Rate ($)", min_value=0.0, value=current_pay, step=0.5, key="mod_pay_hourly")
                    
                    # Save changes button
                    if st.button("Save Changes", type="primary", use_container_width=True):
                        st.success(f"Changes for {mod_emp_name} saved successfully!")
        
        with employee_tabs[3]:
            # Employee deductions
            st.markdown("**Manage Employee Deductions**")
            
            # Select employee
            deduction_emp_id = st.selectbox("Select Employee", 
                                           [f"{emp['name']} ({emp['id']})" for emp in employees],
                                           key="deduction_emp")
            
            if deduction_emp_id:
                # Display current deductions
                st.markdown("**Current Deductions**")
                
                # Mock deduction data
                deductions = [
                    {"type": "401(k)", "amount": "5%", "pre_tax": True},
                    {"type": "Health Insurance", "amount": "$120.00", "pre_tax": True},
                    {"type": "Dental Insurance", "amount": "$25.00", "pre_tax": True},
                    {"type": "Vision Insurance", "amount": "$15.00", "pre_tax": True}
                ]
                
                # Show deductions in a table
                st.dataframe(
                    {
                        "Deduction Type": [d["type"] for d in deductions],
                        "Amount": [d["amount"] for d in deductions],
                        "Pre-Tax": [d["pre_tax"] for d in deductions]
                    },
                    use_container_width=True
                )
                
                # Add new deduction
                st.markdown("**Add New Deduction**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_deduction_type = st.selectbox("Deduction Type", [
                        "401(k)", "Health Insurance", "Dental Insurance", "Vision Insurance", 
                        "Life Insurance", "Disability Insurance", "FSA", "HSA", "Garnishment", "Other"
                    ])
                
                with col2:
                    deduction_amount_type = st.radio("Amount Type", ["Percentage", "Fixed Amount"], horizontal=True)
                    if deduction_amount_type == "Percentage":
                        new_deduction_amount = st.number_input("Percentage (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
                    else:
                        new_deduction_amount = st.number_input("Amount ($)", min_value=0.0, value=50.0, step=5.0)
                
                with col3:
                    new_deduction_pretax = st.checkbox("Pre-Tax", value=True)
                    new_deduction_start = st.date_input("Start Date", key="deduction_start_date")
                
                # Add deduction button
                if st.button("Add Deduction", type="primary", use_container_width=True):
                    st.success(f"Deduction added successfully!")
    
    with tab3:
        st.subheader("Tax Management")
        
        # Tabs for tax management functions
        tax_tabs = st.tabs(["Tax Settings", "Tax Filing", "Year-End"])
        
        with tax_tabs[0]:
            # Tax settings
            st.markdown("**Tax Configuration**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Federal Tax Settings**")
                st.selectbox("Federal Filing Frequency", ["Quarterly", "Monthly", "Semi-Weekly"])
                st.text_input("Federal Employer ID (FEIN)", placeholder="12-3456789")
                
                st.markdown("**Social Security & Medicare**")
                ss_rate = st.number_input("Social Security Rate (%)", min_value=0.0, max_value=20.0, value=6.2, step=0.1)
                medicare_rate = st.number_input("Medicare Rate (%)", min_value=0.0, max_value=10.0, value=1.45, step=0.01)
                st.write(f"Current Social Security Wage Base: $147,000")
            
            with col2:
                st.markdown("**State Tax Settings**")
                default_state = st.selectbox("Default State", ["California", "New York", "Texas", "Florida", "Illinois"])
                st.selectbox("State Filing Frequency", ["Quarterly", "Monthly"])
                st.text_input("State Employer ID", placeholder="123-4567-8")
                
                st.markdown("**Unemployment Insurance**")
                sui_rate = st.number_input("State Unemployment Rate (%)", min_value=0.0, max_value=10.0, value=3.4, step=0.1)
                futa_rate = st.number_input("FUTA Rate (%)", min_value=0.0, max_value=10.0, value=0.6, step=0.1)
            
            # Save settings button
            if st.button("Save Tax Settings", type="primary", use_container_width=True):
                st.success("Tax settings saved successfully!")
        
        with tax_tabs[1]:
            # Tax filing
            st.markdown("**Upcoming Tax Filings**")
            
            # Mock tax filing data
            tax_filings = [
                {"form": "941", "description": "Employer's Quarterly Federal Tax Return", "due_date": "Oct 31, 2025", "status": "Pending"},
                {"form": "DE 9", "description": "Quarterly Contribution Return", "due_date": "Oct 31, 2025", "status": "Pending"},
                {"form": "DE 9C", "description": "Quarterly Contribution Return and Report of Wages", "due_date": "Oct 31, 2025", "status": "Pending"},
                {"form": "940", "description": "Employer's Annual Federal Unemployment Tax Return", "due_date": "Jan 31, 2026", "status": "Not Started"}
            ]
            
            # Show tax filings in a table
            st.dataframe(
                {
                    "Form": [f["form"] for f in tax_filings],
                    "Description": [f["description"] for f in tax_filings],
                    "Due Date": [f["due_date"] for f in tax_filings],
                    "Status": [f["status"] for f in tax_filings]
                },
                use_container_width=True
            )
            
            # Prepare filing button
            col1, col2 = st.columns(2)
            with col1:
                filing_form = st.selectbox("Select Form to Prepare", [f["form"] for f in tax_filings])
            
            with col2:
                st.write("")
                st.write("")
                prepare_btn = st.button("Prepare Selected Filing", use_container_width=True)
                
                if prepare_btn:
                    st.info(f"Preparing {filing_form} filing based on recent payroll data...")
        
        with tax_tabs[2]:
            # Year-end tax processes
            st.markdown("**Year-End Tax Processing**")
            
            # W-2 generation
            st.markdown("**W-2 Processing**")
            tax_year = st.selectbox("Tax Year", ["2025", "2024", "2023"])
            
            col1, col2 = st.columns(2)
            with col1:
                w2_status = st.selectbox("W-2 Status", ["Not Started", "In Progress", "Completed"])
                w2_delivery = st.selectbox("Delivery Method", ["Electronic", "Paper", "Both"])
            
            with col2:
                st.write("")
                st.write("")
                if st.button("Generate W-2 Forms", type="primary", use_container_width=True):
                    st.success(f"Started W-2 generation process for {tax_year}.")
            
            # 1099 processing
            st.markdown("**1099 Processing**")
            
            col1, col2 = st.columns(2)
            with col1:
                ten99_status = st.selectbox("1099 Status", ["Not Started", "In Progress", "Completed"])
                ten99_delivery = st.selectbox("1099 Delivery Method", ["Electronic", "Paper", "Both"])
            
            with col2:
                st.write("")
                st.write("")
                if st.button("Generate 1099 Forms", type="primary", use_container_width=True):
                    st.success(f"Started 1099 generation process for {tax_year}.")
            
            # ACA reporting
            st.markdown("**ACA Reporting (1094-C/1095-C)**")
            
            col1, col2 = st.columns(2)
            with col1:
                aca_status = st.selectbox("ACA Status", ["Not Started", "In Progress", "Completed"])
            
            with col2:
                st.write("")
                st.write("")
                if st.button("Generate ACA Forms", type="primary", use_container_width=True):
                    st.success(f"Started ACA form generation process for {tax_year}.")
    
    with tab4:
        st.subheader("Payroll Reports")
        
        # Report selection
        report_type = st.selectbox("Select Report Type", [
            "Payroll Summary", "Payroll Detail", "Tax Liabilities", 
            "Deduction Summary", "Department Costs", "Employee Earnings",
            "Contractor Payments", "Payroll Register", "Check Register"
        ])
        
        # Date range
        col1, col2, col3 = st.columns(3)
        with col1:
            report_date_range = st.selectbox("Date Range", [
                "Current Pay Period", "Previous Pay Period", "Current Month",
                "Previous Month", "Current Quarter", "Year to Date", "Custom"
            ])
        
        with col2:
            if report_date_range == "Custom":
                report_start_date = st.date_input("Start Date", value=datetime.datetime.now().replace(day=1), key="report_start_date")
            else:
                report_start_date = None
        
        with col3:
            if report_date_range == "Custom":
                report_end_date = st.date_input("End Date", value=datetime.datetime.now(), key="report_end_date")
            else:
                report_end_date = None
        
        # Generate report button
        generate_report_btn = st.button("Generate Report", type="primary", use_container_width=True)
        
        if generate_report_btn:
            with st.spinner("Generating report..."):
                if agent and hasattr(agent, 'generate_payroll_report') and 'payroll_result' in st.session_state:
                    try:
                        # Get report data from agent
                        if report_type == "Payroll Summary":
                            report = agent.generate_payroll_report(st.session_state.payroll_result, "summary")
                        elif report_type == "Tax Liabilities":
                            report = agent.generate_payroll_report(st.session_state.payroll_result, "tax")
                        else:
                            # Default to summary for other report types in this demo
                            report = agent.generate_payroll_report(st.session_state.payroll_result, "summary")
                        
                        # Display report
                        st.success(f"{report_type} generated successfully!")
                        
                        # Display report content based on type
                        if report_type == "Payroll Summary":
                            st.markdown(f"**Pay Period:** {report['period']['start_date']} to {report['period']['end_date']}")
                            st.markdown(f"**Pay Date:** {report['period']['pay_date']}")
                            st.markdown(f"**Total Employees:** {report['totals']['employees']}")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Gross Pay", report['totals']['gross'])
                            with col2:
                                st.metric("Taxes", report['totals'].get('taxes', '$0.00'))
                            with col3:
                                st.metric("Deductions", report['totals'].get('deductions', '$0.00'))
                            with col4:
                                st.metric("Net Pay", report['totals']['net'])
                            
                            # Employer taxes if available
                            if 'employer_taxes' in report:
                                st.markdown("**Employer Taxes**")
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Social Security", report['employer_taxes']['social_security'])
                                with col2:
                                    st.metric("Medicare", report['employer_taxes']['medicare'])
                                with col3:
                                    st.metric("FUTA", report['employer_taxes'].get('futa', '$0.00'))
                                with col4:
                                    st.metric("SUI", report['employer_taxes'].get('sui', '$0.00'))
                                
                        elif report_type == "Tax Liabilities":
                            st.markdown(f"**Pay Period:** {report['period']['start_date']} to {report['period']['end_date']}")
                            
                            st.markdown("**Employee Tax Withholdings**")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Federal Income Tax", report['tax_liabilities']['federal_income_tax'])
                                st.metric("Social Security (Employee)", report['tax_liabilities']['social_security']['employee'])
                            with col2:
                                st.metric("State Income Tax", report['tax_liabilities']['state_income_tax'])
                                st.metric("Medicare (Employee)", report['tax_liabilities']['medicare']['employee'])
                            
                            st.markdown("**Employer Tax Liabilities**")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Social Security (Employer)", report['tax_liabilities']['social_security']['employer'])
                                st.metric("FUTA", report['tax_liabilities'].get('futa', '$0.00'))
                            with col2:
                                st.metric("Medicare (Employer)", report['tax_liabilities']['medicare']['employer'])
                                st.metric("SUI", report['tax_liabilities'].get('sui', '$0.00'))
                            
                            st.metric("Total Tax Liability", report['tax_liabilities']['total_tax_liability'])
                        
                        else:
                            # Generic display for other report types
                            st.json(report)
                        
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                else:
                    # Mock report data
                    st.markdown(f"**{report_type}**")
                    st.markdown("**Pay Period:** 2025-09-01 to 2025-09-15")
                    st.markdown("**Pay Date:** 2025-09-20")
                    
                    if report_type == "Payroll Summary":
                        # Mock summary report
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Gross Pay", "$14,500.00")
                        with col2:
                            st.metric("Taxes", "$3,625.00")
                        with col3:
                            st.metric("Deductions", "$870.00")
                        with col4:
                            st.metric("Net Pay", "$10,005.00")
                        
                        st.markdown("**Employee Count:** 5")
                        
                        # Employer taxes
                        st.markdown("**Employer Taxes**")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Social Security", "$899.00")
                        with col2:
                            st.metric("Medicare", "$210.25")
                        with col3:
                            st.metric("FUTA", "$87.00")
                        with col4:
                            st.metric("SUI", "$493.00")
                    
                    elif report_type == "Tax Liabilities":
                        # Mock tax liability report
                        st.markdown("**Employee Tax Withholdings**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Federal Income Tax", "$2,175.00")
                            st.metric("Social Security (Employee)", "$899.00")
                        with col2:
                            st.metric("State Income Tax", "$580.00")
                            st.metric("Medicare (Employee)", "$210.25")
                        
                        st.markdown("**Employer Tax Liabilities**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Social Security (Employer)", "$899.00")
                            st.metric("FUTA", "$87.00")
                        with col2:
                            st.metric("Medicare (Employer)", "$210.25")
                            st.metric("SUI", "$493.00")
                        
                        st.metric("Total Tax Liability", "$5,553.50")
                    
                    elif report_type == "Department Costs":
                        # Mock department cost report
                        departments = {
                            "Engineering": {"employees": 2, "gross": "$5,284.62", "taxes": "$1,321.15", "net": "$3,675.23"},
                            "Marketing": {"employees": 1, "gross": "$2,000.00", "taxes": "$500.00", "net": "$1,380.00"},
                            "Finance": {"employees": 1, "gross": "$3,269.23", "taxes": "$817.31", "net": "$2,287.92"},
                            "HR": {"employees": 1, "gross": "$2,692.31", "taxes": "$673.08", "net": "$1,884.62"}
                        }
                        
                        for dept, data in departments.items():
                            st.markdown(f"**{dept}**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Employees", data["employees"])
                            with col2:
                                st.metric("Gross Pay", data["gross"])
                            with col3:
                                st.metric("Taxes", data["taxes"])
                            with col4:
                                st.metric("Net Pay", data["net"])
                            st.markdown("---")
                    
                    else:
                        # Generic mock data for other report types
                        st.info("Report generated successfully! Download using the button below.")
                
                # Report actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button("Download as PDF", "Mock PDF data", file_name=f"{report_type.replace(' ', '_')}.pdf", use_container_width=True)
                with col2:
                    st.download_button("Download as Excel", "Mock Excel data", file_name=f"{report_type.replace(' ', '_')}.xlsx", use_container_width=True)
                with col3:
                    st.download_button("Download as CSV", "Mock CSV data", file_name=f"{report_type.replace(' ', '_')}.csv", use_container_width=True)


if __name__ == "__main__":
    main()
