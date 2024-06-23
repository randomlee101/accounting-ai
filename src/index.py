from waitress import serve
from flask import Flask, jsonify, json, request
import google.generativeai as genai


def check_operations():
    result = json.load(open('operations.json'))
    full_operations = result["operations"]
    return full_operations


def extract_operation_names(operations=None):
    if operations is None:
        return []
    operation_names = list(operations.keys())
    return operation_names


app = Flask(__name__)
genai.configure(api_key="<YOUR_API_KEY_HERE>")
model = genai.GenerativeModel("gemini-1.5-pro-latest",
                              system_instruction=[
                                  "You are an accounting assistant",
                                  "You help people gain understanding of different accounting instruments",
                                  "You can also help them perform different operations within the system",
                                  "You will also need to steer them closer to all things accounting instead of "
                                  "deviating",
                                  f"This is a list of some specific operations the system can perform when needed "
                                  f"${extract_operation_names(check_operations())}",
                                  f"If an operation needs to be performed from with this list "
                                  f"${extract_operation_names(check_operations())} check if 'canHandler' in "
                                  f"${check_operations()} for the particular operation is true to see if the system "
                                  f"can handle the operation of not",
                                  "When asking the user for requirements you do not need to include the variable name"
                                  f"If all that is needed for the operation has been provided, return a json response "
                                  f"with the requirements and their values",
                              ])
chat = genai.ChatSession


@app.route("/")
def say_welcome():
    return jsonify({"greetings": "willkommen"})


@app.route("/chat", methods=["GET", "POST"])
def chat():
    message = request.json["message"]
    response = chat.send_message(message)
    result = response.text
    if str(result).__contains__("json"):
        result = json.loads(result[result.find("```json") + len("```json"):result.find("\n```")].strip())
    return jsonify({"response": result})


if __name__ == "__main__":
    chat = model.start_chat()
    print("Server Running on port 3000")
    serve(app, port=3000)
