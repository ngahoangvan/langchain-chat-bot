from abc import ABC, abstractmethod


class Bot(ABC):

    @abstractmethod
    async def start(self):
        pass
