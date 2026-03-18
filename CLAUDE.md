# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nanobot is an ultra-lightweight personal AI assistant framework (~16k Python lines) supporting 16+ chat platforms, multiple LLM providers, and MCP integration. Entry point: `nanobot` CLI → `nanobot/cli/commands.py`.

**Package manager & Python runtime: [`uv`](https://github.com/astral-sh/uv).** Always use `uv sync` to install dependencies and `uv run` to execute Python commands. Do not use `pip`, `python`, or `python3` directly.

## Common Commands

```bash
# Install dependencies
uv sync

# Run the CLI
uv run nanobot

# Run tests
uv run pytest tests/

# Run a single test
uv run pytest tests/test_commands.py::test_function_name -v

# Lint
uv run ruff check nanobot/

# Format
uv run ruff format nanobot/

# Build WhatsApp bridge (Node.js)
cd bridge && npm install && npm run build
```

## Architecture

The agent follows an **event-driven, async-first** design:

```
Channel (Slack/Discord/Telegram/etc.)
  → Message Bus (nanobot/bus/)
    → Agent Loop (nanobot/agent/loop.py)
      → Context Builder (context.py)
      → LLM Provider (nanobot/providers/)
      → Tool Execution (nanobot/agent/tools/)
      → Session Manager (nanobot/session/)
```

**Key modules:**
- `nanobot/agent/loop.py` — Core processing engine: context building, LLM calls, tool execution
- `nanobot/agent/context.py` — Builds prompt context from session history and memory
- `nanobot/agent/memory.py` — Token-aware memory consolidation
- `nanobot/bus/` — Async message bus routing between channels and agent
- `nanobot/channels/` — Platform adapters (Slack, Discord, Telegram, Feishu, DingTalk, WeChat, QQ, Email, Matrix, WhatsApp, Mochat); each extends `channels/base.py`
- `nanobot/providers/` — LLM abstraction; `litellm_provider.py` handles most models; all extend `providers/base.py`
- `nanobot/agent/tools/` — Tool registry and implementations (shell, web, filesystem, MCP, cron, spawn)
- `nanobot/config/schema.py` — Pydantic models for all configuration
- `nanobot/skills/` — Extensible built-in skills (memory, weather, GitHub, etc.)
- `nanobot/cli/onboard_wizard.py` — Interactive setup wizard

## Branching Strategy

- `main` — stable releases
- `nightly` — experimental features; stable work is cherry-picked to `main`

## Testing

Tests use `pytest-asyncio` with `asyncio_mode = "auto"`. Test files in `tests/` cover channels, providers, config, and features individually. The `case/` directory contains integration test cases.

## Configuration

Config lives in Pydantic schemas (`nanobot/config/schema.py`). Templates are in `nanobot/templates/`. The wizard (`onboard_wizard.py`) generates config files interactively.

## Code Style

- Line length: 100 chars (ruff)
- Target: Python 3.11+
- Async-first: use `async/await` throughout; avoid blocking calls
- Pydantic for all data models and config validation
