from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.admin_service import AdminService

# Initialize router
router = APIRouter()

# Admin Controls
@router.get("/admin/survey_responses", response_model=List[Dict[str, Any]])
async def get_all_survey_responses():
    """Retrieve all survey responses."""
    return await AdminService.get_all_survey_responses()

@router.get("/admin/surveys", response_model=List[Dict[str, Any]])
async def get_all_surveys():
    """Retrieve all surveys."""
    return await AdminService.get_all_surveys()

@router.post("/admin/surveys")
async def create_survey(survey_data: Dict[str, Any]):
    """Create a new survey."""
    return await AdminService.create_survey(survey_data)

@router.put("/admin/surveys/{survey_id}")
async def update_survey(survey_id: str, survey_data: Dict[str, Any]):
    """Update an existing survey."""
    return await AdminService.update_survey(survey_id, survey_data)

@router.delete("/admin/surveys/{survey_id}")
async def delete_survey(survey_id: str):
    """Delete a survey."""
    return await AdminService.delete_survey(survey_id)
