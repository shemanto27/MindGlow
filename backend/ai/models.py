"""
MindGlow Models — Pydantic data models for memory and semantic search.
The backend stores and retrieves these structures; memory.py uses them for computation.
"""

from datetime import datetime
from pydantic import BaseModel


class StoredMessage(BaseModel):
    """A past conversation message stored by the backend with its embedding vector."""
    content: str
    role: str  # "user" or "assistant"
    embedding: list[float]
    timestamp: datetime


class SemanticSearchResult(BaseModel):
    """A semantically relevant message returned by memory.py's semantic_search()."""
    content: str
    role: str
    similarity: float
    timestamp: datetime
