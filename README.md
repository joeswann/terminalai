# Claude CLI

A command-line interface for interacting with Claude, Anthropic's AI assistant. Ask questions, process files, pipe command outputs directly to Claude, and execute natural language commands from your terminal.

## Prerequisites

- Python 3.7 or higher
- An Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation

1. Clone or download this repository:

```bash
git clone <repository-url>
cd claude-cli
```

2. Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

3. Source your shell configuration:

```bash
source ~/.bashrc  # or source ~/.zshrc for Zsh
```

4. Set up your API key:

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Add this to your `.bashrc` or `.zshrc` to make it permanent.

The installation script will:

- Create a virtual environment
- Install all dependencies
- Set up the CLI command in your PATH
- Configure your shell environment

## Usage

### Direct Questions

Ask Claude questions directly:

```bash
ai "what is the capital of France?"
ai "how do I list all Python files in a directory?"
```

### Natural Language Command Execution

Execute terminal commands using natural language:

```bash
ai -c "list all files recursively in this folder"
ai -c "show disk usage for all drives"
ai -c "find all python files modified in the last week"
ai -c "create a new directory called projects"
```

The `-c` or `--command` flag tells Claude to:

1. Convert your natural language request into a shell command
2. Show you the command it's about to execute
3. Run the command and display its output

### Process Files

Process file contents:

```bash
cat document.txt | ai summarize
cat code.py | ai "explain this code"
```

### Command Output Processing

Process the output of other commands:

```bash
ls -la | ai "explain these files"
ps aux | ai "which processes are using the most CPU?"
```

## Examples

```bash
# Get coding help
ai "write a python function to calculate fibonacci numbers"

# Execute system commands in natural language
ai -c "compress all jpg files in current directory"
ai -c "show memory usage"
ai -c "find large files over 1GB"

# Analyze logs
tail -n 50 /var/log/system.log | ai "find any error patterns"

# Explain commands
man grep | ai "explain grep's most useful options"

# Summarize documents
cat meeting_notes.txt | ai "create a bullet-point summary"
```

## Command Execution Safety

When using the `-c/--command` flag:

- The tool will always show you the command it plans to execute before running it
- Review the command to ensure it matches your intentions
- Be cautious with destructive operations (delete, remove, etc.)
- The tool executes commands with your current user permissions

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

## Technical Details

- Uses Python virtual environment for isolated dependencies
- Installed in `~/bin` with automatic PATH configuration
- Dependencies managed through `requirements.txt`
- Maximum response length: 1000 tokens
- Uses Claude 3.5 Sonnet model
- Natural language command conversion using Claude
- Safe command execution with subprocess module

## Error Handling

The script will:

- Check for the presence of the API key
- Provide clear error messages if the API call fails
- Show command execution errors if they occur
- Exit with appropriate status codes

## Limitations

- Maximum response length is set to 1000 tokens
- Requires active internet connection
- API usage is subject to Anthropic's rate limits and pricing
- Command execution is limited to your user permissions
- Complex multi-step commands may need to be broken down

## Project Structure

```
claude-cli/
├── README.md
├── requirements.txt
├── install.sh
├── main.py
└── .venv/          # Created during installation
```

## Troubleshooting

If you encounter any issues:

1. Ensure Python 3.7+ is installed: `python3 --version`
2. Verify the API key is set: `echo $ANTHROPIC_API_KEY`
3. Check that `~/bin` is in your PATH: `echo $PATH`
4. Try reinstalling: `./install.sh`
5. For command execution issues, try running the command directly in terminal

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License - See LICENSE file for details.
