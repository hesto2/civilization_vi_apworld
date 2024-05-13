from ..Enum import CivVICheckType
from . import CivVITestBase


class TestStartingHints(CivVITestBase):
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true"
    }

    def test_all_tech_civic_items_are_hinted_default(self) -> None:
        start_location_hints = self.world.options.start_location_hints.value
        for location_name, location_data in self.world.location_table.items():
            if location_data.location_type != CivVICheckType.ERA:
                self.assertTrue(location_name in start_location_hints)
            else:
                self.assertFalse(location_name in start_location_hints)
