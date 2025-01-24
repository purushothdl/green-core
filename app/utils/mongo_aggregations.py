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


def get_weekly_waste_data_aggregation(user_id: str):
    """
    Aggregation pipeline to calculate weekly waste data for the last 2 months.
    Adjusts for IST time zone.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=60)

    return [
        # Filter disposals for the last 2 months
        {
            "$match": {
                "user_id": user_id,
                "date": {"$gte": start_date, "$lte": end_date}
            }
        },
        # Convert UTC dates to IST
        {
            "$addFields": {
                "ist_date": {
                    "$dateToString": {
                        "format": "%Y-%m-%dT%H:%M:%S",
                        "date": {
                            "$add": [
                                "$date",
                                5.5 * 60 * 60 * 1000  # Add 5.5 hours for IST
                            ]
                        }
                    }
                }
            }
        },
        # Group by week and waste type
        {
            "$group": {
                "_id": {
                    "week_start": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {
                                "$subtract": [
                                    {"$toDate": "$ist_date"},
                                    {"$multiply": [{"$dayOfWeek": {"$toDate": "$ist_date"}}, 24 * 60 * 60 * 1000]}
                                ]
                            }
                        }
                    },
                    "waste_type": "$waste_type"
                },
                "total_weight": {"$sum": "$weight"}
            }
        },
        # Group by week to format the output
        {
            "$group": {
                "_id": "$_id.week_start",
                "waste_data": {
                    "$push": {
                        "waste_type": "$_id.waste_type",
                        "weight": "$total_weight"
                    }
                }
            }
        },
        # Sort by week
        {
            "$sort": {
                "_id": 1
            }
        },
        # Format the final output
        {
            "$project": {
                "_id": 0,
                "week": "$_id",
                "waste_data": {
                    "$arrayToObject": {
                        "$zip": {
                            "inputs": ["$waste_data.waste_type", "$waste_data.weight"]
                        }
                    }
                }
            }
        }
    ]