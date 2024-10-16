# 🗄️ The Database
This folder contains the schema and python script to seed the database with initial static data as well as the option to insert dummy data.

## 📋 Overview 
The database created is a PostgreSQL database, hosted on an AWS RDS instance.

## 🛠️ Prerequisites
- **AWS RDS (PostgreSQL)** database running.

Optional:
- **Python** installed (For seeding dummy data)

## ⚙️ Setup
1. Create a `.env` file and fill with the following variables
    ```env
    # Database Configuration
    DB_HOST=<the-RDS-host-address>
    DB_PORT=<the-RDS-port-number>
    DB_NAME=<the-RDS-name>
    DB_USER=<the-RDS-username>
    DB_PASSWORD=<the-RDS-password>
    ```
2. Initialise and seed the database using:
    ```bash
    bash seed.sh
    ```
    This will initialise the database according to the schema.sql file:
    - Create the necessary tables
    - Seed the database with fixed data

### ✨ Generating fake data (**Optional**)
Fake subscriber and article data can be generated for Fox News. This is useful for testing/developing the cloud architecture. The sentiment score is generated using a random truncated distribution, with a mode of `-0.5`. This was chosen, mostly as a placeholder, and for the purpose of testing visualisations. 

The mapping between article headlines and topics can be used for validation later on in the pipeline.

1. Creating and activating virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Run the dummy data generation and insertion:
    ```bash
    python3 generate_dummy_Data.py
    ```

## 📁 Files 
- `schema.sql` defines the database schema and static data using SQL.
- `connect.sh` can be used to connect to the database remotely. 
- `seed.sh` is used to seed the data with master data 
- `generate_dummy_data.py` handles fake data generation and insertion.
- `test_dummy.py` contains unit tests for `generate_dummy_data.py` 

### ✅ Test coverage
To generate a detailed test report:
```bash
pytest -vv
```
To include coverage results:
```bash
pytest --cov -vv
```

## 💬 Explanation of political leaning attribute in schema
Within the `source` table of the database schema, there is a column entitled `source_political_leaning`. We thought it important to include this information about the political orientation of a source in the database, so that users of the finished project (including the dashboard) can filter for sources that sit at particular positions on the political spectrum. 

However, politics as a field is not strictly defined, and there is no singular correct way of classifying the political leaning of a newspaper, politician, or article. We decided to use the [Interactive Media Bias Chart](https://adfontesmedia.com/interactive-media-bias-chart/) to classify the political leanings of the newspapers we have chosen for this project. We found this to be most useful as it not only classifies news sources into 'left' and 'right', but also includes information on what sort of content a news source publishes - from "Original Fact Reporting, High Effort", to "Contains Inaccurate / Fabricated Info". We tried to pick sources from opposite ends of the political spectrum, but also sources that published generally reliable content, and we felt that Fox News and Democracy Now! were the best fit. Ad Fontes Media (the creators of the Interactive Media Bias Chart) include more information on how they created the chart and how they did so to mitigate bias as much as possible, which can be found at [this link](https://adfontesmedia.com/is-the-media-bias-chart-biased/).