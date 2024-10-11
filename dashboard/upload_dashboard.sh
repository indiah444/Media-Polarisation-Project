source .env

EC2_USER="ec2-user"
DASHBOARD_DIR="~/dashboard"

scp -i "$KEY_PATH" db_functions.py dashboard.py requirements.txt .env $EC2_USER@$EC2_HOST:$DASHBOARD_DIR/

ssh -i "$KEY_PATH" $EC2_USER@$EC2_HOST << EOF
    cd $DASHBOARD_DIR
    
    # Check if port 8501 is in use and kill any processes using it
    if lsof -i :8501; then
        echo "Killing processes using port 8501"
        fuser -k 8501/tcp
    else
        echo "No processes are using port 8501"
    fi
    
    # Create a Python virtual environment and install dependencies
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
    echo "Running Streamlit"
    streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
EOF