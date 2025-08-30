#!/usr/bin/env python3
"""
Tests for NenDB Python Driver
"""

import unittest
import json
import requests
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path so we can import the driver
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nen_python_driver import NenDBClient, NenDBError


class TestNenDBClient(unittest.TestCase):
    """Test cases for the NenDB Python client"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = NenDBClient("http://localhost:8080", skip_validation=True)
        self.mock_response = Mock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {"status": "success"}
    
    def test_client_initialization(self):
        """Test client initialization with different configurations"""
        # Test default initialization
        client = NenDBClient(skip_validation=True)
        self.assertEqual(client.base_url, "http://localhost:8080")
        self.assertEqual(client.timeout, 30)
        
        # Test custom initialization
        client = NenDBClient("http://example.com:9000", timeout=60, skip_validation=True)
        self.assertEqual(client.base_url, "http://example.com:9000")
        self.assertEqual(client.timeout, 60)
    
    def test_health_check(self):
        """Test health check endpoint"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "healthy", "service": "nendb"}
            mock_request.return_value = mock_response
            
            result = self.client.health()
            self.assertEqual(result["status"], "healthy")
            self.assertEqual(result["service"], "nendb")
    
    def test_graph_stats(self):
        """Test graph statistics endpoint"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "nodes": 100,
                "edges": 250,
                "algorithms": ["bfs", "dijkstra", "pagerank"],
                "status": "operational"
            }
            mock_request.return_value = mock_response
            
            result = self.client.graph_stats()
            self.assertEqual(result["nodes"], 100)
            self.assertEqual(result["edges"], 250)
            self.assertIn("bfs", result["algorithms"])
    
    def test_bfs_algorithm(self):
        """Test BFS algorithm endpoint"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "algorithm": "bfs",
                "status": "queued",
                "message": "BFS algorithm queued for execution"
            }
            mock_request.return_value = mock_response
            
            result = self.client.bfs(start_node=0, max_depth=3)
            self.assertEqual(result["algorithm"], "bfs")
            self.assertEqual(result["status"], "queued")
    
    def test_dijkstra_algorithm(self):
        """Test Dijkstra algorithm endpoint"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "algorithm": "dijkstra",
                "status": "queued",
                "message": "Dijkstra algorithm queued for execution"
            }
            mock_request.return_value = mock_response
            
            result = self.client.dijkstra(start_node=0, end_node=5)
            self.assertEqual(result["algorithm"], "dijkstra")
            self.assertEqual(result["status"], "queued")
    
    def test_pagerank_algorithm(self):
        """Test PageRank algorithm endpoint"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "algorithm": "pagerank",
                "status": "queued",
                "message": "PageRank algorithm queued for execution"
            }
            mock_request.return_value = mock_response
            
            result = self.client.pagerank(iterations=100, damping_factor=0.85)
            self.assertEqual(result["algorithm"], "pagerank")
            self.assertEqual(result["status"], "queued")
    
    def test_error_handling(self):
        """Test error handling for failed requests"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
            mock_request.return_value = mock_response
            
            with self.assertRaises(NenDBError):
                self.client.health()
    
    def test_connection_timeout(self):
        """Test connection timeout handling"""
        with patch('requests.Session.request', side_effect=requests.exceptions.Timeout("Connection timeout")):
            with self.assertRaises(NenDBError):
                self.client.health()
    
    def test_invalid_json_response(self):
        """Test handling of invalid JSON responses"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_request.return_value = mock_response
            
            with self.assertRaises(NenDBError):
                self.client.health()
    
    def test_validation_errors(self):
        """Test input validation"""
        # Test invalid start_node
        with self.assertRaises(NenDBError):
            self.client.bfs(start_node=-1, max_depth=3)
        
        # Test invalid max_depth
        with self.assertRaises(NenDBError):
            self.client.bfs(start_node=0, max_depth=0)
        
        # Test invalid damping_factor
        with self.assertRaises(NenDBError):
            self.client.pagerank(damping_factor=1.5)


class TestNenDBError(unittest.TestCase):
    """Test cases for custom error handling"""
    
    def test_error_creation(self):
        """Test NenDBError creation and message"""
        error = NenDBError("Test error message")
        self.assertEqual(str(error), "Test error message")
    
    def test_error_with_details(self):
        """Test NenDBError with additional details"""
        error = NenDBError("Connection failed", details={"status_code": 500})
        self.assertIn("Connection failed", str(error))
        self.assertEqual(error.details["status_code"], 500)


if __name__ == "__main__":
    unittest.main()
