from pprint import pprint

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from calls import get_query_response

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    # pprint(data)

    user_message = data.get('message', '')
    chat_history = data.get('chat_history', [])

    if not user_message:
        return jsonify({
            "error": "Please pass query in the message field"
        })

    try:    
        # Get response from the chain
        if user_message == 'start':
            # return jsonify({
            #     "response": "**Developers Den** is a specialized AI solutions company that has successfully served over 25 clients and completed more than 40 AI projects. The company has recently expanded globally with a new USA office in 2023 and offers comprehensive services including product engineering, web development, and mobile development. \n\nWould you like to know more specific details about Developers Den, such as their vision, services, or achievements?"
            # })
            user_message = "Give me brief company overview (maximum 2 sentences)."

        response = get_query_response(query=user_message, chat_history=chat_history)       
        # pprint(response)

        return jsonify({
            "response": response['output']
        })
    except Exception as e:
        print("\nError in chat: ", str(e))
        return jsonify({
            "error": str(e)
        })
    
    

if __name__ == '__main__':
    app.run(debug=True) 