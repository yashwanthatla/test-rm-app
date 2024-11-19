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
from data.sample_data import news_query,asset_with_subtypes,SAMPLE_ASSET_DATA,analyze_news_prompt

load_dotenv()
today = datetime.now()
yesterday = today - timedelta(days=1)


class WorkflowNodes:
    @staticmethod
    def fetch_news(state: GraphState) -> GraphState:
        """Fetch relevant financial news."""
        try:
            news = NewsTools.search_news(news_query)
            print('NEWS',news)
            state.current_stage = "analyze_news"
            state.news_data = news
            return state
        except Exception as e:
            state.error = str(e)
            return state

    @staticmethod
    def analyze_news(state: GraphState) -> GraphState:
        """Analyze news using the agent."""
        print("started analyzing")
        agent = AnalysisAgent().create_agent()
        result = agent.invoke({"input": analyze_news_prompt, "chat_history":state.news_data})
        json_str = result['output']
        json_str = json_str.replace('```', '')
        json_str = json_str.strip()
        print('JSON STRING',json_str)
        analysis_results = json.loads(json_str)
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
                search_results[result['name']] = [json.loads(doc.page_content) for doc in docs]
                search_results['analysis'] = result['analysis']
                search_results['reasoning'] = result['reasoning']
                search_results['key_events'] = result['key_events']
                search_results['date_analyzed'] = result['date_analyzed']
            state.vector_search_results = search_results
            state.current_stage =  END
            return state
        except Exception as e:
            state.error = str(e)
            return state