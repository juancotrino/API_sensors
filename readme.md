# API SENSOR INTERACTION
## Description

This library corresponds to an assignment given by the company 720° in the recruitment process for the position of software developer.

## Aproach

For the development of the API, all points required in the assignment have been taken into account. In addition, the following assumptions have been made:

- The sensors won't fail in sending data to the API.
- The measurements are delivered to the API at least every minute.
- The data sent by the sensors will have resolution of 1 minute, no less.
- The maximum resolution that the user can input for the time parameters is 1 minute.
- One sensor is capable to take multiple types of measurements (parameters).
- The user will always chose a time window available on the database.
- The API will run locally connected to a local server, no containers were asked.

It should be clarified that these assumptions make error handling less relevant under ideal conditions. Error handling was not mentioned in the assignment, so not much emphasis was placed on it during the development of the tool.

## Installation

Simply create a local virtual environment with Python 3.8.13 in a new directory, and from there install it by executing the following command:

```pip install -r requirements.txt````

## PostgreSQL server acces configuration

Please edit the file `local_settings.py` with your respective credentials to connect to a PostgreSQL server.

## Running the API

Please `cd`into the directory of the project, and from there execute the following command:

```python main.py````

Then open this link[http://127.0.0.1:8000/docs] and follow the instructions of the end points.

## Privacy

The original assignment won't be share here due to possible privacy requirements of the company 720°.
