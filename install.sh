#!/bin/bash

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
	echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
	echo -e "${RED}[!]${NC} $1"
}

# Check Python version
if ! command -v python3 &>/dev/null; then
	print_error "Python 3 is required but not installed."
	exit 1
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
cat >~/bin/ai <<EOF
#!/bin/bash
source "$(pwd)/.venv/bin/activate"
python "$(pwd)/main.py" "\$@"
deactivate
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
	else
		SHELL_RC="$HOME/.bashrc"
	fi

	echo 'export PATH="$HOME/bin:$PATH"' >>"$SHELL_RC"
	print_status "Added PATH to $SHELL_RC"
fi

print_status "Installation complete!"
print_status "Please run: source ~/.bashrc (or source ~/.zshrc for Zsh)"
print_status "Then set your API key: export ANTHROPIC_API_KEY='your-key-here'"
