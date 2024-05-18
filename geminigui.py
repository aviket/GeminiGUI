import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QScrollArea , QPlainTextEdit, QPushButton, QVBoxLayout
from gemeini2 import *
from PyQt5.QtCore import Qt
from vertexai.generative_models._generative_models import ResponseValidationError

class GeminiProChatApp(QWidget):
    def __init__(self, project_id, location, model_name="gemini-1.0-pro-002"):
        super().__init__()

        self.gemini_chat = GeminiProChat(project_id, location, model_name)  # Initialize your GeminiProChat class
        self.setWindowTitle("Gemini Pro Chat")
        self.layout = QVBoxLayout()

        # Prompt Input
        self.prompt_input = QPlainTextEdit()
        self.layout.addWidget(QLabel("Enter your prompt:"))
        self.layout.addWidget(self.prompt_input)


        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.get_response)  # Connect to response function
        self.layout.addWidget(self.send_button)

        # Response Display (with QScrollArea)
        self.response_scroll = QScrollArea()
        self.response_label = QLabel()
        self.response_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align text to the top left
        self.response_label.setWordWrap(True)  # Enable word wrap
        self.response_scroll.setWidgetResizable(True)  # Allow resizing of the label within the scroll area
        self.response_scroll.setWidget(self.response_label)
        self.layout.addWidget(self.response_scroll)

        # Set Maximum Height for Response Area
        max_response_height = 700  # Adjust as needed
        self.response_scroll.setMaximumHeight(max_response_height)

        self.setLayout(self.layout)

    def get_response_old(self):
        prompt = self.prompt_input.toPlainText()
        try:
            response = self.gemini_chat.get_chat_response(self.gemini_chat.chat, prompt)

            # Update the label with the response
            self.response_label.setText(response)
        except ResponseValidationError as e:
            error_message = (
                "An error occurred while generating a response:\n"
                f"{e.message}\n"
                "Please try rephrasing your prompt or try again later."
            )
            self.response_label.setText(error_message)
        except Exception as e:  # Catch any other unexpected exceptions
            self.response_label.setText(f"Unexpected error: {e}")


    def get_response(self):
        prompt = self.prompt_input.toPlainText()

        try:
            response = self.gemini_chat.get_chat_response(self.gemini_chat.chat, prompt)
            current_text = self.response_label.text()  # Get existing text from label

            # Add prompt and response with formatting to the label
            new_text = f"You:{prompt}\nGemini:{response}\n______________\n"  
            self.response_label.setText(current_text + new_text)  # Append

        except ResponseValidationError as e:
            error_message = (
                "An error occurred while generating a response:\n"
                f"{str(e)}\n" 
                "Please try rephrasing your prompt or try again later.\n\n"
            )
            self.response_label.setText(self.response_label.text() + error_message)
        except Exception as e:  
            self.response_label.setText(self.response_label.text() + f"Unexpected error: {e}\n\n")




if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Input credentials (replace with actual values)
    project_id = "geminivertex-423117" 
    location = "us-central1" 
    model_name = "gemini-1.0-pro-002" 

    # Create and show the widget
    chat_app = GeminiProChatApp(project_id, location, model_name)
    chat_app.show()
    sys.exit(app.exec_()) 
