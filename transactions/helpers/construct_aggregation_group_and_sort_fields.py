def construct_aggregation_group_and_sort_fields(mode):
    """
    Constructs the group identifier and sort fields for MongoDB aggregation based on the given mode.

    Parameters:
    - mode (str): The grouping mode, can be 'daily', 'weekly', or 'monthly'.

    Returns:
    - tuple:
        - group_id (dict): The group identifier for the aggregation pipeline.
        - sort_fields (list of tuples): Fields to sort by, with sort order.

    Raises:
    - ValueError: If the mode is not one of 'daily', 'weekly', or 'monthly'.
    """
    if mode == "daily":
        group_id = {
            "year": {"$year": "$createdAt"},
            "month": {"$month": "$createdAt"},
            "day": {"$dayOfMonth": "$createdAt"},
        }
        sort_fields = [("_id.year", 1), ("_id.month", 1), ("_id.day", 1)]
    elif mode == "weekly":
        group_id = {
            "isoYear": {"$isoWeekYear": "$createdAt"},
            "isoWeek": {"$isoWeek": "$createdAt"},
        }
        sort_fields = [("_id.isoYear", 1), ("_id.isoWeek", 1)]
    elif mode == "monthly":
        group_id = {"year": {"$year": "$createdAt"}, "month": {"$month": "$createdAt"}}
        sort_fields = [("_id.year", 1), ("_id.month", 1)]
    else:
        raise ValueError("Mode must be 'daily', 'weekly', or 'monthly'")
    return group_id, sort_fields
