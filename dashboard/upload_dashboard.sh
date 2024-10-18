source .env
source ec2.env

EC2_USER="ec2-user"
DASHBOARD_DIR="dashboard"
NLTK_DIR="nltk_data"

ssh -i "$KEY_PATH" $EC2_USER@$EC2_HOST << EOF
    # Check and delete the existing dashboard directory
    if [ -d "$DASHBOARD_DIR" ]; then
        echo "Deleting existing dashboard directory"
        rm -rf $DASHBOARD_DIR
    fi
    
    # Check and delete the existing nltk_data directory
    if [ -d "$NLTK_DIR" ]; then
        echo "Deleting existing nltk_data directory"
        rm -rf $NLTK_DIR
    fi
EOF

scp -i "$KEY_PATH" d_graphs.py 1_Home.py verify_identity.py db_functions.py dataframe_functions.py streamlit_components.py requirements.txt $EC2_USER@$EC2_HOST:$DASHBOARD_DIR/
scp -i "$KEY_PATH" -r pages/ $EC2_USER@$EC2_HOST:$DASHBOARD_DIR/

ssh -i "$KEY_PATH" $EC2_USER@$EC2_HOST << EOF
    cd $DASHBOARD_DIR
    
    # Check if port 8501 is in use and kill any processes using it
    if lsof -i :8501; then
        echo "Killing processes using port 8501"
        fuser -k 8501/tcp
    else
        echo "No processes are using port 8501"
    fi

    # Export secret variables
    export AWS_ACCESS_KEY_BOUDICCA=$AWS_ACCESS_KEY_BOUDICCA
    export AWS_ACCESS_SECRET_KEY_BOUDICCA=$AWS_ACCESS_SECRET_KEY_BOUDICCA
    export REGION=$REGION
    export DB_HOST=$DB_HOST
    export DB_PORT=$DB_PORT
    export DB_USER=$DB_USER
    export DB_PASSWORD=$DB_PASSWORD
    export DB_NAME=$DB_NAME
    
    # Create a Python virtual environment and install dependencies
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
    echo "Running Streamlit"
    streamlit run 1_Home.py --server.port 8501 --server.address 0.0.0.0
EOF