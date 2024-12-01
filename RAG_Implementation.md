# RAG (Retrieval Augmented Generation) Implementation

## Overview

The RAG implementation enables the AI assistant to access and provide accurate company information by combining document retrieval with language model generation.

## Implementation Details

### Document Processing (`prepare_data.py`) 
python
Documents are loaded from PDF files
Text is split into chunks (1024 tokens with 20% overlap)
Chunks are processed using RecursiveCharacterTextSplitter

### Vector Storage (`response.py`)
- Uses Pinecone vector database
- Embeddings created using OpenAI's text-embedding-3-small
- Documents stored as vectors for semantic search

### Query Processing
1. User query is embedded using the same embedding model
2. Similar chunks are retrieved from Pinecone
3. Retrieved context is used to generate accurate responses

### Key Components

1. **Document Preparation**:
   - PDF loading
   - Text chunking
   - Metadata preservation

2. **Vector Storage**:
   - Embedding generation
   - Vector indexing
   - Similarity search

3. **Query Pipeline**:
   - Context retrieval
   - Response generation
   - Source tracking

## Configuration

Key parameters in the implementation:
- Chunk size: 1024 tokens
- Chunk overlap: 20%
- Model: text-embedding-3-small
- Vector dimensions: 1536

## Usage
1. Query Processing:

```python
from KnowledgeBase.response import get_query_result
result = get_query_result(query="What are the company's services?")
```