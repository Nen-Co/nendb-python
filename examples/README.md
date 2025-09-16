# NenDB Knowledge Graph Examples

This directory contains practical examples showing how to use NenDB for knowledge graph applications in Python.

## 🎯 Real-World Use Cases

### 1. E-commerce Recommendations (`real_world_usage.py`)
- **Product recommendations** based on user behavior
- **Cross-selling opportunities** using graph relationships  
- **User behavior analysis** and preference modeling
- **Business analytics** and trend discovery

### 2. Knowledge Graph Data Loading
- **CSV data processing** for knowledge triples
- **Entity relationship mapping** from structured data
- **Batch data insertion** patterns
- **Data quality validation** workflows

### 3. Python Ecosystem Integration
- **pandas/numpy** for data preprocessing
- **scikit-learn/PyTorch** for ML model integration
- **Django/FastAPI** for web API development
- **Docker deployment** patterns

## 📊 Sample Data

`sample_knowledge_data.csv` contains example e-commerce knowledge triples:
```csv
subject,predicate,object
User:alice,purchased,Product:laptop_dell_xps
Product:laptop_dell_xps,category,Electronics
User:bob,viewed,Product:monitor_4k
```

## 🚀 Quick Start

### 1. Start NenDB Server
```bash
cd ../nen-db
zig build
./zig-out/bin/nendb serve
```

### 2. Install Python Dependencies
```bash
pip install -r requirements_knowledge_graph.txt
```

### 3. Run Examples
```bash
# Real-world usage patterns
python3 real_world_usage.py

# Knowledge graph operations (requires nen_python_driver)
python3 knowledge_graph_example.py

# Basic API usage
python3 basic_usage.py
```

## 🔧 Integration Patterns

### Data Science Workflow
```python
import pandas as pd
from nen_db_client import NenDBKnowledgeGraph

# Load data
df = pd.read_csv("your_data.csv")

# Initialize knowledge graph
kg = NenDBKnowledgeGraph()

# Insert knowledge triples
result = kg.load_csv_knowledge("your_data.csv")

# Generate recommendations
recommendations = kg.get_recommendations("User:123")
```

### Web API Integration
```python
from fastapi import FastAPI
from nen_db_client import NenDBKnowledgeGraph

app = FastAPI()
kg = NenDBKnowledgeGraph()

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    return kg.generate_recommendations(user_id)
```

### ML Pipeline Integration  
```python
import torch
from nen_db_client import NenDBKnowledgeGraph

# Extract graph features
kg = NenDBKnowledgeGraph()
user_features = kg.analyze_user_patterns("User:123")

# Use in ML model
model = torch.load("recommendation_model.pt")
predictions = model(user_features)
```

## 📈 Performance Characteristics

Based on our comprehensive API tests:
- **7.6M lookups/second** for entity queries
- **2.3M nodes/second** insertion rate  
- **100% hit rate** for knowledge graph queries
- **10K+ entities** with sub-millisecond response times

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│   Python App    │ ──────────────► │  NenDB Server   │
│                 │                 │   (Zig + HTTP)  │
│  Data Science   │ ◄────────────── │                 │
│  ML Pipeline    │                 │  Knowledge      │
│  Web API        │                 │  Graph Engine   │
└─────────────────┘                 └─────────────────┘
```

## 💡 Next Steps

1. **Adapt examples** to your specific data sources
2. **Extend the API client** with your domain-specific operations
3. **Build intelligent features** using knowledge graph insights
4. **Deploy in production** with Docker + NenDB server
5. **Monitor performance** and optimize for your workload

## 📚 Additional Resources

- [NenDB Core Documentation](../nen-db/README.md)
- [Python Driver API Reference](../nendb-python/README.md)
- [Knowledge Graph Best Practices](https://github.com/Nen-Co/knowledge-graph-guide)
- [Production Deployment Guide](https://github.com/Nen-Co/nen-deployment)