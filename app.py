# Import necessary modules
from flask import Flask, render_template, request, redirect, session, url_for
import boto3  # AWS SDK for Python

# Initialize the Flask app
app = Flask(__name__)

# Secret key for session management (IMPORTANT: Change this in production)
app.secret_key = 'your-secret-key' 

# -----------------------
# Define user credentials
# -----------------------
# These are hardcoded users for login
USERS = {
    'admin': 'adminpass',
    'muneeb': '321@pass',
    'ibad': '623@pass',
    'jameel': '338@pass',
    'anas': '648@pass'
}

# ---------------------------------------------------------
# EC2 instances categorized by AWS region and user-friendly name
# ---------------------------------------------------------
INSTANCES = {
    "ap-south-1": {
        "new-encoder1": "i-0646b5c0e1d41d71c",
        "new-encoder2": "i-094a670fd2feaab0d",
        "serieA-1": "i-0b693d7345d5bea7d",
        "serieA-2": "i-0349c5576161f6c31",
        "wowza-mumbai": "i-0b92b97d1897ee219"
    },
    "ap-southeast-1": {
        "ec2-300": "i-03ca651cc24e9b31e",
        "ec2-301": "i-0b5e728a720a49686",
        "ec2-303": "i-0aa5bf269d06a1b05",
        "ec2-304": "i-0f778dfe642d95d16",
        "ec2-305": "i-0c18b8052793cd987",
        "EPL-1-bangladesh": "i-01bac8b690b47a351",
        "EPL-2-bangladesh": "i-0b10a6fec5136ce17",
        "EPL-3-bangladesh": "i-01088a81128e95170", 
        "mypro-2": "i-00570b0dd329ba551",
        "ucl-ads-2": "i-0e7d862ab48e3fdd7",
        "ucl-ads-3": "i-0da9136038b7ba27e",
        "wowza-singapure": "i-0af589e812a122419"
    },
    "me-central-1": {
        "afc 100": "i-047be7c1a79c06ff7",
        "afc 101": "i-0055c1759b23d60d3",
        "afc 102": "i-051f733166dcac4e7",
        "afc 103": "i-08aefc7fe0888c1fb",
        "afc 105": "i-0e88d7770c5e53f53",
        "afc 106": "i-099ae0dba1311bccc",
        "ec2-encoder200": "i-07c15a6288a6d7920",
        "windows+obs": "i-0827154d37577422e",
        "windows+obs2": "i-0f61b85e5f08b3555",
        "wowza-uae": "i-0369006d658944e62"
    },
    "me-south-1": {
        "wowza-bahrain": "i-0e19dc5a07bb729a2"
    }
}


# ----------------------------------------------------------
# Create boto3 EC2 clients for each region
# ----------------------------------------------------------
ec2_clients = {
    region: boto3.client('ec2', region_name=region)
    for region in INSTANCES
}

# ----------------------------------------------------------
# Route for Login Page
# ----------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get credentials from the login form
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate credentials
        if username in USERS and USERS[username] == password:
            session['user'] = username  # Start user session
            return redirect(url_for('index'))  # Redirect to dashboard
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')  # GET request

# ----------------------------------------------------------
# Route for Logout
# ----------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove session
    return redirect(url_for('login'))  # Redirect to login page

# ----------------------------------------------------------
# Main Dashboard Route
# ----------------------------------------------------------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirect if not logged in

    instance_states = {}

    # Loop through each region and its instances
    for region, machines in INSTANCES.items():
        client = ec2_clients[region]  # Get EC2 client for the region
        response = client.describe_instance_status(IncludeAllInstances=True)

        # Map instance ID to current status (e.g., running, stopped)
        status_map = {
            i['InstanceId']: i['InstanceState']['Name']
            for i in response['InstanceStatuses']
        }

        # Store status for each instance in this region
        instance_states[region] = {
            name: status_map.get(instance_id, 'unknown')  # Default to 'unknown'
            for name, instance_id in machines.items()
        }

    # Render dashboard
    return render_template(
        'index.html',
        instances=INSTANCES,
        instance_states=instance_states,
        user=session['user']
    )

# ----------------------------------------------------------
# Route to Start an EC2 Instance
# ----------------------------------------------------------
@app.route('/start/<region>/<instance_id>', methods=['POST'])
def start_instance(region, instance_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    ec2_clients[region].start_instances(InstanceIds=[instance_id])
    return redirect('/')  # Refresh dashboard

# ----------------------------------------------------------
# Route to Stop an EC2 Instance
# ----------------------------------------------------------
@app.route('/stop/<region>/<instance_id>', methods=['POST'])
def stop_instance(region, instance_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    ec2_clients[region].stop_instances(InstanceIds=[instance_id])
    return redirect('/')  # Refresh dashboard

# ----------------------------------------------------------
# Run the Flask app on all network interfaces at port 5000
# ----------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
