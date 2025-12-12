from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get(path="/", response_model=dict)
def root() -> dict:
    return {"message": "Spy Cat Agency API", "version": "1.0.0"}


@router.get(path="/health", response_model=dict)
def health_check() -> dict:
    return {"status": "healthy"}
