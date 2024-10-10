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

- `schema.sql` defines the database schema and static data using SQL.
- `connect.sh` can be used to connect to the database remotely. 
- `seed.sh` is used to seed the data with master data 


- `generate_dummy_data.py` handles fake data generation and insertion.
- `test_dummy.py` contains unit tests for `generate_dummy_data.py` 

### Generating fake data 
Fake subscriber and article data can be generated for Fox News. This is useful for testing/developing the cloud architecture. The sentiment score is generated using a random truncated distribution, with a mode of `-0.5`. This was chosen, mostly as a placeholder, and for the purpose of testing visualisations. 

The mapping between article headlines and topics can be used for validation later on in the pipeline.

1. Reset the database
2. Run `python3 -m generate_dummy_data.py` to seed the database with dummy data.

### Explanation of political leaning attribute in schema

Within the `source` table of the database schema, there is a column entitled `source_political_leaning`. We thought it important to include this information about the political orientation of a source in the database, so that users of the finished project (including the dashboard) can filter for sources that sit at particular positions on the political spectrum. 

However, politics as a field is not strictly defined, and there is no singular correct way of classifying the political leaning of a newspaper, politician, or article. We decided to use the [Interactive Media Bias Chart](https://adfontesmedia.com/interactive-media-bias-chart/) to classify the political leanings of the newspapers we have chosen for this project. We found this to be most useful as it not only classifies news sources into 'left' and 'right', but also includes information on what sort of content a news source publishes - from "Original Fact Reporting, High Effort", to "Contains Inaccurate / Fabricated Info". We tried to pick sources from opposite ends of the political spectrum, but also sources that published generally reliable content, and we felt that Fox News and Democracy Now! were the best fit. Ad Fontes Media (the creators of the Interactive Media Bias Chart) include more information on how they created the chart and how they did so to mitigate bias as much as possible, which can be found at [this link](https://adfontesmedia.com/is-the-media-bias-chart-biased/).