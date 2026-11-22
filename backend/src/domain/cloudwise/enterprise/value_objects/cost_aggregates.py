from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CostSeriesRow:
    period: str
    service: str
    total: float


@dataclass(frozen=True, slots=True)
class CostSummary:
    total_cost: float
    top_service: str
    subscription_count: int
