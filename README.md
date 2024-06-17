# Account AI Demo

_This is the demo for the LLM powered accounting system_

System Configuration

- pip version - 23.2.1
- python version - 3.9

Project Requirements
- waitress - to serve the app
- Flask - to create the app
- google-generativeai - to integrate the LLM

Installing Dependencies
```commandline
pip install -r requirements.txt --no-cache
```

Running Application

_You need to enter your API key gotten from Google AI Studio in the index file_
```python
genai.configure(api_key="<YOUR_API_KEY_HERE>")
```

_Run the application_
```commandline
python src/index.py
```

Start Chat

_For test purposes, the chat session resets each time you start the server_

```html
http://localhost:3000/chat
```

Request Body

_On the first message the AI is expecting a prompt for the operation to be carried out_
```json lines
{
  "message": '<Enter your message here>'
}
```