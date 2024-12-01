from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain import hub

from tools import (
    SendProfileViaEmail,
    RetrieveCompanyInformation
)
from prompts import tool_agent_prompt

llm = ChatOpenAI(
    model="gpt-4o-mini",
    # temperature=0, 
    max_retries=2
)

tools = [
    SendProfileViaEmail(),
    RetrieveCompanyInformation()
]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", tool_agent_prompt),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def convert_chat_history_understandable(chat_history):
    upd_chat_history = []

    # Iterate over the chat history and add each message as a HumanMessage and AIMessage
    for chat in chat_history:
        if chat.get('role') == 'Human':
            upd_chat_history.append(HumanMessage(chat.get('content')))
        else:
            upd_chat_history.append(AIMessage(chat.get('content')))

    return upd_chat_history


def get_query_response(query: str, chat_history: list):
    """
    Process a query using the provided chat history and return the agent's response.

    Args:
        query (str): The user's query to be processed.
        chat_history (list): List of previous chat messages for context.

    Returns:
        dict: Response from the agent containing the answer and any additional data.
    """
    # Convert chat history into a format understandable by the agent
    if chat_history:
        chat_history = convert_chat_history_understandable(chat_history)
    
    # print("\nUpdated chat history: ", chat_history)

    # Invoke the agent executor with the current query and chat history
    response = agent_executor.invoke(
        {
            "input": f"{query}",
            "chat_history": chat_history
        })

    return response

