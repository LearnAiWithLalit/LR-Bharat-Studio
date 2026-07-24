#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create required dirs if missing
mkdir -p "$SCRIPT_DIR/config" "$SCRIPT_DIR/logs"

cd "$SCRIPT_DIR"

echo "🚀 Starting OmniRoute Docker container..."
if docker compose up -d 2>/dev/null; then
    echo "✅ OmniRoute started."
else
    echo "Running with sudo..."
    sudo docker compose up -d
fi

echo ""
echo "🌐 Dashboard UI         : http://localhost:3000"
echo "🔌 OpenAI Proxy Endpoint: http://localhost:20128/v1"
echo ""
echo "Add your API keys at the dashboard, then run:"
echo "  python3 $PROJECT_DIR/../run.py"
