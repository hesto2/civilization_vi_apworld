import json


_cache = {}


def _get_data(key: str):
    global _cache
    if key not in _cache:
        with open(f"worlds/civ_6/data/{key}.json") as f:
            _cache[key] = json.load(f)
    return _cache[key]


def get_boosts_data():
    return _get_data("boosts")


def get_era_required_items_data():
    return _get_data("era_required_items")


def get_existing_civics_data():
    return _get_data("existing_civics")


def get_existing_techs_data():
    return _get_data("existing_tech")


def get_goody_hut_rewards_data():
    return _get_data("goody_hut_rewards")


def get_new_civic_prereqs_data():
    return _get_data("new_civic_prereqs")


def get_new_civics_data():
    return _get_data("new_civics")


def get_new_tech_prereqs_data():
    return _get_data("new_tech_prereqs")


def get_new_techs_data():
    return _get_data("new_tech")


def get_progressive_districts_data():
    return _get_data("progressive_districts")
