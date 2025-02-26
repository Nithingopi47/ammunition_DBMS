from flask import Flask, request, render_template
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
    db.commit()
    return cursor

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
    return render_template('update_form.html')

@app.route('/update', methods=['POST'])
def update():
    AmmunitionID = request.form['AmmunitionID']
    attribute = request.form['attribute']
    new_value = request.form['new_value']
    
    return update_ammunition(AmmunitionID, attribute, new_value)

if __name__ == '__main__':
    app.run(debug=True)