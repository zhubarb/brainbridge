# BrainBridge 🧠

A proof of concept 1:1 chat applciation with Turing complete BrainFuck language with Python wrapper(s) for network connectivity.
Pure Brainfuck cannot handle TCP/IP networking, so I used a layered architecture where:

1. **Python** handles network I/O
2. **Brainfuck** processes all messages
3. **Clients** see a normal chat experience

## Architecture

```
┌─────────────┐         ┌─────────────┐
│  Client A   │ ──TCP── │   Server    │
└─────────────┘         │ ┌─────────┐ │
                        │ │   BF    │ │
┌─────────────┐         │ │ ,[.,]   │ │
│  Client B   │ ──TCP── │ └─────────┘ │
└─────────────┘         └─────────────┘
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start server
python -m server.server

# Terminal 2: Connect client 1
python -m client.client

# Terminal 3: Connect client 2
python -m client.client

# Debug mode (shows BF memory state)
python -m brainbridge.server.server --debug
```

## Brainfuck Programs

- echo.bf: Passes messages through unchanged
- xor.bf: XOR encryption with key 42

## Limitations

- Pure Brainfuck has no networking primitives
- No Unicode support (ASCII only)
- Single-byte I/O only

## Running Tests
pytest tests/