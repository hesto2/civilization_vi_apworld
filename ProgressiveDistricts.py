import json
import os
import pkgutil
from typing import Dict, List

cached_progressive_districts = None


def get_progressive_districts() -> Dict[str, List[str]]:
    """Returns a dict of all progressive items as the key and a list of the associated
     item names as the value"""
    global cached_progressive_districts
    if not cached_progressive_districts:
        file_path = os.path.join('data', 'progressive_districts.json')
        cached_progressive_districts = json.loads(
            pkgutil.get_data(__name__, file_path).decode())

    return cached_progressive_districts


def get_flat_progressive_districts() -> Dict[str, str]:
    """Returns a dictionary of all items that are associated with a progressive item.
    Key is the item name ("TECH_WRITING") and the value is the associated progressive
    item ("PROGRESSIVE_CAMPUS")"""
    progressive_districts = get_progressive_districts()
    flat_progressive_techs = {}
    for key, value in progressive_districts.items():
        for item in value:
            flat_progressive_techs[item] = key
    return flat_progressive_techs


def convert_items_to_have_progression(items: List[str]):
    """ converts a list of items to instead be their associated progressive item if
    they have one. ["TECH_MINING", "TECH_WRITING"] -> ["TECH_MINING", "PROGRESSIVE_CAMPUS]"""
    flat_progressive_techs = get_flat_progressive_districts()
    new_list = []
    for item in items:
        if item in flat_progressive_techs.keys():
            new_list.append(flat_progressive_techs[item])
        else:
            new_list.append(item)
    return new_list
