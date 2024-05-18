import vertexai
import json
import datetime
import random
import string
from vertexai.generative_models import GenerativeModel, ChatSession

import vertexai
from vertexai.preview.language_models import TextGenerationModel

class GeminiProChat:
    def __init__(self, project_id, location, model_name="gemini-1.0-pro-002"):
        """Initializes the GeminiProChat instance."""

        self.project_id = project_id
        self.location = location
        self.model_name = model_name
         # Generate a unique history file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.history_file = f"chat_history_{timestamp}_{random_string}.json"
        print(self.history_file)  # Added for debugging purposes

        # Initialize Vertex AI
        vertexai.init( project= self.project_id , location=self.location)

        self.model = GenerativeModel(self.model_name )
        self.chat = self.model.start_chat()
        self.conversation_history = []  
        try:
            with open(self.history_file, "a") as f:
                json.dump([], f)  # Start with an empty list if the file is new
        except IOError as e:
            print(f"Error opening history file: {e}")
        # self.load_history()

    # ... (rest of the methods: new_conversation, load_history, save_history) ...

    def get_chat_response(self , chat: ChatSession, prompt: str) -> str:
        if not prompt.strip():  # Check if prompt is empty after stripping whitespace
            return "Empty Prompt"  # Exit the function and return an empty string
        text_response = []
        responses = chat.send_message(prompt, stream=True)
        for chunk in responses:
            text_response.append(chunk.text)
        # Append prompt and response to history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "bot", "content": "".join(text_response)})

        # Write the updated history to the file
        with open(self.history_file, "w") as f:
            json.dump(self.conversation_history, f, indent=2) 
        return "".join(text_response)
    
    

# Example usage
# chat = GeminiProChat("geminivertex-423117", "us-central1")  
# response = chat.get_chat_response(chat.chat , "What is the population of Mumbai?")
# print(response) 
# response = chat.get_chat_response(chat.chat , "And Pune ? Delhi? Chennai?")
# print(response) 
