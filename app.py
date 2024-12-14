from pathlib import Path
import chainlit as cl
from src.llm import ask_order, messages


@cl.on_chat_start
async def main():

    # add startup message
    language = cl.user_session.get("languages").split(",")[0]

    root_path  = Path(__file__).parent
    
    translated_chainlit_md_path = root_path / f"chainlit_{language}.md"
    default_chainlit_md_path = root_path / "chainlit.md"
    if translated_chainlit_md_path.exists():
        message = translated_chainlit_md_path.read_text()
    else:
        message = default_chainlit_md_path.read_text()
    startup_message = cl.Message(content=message)
    await startup_message.send()


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    messages.append({"role": "user", "content": message.content})
    response = ask_order(messages)
    messages.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()