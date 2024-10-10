from langfuse.callback import CallbackHandler as LangfuseCallbackHandler

from configs.common_config import settings


langfuse_callback = LangfuseCallbackHandler(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST,
)
