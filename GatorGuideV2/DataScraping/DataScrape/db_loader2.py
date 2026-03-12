import os
import csv
import mysql.connector
import sys

# DATABASE CONFIG

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "loader_db"

CSV_FOLDER = "data_output"


# FLATTEN NESTED CSV

def flatten_csv(y, prefix=""):
    out = {}

    for key, value in y.items():
        # Create new key with underscore separator if prefix exists
        new_key = key if prefix == "" else f"{prefix}_{key}"

        if isinstance(value, dict):
            # Recursively flatten nested dictionaries
            out.update(flatten_csv(value, new_key))
        else:
            out[new_key] = value

    return out

# CONNECT TO MYSQL

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    print("Connected to MySQL successfully!")

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    sys.exit(1)

# PROCESS ALL JSON FILES

files_processed = 0
files_skipped = 0

for file in os.listdir(CSV_FOLDER):

    if file.endswith(".csv"):

        filepath = os.path.join(CSV_FOLDER, file)
        table_name = file.replace(".csv", "")

        print(f"\nProcessing {file} → table `{table_name}`")

        try:
            # Read csv file
            with open(filepath, "r", encoding="utf-8") as f:
                data = list(csv.DictReader(f))

            # Validate: must be a list
            if not isinstance(data, list):
                print(f"Skipped: Not a list (got {type(data).__name__})")
                files_skipped += 1
                continue

            # Validate: must not be empty
            if len(data) == 0:
                print(f"Skipped: Empty array")
                files_skipped += 1
                continue

            # Flatten all records
            flat_data = [flatten_csv(row) for row in data]

            # Get all column names from first record
            columns = list(flat_data[0].keys())
            print(f"Found {len(columns)} columns, {len(flat_data)} rows")

            # Create table with all columns
            column_sql = ", ".join([f"`{col}` LONGTEXT" for col in columns])

            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {column_sql}
            )
            """

            cursor.execute(create_table_query)
            print(f"Table created/verified")

            # Prepare insert query
            cols = ", ".join([f"`{c}`" for c in columns])
            placeholders = ", ".join(["%s"] * len(columns))

            insert_query = f"""
            INSERT INTO `{table_name}` ({cols})
            VALUES ({placeholders})
            """

            # Insert all rows
            for idx, row in enumerate(flat_data):
                values = [str(row.get(col, "")) for col in columns]
                cursor.execute(insert_query, values)

            conn.commit()
            print(f"Inserted {len(flat_data)} records")
            files_processed += 1

        except FileNotFoundError as e:
            print(f"File not found: {e}")
            files_skipped += 1
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            files_skipped += 1

print("\n" + "="*50)
print(f"Completed! Processed: {files_processed}, Skipped: {files_skipped}")
print("="*50)

cursor.close()
conn.close()