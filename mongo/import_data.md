## MongoDB data import

A. Import raw data into MongoDB

### Step 1: Copy raw data from GCS to your VM
```bash
gsutil cp gs://pj5-glamira-bucket-qt/summary.bson . 
```

### Step 2: Use mongorestore
```bash
mongorestore --db glamira --collection summary --drop summary.bson
```

**Result:**
```
41432473 document(s) restored successfully. 0 document(s) failed to restore.
```

B. Alternative: Use `pymongo`







