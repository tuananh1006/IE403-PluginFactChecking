from typing import List, Optional
from pydantic import BaseModel

class ClaimRequest(BaseModel):
    text: str
    lang: Optional[str] = "vi"

class ClaimResponse(BaseModel):
    claims: List[str]

class EvidenceRequest(BaseModel):
    claim: str
    lang: Optional[str] = "vi"

class EvidenceResponse(BaseModel):
    evidence: List[str]

class VeracityRequest(BaseModel):
    claim: str
    evidence: List[str]

class VeracityResponse(BaseModel):
    label: str
    confidence: float
    explanation: Optional[str]

class FactCheckRequest(BaseModel):
    text: str
    lang: Optional[str] = "vi"

class FactCheckResult(BaseModel):
    claim: str
    evidence: List[str]
    label: str
    explanation: Optional[str]

class FactCheckResponse(BaseModel):
    claims: List[FactCheckResult]
