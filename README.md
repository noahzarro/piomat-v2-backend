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
```jsonc
{
    "wifis": 
    [
        {
            "ssid": "Mutter von Niki Lauda",
            "password": "********"
        }
    ]
}
```

`/wifi/{ssid}` returns the wifi with `ssid`

*response payload*:
```jsonc
{
    "ssid": "Mutter von Niki Lauda",
    "password": "********"
}
```

#### POST
`/wifi` creates a new wifi and installs the wifi list. If it does already exist, it is updated

*request payload*:
```jsonc
{
    "ssid": "", // first value to update
    "password": "" // second value to update
}
```

*response payload*:
```jsonc
{
    "update": true // true is wifi already existed, otherwise false
}
```

#### PUT
`/wifi/{ssid}` updates all fields **except** `ssid` of the wifi with `uid`

*request payload*:
```jsonc
{
    "ssid": "LMS", // gets not updated
    "password": "********" // second value to update
}
```

#### DELETE
`/wifi/{ssid}` deletes the wifi with `ssid`.

### RFID

#### GET
`/rfuid` reads the RFID card and returns the current `c_uid`. The request is non-blocking, i.e. it does not block until a card appears to the reader.

*response payload (if found)* with status code `200`:
```jsonc
{
    "c_uid": "4589A3FE"
}
```

*if not found*: fail with status code `404`


### People
All people are uidentified via their `uid`.

#### GET

`/people` returns a list of all people

*response payload*:
```jsonc
{
    "people":
    [
        {
            // person
        },
    ]
}
```
`/people/by_card/{c_uid}` returns the person with the `c_uid` in their `cards` list.

*response payload*:
```jsonc
{
    "uid": 0,
    "surname": "Noah",
    "lastname": "Zarro",
    "vulgo": "Calmo",
    "balance": 500,
    "today": 3,
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
```jsonc
{
    "uid": 0,
    "surname": "Noah",
    "lastname": "Zarro",
    "vulgo": "Calmo",
    "balance": 500,
    "today": 3,
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
```jsonc
    {
        "uid": 0, // optional, not used 
        "surname": "", // default
        "lastname": "", // default
        "vulgo": "", // default
        "balance": 0, // default
        "today": 0, // default
        "statistics": 0, // default
        "awards": [], // default
        "cards": [] //default
    }
```
*response payload*:
```jsonc
{
    "uid": 0 // newly assigned uid
}
```

#### PUT
`/people/{uid}` updates all fields **except** `uid` of the person with `uid`

*request payload*:
```jsonc
{
    "uid": 0, // optional, is not used
    "balance": 525, // first value to update
    "statistics": 28 // second value to update
}
```

#### DELETE
`/people/{uid}` deletes the person with `uid`.

`/people/new_day` resets everybody's `today` value.

### Miscellaneous

#### GET

`/quote` returns a random quote

*response payload*:
```jsonc
{
    "quote": "actual_quote",
    "author": "actual_author"
}
```

## Database

All persistent data is saved in JSON files. 

### Personal Data

Note that `uid` 0 is reserved for `Master`

```jsonc
[ // list of persons
    {
        "uid": 1, // unique uidentifier 
        "surname": "Noah",
        "lastname": "Zarro",
        "vulgo": "Calmo",
        "balance": 500, // balance in Rp
        "today": 3,  // number of bought items today
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
```jsonc
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

Note that `next_person_uid` must be set to 1 at the beginning, to save 0 for `Master`

```jsonc
{
    "wifis": 
    [ // list of all wifis to connect
        {
            "ssid": "Mutter von Niki Lauda", // should already be unique
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