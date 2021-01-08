# Backend

## API

### System

#### GET
`/shutdown` attempts a backup and shuts down the raspberry pi

*no response*

`/reboot` attempts a backup and reboots the raspberry pi

*no response*

`/backup` attempts a backup. Returns status code `204` for success, and `503` if there was no connection to the backup server.

*empty response*

`/wifis` returns a list of all installed wifis

*response payload*:
```json
{
    "wifis": 
    [
        {
            "id": 0, 
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ],
}
```

`/wifi/{id}` returns the wifi with `id`

*response payload*:
```json
{
    "wifis": 
    [
        {
            "id": 0, 
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ],
}
```

#### POST
`/wifi` creates a new wifi. The next available `id` is chosen by the server. All fields are optional. Returns the `id` of the newly created wifi. Installs all wifis

*request payload*:
```json
{
    "id": 0, // optional, is not used
    "ssid": "", // first value to update
    "password": "" // second value to update
}
```

#### PUT
`/wifi/{id}` updates all fields **except** `id` of the wifi with `id`

*request payload*:
```json
{
    "id": 0, // optional, is not used
    "ssid": "LMS", // first value to update
    "password": "********" // second value to update
}
```

#### DELETE
`/wifi/{id}` deletes the wifi with `id`.

### RFID

#### GET
`/rfid` reads the RFID card and returns the current `uid`. The request in non-blocking

*response payload (if found)*:
```json
{
    "uid": "4589A3FE"
}
```

*response payload (if not found)*:
```json
{
    "uid": null
}
```

### People
All people are identified via their `id`.

#### GET

`/people` returns a list of all people

*response payload*:
```json
[
    {
        // person
    },
]
```
`/people/by_uid/{uid}` returns the person with the `uid` in their `cards` list.

*response payload*:
```json
{
    "id": 0,
    "surname": "Noah",
    "lastname": "Zarro",
    "vulgo": "Calmo",
    "balance": 500,
    "statistics": 27,
    "awards":
    [
        1,
        4,
        5
    ],
    "cards":
    [
        "F5E355A788B132",
        "4589A3FE"
    ]
}
```

`/people/{id}` returns the person with `id`.

*response payload*:
```json
{
    "id": 0,
    "surname": "Noah",
    "lastname": "Zarro",
    "vulgo": "Calmo",
    "balance": 500,
    "statistics": 27,
    "awards":
    [
        1,
        4,
        5
    ],
    "cards":
    [
        "F5E355A788B132",
        "4589A3FE"
    ]
}
```

#### POST
`/people` creates a new person. The next available `id` is chosen by the server. All fields are optional. Returns the `id` of the newly created person.

*request payload*:
```json
    {
        "id": 0, // optional, not used 
        "surname": "", // default
        "lastname": "", // default
        "vulgo": "", // default
        "balance": 0, // default
        "statistics": 0, // default
        "awards": [], // default
        "cards": [] //default
    }
```

#### PUT
`/people/{id}` updates all fields **except** `id` of the person with `id`

*request payload*:
```json
{
    "id": 0, // optional, is not used
    "balance": 525, // first value to update
    "statistics": 28 // second value to update
}
```
`/people/update_id/{id}` updates **only** the `id` field of the person with `id`.

*request payload*:
```json
{
    "id": 5, // new id
}
```

#### DELETE
`/people/{id}` deletes the person with `id`.


## Database

All persistent data is saved in JSON files. 

### Personal Data
```json
[ // list of persons
    {
        "id": 0, // unique identifier 
        "surname": "Noah",
        "lastname": "Zarro",
        "vulgo": "Calmo",
        "balance": 500, // balance in Rp
        "statistics": 27, // number of bought items
        "awards": // list of achieved awards
        [
            1,
            4,
            5
        ],
        "cards": // list of associated RFID card UIDs in HEX format, lengths differ (4, 7 or 10 bytes)
        [
            "F5E355A788B132",
            "4589A3FE"
        ]

    }
]
```

### Achievements
```json
[ // list of possible achievements
    {
        "id": 0,
        "name": "Erstes Pör",
        "description": "Du hast dein erstes Bier gesufft!",
        "image": "first.png"
    }
]
```

### Settings
```json
{
    "wifis": 
    [ // list of all wifis to connect
        {
            "id": 0, // unique identifier
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ],
    "next_person_id": 1, // next id to assign to a person
    "next_wifi_id": 1 // next id to assign to a wifi
}
```
## RFID

The server uses [this library](https://github.com/pimylifeup/MFRC522-python) to read the RFID card.

It only uses the `read_id_no_block` function

## System
The server is able to do the following tasks:
- `shutdown` shuts the raspberry pi down
- `reboot` reboots the raspberry pi
- `backup` attempts a backup
- `wifi` updates the raspberry pi's wifi configuration