from enum import Enum
import json
import os
import pkgutil
import random
from typing import Dict, List, Optional
from BaseClasses import Item, ItemClassification
from .Enum import CivVICheckType, EraType
from .ProgressiveDistricts import get_flat_progressive_districts, get_progressive_districts
CIV_VI_AP_ITEM_ID_BASE = 5041000

NON_PROGRESSION_DISTRICTS = [
    "PROGRESSIVE_PRESERVE",
    "PROGRESSIVE_NEIGHBORHOOD"
]


# Items required as progression for boostsanity mode
BOOSTSANITY_PROGRESSION_ITEMS = [
    "TECH_THE_WHEEL",
    "TECH_MASONRY",
    "TECH_ARCHERY",
    "TECH_ENGINEERING",
    "TECH_CONSTRUCTION",
    "TECH_GUNPOWDER",
    "TECH_MACHINERY",
    "TECH_SIEGE_TACTICS",
    "TECH_STIRRUPS",
    "TECH_ASTRONOMY",
    "TECH_BALLISTICS",
    "TECH_STEAM_POWER",
    "TECH_SANITATION",
    "TECH_COMPUTERS",
    "TECH_COMBUSTION",
    "TECH_TELECOMMUNICATIONS",
    "TECH_ROBOTICS",
    "CIVIC_FEUDALISM",
    "CIVIC_GUILDS",
    "CIVIC_THE_ENLIGHTENMENT",
    "CIVIC_MERCANTILISM",
    "CIVIC_CONSERVATION",
    "CIVIC_CIVIL_SERVICE",
    "CIVIC_GLOBALIZATION",
    "CIVIC_COLD_WAR",
    "CIVIC_URBANIZATION",
    "PROGRESSIVE_NEIGHBORHOOD",
    "PROGRESSIVE_PRESERVE"
]


class FillerItemRarity(Enum):
    COMMON = "RARE"
    UNCOMMON = "UNCOMMON"
    RARE = "COMMON"


FILLER_DISTRIBUTION: Dict[FillerItemRarity, float] = {
    FillerItemRarity.RARE: 0.05,
    FillerItemRarity.UNCOMMON: .2,
    FillerItemRarity.COMMON: 0.75,
}


class FillerItemData:
    name: str
    type: str
    rarity: FillerItemRarity

    def __init__(self, data: Dict[str, str]):
        self.name = data["Name"]
        self.rarity = FillerItemRarity(data["Rarity"])


cached_filler_items: Optional[List[FillerItemData]] = None


def get_filler_item_data() -> Dict[str, FillerItemData]:
    """
    Returns a dictionary of filler items with their data
    """
    global cached_filler_items
    if not cached_filler_items:
        goody_hut_rewards_path = os.path.join('data', 'goody_hut_rewards.json')
        goody_huts: List[Dict[str, str]] = json.loads(
            pkgutil.get_data(__name__, goody_hut_rewards_path).decode())

        # Create a FillerItemData object for each item
        cached_filler_items = {item["Name"]: FillerItemData(item) for item in goody_huts}

    return cached_filler_items


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType
    progression_name: Optional[str]
    civ_name: Optional[str]

    def __init__(self, name, civ_vi_id: int, cost: int,  item_type: CivVICheckType, id_offset: int, classification: ItemClassification, progression_name: Optional[str], civ_name: Optional[str] = None):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE + id_offset
        self.cost = cost
        self.item_type = item_type
        self.progression_name = progression_name
        self.civ_name = civ_name


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int
    item_type: CivVICheckType

    def __init__(self, item: CivVIItemData, player: int, classification: ItemClassification = None):
        super().__init__(item.name, classification or item.classification, item.code, player)
        self.civ_vi_id = item.civ_vi_id
        self.item_type = item.item_type

def format_item_name(name: str) -> str:
    name_parts = name.split("_")
    return " ".join([part.capitalize() for part in name_parts])

