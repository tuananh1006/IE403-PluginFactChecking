from fastapi import APIRouter
from app.models.schemas import EvidenceRequest, EvidenceResponse

router = APIRouter()

@router.post("/", response_model=EvidenceResponse)
async def retrieve_evidence(request: EvidenceRequest):
    dummy_evidence = ["Bằng chứng 1 cho: " + request.claim]
    return {"evidence": dummy_evidence}
