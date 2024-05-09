import os
import pkgutil
from typing import List, Optional, Dict
from BaseClasses import Location, LocationProgressType, Region
import json

from .Enum import CivVICheckType, EraType

CIV_VI_AP_LOCATION_ID_BASE = 5041000

# Locs that should have progression items (keypoint techs/civics, ~1 per era)
PRIORITY_LOCATIONS = [
    "TECH_AP9",
    "TECH_AP15",
    "TECH_AP20",
    "TECH_AP33",
    "TECH_AP35",
    "TECH_AP47",
    "TECH_AP51",
    "TECH_AP59",

    "CIVIC_AP4",
    "CIVIC_AP8",
    "CIVIC_AP19",
    "CIVIC_AP19",
    "CIVIC_AP26",
    "CIVIC_AP33",
    "CIVIC_AP39",
    "CIVIC_AP46",
    "CIVIC_AP48",

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

    # "TECH_AP69",
    # "TECH_AP70",
    # "TECH_AP71",
    # "TECH_AP72",
    # "TECH_AP73",
    # "TECH_AP74",
    # "TECH_AP75",
    # "TECH_AP76",

    # "CIVIC_AP50",
    # "CIVIC_AP56",
    # "CIVIC_AP57",
    # "CIVIC_AP58",
    # "CIVIC_AP59",
    # "CIVIC_AP60",
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

    def __init__(self, player: int, name: str = '', address: int | None = None, parent: Region | None = None):
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
      "TECH_AP0": CivVILocationData,
      "TECH_AP1": CivVILocationData,
      "CIVIC_AP0": CivVILocationData,
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
        "TECH_AP0": CivVILocationData,
        "TECH_AP1": CivVILocationData,
        "CIVIC_AP0": CivVILocationData,
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
    for i in range(len(EraType) - 1):
        container_era = eras[i].name
        era_locations[container_era][container_era] = CivVILocationData(
            container_era, 0, 0, id_base, container_era, CivVICheckType.ERA)
        id_base += 1

    return era_locations
