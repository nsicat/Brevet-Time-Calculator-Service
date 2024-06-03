# Project 6: Brevet time calculator service

Simple listing service from project 5 stored in MongoDB database.

# Author:

Code given in CS322 class

Edited by Nico Sicat "nsicat@uoregon.edu"

## What is in this repository

Minimal implementation of Docker compose in DockerRestAPI folder, using which can create REST API-based services

## Recap 

Code is reused from project 5 (https://bitbucket.org/sicat-nico/proj5-mongo/). Recall: these functionalities were created from the following project. 

1. Two buttons ("Submit") and ("Display") in the page where you have controle times.
2. On clicking the Submit button, the control times were be entered into the database.
3. On clicking the Display button, the entries from the database were be displayed in a new page.
4. You also handled error cases appropriately.

## Functionality added

This project follows four parts. Values for host and port should be change according to the ports associated in docker-compose file.

* Design RESTful service to expose what is stores in MongoDB. Specifically, we'll use the boilerplate given in DockerRestAPI folder, and create
these following APIs:
    * `http://<host:port>/listAll` should return all open and close times in the database
    * `http://<host:port>/listOpenOnly` should return open times only
    * `http://<host:port>/listCloseOnly` should return close times only

* Design consist of two different representations: one in csv and one in json. For the above three basic APIs, JSON should be your default representation. 
    * `http://<host:port>/listAll/csv` should return all open and close times in CSV format
    * `http://<host:port>/listOpenOnly/csv` should return open times only in CSV format
    * `http://<host:port>/listCloseOnly/csv` should return close times only in CSV format

    * `http://<host:port>/listAll/json` should return all open and close times in JSON format
    * `http://<host:port>/listOpenOnly/json` should return open times only in JSON format
    * `http://<host:port>/listCloseOnly/json` should return close times only in JSON format

* program will also add a query parameter to get top "k" open and close times. For examples, see below.

    * `http://<host:port>/listOpenOnly/csv?top=3` should return top 3 open times only (in ascending order) in CSV format 
    * `http://<host:port>/listOpenOnly/json?top=5` should return top 5 open times only (in ascending order) in JSON format
    * `http://<host:port>/listCloseOnly/csv?top=6` should return top 5 close times only (in ascending order) in CSV format
    * `http://<host:port>/listCloseOnly/json?top=4` should return top 4 close times only (in ascending order) in JSON format


## Data Samples

1. JSON looks like this in the program: 
```json
{
    "begin_date": "2017-01-01",
    "begin_time": "00:00",
    "brevet_distance": "200",
    "data": {
        "close": [
            "Mon 1/1 0:32 ",
            "Mon 1/1 0:44 ",
            "Mon 1/1 1:00 ",
            "Mon 1/1 1:04 "
        ],
        "open": [
            "Mon 1/1 0:14 ",
            "Mon 1/1 0:19 ",
            "Mon 1/1 0:26 ",
            "Mon 1/1 0:28 "
        ]
    }
}

```

2. CSV will look like this in program: 
```csv
brevets/distance, brevets/begin_date, brevets/begin_time, brevets/0/open, brevets/0/close, brevets/1/open, brevets/1/close, brevets/2/open, brevets/2/close, brevets/3/open, brevets/3/close, \n 200, 2017-01-01, 00:00, Mon 1/1 0:14 , Mon 1/1 0:32 Mon 1/1 0:19 , Mon 1/1 0:44 Mon 1/1 0:26 , Mon 1/1 1:00 Mon 1/1 0:28 , Mon 1/1 1:04 
```

### ACP Controle Times
Algorithm followed can be found in (https://rusa.org/pages/acp-brevet-control-times-calculator)

This functionality added in this project is determining the opening and closing times of brevet controls based on specified rules defined in (https://rusa.org/pages/rulesForRiders)

### Rules Followed

* Speed Ranges

| Distance Range (km) | Minimum Speed (km/h) | Maximum Speed (km/h) |
|---------------------|----------------------|----------------------|
| 0 - 200             | 15                   | 34                   |
| 200 - 400           | 15                   | 32                   |
| 400 - 600           | 15                   | 30                   |
| 600 - 1000          | 11.428               | 28                   |
| 1000 - 1300         | 13.333               | 26                   |

* Times are rounded up 

## How to Run:

1. Download this repo 
2. Change directory to DockerRestApi
3. Type in terminal "docker-compose up --build"
    * this is for the first time build
    * this is a command used to start Docker containeres as defined in the docker-compose.yml file
4. The website should be up for usage

5. Go to localhost:8000
6. Input values and hit submit (do not hit display because this will display values and erase the database)
7. Go to localhost:5002 and follow instructions from "Functionality Added" to see representations

### How to Stop:
* docker compose down

### How to start again without rebuilding:
* docker compose up 




