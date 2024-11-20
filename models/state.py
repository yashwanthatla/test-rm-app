from typing import Dict, List
from langchain_core.pydantic_v1 import BaseModel, Field

class GraphState(BaseModel):
    """State for the news analysis graph."""
    news_data: str = Field(default="")
    analysis_results: List[Dict] = Field(default_factory=list)
    vector_search_results: List[Dict] = Field(default_factory=list)
    current_stage: str = Field(default="fetch_news")
    error: str = Field(default="")