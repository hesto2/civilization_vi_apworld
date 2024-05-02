"""
Usage: python Tools.py <function_name> <args>
generate_new_techs: Generates AP techs based on the index of the existing techs in the game. Defaults to putting them in ./data/new_tech.json
  args: file_path (optional), output_file (optional)
generate_new_tech_prereqs: Copies the existing prereqs but changes out the names for the associated AP techs
  args: file_path (optional), output_file (optional)
generate_new_prereqs_xml: Takes the data in new_tech_prereqs.json and generates an XML file in the static_mod_files
  args: file_path (optional), output_file (optional)
"""
import json
import sys
from typing import List
import os


def generate_new_techs(file_path, output_file):
    """Generates AP techs based on the index of the existing techs in the game. Defaults to putting them in ./data/new_tech.json"""
    with open(file_path, 'r') as file:
        data = json.load(file)

    with open(output_file, 'w') as output:
        i = 0
        output.write("[\n")
        for item in data:
            # write the item contents to the output file as a json but change the name to be "TECH_AP{index}"
            output.write(json.dumps({"Type": f"TECH_AP{i}", "Cost": item["Cost"],
                         "UITreeRow": item["UITreeRow"], "EraType": item["EraType"]}))
            if i != len(data) - 1:
                output.write(",\n")
            else:
                output.write("\n")
            i += 1
        output.write("]")


def generate_new_civics(file_path, output_file):
    """Generates AP civics based on the index of the existing civics in the game. Defaults to putting them in ./data/new_tech.json"""
    with open(file_path, 'r') as file:
        data = json.load(file)

    with open(output_file, 'w') as output:
        i = 0
        output.write("[\n")
        for item in data:
            # write the item contents to the output file as a json but change the name to be "CIVIC_AP{index}"
            output.write(json.dumps({"Type": f"CIVIC_AP{i}", "Cost": item["Cost"],
                         "UITreeRow": item["UITreeRow"], "EraType": item["EraType"]}))
            if i != len(data) - 1:
                output.write(",\n")
            else:
                output.write("\n")
            i += 1
        output.write("]")


def generate_new_tech_prereqs(file_path, output_file):
    """Copies the existing prereqs but changes out the names for the associated AP techs"""
    with open(file_path, 'r') as file:
        prereq_data = json.load(file)

    with open("./data/new_tech.json", 'r') as file:
        new_tech = json.load(file)

    with open("./data/existing_tech.json", 'r') as file:
        existing_tech = json.load(file)

    with open(output_file, 'w') as output:
        i = 0
        output.write("[\n")
        for item in prereq_data:
            output.write(json.dumps({"Technology": find_new_item_based_on_existing_name(
                item["Technology"], existing_tech, new_tech), "PrereqTech": find_new_item_based_on_existing_name(item["PrereqTech"], existing_tech, new_tech)}))

            if i != len(prereq_data) - 1:
                output.write(",\n")

        # Future techs don't have specific prereqs so we need to add them manually
        i = 0
        for item in new_tech:
            if item["EraType"] == "ERA_FUTURE":
                if i != 0:
                    output.write(",\n")
                output.write(
                    json.dumps({"Technology": item["Type"], "PrereqTech": "TECH_AP60"}))
                i += 1
        output.write("]")


def generate_new_civic_prereqs(file_path, output_file):
    """Copies the existing prereqs but changes out the names for the associated AP civics"""
    with open(file_path, 'r') as file:
        prereq_data = json.load(file)

    with open("./data/new_civics.json", 'r') as file:
        new_civics = json.load(file)

    with open("./data/existing_civics.json", 'r') as file:
        existing_civics = json.load(file)

    with open(output_file, 'w') as output:
        i = 0
        output.write("[\n")
        for item in prereq_data:
            output.write(json.dumps({"Civic": find_new_item_based_on_existing_name(
                item["Civic"], existing_civics, new_civics), "PrereqCivic": find_new_item_based_on_existing_name(item["PrereqCivic"], existing_civics, new_civics)}))

            if i != len(prereq_data) - 1:
                output.write(",\n")

        # Future techs don't have specific prereqs so we need to add them manually
        i = 0
        for item in new_civics:
            if item["EraType"] == "ERA_FUTURE" and item["Type"] != "CIVIC_AP50":
                if i != 0:
                    output.write(",\n")
                output.write(
                    json.dumps({"Civic": item["Type"], "PrereqCivic": "CIVIC_AP50"}))
                i += 1
        output.write("]")


