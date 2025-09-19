"""
Custom exceptions for the NenDB Python driver
"""

from typing import Optional, Dict, Any


class NenDBError(Exception):
    """Base exception for NenDB operations"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class NenDBConnectionError(NenDBError):
    """Raised when connection to NenDB server fails"""

    pass


class NenDBTimeoutError(NenDBError):
    """Raised when a request times out"""

    pass


class NenDBValidationError(NenDBError):
    """Raised when input validation fails"""

    pass


class NenDBAlgorithmError(NenDBError):
    """Raised when graph algorithm execution fails"""

    pass


class NenDBResponseError(NenDBError):
    """Raised when the server returns an error response"""

    pass
