#!/usr/bin/env python3
"""
Command-line interface for NenDB Python Driver
"""

import argparse
import json
import sys
from typing import Dict, Any

from .client import NenDBClient
from .exceptions import NenDBError


def print_json(data: Dict[str, Any], pretty: bool = True):
    """Print data as JSON"""
    if pretty:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))


def health_command(client: NenDBClient, args: argparse.Namespace):
    """Execute health check command"""
    try:
        result = client.health()
        print_json(result, args.pretty)
    except NenDBError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def stats_command(client: NenDBClient, args: argparse.Namespace):
    """Execute graph stats command"""
    try:
        result = client.graph_stats()
        print_json(result, args.pretty)
    except NenDBError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def bfs_command(client: NenDBClient, args: argparse.Namespace):
    """Execute BFS algorithm command"""
    try:
        data = {
            "start_node": args.start_node,
            "max_depth": args.max_depth
        }
        
        if args.filters:
            data["filters"] = json.loads(args.filters)
        
        result = client.bfs(**data)
        print_json(result, args.pretty)
    except NenDBError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def dijkstra_command(client: NenDBClient, args: argparse.Namespace):
    """Execute Dijkstra algorithm command"""
    try:
        result = client.dijkstra(
            start_node=args.start_node,
            end_node=args.end_node,
            weight_property=args.weight_property
        )
        print_json(result, args.pretty)
    except NenDBError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def pagerank_command(client: NenDBClient, args: argparse.Namespace):
    """Execute PageRank algorithm command"""
    try:
        result = client.pagerank(
            iterations=args.iterations,
            damping_factor=args.damping_factor,
            tolerance=args.tolerance
        )
        print_json(result, args.pretty)
    except NenDBError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="NenDB Python Driver CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nendb health
  nendb stats
  nendb bfs --start-node 0 --max-depth 3
  nendb dijkstra --start-node 0 --end-node 5
  nendb pagerank --iterations 100 --damping-factor 0.85
        """
    )
    
    # Global options
    parser.add_argument(
        "--server", "-s",
        default="http://localhost:8080",
        help="NenDB server URL (default: http://localhost:8080)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    parser.add_argument(
        "--pretty", "-p",
        action="store_true",
        help="Pretty-print JSON output"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Health command
    health_parser = subparsers.add_parser("health", help="Check server health")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get graph statistics")
    
    # BFS command
    bfs_parser = subparsers.add_parser("bfs", help="Execute BFS algorithm")
    bfs_parser.add_argument("--start-node", "-s", type=int, required=True, help="Starting node ID")
    bfs_parser.add_argument("--max-depth", "-d", type=int, default=3, help="Maximum search depth")
    bfs_parser.add_argument("--filters", "-f", help="JSON string of filters")
    
    # Dijkstra command
    dijkstra_parser = subparsers.add_parser("dijkstra", help="Execute Dijkstra algorithm")
    dijkstra_parser.add_argument("--start-node", "-s", type=int, required=True, help="Starting node ID")
    dijkstra_parser.add_argument("--end-node", "-e", type=int, required=True, help="Target node ID")
    dijkstra_parser.add_argument("--weight-property", "-w", default="weight", help="Edge weight property")
    
    # PageRank command
    pagerank_parser = subparsers.add_parser("pagerank", help="Execute PageRank algorithm")
    pagerank_parser.add_argument("--iterations", "-i", type=int, default=100, help="Maximum iterations")
    pagerank_parser.add_argument("--damping-factor", "-d", type=float, default=0.85, help="Damping factor")
    pagerank_parser.add_argument("--tolerance", "-t", type=float, default=1e-6, help="Convergence tolerance")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Create client
        client = NenDBClient(args.server, timeout=args.timeout)
        
        # Execute command
        if args.command == "health":
            health_command(client, args)
        elif args.command == "stats":
            stats_command(client, args)
        elif args.command == "bfs":
            bfs_command(client, args)
        elif args.command == "dijkstra":
            dijkstra_command(client, args)
        elif args.command == "pagerank":
            pagerank_command(client, args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
            
    except NenDBError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    finally:
        if 'client' in locals():
            client.close()


if __name__ == "__main__":
    main()
