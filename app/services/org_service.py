from app.core.exceptions import OrgNotFoundError
from app.repositories.org_repository import OrgRepository
from app.schemas.orgs import OrgCreate, OrgResponse

class OrgService:
    def __init__(self, orgs_collection):
        self.org_repo = OrgRepository(orgs_collection)

    async def create_org(self, org: OrgCreate) -> OrgResponse:
        org_dict = org.dict()
        created_org = await self.org_repo.create_org(org_dict)
        return OrgResponse(**created_org)

    async def get_org(self, org_id: str) -> OrgResponse:
        org = await self.org_repo.get_org_by_id(org_id)
        if not org:
            raise OrgNotFoundError("Org not found")
        return OrgResponse(**org)

    async def update_org(self, org_id: str, update_data: dict) -> OrgResponse:
        updated_org = await self.org_repo.update_org(org_id, update_data)
        return OrgResponse(**updated_org)

    async def delete_org(self, org_id: str):
        await self.org_repo.delete_org(org_id)

    async def get_all_orgs(self) -> list[OrgResponse]:
        orgs = await self.org_repo.get_all_orgs()
        return [OrgResponse(**org) for org in orgs] 
    
    async def add_rating(self, org_id: str, user_id: str, rating: int):
        return await self.org_repo.add_rating(org_id, user_id, rating)