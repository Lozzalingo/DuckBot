import sys
from sentence_transformers import SentenceTransformer
from models import call_deepseek, call_ollama

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(call_ollama(user_input))
        #print(call_deepseek(user_input))
    else:
        print("No input provided.")
