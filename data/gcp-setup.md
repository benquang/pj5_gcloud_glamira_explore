## GCP Setup

A. Create a bucket in Google Cloud Storage

+ Location: `asia-southeast1 (singapore)`, type `region`
+ Default storage class:   `Standard`
+ Hierarchical namespace: Enable
+ Rapid Cache: Disabled
+ How to control access
  - Prevent public access: Enforced public access prevention on this bucket
  - Access control: Uniform
+ How to protect data object
  - Data protection: soft delete policy (for data recovery) - use default retention duration
  - Data encryption: google-managed encryption key


B. Create a VM instance

+ Region:`southeast1 (singapore)` 
+ Machine type: e2-highmem-2
+ Edit disk size to 100GB, copy scripts in equivalent code to edit and create

C. MongoDB install

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

  