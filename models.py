import sqlite3
import subprocess
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval import search_duckboy_facts


def call_deepseek(user_input):
    try:
        model_name = "deepseek-r1:32b"  # Using deepseek model

        # Try fetching relevant fact from database
        retrieved_fact = search_duckboy_facts(user_input)

        if retrieved_fact:
            final_prompt = f"The user asked this: {user_input}. Here's some additional information: {retrieved_fact}. When you reply, get into character and respond as Duck Boy.\n\nKeep the response short but funny."
        else:
            final_prompt = f"Remember, you are Duck Boy and you should respond in character.\n\n{user_input}. Keep the response short but funny."

        # Call the Deepseek subprocess
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=final_prompt,
            text=True,
            capture_output=True
        )
        response = result.stdout.strip()
        print(f"Thinking Response: {response}")

        # Extract text after </think> tag using regex
        match = re.search(r"</think>\s*(.*)", response, re.DOTALL)

        # Extract response text or return the full response if no match is found
        response_text = match.group(1) if match else response

        return response_text
    except Exception as e:
        print(f"Error generating reply: {e}")
        return "Oops, I seem to have short-circuited!"
    
# Function to call Ollama with dynamic prompt
def call_ollama(user_input):
    try:
        model_name = "llama3.2:latest"  # Replace with your AI model

        # Try fetching relevant fact from database
        retrieved_fact = search_duckboy_facts(user_input)

        if retrieved_fact:
            final_prompt = f"The user asked this: {user_input}. Here's some addional information: {retrieved_fact}. When you reply, get into character and respond as Duck Boy.\n\n. Keep the response short but funny."
        else:
            final_prompt = f"Remember, you are Duck Boy and you should respond in character.\n\n{user_input}. Keep the response short but funny."

        # Call Ollama with final prompt
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=final_prompt,
            text=True,
            capture_output=True
        )
        response = result.stdout.strip()
        return response
    except Exception as e:
        print(f"Error generating reply: {e}")
        return "Oops, I seem to have short-circuited!"
