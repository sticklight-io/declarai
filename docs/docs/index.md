<p align="center">
  <a href="https://localhost:8000"><img src="./img/Logo-declarai.svg" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Declarai, turning Python functions into LLM tasks, easy to use, and production-ready.</em>
</p>

---

## Introduction

Declarai turns your Python functions into LLM tasks, utilizing your function's details, like type hints and docstrings,
to instruct an AI model on what to do. Simply put, you write Python code as you normally would, and Declarai empowers it
with AI capabilities.

Designed with a clear focus on developer experience, Declarai allows you to write Python code as you normally would,
instead of crafting complex LLM prompts.

---

## The Key Features

- ** Pythonic Interface to LLM:** - Leverage python expertise instead of working hard crafting prompts.

- ** Type-Guided Prompt Engineering:** - Using Python's type annotations, Declarai crafts precise prompts that guide
  LLMs towards the expected output type. This reduces potential misunderstandings and boosts the consistency of AI
  outputs.

- ** Contextual Prompts through Docstrings:** - Use function docstrings to provide contextual information to LLMs,
  enhancing their understanding of the task at hand and improving their performance.

- ** Automated LLM Task Execution:** - Feeding prompts to the LLM, collecting and processing responses is seamlessly
  automated, reducing boilerplate and focusing on core application logic.

This approach enhances code readability, maintainability, and predictability

---

## Installation

<div class="termy">

```console
$ pip install declarai

---> 100%
Done!
```

</div>


---

## Examples

<br>
#### Extract Phone Numbers

In this example, we define a task to extract phone numbers from a given email content.

* Create a file named `extract_phone_number.py` and add the following code:

    ```Python
    from declarai import task
    
    @task
    def extract_phone_number(email: str) -> List[str]:
        """
        Extract the phone number from the provided email
        :param email: email content
        :return: The phone numbers that are used in the email
        """
        return magic(email)
    
    res = extract_phone_number(
        email="Hello, my phone number is 123456789. What's yours?"
        )
    
    print(f"Phone numbers: {res}")
    ```

* Run the file:

    <div class="termy">
    
        ```console
        $ python extract_phone_number.py
        
        Phone numbers: [123456789]
        ```
    
    </div>




