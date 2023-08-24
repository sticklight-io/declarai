# Evals
The evals library is a companion to declarai and helps us, and you, monitor prompts across models and over time.
We plan to run a suite of evaluations for every release of the package to ensure that changes in the prompt
infrastructure will not reduce the quality of results.

## Running the evaluations
To run the evaluations, you will need to install the `declarai` package. You can do this by running
```bash
pip install declarai
```

Once you have installed the package, you can run the evaluations by running
```bash
python -m evals.evaluator
```

After the evaluations have finished running, you should be able to view the results in your terminal:
```bash
Running Metadata-Significance scenarios...
generate_a_poem_no_metadata... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
generate_a_poem_only_return_type... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Provider        ┃ Model           ┃ version         ┃ Scenario                                 ┃ runtime    ┃ output                                                                                               ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ openai          │ gpt-3.5-turbo   │ latest          │ generate_a_poem_no_metadata              │ 1.235s     │ Using LLMs is fun!                                                                                   │
│ openai          │ gpt-3.5-turbo   │ 0301            │ generate_a_poem_no_metadata              │ 0.891s     │ Using LLMs is fun!                                                                                   │
│                 │                 │                 │                                          │            │ It's like playing with words                                                                         │
│                 │                 │                 │                                          │            │ Creating models that learn                                                                           │
│                 │                 │                 │                                          │            │ And watching them fly like birds                                                                     │
│ openai          │ gpt-3.5-turbo   │ 0613            │ generate_a_poem_no_metadata              │ 1.071s     │ Using LLMs is fun!                                                                                   │
│ openai          │ gpt-4           │ latest          │ generate_a_poem_no_metadata              │ 3.494s     │ {'poem': 'Using LLMs, a joyous run,\n In the world of AI, under the sun.\nWith every task, they       │
│                 │                 │                 │                                          │            │ stun,\nIndeed, using LLMs is fun!'}                                                                  │
│ openai          │ gpt-4           │ 0613            │ generate_a_poem_no_metadata              │ 4.992s     │ {'title': 'Using LLMs is fun!', 'poem': "With LLMs, the fun's just begun, \nCoding and learning,     │
│                 │                 │                 │                                          │            │ second to none. \nComplex tasks become a simple run, \nOh, the joy when the work is done!"}          │
│ openai          │ gpt-3.5-turbo   │ latest          │ generate_a_poem_only_return_type         │ 2.1s       │ Learning with LLMs, a delightful run,                                                                │
│                 │                 │                 │                                          │            │ Exploring new knowledge, it's never done.                                                            │
│                 │                 │                 │                                          │            │ With every challenge, we rise and we stun,                                                           │
│                 │                 │                 │                                          │            │ Using LLMs, the learning is always fun!                                                              │
│...              │...              │...              │...                                       │...         │ ...                                                                                                  │
└─────────────────┴─────────────────┴─────────────────┴──────────────────────────────────────────┴────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
