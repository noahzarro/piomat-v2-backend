import json
import time
import random
import os
from flask import Flask, send_file
from flask_cors import CORS
from flask import request
import requests

app = Flask("backend")
CORS(app)

# default person
default_person = {
    "uid": 0,
    "surname": "",
    "lastname": "",
    "vulgo": "",
    "balance": 0,
    "today": 0,
    "statistics": 0,
    "awards": [],
    "cards": [],
    "stickers" :
        {
            "collection": [0],
            "selected": 0
        }
}

# * file operations

def get_stickers_list():
    # returns a list of all stickers
    with open("stickers.json") as f:
        return json.load(f)

def get_people_list():
    # returns a list of all people
    with open("people.json") as f:
        return json.load(f)


def set_people_list(people):
    # writes the settings dict
    with open("people.json", "w") as f:
        json.dump(people, f)


def get_settings():
    # returns the settings dict
    with open("settings.json") as f:
        return json.load(f)


def set_settings(settings):
    # writes the settings dict
    with open("settings.json", "w") as f:
        json.dump(settings, f)


def get_quotes_list():
    # returns a list of all quotes
    with open("quotes.json") as f:
        return json.load(f)

# * people operations


def add_person(new_person):
    # saves a new person
    people_list = get_people_list()
    people_list.append(new_person)
    set_people_list(people_list)


def increment_next_person_id():
    # gets and returns the current next_person_uid from the settings file, increments it and saves it again
    settings = get_settings()
    this_id = settings["next_person_uid"]
    settings["next_person_uid"] = this_id+1
    set_settings(settings)
    return this_id


def create_new_person(new_person_dict):
    # assigns a new id to the person and saves it
    new_person = default_person
    new_person.update(new_person_dict)
    new_person["uid"] = increment_next_person_id()
    add_person(new_person)
    return {"uid": new_person["uid"]}


def find_person_by_uid(uid):
    # return person with uid
    people_list = get_people_list()
    for person in people_list:
        if person["uid"] == uid:
            return person
    return {}


def find_person_by_card(c_uid):
    # return person with c_uid in cards list
    people_list = get_people_list()
    for person in people_list:
        for card_uid in person["cards"]:
            if card_uid == c_uid:
                return person
    return {}


def update_person(uid, new_person_dict):
    # updates a person with new values
    people_list = get_people_list()
    found = False
    for person in people_list:
        if person["uid"] == uid:
            person.update(new_person_dict)
            found = True
    set_people_list(people_list)
    return found


def remove_person(uid):
    # removes person with uid from list
    people_list = get_people_list()
    new_list = [person for person in people_list if person["uid"] != uid]
    set_people_list(new_list)


# * misc operations

def get_random_quote():
    # returns a randomly chosen quote
    quotes_list = get_quotes_list()
    return random.choice(quotes_list)


# * system operations

def do_backup():
    backup_data = get_people_list()
    req = requests.post("https://backup.pio-o-mat.ch/backup", json={"backup": backup_data})
    return req.ok

def do_shutdown():
    # TODO
    print("NYI shutdown")


def do_reboot():
    # TODO
    print("NYI reboot")


def do_success():
    # TODO
    print("NYI success")


def do_failure():
    # TODO
    print("NYI failure")

# * wifi operations


def install_wifis():
    # TODO
    print("NYI wifi")


def get_wifi_list():
    # returns current list of wifis
    return get_settings()["wifis"]


def set_wifi_list(new_wifis):
    # overwrites the wifis list in the database with new_wifis
    old_settings = get_settings()
    old_settings["wifis"] = new_wifis
    set_settings(old_settings)


def add_wifi(new_wifi):
    # saves a new wifi
    wifi_list = get_wifi_list()
    wifi_list.append(new_wifi)
    set_wifi_list(wifi_list)


def find_wifi_by_ssid(ssid):
    # return wifi with uid
    wifi_list = get_wifi_list()
    for wifi in wifi_list:
        if wifi["ssid"] == ssid:
            return wifi
    return {}


def update_wifi(ssid, new_wifi_dict):
    # updates a wifi with new values
    wifi_list = get_wifi_list()
    found = False
    for wifi in wifi_list:
        if wifi["ssid"] == ssid:
            wifi.update(new_wifi_dict)
            found = True
    set_wifi_list(wifi_list)
    return found


def remove_wifi(ssid):
    # removes wifi with ssid from list
    wifi_list = get_wifi_list()
    new_list = [wifi for wifi in wifi_list if wifi["ssid"] != ssid]
    set_wifi_list(new_list)


# * system requests


@app.route('/')
def test():
    # test
    return "hello world"


@app.route('/backup')
def backup():
    # backup
    suc = do_backup()
    if suc:
        return ("", 204)
    else:
        return ("", 404)


@app.route('/shutdown')
def shutdown():
    # shutdown
    do_shutdown()
    return ("", 204)


@app.route('/reboot')
def reboot():
    # reboot
    do_reboot()
    return ("", 204)


@app.route('/success')
def success():
    # success
    do_success()
    return ("", 204)


@app.route('/failure')
def failure():
    # failure
    do_failure()
    return ("", 204)

