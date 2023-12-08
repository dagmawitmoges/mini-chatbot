import tkinter as tk
from tkinter import scrolledtext
from fuzzywuzzy import fuzz

import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Define responses based on user input
responses = {
    "hello": "Hi there! How can I help you today?",
    "how can i pay my bill?": "You can pay your bill online through our website or mobile app.",
    "i'm experiencing internet issues.": "Have you tried restarting your router? That often resolves connectivity issues.",
    "yes , i have already done that": "in that case: please check the physical connections to ensure everything is properly connected.",
    "what are your business hours?": "Our business hours are from 9 AM to 6 PM: Monday to Friday.",
    "how do i change my plan?": "You can change your plan by logging into your account on our website.",
    "i forgot my password.": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
    "is there a service outage in my area?": "Please provide your location: and i'll check for any reported outages.",
    "can i upgrade my current package?": "Yes: you can upgrade your package by contacting our customer support team.",
    "how do i contact customer support?": "You can reach our customer support by calling our toll-free number or using the live chat option on our website.",
    "do you offer any discounts for long-term customers?": "Yes: we have special loyalty discounts for customers who have been with us for over a year.",
    "what is the speed of your internet plans?": "Our internet plans offer speeds ranging from 25 Mbps to 1 Gbps: depending on the package you choose.",
    "i'm moving. how do i transfer my service?": "Contact our customer support team with your new address: and they'll assist you in transferring your service.",
    "are you rational?": "i operate based on patterns and data i've been trained on: aiming to provide coherent and contextually relevant responses. However: i don't possess emotions: consciousness: or personal opinions. My 'rationality' stems from processing information within predefined patterns and rules.",
    "thank you for setting up my service.": "You're welcome! if you have any further questions or need assistance: don't hesitate to ask.",
    "i really appreciate the help.": "My pleasure! Have a wonderful day.",
    "user_name_question": "What's your name?",
    "user_name_response": "Nice to meet you, {user_name}! How can i assist you today?"
}

# Initialize user's name
user_name = ""
initial_interaction = True
def get_matching_response(user_input):
    # Calculate similarity scores between user input and predefined responses
    similarity_scores = {key: fuzz.ratio(user_input.lower(), key) for key in responses}

    # Get the response with the highest similarity
    max_key = max(similarity_scores, key=similarity_scores.get)
    max_score = similarity_scores[max_key]

    # Return the response if similarity is above a threshold
    threshold = 60  # You can adjust this threshold as needed
    return responses[max_key] if max_score >= threshold else None

def process_input(user_input):
    global user_name , initial_interaction

    # Convert user input to lowercase
    user_input_lower = user_input.lower()

    # Process user input with spaCy
    doc = nlp(user_input_lower)

    # Check for specific intents
    if "name" in user_input_lower and "your" in user_input_lower:
        response = responses.get("user_name_question", "I'm sorry, I don't understand that.")
    elif not user_name:
        # If user's name is not set, ask for it
        user_name = user_input
        response = responses.get("user_name_response", "Nice to meet you! How can I assist you today?")
        response = response.replace("{user_name}", user_name)
    else:
        # Use fuzzy matching to get a related response
        related_response = get_matching_response(user_input)
        if related_response:
            response = related_response.replace("{user_name}", user_name)
        else:
            response = "I'm sorry, I don't understand that."


# Get and display the response
    chat_log.config(state=tk.NORMAL)
    if initial_interaction == False:
        chat_log.insert(tk.END, f"User: {user_input}\n")
        chat_log.insert(tk.END, f"Chatbot: {response}\n\n")
        chat_log.config(state=tk.DISABLED)
        chat_entry.delete(0, tk.END)
    else:
        chat_log.insert(tk.END, f"Chatbot: {response}\n\n")
        chat_log.config(state=tk.DISABLED)
        chat_entry.delete(0, tk.END)
        initial_interaction = False

def send_message():
    user_input = chat_entry.get()
    process_input(user_input)

# Create the main window
root = tk.Tk()
root.title("Simple Chatbot Interface")

# Create a scrolled text widget for chat log
chat_log = scrolledtext.ScrolledText(root, width=40, height=15, state=tk.DISABLED)
chat_log.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Create an entry widget for user input
chat_entry = tk.Entry(root, width=30)
chat_entry.grid(row=1, column=0, padx=10, pady=10)

# Ask for the user's name immediately upon running the app
process_input("What's your name?")

# Create a button to send user input
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()