import os
from typing import List, Optional, Dict
from BaseClasses import Location, Region
import json

from worlds.civ_6.Enum import CivVICheckType, EraType

CIV_VI_AP_LOCATION_ID_BASE = 5041000


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
    with open(new_tech_prereq_path) as f:
        new_tech_prereqs = json.load(f)

    new_tech_path = os.path.join(
        current_directory, 'data', 'new_tech.json')

    with open(new_tech_path) as f:
        new_techs = json.load(f)

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
    with open(new_civic_prereq_path) as f:
        new_civic_prereqs = json.load(f)

    new_civic_path = os.path.join(
        current_directory, 'data', 'new_civics.json')

    with open(new_civic_path) as f:
        new_civics = json.load(f)

    for data in new_civics:
        era_type = data['EraType']
        if era_type not in era_locations:
            era_locations[era_type] = {}
        prereq_data = [
            item for item in new_civic_prereqs if item['Civic'] == data['Type']]
        era_locations[era_type][data["Type"]] = CivVILocationData(
            data["Type"], data['Cost'], data['UITreeRow'], id_base, era_type, CivVICheckType.CIVIC, prereq_data)
        id_base += 1

    return era_locations
