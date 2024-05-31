from ..Locations import get_boost_data
from . import CivVITestBase


class TestBoostsanityIncluded(CivVITestBase):
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "boostsanity": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "false",
        "pre_hint_items": "all",
    }

    def test_goody_huts_get_included(self) -> None:
        self.test_fill()
        locations = self.multiworld.get_locations(self.player)
        found_locations = 0
        for location in locations:
            if "BOOST" in location.name != -1:
                found_locations += 1
        num_boost_locations = len(get_boost_data())
        self.assertEqual(found_locations, num_boost_locations)


class TestBoostsanityExcluded(CivVITestBase):
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "boostsanity": "false",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "false",
        "pre_hint_items": "all",
    }

    def test_goody_huts_are_not_included(self) -> None:
        self.test_fill()
        locations = self.multiworld.get_locations(self.player)
        found_locations = 0
        for location in locations:
            if "BOOST" in location.name != -1:
                found_locations += 1
        self.assertEqual(found_locations, 0)
