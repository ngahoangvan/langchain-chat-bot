from core.ai.memories.postgres_memory import PostgresChatMemoryMessage


def get_chat_history(session_id):
    memory = PostgresChatMemoryMessage.get_instance(session_id=session_id)
    chat_history = memory.get_chat_history()
    return chat_history
