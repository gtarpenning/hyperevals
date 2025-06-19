# HyperEvals

Hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs.

## Motivation

Evaluating LLMs is both notoriously challenging and yet critical before confidently deploying in production environments. Seemingly small tweaks in prompts or upgrades to the model can have a significant impact on performance across various tasks, hence the need for carefully crafted evaluations. 

HyperEvals provides hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs, inspired by W&B's sweeps combined with hyperband optimization.

<img width="673" alt="image" src="https://github.com/user-attachments/assets/dd2c7745-4d1e-47c8-a083-382f6f62449b" />


## Installation

```bash
pip install hyperevals
```

For development installation:
```bash
git clone https://github.com/griffintarpenning/hyperevals.git
cd hyperevals
pip install -e ".[dev]"
```

## Quick Start

```bash
# Install the package
pip install hyperevals

# Run with a configuration file
hyperevals run config.yaml

# Show version
hyperevals --version
```

## Usage

### MVP Flow
1. Create a CSV dataset
2. Create a prompt template
3. Create an executable Model file
4. Create executable scorers 
5. Create a config file
6. Run the evaluation
7. Iterate on prompt and model parameters
8. Hyperband kills bad optimizations early
9. Final prompt is reported w/ accuracy

### Sample Configuration

```yaml
dataset: /data/test.csv
model: /models/test.py
scorer: /scorers/scorer.py
max_parallelism: 2  
hyperband:
  min_examples: 10
  bands: [10, 20, 30, 40, 50]
```

## TODO
- multi-step scorers for agent evals


Shape of the eval output:
| id | step | input | output | score |
|----|------|-------|--------|-------|
| 1  | 1    | "Hey, whats your name?" | "My name is John" | 0.95 |
| 1  | 2    | "What is your favorite color?" | "My favorite color is blue" | 0.95 |
| 1  | 3    | "What is your favorite food?" | "My favorite food is pizza" | 0.95 |
| 2  | 1    | "What is your name?" | "My name is John" | 0.95 |
| 2  | 2    | "Wow great!" | "..." | 0.95 |
