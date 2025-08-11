def process_claim(text: str):
    """
    Placeholder AI claim evaluator.
    Pretends to run the text through an AI and returns a dummy verdict.
    """
    if "flood" in text.lower():
        return {"analysis": "Claim approved with moderate confidence", "confidence": 0.85, "approved": True}
    else:
        return {"analysis": "Claim needs manual review", "confidence": 0.6, "approved": False}




