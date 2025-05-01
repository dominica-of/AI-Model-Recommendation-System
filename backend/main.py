from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from backend.recommender import recommend_models_with_llm
f#rom backend.database import get_models_from_db
from backend.schemas import ModelInput

app = FastAPI()

@app.get("/recommend", summary="Get AI model recommendations")
def get_recommendations(
    input_data: str = Query(..., description="Input data type, e.g. Text, Image, Speech"),
    task: str = Query(..., description="Task type, e.g. Sentiment Analysis, Object Detection"),
    max_memory: Optional[int] = Query(None, description="Max RAM in GB"),
    allow_proprietary: Optional[bool] = Query(False, description="Include proprietary models")
):
    models = get_models_from_db()
    try:
        return recommend_models_with_llm(models, input_data, task, max_memory, allow_proprietary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))