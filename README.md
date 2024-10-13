# Globant Challenges

## Introduction
This is a Globant challenge project that involves creating a REST API using Flask. The API loads data into a PostgreSQL database and provides two methods to generate metric information.

## Requirements
- **Operating System**: Linux, macOS, or Windows
- **Docker**: Ensure Docker is installed and running on your system
- **Git**: Version control system

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/globant-challenges.git
cd globant-challenges
```

2. **Build the Docker image**:
```bash
cd docker
docker-compose up --build
```
3. **Load initial data**:
The `upload_data.sh` script contains the requests to load the initial data into the PostgreSQL database. Run the script using:
```bash
./upload_data.sh
 ```

4. **Generate metrics**:
The `get_metric` script contains the requests to generate the metric tables. Run the script using:
```bash
./get_metric
```

## Recommended Architecture
Since the challenge involves data migration to an SQL database, processing CSV files, and creating an API, I recommend the following approach:

### Cloud Infrastructure (AWS or Azure)
#### REST API:
- Use AWS Lambda to create a serverless API, which reduces costs and facilitates scalability.
- To process CSV files, you can use AWS S3 (or Azure Blob Storage) to store the CSVs, and AWS API Gateway to manage the requests.

#### SQL Database:
- Use Amazon RDS (or Azure SQL Database) for a scalable relational database to store the migrated data.

#### Batch Processing:
- AWS Glue (or Azure Data Factory) to transform and load large volumes of data.
- Alternatively, AWS Batch or Fargate to run batch processing if it needs to be done in containers.

#### Containers:
- Use Docker to containerize the API application and simplify deployment, both locally and in the cloud.
- Manage containers with AWS ECS (or Azure Kubernetes Service).

