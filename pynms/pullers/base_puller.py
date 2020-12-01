from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class BasePuller(ABC):
    pulling_interval: int
    recivers: set

    @abstractmethod
    def start(address: str) -> None:
        pass
