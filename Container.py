from dataclasses import dataclass
import os
from typing import List
import zipfile
from worlds.Files import APContainer

from worlds.civ_6.Enum import CivVICheckType
from worlds.civ_6.Locations import CivVILocation, CivVILocationData
from worlds.civ_6.Options import CivVIOptions


# Python fstrings don't allow backslashes, so we use this workaround
nl = "\n"
tab = "\t"
apo = "\'"


@dataclass
class CivTreeItem:
    name: str
    cost: int
    ui_tree_row: int


class CivVIContainer(APContainer):
    """
    Responsible for generating the dynamic mod files for the Civ VI multiworld
    """
    game: str = "Civilization VI"

    def __init__(self, patch_data: dict, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, yml in self.patch_data.items():
            opened_zipfile.writestr(filename, yml)
        super().write_contents(opened_zipfile)

def get_cost(world, location: CivVILocationData) -> int:
    """
    Returns the cost of the item based on the game options
    """
    options: CivVIOptions = world.options
    multiplier = options.research_cost_multiplier
    return int(world.location_table[location.name].cost * multiplier)

def generate_new_items(world) -> str:
    """
    Generates the XML for the new techs/civics as well as the blockers used to prevent players from researching their own items
    """
    locations: List[CivVILocation] = world.multiworld.get_filled_locations(
        world.player)
    techs = [location for location in locations if location.location_type ==
             CivVICheckType.TECH]
    civics = [location for location in locations if location.location_type ==
              CivVICheckType.CIVIC]
# fmt: off
    return f"""<?xml version="1.0" encoding="utf-8"?>
<GameInfo>
  <Types>
    <Row Type="TECH_BLOCKER" Kind="KIND_TECH" />
    <Row Type="CIVIC_BLOCKER" Kind="KIND_CIVIC" />
  {"".join([f'{tab}<Row Type="{tech.name}" Kind="KIND_TECH" />{nl}' for
           tech in techs])}
  {"".join([f'{tab}<Row Type="{civic.name}" Kind="KIND_CIVIC" />{nl}' for
           civic in civics])}
  </Types>
  <Technologies>
      <Row TechnologyType="TECH_BLOCKER" Name="TECH_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="9999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Tech created to prevent players from researching their own tech"/>
{"".join([f'{tab}<Row TechnologyType="{location.name}" '
               f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
               f'{location.item.name}" '
               f'EraType="{world.location_table[location.name].era_type}" '
               f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
               f'Cost="{get_cost(world, world.location_table[location.name])}" '
               f'Description="{location.name}" '
               f'AdvisorType="ADVISOR_GENERIC" />{nl}'
               for location in techs])}
  </Technologies>
  <Civics>
      <Row CivicType="CIVIC_BLOCKER" Name="CIVIC_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="9999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Civic created to prevent players from researching their own civics"/>
{"".join([f'{tab}<Row CivicType="{location.name}" '
               f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
               f'{location.item.name}" '
               f'EraType="{world.location_table[location.name].era_type}" '
               f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
               f'Cost="{get_cost(world, world.location_table[location.name])}" '
               f'Description="{location.name}" '
               f'AdvisorType="ADVISOR_GENERIC" />{nl}'
               for location in civics])}
  </Civics>
</GameInfo>
    """
# fmt: on