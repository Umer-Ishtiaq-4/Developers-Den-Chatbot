# Developers Den AI Assistant

An AI-powered chatbot that helps users learn about Developers Den company through natural conversation and can send company profiles via email.

## Setup Instructions

1. Clone the repository
2. Create a virtual environment and activate it: 
3. Install dependencies:
pip install -r requirements.txt
4. Create a `.env` file with the following variables:
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
5. Run the application:
python app.py

## Architecture Overview

The application is built using:
- Flask for the web server
- LangChain for AI agent orchestration
- OpenAI's GPT-4o-mini for natural language processing
- Pinecone for vector database storage
- RAG (Retrieval Augmented Generation) for company information retrieval

Key components:
- `app.py`: Flask server and main entry point
- `calls.py`: Agent setup and chat processing
- `tools.py`: Custom tools for company info retrieval and email sending
- `KnowledgeBase/`: RAG implementation for company information storage and retrieval

## Key Design Decisions

1. **LangChain Tools Agent**: Used `create_openai_tools_agent` for its simplicity and effectiveness in handling the two main tools:
   - Company information retrieval
   - Email profile sending

2. **Model Selection**:
   - GPT-4o-mini for agent decisions due to workflow simplicity
   - OpenAI's text-embedding-3-small for document embeddings, optimized for small PDF documents

3. **Vector Database**: Chose Pinecone for:
   - Fully managed solution
   - Reduced operational overhead
   - Good integration with LangChain

## Known Limitations

1. Document Processing:
   - Current parameter setup may not scale well with larger documents

2. Chat Interface:
   - Basic implementation without real-time updates

## Future Improvements

1. Real-time Chat:
   - Implement WebSocket for real-time communication
   - Add typing indicators and message status

2. Monitoring:
   - Add analytics for chat interactions
   - Implement feedback collection

3. UI/UX:
   - Add message threading
   - Implement message reactions
   - Add file attachment support