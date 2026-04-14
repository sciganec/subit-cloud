from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/classify")
def classify(data: dict):
    text = data.get("text", "")
    return {"subit_id": 0, "archetype_name": "test", "energy": 0.0, "axes": {}}