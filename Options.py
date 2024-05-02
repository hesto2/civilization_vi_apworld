from dataclasses import dataclass
from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions


class ProgressiveDistricts(DefaultOnToggle):
    """Each tech/civic that would normally unlock a district or district building now has a logical progression. Example: TECH_BRONZE_WORKING is now PROGRESSIVE_ENCAMPMENT"""
    display_name = "Progressive Districts"


class ResearchCostMultiplier(Choice):
    """Multiplier for research cost of techs and civics, higher values make research more expensive. Cheap = 0.5x, Expensive = 1.5x. Default is 1. """
    display_name = "Tech/Civic Cost Multiplier"
    option_cheap = 0.5
    option_default = 1
    option_expensive = 1.5
    default = 1

@dataclass
class CivVIOptions(PerGameCommonOptions):
    progressive_districts: ProgressiveDistricts
    research_cost_multiplier: ResearchCostMultiplier
    death_link: DeathLink
