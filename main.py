from graph.workflow import NewsAnalysisWorkflow
import json

def main():
    """Run the news analysis workflow."""
    initial_state = {
        "news_data":"",
        "analysis_results":[],
        "vector_search_results":[],
        "current_stage":"",
        "error":""
    }
    graph = NewsAnalysisWorkflow.create_graph()
    result = graph.invoke(initial_state)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()