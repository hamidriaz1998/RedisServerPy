# RedisServerPy

A lightweight Redis server implementation written in Python that supports basic Redis commands and protocol.

## Features

- **Multi-threaded server** - Handles multiple concurrent client connections
- **Redis protocol compatible** - Supports RESP (Redis Serialization Protocol)
- **In-memory key-value storage** - Fast data access with Python dictionaries
- **TTL support** - Keys can expire after a specified time
- **Supported commands**:
  - `PING` - Test server connectivity
  - `ECHO` - Echo messages back to client
  - `SET` - Store key-value pairs with optional TTL
  - `GET` - Retrieve values by key

## Quick Start

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RedisServerPy
```

2. Run the server:
```bash
python src/main.py
```

The server will start on `localhost:6379` by default.

### Usage

Connect to the server using any Redis client or telnet:

```bash
# Using redis-cli
redis-cli

# Using telnet
telnet localhost 6379
```

### Example Commands

```redis
# Test connectivity
PING
# Returns: PONG

# Echo a message
ECHO "Hello World"
# Returns: Hello World

# Set a key-value pair
SET mykey "Hello Redis"
# Returns: OK

# Get a value
GET mykey
# Returns: Hello Redis

# Set with TTL (expires after 5000ms)
SET tempkey "temporary" PX 5000
# Returns: OK
```

## Project Structure

```
RedisServerPy/
├── src/
│   ├── main.py           # Entry point
│   ├── mainServer.py     # Main server implementation
│   ├── commandExec.py    # Command execution logic
│   ├── databaseHandler.py# In-memory database
│   ├── redisParser.py    # Redis protocol parser
│   └── argParser.py      # Command-line argument parser
└── README.md
```

## Architecture

- **Server** (`mainServer.py`): Handles client connections and threading
- **Command Executor** (`commandExec.py`): Processes Redis commands
- **Database Handler** (`databaseHandler.py`): Manages in-memory key-value storage
- **Redis Parser** (`redisParser.py`): Parses Redis protocol messages
- **Argument Parser** (`argParser.py`): Handles command-line arguments

## Configuration

The server accepts the following command-line arguments:

- `--dir`: Directory where RDB files are stored
- `--dbfilename`: Name of the RDB file

## Limitations

- Data is stored in memory only (no persistence)
- Limited command set compared to full Redis
- No clustering or replication support
- No authentication mechanism

## Development

To extend the server with new commands:

1. Add the command handler in `commandExec.py`
2. Update the `execute` method to route the new command
3. Ensure proper Redis protocol response format

## License

This project is open source and available under the MIT License.
