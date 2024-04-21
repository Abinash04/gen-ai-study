# Gen AI Case Study

## Overview

Vectorize the Frankendstein PDF book into the chromadb database. Use LLM to ask the defined question against the book. Use LLM to evaluate if the answer is sufficient.

Complete the tasks in the files and run the code, the evaluation should pass. Create a git commit for all code/config changes and zip entire folder contents, excluding venv/data folders. Also attach terminal text output of the execution.

## Environment Setup

Requirements:

- docker
- poetry
- vscode

## 1. Ingest (`./src/app/ingest.py`)

Instructions are in the file under the `TASK` comment.

## 2. Query (`./src/app/query.py`)

Instructions are in the file under the `TASK` comment.

## 3. Evaluate (`./src/app/evaluate.py`)

Instructions are in the file under the `TASK` comment.

## Local LLM Setup

The local LLM will run in docker of Ollama via the `./docker-compose.yml`.

```shell
docker compose up
```

In another terminal execute to install and run `llama2`.

```shell
docker exec -it ollama ollama run llama2
```

## Poetry Env

```shell
# Start poetry environment shell in terminal
poetry shell

# Install project dependencies
poetry install

# Run __main__.py
app run
```

## Terminal Text Output

1. **Initial Set up with Python3.12 and Poetry1.8.2**


<img width="1733" alt="image" src="https://github.com/Abinash04/gen-ai-study/assets/15240069/e6f25704-3c02-42a3-a689-138f22dad127">


2. **Ingesting Data**



<img width="1733" alt="image" src="https://github.com/Abinash04/gen-ai-study/assets/15240069/1a209ec3-259e-4c64-a806-c93765551db8">


3. **Initial Run without Yes or No Results**


<img width="1737" alt="image" src="https://github.com/Abinash04/gen-ai-study/assets/15240069/cafe78e5-7fbd-42a6-b8cc-82075962a822">



4. **Running LLM from Docker container - AWS EC2 instance using Iac (Terraform)**


<img width="1633" alt="image" src="https://github.com/Abinash04/gen-ai-study/assets/15240069/6e9909fd-090d-4e01-9aba-ac8880998118">


5. ***Final Result***


<img width="1730" alt="image" src="https://github.com/Abinash04/gen-ai-study/assets/15240069/baf571e2-2fa0-4833-a004-83dec5e54029">





