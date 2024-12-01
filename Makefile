.PHONY: run-bot run-api

# Default Python command
PYTHON = poetry run python

# Run the bot
run-bot:
	@bash -c "start-bot.sh"

# Run the API
run-api:
	@bash -c "start-uvicorn.sh"

# Help command to list available targets
help:
	@echo "Available commands:"
	@echo "  run-bot  - Run the chatbot"
	@echo "  run-api  - Run the API server"
