from enum import Enum


class ProvisionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

    def is_terminal(self) -> bool:
        return self in (ProvisionStatus.SUCCESS, ProvisionStatus.FAILED)
