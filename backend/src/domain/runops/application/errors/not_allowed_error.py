class NotAllowedError(Exception):
    def __init__(self, action: str) -> None:
        self.action = action
        super().__init__(f"Not allowed: {action}")
