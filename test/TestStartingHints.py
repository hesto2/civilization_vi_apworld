from BaseClasses import ItemClassification
from ..Enum import CivVICheckType
from . import CivVITestBase

class TestStartingHints(CivVITestBase):
    options = {
      "progressive_eras": "true",
      "death_link": "true",
      "death_link_effect": "unit_killed",
      "progressive_districts": "true",
      "pre_hint_items": "all",
    }

    def test_all_tech_civic_items_are_hinted_default(self) -> None:
        self.test_fill()
        start_location_hints = self.world.options.start_location_hints.value
        for location_name, location_data in self.world.location_table.items():
            if location_data.location_type != CivVICheckType.ERA:
                self.assertTrue(location_name in start_location_hints)
            else:
                self.assertFalse(location_name in start_location_hints)

class TestOnlyProgressionItemsHinted(CivVITestBase):
  options = {
    "progressive_eras": "true",
    "death_link": "true",
    "death_link_effect": "unit_killed",
    "progressive_districts": "true",
    "pre_hint_items": "progression",
  }

  def test_only_progression_items_are_hinted(self) -> None:
      self.test_fill()
      start_location_hints = self.world.options.start_location_hints.value
      for hint in start_location_hints:
          location_data = self.world.get_location(hint)
          self.assertTrue(location_data.item.classification == ItemClassification.progression)

class TestNoJunkItemsHinted(CivVITestBase):
  options = {
    "progressive_eras": "true",
    "death_link": "true",
    "death_link_effect": "unit_killed",
    "progressive_districts": "true",
    "pre_hint_items": "no_junk",
  }

  def test_no_junk_items_are_hinted(self) -> None:
      self.test_fill()
      start_location_hints = self.world.options.start_location_hints.value
      for hint in start_location_hints:
          location_data = self.world.get_location(hint)
          self.assertTrue(location_data.item.classification == ItemClassification.progression or location_data.item.classification == ItemClassification.useful)

class TestNoItemsHinted(CivVITestBase):
  options = {
    "progressive_eras": "true",
    "death_link": "true",
    "death_link_effect": "unit_killed",
    "progressive_districts": "true",
    "pre_hint_items": "none",
  }

  def test_no_items_are_hinted(self) -> None:
      self.test_fill()
      start_location_hints = self.world.options.start_location_hints.value
      self.assertEqual(len(start_location_hints), 0)