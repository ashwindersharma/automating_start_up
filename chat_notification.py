import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import subprocess
import ollama
OLLAMA_URL = "http://localhost:11434/api/generate"

    # Intent-action mapping


# response = ollama.chat(
#     model="llama3.2:latest",
#     messages=[{"role": "user", "content": "Hello, how are you?"}]
# )

# print(response)


# def send_message():
#     user_message = entry.get()
#     if user_message:
#         chat_window.insert(tk.END, f"You: {user_message}\n")
#         entry.delete(0, tk.END)
#             # Send the message to Ollama API
#         response = send_to_ollama(user_message)
#         if response:
#             chat_window.insert(tk.END, f"AI: {response}\n")

# def send_to_ollama(prompt):
#     try:
#         payload = {
#             "model": "llama3.2:latest",
#             "prompt": prompt,
#             "stream": True  # Set to True if you want to stream the response
#         }
#         response = requests.post(OLLAMA_URL, json=payload)
#         response_json = response.json()
#         return response_json.get("response", "No response from AI")
#     except Exception as e:
#         return f"Error: {str(e)}"
intent_mapping = {
        "setup my pc for work": "fucntioncall",
        "kick started": "fucntioncall",
        "get started": "fucntioncall",
        "setup xampp": "fucntioncall",
        "open project": "fucntioncall",
    }
def send_message():
    user_message = entry.get()
    detected_intent = detect_intent(user_message)
    print(detected_intent)
    response = execute_action(detected_intent,user_message)

    # Newline after response

def stream_ollama(prompt):
    try:
        payload = {
            "model":  "llama3.2:latest",
            "prompt": prompt,
            "stream": True  # Enable streaming
        }
        response = requests.post(OLLAMA_URL, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    yield json_data.get("response", "")
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        yield f"Error: {str(e)}"


def detect_intent(user_input):
    """Use Ollama to extract intent from user input."""
    response = ollama.chat(
        model="llama3.2:latest",  # Replace with the actual model name
        messages=[
            {"role": "system", "content": "Identify the user's intent from the following list: "
                                          "'setup my pc for work', 'kick started', 'get started', "
                                          "'setup xampp', 'open project'. "
                                          "If the user intent matches one of these, return the exact phrase. "
                                          "If it does NOT match, return only 'general_query'."},
            {"role": "user", "content": user_input}
        ]
    )
    
    detected_intent = response['message']['content'].strip().lower()
    return detected_intent

def execute_action(intent,user_message):
    """Execute script if intent matches, else respond naturally."""

    if user_message:
        chat_window.insert(tk.END, f"You: {user_message}\n")
        entry.delete(0, tk.END)

        chat_window.insert(tk.END, "AI: ")  # Start AI response line
        app.update_idletasks()  # Force update UI

     

    if intent in intent_mapping:
        script_path = intent_mapping[intent]
        print(f"Executing: {script_path}")
        # subprocess.run([script_path], shell=True)
        return "Your setup has been initiated!"
    else:
           # Send message to Ollama
        for chunk in stream_ollama(user_message):
            chat_window.insert(tk.END, chunk)
            chat_window.see(tk.END)  # Auto-scroll
            app.update_idletasks()  # Update UI as response comes in

        chat_window.insert(tk.END, "\n") 
        # return ask_ollama(intent)  # Handle non-matching intents

def ask_ollama(user_input):
    """Get a natural response from Ollama for general queries."""
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[{"role": "user", "content": user_input}]
    )
    return response['message']['content']
  
    # Get user intent
# Create the main application window
app = tk.Tk()
app.title("Ai Ash Model")
app.geometry("800x800")

# Chat display area
chat_window = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=20)
chat_window.pack(pady=10)

# Input field
entry = tk.Entry(app, width=40)
entry.pack(pady=5)

# Send button
send_button = tk.Button(app, text="Send Mess", command=send_message)
send_button.pack()

# Start the application
app.mainloop()

# make a executable app pyinstaller --onefile --windowed --name ChatApp chat_notification.py

