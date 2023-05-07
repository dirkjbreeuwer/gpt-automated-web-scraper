"""test_gpt_interaction.py: A script to test the GPTInteraction class."""
import sys
import os
from gpt_interaction.gpt_interaction import GPTInteraction

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    gpt = GPTInteraction()

    prompt = "Translate the following English text to French: 'Hello, how are you?'"
    response = gpt.call(prompt)

    print(f"Prompt: {prompt}")
    print(f"Response: {response.strip()}")
