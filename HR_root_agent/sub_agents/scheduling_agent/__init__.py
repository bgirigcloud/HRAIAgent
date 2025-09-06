# Scheduling agent package
try:
    from .agent import scheduling_agent
    __all__ = ['scheduling_agent']
except ImportError:
    # Handle case where relative import fails
    __all__ = []
