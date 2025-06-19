#!/usr/bin/env python3

import sys
from litellm import completion

def main():
    # Read input from stdin
    input_text = sys.stdin.read().strip()
    
    try:
        # Use litellm to call gpt4.1-nano
        response = completion(
            model="gpt-4o-mini",  # Using actual model name
            messages=[{"role": "user", "content": input_text}],
            max_tokens=100
        )
        
        # Output the response
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 