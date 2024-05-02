import pkgutil
import typing
from BaseClasses import CollectionState, Region
from worlds.AutoWorld import World
from .Enum import EraType
from .Locations import CivVILocation
from .ProgressiveItems import get_flat_progressive_items
from .Options import CivVIOptions
import json
import os


def get_required_items_for_era(era: EraType):
    """Gets the specific techs/civics that are required for the specified era"""
    era_required_items = {}
    file_path = os.path.join(os.path.dirname(
        __file__), 'data/era_required_items.json')
    era_required_items = json.loads(
        pkgutil.get_data(__name__, file_path).decode())
    return era_required_items[era.value]


def get_cumulative_prereqs_for_era(end_era: EraType, exclude_progressive_items: bool = True):
    """Gets the specific techs/civics that are required for the specified era as well as all previous eras"""
    cumulative_prereqs = []
    era_required_items = {}
    file_path = os.path.join(os.path.dirname(
        __file__), 'data/era_required_items.json')
    era_required_items = json.loads(
        pkgutil.get_data(__name__, file_path).decode())

    for era in EraType:
        cumulative_prereqs += era_required_items[era.value]
        if era == end_era:
            break
    # If we are excluding progressive items, we need to remove them from the list of expected items (TECH_BRONZE_WORKING won't be here since it will be PROGRESSIVE_ENCAMPMENT)
    if exclude_progressive_items:
        flat_progressive_items = get_flat_progressive_items()
        prereqs_without_progressive_items = []
        for item in cumulative_prereqs:
            if item in flat_progressive_items:
                continue
            else:
                prereqs_without_progressive_items.append(item)
        return prereqs_without_progressive_items

    return cumulative_prereqs


def has_required_items(state: CollectionState, era: EraType, player: int, has_progressive_items: bool):
    """ If player has progressive items enabled, it will count how many progressive techs it should have, otherwise return the default array"""
    if has_progressive_items:
        file_path = os.path.join(os.path.dirname(
            __file__), 'data/progressive_districts.json')
        progressive_districts = json.loads(
            pkgutil.get_data(__name__, file_path).decode())

        # Verify we can still reach non progressive items
        all_previous_items_no_progression = get_cumulative_prereqs_for_era(
            era, True)
        if not state.has_all(all_previous_items_no_progression, player):
            return False

        # Verify we have the correct amount of progressive items
        all_previous_items = get_cumulative_prereqs_for_era(
            era, False)
        required_counts: typing.Dict[str, int] = {}

        for key, value in progressive_districts.items():
            required_counts[key] = 0
            for item in all_previous_items:
                if item in value:
                    required_counts[key] += 1

        for key, value in required_counts.items():
            has_amount = state.has(key, player, required_counts[key])
            if not has_amount:
                return False
        return True
    else:
        file_path = os.path.join(os.path.dirname(
            __file__), 'data/era_required_items.json')
        era_required_items = json.loads(
            pkgutil.get_data(__name__, file_path).decode())
        return state.has_all(era_required_items[era.value], player)


def create_regions(world: World, options: CivVIOptions, player: int):
    menu = Region("Menu", player, world.multiworld)
    world.multiworld.regions.append(menu)

    regions: typing.List[Region] = []
    for era in EraType:
        era_region = Region(era.value, player, world.multiworld)
        era_locations = {location.name: location.code for key,
                         location in world.location_by_era[era.value].items()}
        era_region.add_locations(era_locations, CivVILocation)

        regions.append(era_region)
        world.multiworld.regions.append(era_region)

    menu.connect(world.get_region(EraType.ERA_ANCIENT.value))

    has_progressive_items = bool(options.progressive_districts.value)

    world.get_region(EraType.ERA_ANCIENT.value).connect(
        world.get_region(EraType.ERA_CLASSICAL.value), None,
        lambda state: has_required_items(
            state, EraType.ERA_ANCIENT, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_CLASSICAL.value).connect(
        world.get_region(EraType.ERA_MEDIEVAL.value), None, lambda state:  has_required_items(
            state, EraType.ERA_CLASSICAL, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_MEDIEVAL.value).connect(
        world.get_region(EraType.ERA_RENAISSANCE.value), None, lambda state:  has_required_items(
            state, EraType.ERA_MEDIEVAL, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_RENAISSANCE.value).connect(
        world.get_region(EraType.ERA_INDUSTRIAL.value), None, lambda state:  has_required_items(
            state, EraType.ERA_RENAISSANCE, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_INDUSTRIAL.value).connect(
        world.get_region(EraType.ERA_MODERN.value), None, lambda state:  has_required_items(
            state, EraType.ERA_INDUSTRIAL, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_MODERN.value).connect(
        world.get_region(EraType.ERA_ATOMIC.value), None, lambda state:  has_required_items(
            state, EraType.ERA_MODERN, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_ATOMIC.value).connect(
        world.get_region(EraType.ERA_INFORMATION.value), None, lambda state:  has_required_items(
            state, EraType.ERA_ATOMIC, player, has_progressive_items)
    )

    world.get_region(EraType.ERA_INFORMATION.value).connect(
        world.get_region(EraType.ERA_FUTURE.value), None, lambda state:  has_required_items(state, EraType.ERA_INFORMATION, player, has_progressive_items))
