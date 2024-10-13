curl -F "file=@data/hired_employees.csv" -F "table_name=employees" http://127.0.0.1:5000/api/upload_csv
curl -F "file=@data/jobs.csv" -F "table_name=jobs" http://127.0.0.1:5000/api/upload_csv
curl -F "file=@data/departments.csv" -F "table_name=departments" http://127.0.0.1:5000/api/upload_csv
