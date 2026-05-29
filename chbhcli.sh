#!/usr/bin/env bash

# Ensures the script crashes rather than creates a bad environment
set -euo pipefail

# Sets up current working directory and script directory
SWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CWD="$PWD"
VENV_DIR="$CWD/.venv"

# Installs chbhcli so it's accessable from anywhere. 
cmd_install() {
    # Warning: Currently doesn't work
    if ! grep -q 'alias chbhcli' "$HOME/.bashrc"; then
	    echo "alias chbhcli=\"bash $SWD/chbhcli\"" >> "$HOME/.bashrc"
    fi
   echo "Installed! Run: source ~/.bashrc"
  echo "You can use the chbhcli from anywhere" 

}

# Creates a general purpose MEG environment using UV
cmd_meg_env() {
    (
	module purge
	module load bluebear
	module load bear-apps/2023a
	module load uv/0.6.5
	module load Python/3.11.3-GCCcore-12.3.0
	cd "$CWD"
	uv sync
    )
    echo "Environment set up"
    echo "Active using: source .venv/bin/activate"
}

# Manages bash inputs
case "${1:-}" in
    install) cmd_install ;;
    meg_env) cmd_meg_env ;;
    *) echo "Invalid command" ;;
esac
