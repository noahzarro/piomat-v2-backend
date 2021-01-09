import json

from dataclasses import dataclass
from dacite import from_dict
from flask import Flask

app = Flask("backend")


# * datatypes

@dataclass
class Wifi:
    uid: int
    ssid: str
    password: str


@dataclass
class Settings:
    wifis: List[Wifi]
    next_person_uid: int
    next_wifi_uid: int


@dataclass
class Person:
    uid: int
    surname: str
    lastname: str
    vulgo: str
    balance: int
    statistics: int
    awards: List[int]
    cards: List[str]


# * people

def get_people_list():
    # returns a list of all people
    with open("people.json") as f:
        return json.load(f)


def get_settings():
    # returns the settings dict
    with open("settings.json") as f:
        return json.load(f)


def set_settings(settings):
    # writes the settings dict
    with open("settings.json", "w") as f:
        json.dump(settings, f)


def increment_next_person_id():
    # gets and returns the current next_person_uid from the settings file, increments it and saves it again
    settings = get_settings()
    this_id = settings["next_person_uid"]
    settings["next_person_uid"] = this_id+1
    set_settings(settings)
    return this_id


def create_new_person():
    # assigns a new id to the person and saves it
    


# * system requests

@app.route('/')
def test():
    # test
    return "hello world"


@app.route('/people', methods=['GET', 'POST'])
def people():
    # return people list
    if request.method == 'GET':
        return get_people_list()

    # create new people list
    elif request.method == 'POST':
        return create_new_person(request.form)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5080, threaded=False)
