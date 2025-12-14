import weaviate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_weaviate import WeaviateVectorStore
from app.config import get_settings

settings = get_settings()

def get_embeddings():
    """Initialize embedding model"""
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def get_vectorstore():
    """Get or create vector store"""
    # Connect using simple URL
    client = weaviate.connect_to_custom(
        http_host=settings.weaviate_url.replace("http://", "").split(":")[0],
        http_port=int(settings.weaviate_url.split(":")[-1]) if ":" in settings.weaviate_url else 8080,
        http_secure=False,
        grpc_host=settings.weaviate_url.replace("http://", "").split(":")[0],
        grpc_port=50051,
        grpc_secure=False
    )
    
    embeddings = get_embeddings()
    
    # Use WeaviateVectorStore
    vectorstore = WeaviateVectorStore(
        client=client,
        index_name="DocumentQA",
        text_key="text",
        embedding=embeddings
    )
    
    return vectorstore
