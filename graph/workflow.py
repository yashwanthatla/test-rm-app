import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from langgraph.graph import Graph, StateGraph
from models.state import GraphState
from nodes.workflow_nodes import WorkflowNodes
from dotenv import load_dotenv

load_dotenv()


class NewsAnalysisWorkflow:
    @staticmethod
    def create_graph() -> Graph:
        """Create and return the workflow graph."""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("fetch_news", WorkflowNodes.fetch_news)
        workflow.add_node("analyze_news", WorkflowNodes.analyze_news)
        workflow.add_node("search_vectorstore", WorkflowNodes.search_vectorstore)
        
        # Add edges
        workflow.add_edge("fetch_news", "analyze_news")
        workflow.add_edge("analyze_news", "search_vectorstore")
        
        # Set entry point
        workflow.set_entry_point("fetch_news")
        
        return workflow.compile()
