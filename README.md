# Claude CLI

A command-line interface for interacting with Claude, Anthropic's AI assistant. Ask questions, process files, and pipe command outputs directly to Claude from your terminal.

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

# Analyze logs
tail -n 50 /var/log/system.log | ai "find any error patterns"

# Explain commands
man grep | ai "explain grep's most useful options"

# Summarize documents
cat meeting_notes.txt | ai "create a bullet-point summary"
```

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

## Technical Details

- Uses Python virtual environment for isolated dependencies
- Installed in `~/bin` with automatic PATH configuration
- Dependencies managed through `requirements.txt`
- Maximum response length: 1000 tokens
- Uses Claude 3.5 Sonnet model

## Error Handling

The script will:

- Check for the presence of the API key
- Provide clear error messages if the API call fails
- Exit with appropriate status codes

## Limitations

- Maximum response length is set to 1000 tokens
- Requires active internet connection
- API usage is subject to Anthropic's rate limits and pricing

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

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License - See LICENSE file for details.
