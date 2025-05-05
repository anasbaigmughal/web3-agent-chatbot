import chainlit as cl
from agents import Runner
from ..config.settings import config
from ..components.blockchain_agents import triage_agent
from openai.types.responses import ResponseTextDeltaEvent

@cl.on_chat_start
async def handle_chat_start():
    """Initialize chat session."""
    cl.user_session.set("chat_history", [])
    await cl.Message(content="Welcome to Web3 Agent Chatbot!").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """Process incoming messages and maintain chat history."""
    try:
        chat_history = cl.user_session.get("chat_history")
        chat_history.append({"role": "user", "content": message.content})
        msg = cl.Message(content="")

        print(f"🟢 Processing user message: {message.content}")

        stream = Runner.run_streamed(triage_agent, input=chat_history, run_config=config)

        async for event in stream.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)
            elif event.type == "tool_call":
                print(f"🟢 Tool call detected: {event.data}")

        chat_history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", chat_history)
        await msg.update()
        print(f"🟢 Chat history: {chat_history}")
    except Exception as e:
        print(f"🔴 Error in handle_message: {str(e)}")
        msg.content = f"Error: {str(e)}"
        await msg.update()
