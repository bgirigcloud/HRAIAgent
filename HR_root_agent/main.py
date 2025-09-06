import asyncio
from google.adk.runners import InMemoryRunner
from agent import root_agent
from google.genai.types import Content, Part
from google.adk.sessions.in_memory_session_service import InMemorySessionService

async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="HR_root_agent", user_id="user_123", session_id="session_123")
    runner = InMemoryRunner(agent=root_agent)
    runner._in_memory_session_service = session_service
    for event in runner.run(
        user_id="user_123",
        session_id="session_123",
        new_message=Content(parts=[Part(text="Hello")]),
    ):
        print(event)

if __name__ == "__main__":
    asyncio.run(main())