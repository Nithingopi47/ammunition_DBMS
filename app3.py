import mysql.connector

def display_table(table_name):
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password",
        database="database_name"
    )

    # Create a cursor
    mycursor = mydb.cursor()

    # Execute a query to fetch data from the table
    mycursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows
    rows = mycursor.fetchall()

    # Display the table
    if not rows:
        print("Table is empty")
    else:
        # Print table headers
        headers = [desc[0] for desc in mycursor.description]
        print(" | ".join(headers))

        # Print rows
        for row in rows:
            print(" | ".join(str(cell) for cell in row))

    # Close cursor and connection
    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    table_name = input("Enter the name of the table: ")
    display_table(table_name)