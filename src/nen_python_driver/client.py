"""
Main client implementation for connecting to NenDB
"""

import json
from typing import Dict, Optional, Any
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    NenDBError,
    NenDBConnectionError,
    NenDBTimeoutError,
    NenDBValidationError,
    NenDBResponseError,
)


class NenDBClient:
    """
    High-performance Python client for NenDB graph database

    This client communicates with NenDB's Zig-based HTTP server,
    providing Python-native access to graph algorithms and operations.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        timeout: int = 30,
        retries: int = 3,
        session: Optional[requests.Session] = None,
        skip_validation: bool = False,
    ):
        """
        Initialize the NenDB client

        Args:
            base_url: Base URL of the NenDB server
            timeout: Request timeout in seconds
            retries: Number of retries on failure
            session: Optional requests.Session for connection pooling
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries

        # Create or use provided session
        self.session = session or self._create_session()

        # Validate connection (only if not in test mode)
        if not skip_validation:
            try:
                self.health()
            except Exception as e:
                raise NenDBConnectionError(
                    f"Failed to connect to NenDB server at "
                    f"{self.base_url}: {e}"
                )

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic and connection pooling"""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1,
        )

        # Mount adapter with retry logic
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the NenDB server

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            NenDBError: On request failure
        """
        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout,
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise NenDBResponseError(
                    f"Invalid JSON response from server: {e}",
                    details={
                        "status_code": response.status_code,
                        "response_text": response.text,
                    },
                )

        except requests.exceptions.Timeout:
            raise NenDBTimeoutError(
                f"Request to {endpoint} timed out after {self.timeout} seconds"
            )
        except requests.exceptions.ConnectionError as e:
            raise NenDBConnectionError(f"Connection failed to {endpoint}: {e}")
        except requests.exceptions.HTTPError as e:
            # Try to extract error details from response
            try:
                error_data = response.json()
                error_msg = error_data.get("error", str(e))
                details = {
                    "status_code": response.status_code,
                    "response": error_data,
                }
            except Exception:
                error_msg = str(e)
                details = {"status_code": response.status_code}

            raise NenDBResponseError(
                f"HTTP error on {endpoint}: {error_msg}", details=details
            )
        except Exception as e:
            raise NenDBError(f"Unexpected error on {endpoint}: {e}")

    def health(self) -> Dict[str, Any]:
        """
        Check server health

        Returns:
            Health status information

        Raises:
            NenDBError: On connection failure
        """
        return self._make_request("GET", "/health")

    def graph_stats(self) -> Dict[str, Any]:
        """
        Get graph statistics

        Returns:
            Graph statistics including node count, edge count, and available
            algorithms

        Raises:
            NenDBError: On request failure
        """
        return self._make_request("GET", "/graph/stats")

    def bfs(
        self,
        start_node: int,
        max_depth: int = 3,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute Breadth-First Search algorithm

        Args:
            start_node: Starting node ID
            max_depth: Maximum search depth
            filters: Optional node/edge filters

        Returns:
            BFS algorithm result

        Raises:
            NenDBError: On algorithm failure
        """
        if not isinstance(start_node, int) or start_node < 0:
            raise NenDBValidationError(
                "start_node must be a non-negative integer"
            )
        if not isinstance(max_depth, int) or max_depth < 1:
            raise NenDBValidationError("max_depth must be a positive integer")

        data = {"start_node": start_node, "max_depth": max_depth}

        if filters:
            data["filters"] = filters

        return self._make_request("POST", "/graph/algorithms/bfs", data=data)

    def dijkstra(
        self,
        start_node: int,
        end_node: int,
        weight_property: str = "weight",
    ) -> Dict[str, Any]:
        """
        Execute Dijkstra's shortest path algorithm

        Args:
            start_node: Starting node ID
            end_node: Target node ID
            weight_property: Edge property to use as weight

        Returns:
            Dijkstra algorithm result

        Raises:
            NenDBError: On algorithm failure
        """
        if not isinstance(start_node, int) or start_node < 0:
            raise NenDBValidationError(
                "start_node must be a non-negative integer"
            )
        if not isinstance(end_node, int) or end_node < 0:
            raise NenDBValidationError(
                "end_node must be a non-negative integer"
            )
        if not isinstance(weight_property, str):
            raise NenDBValidationError("weight_property must be a string")

        data = {
            "start_node": start_node,
            "end_node": end_node,
            "weight_property": weight_property,
        }

        return self._make_request(
            "POST", "/graph/algorithms/dijkstra", data=data
        )

    def pagerank(
        self,
        iterations: int = 100,
        damping_factor: float = 0.85,
        tolerance: float = 1e-6,
    ) -> Dict[str, Any]:
        """
        Execute PageRank algorithm

        Args:
            iterations: Maximum number of iterations
            damping_factor: Damping factor (0.0 to 1.0)
            tolerance: Convergence tolerance

        Returns:
            PageRank algorithm result

        Raises:
            NenDBError: On algorithm failure
        """
        if not isinstance(iterations, int) or iterations < 1:
            raise NenDBValidationError("iterations must be a positive integer")
        if not isinstance(damping_factor, float) or not (
            0.0 <= damping_factor <= 1.0
        ):
            raise NenDBValidationError(
                "damping_factor must be between 0.0 and 1.0"
            )
        if not isinstance(tolerance, float) or tolerance <= 0.0:
            raise NenDBValidationError("tolerance must be a positive float")

        data = {
            "iterations": iterations,
            "damping_factor": damping_factor,
            "tolerance": tolerance,
        }

        return self._make_request(
            "POST", "/graph/algorithms/pagerank", data=data
        )

    def close(self):
        """Close the client session and free resources"""
        if self.session:
            self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
