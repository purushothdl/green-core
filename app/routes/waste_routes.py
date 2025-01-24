from fastapi import APIRouter, Depends, Form, UploadFile, File
from app.schemas.waste import WasteDisposalCreate, WasteDisposalResponse
from app.services.waste_service import WasteService
from app.dependencies.service_dependencies import get_waste_service
from app.dependencies.auth_dependencies import get_current_user
from app.core.google_cloud_storage import GoogleCloudStorage
from app.utils.gcs_utils import generate_unique_filename

router = APIRouter(prefix="/waste", tags=["waste"])

@router.post("/dispose", response_model=WasteDisposalResponse)
async def create_disposal(
    org_name: str = Form(...),
    waste_type: str = Form(...),
    weight: float = Form(...),
    photo: UploadFile = File(...),
    waste_service: WasteService = Depends(get_waste_service),
    gcs: GoogleCloudStorage = Depends(GoogleCloudStorage),
    current_user: dict = Depends(get_current_user),
):
    unique_filename = generate_unique_filename(photo.filename)

    photo_url = await gcs.upload_file(
        photo.file,
        f"green-core/disposals/{current_user.id}/{unique_filename}"
    )
    disposal = WasteDisposalCreate(
        org_name=org_name,
        waste_type=waste_type,
        weight=weight,
        photo_url=photo_url
    )
    return await waste_service.create_disposal(current_user.id, disposal)

@router.get("/history", response_model=list[WasteDisposalResponse])
async def get_disposal_history(
    waste_service: WasteService = Depends(get_waste_service),
    current_user: dict = Depends(get_current_user),
):
    return await waste_service.get_disposals_by_user(current_user.id)

@router.get("/stats")
async def get_waste_stats(
    waste_service: WasteService = Depends(get_waste_service),
    current_user: dict = Depends(get_current_user),
):
    return await waste_service.get_waste_stats(current_user.id)

@router.get("/graph")
async def get_weekly_waste_graph(
    waste_service: WasteService = Depends(get_waste_service),
    current_user: dict = Depends(get_current_user),
):
    return await waste_service.get_weekly_waste_data(current_user.id)