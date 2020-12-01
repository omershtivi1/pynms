from dataclasses import dataclass


# TODO move to Set, and obj pullers, listeners
@dataclass
class Device:
    target: str
    pullers: set
    listeners: set

    @classmethod
    def load(cls, target: str):
        return cls(target, {})

    def add_puller(self, puller) -> None:
        self.pullers.add(puller)

    def add_listener(self, listener) -> None:
        self.listeners.add(listener)

    def start(self) -> None:
        for puller in self.pullers:
            puller.start(self.target)
