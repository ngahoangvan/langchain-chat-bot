.PHONY: run-bot run-api

# Default Python command
PYTHON = python3

# Run the bot
run-bot:
	$(PYTHON) src/bot/main.py

# Run the API
run-api:
	$(PYTHON) src/api/app.py

# Help command to list available targets
help:
	@echo "Available commands:"
	@echo "  run-bot  - Run the chatbot"
	@echo "  run-api  - Run the API server"