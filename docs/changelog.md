### v0.1.8

[View full release on GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.8) and [PyPi](https://pypi.org/project/declarai/0.1.8/)

Changes:

  - Dual support for DECLARAI_OPEN_AI_KEY and OPENAI_API_KEY.
  - Introduced support for pydantic description field.
  - Enabled Azure OpenAI LLM. Closes #67 and #72.
  - Default Azure API version fixed.

Contributors:

  - @helmanofer
  - @matankley
  - @shobhit9957

---
### v0.1.7

[View full release on GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.7) and [PyPi](https://pypi.org/project/declarai/0.1.7/)

**Improvements and Refactoring**

A major focus on refining API Reference docs and refactoring the internal structure of the project.

Changes:

  - Introduction of gpt-3.5-turbo-16k support.
  - Internal structure refactored and API reference generation in the docs.
  - Fixes and updates in documentation.

Contributors:

  - @helmanofer
  - @matankley

---


### v0.1.6

[View full release on GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.6) and [PyPi](https://pypi.org/project/declarai/0.1.6/)

**Bug Fix Release**

Changes:

  - Fixed chat greeting duplication bug. Closes #84.

Contributors:

  - @matankley

---

### v0.1.5

[View full release on GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.5) and [PyPi](https://pypi.org/project/declarai/0.1.5/)

**Extended Database Support**

In this update, Declarai extends its support to PostgreSQL, Redis, and MongoDB databases for saving chat message history.

Changes:

  - Support for PostgreSQL, Redis, and MongoDB databases to save chat messages. Closes #77.

Contributors:

  - @matankley

---

### v0.1.4

[View full release on GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.4) and [PyPi](https://pypi.org/project/declarai/0.1.4/)

**Introduction of Chat Memory**

Declarai now supports retaining message history across chat sessions, ensuring continuity and context.

Changes:

  - Removal of operator inheritance from llm params type.
  - Added chat memory to preserve message history between sessions. Closes #62.

Contributors:

  - @matankley

---


### v0.1.3

[View full release on GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.3) and [PyPi](https://pypi.org/project/declarai/0.1.3/)

**Enhanced Control Over LLM Params**

In this version, users gain the ability to finetune the parameters of the Language Model like temperature and max tokens. 

Changes:

  - Control the llm params such as temperature, max tokens, and more. Closes #54.
  - Deployment example with FastAPI for Declarai tasks added. Closes #63.
  - Support for passing LLM parameters directly to tasks. Closes #70.
  - Comprehensive documentation added for LLMParams control.
  - Updated package version.

Contributors:

  - @matankley

---


### v0.1.2

View full release on [GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.2) and [PyPi](https://pypi.org/project/declarai/0.1.2/)

**Minor bug fixes**

Changes:

  - Updates to documentation
  - Updates to dependencies with reported vulnerabilities
  - Fix typing and improve support for IDE autocompletion
  - Fix issue with initialization failing when passed the `openai_token` at runtime.




### v0.1.1

View full release on [GitHub](https://github.com/vendi-ai/declarai/releases/tag/v0.1.1) and [PyPi](https://pypi.org/project/declarai/0.1.1/)

**Announcing the first release of Declarai!** 🥳 🥳

Declarai was born out of the awe and excitement of LLMs, along with our passion for excellent engineering and real-world applications at scale.

We hope this project will help introduce more developers into the world of LLMs and enable them to more easily and reliably integrate these amazing capabilities into their production systems.

Main features:

  - Task interface
  - Chat interface
  - Middlewares
  - Exhaustive documentation
  - OpenAI support
  - LLM prompt best practices
