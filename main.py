#!/usr/bin/env python3
"""
Main entry point for the HR Agent system.
This file provides the structure that Google ADK framework expects.
"""

# Load environment variables from .env file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

from HR_root_agent import root_agent

# Create the structure that Google ADK expects: agent_module.agent.root_agent
class agent:
    root_agent = root_agent

# Make the agent class available at module level
__all__ = ['agent', 'root_agent']

