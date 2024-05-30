import json
import os
import pkgutil
from typing import List
from ..Enum import EraType
from ..ProgressiveDistricts import convert_items_to_have_progression
from . import CivVITestBase


def collect_items_for_era(test, era: EraType) -> None:
    file_path = os.path.join('..', 'data', 'era_required_items.json')
    era_required_items = json.loads(
        pkgutil.get_data(__name__, file_path).decode())
    test.collect_by_name(era_required_items[era.value])


def collect_items_for_era_progressive(test, era: EraType) -> None:
    file_path = os.path.join('..', 'data', 'era_required_items.json')
    era_progression_items = json.loads(
        pkgutil.get_data(__name__, file_path).decode())
    progressive_items = convert_items_to_have_progression(
        era_progression_items[era.value])
    test.collect_by_name(progressive_items)


class TestNonProgressiveRegionRequirements(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "none",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "false",
    }

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))


class TestNonProgressiveRegionRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "none",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        collect_items_for_era(self, EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))


class TestProgressiveDistrictRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "districts_only",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))
        collect_items_for_era_progressive(self, EraType.ERA_ANCIENT)

        collect_items_for_era_progressive(self, EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))

class TestProgressiveDistrictRequirements(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "districts_only",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "false",
    }

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))
        collect_items_for_era_progressive(self, EraType.ERA_ANCIENT)

        collect_items_for_era_progressive(self, EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        collect_items_for_era_progressive(self, EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))


class TestProgressiveEraRequirements(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "eras_and_districts",
        "death_link": "false",
        "death_link_effect": "unit_killed"
    }

    def test_eras_are_accessible_with_progressive_eras(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["PROGRESSIVE_ERA"])

        def check_eras_accessible(eras: List[EraType]):
            for era in EraType:
                if era in eras:
                    self.assertTrue(state.can_reach(
                        era.value, "Region", self.player))
                else:
                    self.assertFalse(state.can_reach(
                        era.value, "Region", self.player))

        progresive_era_item = self.get_item_by_name("PROGRESSIVE_ERA")
        accessible_eras = [EraType.ERA_ANCIENT]
        check_eras_accessible(accessible_eras)

        # Classical era requires 2 progressive era items
        self.collect(progresive_era_item)
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_CLASSICAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MEDIEVAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_RENAISSANCE]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INDUSTRIAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MODERN]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_ATOMIC]
        check_eras_accessible(accessible_eras)

        # Since we collect 2 in the ancient era, information and future era have same logic requirement
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INFORMATION]
        accessible_eras += [EraType.ERA_FUTURE]
        check_eras_accessible(accessible_eras)


class TestProgressiveEraRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "eras_and_districts",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_with_progressive_eras(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["PROGRESSIVE_ERA"])

        def check_eras_accessible(eras: List[EraType]):
            for era in EraType:
                if era in eras:
                    self.assertTrue(state.can_reach(
                        era.value, "Region", self.player))
                else:
                    self.assertFalse(state.can_reach(
                        era.value, "Region", self.player))

        progresive_era_item = self.get_item_by_name("PROGRESSIVE_ERA")
        accessible_eras = [EraType.ERA_ANCIENT]
        check_eras_accessible(accessible_eras)

        # Classical era requires 2 progressive era items
        self.collect(progresive_era_item)
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_CLASSICAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MEDIEVAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_RENAISSANCE]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INDUSTRIAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MODERN]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_ATOMIC]
        check_eras_accessible(accessible_eras)

        # Since we collect 2 in the ancient era, information and future era have same logic requirement
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INFORMATION]
        accessible_eras += [EraType.ERA_FUTURE]
        check_eras_accessible(accessible_eras)
