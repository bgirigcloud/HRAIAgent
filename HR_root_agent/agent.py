# Load environment variables from .env file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.google_llm import Gemini

# Import sub-agents
from sub_agents.job_description.agent import job_description_agent
from sub_agents.email_send_agent.agent import email_send_agent
from sub_agents.interview_transcript_agent.agent import interview_transcript_agent
from sub_agents.resume_analyzer.agent import resume_analyzer_agent
from sub_agents.scheduling_agent.agent import scheduling_agent
from sub_agents.ats_tool.agent import ats_agent

# Import new agents
try:
    from sub_agents.payroll_agent.agent import PayrollAgent
    payroll_agent = PayrollAgent()
    HAS_PAYROLL_AGENT = True
except ImportError:
    payroll_agent = None
    HAS_PAYROLL_AGENT = False
    print("Warning: Payroll agent not available.")

try:
    from sub_agents.onboarding_agent.agent import OnboardingAgent
    onboarding_agent = OnboardingAgent()
    HAS_ONBOARDING_AGENT = True
except ImportError:
    onboarding_agent = None
    HAS_ONBOARDING_AGENT = False
    print("Warning: Onboarding agent not available.")

# Import new advanced agents
try:
    from sub_agents.neo4j_agent import neo4j_agent
    HAS_NEO4J_AGENT = True
except ImportError:
    neo4j_agent = None
    HAS_NEO4J_AGENT = False
    print("Warning: Neo4j agent not available. Install dependencies with: pip install neo4j")

try:
    from sub_agents.pgvector_db_agent import pgvector_db_agent
    HAS_PGVECTOR_AGENT = True
except ImportError:
    pgvector_db_agent = None
    HAS_PGVECTOR_AGENT = False
    print("Warning: PGVector DB agent not available. Install dependencies with: pip install psycopg2-binary numpy")

try:
    from sub_agents.rag_agent import rag_agent
    HAS_RAG_AGENT = True
    # Set vector DB agent for the RAG agent to use
    if HAS_PGVECTOR_AGENT:
        rag_agent.set_vector_db_agent(pgvector_db_agent)
except ImportError:
    rag_agent = None
    HAS_RAG_AGENT = False
    print("Warning: RAG agent not available. Install dependencies with: pip install sentence-transformers")

try:
    from sub_agents.mcp_server_agent import mcp_server_agent
    HAS_MCP_SERVER_AGENT = True
except ImportError:
    mcp_server_agent = None
    HAS_MCP_SERVER_AGENT = False
    print("Warning: MCP Server agent not available. Install dependencies with: pip install fastapi uvicorn")


def list_sub_agents():
    """Lists the available sub-agents."""
    agents = {
        "job_description_agent": "Generates job descriptions.",
        "email_send_agent": "Sends emails.",
        "interview_transcript_agent": "Analyzes interview transcripts.",
        "resume_analyzer_agent": "Analyzes resumes.",
        "scheduling_agent": "Schedules interviews.",
        "ats_agent": "Manages the applicant tracking system.",
    }
    
    if HAS_ONBOARDING_AGENT:
        agents["onboarding_agent"] = "Automates the process of welcoming new employees."
    
    if HAS_PAYROLL_AGENT:
        agents["payroll_agent"] = "Automates payroll processing, tax management, and reporting."
    
    if HAS_NEO4J_AGENT:
        agents["neo4j_agent"] = "Provides graph database capabilities for organizational relationships."
        
    if HAS_PGVECTOR_AGENT:
        agents["pgvector_db_agent"] = "Manages vector database operations for similarity search."
        
    if HAS_RAG_AGENT:
        agents["rag_agent"] = "Provides Retrieval Augmented Generation for context-aware responses."
        
    if HAS_MCP_SERVER_AGENT:
        agents["mcp_server_agent"] = "Serves as a Model Context Protocol server for integrations."
        
    return agents

# Create a list of available sub-agents
sub_agents_list = [
    job_description_agent,
    email_send_agent,
    interview_transcript_agent,
    resume_analyzer_agent,
    scheduling_agent,
    ats_agent
]

# Add optional agents if available
if HAS_ONBOARDING_AGENT:
    sub_agents_list.append(onboarding_agent)

if HAS_PAYROLL_AGENT:
    sub_agents_list.append(payroll_agent)

if HAS_NEO4J_AGENT:
    sub_agents_list.append(neo4j_agent)
    
if HAS_PGVECTOR_AGENT:
    sub_agents_list.append(pgvector_db_agent)
    
if HAS_RAG_AGENT:
    sub_agents_list.append(rag_agent)
    
if HAS_MCP_SERVER_AGENT:
    sub_agents_list.append(mcp_server_agent)

root_agent = Agent(
    name="HR_root_agent",
    model=Gemini(api_key=os.getenv('GOOGLE_API_KEY')),
    description="A comprehensive HR management system that coordinates various HR processes",
    instruction="""You are a comprehensive HR management assistant that can coordinate and perform various HR tasks. 
    You have access to specialized sub-agents for:
    - Job description generation and management
    - Professional email composition and sending
    - Interview transcript analysis and summarization
    - Resume parsing and candidate evaluation
    - Interview scheduling and calendar coordination
    - ATS (Applicant Tracking System) for complete hiring workflow management
    - Employee onboarding process automation
    - Payroll processing and management
    - Graph database operations for organizational relationships (Neo4j)
    - Vector database operations for similarity search (PGVector)
    - Retrieval Augmented Generation for context-aware responses (RAG)
    - Model Context Protocol server for integrations (MCP)
    
    You can delegate specific tasks to the appropriate sub-agents or coordinate between them for complex workflows.""",
    sub_agents=sub_agents_list,
    tools=[list_sub_agents],
)