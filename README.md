

# AI-Driven SQL Chatbot with LangChain

## Overview

This project is a modular AI-powered SQL chatbot that converts natural language questions into SQL queries using semantic search and large language models. It connects with a PostgreSQL database and uses LangChain’s vector embeddings for context-aware query generation.

***

## Features

- Semantic search over database schema and sample data using LangChain
- AI-generated SQL queries via OpenRouter or OpenAI APIs
- Modular structure for scalability and easy maintenance
- Command-line interface for interactive querying
- Clean and informative result formatting

***

## File Structure

```
project_root/
│
├── chatbot/
│   ├── __init__.py
│   ├── config.py
│   ├── db_connection.py
│   ├── schema_loader.py
│   ├── vector_store.py
│   ├── query_generator.py
│   ├── query_executor.py
│   ├── utils.py
│   └── chatbot.py
│
└── main.py
```

***

## Installation and Setup

### 1. Clone the repository or create project directory

```bash
mkdir sql_bot
cd sql_bot
```

### 2. Create and activate a virtual environment

- On Windows:

```bash
python -m venv chatbot_env
chatbot_env\Scripts\activate
```

- On macOS/Linux:

```bash
python -m venv chatbot_env
source chatbot_env/bin/activate
```

### 3. Upgrade pip (optional)

```bash
python -m pip install --upgrade pip
```

### 4. Install dependencies

Create a `requirements.txt` file with the following content:

```
psycopg2
pandas
requests
langchain
chromadb
langchain-community
openai
sentence-transformers
```

Then install packages:

```bash
pip install -r requirements.txt
```

***

## Configuration

Edit `chatbot/config.py` and update the following:

- PostgreSQL DB connection parameters (host, port, database, user, password)
- API keys for OpenRouter or OpenAI

***

## Running the Chatbot

Execute the following command to start the chatbot CLI:

```bash
python main.py
```

***

## Usage

Type natural language queries about your database and get real-time SQL-generated answers.

Examples:

- `Count of passengers`
- `List all tables`
- `Show students studying Machine Learning`

***

## Optional: Save and Reuse Dependencies

Export installed packages:

```bash
pip freeze > requirements.txt
```

Reinstall later using:

```bash
pip install -r requirements.txt
```

***

