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

def insert_into_table(table_name, values):
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password@1234567",
        database="ammunition_management"
    )

    # Create a cursor
    mycursor = mydb.cursor()

    # Execute insert query
    query = f"INSERT INTO {table_name} VALUES ({','.join('%s' for _ in range(len(values)))})"
    mycursor.execute(query, values)

    # Commit changes
    mydb.commit()

    # Close cursor and connection
    mycursor.close()
    mydb.close()

def update_table(table_name, set_values, condition):
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password@1234567",
        database="ammunition_management"
    )

    # Create a cursor
    mycursor = mydb.cursor()

    # Execute update query
    query = f"UPDATE {table_name} SET {', '.join(f'{column}=%s' for column in set_values.keys())} WHERE {condition[0]}=%s"
    values = list(set_values.values())
    values.append(condition[1])
    mycursor.execute(query, values)

    # Commit changes
    mydb.commit()

    # Close cursor and connection
    mycursor.close()
    mydb.close()

def delete_from_table(table_name, condition):
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password@1234567",
        database="ammunition_management"
    )

    # Create a cursor
    mycursor = mydb.cursor()

    # Execute delete query
    query = f"DELETE FROM {table_name} WHERE {condition[0]}=%s"
    mycursor.execute(query, (condition[1],))

    # Commit changes
    mydb.commit()

    # Close cursor and connection
    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    table_name = input("Enter the name of the table: ")
    display_table(table_name)

    operation = input("Enter operation (insert/update/delete): ")

    if operation == "insert":
        values = input("Enter values separated by comma: ").split(",")
        insert_into_table(table_name, values)
    elif operation == "update":
        set_values = dict(input("Enter column=value pairs separated by comma: ").split(","))
        condition = input("Enter condition column=value: ").split("=")
        update_table(table_name, set_values, condition)
    elif operation == "delete":
        condition = input("Enter condition column=value: ").split("=")
        delete_from_table(table_name, condition)

    # Display updated table
    display_table(table_name)