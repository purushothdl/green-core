from datetime import datetime, timedelta

def get_waste_stats_aggregation(user_id: str):
    """
    Aggregation pipeline to calculate total waste and weight by type for a user.
    """
    return [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$waste_type",
                "total_weight": {"$sum": "$weight"}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_weight": {"$sum": "$total_weight"},
                "waste_by_type": {
                    "$push": {
                        "type": "$_id",
                        "weight": "$total_weight"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "total_weight": 1,
                "waste_by_type": {
                    "$arrayToObject": {
                        "$zip": {
                            "inputs": ["$waste_by_type.type", "$waste_by_type.weight"]
                        }
                    }
                }
            }
        }
    ]



def get_weekly_waste_data_db(user_id: str):
    """
    Aggregation pipeline to calculate weekly waste totals for the last 2 months.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=60)

    return [
        # 1. Filter disposals for the last 60 days (UTC)
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lte": end_date}
            }
        },
        # 2. Group by ISO week in IST (Monday start)
        {
            "$group": {
                "_id": {
                    "year": {"$isoWeekYear": {"date": "$date", "timezone": "Asia/Kolkata"}},
                    "week": {"$isoWeek": {"date": "$date", "timezone": "Asia/Kolkata"}}
                },
                "total_weight": {"$sum": "$weight"}
            }
        },
        # 3. Format week start date (IST)
        {
            "$project": {
                "_id": 0,
                "week": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": {
                            "$dateFromParts": {
                                "isoWeekYear": "$_id.year",
                                "isoWeek": "$_id.week",
                                "isoDayOfWeek": 1,  # Monday
                                "timezone": "Asia/Kolkata"
                            }
                        }
                    }
                },
                "total_weight": 1
            }
        },
        # 4. Sort by week
        {"$sort": {"week": 1}}
    ]


