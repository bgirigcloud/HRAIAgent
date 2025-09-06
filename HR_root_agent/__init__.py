# HR Root Agent package
try:
    from .agent import root_agent
    
    # Create the structure that Google ADK expects: agent_module.agent.root_agent
    class agent:
        root_agent = root_agent
    
    __all__ = ['root_agent', 'agent']
except ImportError:
    # Handle case where relative import fails
    __all__ = []
