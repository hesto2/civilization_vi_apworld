import json
import os
import pkgutil
from ..Enum import EraType
from ..ProgressiveItems import convert_items_to_have_progression
from . import CivVITestBase


class TestNonProgressiveRegionRequirements(CivVITestBase):
    options = {
        "progressive_districts": "false"
    }

    def collect_items_for_era(self, era: EraType) -> None:
        file_path = os.path.join(os.path.dirname(
            __file__), '../data/era_required_items.json')
        era_required_items = json.loads(
            pkgutil.get_data(__name__, file_path).decode())
        self.collect_by_name(era_required_items[era.value])

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))


class TestProgressiveRegionRequirements(CivVITestBase):
    options = {
        "progressive_districts": "true"
    }

    def collect_items_for_era_progressive(self, era: EraType) -> None:
        file_path = os.path.join(os.path.dirname(
            __file__), '../data/era_required_items.json')
        era_progression_items = json.loads(
            pkgutil.get_data(__name__, file_path).decode())
        progressive_items = convert_items_to_have_progression(
            era_progression_items[era.value])
        self.collect_by_name(progressive_items)

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))
        self.collect_items_for_era_progressive(EraType.ERA_ANCIENT)

        self.collect_items_for_era_progressive(EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        self.collect_items_for_era_progressive(EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))
