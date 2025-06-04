from fastapi import FastAPI
from app.routers import factcheck, claim_detection, evidence_retrieval, veracity_prediction

app = FastAPI(title="Fact Check Editor API")

# Đăng ký các router
app.include_router(factcheck.router, prefix="/api/fact-check", tags=["Fact Check"])
app.include_router(claim_detection.router, prefix="/api/claim-detection", tags=["Claim Detection"])
app.include_router(evidence_retrieval.router, prefix="/api/evidence-retrieval", tags=["Evidence Retrieval"])
app.include_router(veracity_prediction.router, prefix="/api/veracity-prediction", tags=["Veracity Prediction"])

@app.get("/")
def home():
    return {"message": "Fact Check Editor API is running"}
