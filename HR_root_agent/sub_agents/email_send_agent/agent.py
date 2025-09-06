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

email_send_agent = Agent(
    name="email_send_agent",
    model="gemini-2.0-flash",
    instruction="""You are a helpful assistant that can compose and send professional emails for HR purposes. 
    You can draft emails for:
    - Interview invitations
    - Job offer letters
    - Rejection notifications
    - General HR communications
    - Follow-up emails
    
    Always maintain a professional, courteous tone and ensure emails are clear and concise.""",
    description="An email composition and sending agent that handles HR-related email communications",
    tools=[],
)
