# The Database

## Overview 
The database created is a PostgreSQL database, hosted on an AWS RDS instance.

## Setup 

1. `python3 -m venv venv` to create a virtual environment.

2. `source venv/bin/activate` to activate the virtual environment.

3. Configure your environment `.env` file:

```sh 
DB_HOST=XXXXXX
DB_PORT=XXXXX
DB_PASSWORD=XXXXXX
DB_USER=XXXXX
DB_NAME=XXXXX
```

4. `pip install -r requirements.txt` 

5. `python3 -m [filename]` can be used to run an individual file

## Files 

- `connect.sh` can be used to connect to the database remotely. 
- `seed.sh` is used to seed the data with master data 


- `generate_dummy_data.py` handles fake data generation and insertion.


### Generating fake data 
Fake subscriber and article data can be generated for Fox News. This is useful for testing/developing the cloud architecture. The sentiment score is generated using a random truncated distribution, with a mode of `-0.5`. This was chosen, mostly as a placeholder, and for the purpose of testing visualisations. 

The mapping between article headlines and topics can be used for validation later on in the pipeline.

1. Reset the database
2. Run `python3 -m generate_dummy_data.py` to seed the database with dummy data.