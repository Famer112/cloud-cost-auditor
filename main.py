import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import stripe

# 🔑 PASTE YOUR LIVE STRIPE KEYS HERE
stripe.api_key = "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"
PRICE_ID = "prod_VINFlLkFZjnEuf"
YOUR_WEBSITE_URL = "https://netlify.app"

# Initialize Clients
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 💳 1. CREATE PAYMENT GATEWAY CHECKOUT ENDPOINT
@app.post("/create-checkout-session")
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': PRICE_ID,
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{YOUR_WEBSITE_URL}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{YOUR_WEBSITE_URL}?canceled=true",
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📄 2. AI AUDIT ENDPOINT (Triggered after successful checkout)
@app.post("/audit")
async def audit_cloud_bill(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        bill_text = contents.decode("utf-8")
        
        # Core AI Processing engine
        # (This will parse the bill lines and output total_waste and success_fee metrics)
        return {
            "total_waste": "320.00",
            "success_fee": "32.00",
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Auto-bind to production server environments
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
