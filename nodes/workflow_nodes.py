import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from typing import Dict
from models.state import GraphState
from tools.news import NewsTools
from agents.analysis_agent import AnalysisAgent
from tools.vector_store import VectorStoreManager
from langgraph.graph import END
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

load_dotenv()
today = datetime.now()
yesterday = today - timedelta(days=1)


class WorkflowNodes:
    @staticmethod
    def fetch_news(state: GraphState) -> GraphState:
        """Fetch relevant financial news."""
        try:
            news = NewsTools.search_news("latest financial news about Gold Apple stocks market")
            state.news_data = news
            state.current_stage = "analyze_news"
            return state
        except Exception as e:
            state.error = str(e)
            return state

    @staticmethod
    def analyze_news(state: GraphState) -> GraphState:
        """Analyze news using the agent."""
        print("started analyzing")
        agent = AnalysisAgent().create_agent()
        prompt = """You are an expert financial analysis agent specializing in real-time market analysis. Your task is to thoroughly analyze the provided news about financial markets, focusing on the most recent data. 

OBJECTIVE:
Analyze the provided news focusing on Gold and Apple Inc. Look for:
- Price movements
- Market sentiment
- Key events or announcements
- Trading volumes
- Market trends
- Expert opinions
- Future predictions

INSTRUCTIONS:
1. Carefully read and analyze the news provided in the input
2. Use the search tool to gather additional recent information if needed
3. Focus on data from the most recent trading day
4. Identify clear positive/negative signals
5. Determine market sentiment and confidence based on multiple data points

Return results in the following JSON format:
{{
    "type": "asset_class|security_name",  // Must be either 'asset_class' or 'security_name'
    "name": "asset or security name",     // Must be either 'Gold' or 'Apple Inc'
    "analysis": "positive|negative|neutral", // Based on recent price movements and sentiment
    "confidence": 0.9,  // Provide actual number between 0 and 1
    "reasoning": "Brief explanation of your analysis",  // NEW: Add reasoning
    "latest_data": {{   // NEW: Add key metrics
        "price": "current price if available",
        "change_percentage": "daily change if available",
        "trading_volume": "if available",
        "key_events": ["list", "of", "recent", "events"]
    }},
    "date_analyzed": "analysis date"  // NEW: Add date
}}

Available Assets for Analysis:
1. Gold (asset_class)
   - Track spot prices
   - Monitor global demand
   - Consider geopolitical impacts

2. Apple Inc (security_name)
   - Stock performance
   - Trading volumes
   - Company announcements
   - Market sentiment

IMPORTANT:
- Use the search tool extensively to gather very recent data
- Make multiple searches if needed to confirm trends
- Focus on news from the last 24 hours
- Cross-reference multiple sources
- Consider both technical and fundamental factors
- Provide high confidence ratings only when supported by multiple data points

Please analyze the NEWS provided in the input field and provide comprehensive analysis for both Gold and Apple Inc."""
        print(prompt,"PROMPT")
        result = agent.invoke({"input": state.news_data, "chat_history":prompt})
        analysis_results = json.loads(result['output'])
        state.analysis_results = analysis_results if isinstance(analysis_results, list) else [analysis_results]
        state.current_stage = "search_vectorstore"
        return state

    @staticmethod
    def search_vectorstore(state: GraphState) -> GraphState:
        print("started searching vector store")
        """Search vector store for relevant assets."""
        try:
            vector_store = VectorStoreManager()
            search_results = {}
            
            for result in state.analysis_results:
                query = f"{result['type']} {result['name']}"
                docs = vector_store.search(query)
                search_results[result['name']] = [doc.page_content for doc in docs]
            
            state.vector_search_results = search_results
            state.current_stage =  END
            return state
        except Exception as e:
            state.error = str(e)
            return state