class PolicyViolationError(Exception):
    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        super().__init__("Policy violation: " + "; ".join(violations))