# * rfid requests


@app.route('/rfuid')
def rfuid():
    time.sleep(1)
    if random.random() > 0.5:
        data = {
            "c_uid": "4589A3FE8"  # + str(random.randint(0,10))
        }
        return (data, 200)
    else:
        return ("", 404)

# * people requests


@app.route('/people', methods=['GET', 'POST'])
def people():
    # return people list
    if request.method == 'GET':
        return {"people": get_people_list()}

    # create new people list
    elif request.method == 'POST':
        print(request.get_json(force=True))
        return create_new_person(request.get_json(force=True))


@app.route('/people/<uid>', methods=['GET', 'PUT', 'DELETE'])
def people_uid(uid):
    # return person
    if request.method == 'GET':
        found_person = find_person_by_uid(int(uid))
        if found_person == {}:
            return ("person with uid "+uid+" not found", 404)
        else:
            return found_person

    # updates person, identified by (changes to master are discared)
    elif request.method == 'PUT':
        person_dict = request.get_json(force=True)
        if person_dict["uid"] == 0:
            return ("", 204) # discard changes to master
        found = update_person(int(uid), person_dict)
        if found:
            return ("", 204)
        else:
            return (uid + " not found", 404)

    # removes person with uid from database (changes to master are discared)
    if request.method == 'DELETE':
        if int(uid) == 0:
            return ("", 204) # discard changes to master
        remove_person(int(uid))
        return ("", 204)


@app.route('/people/by_card/<c_uid>', methods=['GET'])
def people_by_card(c_uid):
    # return person
    if request.method == 'GET':
        found_person = find_person_by_card(c_uid)
        if found_person == {}:
            return ("person with card id "+c_uid+" not found", 404)
        else:
            return found_person


@app.route('/people/new_day', methods=['DELETE'])
def people_new_day():
    # return people list
    if request.method == 'DELETE':
        people = get_people_list()
        print(people)
        todays_list = []
        for person in people:
            print(person)
            person["today"] = 0
            todays_list.append(person)
        print("setting list")
        set_people_list(todays_list)
        print("set list")
        return ("", 204)


# * WIFI requests

@app.route('/wifis', methods=['GET'])
def wifis():
    if request.method == 'GET':
        wifis = get_wifi_list()
        return({"wifis": wifis}, 200)


@app.route('/wifi/<ssid>', methods=['GET', 'PUT', 'DELETE'])
def wifi(ssid):
    # return wifi
    if request.method == 'GET':
        found_wifi = find_wifi_by_ssid(ssid)
        if found_wifi == {}:
            return ("wifi with ssid "+ssid+" not found", 404)
        else:
            return found_wifi

    # updates wifi, identified by ssid
    elif request.method == 'PUT':
        wifi_dict = request.get_json(force=True)
        found = update_wifi(ssid, wifi_dict)
        if found:
            return ("", 204)
        else:
            return (ssid + " not found", 404)

    # removes wifi with ssid from database
    if request.method == 'DELETE':
        remove_wifi(ssid)
        return ("", 204)

@app.route('/wifi', methods=['POST'])
def new_wifi():
    if request.method == 'POST':
        wifi_dict = request.get_json(force=True)
        ssid = wifi_dict["ssid"]
        # only add wifi if it does not yet exist
        if find_wifi_by_ssid(ssid) == {}:
            add_wifi(wifi_dict)
            return ({"update": False}, 200)
        else:
            update_wifi(ssid, wifi_dict)
            return ({"update": True}, 200)


# * stickers

def get_sticker_image_file_name(sid):
    stickers = get_stickers_list()
    return stickers[sid]["image"]

def get_sticker_sound_file_name(sid):
    stickers = get_stickers_list()
    return stickers[sid]["sound"]

@app.route('/stickers/image/<sid>', methods=['GET'])
def get_sticker_image(sid):
    file_path = get_sticker_image_file_name(sid)
    return send_file(os.path.join("stickers", file_path))

@app.route('/stickers/sound/<sid>', methods=['GET'])
def get_sticker_sound(sid):
    file_path = get_sticker_sound_file_name(sid)
    return send_file(os.path.join("stickers", file_path))

@app.route('/stickers/name/<sid>', methods=['GET'])
def get_sticker_name(sid):
    stickers = get_stickers_list()
    name =  stickers[sid]["name"]
    return ({"name": name}, 200)


# * misc request


@app.route('/quote', methods=['GET'])
def get_quote():
    return get_random_quote()


if __name__ == '__main__':
    # create json files if they do not exist yet
    if not os.path.exists("people.json"):
        with open("people.json", "w") as f:
            json.dump([{"uid": 0, "surname": "Master", "lastname": "Master", "vulgo": "Master", "balance": 100, "today": 0, "statistics": 0, "awards": [], "cards": ["MASTER"]}], f)
    if not os.path.exists("settings.json"):
        with open("settings.json", "w") as f:
            json.dump({"wifis":[], "next_person_uid": 1, "next_wifi_uid": 1 }, f)
    app.run(host="127.0.0.1", port=5080, threaded=False)
