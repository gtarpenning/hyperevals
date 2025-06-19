#!/usr/bin/env python3

import argparse
import sys
from litellm import completion

PROMPT = """Score this LLM output given the input and expected output (if provided), 1-100. Only output the score.

Input: {input_text}
Model Output: {model_output}
Expected Output: {expected_output}"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-output", required=True, help="The model's output to score")
    parser.add_argument("--expected-output", required=False, default="", help="The expected output (optional)")
    args = parser.parse_args()
    
    # Read input text from stdin
    input_text = sys.stdin.read().strip()
    
    # Format the prompt with all available information
    content = PROMPT.format(
        input_text=input_text,
        model_output=args.model_output,
        expected_output=args.expected_output or "Not provided"
    )
    
    try:
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
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