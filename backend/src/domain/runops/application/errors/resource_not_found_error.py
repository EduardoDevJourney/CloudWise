class ResourceNotFoundError(Exception):
    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}")


class NotAllowedError(Exception):
    def __init__(self, action: str) -> None:
        self.action = action
        super().__init__(f"Not allowed: {action}")
