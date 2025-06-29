# BrainBridge

A proof of concept 1:1 chat applciation with the Turing complete BrainFuck language with Python wrapper(s) for network connectivity & CLI.

## Architecture

Pure Brainfuck cannot handle TCP/IP networking, so I used a layered architecture where:

1. **Python** handles network I/O
2. **Brainfuck** processes all messages
3. **Clients** see a normal chat experience

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
python -m server.server --debug
```

## Brainfuck Programs

Available BF programs in `brainfuck/programs/`:

1. **echo.bf** `,[.,]` - Simple echo service (default)
2. **xor.bf** - XOR encryption with key 42
3. **simple_encrypt.bf** `,[+++++++++++++.,]` - ROT13-style encryption (adds 13)
4. **simple_decrypt.bf** `,[-------------.,]` - ROT13-style decryption (subtracts 13)

### Using Different Programs

```bash
# Run with specific program by name
python -m server.server --bf simple_encrypt
```

### Encryption Demo

When using `simple_encrypt`, the server showcases the encryption process:
- Sender sees: `[You]: Hello`
- Recipient sees: `[Sender]: [Uryy|] Hello` (encrypted text in gray brackets, then decrypted)

## Limitations

- Pure Brainfuck has no networking primitives
- No Unicode support (ASCII only)
- Single-byte I/O only

## Running Tests
pytest tests/