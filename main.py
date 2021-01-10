import json
from flask import Flask
from flask import request

app = Flask("backend")

# default person
default_person = {
    "uid": 0,
    "surname": "",
    "lastname": "",
    "vulgo": "",
    "balance": 0,
    "statistics": 0,
    "awards": [],
    "cards": []
}

# * file operations


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

# * system requests


@app.route('/')
def test():
    # test
    return "hello world"

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
    # return people list
    if request.method == 'GET':
        found_person = find_person_by_uid(int(uid))
        if found_person == {}:
            return ("person with uid "+uid+" not found", 404)
        else:
            return found_person

    # updates person, identified by uid
    elif request.method == 'PUT':
        person_dict = request.get_json(force=True)
        found = update_person(int(uid), person_dict)
        if found:
            return ("", 204)
        else:
            return (uid + " not found", 404)

    # removes person with uid from database
    if request.method == 'DELETE':
        remove_person(int(uid))
        return ("", 204)


@app.route('/people/by_card/<c_uid>', methods=['GET'])
def people_by_card(c_uid):
    # return people list
    if request.method == 'GET':
        found_person = find_person_by_card(c_uid)
        if found_person == {}:
            return ("person with card id "+c_uid+" not found", 404)
        else:
            return found_person


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5080, threaded=False)
