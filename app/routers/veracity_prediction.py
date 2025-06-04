from fastapi import APIRouter
from app.models.schemas import VeracityRequest, VeracityResponse

router = APIRouter()

@router.post("/", response_model=VeracityResponse)
async def predict_veracity(request: VeracityRequest):
    return {
        "label": "REFUTES",
        "confidence": 0.95,
        "explanation": "Bằng chứng cho thấy claim không đúng."
    }
