import psycopg2
import subprocess

# Database connection parameters
db_params = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}

def delete_entries_and_vacuum():
    try:
        # Establish database connection
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Delete entries
        delete_query = "DELETE FROM your_table WHERE condition;"
        cursor.execute(delete_query)
        conn.commit()
        print(f"{cursor.rowcount} entries deleted.")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Run VACUUM FULL using subprocess
        vacuum_command = f"psql -d {db_params['dbname']} -U {db_params['user']} -h {db_params['host']} -c 'VACUUM FULL;'"
        subprocess.run(vacuum_command, shell=True, check=True)
        print("VACUUM FULL executed successfully.")
        
    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    delete_entries_and_vacuum()
