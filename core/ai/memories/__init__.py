from langchain_core.messages import BaseMessage

from langchain_community.chat_message_histories import SQLChatMessageHistory
from configs.common_config import settings
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from core.enumerate import OpenAIModel
from core.utils.common_utils import calculate_token
from langchain_core.messages import SystemMessage


def get_message_history(session_id: str) -> tuple[list[BaseMessage], ConversationSummaryMemory]:
    message_history = SQLChatMessageHistory(
        session_id=session_id,
        connection_string=str(settings.DATABASE_URI),
    )
    memory = ConversationSummaryMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        llm=ChatOpenAI(
            temperature=0,
            model=OpenAIModel.GPT_4O_MINI,
        )
    )
    historical_messages = memory.chat_memory.messages
    token_count = [
        calculate_token(msg.content) for msg in historical_messages[:-2]
    ]
    if sum(token_count) > 2000:
        prev_messages = historical_messages[:-2]
        new_summary = memory.predict_new_summary(prev_messages, "")
        chat_history = [
            SystemMessage(content=new_summary),
            historical_messages[-2], # Last HumanMessage
            historical_messages[-1] # Last AIMessage
        ]
    else:
        chat_history = historical_messages
    
    return chat_history, memory
