from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 1024  # Size of text chunks for splitting documents
CHUNK_OVERLAP = CHUNK_SIZE * 0.2  # Overlap between chunks (20%)

def load_documents(directory):
    """
    Load PDF documents from specified directory.
    
    Args:
        directory (str): Path to directory containing PDF files
        
    Returns:
        list: List of loaded documents
    """
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents

def split_documents(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Split documents into smaller chunks for processing.
    
    Args:
        docs (list): List of documents to split
        chunk_size (int): Size of each chunk
        chunk_overlap (int): Overlap between chunks
        
    Returns:
        list: List of document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc = text_splitter.split_documents(docs)
    return doc

def prepare_documents(documents_folder="Documents/"):
    """
    Prepare documents by loading and splitting them.
    
    Args:
        documents_folder (str): Path to documents folder
        
    Returns:
        list: Processed document chunks
    """
    try:
        original_documents = load_documents(documents_folder)
        print("Total documents: ", len(original_documents), end="\n")
    except Exception as e:
        print("Error loading documents: ", e)
        raise Exception(e)
    
    documents = split_documents(docs=original_documents)
    print("Total documents after splitting: ", len(documents), end="\n")
    # print(documents[0])

    return documents