from enum import Enum
import json
import os
import pkgutil
from typing import Dict, List
from BaseClasses import Item, ItemClassification
from .Enum import CivVICheckType
from .ProgressiveItems import get_flat_progressive_items, get_progressive_items
CIV_VI_AP_ITEM_ID_BASE = 5041000


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType
    progression_name: str | None

    def __init__(self, name, civ_vi_id: int, cost: int,  item_type: CivVICheckType, id_offset: int, classification: ItemClassification, progression_name: str | None):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE + id_offset
        self.cost = cost
        self.item_type = item_type
        self.progression_name = progression_name


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int
    item_type: CivVICheckType

    def __init__(self, item: CivVIItemData, player: int):
        super().__init__(item.name, item.classification, item.code, player)
        self.civ_vi_id = item.civ_vi_id
        self.item_type = item.item_type


def generate_item_table() -> Dict[str, CivVIItemData]:
    """
    Uses the data from existing_tech.json to generate a location table in the following format:
    {
      "TECH_POTTERY": ItemData,
      "TECH_ANIMAL_HUSBANDRY": ItemData,
      "CIVIC_CODE_OF_LAWS": ItemData,
      "CIVIC_CRAFTSMANSHIP": ItemData
      ...
    }
    """
    # Generate Techs
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    existing_tech_path = os.path.join(
        current_directory, 'data', 'existing_tech.json')

    existing_techs = json.loads(pkgutil.get_data(
        __name__, existing_tech_path).decode())

    file_path = os.path.join(os.path.dirname(
        __file__), 'data/era_required_items.json')
    required_items: List[str] = []
    era_required_items = json.loads(
        pkgutil.get_data(__name__, file_path).decode())
    for key, value in era_required_items.items():
        required_items += value

    progresive_items = get_flat_progressive_items()

    item_table = {}

    # Used to offset the CivVIItemData code so tech's and civics don't overlap ids
    tech_id_base = 0
    for tech in existing_techs:
        classification = ItemClassification.progression if tech[
            "Type"] in required_items else ItemClassification.useful
        name = tech["Type"]
        progression_name = None
        check_type = CivVICheckType.TECH
        if tech["Type"] in progresive_items.keys():
            progression_name = progresive_items[name]

        item_table[tech["Type"]] = CivVIItemData(
            name, tech_id_base, tech["Cost"], check_type, 0, classification, progression_name)

        tech_id_base += 1

    # Generate Civics
    existing_civics_path = os.path.join(
        current_directory, 'data', 'existing_civics.json')
    civic_id_base = 0

    existing_civics = json.loads(
        pkgutil.get_data(__name__, existing_civics_path).decode())

    for civic in existing_civics:
        name = civic["Type"]
        progression_name = None
        check_type = CivVICheckType.CIVIC
        if civic["Type"] in progresive_items.keys():
            progression_name = progresive_items[name]

        classification = ItemClassification.progression if civic[
            "Type"] in required_items else ItemClassification.useful
        item_table[civic["Type"]] = CivVIItemData(
            civic["Type"], civic_id_base, civic["Cost"], check_type, tech_id_base, classification, progression_name)

        civic_id_base += 1

    # Generate Progressive Items
    progressive_id_base = 0
    progresive_items = get_progressive_items()
    for item_name in progresive_items.keys():
        item_table[item_name] = CivVIItemData(
            item_name, progressive_id_base, 0, CivVICheckType.PROGRESSIVE, civic_id_base + tech_id_base, ItemClassification.progression, None)
        progressive_id_base += 1

    return item_table
