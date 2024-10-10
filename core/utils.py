import json
from pathlib import Path


async def get_workpattern_data_from_json(json_file_path: str | Path) -> list:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data


async def get_workpatterns_dicts_list(json_data: list) -> list[dict]:
    workpatterns_list: list = []
    for id, item in enumerate(json_data, start=1):
        item.update(id=id)
        workpatterns_list.append(item)
    return workpatterns_list
