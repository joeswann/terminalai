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
    prompt = f"""As an expert in shell commands, convert this natural language request into the most appropriate shell command or sequence of commands. Consider:

1. Use common unix/linux commands and standard tools
2. Prefer safer options when available (e.g., 'rm -i' instead of just 'rm')
3. Use clear formatting for better readability
4. Handle edge cases and errors appropriately
5. Use proper quoting for file paths and variables

Request: {natural_language}

Respond with ONLY the command(s), no explanations or additional text. Examples:
- "list all files recursively" → ls -R
- "show disk usage" → df -h
- "remove all pdf files" → rm -i *.pdf
- "find large files" → find . -type f -size +100M -exec ls -lh {{}};
- "show system memory" → free -h

For multiple commands, use && to ensure each step completes successfully before proceeding."""

    command = ask_claude(prompt).strip()
    return command

def execute_command(command):
    """Execute the shell command and return output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Command failed with error:\n{result.stderr}")
            sys.exit(result.returncode)
        return result.stdout
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        sys.exit(1)

def process_pipe_input(content):
    """Process input received through pipe."""
    prompt = f"""As a helpful AI assistant, I'll analyze or process the following content. If it appears to be:
- Code: I'll explain, improve, or debug it
- Log file: I'll identify patterns, errors, or issues
- Text: I'll summarize or analyze it
- Data: I'll provide insights or statistics
- Commands: I'll explain their purpose and usage

Content to process:

{content}

Please provide a clear and concise response."""
    return ask_claude(prompt)

def main():
    parser = argparse.ArgumentParser(
        description='Command-line interface for Claude AI',
        epilog='Examples:\n'
               '  ai "explain how DNS works"\n'
               '  ai -c "show memory usage"\n'
               '  cat error.log | ai "find issues"\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('prompt', nargs='?', help='Question or request for Claude')
    parser.add_argument('-c', '--command', action='store_true', 
                      help='Convert natural language to shell command and execute it')
    args = parser.parse_args()

    # Check if receiving input from pipe
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        response = process_pipe_input(stdin_content)
        print(response)
        sys.exit(0)
    # If no pipe and no arguments, show usage
    elif not args.prompt:
        parser.print_help()
        sys.exit(1)
    # Handle command conversion and execution
    elif args.command:
        command = convert_to_command(args.prompt)
        print(f"Executing: {command}")
        output = execute_command(command)
        print(output)
        sys.exit(0)
    # Use provided prompt
    else:
        response = ask_claude(args.prompt)
        print(response)
    
if __name__ == "__main__":
    main()
