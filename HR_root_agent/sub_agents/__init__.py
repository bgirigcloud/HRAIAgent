# Sub-agents package for HR management system
try:
    from .job_description.agent import job_description_agent
    from .email_send_agent.agent import email_send_agent
    from .interview_transcript_agent.agent import interview_transcript_agent
    from .resume_analyzer.agent import resume_analyzer_agent
    from .scheduling_agent.agent import scheduling_agent
    
    __all__ = [
        'job_description_agent',
        'email_send_agent', 
        'interview_transcript_agent',
        'resume_analyzer_agent',
        'scheduling_agent'
    ]
except ImportError:
    # Handle case where relative imports fail
    __all__ = []
