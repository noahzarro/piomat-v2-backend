# Backend

## API

### System

#### GET
`/` for testing purposes, returns `hello world`

`/shutdown` attempts a backup and shuts down the raspberry pi

*no response*

`/reboot` attempts a backup and reboots the raspberry pi

*no response*

`/backup` attempts a backup. Returns status code `204` for success, and `503` if there was no connection to the backup server.

*empty response*

`/success` lights the green LED for a short amount of time and plays a short buzzer sound.

`/failure` lights the red LED for a short amount of time and plays the buzzer a 3 times.

`/wifis` returns a list of all installed wifis

*response payload*:
```json
{
    "wifis": 
    [
        {
            "uid": 0, 
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ],
}
```

`/wifi/{uid}` returns the wifi with `uid`

*response payload*:
```json
{
    "wifis": 
    [
        {
            "uid": 0, 
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ],
}
```

#### POST
`/wifi` creates a new wifi. The next available `uid` is chosen by the server. All fields are optional. Returns the `uid` of the newly created wifi. Installs all wifis

*request payload*:
```json
{
    "uid": 0, // optional, is not used
    "ssid": "", // first value to update
    "password": "" // second value to update
}
```

#### PUT
`/wifi/{uid}` updates all fields **except** `uid` of the wifi with `uid`

*request payload*:
```json
{
    "uid": 0, // optional, is not used
    "ssid": "LMS", // first value to update
    "password": "********" // second value to update
}
```

#### DELETE
`/wifi/{uid}` deletes the wifi with `uid`.

### RFID

#### GET
`/rfuid` reads the RFID card and returns the current `c_uid`. The request in non-blocking

*response payload (if found)*:
```json
{
    "c_uid": "4589A3FE"
}
```

*response payload (if not found)*:
```json
{
    "c_uid": null
}
```

### People
All people are uidentified via their `uid`.

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
`/people/by_card/{c_uid}` returns the person with the `c_uid` in their `cards` list.

*response payload*:
```json
{
    "uid": 0,
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

`/people/{uid}` returns the person with `uid`.

*response payload*:
```json
{
    "uid": 0,
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
`/people` creates a new person. The next available `uid` is chosen by the server. All fields are optional. Returns the `uid` of the newly created person.

*request payload*:
```json
    {
        "uid": 0, // optional, not used 
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
`/people/{uid}` updates all fields **except** `uid` of the person with `uid`

*request payload*:
```json
{
    "uid": 0, // optional, is not used
    "balance": 525, // first value to update
    "statistics": 28 // second value to update
}
```
`/people/update_uid/{uid}` updates **only** the `uid` field of the person with `uid`.

*request payload*:
```json
{
    "uid": 5, // new uid
}
```

#### DELETE
`/people/{uid}` deletes the person with `uid`.


## Database

All persistent data is saved in JSON files. 

### Personal Data
```json
[ // list of persons
    {
        "uid": 0, // unique uidentifier 
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
        "uid": 0,
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
            "uid": 0, // unique uidentifier
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ],
    "next_person_uid": 1, // next uid to assign to a person
    "next_wifi_uid": 1 // next uid to assign to a wifi
}
```
## RFID

The server uses [this library](https://github.com/pimylifeup/MFRC522-python) to read the RFID card.

It only uses the `read_uid_no_block` function

## System
The server is able to do the following tasks:
- `shutdown` shuts the raspberry pi down
- `reboot` reboots the raspberry pi
- `backup` attempts a backup
- `wifi` updates the raspberry pi's wifi configuration