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

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make the script executable:

```bash
chmod +x ai
```

4. Add to your PATH by either:

   Moving to system bin:

   ```bash
   sudo mv ai /usr/local/bin/
   ```

   OR

   Creating a personal bin directory:

   ```bash
   mkdir -p ~/bin
   mv ai ~/bin/
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc for Zsh
   source ~/.bashrc  # or source ~/.zshrc for Zsh
   ```

5. Set up your API key:

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Add this to your `.bashrc` or `.zshrc` to make it permanent.

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

## Error Handling

The script will:

- Check for the presence of the API key
- Provide clear error messages if the API call fails
- Exit with appropriate status codes

## Limitations

- Maximum response length is set to 1000 tokens
- Requires active internet connection
- API usage is subject to Anthropic's rate limits and pricing

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License - See LICENSE file for details.
