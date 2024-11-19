import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor, Tool
from tools.news import NewsTools
from config.settings import Settings
from dotenv import load_dotenv
from langchain import hub

load_dotenv()

class AnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(**Settings.get_model_kwargs())
        self.tools = [Tool(
            name="Google Searching tool",
            func=NewsTools.search_news,
            description="Useful to search regarding the stock news for assets and instruments"
        )]
        self.prompt = hub.pull("hwchase17/react-chat")
    
    def _create_prompt_template(self):
        return """You are a financial analysis agent. Analyze news and categorize them according to asset classes 
and securities. Return results in the following JSON format:

{{
    "type": "asset_class|security_name",
    "name": "asset or security name",
    "analysis": "positive|negative|neutral",
    "confidence": "float between 0 and 1"
}}

Available Asset Classes and Securities:
- Gold (asset_class)
- US Equities (asset_class)
- Apple Inc (security_name)

Use the search tool to gather more information if needed."""
    
    def create_agent(self):
        """Create and return the analysis agent."""
        prompt = create_react_agent(
            self.llm,
            self.tools,
            self.prompt
        )
        return AgentExecutor(agent=prompt, tools=self.tools,verbose=True)
