# tools/vector_store.py
import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import json
from pathlib import Path
from typing import List, Dict
from data.sample_data import SAMPLE_ASSET_DATA
from dotenv import load_dotenv

load_dotenv()


class VectorStoreManager:
    def __init__(self, store_path: str = "vectorstore"):
        self.store_path = Path(store_path)
        self.embeddings = OpenAIEmbeddings()
        self.collections = {
            "asset_class": "asset_classes",
            "security_name": "securities",
            "sub_class": "sub_classes"
        }
    
    def _get_collection_data(self) -> Dict[str, List[Dict]]:
        """Organize sample data by collection type."""
        collections_data = {
            "asset_class": [],
            "security_name": [],
            "sub_class": []
        }
        
        for item in SAMPLE_ASSET_DATA:
            if item["type"] == "asset_class":
                collections_data["asset_class"].append(item)
                # Add sub-classes if they exist
                if "sub_classes" in item:
                    for sub_class in item["sub_classes"]:
                        collections_data["sub_class"].append({
                            "name": sub_class,
                            "parent": item["name"],
                            "type": "sub_class"
                        })
            elif item["type"] == "security_name":
                collections_data["security_name"].append(item)
        
        return collections_data

    def init_vectorstore(self):
        """Initialize separate Chroma collections for each data type."""
        collections = {}
        data_by_collection = self._get_collection_data()
        
        for collection_type, collection_name in self.collections.items():
            texts = [json.dumps(item) for item in data_by_collection[collection_type]]
            metadatas = [{"type": collection_type} for _ in texts]
            
            collections[collection_type] = Chroma.from_texts(
                texts=texts,
                metadatas=metadatas,
                embedding=self.embeddings,
                collection_name=collection_name,
                persist_directory=str(self.store_path / collection_name)
            )
        
        return collections
    
    def search(self, query: str, k: int = 4):
        """Search the appropriate Chroma collection based on query type."""
        collections = self.init_vectorstore()  # In production, load existing collections
        
        # Determine which collection to search based on the query
        if "asset_class" in query.lower():
            collection = collections["asset_class"]
        elif "security" in query.lower():
            collection = collections["security_name"]
        elif "sub_class" in query.lower():
            collection = collections["sub_class"]
        else:
            # Search all collections and combine results
            all_results = []
            for collection in collections.values():
                all_results.extend(collection.similarity_search(query, k=k))
            return all_results
        
        return collection.similarity_search(query, k=k)
    
    def initialize_with_sample_data(self):
        """Initialize and persist the vector store with sample data."""
        # Create store directory if it doesn't exist
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize collections with sample data
        collections = self.init_vectorstore()
        
        # Persist each collection
        for collection_type, collection in collections.items():
            collection.persist()
        
        return collections


# Usage example:
if __name__ == "__main__":
    # Initialize vector store with sample data
    vector_store = VectorStoreManager()
    vector_store.initialize_with_sample_data()
    print("Vector store initialized with sample data!")
