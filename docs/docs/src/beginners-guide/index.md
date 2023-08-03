# Tutorial - Beginners guide

This tutorial is a step-by-step guide to using **Declarai**. It walks you through the most basic features of the library.

Each section gradually builds on the previous one while sections are structured by topic, 
so that you can skip to whichever part is relevant to you. 

## Before we start

If you haven't already, install the Declarai library as follows:

```bash
$ pip install declarai
```
!!! info

    For this tutorial you will need an openai token. This token is completely your's and is not shared, stored or managed
    anywhere but on your machine! you can see more information about obtaining a token here: [openai](/declarai/src/providers/openai/)

After installation, open a python file and start with setting up your declarai app:

Once completed, the rest of the examples in this module should be as simple as copy/paste.



```python title="declarai_tutorial.py"
from declarai import Declarai

declarai = Declarai(provider="openai", model="gpt-3.5-turbo", openai_token="<your-openai-token>")
```


!!! info

     Do your best to copy, run and edit the code in your editor to really understand how powerful Declarai is.

<div style="text-align: center">
    <a href="simple-task/" class="md-button">
        Lets go! <i class="fas fa-arrow-left"></i>
    </a>
</div>

## Advanced User Guide

If you feel this tutorial is too easy, feel free to jump to our [**Advanced**](../advanced/) section, which covers more complex 
topics like middlewares, running evaluations and building multi provider flows.

We recommend you to read the tutorial first, and then the advanced guide if you want to learn more.