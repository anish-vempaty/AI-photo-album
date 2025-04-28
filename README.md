# 📸 AI Photo Album

This project implements an AI-powered photo album web application, allowing users to upload, index, and search photos using natural language queries.  
It is built using **AWS S3**, **Lambda**, **Lex**, **Rekognition**, **OpenSearch**, and **API Gateway**.

---

## 📂 Project Structure

```
AI-photo-album/
├── Lambda_Functions/
│   ├── index-photos.py   # Indexes uploaded photos to OpenSearch
│   └── Search-Photos.py  # Handles search queries
├── Frontend/
│   └── index.html        # Simple web app for uploading and searching photos
└── README.md             # Project documentation
```

---

## ⚙️ Features

- Upload photos to AWS S3 with optional **custom labels**.
- **Auto-label** photos using AWS Rekognition.
- **Index** photo metadata into AWS OpenSearch.
- **Natural Language Search** using AWS Lex and OpenSearch.
- Fully functional **frontend** hosted on S3 as a static website.

---

## 🚀 How it Works

1. **Upload**:  
   Users upload photos using the web frontend.  
   The photo is stored in an S3 bucket with optional `x-amz-meta-customlabels`.

2. **Indexing**:  
   A Lambda function (`index-photos`) is triggered on S3 upload.
   - Detects labels using Rekognition.
   - Combines them with custom labels.
   - Indexes the metadata into OpenSearch.

3. **Search**:  
   Users enter a search query.
   - AWS Lex processes the text to extract keywords.
   - Lambda (`search-photos`) searches OpenSearch for matching photos.
   - Matching photos are displayed to the user.

---

## 🛠️ Technologies Used

- **AWS S3** (photo storage)
- **AWS Lambda** (backend logic)
- **AWS Rekognition** (automatic label detection)
- **AWS OpenSearch** (search engine)
- **AWS API Gateway** (API layer)
- **AWS Lex** (natural language understanding)
- **AWS CloudFormation** (optional infra deployment)
- **AWS CodePipeline** (optional continuous deployment)
- **HTML/CSS/JS** (frontend)

---

## 📋 Setup Overview

- Create an S3 bucket for storing photos.
- Deploy Lambda functions and connect triggers.
- Create an OpenSearch domain and an API Gateway.
- Configure a Lex bot for natural language understanding.
- Host the frontend on an S3 bucket with static hosting enabled.

---

## 📸 Example Usage

> **Upload page**  
> Upload a photo and optionally enter custom labels like "beach, sunset".

> **Search page**  
> Type queries like:
> - "show me beach photos"
> - "find dogs"
> - "show pictures of sunsets"

---

## 📚 References

- [AWS Rekognition Documentation](https://aws.amazon.com/rekognition/)
- [AWS OpenSearch Documentation](https://docs.aws.amazon.com/opensearch-service/)
- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [AWS Lex Documentation](https://aws.amazon.com/lex/)

---

# ✅ Project Status

- ✅ Upload and Indexing: Working
- ✅ Searching with Natural Language: Working
- ✅ Frontend Hosting: Working

---
