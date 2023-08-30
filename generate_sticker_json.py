import os
import json

start_directory = "stickers"
stickers = {}
next_id = 1

# first create entry according to the mp3 files
for file_name in os.listdir(start_directory):
    if file_name.startswith("default"):
        continue
    if file_name.endswith(".mp3"):
        name = file_name.split(".")[0]
        entry = {"name": name, "sound": file_name}
        stickers[next_id] = entry
        next_id += 1


def get_sid_by_name(name):
    for sid in stickers:
        if stickers[sid]["name"] == name:
            return sid
    print(name + " not found")

def capitalize_name(name: str):
    final_string = ""
    words = name.split("_")
    for word in words:
        final_string += word.capitalize() + " "
    return final_string.strip()

# now add images
for file_name in os.listdir(start_directory):
    if file_name.startswith("default"):
        continue
    if not (file_name.endswith(".mp3")):
        name = file_name.split(".")[0]
        sid = get_sid_by_name(name)
        entry = stickers[sid] 
        entry["image"] = file_name
        stickers[sid] = entry

# capitalize name
for sid in stickers:
    name = stickers[sid]["name"]
    stickers[sid]["name"] = capitalize_name(name)

# save everything
with open("stickers_generated.json", "w") as f:
    json.dump(stickers, f)