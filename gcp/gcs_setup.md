## GCS Setup

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

B. Upload raw data to GCS

```bash
gsutil cp summary.bson gs://pj5-glamira-bucket-qt
```





