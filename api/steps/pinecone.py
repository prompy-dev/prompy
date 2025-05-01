import os
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from flask import current_app
from pinecone import Pinecone

def log_response(res):
    current_app.logger.debug(res)

def pinecone_query():
    return RunnableLambda(_query_pinecone)

def _query_pinecone(d: dict):
    try:
            
        embedding = d.get("embedding")
        if embedding is None:
            raise Exception("Missing 'embedding' in input dictionary")
            
        parsed_response = d.get("parsed_response")
        if parsed_response is None:
            raise Exception("Missing 'parsed_response' in input dictionary")

        # Initialize Pinecone client using the new API
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        
        # Get a reference to the index
        index = pc.Index(os.environ.get("PINECONE_INDEX_NAME"))
        
        # Query Pinecone directly with the embedding
        query_response = index.query(
            vector=embedding,
            top_k=3,
            include_metadata=True
        )
        
        # Convert Pinecone matches to LangChain Document objects
        results = []
        for match in query_response.matches:
            if match.metadata and 'text' in match.metadata:
                doc = Document(
                    page_content=match.metadata.get('text', ''),
                    metadata={k: v for k, v in match.metadata.items() if k != 'text'}
                )
                results.append(doc)
                
        # Format the results for the next step
        context = "\n\n".join([doc.page_content for doc in results])
        
        log_response(f"Found {len(results)} relevant documents from Pinecone")

        d["pinecone_results"] = results
        d["context"] = context
        return d
        
    except Exception as e:
        current_app.logger.error(f"Pinecone error details: {str(e)}")
        current_app.logger.error(f"Error type: {type(e).__name__}")
        raise Exception(f"PineconeQueryException: {str(e)}")
    