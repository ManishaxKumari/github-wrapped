from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union

from src.models import MonthData, MonthDatum, UserPackage
from src.utils import format_number


def get_month_data(data: UserPackage) -> MonthData:
    months: Dict[int, Dict[str, int]] = defaultdict(
        lambda: {"contribs": 0, "loc_changed": 0}
    )

    for item in data.contribs.total:
        month = datetime.fromisoformat(item.date).month - 1
        months[month]["contribs"] += item.stats.contribs_count
        loc_changed = sum(
            [x.additions + x.deletions for x in item.stats.languages.values()]
        )
        months[month]["loc_changed"] += loc_changed

    out: List[MonthDatum] = []
    for k in range(12):
        v = months[k]
        _obj: Dict[str, Union[str, int]] = {"month": k, **v}
        _obj["formatted_loc_changed"] = format_number(v["loc_changed"])
        out.append(MonthDatum.parse_obj(_obj))

    return MonthData(months=out)