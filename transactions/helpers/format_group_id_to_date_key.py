import datetime

from khayyam import JalaliDate


def format_group_id_to_date_key(group_id, mode):
    """
    Formats the aggregation group identifier into a human-readable date key based on the mode.

    Parameters:
    - group_id (dict): The group identifier from the aggregation result.
    - mode (str): The grouping mode, can be 'daily', 'weekly', or 'monthly'.

    Returns:
    - key (str): The formatted date key.

    Raises:
    - ValueError: If the mode is not one of 'daily', 'weekly', or 'monthly'.

    """

    group_id = {k: v for k, v in group_id.items() if k != "merchantId"}

    if mode == "daily":
        date = datetime.datetime(group_id["year"], group_id["month"], group_id["day"])
        jalali_date = JalaliDate(date)
        key = jalali_date.strftime("%Y/%m/%d")
    elif mode == "weekly":
        iso_year = group_id["isoYear"]
        iso_week = group_id["isoWeek"]
        date = datetime.date.fromisocalendar(iso_year, iso_week, 1)
        jalali_date = JalaliDate(date)
        week_number = int(jalali_date.strftime("%W"))
        key = f"{jalali_date.year} هفته {week_number} سال"
    elif mode == "monthly":
        date = datetime.datetime(group_id["year"], group_id["month"], 1)
        jalali_date = JalaliDate(date)
        month_name = jalali_date.strftime("%B")
        key = f"{jalali_date.year} {month_name}"
    else:
        raise ValueError("Mode must be 'daily', 'weekly', or 'monthly'")
    return key
