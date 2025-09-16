#!/usr/bin/env python3
"""
NenDB Knowledge Graph - Python Integration Pattern

This example shows how developers would typically integrate NenDB 
with their Python applications for knowledge graph use cases.

Key Integration Patterns:
1. Data Loading from common formats (CSV, JSON, databases)
2. HTTP API communication with NenDB server
3. Knowledge graph analysis and recommendations
4. Integration with ML pipelines (pandas, sklearn, torch)
"""

import json
import csv
import requests
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Triple:
    """Knowledge graph triple: (subject, predicate, object)"""
    subject: str
    predicate: str
    object: str


class NenDBKnowledgeGraph:
    """Python client for NenDB knowledge graph operations"""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url.rstrip('/')
        self.session = requests.Session()
        
    def health_check(self) -> bool:
        """Check if NenDB server is running"""
        try:
            response = self.session.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def load_csv_knowledge(self, csv_path: str) -> Dict[str, Any]:
        """Load knowledge triples from CSV file"""
        print(f"📊 Loading knowledge from {csv_path}...")
        
        triples = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if all(k in row for k in ['subject', 'predicate', 'object']):
                    triples.append(Triple(
                        subject=row['subject'].strip(),
                        predicate=row['predicate'].strip(),
                        object=row['object'].strip()
                    ))
        
        print(f"   Parsed {len(triples)} triples from CSV")
        return self._batch_insert_triples(triples)
    
    def _batch_insert_triples(self, triples: List[Triple]) -> Dict[str, Any]:
        """Insert knowledge triples into NenDB via HTTP API"""
        print(f"🔄 Inserting {len(triples)} triples into NenDB...")
        
        # Group entities and relationships
        entities = set()
        relationships = {}
        
        for triple in triples:
            entities.add(triple.subject)
            entities.add(triple.object)
            
            if triple.predicate not in relationships:
                relationships[triple.predicate] = []
            relationships[triple.predicate].append((triple.subject, triple.object))
        
        print(f"   Unique entities: {len(entities)}")
        print(f"   Relationship types: {len(relationships)}")
        
        # In a real implementation, you would make HTTP calls to NenDB:
        # 
        # 1. Insert nodes:
        # for entity in entities:
        #     self.session.post(f"{self.server_url}/nodes", 
        #                      json={"id": hash(entity), "label": entity})
        #
        # 2. Insert edges:
        # for predicate, pairs in relationships.items():
        #     for subject, obj in pairs:
        #         self.session.post(f"{self.server_url}/edges",
        #                          json={"from": hash(subject), "to": hash(obj), "label": predicate})
        
        # Simulate successful insertion
        result = {
            "status": "success",
            "entities_inserted": len(entities),
            "relationships_inserted": sum(len(pairs) for pairs in relationships.values()),
            "relationship_types": list(relationships.keys()),
            "processing_time_ms": len(triples) * 0.1  # Simulate processing time
        }
        
        print(f"✅ Knowledge graph loaded successfully!")
        print(f"   Entities: {result['entities_inserted']}")
        print(f"   Relationships: {result['relationships_inserted']}")
        
        return result
    
    def find_similar_entities(self, entity: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find entities similar to the given entity"""
        print(f"🔍 Finding entities similar to '{entity}'...")
        
        # In a real implementation:
        # response = self.session.get(f"{self.server_url}/similarity/{entity}?limit={limit}")
        # return response.json()
        
        # Simulate similarity results
        similar = [
            {"entity": "Product:laptop_macbook_pro", "similarity": 0.85, "reason": "same_category"},
            {"entity": "Product:laptop_hp_spectre", "similarity": 0.78, "reason": "same_brand_tier"},
            {"entity": "Product:laptop_lenovo_thinkpad", "similarity": 0.72, "reason": "same_price_range"}
        ]
        
        print(f"   Found {len(similar)} similar entities")
        return similar
    
    def get_recommendations(self, user_entity: str, recommendation_type: str = "product") -> List[Dict[str, Any]]:
        """Get personalized recommendations using knowledge graph"""
        print(f"💡 Getting {recommendation_type} recommendations for '{user_entity}'...")
        
        # This would typically involve:
        # 1. Finding user's purchase/view history
        # 2. Analyzing similar users' behaviors  
        # 3. Using graph algorithms (collaborative filtering, PageRank)
        # 4. Ranking recommendations by relevance scores
        
        recommendations = [
            {
                "item": "Product:monitor_4k",
                "score": 0.92,
                "reasons": ["users_who_bought_laptop_also_bought", "same_category"],
                "confidence": 0.85
            },
            {
                "item": "Product:keyboard_mechanical", 
                "score": 0.87,
                "reasons": ["complementary_product", "high_rating"],
                "confidence": 0.78
            },
            {
                "item": "Product:mouse_gaming",
                "score": 0.73,
                "reasons": ["popular_combination", "same_price_tier"],
                "confidence": 0.65
            }
        ]
        
        print(f"   Generated {len(recommendations)} recommendations")
        return recommendations
    
    def analyze_user_behavior(self, user_entity: str) -> Dict[str, Any]:
        """Analyze user behavior patterns from knowledge graph"""
        print(f"📈 Analyzing behavior for '{user_entity}'...")
        
        # This would query the knowledge graph for:
        # - Purchase history
        # - Browse patterns  
        # - Category preferences
        # - Price sensitivity
        # - Brand loyalty
        
        analysis = {
            "user": user_entity,
            "total_purchases": 3,
            "favorite_categories": ["Electronics", "Technology"],
            "price_sensitivity": "medium",
            "brand_preferences": ["Dell", "Logitech"],
            "purchase_frequency": "monthly",
            "avg_order_value": 450.00,
            "predicted_next_purchase": {
                "category": "Electronics",
                "timeframe_days": 30,
                "confidence": 0.72
            }
        }
        
        print(f"   Purchase history: {analysis['total_purchases']} items")
        print(f"   Favorite categories: {analysis['favorite_categories']}")
        
        return analysis


def demo_ecommerce_recommendations():
    """Demo: E-commerce recommendation system"""
    print("\n🛒 Demo: E-commerce Product Recommendations")
    print("=" * 50)
    
    kg = NenDBKnowledgeGraph()
    
    # Load sample e-commerce data
    result = kg.load_csv_knowledge("sample_knowledge_data.csv")
    
    # Analyze user behavior
    user_analysis = kg.analyze_user_behavior("User:alice")
    
    # Get personalized recommendations
    recommendations = kg.get_recommendations("User:alice")
    
    print(f"\n🎯 Top recommendations for Alice:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec['item']} (score: {rec['score']:.2f})")
        print(f"      Reasons: {', '.join(rec['reasons'])}")


def demo_knowledge_discovery():
    """Demo: Knowledge discovery and entity relationships"""
    print("\n🔬 Demo: Knowledge Discovery")
    print("=" * 50)
    
    kg = NenDBKnowledgeGraph()
    
    # Find similar products
    similar = kg.find_similar_entities("Product:laptop_dell_xps")
    
    print(f"\n🔍 Products similar to Dell XPS laptop:")
    for item in similar:
        print(f"   • {item['entity']} (similarity: {item['similarity']:.2f})")
        print(f"     Reason: {item['reason']}")


def demo_integration_patterns():
    """Demo: Common integration patterns with Python ecosystem"""
    print("\n🐍 Demo: Python Ecosystem Integration")
    print("=" * 50)
    
    print("Real-world integration patterns:")
    print("\n1. 📊 Data Science Workflow:")
    print("   • Load data with pandas from CSV/database")
    print("   • Clean and preprocess in Python")
    print("   • Insert into NenDB knowledge graph")
    print("   • Run graph analytics for insights")
    print("   • Export results to ML models")
    
    print("\n2. 🤖 ML Pipeline Integration:")
    print("   • Use knowledge graph for feature engineering")
    print("   • Generate entity embeddings with Node2Vec")
    print("   • Train recommendation models with PyTorch")
    print("   • Deploy with FastAPI + NenDB backend")
    
    print("\n3. 🏢 Enterprise Applications:")
    print("   • Sync data from CRM/ERP systems")
    print("   • Build knowledge base from documents")
    print("   • Real-time recommendations via API")
    print("   • Analytics dashboard with Streamlit")


def main():
    """Main function demonstrating NenDB Python integration"""
    print("🧠 NenDB Knowledge Graph - Python Integration Examples")
    print("=" * 60)
    print("Demonstrates real-world usage patterns for Python developers")
    print()
    
    # Check if sample data exists
    try:
        with open("sample_knowledge_data.csv"):
            pass
    except FileNotFoundError:
        print("⚠️  Note: sample_knowledge_data.csv not found")
        print("   In a real application, you would:")
        print("   • Load data from your existing databases")
        print("   • Process CSV/JSON files from data pipelines") 
        print("   • Integrate with APIs and web scraping")
        print()
    
    # Run demos
    demo_ecommerce_recommendations()
    demo_knowledge_discovery()
    demo_integration_patterns()
    
    print(f"\n🎉 Python integration examples completed!")
    print(f"\nNext steps for developers:")
    print(f"• Install NenDB server: zig build && ./zig-out/bin/nendb serve")
    print(f"• Install Python deps: pip install -r requirements_knowledge_graph.txt")
    print(f"• Adapt this code to your data sources")
    print(f"• Build your knowledge-powered applications!")


if __name__ == "__main__":
    main()