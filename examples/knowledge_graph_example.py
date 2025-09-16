#!/usr/bin/env python3
"""
Knowledge Graph Example for NenDB Python Driver

This example demonstrates real-world knowledge graph usage patterns:
- Loading knowledge from CSV/JSON data
- Querying relationships
- Building recommendation systems
- Entity resolution and disambiguation

Real-world use cases:
- Product recommendation systems
- Scientific literature analysis
- Social network analysis
- Knowledge base construction
"""

import sys
import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple

# Add the src directory to the path so we can import the driver
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nen_python_driver import NenDBClient, NenDBError


class KnowledgeGraphClient:
    """High-level wrapper for knowledge graph operations"""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.client = NenDBClient(server_url)
        
    def load_triples_from_csv(self, csv_path: str, 
                             subject_col: str = "subject",
                             predicate_col: str = "predicate", 
                             object_col: str = "object") -> Dict[str, Any]:
        """Load knowledge triples from CSV file"""
        print(f"📊 Loading knowledge triples from {csv_path}...")
        
        # Read CSV with pandas
        df = pd.read_csv(csv_path)
        print(f"   Found {len(df)} rows in CSV")
        
        # Convert to triples format
        triples = []
        for _, row in df.iterrows():
            if pd.notna(row[subject_col]) and pd.notna(row[predicate_col]) and pd.notna(row[object_col]):
                triples.append({
                    "subject": str(row[subject_col]).strip(),
                    "predicate": str(row[predicate_col]).strip(), 
                    "object": str(row[object_col]).strip()
                })
        
        print(f"   Converted to {len(triples)} valid triples")
        
        # Batch insert triples into NenDB
        return self.batch_insert_triples(triples)
    
    def load_triples_from_json(self, json_path: str) -> Dict[str, Any]:
        """Load knowledge triples from JSON file"""
        print(f"📋 Loading knowledge triples from {json_path}...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON formats
        if isinstance(data, list):
            triples = data
        elif 'triples' in data:
            triples = data['triples']
        else:
            raise ValueError("JSON must contain list of triples or 'triples' key")
        
        print(f"   Found {len(triples)} triples in JSON")
        return self.batch_insert_triples(triples)
    
    def batch_insert_triples(self, triples: List[Dict[str, str]]) -> Dict[str, Any]:
        """Efficiently insert knowledge triples in batches"""
        print(f"🔄 Inserting {len(triples)} triples into knowledge graph...")
        
        # Create entity mappings
        entities = set()
        relations = set()
        
        for triple in triples:
            entities.add(triple["subject"])
            entities.add(triple["object"])
            relations.add(triple["predicate"])
        
        print(f"   Unique entities: {len(entities)}")
        print(f"   Unique relations: {len(relations)}")
        
        # TODO: Implement batch API calls to NenDB
        # For now, simulate the process
        result = {
            "status": "success",
            "entities_created": len(entities),
            "relations_created": len(relations),
            "triples_inserted": len(triples),
            "processing_time_ms": 150  # Simulated
        }
        
        print(f"✅ Knowledge graph loaded: {result['entities_created']} entities, {result['triples_inserted']} relationships")
        return result
    
    def find_related_entities(self, entity: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """Find entities related to a given entity"""
        print(f"🔍 Finding entities related to '{entity}' (depth={max_depth})...")
        
        # TODO: Implement relationship traversal API
        # Simulate finding related entities
        related = [
            {"entity": "related_entity_1", "relationship": "knows", "distance": 1},
            {"entity": "related_entity_2", "relationship": "works_with", "distance": 1},
            {"entity": "related_entity_3", "relationship": "friend_of", "distance": 2}
        ]
        
        print(f"   Found {len(related)} related entities")
        return related
    
    def get_recommendations(self, entity: str, recommendation_type: str = "similar") -> List[Dict[str, Any]]:
        """Get recommendations based on knowledge graph relationships"""
        print(f"💡 Getting {recommendation_type} recommendations for '{entity}'...")
        
        # TODO: Implement recommendation algorithm
        # This would typically use graph algorithms like:
        # - Collaborative filtering through shared connections
        # - PageRank for entity importance
        # - Node2Vec for similarity embeddings
        
        recommendations = [
            {"entity": "recommended_item_1", "score": 0.85, "reason": "shared_connections"},
            {"entity": "recommended_item_2", "score": 0.72, "reason": "similar_attributes"},
            {"entity": "recommended_item_3", "score": 0.68, "reason": "collaborative_filtering"}
        ]
        
        print(f"   Generated {len(recommendations)} recommendations")
        return recommendations
    
    def analyze_graph_metrics(self) -> Dict[str, Any]:
        """Analyze knowledge graph structure and metrics"""
        print("📈 Analyzing knowledge graph metrics...")
        
        # TODO: Implement graph analysis APIs
        metrics = {
            "total_nodes": 15000,
            "total_edges": 45000,
            "avg_degree": 3.0,
            "clustering_coefficient": 0.25,
            "most_connected_entities": [
                {"entity": "Person:John_Smith", "connections": 245},
                {"entity": "Company:Tech_Corp", "connections": 189},
                {"entity": "Location:New_York", "connections": 156}
            ],
            "most_common_relations": [
                {"relation": "works_at", "count": 2500},
                {"relation": "located_in", "count": 1800},
                {"relation": "knows", "count": 1200}
            ]
        }
        
        print(f"   Graph contains {metrics['total_nodes']} nodes and {metrics['total_edges']} edges")
        print(f"   Average degree: {metrics['avg_degree']}")
        return metrics


def demo_product_recommendations():
    """Demo: Product recommendation system using knowledge graph"""
    print("\n🛒 Demo: E-commerce Product Recommendations")
    print("-" * 50)
    
    kg = KnowledgeGraphClient()
    
    # Simulate loading product catalog
    print("Loading product catalog knowledge graph...")
    result = kg.batch_insert_triples([
        {"subject": "User:alice", "predicate": "purchased", "object": "Product:laptop"},
        {"subject": "User:alice", "predicate": "viewed", "object": "Product:mouse"},
        {"subject": "User:bob", "predicate": "purchased", "object": "Product:laptop"},
        {"subject": "User:bob", "predicate": "purchased", "object": "Product:keyboard"},
        {"subject": "Product:laptop", "predicate": "category", "object": "Electronics"},
        {"subject": "Product:mouse", "predicate": "category", "object": "Electronics"},
        {"subject": "Product:keyboard", "predicate": "category", "object": "Electronics"}
    ])
    
    # Get recommendations for Alice
    recommendations = kg.get_recommendations("User:alice", "product")
    print(f"Recommendations for Alice: {recommendations}")


def demo_scientific_literature():
    """Demo: Scientific literature analysis"""
    print("\n📚 Demo: Scientific Literature Knowledge Graph")
    print("-" * 50)
    
    kg = KnowledgeGraphClient()
    
    # Simulate loading research papers
    print("Loading scientific literature knowledge graph...")
    literature_triples = [
        {"subject": "Paper:123", "predicate": "authored_by", "object": "Author:Dr_Smith"},
        {"subject": "Paper:123", "predicate": "cites", "object": "Paper:456"},
        {"subject": "Paper:123", "predicate": "topic", "object": "Machine_Learning"},
        {"subject": "Author:Dr_Smith", "predicate": "affiliated_with", "object": "University:MIT"},
        {"subject": "Paper:456", "predicate": "topic", "object": "Deep_Learning"}
    ]
    
    result = kg.batch_insert_triples(literature_triples)
    
    # Find related papers
    related = kg.find_related_entities("Paper:123", max_depth=2)
    print(f"Papers related to Paper:123: {related}")


def demo_social_network():
    """Demo: Social network analysis"""
    print("\n👥 Demo: Social Network Analysis")
    print("-" * 50)
    
    kg = KnowledgeGraphClient()
    
    # Simulate loading social connections
    social_triples = [
        {"subject": "Person:Alice", "predicate": "knows", "object": "Person:Bob"},
        {"subject": "Person:Bob", "predicate": "knows", "object": "Person:Charlie"},
        {"subject": "Person:Alice", "predicate": "works_at", "object": "Company:TechCorp"},
        {"subject": "Person:Bob", "predicate": "works_at", "object": "Company:TechCorp"},
        {"subject": "Person:Charlie", "predicate": "lives_in", "object": "City:SF"}
    ]
    
    result = kg.batch_insert_triples(social_triples)
    
    # Analyze social connections
    metrics = kg.analyze_graph_metrics()
    print(f"Social network metrics: {metrics}")


def main():
    """Main function demonstrating real-world knowledge graph usage"""
    print("🧠 NenDB Knowledge Graph - Real-World Usage Examples")
    print("=" * 60)
    
    try:
        # Run different demo scenarios
        demo_product_recommendations()
        demo_scientific_literature() 
        demo_social_network()
        
        print("\n🎉 Knowledge graph demos completed!")
        print("\nReal-world integration patterns:")
        print("• Load data from CSV/JSON/databases")
        print("• Use pandas for data preprocessing")
        print("• Implement recommendation algorithms")
        print("• Analyze graph structure and metrics")
        print("• Export results for ML pipelines")
        
    except NenDBError as e:
        print(f"❌ NenDB Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())