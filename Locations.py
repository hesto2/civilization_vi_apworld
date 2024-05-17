import os
import pkgutil
from typing import List, Optional, Dict
from BaseClasses import Location, LocationProgressType, Region
import json

from .Enum import CivVICheckType, EraType

CIV_VI_AP_LOCATION_ID_BASE = 5041000

# Locs that should have progression items (keypoint techs/civics, ~1 per era)
PRIORITY_LOCATIONS = [
    "TECH_ANCEINT_09",
    "TECH_CLASSICAL_15",
    "TECH_MEDIEVAL_20",
    "TECH_RENAISSANCE_33",
    "TECH_INDUSTRIAL_35",
    "TECH_MODERN_47",
    "TECH_ATOMIC_51",
    "TECH_INFORMATION_59",

    "CIVIC_ANCIENT_04",
    "CIVIC_CLASSICAL_08",
    "CIVIC_MEDIEVAL_19",
    "CIVIC_RENAISSANCE_26",
    "CIVIC_INDUSTRIAL_33",
    "CIVIC_MODERN_39",
    "CIVIC_ATOMIC_46",
    "CIVIC_INFORMATION_48",

    "ERA_CLASSICAL",
    "ERA_MEDIEVAL",
    "ERA_RENAISSANCE",
    "ERA_INDUSTRIAL",
    "ERA_MODERN",
    "ERA_ATOMIC",
    "ERA_INFORMATION",
    "ERA_FUTURE"
]

# Locs that should not have progression items (future techs/civics)
# Disabled for now since we don't have junk/filler items to put here in single world games
EXCLUDED_LOCATIONS = [

    # "TECH_FUTURE_69",
    # "TECH_FUTURE_70",
    # "TECH_FUTURE_71",
    # "TECH_FUTURE_72",
    # "TECH_FUTURE_73",
    # "TECH_FUTURE_74",
    # "TECH_FUTURE_75",
    # "TECH_FUTURE_76",

    # "CIVIC_FUTURE_50",
    # "CIVIC_FUTURE_56",
    # "CIVIC_FUTURE_57",
    # "CIVIC_FUTURE_58",
    # "CIVIC_FUTURE_59",
    # "CIVIC_FUTURE_60",
]


class CivVILocationData():
    game: str = "Civilization VI"
    name: str
    cost: int
    uiTreeRow: int
    civ_id: int
    code: int
    era_type: EraType
    location_type: CivVICheckType
    pre_reqs: List[str]

    def __init__(self, name: str, cost: int, uiTreeRow: int, id: int, era_type: EraType, location_type: CivVICheckType, pre_reqs: Optional[List[str]] = None):
        self.name = name
        self.cost = cost
        self.uiTreeRow = uiTreeRow
        self.civ_id = id
        self.code = id + CIV_VI_AP_LOCATION_ID_BASE
        self.era_type = era_type
        self.pre_reqs = pre_reqs
        self.location_type = location_type


class CivVILocation(Location):
    game: str = "Civilization VI"
    location_type: CivVICheckType

    def __init__(self, player: int, name: str = '', address: Optional[int] = None, parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        if name.split("_")[0] == "TECH":
            self.location_type = CivVICheckType.TECH
        elif name.split("_")[0] == "CIVIC":
            self.location_type = CivVICheckType.CIVIC
        elif name.split("_")[0] == "ERA":
            self.location_type = CivVICheckType.ERA

        if self.name in PRIORITY_LOCATIONS:
            self.progress_type = LocationProgressType.PRIORITY
        elif self.name in EXCLUDED_LOCATIONS:
            self.progress_type = LocationProgressType.EXCLUDED
        else:
            self.progress_type = LocationProgressType.DEFAULT


def generate_flat_location_table() -> Dict[str, CivVILocationData]:
    """
    Generates a flat location table in the following format:
    {
      "TECH_AP_ANCIENT_00": CivVILocationData,
      "TECH_AP_ANCIENT_01": CivVILocationData,
      "CIVIC_AP_ANCIENT_00": CivVILocationData,
      ...
    }
    """
    era_locations = generate_era_location_table()
    flat_locations = {}
    for era_type, locations in era_locations.items():
        for location_id, location_data in locations.items():
            flat_locations[location_id] = location_data
    return flat_locations


def generate_era_location_table() -> Dict[EraType, Dict[str, CivVILocationData]]:
    """
    Uses the data from existing_tech.json to generate a location table in the following format:
    {
      "ERA_ANCIENT": {
        "TECH_AP_ANCIENT_00": CivVILocationData,
        "TECH_AP_ANCIENT_01": CivVILocationData,
        "CIVIC_AP_ANCIENT_00": CivVILocationData,
      },
      ...
    }
    """
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    new_tech_prereq_path = os.path.join(
        current_directory, 'data', 'new_tech_prereqs.json')
    new_tech_prereqs = json.loads(
        pkgutil.get_data(__name__, new_tech_prereq_path).decode())

    new_tech_path = os.path.join(
        current_directory, 'data', 'new_tech.json')

    new_techs = json.loads(pkgutil.get_data(
        __name__, new_tech_path).decode())

    era_locations = {}
    id_base = 0
# Techs
    for data in new_techs:
        era_type = data['EraType']
        if era_type not in era_locations:
            era_locations[era_type] = {}

        prereq_data = [
            item for item in new_tech_prereqs if item['Technology'] == data['Type']]

        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"], data['Cost'], data['UITreeRow'], id_base, era_type, CivVICheckType.TECH, prereq_data)
        id_base += 1
# Civics
    new_civic_prereq_path = os.path.join(
        current_directory, 'data', 'new_civic_prereqs.json')
    new_civic_prereqs = json.loads(
        pkgutil.get_data(__name__, new_civic_prereq_path).decode())

    new_civic_path = os.path.join(
        current_directory, 'data', 'new_civics.json')

    new_civics = json.loads(pkgutil.get_data(
        __name__, new_civic_path).decode())

    for data in new_civics:
        era_type = data['EraType']
        if era_type not in era_locations:
            era_locations[era_type] = {}
        prereq_data = [
            item for item in new_civic_prereqs if item['Civic'] == data['Type']]
        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"], data['Cost'], data['UITreeRow'], id_base, era_type, CivVICheckType.CIVIC, prereq_data)
        id_base += 1

# Eras
    eras = list(EraType)
    for i in range(len(EraType)):
        location_era = eras[i].name

        if location_era == "ERA_ANCIENT":
            continue

        era_locations[location_era][location_era] = CivVILocationData(
            location_era, 0, 0, id_base, location_era, CivVICheckType.ERA)
        id_base += 1

    return era_locations
