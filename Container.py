from dataclasses import dataclass
import os
from typing import List
import zipfile
from BaseClasses import ItemClassification
from worlds.Files import APContainer

from .Enum import CivVICheckType
from .Locations import CivVILocation, CivVILocationData
from .Options import CivVIOptions


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
      <Row TechnologyType="TECH_BLOCKER" Name="TECH_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="99999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Tech created to prevent players from researching their own tech. If you can read this, then congrats you have reached the end of your tree before beating the game!"/>
{"".join([f'{tab}<Row TechnologyType="{location.name}" '
                f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
                f'{location.item.name}" '
                f'EraType="{world.location_table[location.name].era_type}" '
                f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
                f'Cost="{get_cost(world, world.location_table[location.name])}" '
                f'Description="{location.name}" '
                f'AdvisorType="{"ADVISOR_PROGRESSIVE" if location.item.classification == ItemClassification.progression else "ADVISOR_GENERIC"}"'
                f'/>{nl}'
                for location in techs])}
  </Technologies>
  <Civics>
      <Row CivicType="CIVIC_BLOCKER" Name="CIVIC_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="99999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Civic created to prevent players from researching their own civics. If you can read this, then congrats you have reached the end of your tree before beating the game!"/>
{"".join([f'{tab}<Row CivicType="{location.name}" '
                    f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
                    f'{location.item.name}" '
                    f'EraType="{world.location_table[location.name].era_type}" '
                    f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
                    f'Cost="{get_cost(world, world.location_table[location.name])}" '
                    f'Description="{location.name}" '
                    f'AdvisorType="{"ADVISOR_PROGRESSIVE" if location.item.classification == ItemClassification.progression else "ADVISOR_GENERIC"}"'
                    f'/>{nl}'
                    for location in civics])}
  </Civics>
</GameInfo>
    """


def generate_setup_file(world) -> str:
    """
    Generates the Lua for the setup file. This sets initial variables and state that affect gameplay around Progressive Eras
    """
    if world.options.progression_style.current_key == "eras_and_districts":
        return f"""
    -- Init Progressive Era Value if it hasn't been set already
    if Game.GetProperty("MaxAllowedEra") == nil then
      print("Setting MaxAllowedEra to 0")
      Game.SetProperty("MaxAllowedEra", 0)
    end
    """
    return f"""
    -- No setup needed for Progressive Eras
      """


def generate_goody_hut_sql(world) -> str:
    """
    Generates the SQL for the goody huts or an empty string if they are disabled since the mod expects the file to be
    """

    if world.options.shuffle_goody_hut_rewards.value:
        return f"""
        UPDATE GoodyHutSubTypes SET Description = NULL WHERE GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND Weight > 0;

INSERT INTO Modifiers
                (ModifierId, ModifierType, RunOnce, Permanent, SubjectRequirementSetId)
SELECT ModifierID||'_AI', ModifierType, RunOnce, Permanent, 'PLAYER_IS_AI'
FROM Modifiers
WHERE EXISTS (
        SELECT ModifierId
        FROM GoodyHutSubTypes
        WHERE Modifiers.ModifierId = GoodyHutSubTypes.ModifierId AND GoodyHutSubTypes.GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND GoodyHutSubTypes.Weight > 0);

INSERT INTO ModifierArguments
                (ModifierId, Name, Type, Value)
SELECT ModifierID||'_AI', Name, Type, Value
FROM ModifierArguments
WHERE EXISTS (
        SELECT ModifierId
        FROM GoodyHutSubTypes
        WHERE ModifierArguments.ModifierId = GoodyHutSubTypes.ModifierId AND GoodyHutSubTypes.GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND GoodyHutSubTypes.Weight > 0);

UPDATE GoodyHutSubTypes
SET ModifierID = ModifierID||'_AI'
WHERE GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND Weight > 0;

      """
    else:
        return "-- Goody Huts are disabled, no changes needed"
