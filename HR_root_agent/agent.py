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


def list_sub_agents():
    """Lists the available sub-agents."""
    return {
        "job_description_agent": "Generates job descriptions.",
        "email_send_agent": "Sends emails.",
        "interview_transcript_agent": "Analyzes interview transcripts.",
        "resume_analyzer_agent": "Analyzes resumes.",
        "scheduling_agent": "Schedules interviews.",
        "ats_agent": "Manages the applicant tracking system.",
    }

root_agent = Agent(
    name="HR_root_agent",
    model=Gemini(api_key=os.getenv('GOOGLE_API_KEY')),
    description="A comprehensive HR management system that coordinates various HR processes including job descriptions, email communications, interview analysis, resume evaluation, and scheduling",
    instruction="""You are a comprehensive HR management assistant that can coordinate and perform various HR tasks. 
    You have access to specialized sub-agents for:
    - Job description generation and management
    - Professional email composition and sending
    - Interview transcript analysis and summarization
    - Resume parsing and candidate evaluation
    - Interview scheduling and calendar coordination
    - ATS (Applicant Tracking System) for complete hiring workflow management
    
    You can delegate specific tasks to the appropriate sub-agents or coordinate between them for complex workflows.""",
    sub_agents=[
        job_description_agent,
        email_send_agent,
        interview_transcript_agent,
        resume_analyzer_agent,
        scheduling_agent,
        ats_agent
    ],
    tools=[list_sub_agents],
)