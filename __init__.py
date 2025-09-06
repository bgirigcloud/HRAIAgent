# HR Agent package
# This makes the HR_agent directory a Python package

try:
    from HR_root_agent import root_agent, agent
    
    # Create the structure that Google ADK expects: agent_module.agent.root_agent
    __all__ = ['root_agent', 'agent', 'HR_root_agent']
except ImportError:
    __all__ = []
