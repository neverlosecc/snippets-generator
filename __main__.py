from . import *
import requests
import logging
import json


logging.basicConfig(level=logging.INFO)

config = {}
with open("./config.json", "r") as f:
    config = json.loads(f.read())


base_file_url = "https://raw.githubusercontent.com/{}}/{}/master/".format(config["owner"], config["repo"])
tree = requests.get("https://api.github.com/repos/{}/{}/git/trees/master?recursive=1"
                    .format(config["owner"], config["repo"]))
tree = tree.json()["tree"]

files = []

for file in tree:
    if "developers" not in file["path"]:
        continue

    if "classes" not in file["path"] and "tables" not in file["path"]:
        continue

    if "README.md" in file["path"] or "SUMMARY.md" in file["path"]:
        continue

    if not file["path"].endswith(".md"):
        continue

    if "developers/tables/" in file["path"]:
        files.append({"path": file["path"], "is_table": True})
    elif "developers/classes/" in file["path"]:
        files.append({"path": file["path"], "is_table": False})

for file in files:
    if "c_base" in file["path"] or "igameevent" in file["path"]:  # TODO: Fix globalname searcher to avoid this checks
        continue
    Parser.parse_content(file["path"], requests.get(base_file_url + file["path"]).text, file["is_table"])

Generator.get().generate()
Generator.get().write("output.json")
