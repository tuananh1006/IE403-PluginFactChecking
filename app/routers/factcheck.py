from fastapi import APIRouter
from app.models.schemas import FactCheckRequest, FactCheckResponse, FactCheckResult

router = APIRouter()

@router.post("/", response_model=FactCheckResponse)
async def full_fact_check(request: FactCheckRequest):
    claim = request.text
    evidence = ["Giả định bằng chứng"]
    label = "SUPPORTS"
    explanation = "Dựa trên bằng chứng, claim được xác nhận."
    result = FactCheckResult(claim=claim, evidence=evidence, label=label, explanation=explanation)
    return {"claims": [result]}
