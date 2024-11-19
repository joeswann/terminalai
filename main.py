#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from anthropic import Anthropic

def get_api_key():
    """Get API key from environment variable."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    return api_key

def ask_claude(prompt, model="claude-3-5-sonnet-20241022"):
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

def convert_to_command(natural_language):
    """Convert natural language to shell command using Claude."""
    prompt = f"""Convert this natural language request into a shell command (just return the command itself, no explanation):
    
Request: {natural_language}

Respond with just the command, nothing else. For example:
- "list all files recursively" -> "ls -R"
- "show disk usage" -> "df -h"
"""
    command = ask_claude(prompt).strip()
    return command

def execute_command(command):
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout if result.stdout else result.stderr
    except subprocess.SubprocessError as e:
        print(f"Error executing command: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Command-line interface for Claude')
    parser.add_argument('prompt', nargs='?', help='Direct prompt for Claude')
    parser.add_argument('-c', '--command', action='store_true', 
                      help='Convert natural language to shell command and execute it')
    args = parser.parse_args()

    # Check if receiving input from pipe
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        prompt = f"Here's the content to process:\n\n{stdin_content}\n\nPlease provide a response."
    # If no pipe and no arguments, show usage
    elif not args.prompt:
        parser.print_help()
        sys.exit(1)
    # Handle command conversion and execution
    elif args.command:
        command = convert_to_command(args.prompt)
        print(f"Executing: {command}")
        output = execute_command(command)
        print("\nOutput:")
        print(output)
        return
    # Use provided prompt
    else:
        prompt = args.prompt

    response = ask_claude(prompt)
    print(response)
    
if __name__ == "__main__":
    main()
