
# AWS EC2 Control Panel (Docker + Flask)

This project provides a simple **web dashboard** to manage AWS EC2 instances across multiple regions.  
It is built with **Flask**, **Boto3**, and **Docker Compose**.

## 🚀 Features
- Login system with multiple users.
- Start and stop EC2 instances directly from a web UI.
- Support for multiple AWS regions.
- Real-time instance status display (running, stopped, pending, etc.).
- Simple deployment with Docker Compose.

---

## 📂 Project Structure
ec2-control-plan-docker-compose/
├── app/ # Flask application
│ ├── app.py # Main Flask app
│ ├── Dockerfile # Docker build file
│ ├── requirements.txt # Python dependencies
│ └── templates/ # HTML templates (login + dashboard)
│ ├── login.html
│ └── index.html
├── docker-compose.yml # Docker Compose configuration
└── README.md # Project documentation


---

## ⚙️ Prerequisites
- Docker & Docker Compose installed
- AWS credentials with EC2 access
- An EC2 instance (or local machine) to host this dashboard

---

## 🔑 Setup AWS Credentials
Create a `.env` file in the project root:

```env
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key

These will be passed into the container by docker-compose.yml.

💡 Tip: If running this inside an AWS EC2 instance, you can also attach an IAM Role instead of using static keys.

🐳 Deployment with Docker Compose

Build and start the container

docker compose up -d --build

http://<your-server-ip>:5006

🌍 Supported AWS Regions & Instances

Instances are pre-defined in app.py. Examples:

🌍 Supported AWS Regions & Instances

Instances are pre-defined in app.py. Examples:

INSTANCES = {
    "ap-south-1": {
        "new-encoder1": "i-0646b5c0e1d41d71c",
        "wowza-mumbai": "i-0b92b97d1897ee219"
    },
    "ap-southeast-1": {
        "ec2-300": "i-03ca651cc24e9b31e",
        "wowza-singapure": "i-0af589e812a122419"
    },
    "me-central-1": {
        "afc 100": "i-047be7c1a79c06ff7"
    },
    "me-south-1": {
        "wowza-bahrain": "i-0e19dc5a07bb729a2"
    }
}
🛠️ Development (without Docker)

Run locally (for debugging):
cd app
pip install -r requirements.txt
python3 app.py

The app will run on:
👉 http://127.0.0.1:5000

📜 License

This project is for internal use and demos.
You may customize and extend it as needed.






