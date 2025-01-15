from gpt4all import GPT4All

MODEL_PATH = "models/"  # Update with your model path
MODEL_NAME = "gpt4all-13b-snoozy-q4_0.gguf"  # Add model name

model = GPT4All(model_name=MODEL_NAME, model_path=MODEL_PATH, allow_download=False) # Set allow_download to False

def get_chatbot_response(user_input):
    """
    Generates a response from the GPT4All chatbot.

    Args:
        user_input: The user's input text.

    Returns:
        The chatbot's response.
    """
    with model.chat_session():
        response = model.generate(prompt=user_input, temp=0.7)  # Adjust temp for creativity
        return response