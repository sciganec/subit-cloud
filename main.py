# subit_api_simple.py
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from collections import defaultdict
import uvicorn

# ... (вставити функції heuristic_text_to_subit, compute_energy, subit_to_axes, MARKERS, CATEGORY_TO_BITS – ті самі, що й раніше)

app = FastAPI(title="SUBIT Classifier API", version="1.0")

class ClassifyRequest(BaseModel):
    text: str

class ClassifyResponse(BaseModel):
    subit_id: int
    archetype_name: str
    energy: float
    axes: Dict[str, str]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/classify", response_model=ClassifyResponse)
async def classify(request: ClassifyRequest):
    subit_vec = heuristic_text_to_subit(request.text)
    energy = compute_energy(subit_vec)
    axes = subit_to_axes(subit_vec)
    bits = (subit_vec > 0).astype(int)
    subit_id = 0
    for i, b in enumerate(reversed(bits)):
        subit_id |= (b << i)
    # Спрощене ім'я архетипу (без subit_to_name)
    archetype_name = f"Archetype {subit_id}"
    return ClassifyResponse(
        subit_id=subit_id,
        archetype_name=archetype_name,
        energy=energy,
        axes=axes
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)