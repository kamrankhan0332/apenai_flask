from flask import Flask, request, jsonify
from .chatbot import ChatGPTBot

app = Flask(__name__)
openai_api_key = "insert open ai key here"
chatbot = ChatGPTBot(api_key=openai_api_key, engine="davinci")


@app.route('/create_prompt', methods=['POST'])
def create_prompt():
    data = request.get_json()
    prompt = data.get('prompt')
    unique_id = chatbot.create_prompt(prompt)
    return jsonify({"id": unique_id, "prompt": prompt})


@app.route('/get_response/<unique_id>', methods=['GET'])
def get_response(unique_id):
    for item in chatbot.prompts:
        if item['id'] == unique_id:
            response = chatbot.get_response(unique_id)
            return jsonify({"response": response})
    return jsonify({"message": "Prompt not found."}), 404


@app.route('/update_prompt/<unique_id>', methods=['PUT'])
def update_prompt(unique_id):
    data = request.get_json()
    new_prompt = data.get('new_prompt')
    for item in chatbot.prompts:
        if item['id'] == unique_id:
            chatbot.update_prompt(unique_id, new_prompt)
            return jsonify({"message": "Prompt updated successfully."})
    return jsonify({"message": "Prompt not found."}), 404


@app.route('/delete_prompt/<unique_id>', methods=['DELETE'])
def delete_prompt(unique_id):
    if chatbot.delete_prompt(unique_id):
        return jsonify({"message": "Prompt deleted successfully."})
    else:
        return jsonify({"message": "Prompt not found."}), 404
