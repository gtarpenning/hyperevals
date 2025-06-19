"""
Main evaluation class. 

Responsible for taking a config and running the evaluation. Runs the model file on the inputs and scores the outputs.
If the files are python, execute with python, otherwise just run the file. After every step, append output to a jsonl
output file corresponding to the run. Handle errors nicely. Progress bar. Very simple but nice Rich summary of the output.

Output shape:
| id | step | input | output | score |
|----|------|-------|--------|-------|
| 1  | 1    | "Hey, whats your name?" | "My name is John" | 0.95 |
| 1  | 2    | "What is your favorite color?" | "My favorite color is blue" | 0.95 |
| 1  | 3    | "What is your favorite food?" | "My favorite food is pizza" | 0.95 |
| 2  | 1    | "What is your name?" | "My name is John" | 0.95 |
| 2  | 2    | "Wow great!" | "..." | 0.95 |


Example config:
```yaml
dataset: /data/test.csv
model: /models/test.py
scorer: /scorers/scorer.py
eval_parallelism: 2
hyperband:
  min_examples: 10
  bands: [10, 20, 30, 40, 50]
```
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
from rich.console import Console
from rich.progress import Progress, TaskID

from .summary import print_summary

console = Console()


def run_script(script_path: str, input_text: str) -> Tuple[str, str]:
    """Run script and return (output, error_msg)."""
    try:
        if script_path.endswith(".py"):
            result = subprocess.run(
                [sys.executable, script_path],
                input=input_text,
                text=True,
                capture_output=True,
                timeout=30,
            )
        else:
            result = subprocess.run(
                [script_path],
                input=input_text,
                text=True,
                capture_output=True,
                timeout=30,
            )

        if result.returncode != 0:
            error_msg = f"Script failed with code {result.returncode}: {result.stderr}"
            return result.stdout.strip() if result.stdout else "", error_msg
        return result.stdout.strip(), ""
    except Exception as e:
        error_msg = f"Exception running script: {str(e)}"
        return "", error_msg


class Eval:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Generate timestamped output filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = f"eval-results-{timestamp}.jsonl"

    def _save_result(self, result: Dict[str, Any]):
        """Append result to JSONL file."""
        with open(self.output_file, "a") as f:
            f.write(json.dumps(result) + "\n")

    def run(self):
        """Run the evaluation."""
        # Load dataset
        df = pd.read_csv(self.config["dataset"])
        console.print(f"Loaded {len(df)} examples from {self.config['dataset']}")
        console.print(f"Output will be saved to: {self.output_file}")

        # Initialize output file
        Path(self.output_file).unlink(missing_ok=True)

        results = []

        with Progress() as progress:
            task = progress.add_task("Evaluating...", total=len(df))

            for idx, row in df.iterrows():
                example_id = idx + 1
                input_text = str(row.get("input", ""))

                # Run model
                model_output, model_error = run_script(self.config["model"], input_text)

                # Surface model errors to console
                if model_error:
                    console.print(
                        f"[red]Model error for example {example_id}: {model_error}[/red]"
                    )

                # Run scorer
                scorer_input = f"{input_text}\n---\n{model_output}"
                score_output, scorer_error = run_script(
                    self.config["scorer"], scorer_input
                )

                # Surface scorer errors to console
                if scorer_error:
                    console.print(
                        f"[yellow]Scorer error for example {example_id}: {scorer_error}[/yellow]"
                    )

                # Parse score
                try:
                    score = float(score_output) if score_output else 0.0
                except:
                    score = 0.0

                # Collect all errors
                errors = []
                if model_error:
                    errors.append(f"model: {model_error}")
                if scorer_error:
                    errors.append(f"scorer: {scorer_error}")

                # Save result
                result = {
                    "id": example_id,
                    "step": 1,
                    "input": input_text,
                    "output": model_output,
                    "score": score,
                    "errors": errors,
                }

                self._save_result(result)
                results.append(result)

                progress.advance(task)

        print_summary(results, self.output_file)
