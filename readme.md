# HyperEvals

## Motivation

Evaluating LLMS is both notoriously challenging and yet critical before confidently deploying in production environments. Seemingly small tweaks in prompt or upgrades to the model can have a significant impact on the performance at various tasks, hence the need for carefully crafted evaluations. HyperEvals provides hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs.

Inspired by W&B's sweeps + hyperband. 

MVP flow
- Create a csv dataset
- Create a prompt template
- Create an executable Model file
- Create executable scorers 
- Create a config file


Sample config

```yaml
dataset: /data/test.csv
prompt_template: /prompts/test.txt
model: /models/test.py
scorers:
  - scorer1: /scorers/scorer1.py
  - scorer2: /scorers/scorer2.py
hyperband:
  min_examples: 10
  bands: [10, 20, 30, 40, 50]
```
