# Build ChatBot with Langchain and FastAPI

This project aim to devvelop a chatbot for multiple platform like Slack, Google Chat, MS Team,...

## List supported platform

- [x] Slack
- [ ] MS Team
- [ ] Google Chat
- [ ] Telegram

## Installation
### Pre-requisite
- Python 3.10+
- Poetry

### Create your python virtual environment
Some virtualenv you can follow. In this project, I'm using poetry.

- With poetry
```bash
# Clone the project
$ git clone https://github.com/ngahoangvan/langchain-chat-bot.git

# Go to project
$ cd langchain-chat-bot

# Install pipenv from pip
$ poetry install

# Activate your virtual environment
$ poetry shell

# verify the virtual environment
$ poetry env info

```

### Install and running project

```bash
# Create .env file
$ cp .env.example .env

# Create migration
$ alembic revision --autogenerate -m "your_message"

# Apply migration file
$ alembic upgrade head

# Run server
$ fastapi dev main.py

# Run your bot
$ python bot.py
```

## Folder Structure
```bash
```bash
.
├── Dockerfile           # Docker configuration file for containerizing the application
├── Makefile             # Makefile for automating tasks
├── README.md            # Project documentation
├── alembic.ini          # Alembic configuration file for database migrations
├── bot.py               # Main script to run the chatbot
├── celery_task          # Folder containing Celery tasks for asynchronous processing
├── configs              # Configuration files for the project
├── core                 # Core application logic
│   ├── ai               # AI-related functionalities
│   ├── bot              # Bot-related functionalities
│   ├── callbacks        # Callback functions
│   ├── constants.py     # Constant values used across the project
│   ├── databases        # Database-related functionalities
│   ├── decorators       # Custom decorators
│   ├── enumerate.py     # Enumerations used in the project
│   ├── exceptions       # Custom exception handling
│   ├── loggers          # Logging configurations and utilities
│   ├── services         # Service layer for business logic
│   └── utils            # Utility functions
├── docker-compose.yaml  # Docker Compose file for the project
├── hishel_cache.db      # Cache database file
├── logging.ini          # Logging configuration file
├── main.py              # Entry point for the FastAPI server
├── migrations           # Database migration scripts
├── notebooks            # Jupyter notebooks for experiments and documentation
├── poetry.lock          # Poetry lock file for dependencies
├── pyproject.toml       # Poetry configuration file
├── scripts              # Utility scripts
└── test.py              # Test script
```

## TODO list
- [x] Use Langchain to create an AI agent
- [x] Create a list of tools
- [x] Slack Chatbot
- [ ] Create Unit Test
- [ ] Refactor Code
