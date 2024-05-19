from BaseClasses import ItemClassification
from . import CivVITestBase


class TestGoodyHutsIncluded(CivVITestBase):
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "true",
        "pre_hint_items": "all",
    }

    def test_goody_huts_get_included(self) -> None:
        self.test_fill()
        expected_goody_huts = 10
        found = 0
        for i in range(expected_goody_huts):
            location = self.multiworld.get_location(f"GOODY_HUT_{i + 1}", self.player)
            self.assertEqual(location.item.classification, ItemClassification.filler)
            found += 1
        self.assertEqual(found, expected_goody_huts)


class TestGoodyHutsExcluded(CivVITestBase):
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "false",
        "pre_hint_items": "all",
    }

    def test_goody_huts_are_not_included(self) -> None:
        self.test_fill()
        found_goody_huts = 0
        for location in self.multiworld.get_locations(self.player):
            if location.name.startswith("GOODY_HUT_"):
                found_goody_huts += 1
        self.assertEqual(found_goody_huts, 0)
