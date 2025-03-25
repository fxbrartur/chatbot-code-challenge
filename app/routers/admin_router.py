from fastapi import APIRouter, HTTPException
from app.db import MockRPCDatabase
from app.utils.rpc_retrier_wrapper import RPCRetrier
from typing import List, Dict, Any

# Initialize router, database, and retrier
router = APIRouter()
db = MockRPCDatabase()
retrier = RPCRetrier(max_retries=3, retry_delay=1)

# Admin Controls
@router.get("/admin/survey_responses", response_model=List[Dict[str, Any]])
async def get_all_survey_responses():
    """Retrieve all survey responses."""
    try:
        return await retrier.call(db.get_all_survey_responses)
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to retrieve survey responses due to RPC error.")

@router.get("/admin/surveys", response_model=List[Dict[str, Any]])
async def get_all_surveys():
    """Retrieve all surveys."""
    try:
        return await retrier.call(db.get_all_surveys)
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to retrieve surveys due to RPC error.")

@router.post("/admin/surveys")
async def create_survey(survey_data: Dict[str, Any]):
    """Create a new survey."""
    try:
        survey_id = survey_data.get("survey_id")
        if not survey_id:
            raise HTTPException(status_code=400, detail="Survey ID is required.")
        existing_survey = await retrier.call(db.get_survey_info, survey_id)
        if existing_survey:
            raise HTTPException(status_code=400, detail="Survey with this ID already exists.")
        await retrier.call(db.create_survey, survey_id, survey_data)
        return {"message": "Survey created successfully."}
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to create survey due to RPC error.")

@router.put("/admin/surveys/{survey_id}")
async def update_survey(survey_id: str, survey_data: Dict[str, Any]):
    """Update an existing survey."""
    try:
        existing_survey = await retrier.call(db.get_survey_info, survey_id)
        if not existing_survey:
            raise HTTPException(status_code=404, detail="Survey not found.")
        await retrier.call(db.update_survey, survey_id, survey_data)
        return {"message": "Survey updated successfully."}
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to update survey due to RPC error.")

@router.delete("/admin/surveys/{survey_id}")
async def delete_survey(survey_id: str):
    """Delete a survey."""
    try:
        existing_survey = await retrier.call(db.get_survey_info, survey_id)
        if not existing_survey:
            raise HTTPException(status_code=404, detail="Survey not found.")
        await retrier.call(db.delete_survey, survey_id)
        return {"message": "Survey deleted successfully."}
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to delete survey due to RPC error.")

@router.delete("/admin/survey_responses/{response_id}")
async def delete_survey_response(response_id: str):
    """Delete a specific survey response."""
    try:
        deleted = await retrier.call(db.delete_survey_response, response_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Survey response not found.")
        return {"message": "Survey response deleted successfully."}
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to delete survey response due to RPC error.")