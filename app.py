import time
from pprint import pprint

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

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
        # static first message
        if user_message == 'start':
            time.sleep(1)
            # user_message = "Give me brief company overview (maximum 2 sentences)."
            return jsonify({
                "response": "**Developers Den** is a specialized AI solutions company that has served over 25 clients and completed more than 40 AI projects. We recently expanded globally with a new office in the USA in 2023, offering services in product engineering, web development, and mobile development. \n\nWould you like to know more about our vision, services, or achievements?"
            })

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