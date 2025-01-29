from bson import ObjectId
from datetime import datetime, timedelta

import pytz
from app.utils.mongo_aggregations import (
    get_waste_stats_aggregation,
    get_weekly_waste_data_db,

)

class WasteRepository:
    def __init__(self, waste_collection):
        self.waste_collection = waste_collection

    async def create_disposal(self, disposal: dict):
        """
        Creates a new waste disposal record and returns it with an ID.
        """
        disposal["date"] = datetime.utcnow()
        result = await self.waste_collection.insert_one(disposal)
        disposal["id"] = str(result.inserted_id)
        return disposal

    async def get_disposals_by_user(self, user_id: str):
        """
        Fetches all waste disposal records for a user.
        """
        disposals = []
        async for disposal in self.waste_collection.find({"user_id": user_id}):
            disposal["id"] = str(disposal["_id"])
            disposals.append(disposal)
        return disposals
    
    async def get_waste_stats(self, user_id: str):
        """
        Fetches total waste and weight by type for a user.
        """
        pipeline = get_waste_stats_aggregation(user_id)
        result = await self.waste_collection.aggregate(pipeline).to_list(1)
        return result[0] if result else {"total_weight": 0, "waste_by_type": {}}


    async def get_weekly_waste_data(self, user_id: str):
        """
        Fetches weekly waste data for the last 2 months, adjusted for IST.
        Returns only entries with non-zero total_weight.
        """
        pipeline = get_weekly_waste_data_db(user_id)
        results = await self.waste_collection.aggregate(pipeline).to_list(None)
        
        non_zero_results = [entry for entry in results if entry.get("total_weight", 0) != 0]
        
        return non_zero_results