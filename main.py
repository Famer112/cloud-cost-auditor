import os
import json
from typing import List
from openai import OpenAI
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# Initialize the OpenAI Client and Web Server
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptimizationStep(BaseModel):
    step_number: int
    resource_id: str
    provider: str
    issue_type: str
    current_monthly_cost: float
    potential_monthly_saving: float
    action_required: str

class CloudAuditReport(BaseModel):
    provider_detected: str
    total_monthly_spend: float
    total_waste_found: float
    your_success_fee_10_percent: float
    option_a_immediate_payment: float
    option_b_monthly_payment_installment: float
    optimization_steps: List[OptimizationStep]

@app.post("/audit", response_model=CloudAuditReport)
async def run_cloud_audit(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        raw_bill_data = contents.decode("utf-8")
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

    system_prompt = (
        "You are an expert Cloud FinOps AI Auditor. "
        "Analyze the provided raw cloud billing data, identify financial waste, and calculate precise math. "
        "Exclusions: Never suggest deleting active production databases or root boot disks.\n\n"
        "Mathematical Rules:\n"
        "1. Total Monthly Waste = Sum of all flagged wasteful line items\n"
        "2. Success Fee (10%) = Total Monthly Waste * 0.10\n"
        "3. Option A (Immediate Pay) = Success Fee * 0.90\n"
        "4. Option B (3-Month Installments) = Success Fee / 3"
    )

    response = client.beta.chat.completions.parse(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this raw JSON/CSV cloud billing data:\n\n{raw_bill_data}"}
        ],
        response_format=CloudAuditReport,
        temperature=0.1
    )
    
    return response.choices.message.parsed

if __name__ == "__main__":
    import uvicorn
    # This acts exactly like typing uvicorn main:app --reload into a terminal automatically
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

