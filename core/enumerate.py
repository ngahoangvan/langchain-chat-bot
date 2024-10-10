from enum import Enum


class EmbeddingModel(str, Enum):
    EMBEDDING_ADA_V2 = "text-embedding-ada-002"
    EMBEDDING_V3_LARGE = "text-embedding-3-large"
    EMBEDDING_V3_SMALL = "text-embedding-3-small"


class OpenAIModel(str, Enum):
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_4_0125_PREVIEW = "gpt-4-0125-preview"
    GPT_4O = "gpt-4o"
    GPT_4O_2024_05_13 = "gpt-4o-2024-05-13"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT_3_5_TURBO_0125 = "gpt-3.5-turbo-0125"


class DatabaseSchema(str, Enum):
    DEFAULT = "public"
    SHOPEE = "shopee"
