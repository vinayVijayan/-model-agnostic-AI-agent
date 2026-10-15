import os
import time
from litellm import completion
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

def generate_response(messages: List[Dict], retries: int = 3) -> str:
    """Call LLM to get response with automatic retries for busy servers"""
    for attempt in range(retries):
        try:
            response = completion(
                model="gemini/gemini-3.8-flash", 
                messages=messages,
                max_tokens=1024
            )
            return response.choices[0].message.content
            
        except Exception as e:
            if "503" in str(e) or "429" in str(e):
                print(f"Server busy. Retrying in {5 * (attempt + 1)} seconds...")
                time.sleep(5 * (attempt + 1)) # Waits 5s, then 10s, then 15s
            else:
                raise e # If it's a different error, crash normally
                
    return "Error: Could not connect to Gemini after multiple attempts."

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
        {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
    ]
    
    print("Thinking...")
    response = generate_response(messages)
    print(response)