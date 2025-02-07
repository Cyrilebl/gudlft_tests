import os
import json


def load_json(file_name):
    file_path = os.path.join("data", file_name)
    with open(file_path) as file:
        return json.load(file)


def load_clubs():
    return load_json("clubs.json")["clubs"]


def load_competitions():
    return load_json("competitions.json")["competitions"]
