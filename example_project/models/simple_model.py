#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from litellm import completion

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="Path to prompt file")
    args, _ = parser.parse_known_args()
    
    # Read input from stdin
    input_text = sys.stdin.read().strip()
    
    # Read prompt if provided
    prompt_text = ""
    if args.prompt and Path(args.prompt).exists():
        with open(args.prompt, 'r') as f:
            prompt_text = f.read().strip()
    
    try:
        # Prepare messages
        messages = []
        if prompt_text:
            messages.append({"role": "system", "content": prompt_text})
        messages.append({"role": "user", "content": input_text})
        
        # Use litellm to call gpt4-mini
        response = completion(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100
        )
        
        # Output the response
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 