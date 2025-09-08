"""
MCP Server Agent for HR AI Assistant.

This agent provides Model Context Protocol server capabilities for the HR system.
"""

import os
from typing import Dict, List, Any, Optional, Union
import json
import asyncio
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager

class MCPRequest(BaseModel):
    """Model for MCP request structure."""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    """Model for MCP response structure."""
    response: str
    metadata: Optional[Dict[str, Any]] = None

class MCPServerAgent:
    """Agent for managing Model Context Protocol server operations."""
    
    def __init__(self, name: str = "MCP Server Assistant"):
        self.name = name
        self.app = None
        self.host = os.getenv("MCP_HOST", "0.0.0.0")
        self.port = int(os.getenv("MCP_PORT", "8000"))
        self.tools = {}
        
    def register_tool(self, name: str, tool_func, description: str):
        """Register a tool with the MCP server."""
        self.tools[name] = {
            "func": tool_func,
            "description": description
        }
        
    def initialize_app(self):
        """Initialize the FastAPI application."""
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup logic
            print("Starting MCP Server...")
            yield
            # Shutdown logic
            print("Shutting down MCP Server...")
            
        app = FastAPI(lifespan=lifespan)
        
        @app.post("/api/v1/completions")
        async def handle_completion(request: MCPRequest):
            """Handle MCP completion requests."""
            try:
                # Process the request
                response = self.process_completion(request.prompt, request.context, request.options)
                return MCPResponse(response=response)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                
        @app.post("/api/v1/tools/{tool_name}")
        async def handle_tool_call(tool_name: str, request: Request):
            """Handle MCP tool calls."""
            if tool_name not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
                
            try:
                body = await request.json()
                tool_func = self.tools[tool_name]["func"]
                result = tool_func(**body)
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                
        @app.get("/api/v1/tools")
        async def list_tools():
            """List available tools."""
            return {
                name: {"description": info["description"]} 
                for name, info in self.tools.items()
            }
                
        self.app = app
        return app
        
    def process_completion(self, prompt: str, context: Optional[Dict] = None, options: Optional[Dict] = None) -> str:
        """Process a completion request."""
        # In a real implementation, this would call an LLM
        # This is a placeholder implementation
        return f"MCP Server processed: {prompt}"
        
    def start_server(self):
        """Start the MCP server."""
        if not self.app:
            self.initialize_app()
            
        import uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port)
        
    async def start_server_async(self):
        """Start the MCP server asynchronously."""
        if not self.app:
            self.initialize_app()
            
        import uvicorn
        config = uvicorn.Config(self.app, host=self.host, port=self.port)
        server = uvicorn.Server(config)
        await server.serve()
        
    # Example HR-specific tools
    def hr_knowledge_tool(self, query: str) -> Dict:
        """Tool for retrieving HR knowledge."""
        # This would connect to a knowledge base in a real implementation
        hr_knowledge = {
            "policies": {
                "pto": "Employees receive 20 days of PTO per year...",
                "remote_work": "Remote work is available 2 days per week..."
            },
            "procedures": {
                "onboarding": "New employees must complete onboarding within 2 weeks...",
                "offboarding": "Departing employees must return all equipment..."
            }
        }
        
        # Simple keyword matching for demo
        result = {}
        if "pto" in query.lower() or "time off" in query.lower():
            result["pto"] = hr_knowledge["policies"]["pto"]
        if "remote" in query.lower() or "wfh" in query.lower():
            result["remote_work"] = hr_knowledge["policies"]["remote_work"]
        if "onboarding" in query.lower() or "new employee" in query.lower():
            result["onboarding"] = hr_knowledge["procedures"]["onboarding"]
        if "offboarding" in query.lower() or "leaving" in query.lower():
            result["offboarding"] = hr_knowledge["procedures"]["offboarding"]
            
        return result or {"message": "No relevant HR knowledge found for the query"}

# Create an instance of the MCP Server Agent
mcp_server_agent = MCPServerAgent()

# Register HR tools
mcp_server_agent.register_tool(
    "hr_knowledge", 
    mcp_server_agent.hr_knowledge_tool,
    "Retrieve information from the HR knowledge base"
)
