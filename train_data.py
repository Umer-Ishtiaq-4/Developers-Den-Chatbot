"""
A module for training and querying a document-based QA system using LangChain and Pinecone.
Handles document loading, chunking, embedding, and question answering functionality.
"""

import os
from pprint import pprint

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore 
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import ServerlessSpec, Pinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configuration constants
INDEX_NAME = "test-index"
CHUNK_SIZE = 1024  # Size of text chunks for splitting documents
CHUNK_OVERLAP = CHUNK_SIZE * 0.2  # Overlap between chunks (20%)

# Initialize embedding model
embedding_model = 'text-embedding-3-small'
embeddings = OpenAIEmbeddings(
    model=embedding_model
)

# Initialize vector store
vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

# Initialize Pinecone client
pc = Pinecone()

# Initialize language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

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

def prepare_data(documents_folder="Documents/"):
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

def train_data():
    """
    Train the vector store with prepared documents.
    
    Returns:
        bool: True if training successful, False otherwise
    """
    documents = prepare_data()

    try:
        vectorstore.add_documents(documents=documents)
        return True
    except Exception as e:
        print(e)
        return False

def get_qa_chain_prompt():
    """
    Get the QA chain prompt template.
    
    Returns:
        PromptTemplate: Configured prompt template
    """
    template = """\
Use the following pieces of context to answer the question at the end. Always use numbers when generating steps. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer straight forward. Your answer should be properly formatted.
{context}
Question: {question}
Helpful Answer:"""
    return PromptTemplate.from_template(template)

def get_query_result(query):
    """
    Get answer for a given query using the QA chain.
    
    Args:
        query (str): Question to be answered
        
    Returns:
        dict/str: Query result or error message
    """
    QA_CHAIN_PROMPT = get_qa_chain_prompt()

    # Initialize QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            # search_kwargs={"k": 2}
        ),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        return_source_documents=True,
        verbose=False
    )

    try:
        print("Querying...")
        result = qa_chain.invoke({
            "query": query
        })
        return result.get('result')
    except Exception as e:
        print(e)
        return "There was an error retrieving data for your request. Please try again."

def main(query):
    """
    Main function to process queries and display results.
    
    Args:
        query (str): Question to be answered
    """
    # Uncomment to train data
    # trained = train_data()
    # if trained:
    #     print("Data trained successfully", end="\n\n")
    # else:
    #     print("Data training failed", end="\n\n")

    result = get_query_result(query=query)

    if isinstance(result, dict):
        print("Answer: ", result["result"], sep='\n', end="\n\n")
        print("Source: ", [doc.metadata["source"] for doc in result["source_documents"]], end="\n\n")
    else:
        print("Error: ", result)

if __name__ == "__main__":
    main(query="What are the services provided by the company?")