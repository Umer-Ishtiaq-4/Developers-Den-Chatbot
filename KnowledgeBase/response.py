from pprint import pprint

from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore 
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pinecone import ServerlessSpec, Pinecone

from .prepare_data import prepare_documents

# Load environment variables
load_dotenv()

# Configuration constants
INDEX_NAME = "test-index"

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
    Get the answer for a given query using the QA chain.
    
    Args:
        query (str): The question to be answered.
        
    Returns:
        dict/str: The query result or an error message.
    """
    # Retrieve the QA chain prompt template
    QA_CHAIN_PROMPT = get_qa_chain_prompt()

    # Initialize the QA chain with the specified parameters
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
    
        # Check if the result is a dictionary
        if isinstance(result, dict):
            print("Answer: ", result["result"], sep='\n', end="\n\n")
            print("Source: ", [doc.metadata["source"] for doc in result["source_documents"]], end="\n\n")

            return result.get('result')
        else:
            print("Error: ", result)
            raise Exception("There was an error retrieving data for your request. Please try again.")
            
    except Exception as e:
        print(e)
        return "There was an error retrieving data for your request. Please try again."


def train_data():
    """
    Train the vector store with prepared documents.
    
    Returns:
        bool: True if training successful, False otherwise
    """
    documents = prepare_documents(documents_folder="Documents/")

    try:
        vectorstore.add_documents(documents=documents)
        return True
    except Exception as e:
        print(e)
        return False
    
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

    # print(result)

if __name__ == "__main__":
    main(query="What are the services provided by the company?")