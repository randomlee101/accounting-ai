from waitress import serve
from flask import Flask, jsonify, json, request
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key="<YOUR_API_KEY_HERE>")
model = genai.GenerativeModel("gemini-1.0-pro-latest")
chat = genai.ChatSession


def check_operations():
    result = json.load(open('operations.json'))
    full_operations = result["operations"]
    return full_operations


def extract_operation_names(operations=None):
    if operations is None:
        return []
    operation_names = list(operations.keys())
    return operation_names


def perform_operation(operation, operation_name):
    if operation["canHandler"] is False:
        print(operation_name)
        response = chat.send_message(
            f"Generate an humane message telling the user you can not perform this operation {operation_name} directly, you don't need to make further suggestions, just say you cannot perform it, then try to make {operation_name} blend into the text without looking like an actual variable.")
        list_of_guidance = "Please follow these steps:"
        count = 0
        for g in operation["guidance"]:
            list_of_guidance = f"{list_of_guidance} \n{count + 1}. {g}"
        new_text = f"{response.text} {list_of_guidance}"
        return operation["canHandler"], new_text
    else:
        requirements = operation["requiredInputs"]
        command = (f"Generate a json from the previous prompt with this as requirements {requirements} strictly, "
                   f"anything that isn't available should default to null")
        response = chat.send_message(command)
        print(response.text)
        return operation["canHandler"], json.loads(response.text.removeprefix("```json").removesuffix("```").strip())


def check_if_all_requirements_are_met(data=None):
    if data is None:
        data = {}
    missing_requirements = [r for r in data.keys() if data[r] is None]
    return missing_requirements


@app.route("/")
def say_welcome():
    return jsonify({"greetings": "willkommen"})


@app.route("/chat", methods=["GET", "POST"])
def chat():
    all_operations = check_operations()
    operation_keys = extract_operation_names(all_operations)
    message = request.json["message"]
    command = (f"which of the following operations {operation_keys} tally with the message {message}. If not of it "
               f"tallies, just return None")
    response = chat.send_message(command)
    if response.text == "None":
        return jsonify({"response": "This operation is not recognized by the system."})
    op_name = response.text.replace('\'', '').strip()
    can_handle, result = perform_operation(all_operations[op_name], operation_name=op_name)
    return jsonify({"response": result})


if __name__ == "__main__":
    print(check_if_all_requirements_are_met({"hello": None}))
    chat = model.start_chat()
    print("Server Running on port 3000")
    serve(app, port=3000)
