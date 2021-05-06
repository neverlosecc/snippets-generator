import json
import logging
import pathlib

import requests

from . import Generator
from . import Parser

logging.basicConfig(level=logging.INFO)

session = requests.Session()
session.headers = {"Cache-Control": "no-cache"}

with open(str(pathlib.Path(__file__).parent / "config.json"), "r") as f:
    config = json.loads(f.read())

additions = {}
for addition_key in config["additions"].keys():
    addition_value = config["additions"][addition_key]
    for addition in addition_value:
        additions[addition] = addition_key

base_file_url = "https://raw.githubusercontent.com/{}/{}/master/".format(
    config["owner"], config["repo"]
)
tree = session.get(
    "https://api.github.com/repos/{}/{}/git/trees/master?recursive=1".format(
        config["owner"], config["repo"]
    ),
)
tree = tree.json()["tree"]

files = []

for file in tree:
    if "developers" not in file["path"]:
        continue

    if "README.md" in file["path"] or "SUMMARY.md" in file["path"]:
        continue

    if not file["path"].endswith(".md"):
        continue

    if "developers/tables/" in file["path"]:
        files.append({"path": file["path"], "is_table": True})
    elif "developers/classes/" in file["path"]:
        files.append({"path": file["path"], "is_table": False})
    else:
        for key in additions.keys():
            if key in file["path"]:
                files.append(
                    {
                        "path": file["path"],
                        "is_table": True,
                        "table_name": additions[key],
                    }
                )

for file in files:
    if (
            "c_base" in file["path"] or "IGameEvent" in file["path"] or "ConVar" in file["path"]
    ):  # TODO: Fix globalname searcher to avoid this checks
        continue
    tbl_name = None
    if "table_name" in file.keys():
        tbl_name = file["table_name"]

    Parser.parse_content(
        file["path"],
        session.get(base_file_url + file["path"]).text,
        file["is_table"],
        tbl_name,
    )

Generator.get().generate()
Generator.get().write("output.json")
