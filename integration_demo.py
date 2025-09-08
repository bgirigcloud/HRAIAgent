"""
HR Multi-Agent System Integration Demo

This script demonstrates how to use the restructured HR Multi-Agent system
with all the advanced capabilities.
"""

import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Import the root agent which coordinates all sub-agents
try:
    from HR_root_agent.agent import root_agent
    print("Successfully imported root agent")
    
    # List available sub-agents
    from HR_root_agent.agent import list_sub_agents
    available_agents = list_sub_agents()
    print("\nAvailable agents:")
    for agent_name, description in available_agents.items():
        print(f"- {agent_name}: {description}")
    
    # Demonstrate using the job description agent through the root agent
    print("\n--- Job Description Analysis ---")
    jd_text = """
    Senior Software Engineer
    
    About Us:
    CloudHero is a leading cloud solutions provider helping businesses transform through technology.
    
    Requirements:
    - 5+ years of experience in software development
    - Proficiency in Python, JavaScript, and cloud technologies
    - Experience with AWS, Docker, and Kubernetes
    - Strong problem-solving and communication skills
    
    Responsibilities:
    - Design and develop scalable applications
    - Lead technical projects and mentor junior developers
    - Collaborate with cross-functional teams
    """
    
    # Ask the root agent to analyze the job description
    response = root_agent.ask(f"Analyze this job description: {jd_text}")
    print(f"Root agent response: {response}\n")
    
    # Demonstrate using the neo4j agent if available
    try:
        from HR_root_agent.sub_agents.neo4j_agent import neo4j_agent
        print("\n--- Neo4j Graph Database Demo ---")
        print(f"Connecting to Neo4j: {neo4j_agent.connect()}")
        print("Example organizational hierarchy query would retrieve data here")
    except ImportError:
        print("Neo4j agent not available")
    
    # Demonstrate using the pgvector agent if available
    try:
        from HR_root_agent.sub_agents.pgvector_db_agent import pgvector_db_agent
        print("\n--- PGVector Database Demo ---")
        print(f"Connecting to PGVector: {pgvector_db_agent.connect()}")
        print("Example vector similarity search would retrieve data here")
    except ImportError:
        print("PGVector DB agent not available")
    
    # Demonstrate using the RAG agent if available
    try:
        from HR_root_agent.sub_agents.rag_agent import rag_agent
        print("\n--- RAG Demo ---")
        if rag_agent.model:
            embedding = rag_agent.generate_embedding("Example text for embedding generation")
            print(f"Generated embedding of length: {len(embedding)}")
        else:
            print("RAG agent model not loaded")
    except ImportError:
        print("RAG agent not available")
    
    # Demonstrate using the MCP server agent if available
    try:
        from HR_root_agent.sub_agents.mcp_server_agent import mcp_server_agent
        print("\n--- MCP Server Demo ---")
        app = mcp_server_agent.initialize_app()
        print(f"MCP Server initialized with host: {mcp_server_agent.host}, port: {mcp_server_agent.port}")
        print("Example MCP completion request would be processed here")
    except ImportError:
        print("MCP Server agent not available")
    
except ImportError as e:
    print(f"Error importing root agent: {e}")
    print("Using mock implementation instead...")
    
    # Use mock implementation for demonstration
    from demo_agents import get_hr_agents
    agents = get_hr_agents()
    
    print("\nAvailable mock agents:")
    for agent_name, agent in agents.items():
        print(f"- {agent_name}: {agent.name}")
    
    # Demonstrate using the root agent
    print("\n--- Mock Job Description Analysis ---")
    jd_text = """
    Senior Software Engineer
    
    About Us:
    CloudHero is a leading cloud solutions provider helping businesses transform through technology.
    
    Requirements:
    - 5+ years of experience in software development
    - Proficiency in Python, JavaScript, and cloud technologies
    - Experience with AWS, Docker, and Kubernetes
    - Strong problem-solving and communication skills
    """
    
    # Ask the mock root agent
    response = agents["root"].ask(f"Analyze this job description: {jd_text}")
    print(f"Mock root agent response: {response}")
    
    # Demonstrate other mock agents
    print("\n--- Mock Neo4j Demo ---")
    response = agents["neo4j"].ask("Show me the organizational hierarchy")
    print(f"Mock Neo4j agent response: {response}")
    
    print("\n--- Mock PGVector Demo ---")
    response = agents["pgvector_db"].ask("Find candidates matching the senior developer role")
    print(f"Mock PGVector agent response: {response}")
    
    print("\n--- Mock RAG Demo ---")
    response = agents["rag"].ask("What skills are needed for a DevOps role?")
    print(f"Mock RAG agent response: {response}")
    
    print("\n--- Mock MCP Server Demo ---")
    response = agents["mcp_server"].ask("Process this HR knowledge request")
    print(f"Mock MCP Server agent response: {response}")

print("\nDemo completed successfully!")
