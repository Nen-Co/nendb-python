# NenDB Python Driver

A high-performance Python client for the NenDB graph database, built with Zig under the hood.

## Features

- **High Performance**: Built on top of NenDB's Zig-based HTTP server
- **Python Native**: Familiar Python API for graph operations
- **Graph Algorithms**: BFS, Dijkstra, PageRank, and more
- **Type Safety**: Full type hints and error handling
- **Async Support**: Both synchronous and asynchronous operations

## Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│   Python App    │ ──────────────► │  NenDB Server   │
│                 │                 │   (Zig + HTTP)  │
│  nen-python-    │ ◄────────────── │                 │
│     driver      │                 │                 │
└─────────────────┘                 └─────────────────┘
```

The Python driver communicates with NenDB's HTTP server, which is built in Zig for maximum performance. This gives you the best of both worlds: Python's ease of use with Zig's performance.

## Installation

```bash
pip install NenDB
```

## Quick Start

```python
from nen_python_driver import NenDBClient

# Connect to NenDB server
client = NenDBClient("http://localhost:8080")

# Check server health
health = client.health()
print(f"Server status: {health['status']}")

# Get graph statistics
stats = client.graph_stats()
print(f"Graph has {stats['nodes']} nodes and {stats['edges']} edges")

# Run BFS algorithm
result = client.bfs(start_node=0, max_depth=3)
print(f"BFS algorithm: {result['status']}")
```

## API Reference

### Client Initialization

```python
client = NenDBClient(
    base_url="http://localhost:8080",  # NenDB server URL
    timeout=30,                        # Request timeout in seconds
    retries=3                          # Number of retries on failure
)
```

### Health & Status

```python
# Check server health
health = client.health()

# Get graph statistics
stats = client.graph_stats()
```

### Graph Algorithms

```python
# Breadth-First Search
bfs_result = client.bfs(
    start_node=0,      # Starting node ID
    max_depth=3,       # Maximum search depth
    filters={}          # Optional node/edge filters
)

# Dijkstra Shortest Path
dijkstra_result = client.dijkstra(
    start_node=0,      # Starting node ID
    end_node=5,        # Target node ID
    weight_property="cost"  # Edge weight property
)

# PageRank
pagerank_result = client.pagerank(
    iterations=100,           # Number of iterations
    damping_factor=0.85,      # Damping factor
    tolerance=1e-6            # Convergence tolerance
)
```

### Error Handling

```python
from nen_python_driver import NenDBError

try:
    result = client.bfs(start_node=0, max_depth=3)
except NenDBError as e:
    print(f"Error: {e}")
    if e.details:
        print(f"Details: {e.details}")
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=nen_python_driver tests/
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -r requirements-docs.txt

# Build docs
sphinx-build -b html docs/ docs/_build/html
```

## Performance

The Python driver is designed for high performance:

- **Connection Pooling**: Reuses HTTP connections
- **Request Batching**: Batches multiple operations
- **Async Support**: Non-blocking operations
- **Error Recovery**: Automatic retries and fallbacks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: GitHub Issues
- **Documentation**: [docs.nen.co](https://docs.nen.co)
- **Community**: [Discord](https://discord.gg/nen)
