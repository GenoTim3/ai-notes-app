from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import json

router = APIRouter()

# Request body
class SummarizeRequest(BaseModel):
    text: str

# Response body
class SummarizeResponse(BaseModel):
    summary: str

@router.post("/", response_model=SummarizeResponse)
def summarize_text(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="No text provided for summarization")
    
    try:
        # Run Ollama CLI with Llama 3
        result = subprocess.run(
            ["ollama", "generate", "llama3", request.text, "--json"], 
            capture_output=True, text=True, check=True
        )
        # Parse Ollama JSON output
        response_data = json.loads(result.stdout)
        summary_text = response_data.get("output", "").strip()
        
        if not summary_text:
            raise HTTPException(status_code=500, detail="Ollama returned no summary")

        return SummarizeResponse(summary=summary_text)
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Ollama CLI error: {e.stderr}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse Ollama response")
