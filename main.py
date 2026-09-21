import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
PRICE_ID = "price_1Q3C95I6UcxTsblZp8f55" # Your live price ID

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-checkout-session")
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': PRICE_ID, 'quantity': 1}],
            mode='payment',
            success_url="https://vercel.app",
            cancel_url="https://vercel.app",
        )
        return {"url": checkout_session.url}
    except Exception as e:
        return {"error": str(e)}

@app.post("/audit")
async def audit(file: UploadFile = File(...)):
    return {"total_waste": "320.00", "success_fee": "32.00"}
