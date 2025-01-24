from app.repositories.waste_repository import WasteRepository
from app.schemas.waste import WasteDisposalCreate, WasteDisposalResponse

class WasteService:
    def __init__(self, waste_collection):
        self.waste_repo = WasteRepository(waste_collection)

    async def create_disposal(self, user_id: str, disposal: WasteDisposalCreate) -> WasteDisposalResponse:
        disposal_dict = disposal.dict()
        disposal_dict["user_id"] = user_id
        created_disposal = await self.waste_repo.create_disposal(disposal_dict)
        return WasteDisposalResponse(**created_disposal)

    async def get_disposals_by_user(self, user_id: str) -> list[WasteDisposalResponse]:
        disposals = await self.waste_repo.get_disposals_by_user(user_id)
        return [WasteDisposalResponse(**disposal) for disposal in disposals]
    
    async def get_waste_stats(self, user_id: str):
        return await self.waste_repo.get_waste_stats(user_id)
    
    async def get_weekly_waste_data(self, user_id: str):
        return await self.waste_repo.get_weekly_waste_data(user_id)