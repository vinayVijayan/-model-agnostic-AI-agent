import os
from litellm import completion
from typing import List, Dict
from dotenv import load_dotenv

# Load your local .env file securely
load_dotenv()

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="gemini/gemini-3.8-flash",  # Changed to match your working Gemini setup
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

def extract_code_block(response: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response
    code_block = response.split('```')[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:]
    return code_block.strip()

def intialize_python_func():
    print("what  lanuage should you consider learning?")
    function_description = input().strip()

    messages = [
        {'role':'system','content':"you are a language expert, give instructions on how to make the language easier to learn"}
    ]
    messages.append({
        'role':"user",'content':f"write some general learning techniques on how to learn {function_description} faster Output the function in a ```python code block```."
    })
    initial_function = generate_response(messages)
    initial_function = extract_code_block(initial_function)

    print(f"Techniques on How to learn {function_description} faster:")

    print(initial_function)

    messages.append({"role": "assistant", "content": "```python\n\n"+initial_function+"\n\n```"})

    messages.append({
        "role":"user",'content':"Add a documentation on the structure of the learning process Output the function in a ```python code block```."
    })
    documented_responce = generate_response(messages)
    documented_responce = extract_code_block(documented_responce)
    print("\n=== Documented ===")
    print(documented_responce)

if __name__ == "__main__":
    intialize_python_func()



