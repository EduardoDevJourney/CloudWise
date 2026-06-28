from fastapi import APIRouter

from infra.http.dtos.api_dtos import HealthDTO

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthDTO)
def health() -> HealthDTO:
    return HealthDTO()
