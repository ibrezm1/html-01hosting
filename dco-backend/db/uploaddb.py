import os
import psycopg2
from psycopg2 import sql

# Function to run SQL files for PostgreSQL in a specific order
def upload_postgres_db(pg_folder, db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    try:
        # Read filenames into a list and sort alphabetically
        sql_filenames = [f for f in os.listdir(pg_folder) if f.endswith(".sql")]
        sql_filenames.sort()

        for file_name in sql_filenames:
            with open(os.path.join(pg_folder, file_name), "r") as sql_file:
                sql_script = sql_file.read()
                cursor.execute(sql.SQL(sql_script))
                print(f"Executed {file_name} on PostgreSQL")
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    # For PostgreSQL
    pg_folder = "."  # Replace with path to PostgreSQL SQL files folder
    db_params = {
        'dbname': 'your_db_name',
        'user': 'your_db_user',
        'password': 'your_db_password',
        'host': 'localhost',  # or your PostgreSQL server host
        'port': '5432'
    }
    upload_postgres_db(pg_folder, db_params)