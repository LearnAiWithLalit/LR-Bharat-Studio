#!/usr/bin/env bash
# =============================================================
# setup.sh — LR-Bharat-Studio One-Click Setup
# Installs all dependencies and starts required services.
# Designed to work on Ubuntu 22.04+ / AMD ROCm / NVIDIA CUDA.
# =============================================================
set -e

STUDIO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║         LR-Bharat-Studio — Setup Script             ║"
echo "║  AI Audio/Video Story Generation Pipeline           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── 1. System Python deps ──────────────────────────────────
echo -e "${YELLOW}[1/6] Installing Python dependencies...${NC}"
pip install --quiet \
    torch torchaudio \
    soundfile \
    scipy numpy \
    pyyaml \
    chatterbox-tts 2>/dev/null || \
pip install --quiet \
    torch torchaudio --index-url https://download.pytorch.org/whl/rocm6.2 && \
pip install --quiet soundfile scipy numpy pyyaml
echo -e "${GREEN}✅ Python dependencies installed${NC}"

# ── 2. OmniRoute (LLM proxy — free multi-model API router) ─
echo -e "${YELLOW}[2/6] Setting up OmniRoute LLM Router...${NC}"
if docker ps 2>/dev/null | grep -q omniroute; then
    echo -e "${GREEN}✅ OmniRoute already running on http://localhost:20128${NC}"
else
    if command -v docker &>/dev/null; then
        cd "$STUDIO_DIR/tools/omniroute"
        bash start.sh
        cd "$STUDIO_DIR"
        echo -e "${GREEN}✅ OmniRoute started on http://localhost:20128${NC}"
    else
        echo -e "${YELLOW}⚠️  Docker not found. OmniRoute skipped (FreeBuff will be used as fallback).${NC}"
    fi
fi

# ── 3. FreeBuff (100% free LLM — no API key needed) ────────
echo -e "${YELLOW}[3/6] Setting up FreeBuff (free LLM fallback)...${NC}"
if command -v freebuff &>/dev/null; then
    echo -e "${GREEN}✅ FreeBuff already installed: $(freebuff --version 2>/dev/null || echo 'installed')${NC}"
else
    if command -v npm &>/dev/null; then
        npm install -g freebuff --quiet
        echo -e "${GREEN}✅ FreeBuff installed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  npm not found. Attempting with bundled node binary...${NC}"
        NODE_BIN="$STUDIO_DIR/tools/freebuff/node"
        if [ -f "$NODE_BIN" ]; then
            "$NODE_BIN" "$(which npm 2>/dev/null || echo npm)" install -g freebuff --quiet 2>/dev/null \
                && echo -e "${GREEN}✅ FreeBuff installed via bundled node${NC}" \
                || echo -e "${YELLOW}⚠️  FreeBuff install failed. LLM will use OmniRoute only.${NC}"
        else
            echo -e "${YELLOW}⚠️  FreeBuff skipped. Install manually: npm install -g freebuff${NC}"
        fi
    fi
fi

# ── 4. Config setup ─────────────────────────────────────────
echo -e "${YELLOW}[4/6] Setting up configuration...${NC}"
if [ ! -f "$STUDIO_DIR/config/config.yaml" ]; then
    cp "$STUDIO_DIR/config/config.yaml.example" "$STUDIO_DIR/config/config.yaml"
fi
echo -e "${GREEN}✅ Config ready at config/config.yaml${NC}"

# ── 5. Output directories ───────────────────────────────────
echo -e "${YELLOW}[5/6] Creating output directories...${NC}"
mkdir -p "$STUDIO_DIR/output"/{audio,images,video,qa_reports,plans}
echo -e "${GREEN}✅ Output directories ready${NC}"

# ── 6. Quick health check ───────────────────────────────────
echo -e "${YELLOW}[6/6] Running health check...${NC}"
python3 "$STUDIO_DIR/brain/content_analyzer.py" > /dev/null 2>&1 \
    && echo -e "${GREEN}✅ Content Analyzer OK${NC}" \
    || echo -e "${YELLOW}⚠️  Content Analyzer check failed - check Python deps${NC}"

python3 "$STUDIO_DIR/brain/llm_router.py" > /dev/null 2>&1 \
    && echo -e "${GREEN}✅ LLM Router OK${NC}" \
    || echo -e "${YELLOW}⚠️  LLM Router check failed - ensure OmniRoute or FreeBuff is running${NC}"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗"
echo "║           Setup Complete! 🎉                         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "  Run the pipeline:"
echo "    python3 agents/agent7_master_orchestrator.py"
echo ""
echo "  Or with a custom prompt:"
echo "    python3 run.py --prompt 'Create a Hindi kids story about a magical forest'"
echo ""
echo "  OmniRoute Dashboard: http://localhost:3000"
echo "  FreeBuff (free LLM): freebuff"
echo ""
