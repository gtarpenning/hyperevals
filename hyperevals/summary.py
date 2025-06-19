"""
Summary display functionality for evaluation results.
"""

from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


def print_summary(results: List[Dict[str, Any]], output_file: str):
    """Print evaluation summary with stats and examples."""
    if not results:
        console.print("No results to summarize.")
        return

    scores = [r["score"] for r in results if isinstance(r["score"], (int, float))]
    avg_score = sum(scores) / len(scores) if scores else 0

    # Count errors
    error_count = sum(1 for r in results if r.get("errors"))
    has_errors = error_count > 0

    print("\n\n")

    # Stats table
    stats_table = Table(title="Evaluation Summary")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")

    stats_table.add_row("Total Examples", str(len(results)))
    stats_table.add_row("Average Score", f"{avg_score:.3f}")
    stats_table.add_row("Examples with Errors", str(error_count))
    stats_table.add_row("Output File", output_file)

    console.print(stats_table)

    # Examples table
    print("\n")
    examples_table = Table(title="Sample Results")
    examples_table.add_column("ID", style="dim", width=4)
    examples_table.add_column("Input", style="white", width=30)
    examples_table.add_column("Output", style="blue", width=40)
    examples_table.add_column("Score", style="green", width=8)

    # Add errors column only if there are errors
    if has_errors:
        examples_table.add_column("Errors", style="red", width=30)

    # Select examples: mix of high/low scores and errors
    selected_examples = _select_examples(results, max_examples=8)

    for example in selected_examples:
        # Truncate long text
        input_text = _truncate_text(example["input"], 40)
        output_text = _truncate_text(example["output"], 60)

        row_data = [
            str(example["id"]),
            input_text,
            output_text,
            f"{example['score']:.2f}",
        ]

        # Add errors column if needed
        if has_errors:
            error_text = (
                "; ".join(example.get("errors", [])) if example.get("errors") else ""
            )
            error_text = _truncate_text(error_text, 40)
            row_data.append(error_text)

        examples_table.add_row(*row_data)

    console.print(examples_table)


def _select_examples(
    results: List[Dict[str, Any]], max_examples: int = 8
) -> List[Dict[str, Any]]:
    """Select a mix of high/low scoring examples and error examples."""
    if len(results) <= max_examples:
        return results

    # Sort by score
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    # Get examples with errors
    error_examples = [r for r in results if r.get("errors")]

    # Get high scoring examples (top half)
    high_scoring = sorted_results[: len(sorted_results) // 2]

    # Get low scoring examples (bottom half)
    low_scoring = sorted_results[len(sorted_results) // 2 :]

    selected = []

    # Add some error examples first (up to 2)
    selected.extend(error_examples[:2])

    # Add high scoring examples
    remaining = max_examples - len(selected)
    high_count = min(remaining // 2, len(high_scoring))
    selected.extend(high_scoring[:high_count])

    # Add low scoring examples
    remaining = max_examples - len(selected)
    low_count = min(remaining, len(low_scoring))
    selected.extend(low_scoring[:low_count])

    # Remove duplicates while preserving order
    seen = set()
    unique_selected = []
    for item in selected:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique_selected.append(item)

    return unique_selected[:max_examples]


def _truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max_length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
