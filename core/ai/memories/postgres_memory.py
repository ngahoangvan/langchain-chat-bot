
from langchain_community.chat_message_histories import SQLChatMessageHistory
from configs.common_config import settings
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from core.enumerate import OpenAIModel
from core.utils.common_utils import calculate_token
from langchain_core.messages import SystemMessage


class PostgresChatMemoryMessage:
    _instances = {}

    @classmethod
    def get_instance(cls, session_id: str) -> 'PostgresChatMemoryMessage':
        """Get or create a PostgresChatMemoryMessage instance for a given session ID.

        Args:
            session_id (str): Unique identifier for the chat session (e.g., Slack channel ID)

        Returns:
            PostgresChatMemoryMessage: Instance of the memory manager for the session
        """
        if session_id not in cls._instances:
            cls._instances[session_id] = cls(session_id)
        return cls._instances[session_id]

    def __init__(self, session_id: str) -> None:
        """Initialize a new PostgresChatMemoryMessage instance.

        Args:
            session_id (str): Unique identifier for the chat session
        """
        self.session_id = session_id
        self.message_history = SQLChatMessageHistory(
            session_id=session_id,
            connection_string=str(settings.DATABASE_URI),
        )
        self.memory = ConversationSummaryMemory(
            memory_key="chat_history",
            chat_memory=self.message_history,
            llm=ChatOpenAI(
                temperature=0,
                model=OpenAIModel.GPT_4O_MINI,
            ),
        )
        self._update_chat_history()

    def _update_chat_history(self) -> None:
        """Update the chat history and manage token limits.

        If the total token count exceeds 2000, summarize previous messages
        and keep only the summary plus the last two messages.
        """
        self.chat_history = self.message_history.messages
        self.token_count = [
            calculate_token(msg.content) for msg in self.chat_history[:-2]
        ]
        if sum(self.token_count) > 2000:
            prev_messages = self.chat_history[:-2]
            new_summary = self.memory.predict_new_summary(prev_messages, "")
            self.chat_history = [
                SystemMessage(content=new_summary),
                self.chat_history[-2],  # Last HumanMessage
                self.chat_history[-1],  # Last AIMessage
            ]
        else:
            self.chat_history = self.chat_history

    def get_chat_history(self) -> list:
        """Retrieve the current chat history.

        Returns:
            list: List of chat messages
        """
        self._update_chat_history()
        return self.chat_history

    def get_memory(self) -> ConversationSummaryMemory:
        """Get the ConversationSummaryMemory instance.

        Returns:
            ConversationSummaryMemory: The memory instance managing this chat
        """
        return self.memory
