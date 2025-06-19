#!/usr/bin/env python3

import sys
from litellm import completion

PROMPT = """Score this llm output (give the input), 1-100. Only output the score."""

def main():
    # Read input which contains: input_text\n---\nmodel_output
    content = sys.stdin.read().strip()
    
    try:
        # Use litellm to call gpt4.1-nano
        response = completion(
            model="gpt-4o-mini",  # Using actual model name
            messages=[{"role": "user", "content": PROMPT + "\n\n" + content}],
            max_tokens=10
        )

        score = response.choices[0].message.content
        score = float(score)
        
        # Output the response
        print(score)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 