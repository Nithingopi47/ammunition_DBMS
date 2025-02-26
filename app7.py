from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Connection Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password",
    database="database_name"
)
    
# Function to execute SQL queries
def execute_query(query, params=None):
    cursor = db.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    # Consume results
    results = cursor.fetchall()

    
    # Close cursor
    cursor.close()
    
    db.commit()
    return results

# Insert into tables
def insert_into_tables(AmmunitionID, Name, Caliber, Manufacturer, Quantity, ExpirationDate, StorageLocation):
    try:
        # Insert data into ammunition_type table
        query1 = "INSERT INTO ammunition_type (AmmunitionID, Name, Caliber, Manufacturer) VALUES (%s, %s, %s, %s)"
        values1 = (AmmunitionID, Name, Caliber, Manufacturer)
        execute_query(query1, values1)

        # Insert data into inventory table
        query2 = "INSERT INTO inventory (AmmunitionID, Quantity, ExpirationDate, StorageLocation) VALUES (%s, %s, %s, %s)"
        values2 = (AmmunitionID, Quantity, ExpirationDate, StorageLocation)
        execute_query(query2, values2)

        return "Ammunition inserted successfully!"
    except Exception as e:
        return f"Error inserting ammunition: {str(e)}"

# Update tables
def update_ammunition(AmmunitionID, attribute, new_value):
    try:
        # Mapping attribute to column names
        ammunition_column_mapping = {
            'Name': 'Name',
            'Caliber': 'Caliber',
            'Manufacturer': 'Manufacturer'
        }
        
        inventory_column_mapping = {
            'Quantity': 'Quantity',
            'ExpirationDate': 'ExpirationDate',
            'StorageLocation': 'StorageLocation'
        }
        
        if attribute in ammunition_column_mapping:
            # Construct the UPDATE query for ammunition_type table
            ammunition_query = f"UPDATE ammunition_type SET {ammunition_column_mapping[attribute]} = %s WHERE AmmunitionID = %s"
            ammunition_values = (new_value, AmmunitionID)
            execute_query(ammunition_query, ammunition_values)
        
        if attribute in inventory_column_mapping:
            # Construct the UPDATE query for inventory table
            inventory_query = f"UPDATE inventory SET {inventory_column_mapping[attribute]} = %s WHERE AmmunitionID = %s"
            inventory_values = (new_value, AmmunitionID)
            execute_query(inventory_query, inventory_values)
        
        return f"Ammunition {attribute} updated successfully!"
    except Exception as e:
        return f"Error updating ammunition: {str(e)}"


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete_form.html')
    elif request.method == 'POST':
        AmmunitionID = request.form['AmmunitionID']
        
        # Delete data from tables
        try:
            # Delete data from inventory table
            query1 = "DELETE FROM inventory WHERE AmmunitionID = %s"
            execute_query(query1, (AmmunitionID,))
            
            # Delete data from ammunition_type table
            query2 = "DELETE FROM ammunition_type WHERE AmmunitionID = %s"
            execute_query(query2, (AmmunitionID,))
            
            
            
            return "Ammunition deleted successfully!"
        except Exception as e:
            return f"Error deleting ammunition: {str(e)}"


# Route to display form to select columns
@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        return render_template('read_form.html')
    elif request.method == 'POST':
        # Get selected columns
        columns = request.form.getlist('columns')
        
        # Construct the SELECT query dynamically
        selected_columns = ', '.join(columns)
        query = f"SELECT {selected_columns} FROM ammunition_type INNER JOIN inventory ON ammunition_type.AmmunitionID = inventory.AmmunitionID"

        # Execute the query
        result = execute_query(query)

        return render_template('result.html', result=result, columns=columns)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert_form.html')
    elif request.method == 'POST':
        AmmunitionID = request.form['AmmunitionID']
        Name = request.form['Name']
        Caliber = request.form['Caliber']
        Manufacturer = request.form['Manufacturer']
        Quantity = request.form['Quantity']
        ExpirationDate = request.form['ExpirationDate']
        StorageLocation = request.form['StorageLocation']
        
        return insert_into_tables(AmmunitionID, Name, Caliber, Manufacturer, Quantity, ExpirationDate, StorageLocation)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update_form.html')
    elif request.method == 'POST':
        AmmunitionID = request.form['AmmunitionID']
        attribute = request.form['attribute']
        new_value = request.form['new_value']
        
        return update_ammunition(AmmunitionID, attribute, new_value)
    

if __name__ == '__main__':
    app.run(debug=True)