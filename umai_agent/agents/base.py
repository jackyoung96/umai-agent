from swarm import Agent

class BaseAgent(Agent):
    def __init__(self, name: str, instructions: str):
        super().__init__(name, instructions)

    def __doc__(self):
        return self.instructions

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls(*args, **kwargs)