def generate_new_prereqs_xml(output_file):
    """Takes the data in new_tech_prereqs.json and generates an XML file in the static_mod_files. Then takes the existing tech and adds a "tech_blocker" prereq tp each existing one"""
    with open('./data/new_tech_prereqs.json', 'r') as file:
        prereq_tech_data = json.load(file)
    with open("./data/existing_tech.json", 'r') as file:
        existing_tech = json.load(file)
    with open("./data/new_civic_prereqs.json", 'r') as file:
        prereq_civic_data = json.load(file)
    with open("./data/existing_civics.json", 'r') as file:
        existing_civics = json.load(file)

# fmt: off
    with open(output_file, 'w') as output:
        output.write("""
  <?xml version="1.0" encoding="utf-8"?>
  <GameData>
    <TechnologyPrereqs>
                 """)
        for item in prereq_tech_data:
            output.write(f'<Row Technology="{item["Technology"]}" PrereqTech="{item["PrereqTech"]}" />')
            output.write("\n")
        # Add the blocker tech to each existing tech so it can't be researched
        for item in existing_tech:
            output.write(f'<Row Technology="{item["Type"]}" PrereqTech="TECH_BLOCKER" />')
            output.write("\n")
        output.write("""
    </TechnologyPrereqs>
    <CivicPrereqs>\n""")
        for item in prereq_civic_data:
            output.write(f'<Row Civic="{item["Civic"]}" PrereqCivic="{item["PrereqCivic"]}" />')
            output.write("\n")
        # Add the blocker civic to each existing civic so it can't be researched
        for item in existing_civics:
            output.write(f'<Row Civic="{item["Type"]}" PrereqCivic="CIVIC_BLOCKER" />')
            output.write("\n")
        output.write("""</CivicPrereqs>
  </GameData>
    """)
# fmt: on


def find_new_item_based_on_existing_name(existing_name: str, existing_items: List[dict], new_item: List[dict]) -> str:
    for i in range(len(existing_items)):
        if existing_items[i]["Type"] == existing_name:
            return new_item[i]["Type"]
    return ""


# Allow this function to be run from the command line
if __name__ == "__main__":
    existing_tech = "./data/existing_tech.json"
    new_tech = "./data/new_tech.json"
    existing_tech_prereqs = "./data/existing_tech_prereqs.json"
    new_tech_prereqs = "./data/new_tech_prereqs.json"

    existing_civics = "./data/existing_civics.json"
    new_civics = "./data/new_civics.json"
    existing_civic_prereqs = "./data/existing_civic_prereqs.json"
    new_civic_prereqs = "./data/new_civic_prereqs.json"

    new_prereqs_xml = "./static_mod_files/NewPrereqs.xml"

    if len(sys.argv) < 2:
        generate_new_techs(existing_tech, new_tech)
        generate_new_tech_prereqs(existing_tech_prereqs, new_tech_prereqs)

        generate_new_civics(existing_civics, new_civics)
        generate_new_civic_prereqs(existing_civic_prereqs, new_civic_prereqs)

        generate_new_prereqs_xml(new_prereqs_xml)

    else:
        function_name = sys.argv[1]

        if function_name == "generate_new_techs":
            file_path = "./data/existing_tech.json"
            output_file = "./data/new_tech.json"

            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                output_file = sys.argv[3]
            generate_new_techs(file_path, output_file)

        elif function_name == "generate_new_prereqs":
            file_path = "./data/existing_tech_prereqs.json"
            output_file = "./data/new_tech_prereqs.json"

            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                output_file = sys.argv[3]
            generate_new_tech_prereqs(file_path, output_file)

        elif function_name == "generate_new_prereqs_xml":
            file_path = "./data/new_tech_prereqs.json"
            output_file = "./static_mod_files/NewPrereqs.xml"
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                output_file = sys.argv[3]
            generate_new_prereqs_xml(file_path, output_file)

        elif function_name == "generate_new_civics":
            file_path = "./data/existing_civics.json"
            output_file = "./data/new_civics.json"

            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                output_file = sys.argv[3]
            generate_new_civics(file_path, output_file)

        elif function_name == "generate_new_civic_prereqs":
            file_path = "./data/existing_civic_prereqs.json"
            output_file = "./data/new_civic_prereqs.json"

            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                output_file = sys.argv[3]
            generate_new_civic_prereqs(file_path, output_file)
