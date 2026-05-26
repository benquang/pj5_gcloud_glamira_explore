## GCS Setup

A. Create a VM instance

+ Region:`southeast1 (singapore)` 
+ Machine type: e2-highmem-2
+ Edit disk size to 100GB, copy scripts in equivalent code to edit and create

B. Install MongoDB on VM

```bash
sudo apt update
sudo apt install -y gnupg curl

# Import MongoDB 8.0 GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
	sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor

# Add MongoDB 8.0 repository (Ubuntu 22.04 Jammy)
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | \
	sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start and enable service
sudo systemctl start mongod
sudo systemctl enable mongod

# Check version
mongod --version

# Test connection
mongosh
```

