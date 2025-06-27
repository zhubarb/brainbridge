# BrainBridge 🧠

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start server
python -m brainbridge.server.server --bf brainfuck/programs/echo.bf

# Terminal 2: Connect client
python -m brainbridge.client.client

# Debug mode (shows BF memory state)
python -m brainbridge.server.server --debug
```

## Architecture

┌─────────────┐         ┌─────────────┐
│  Client A   │ ──TCP── │   Server    │
└─────────────┘         │ ┌─────────┐ │
                        │ │   BF    │ │
┌─────────────┐         │ │ ,[.,]   │ │
│  Client B   │ ──TCP── │ └─────────┘ │
└─────────────┘         └─────────────┘

## Brainfuck Programs

- echo.bf: Passes messages through unchanged
- xor.bf: XOR encryption with key 42 (stretch goal)

## Limitations

- Pure Brainfuck has no networking primitives
- No Unicode support (ASCII only)
- Single-byte I/O only

## Running Tests
pytest tests/