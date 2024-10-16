# 📈 Media Polarisation Dashboard

## 📋 Overview
This folder hosts the Media Polarisation project dashboard. This dashboard showcases several different graphics and data representations of sentiment on different media topics.

## 🛠️ Prerequisites
- **EC2** deployed using [Terraform](../terraform/README.md)
- **PEM Key** generated using [Terraform](../terraform/README.md)  

Optional:
- **Python** installed (For running dashboard locally)

## ⚙️ Setup 

Create a `.env` file with the following environment variables:
```
# AWS Configuration
AWS_ACCESS_KEY_BOUDICCA=<your_aws_access_key>
AWS_ACCESS_SECRET_KEY_BOUDICCA=<your_aws_secret_access_key>
REGION=eu-west-2

# Database Configuration
DB_HOST=<the-RDS-host-address>
DB_PORT=<the-RDS-port-number>
DB_NAME=<the-RDS-name>
DB_USER=<the-RDS-username>
DB_PASSWORD=<the-RDS-password>

# EC2 Configuration
EC2_HOST=<the-ec2-dns-or-ip-address>
KEY_PATH=../terraform/c13-boudicca-mp-key-pair.pem
```

### ☁️ Transferring to EC2
As part of deploying the overall cloud infrastructure, the dashboard files must be transferred to the EC2 and then run in the background:

1. upload and upload the application:
    ```bash
    bash upload_dashboard.sh
    ```
    This will:
    - Transfer the dashboarding files
    - Run the streamlit dashboard
2. You can exit the EC2 terminal by pressing `CTRL + c` buttons together

### 💻 Running Locally (MacOS)
The daily email generator can also be ran locally by:

1. Creating and activating virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
3. Running the dashboard:
    ```bash
    streamlit run Home.py
    ```

## 📁 Files
- `db_functions.py`: Where you can put any functions that interact with the database.
- `d_graphs.py`: Where you can put any functions that create graphs.
- `pages` folder: Where you can put your dashboard page. Name it what you want it to be in the side bar, e.g. `Topic_Filter.py` shows as Topic Filter
- Create any other files that you need!

### ✅ Test coverage
To generate a detailed test report:
```bash
pytest -vv
```
To include coverage results:
```bash
pytest --cov -vv
```
