# Evaluations

The `evals` library is an addition over the base `declarai` library that provides tools to track and benchmark
the performance of prompt strategies across models and providers.

We understand that a major challenge in the field of prompt engineering is the lack of a standardised way to evaluate
along with the continuously evolving nature of the field. As such, we have designed the `evals` library to be a lean
wrapper over the `declarai` library that allows users to easily track and benchmark changes in prompts and models.

### Usage

<div class="termy">

```console
$ python -m declarai.evals.evaluator
Running Extraction scenarios...
single_value_extraction... 
---> 100%
multi_value_extraction...
---> 100%
multi_value_multi_type_extraction...
---> 100%
...
Done!
```

</div>

### Evaluations
The output table will allow you to review the performance of your task across models and provides and make an informed
decision on which model and provider to use for your task.

| Provider | Model         | version | Scenario                         | runtime | <div style="width:290px">output</div>                                                                                                                                                        |
|:---------|:--------------|:--------|:---------------------------------|:--------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| openai   | gpt-3.5-turbo | latest  | generate_a_poem_no_metadata      | 1.235s  | Using LLMs is fun!                                                                                                                                                                           |
| openai   | gpt-3.5-turbo | 0301    | generate_a_poem_no_metadata      | 0.891s  | Using LLMs is fun! It's like playing with words Creating models that learn And watching them fly like birds                                                                                  | 
| openai   | gpt-3.5-turbo | 0613    | generate_a_poem_no_metadata      | 1.071s  | Using LLMs is fun!                                                                                                                                                                           |
| openai   | gpt-4         | latest  | generate_a_poem_no_metadata      | 3.494s  | {'poem': 'Using LLMs, a joyous run,\nIn the world of AI, under the sun.\nWith every task, they stun,\nIndeed, using LLMs is fun!'}                                                           |
| openai   | gpt-4         | 0613    | generate_a_poem_no_metadata      | 4.992s  | {'title': 'Using LLMs is fun!', 'poem': "With LLMs, the fun's just begun, \nCoding and learning, second to none. \nComplex tasks become a simple run, \nOh, the joy when the work is done!"} |
| openai   | gpt-3.5-turbo | latest  | generate_a_poem_only_return_type | 2.1s    | Learning with LLMs, a delightful run, Exploring new knowledge, it's never done. With every challenge, we rise and we stun, Using LLMs, the learning is always fun!                           |
