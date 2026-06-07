from fastapi import FastAPI

app = FastAPI(
    title="PaymentShield API",
    description="Security-focused payment intelligence platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "application": "PaymentShield",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }