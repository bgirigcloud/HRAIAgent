# Job description agent package
try:
    from .agent import job_description_agent
    __all__ = ['job_description_agent']
except ImportError:
    # Handle case where relative import fails
    __all__ = []
