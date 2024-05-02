import os
from typing import Dict

import Utils
from .Container import CivVIContainer, generate_new_items
from .Enum import CivVICheckType
from .Items import CivVIItemData, generate_item_table, CivVIItem
from .Locations import CivVILocationData, EraType, generate_era_location_table, generate_flat_location_table
from .Options import CivVIOptions
from .Regions import create_regions
from BaseClasses import Item, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

def run_client():
    print("Running Civ6 Client")
    from Civ6Client import main  # lazy import
    launch_subprocess(main, name="Civ6Client")


components.append(
    Component("Civ6 Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apcivvi"))
)


class CivVIWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Civlization VI for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["hesto2"]
    )]


class CivVIWorld(World):
    """
    Civilization VI is a turn-based strategy video game in which one or more players compete alongside computer-controlled AI opponents to grow their individual civilization from a small tribe to control the entire planet across several periods of development.
    """

    game: str = "Civilization VI"
    topology_present = False
    options_dataclass = CivVIOptions

    web = CivVIWeb()

    item_name_to_id = {
        item.name: item.code for item in generate_item_table().values()}
    location_name_to_id = {
        location.name: location.code for location in generate_flat_location_table().values()}

    item_table: Dict[str, CivVIItemData] = {}
    location_by_era: Dict[EraType, Dict[str, CivVILocationData]]

    data_version = 1
    required_client_version = (0, 4, 5)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.location_by_era = generate_era_location_table()

        self.location_table = {}
        self.item_table = generate_item_table()

        for _era, locations in self.location_by_era.items():
            for _item_name, location in locations.items():
                self.location_table[location.name] = location

    def create_regions(self):
        create_regions(self, self.options, self.player)

    def create_item(self, name: str) -> Item:
        item: CivVIItemData = self.item_table[name]

        if self.options.progressive_districts and item.progression_name != None:
            item = self.item_table[item.progression_name]

        return CivVIItem(item, self.player)

    def create_items(self):
        for item_name, data in self.item_table.items():
          # Don't add progressive items to the itempool here, instead add the base item and have create_item convert it
            if data.item_type == CivVICheckType.PROGRESSIVE:
                continue
            self.multiworld.itempool += [self.create_item(
                item_name)]

    def fill_slot_data(self):
        return {
            "progressive_districts": self.options.progressive_districts.value,
            "death_link": self.options.death_link.value,

        }

    def generate_output(self, output_directory: str):
      # fmt: off
        mod_name = f"AP-{self.multiworld.get_file_safe_player_name(self.player)}"
      # fmt: on
        mod_dir = os.path.join(
            output_directory, mod_name + "_" + Utils.__version__)
        mod_files = {
            f"NewItems.xml": generate_new_items(self),
        }
        mod = CivVIContainer(mod_files, mod_dir, output_directory, self.player,
                             self.multiworld.get_file_safe_player_name(self.player))
        mod.write()
