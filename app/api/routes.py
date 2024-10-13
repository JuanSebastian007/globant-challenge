from flask import jsonify, request, Response
from app.api import api_bp
from app.db.models import Employee, Department, Job
from app.db.database import db
import pandas as pd
from sqlalchemy import text
import csv, io


@api_bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    """
    Endpoint to upload and process a CSV file for different tables.
    This function handles the upload of a CSV file and processes its content to insert data into the specified table.
    The table is determined by the 'table_name' parameter provided in the form data.
    The function supports three tables:
    - 'employees': The CSV file must contain 5 columns.
    - 'jobs': The CSV file must contain 2 columns.
    - 'departments': The CSV file must contain 2 columns.
    The function performs the following steps:
    1. Validates the presence and format of the uploaded file.
    2. Reads the CSV file into a pandas DataFrame.
    3. Validates the number of columns based on the specified table.
    4. Processes each row of the DataFrame and adds the corresponding records to the database.
    5. Commits the transaction if all operations are successful.
    6. Rolls back the transaction and returns an error message if any exception occurs.
    Returns:
        Response: A JSON response indicating the status of the operation.
        - 200: If the data is successfully loaded into the specified table.
        - 400: If there is a validation error with the file or table name.
        - 500: If an internal server error occurs during processing.
    """

    file = request.files.get("file")
    table_name = request.form.get("table_name")

    if not file or not file.filename.endswith(".csv"):
        return (
            jsonify({"status": "error", "message": "Por favor sube un archivo CSV"}),
            400,
        )

    try:
        df = pd.read_csv(file)
        if table_name == "employees":
            if df.shape[1] != 5:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "El archivo CSV para employees debe contener 5 columnas",
                        }
                    ),
                    400,
                )
            df = df.dropna()  # Eliminar filas con NaN en cualquier columna

            for _, row in df.iterrows():
                employee = Employee(
                    id=row[0],
                    name=row[1],
                    datetime=row[2],
                    department_id=row[3],
                    job_id=row[4],
                )
                db.session.add(employee)
        elif table_name == "jobs":
            if df.shape[1] != 2:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "El archivo CSV para jobs debe contener 2 columnas",
                        }
                    ),
                    400,
                )

            for _, row in df.iterrows():
                job = Job(id=row[0], job=row[1])
                db.session.add(job)

        elif table_name == "departments":
            if df.shape[1] != 2:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "El archivo CSV para departments debe contener 2 columnas",
                        }
                    ),
                    400,
                )

            for _, row in df.iterrows():
                department = Department(id=row[0], department=row[1])
                db.session.add(department)
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Valor de table_name no válido. Debe ser 'employees', 'departments' o 'jobs'.",
                    }
                ),
                400,
            )
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Datos cargados exitosamente en la tabla {table_name}",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route("/employees_by_quarter", methods=["GET"])
def employees_by_quarter():
    """
    Generates a CSV report of the number of employees per department and job for each quarter of the year 2021.

    This function executes a SQL query to retrieve the count of employees grouped by department and job for each quarter
    of the year 2021. The results are then written to a CSV file and returned as a downloadable response.

    Returns:
        Response: A Flask Response object containing the CSV data with the following columns:
            - department: The name of the department.
            - job: The job title.
            - q1: The number of employees in the first quarter.
            - q2: The number of employees in the second quarter.
            - q3: The number of employees in the third quarter.
            - q4: The number of employees in the fourth quarter.
    """

    query = text(
        """
    SELECT d.department, j.job,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    JOIN jobs j ON e.job_id = j.id
    WHERE EXTRACT(YEAR FROM e.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job;
    """
    )

    result = db.session.execute(query)
    employees_by_quarter = [dict(row) for row in result.mappings()]

    output = io.StringIO()
    writer = csv.DictWriter(
        output, fieldnames=["department", "job", "q1", "q2", "q3", "q4"]
    )
    writer.writeheader()
    writer.writerows(employees_by_quarter)

    csv_content = output.getvalue()
    output.close()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=employees_by_quarter.csv"},
    )


@api_bp.route("/departments_above_avg", methods=["GET"])
def departments_above_avg():
    """
    Endpoint to retrieve departments with above-average hires in 2021.

    This function executes a SQL query to calculate the average number of hires per department
    for the year 2021 and then selects departments that have a number of hires greater than this average.
    The results are returned as a CSV file.

    Returns:
        Response: A Flask Response object containing the CSV data with the following columns:
            - id: The department ID.
            - department: The name of the department.
            - hires: The number of hires in the department.
    """

    query_avg = text(
        """
    WITH department_hires AS (
        SELECT d.id, d.department, COUNT(e.id) AS hires
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE EXTRACT(YEAR FROM e.datetime) = 2021
        GROUP BY d.id, d.department
    ),
    avg_hires AS (
        SELECT AVG(hires) AS avg_hires FROM department_hires
    )
    SELECT dh.id, dh.department, dh.hires
    FROM department_hires dh, avg_hires
    WHERE dh.hires > avg_hires.avg_hires
    """
    )

    result = db.session.execute(query_avg)
    departments = [dict(row) for row in result.mappings()]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "department", "hires"])
    writer.writeheader()
    writer.writerows(departments)

    csv_content = output.getvalue()
    output.close()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=departments_above_avg.csv"
        },
    )
