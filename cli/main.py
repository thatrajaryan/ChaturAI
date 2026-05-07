import os
import asyncio
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path so we can import app
project_root = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_root))

from app.chat.chat import ChatService
from app.chat.openrouter import OpenRouterModel

async def run_research(prompt: str):
    """Run the research loop from the CLI."""
    # Load environment variables
    load_dotenv(project_root / ".env")
    
    assistant_file = project_root / "assistant.md"
    
    # Initialize Provider and Service
    try:
        model = OpenRouterModel()
        chat_impl = ChatService(provider=model, project_root=str(project_root), assistant_file=str(assistant_file))
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure OPEN_ROUTER_API_KEY and OPEN_ROUTER_MODEL are set in your .env file.")
        return

    session_id = "cli_session"
    
    print(f"\n--- Researching: {prompt} ---\n")
    
    try:
        async for chunk in chat_impl.send_message_stream(prompt, session_id):
            print(chunk, end="", flush=True)
        print("\n\n--- Research Completed ---\n")
    except Exception as e:
        print(f"\n\nAn error occurred during research: {e}")

def main():
    parser = argparse.ArgumentParser(description="ChaturAI CLI Researcher")
    parser.add_argument("prompt", help="The topic you want to research")
    
    args = parser.parse_args()
    
    if not args.prompt:
        parser.print_help()
        return

    try:
        asyncio.run(run_research(args.prompt))
    except KeyboardInterrupt:
        print("\nResearch interrupted by user.")

if __name__ == "__main__":
    main()
