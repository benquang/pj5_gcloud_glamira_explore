## GCP Setup

Install mongodb in VM instance

+ gcloud compute ssh pj5-instance-qt
+ Setup: download and add repository 
  - curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
  - echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
  - sudo apt install -y mongodb-org
+ Start and enable service:
  - sudo systemctl start mongod
  - sudo systemctl enable mongod
+ Connection test:
  - mongod --version
  - mongosh