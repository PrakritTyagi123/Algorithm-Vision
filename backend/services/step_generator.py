"""Service: Step Generator — utility for building step lists."""


class StepGenerator:
    """Helper for algorithms to record steps in a consistent format."""

    def __init__(self):
        self.steps = []

    def add(self, **kwargs):
        kwargs["step"] = len(self.steps) + 1
        self.steps.append(kwargs)

    def get_steps(self) -> list[dict]:
        return self.steps

    def reset(self):
        self.steps = []

    @property
    def count(self) -> int:
        return len(self.steps)