def generate_item_table() -> Dict[str, CivVIItemData]:

    # Generate Techs
    existing_tech_path = os.path.join('data', 'existing_tech.json')

    existing_techs = json.loads(pkgutil.get_data(
        __name__, existing_tech_path).decode())

    file_path = os.path.join('data', 'era_required_items.json')
    required_items: List[str] = []
    era_required_items = json.loads(
        pkgutil.get_data(__name__, file_path).decode())

    for key, value in era_required_items.items():
        required_items += value

    progresive_items = get_flat_progressive_districts()

    item_table = {}

    # Used to offset the CivVIItemData code so tech's and civics don't overlap ids
    tech_id_base = 0
    for tech in existing_techs:
        classification = ItemClassification.useful
        name = tech["Name"]
        civ_name = tech["Type"]
        if civ_name in required_items:
            classification = ItemClassification.progression
        progression_name = None
        check_type = CivVICheckType.TECH
        if civ_name in progresive_items.keys():
            progression_name = format_item_name(progresive_items[civ_name])

        item_table[name] = CivVIItemData(
            name, tech_id_base, tech["Cost"], check_type, 0, classification, progression_name, civ_name=civ_name)

        tech_id_base += 1

    # Generate Civics
    existing_civics_path = os.path.join('data', 'existing_civics.json')
    civic_id_base = 0

    existing_civics = json.loads(
        pkgutil.get_data(__name__, existing_civics_path).decode())

    for civic in existing_civics:
        name = civic["Name"]
        civ_name = civic["Type"]
        progression_name = None
        check_type = CivVICheckType.CIVIC

        if civ_name in progresive_items.keys():
            progression_name = format_item_name(progresive_items[civ_name])

        classification = ItemClassification.useful
        if civ_name in required_items:
            classification = ItemClassification.progression

        item_table[name] = CivVIItemData(
            name, civic_id_base, civic["Cost"], check_type, tech_id_base, classification, progression_name, civ_name=civ_name)

        civic_id_base += 1

    # Generate Progressive Districts
    progressive_id_base = 0
    progresive_items = get_progressive_districts()
    for item_name in progresive_items.keys():
        progression = ItemClassification.progression
        if item_name in NON_PROGRESSION_DISTRICTS:
            progression = ItemClassification.useful
        name = format_item_name(item_name)
        item_table[name] = CivVIItemData(
            name, progressive_id_base, 0, CivVICheckType.PROGRESSIVE_DISTRICT, civic_id_base + tech_id_base, progression, None, civ_name=item_name)
        progressive_id_base += 1

    # Generate progressive eras
    progressive_era_name = format_item_name("PROGRESSIVE_ERA")
    item_table[progressive_era_name] = CivVIItemData(progressive_era_name, progressive_id_base, 0, CivVICheckType.ERA, civic_id_base + tech_id_base, ItemClassification.progression, None, civ_name="PROGRESSIVE_ERA")
    progressive_id_base += 1

    # Generate goody hut items
    goody_huts = get_filler_item_data()
    for value in goody_huts.values():
        item_table[value.name] = CivVIItemData(value.name, progressive_id_base, 0, CivVICheckType.GOODY, civic_id_base + tech_id_base, ItemClassification.filler, None)
        progressive_id_base += 1

    return item_table


def get_items_by_type(item_type: CivVICheckType, item_table: Dict[str, CivVIItemData]) -> List[CivVIItemData]:
    """
    Returns a list of items that match the given item type
    """
    return [item for item in item_table.values() if item.item_type == item_type]


def get_random_filler_by_rarity(rarity: FillerItemRarity, item_table: Dict[str, CivVIItemData]) -> CivVIItemData:
    """
    Returns a random filler item by rarity
    """
    items = [item for item in get_filler_item_data().values() if item.rarity == rarity]
    return items[random.randint(0, len(items) - 1)]
