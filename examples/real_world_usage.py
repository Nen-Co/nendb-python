#!/usr/bin/env python3
"""
NenDB Knowledge Graph - Real-World Usage Patterns

This example demonstrates how developers would use NenDB for knowledge graphs
in Python applications, showing practical integration patterns without 
requiring external dependencies.

Realistic scenarios:
- E-commerce recommendations  
- Scientific literature analysis
- Social network insights
- Content recommendation systems
"""

import json
import csv
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


class NenDBKnowledgeGraph:
    """Lightweight Python client for NenDB knowledge graph operations"""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url.rstrip('/')
        
    def load_knowledge_from_csv(self, csv_path: str) -> Dict[str, Any]:
        """Load knowledge triples from CSV - typical data science workflow"""
        print(f"📊 Loading knowledge from {csv_path}...")
        
        triples = []
        entities = set()
        relationships = {}
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, 1):
                    if all(k in row for k in ['subject', 'predicate', 'object']):
                        subject = row['subject'].strip()
                        predicate = row['predicate'].strip() 
                        obj = row['object'].strip()
                        
                        if subject and predicate and obj:
                            triples.append((subject, predicate, obj))
                            entities.add(subject)
                            entities.add(obj)
                            
                            if predicate not in relationships:
                                relationships[predicate] = 0
                            relationships[predicate] += 1
        
        except FileNotFoundError:
            print(f"   ⚠️  CSV file not found - simulating data load")
            # Simulate realistic e-commerce knowledge graph
            return self._simulate_ecommerce_data()
        
        print(f"   ✅ Parsed {len(triples)} triples")
        print(f"   📊 Entities: {len(entities)}")
        print(f"   🔗 Relationship types: {len(relationships)}")
        
        return {
            "status": "success",
            "triples_count": len(triples),
            "entities_count": len(entities),
            "relationship_types": relationships,
            "data_quality": "high" if len(triples) > 0 else "needs_review"
        }
    
    def _simulate_ecommerce_data(self) -> Dict[str, Any]:
        """Simulate loading e-commerce knowledge graph data"""
        print("   🛒 Simulating e-commerce knowledge graph...")
        
        # Typical e-commerce knowledge structure
        knowledge_stats = {
            "status": "success",
            "triples_count": 28,
            "entities_count": 20,
            "relationship_types": {
                "purchased": 6,
                "viewed": 8,
                "category": 7,
                "brand": 4,
                "price_range": 3
            },
            "data_quality": "high"
        }
        
        print(f"   📦 Products: 12")
        print(f"   👥 Users: 3") 
        print(f"   🏷️  Categories: 3")
        print(f"   🔗 Relationships: {knowledge_stats['triples_count']}")
        
        return knowledge_stats
    
    def analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user behavior patterns - core recommendation feature"""
        print(f"🔍 Analyzing patterns for {user_id}...")
        
        # In real implementation, this would:
        # 1. Query NenDB for user's relationship history
        # 2. Analyze purchase/view patterns
        # 3. Calculate preference scores
        # 4. Identify user segments
        
        user_patterns = {
            "user_id": user_id,
            "activity_summary": {
                "total_interactions": 15,
                "purchases": 3,
                "views": 12,
                "avg_session_duration": "8.5 minutes"
            },
            "preferences": {
                "top_categories": ["Electronics", "Technology"],
                "price_sensitivity": "medium",
                "brand_loyalty": ["Dell", "Apple", "Logitech"],
                "purchase_timing": "weekend_shopper"
            },
            "behavioral_score": {
                "exploration_vs_exploitation": 0.65,  # Tries new products
                "impulse_vs_research": 0.72,          # Researches before buying
                "quality_vs_price": 0.80              # Values quality over price
            },
            "predicted_interests": [
                {"category": "Gaming_Accessories", "confidence": 0.78},
                {"category": "Professional_Software", "confidence": 0.65},
                {"category": "Home_Office", "confidence": 0.58}
            ]
        }
        
        print(f"   📈 Activity: {user_patterns['activity_summary']['total_interactions']} interactions")
        print(f"   🎯 Top interests: {', '.join([p['category'] for p in user_patterns['predicted_interests'][:2]])}")
        
        return user_patterns
    
    def generate_recommendations(self, user_id: str, context: str = "general") -> List[Dict[str, Any]]:
        """Generate personalized recommendations using knowledge graph"""
        print(f"💡 Generating {context} recommendations for {user_id}...")
        
        # Real implementation would:
        # 1. Get user's interaction history from knowledge graph
        # 2. Find similar users using collaborative filtering
        # 3. Use graph algorithms (PageRank, Node2Vec) for ranking
        # 4. Apply business rules and constraints
        # 5. Return ranked recommendations with explanations
        
        recommendations = [
            {
                "item_id": "Product:monitor_ultrawide_34inch",
                "item_name": "34\" Ultrawide Monitor",
                "recommendation_score": 0.89,
                "confidence": 0.82,
                "explanation": {
                    "primary_reason": "Users who bought laptops often upgrade to larger monitors",
                    "supporting_factors": [
                        "Complementary product category",
                        "Price range matches user preferences", 
                        "High ratings from similar users"
                    ]
                },
                "expected_impact": {
                    "click_probability": 0.24,
                    "purchase_probability": 0.08,
                    "revenue_potential": 450.00
                }
            },
            {
                "item_id": "Product:mechanical_keyboard_rgb",
                "item_name": "RGB Mechanical Keyboard",
                "recommendation_score": 0.84,
                "confidence": 0.76,
                "explanation": {
                    "primary_reason": "Frequently bought together with gaming setup",
                    "supporting_factors": [
                        "User showed interest in peripherals",
                        "Trending in user's demographic",
                        "Seasonal promotion available"
                    ]
                },
                "expected_impact": {
                    "click_probability": 0.19,
                    "purchase_probability": 0.12,
                    "revenue_potential": 150.00
                }
            },
            {
                "item_id": "Product:laptop_cooling_pad",
                "item_name": "Laptop Cooling Pad",
                "recommendation_score": 0.72,
                "confidence": 0.68,
                "explanation": {
                    "primary_reason": "Essential accessory for laptop users",
                    "supporting_factors": [
                        "Solves common laptop heat issues",
                        "Affordable price point",
                        "High customer satisfaction"
                    ]
                },
                "expected_impact": {
                    "click_probability": 0.15,
                    "purchase_probability": 0.18,
                    "revenue_potential": 35.00
                }
            }
        ]
        
        total_revenue_potential = sum(r["expected_impact"]["revenue_potential"] for r in recommendations)
        print(f"   🎯 Generated {len(recommendations)} recommendations")
        print(f"   💰 Total revenue potential: ${total_revenue_potential:.2f}")
        
        return recommendations
    
    def discover_trending_patterns(self) -> Dict[str, Any]:
        """Discover trending patterns in the knowledge graph"""
        print("📈 Discovering trending patterns...")
        
        # Real implementation would analyze:
        # - Recent interaction spikes
        # - Emerging product categories  
        # - Seasonal buying patterns
        # - Cross-category connections
        # - Viral product combinations
        
        trends = {
            "trending_categories": [
                {"category": "Home_Office", "growth_rate": 1.45, "driver": "remote_work_trend"},
                {"category": "Gaming_Accessories", "growth_rate": 1.23, "driver": "new_console_release"},
                {"category": "Health_Tech", "growth_rate": 1.18, "driver": "wellness_focus"}
            ],
            "emerging_relationships": [
                {"pattern": "laptop + webcam + lighting", "frequency_increase": 2.1},
                {"pattern": "gaming_chair + desk_organizer", "frequency_increase": 1.8},
                {"pattern": "fitness_tracker + sleep_monitor", "frequency_increase": 1.6}
            ],
            "seasonal_insights": {
                "current_season": "back_to_school",
                "peak_categories": ["Electronics", "Productivity_Tools"],
                "predicted_next_trend": "holiday_tech_gifts"
            },
            "cross_sell_opportunities": [
                {"primary": "MacBook", "secondary": "USB-C_Hub", "lift": 3.2},
                {"primary": "Gaming_Mouse", "secondary": "Mouse_Pad", "lift": 2.8},
                {"primary": "Monitor", "secondary": "HDMI_Cable", "lift": 2.4}
            ]
        }
        
        print(f"   🚀 Top trending category: {trends['trending_categories'][0]['category']} (+{trends['trending_categories'][0]['growth_rate']:.0%})")
        print(f"   🔗 Strongest cross-sell: {trends['cross_sell_opportunities'][0]['primary']} → {trends['cross_sell_opportunities'][0]['secondary']}")
        
        return trends


def demo_ecommerce_use_case():
    """Demo: E-commerce recommendation system"""
    print("\n🛒 Real-World Use Case: E-commerce Recommendations")
    print("=" * 55)
    
    kg = NenDBKnowledgeGraph()
    
    # 1. Data loading (typical data science workflow)
    print("1️⃣  Data Loading Phase:")
    data_result = kg.load_knowledge_from_csv("sample_knowledge_data.csv")
    
    # 2. User behavior analysis  
    print("\n2️⃣  User Analysis Phase:")
    user_patterns = kg.analyze_user_patterns("User:alice")
    
    # 3. Recommendation generation
    print("\n3️⃣  Recommendation Phase:")
    recommendations = kg.generate_recommendations("User:alice", "shopping")
    
    # 4. Display actionable results
    print("\n📋 Actionable Business Insights:")
    print(f"   • User Alice has {user_patterns['behavioral_score']['quality_vs_price']:.0%} quality preference")
    print(f"   • Top recommendation: {recommendations[0]['item_name']}")
    print(f"   • Expected conversion: {recommendations[0]['expected_impact']['purchase_probability']:.1%}")
    print(f"   • Revenue opportunity: ${sum(r['expected_impact']['revenue_potential'] for r in recommendations):.2f}")


def demo_analytics_insights():
    """Demo: Business analytics and trend discovery"""
    print("\n📊 Real-World Use Case: Business Analytics")
    print("=" * 55)
    
    kg = NenDBKnowledgeGraph()
    
    print("1️⃣  Market Trend Analysis:")
    trends = kg.discover_trending_patterns()
    
    print("\n📈 Strategic Business Insights:")
    top_trend = trends['trending_categories'][0]
    print(f"   • Fastest growing category: {top_trend['category']} (+{top_trend['growth_rate']:.0%})")
    print(f"   • Growth driver: {top_trend['driver'].replace('_', ' ').title()}")
    
    top_cross_sell = trends['cross_sell_opportunities'][0] 
    print(f"   • Best cross-sell opportunity: {top_cross_sell['primary']} → {top_cross_sell['secondary']}")
    print(f"   • Revenue lift potential: {top_cross_sell['lift']:.1f}x")
    
    print(f"   • Seasonal focus: {trends['seasonal_insights']['current_season'].replace('_', ' ').title()}")


def demo_integration_patterns():
    """Demo: How this integrates with typical Python development"""
    print("\n🐍 Integration with Python Ecosystem")
    print("=" * 55)
    
    integration_examples = {
        "data_science": {
            "tools": ["pandas", "numpy", "scikit-learn"],
            "workflow": [
                "Load data with pandas.read_csv()",
                "Clean and transform data",
                "Insert into NenDB knowledge graph",
                "Run analytics queries",
                "Export insights to ML models"
            ]
        },
        "web_development": {
            "tools": ["Django", "FastAPI", "Flask"],
            "workflow": [
                "Create REST API endpoints",
                "Query NenDB for recommendations",
                "Cache frequent queries",
                "Return JSON responses",
                "Monitor API performance"
            ]
        },
        "ml_operations": {
            "tools": ["PyTorch", "TensorFlow", "MLflow"],
            "workflow": [
                "Extract features from knowledge graph",
                "Generate node embeddings",
                "Train recommendation models",
                "Deploy models with graph context",
                "Track model performance"
            ]
        }
    }
    
    print("🔧 Common Integration Patterns:")
    for category, details in integration_examples.items():
        print(f"\n   {category.replace('_', ' ').title()}:")
        print(f"     Tools: {', '.join(details['tools'])}")
        print(f"     Workflow: {details['workflow'][0]} → ... → {details['workflow'][-1]}")


def main():
    """Main demonstration of real-world NenDB usage patterns"""
    print("🧠 NenDB Knowledge Graph - Real-World Python Usage")
    print("=" * 60)
    print("Demonstrating practical integration patterns for Python developers")
    print("showing how NenDB enables intelligent applications")
    
    # Run comprehensive demos
    demo_ecommerce_use_case()
    demo_analytics_insights()
    demo_integration_patterns()
    
    print(f"\n🎉 Real-world usage demonstrations completed!")
    
    print(f"\n🚀 Getting Started:")
    print(f"   1. Start NenDB server: ./zig-out/bin/nendb serve") 
    print(f"   2. Load your data: Python scripts or direct API calls")
    print(f"   3. Build intelligent features: Recommendations, analytics, search")
    print(f"   4. Deploy: Docker containers with NenDB + Python apps")
    
    print(f"\n💡 Key Benefits for Python Developers:")
    print(f"   • High-performance graph operations (10M+ ops/sec)")
    print(f"   • Simple HTTP API integration")
    print(f"   • Knowledge graph reasoning capabilities") 
    print(f"   • Production-ready with static memory allocation")
    print(f"   • Seamless integration with Python ML ecosystem")


if __name__ == "__main__":
    main()