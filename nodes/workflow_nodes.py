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
from langchain_openai import ChatOpenAI
from config.settings import Settings

load_dotenv()
today = datetime.now()
yesterday = today - timedelta(days=1)


class WorkflowNodes:
    @staticmethod
    def fetch_news(state: GraphState) -> GraphState:
        """Fetch relevant financial news."""
        try:
            news = NewsTools.search_news(news_query)
            print("NEWS", news)
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
        result = agent.invoke(
            {"input": analyze_news_prompt, "chat_history": state.news_data}
        )
        json_str = result["output"]
        json_str = json_str.replace("```", "")
        json_str = json_str.strip()
        print("JSON STRING", json_str)
        analysis_results = json.loads(json_str)
        state.analysis_results = (
            analysis_results
            if isinstance(analysis_results, list)
            else [analysis_results]
        )
        state.current_stage = "search_vectorstore"
        return state

    @staticmethod
    def search_vectorstore(state: GraphState) -> GraphState:
        print("started searching vector store")
        """Search vector store for relevant assets."""
        try:
            vector_store = VectorStoreManager()
            search_results = []
            
            for result in state.analysis_results:
                query = {"name":result['name'],"type":result['type']}
                docs = vector_store.search(query)
                search_result = {}
                search_result["searched_name"] = result['name']
                search_result["vector_search_results"] = [json.loads(doc.page_content) for doc in docs]
                search_result['analysis'] = result['analysis']
                search_result['reasoning'] = result['reasoning']
                search_result['key_events'] = result['key_events']
                search_result['date_analyzed'] = result['date_analyzed']
                search_results.append(search_result)
            state.vector_search_results = search_results
            state.current_stage =  'refine_result'
            return state
        except Exception as e:
            state.error = str(e)
            return state

    @staticmethod
    def refine_result(state: GraphState) -> GraphState:
        """Refine the results from the vector store using LLM."""
        print("filtering vector store")
        
        print("filtering vector store")
        llm = ChatOpenAI(**Settings.get_model_kwargs())

        # # Convert the complex nested structure to a clean, deduplicated format
        # def process_asset_classes(asset_dict):
        #     processed_results = []
        #     seen = set()

        #     print("asset dict", asset_dict)
        #     # Process each asset class category
        #     for category, items in asset_dict.items():
        #         if category in [
        #             "analysis",
        #             "reasoning",
        #             "key_events",
        #             "date_analyzed",
        #         ]:
        #             continue

        #         for item in items:
        #             # Create a unique key based on name and description
        #             key = (item["name"], item["description"])

        #             # Avoid duplicates
        #             if key not in seen:
        #                 processed_item = {
        #                     "name": item["name"],
        #                     "type": item["type"],
        #                     "description": item["description"],
        #                     "category": category,
        #                 }
        #                 processed_results.append(processed_item)
        #                 seen.add(key)

        #     return processed_results

        # # Process the vector search results
        # processed_vector_results = process_asset_classes(
        #     state.vector_search_results
        # )

        print("vector_search_results2", state.vector_search_results)
        refinement_prompt = f"""
        You are a financial analysis assistant. Refine the following processed vector store results:

        Processed Results:
        {json.dumps(state.vector_search_results, indent=2)}

        Task:
        - Review and consolidate the processed results
        - Remove any remaining duplicates
        - Enhance descriptions if they are too generic
        - Add analysis sentiment and confidence for each asset class
        - Ensure JSON follows this exact schema:
        [
            {{
                "name": "asset or security name",
                "type": "asset_class|asset_sub_class",
                "description": "detailed description of the asset",
                "category": "parent category (e.g., Equities, Gold, Fixed Income)",
                "analysis": "positive|negative|neutral",
                "confidence": "float between 0 and 1",
                "reasoning": "short explanation about the analysis"
            }},
            ...
        ]

        Provide a concise, precise, and non-redundant output. Ensure the JSON is valid and follows the schema exactly.
        """

        # Get refined results from LLM
        refined_results = llm.predict(refinement_prompt)
        print("Refined results", refined_results)
        # Parse and validate the results
        parsed_results = json.loads(refined_results)

        print("parsed_results", parsed_results)
        if not isinstance(parsed_results, list):
            raise ValueError("Refined results are not a valid list.")

        # Update the state with refined results
        state.vector_search_results = parsed_results
        state.current_stage = END
        return state