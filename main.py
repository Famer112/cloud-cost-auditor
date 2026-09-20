@app.get("/")
def home():
    return {"status": "healthy", "message": "Multi-Cloud AI Cost Auditor Backend Online"}
