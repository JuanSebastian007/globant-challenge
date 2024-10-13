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