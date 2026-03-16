# MindGlow Chatbot

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-0A9F6E?logo=openai&logoColor=white)
![Interface](https://img.shields.io/badge/Interface-CLI-1F6FEB)
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey)

MindGlow is a dual-chatbot system designed for reflective conversations and structured learning.

- `ReflectBot`: emotionally supportive, non-directive reflection with option-based deepening.
- `InnerLearningBot`: detailed educational responses with structured explanations.

This repository is currently optimized for backend handoff: core bot logic, shared filters, and memory utility modules are isolated and easy to integrate into an API layer.

## Contents

- [What This Project Includes](#what-this-project-includes)
- [Current Architecture](#current-architecture)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Run the Chatbots](#run-the-chatbots)
- [Use as Python Modules](#use-as-python-modules)
- [Response Contracts](#response-contracts)
- [Environment Variables](#environment-variables)
- [Backend Integration Notes](#backend-integration-notes)
- [Safety Notes](#safety-notes)
- [Troubleshooting](#troubleshooting)

## What This Project Includes

### 1) ReflectBot (`chatbot_reflect.py`)
- Uses OpenAI chat completions for reflective dialogue.
- Applies language detection and matches output language to the user.
- Applies directive filtering (`check_for_directives`) and retries up to 2 times.
- Performs crisis detection and returns localized crisis resources when triggered.
- Supports direct CLI run (`python chatbot_reflect.py`).

### 2) InnerLearningBot (`chatbot_learning.py`)
- Uses OpenAI chat completions for detailed educational responses.
- Applies language detection and crisis detection.
- Supports direct CLI run (`python chatbot_learning.py`).

### 3) Shared Utilities
- `config.py`: environment settings, system prompts, static profile, crisis resources.
- `filters.py`: language detection, directive phrase detection, crisis phrase detection.
- `memory.py`: embedding generation and semantic ranking helpers.
- `models.py`: Pydantic models used by memory utilities.
- `youtube_search.py`: standalone YouTube Data API search helper module.

Note: the `youtube_search.py` demo `main()` currently uses an inline API key constant; replace it with your own key handling before production use.

## Current Architecture

```text
MindGlow-Chatbot/
|- chatbot_reflect.py
|- chatbot_learning.py
|- config.py
|- filters.py
|- memory.py
|- models.py
|- youtube_search.py
|- requirements.txt
|- .env.example
`- README.md
```

## Requirements

- Python 3.12+
- OpenAI API key
- Internet connection for OpenAI API calls

Dependencies are listed in `requirements.txt`:

- `openai`
- `pydantic-settings`
- `python-dotenv`
- `numpy`
- `langdetect`
- `requests`

## Quick Start

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables

Copy `.env.example` to `.env`, then set at least your OpenAI key:

```env
OPENAI_API_KEY=your-openai-api-key
```

## Run the Chatbots

From the project directory:

```bash
python chatbot_reflect.py
python chatbot_learning.py
```

Interactive commands in both CLIs:

- `reset` clears conversation history.
- `quit` exits the chatbot.

## Use as Python Modules

```python
from chatbot_reflect import ReflectBot
from chatbot_learning import InnerLearningBot

reflect = ReflectBot()
learning = InnerLearningBot()

reflect_result = reflect.chat("I feel overwhelmed today")
print(reflect_result["reply"])

learning_result = learning.chat("Explain neural networks in simple terms")
print(learning_result["reply"])
```

## Response Contracts

### ReflectBot response (`ReflectBot.chat`)

Possible keys:

- `reply` (`str`)
- `language` (`str`)
- `crisis_detected` (`bool`)
- `was_filtered` (`bool`)
- `filter_reason` (`str | None`)
- `turn` (`int`, non-crisis path)
- `crisis_resources` (`str`, crisis path)
- `crisis_indicators` (`list[str]`, crisis path)

### InnerLearningBot response (`InnerLearningBot.chat`)

Possible keys:

- `reply` (`str`)
- `language` (`str`)
- `crisis_detected` (`bool`)
- `crisis_resources` (`str`, crisis path)
- `crisis_indicators` (`list[str]`, crisis path)

## Environment Variables

Defined in `config.py` (`Settings`):

- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (default: `gpt-4o`)
- `EMBEDDING_MODEL` (default: `text-embedding-3-small`)
- `MAX_CONTEXT_MESSAGES` (default: `20`)
- `SIMILARITY_THRESHOLD` (default: `0.75`)
- `YOUTUBE_API_KEY` (optional)

## Backend Integration Notes

- The bots currently keep conversation history in-memory (`self.conversation_history`).
- `memory.py` is computation-only; persistence should be implemented in backend storage.
- `models.py` provides typed contracts for stored messages and semantic search results.
- `config.py` currently contains a static user profile; backend can replace this with dynamic profile injection.

## Safety Notes

- Crisis phrase detection is implemented in `filters.py` and used in both bots.
- ReflectBot includes non-directive response filtering to reduce advice-like output.
- This is not a crisis intervention service. In production, always provide region-appropriate emergency escalation paths.

## Troubleshooting

### `did not find executable ...` when running Python in `.venv`

Your virtual environment may reference a stale interpreter path. Recreate it:

```powershell
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Verify active Python version

```bash
python --version
```

Expected: `Python 3.12.x`

## License

No license file is currently included in this repository. Add a license before public redistribution.
