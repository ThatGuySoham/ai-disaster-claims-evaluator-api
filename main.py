# main.py
import uuid
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, constr
from typing import Optional, List
from utils.doc_parser import parse_doc
from utils.llm_query import process_claim as llm_process_claim
from utils.vector_store import store_chunks  # should return a policy_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("claim-evaluator")

app = FastAPI(
    title="AI Disaster Claim Processor",
    description="API for automated insurance claim validation",
    version="1.0"
)

class Claim(BaseModel):
    text: constr(min_length=10, max_length=1000)

class UploadResponse(BaseModel):
    message: str
    chunks_processed: int
    policy_id: Optional[str] = None

class ClaimResponse(BaseModel):
    result: str
    confidence_score: Optional[float] = None
    is_approved: Optional[bool] = None

@app.post(
    "/upload-policy/",
    response_model=UploadResponse,
    summary="Upload policy document",
    responses={
        400: {"description": "Invalid file type"},
        413: {"description": "File too large"},
        422: {"description": "No text extracted"},
        500: {"description": "Processing error"}
    }
)
async def upload_policy(file: UploadFile = File(..., description="Policy document (PDF or DOCX)")):
    """Upload a policy document (PDF / DOCX). Returns number of chunks and policy_id."""
    allowed = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    }
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Only PDF / DOCX / DOC files allowed")

    try:
        content = await file.read()
        if len(content) > 10_000_000:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")

        chunks = parse_doc(content)
        if not chunks:
            raise HTTPException(status_code=422, detail="No text could be extracted from the document")

        # store_chunks should return an id. If not, generate one here.
        policy_id = store_chunks(chunks)
        if not policy_id:
            policy_id = str(uuid.uuid4())

        return {
            "message": "Policy processed successfully",
            "chunks_processed": len(chunks),
            "policy_id": policy_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload policy failed")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post(
    "/process-claim/",
    response_model=ClaimResponse,
    summary="Evaluate a claim text",
    responses={500: {"description": "Claim analysis failed"}}
)
async def analyze_claim(claim: Claim):
    """Analyze claim text using the LLM helper and return verdict + confidence."""
    try:
        result = llm_process_claim(claim.text)
        # Expect result to be a dict like {"analysis": "...", "confidence": 0.9, "approved": True}
        return {
            "result": result.get("analysis", "No analysis returned"),
            "confidence_score": result.get("confidence"),
            "is_approved": result.get("approved")
        }
    except Exception as e:
        logger.exception("Claim analysis failed")
        raise HTTPException(status_code=500, detail=f"Claim analysis failed: {str(e)}")

