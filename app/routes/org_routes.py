from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app.core.google_cloud_storage import GoogleCloudStorage
from app.dependencies.auth_dependencies import get_current_user
from app.schemas.orgs import OrgCreate, OrgResponse
from app.services.org_service import OrgService
from app.dependencies.service_dependencies import get_org_service
from app.utils.gcs_utils import generate_unique_filename

router = APIRouter(prefix="/orgs", tags=["orgs"])

@router.post("/", response_model=OrgResponse)
async def create_org(
    org: OrgCreate,
    org_service: OrgService = Depends(get_org_service),
):
    return await org_service.create_org(org)

@router.get("/{org_id}", response_model=OrgResponse)
async def get_org(
    org_id: str,
    org_service: OrgService = Depends(get_org_service),
):
    return await org_service.get_org(org_id)

@router.put("/{org_id}", response_model=OrgResponse)
async def update_org(
    org_id: str,
    update_data: dict,
    org_service: OrgService = Depends(get_org_service),
):
    return await org_service.update_org(org_id, update_data)

@router.delete("/{org_id}")
async def delete_org(
    org_id: str,
    org_service: OrgService = Depends(get_org_service),
):
    await org_service.delete_org(org_id)
    return {"message": "Org deleted successfully"}

@router.get("/", response_model=list[OrgResponse])
async def get_all_orgs(
    org_service: OrgService = Depends(get_org_service),
):
    return await org_service.get_all_orgs()

@router.post("/{org_id}/rate")
async def rate_org(
    org_id: str,
    rating: int,
    current_user: dict = Depends(get_current_user),
    org_service: OrgService = Depends(get_org_service),
):
    return await org_service.add_rating(org_id, current_user.id, rating)

@router.post("/{org_id}/upload-image", response_model=OrgResponse)
async def upload_org_image(
    org_id: str,
    image: UploadFile = File(...),
    org_service: OrgService = Depends(get_org_service),
    gcs: GoogleCloudStorage = Depends(GoogleCloudStorage),
):
    unique_filename = generate_unique_filename(image.filename)
    image_url = await gcs.upload_file(
        image.file,
        f"green-core/orgs/{org_id}/{unique_filename}"
    )
    updated_org = await org_service.update_org(org_id, {"image_url": image_url})
    return updated_org