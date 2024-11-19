#!/bin/bash

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
	echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
	echo -e "${RED}[!]${NC} $1"
}

print_info() {
	echo -e "${BLUE}[i]${NC} $1"
}

# Check if script is being run with sudo
if [ "$EUID" -eq 0 ]; then
	print_error "Please do not run this script with sudo. It should be run as your regular user."
	exit 1
fi

# Check Python version
print_info "Checking Python version..."
if ! command -v python3 &>/dev/null; then
	print_error "Python 3 is required but not installed."
	exit 1
fi

# Clean up any existing virtual environment
if [ -d ".venv" ]; then
	print_info "Removing existing virtual environment..."
	rm -rf .venv
fi

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv .venv || {
	print_error "Failed to create virtual environment"
	exit 1
}

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate || {
	print_error "Failed to activate virtual environment"
	exit 1
}

# Upgrade pip
print_status "Upgrading pip..."
python -m pip install --upgrade pip || {
	print_error "Failed to upgrade pip"
	exit 1
}

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt || {
	print_error "Failed to install requirements"
	exit 1
}

# Create bin directory if it doesn't exist
mkdir -p ~/bin

# Create the wrapper script
print_status "Creating wrapper script..."
cat >~/bin/ai <<'EOF'
#!/bin/bash
# Get the directory where the script is installed
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/personal/terminalai"

# Activate virtual environment and run the script
source "${SCRIPT_DIR}/.venv/bin/activate"
python "${SCRIPT_DIR}/main.py" "$@"
status=$?
deactivate
exit $status
EOF

# Make the wrapper script executable
chmod +x ~/bin/ai || {
	print_error "Failed to make wrapper script executable"
	exit 1
}

# Add ~/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
	print_status "Adding ~/bin to PATH..."

	# Detect shell
	if [ -n "$ZSH_VERSION" ]; then
		SHELL_RC="$HOME/.zshrc"
	elif [ -n "$BASH_VERSION" ]; then
		SHELL_RC="$HOME/.bashrc"
	else
		print_error "Unsupported shell. Please manually add ~/bin to your PATH"
		exit 1
	fi

	echo 'export PATH="$HOME/bin:$PATH"' >>"$SHELL_RC"
	print_status "Added PATH to $SHELL_RC"
fi

print_status "Installation complete!"
print_info "Next steps:"
echo -e "1. Run: ${GREEN}source ~/.bashrc${NC} (or ${GREEN}source ~/.zshrc${NC} for Zsh)"
echo -e "2. Set your API key: ${GREEN}export ANTHROPIC_API_KEY='your-key-here'${NC}"
echo -e "3. Add the API key to your shell config to make it permanent"
echo
print_info "Example usage:"
echo -e "- Ask a question: ${GREEN}ai \"what is the capital of France?\"${NC}"
echo -e "- Execute a command: ${GREEN}ai -c \"show disk usage\"${NC}"
echo -e "- Process a file: ${GREEN}cat file.txt | ai \"summarize this\"${NC}"
