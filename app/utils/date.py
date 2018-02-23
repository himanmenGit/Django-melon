import re

from datetime import date

__all__ = (
    'get_valid_date',
)


def get_valid_date(need_check_date):
    modify_date = None
    if need_check_date:
        date_list = [0, 1, 1]
        for index, dates in enumerate(re.split(r'[^\d]', need_check_date)):
            date_list[index] = int(dates)
        modify_date = date(date_list[0], date_list[1], date_list[2])
    return modify_date
