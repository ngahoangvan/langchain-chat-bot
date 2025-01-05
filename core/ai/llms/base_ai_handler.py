from abc import ABC, abstractmethod


class BaseAIHandler(ABC):
    """
    This class defines the interface for an AI handler to be used
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def invoke(self):
        pass
