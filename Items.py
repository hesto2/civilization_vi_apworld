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
    COMMON = 1
    UNCOMMON = 2
    RARE = 3


FILLER_DISTRIBUTION: Dict[FillerItemRarity, float] = {
    FillerItemRarity.RARE: 0.1,
    FillerItemRarity.UNCOMMON: .3,
    FillerItemRarity.COMMON: 0.6,
}

FILLER_ITEMS = {
    "GOODY_GOLD_SMALL_MODIFIER": FillerItemRarity.COMMON,
    "GOODY_GOLD_SMALL_MODIFIER": FillerItemRarity.COMMON,
    "GOODY_GOLD_SMALL_MODIFIER": FillerItemRarity.UNCOMMON,
    "GOODY_FAITH_SMALL_MODIFIER": FillerItemRarity.COMMON,
    "GOODY_FAITH_MEDIUM_MODIFIER": FillerItemRarity.COMMON,
    "GOODY_FAITH_LARGE_MODIFIER": FillerItemRarity.UNCOMMON,
    "GOODY_DIPLOMACY_GRANT_FAVOR": FillerItemRarity.COMMON,
    "GOODY_DIPLOMACY_GRANT_GOVERNOR_TITLE": FillerItemRarity.RARE,
    "GOODY_DIPLOMACY_GRANT_ENVOY": FillerItemRarity.UNCOMMON,
    "GOODY_CULTURE_GRANT_ONE_RELIC": FillerItemRarity.RARE,
    "GOODY_MILITARY_GRANT_SCOUT": FillerItemRarity.COMMON,
    "GOODY_SURVIVORS_ADD_POPULATION": FillerItemRarity.UNCOMMON,
    "GOODY_SURVIVORS_GRANT_BUILDER": FillerItemRarity.UNCOMMON,
    "GOODY_SURVIVORS_GRANT_TRADER": FillerItemRarity.UNCOMMON,
    "GOODY_SURVIVORS_GRANT_SETTLER": FillerItemRarity.UNCOMMON,
}


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType
    progression_name: Optional[str]

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

    def __init__(self, item: CivVIItemData, player: int, classification: ItemClassification = None):
        super().__init__(item.name, classification or item.classification, item.code, player)
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
        name = tech["Type"]
        if name in required_items:
            classification = ItemClassification.progression
        progression_name = None
        check_type = CivVICheckType.TECH
        if name in progresive_items.keys():
            progression_name = progresive_items[name]

        item_table[name] = CivVIItemData(
            name, tech_id_base, tech["Cost"], check_type, 0, classification, progression_name)

        tech_id_base += 1

    # Generate Civics
    existing_civics_path = os.path.join('data', 'existing_civics.json')
    civic_id_base = 0

    existing_civics = json.loads(
        pkgutil.get_data(__name__, existing_civics_path).decode())

    for civic in existing_civics:
        name = civic["Type"]
        progression_name = None
        check_type = CivVICheckType.CIVIC

        if name in progresive_items.keys():
            progression_name = progresive_items[name]

        classification = ItemClassification.useful
        if name in required_items:
            classification = ItemClassification.progression

        item_table[name] = CivVIItemData(
            name, civic_id_base, civic["Cost"], check_type, tech_id_base, classification, progression_name)

        civic_id_base += 1

    # Generate Progressive Districts
    progressive_id_base = 0
    progresive_items = get_progressive_districts()
    for item_name in progresive_items.keys():
        progression = ItemClassification.progression
        if item_name in NON_PROGRESSION_DISTRICTS:
            progression = ItemClassification.useful
        item_table[item_name] = CivVIItemData(
            item_name, progressive_id_base, 0, CivVICheckType.PROGRESSIVE_DISTRICT, civic_id_base + tech_id_base, progression, None)
        progressive_id_base += 1

    # Generate progressive eras
    item_table["PROGRESSIVE_ERA"] = CivVIItemData("PROGRESSIVE_ERA", progressive_id_base, 0, CivVICheckType.ERA, civic_id_base + tech_id_base, ItemClassification.progression, None)
    progressive_id_base += 1

    # Generate goody hut items
    item_table["GOODY_GOLD_SMALL_MODIFIER"] = CivVIItemData("GOODY_GOLD_SMALL_MODIFIER", progressive_id_base, 0, CivVICheckType.GOODY, civic_id_base + tech_id_base, ItemClassification.filler, None)
    for key, value in FILLER_ITEMS.items():
        item_table[key] = CivVIItemData(key, progressive_id_base, 0, CivVICheckType.GOODY, civic_id_base + tech_id_base, ItemClassification.filler, None)
        progressive_id_base += 1

    return item_table


def get_random_filler_by_rarity(rarity: FillerItemRarity) -> CivVIItemData:
    """
    Returns a random filler item by rarity
    """
    items = [item for item, item_rarity in FILLER_ITEMS.items() if item_rarity == rarity]
    return items[random.randint(0, len(items) - 1)]
