from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import get_settings
from pathlib import Path
from typing import List

settings = get_settings()

def load_and_split_document(file_path: str) -> List:
    """Load and split document into chunks"""
    file_extension = Path(file_path).suffix.lower()
    
    # Load document based on type
    if file_extension == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension in ['.txt', '.md']:
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    documents = loader.load()
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len
    )
    
    splits = text_splitter.split_documents(documents)
    return splits
