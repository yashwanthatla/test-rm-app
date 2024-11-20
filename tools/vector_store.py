# tools/vector_store.py
import sys
import os
from pathlib import Path
import shutil

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
            "asset_sub_class": "sub_classes"
        }
        self._initialized_collections = None 
    
    def reset_vectorstore(self):
        """Delete all existing collections and their data."""
        if self.store_path.exists():
            shutil.rmtree(self.store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
    
    def _get_collection_data(self) -> Dict[str, List[Dict]]:
        """Organize sample data by collection type."""
        collections_data = {
            "asset_class": [],
            "asset_sub_class": [],  # Changed from sub_class to match data
        }
        
        for item in SAMPLE_ASSET_DATA:
            item_type = item["type"]
            if item_type in collections_data:
                collections_data[item_type].append(item)
        print("collection_data",collections_data)
        
        return collections_data

    def init_vectorstore(self):
        """Initialize separate Chroma collections for each data type."""
        collections = {}
        data_by_collection = self._get_collection_data()
        
        for collection_type, collection_name in self.collections.items():
            # print("collection type",collection_type,"collection_name",collection_name)
            texts = [json.dumps(item) for item in data_by_collection[collection_type]]
            # print('vector store text',texts)
            metadatas = [{"type": collection_type} for _ in texts]
            # print("metadata",metadatas)
            collections[collection_type] = Chroma.from_texts(
                texts=texts,
                metadatas=metadatas,
                embedding=self.embeddings,
                collection_name=collection_name,
                persist_directory=str(self.store_path / collection_name)
            )
        self._initialized_collections = collections
        
        return collections
    
    def search(self, query: str, min_confidence: float = 0.85):
        """Search the appropriate Chroma collection based on query type."""
        if self._initialized_collections is None:
            collections = self.init_vectorstore()
        else:
            collections = self._initialized_collections
        k = 20  
        
        def get_filtered_results(collection):
            # Get results with scores
            results_with_scores = collection.similarity_search_with_relevance_scores(query, k=k)
            print(results_with_scores," result with scores for query ",query)
            # Filter results based on confidence threshold and convert scores to percentage
            filtered_results = []
            for doc, score in results_with_scores:
                # Convert similarity score to percentage (scores are typically between -1 and 1)
                confidence_percentage = (score + 1) / 2  # Normalize to 0-1 range
                if confidence_percentage >= min_confidence:
                    filtered_results.append(doc)
            
            return filtered_results
        
        # Determine which collection to search based on the query
        query_lower = query.lower()
        if "asset_class" in query_lower:
            collection = collections.get("asset_class")
            return get_filtered_results(collection) if collection else []
        
        elif "security" in query_lower:
            collection = collections.get("security_name")
            return get_filtered_results(collection) if collection else []
        
        elif "asset_sub_class" in query_lower:
            collection = collections.get("asset_sub_class")
            return get_filtered_results(collection) if collection else []
        
        else:
            # Search all collections and combine results
            all_results = []
            for collection in collections.values():
                if collection:  # Only search if collection exists
                    filtered_docs = get_filtered_results(collection)
                    all_results.extend(filtered_docs)
            return all_results

    
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
    print("Resetting vector store...")
    vector_store.reset_vectorstore()
    print("Initializing with sample data")
    vector_store.initialize_with_sample_data()
    print("Vector store initialized with sample data!")
