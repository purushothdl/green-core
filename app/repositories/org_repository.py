from datetime import datetime
from bson import ObjectId

from app.core.exceptions import DuplicateRatingError, OrgNotFoundError
from app.utils.mongo_utils import convert_objectids_to_strings

class OrgRepository:
    def __init__(self, orgs_collection):
        self.orgs_collection = orgs_collection

    async def create_org(self, org: dict):
        org["created_at"] = datetime.utcnow()
        result = await self.orgs_collection.insert_one(org)
        org["id"] = str(result.inserted_id)
        return org

    async def get_org_by_id(self, org_id: str):
        org = await self.orgs_collection.find_one({"_id": ObjectId(org_id)})
        if org:
            org["id"] = str(org["_id"])
        return org

    async def update_org(self, org_id: str, update_data: dict):
        result = await self.orgs_collection.update_one(
            {"_id": ObjectId(org_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise OrgNotFoundError("Org not found")
        return await self.get_org_by_id(org_id)

    async def delete_org(self, org_id: str):
        result = await self.orgs_collection.delete_one({"_id": ObjectId(org_id)})
        if result.deleted_count == 0:
            raise OrgNotFoundError("Org not found")
        
    async def get_all_orgs(self):
        orgs = []
        async for org in self.orgs_collection.find():
            org["id"] = str(org["_id"])
            orgs.append(org)
        return orgs
    
    async def add_rating(self, org_id: str, user_id: str, rating: int):
        org = await self.orgs_collection.find_one({"_id": ObjectId(org_id)})
        if not org:
            raise OrgNotFoundError("Org not found")

        if "user_ratings" in org:
            for user_rating in org["user_ratings"]:
                if user_rating["user_id"] == user_id:
                    raise DuplicateRatingError("User has already rated this org")

        if "user_ratings" not in org:
            org["user_ratings"] = []
        org["user_ratings"].append({"user_id": user_id, "rating": rating})

        total_ratings = sum(r["rating"] for r in org["user_ratings"])
        num_ratings = len(org["user_ratings"])
        org["rating"] = total_ratings / num_ratings

        await self.orgs_collection.update_one(
            {"_id": ObjectId(org_id)},
            {"$set": {"user_ratings": org["user_ratings"], "rating": org["rating"]}}
        )
        return convert_objectids_to_strings(org)