#!/usr/bin/env python3
"""
Basic usage example for NenDB Python Driver

This example demonstrates how to connect to the NenDB server
and execute various graph algorithms.
"""

import sys
import os

# Add the src directory to the path so we can import the driver
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nen_python_driver import NenDBClient, NenDBError


def main():
    """Main example function"""
    print("🚀 NenDB Python Driver - Basic Usage Example")
    print("=" * 50)
    
    try:
        # Initialize the client
        print("📡 Connecting to NenDB server...")
        client = NenDBClient("http://localhost:8080")
        print("✅ Connected successfully!")
        
        # Check server health
        print("\n🏥 Checking server health...")
        health = client.health()
        print(f"   Status: {health['status']}")
        print(f"   Service: {health['service']}")
        print(f"   Version: {health['version']}")
        
        # Get graph statistics
        print("\n📊 Getting graph statistics...")
        stats = client.graph_stats()
        print(f"   Nodes: {stats['nodes']}")
        print(f"   Edges: {stats['edges']}")
        print(f"   Status: {stats['status']}")
        print(f"   Available algorithms: {', '.join(stats['algorithms'])}")
        
        # Execute BFS algorithm
        print("\n🔍 Executing BFS algorithm...")
        bfs_result = client.bfs(start_node=0, max_depth=3)
        print(f"   Algorithm: {bfs_result['algorithm']}")
        print(f"   Status: {bfs_result['status']}")
        print(f"   Message: {bfs_result['message']}")
        
        # Execute Dijkstra algorithm
        print("\n🛣️  Executing Dijkstra algorithm...")
        dijkstra_result = client.dijkstra(start_node=0, end_node=5)
        print(f"   Algorithm: {dijkstra_result['algorithm']}")
        print(f"   Status: {dijkstra_result['status']}")
        print(f"   Message: {dijkstra_result['message']}")
        
        # Execute PageRank algorithm
        print("\n📈 Executing PageRank algorithm...")
        pagerank_result = client.pagerank(iterations=100, damping_factor=0.85)
        print(f"   Algorithm: {pagerank_result['algorithm']}")
        print(f"   Status: {pagerank_result['status']}")
        print(f"   Message: {pagerank_result['message']}")
        
        print("\n🎉 All operations completed successfully!")
        
    except NenDBError as e:
        print(f"❌ NenDB Error: {e}")
        if hasattr(e, 'details') and e.details:
            print(f"   Details: {e.details}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Clean up
        if 'client' in locals():
            client.close()


if __name__ == "__main__":
    main()
