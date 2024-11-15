#!/usr/bin/env python3
import os
import sys
import argparse
from anthropic import Anthropic

def get_api_key():
    """Get API key from environment variable."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    return api_key

def ask_claude(prompt, model="claude-3-sonnet-20240229"):
    """Send prompt to Claude and return response."""
    client = Anthropic(api_key=get_api_key())
    
    try:
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Command-line interface for Claude')
    parser.add_argument('prompt', nargs='?', help='Direct prompt for Claude')
    args = parser.parse_args()

    # Check if receiving input from pipe
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        prompt = f"Here's the content to process:\n\n{stdin_content}\n\nPlease provide a response."
    # If no pipe and no arguments, show usage
    elif not args.prompt:
        parser.print_help()
        sys.exit(1)
    # Use provided prompt
    else:
        prompt = args.prompt

    response = ask_claude(prompt)
    print(response)
    
if __name__ == "__main__":
    main()
