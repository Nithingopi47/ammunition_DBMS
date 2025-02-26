from flask import Flask, request, jsonify
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
#test query
def execute_query(query, params=None):
    cursor = db.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        db.commit()
        return cursor
    finally:
        cursor.close()

# CRUD Operations

# Create
@app.route('/localhost:3306/api/ammunition', methods=['POST'])
def add_ammunition_type():
    data = request.get_json()
    query = "INSERT INTO AmmunitionTypes (Name, Caliber, Manufacturer) VALUES (%s, %s, %s)"
    params = (data['Name'], data['Caliber'], data['Manufacturer'])
    execute_query(query, params)
    return jsonify({'message': 'Ammunition type added successfully'})

# Read
@app.route('/localhost:3306/api/ammunition', methods=['GET'])
def get_ammunition_types():
    query = "SELECT * FROM AmmunitionTypes"
    result = execute_query(query)
    ammunition_types = [{'AmmunitionID': row[0], 'Name': row[1], 'Caliber': row[2], 'Manufacturer': row[3]} for row in result]
    return jsonify(ammunition_types)

# Update
@app.route('/localhost:3306/api/ammunition/<int:ammunition_id>', methods=['PUT'])
def update_ammunition_type(ammunition_id):
    data = request.get_json()
    query = "UPDATE AmmunitionTypes SET Name=%s, Caliber=%s, Manufacturer=%s WHERE AmmunitionID=%s"
    params = (data['Name'], data['Caliber'], data['Manufacturer'], ammunition_id)
    execute_query(query, params)
    return jsonify({'message': 'Ammunition type updated successfully'})

# Delete
@app.route('/localhost:3306/api/ammunition/<int:ammunition_id>', methods=['DELETE'])
def delete_ammunition_type(ammunition_id):
    query = "DELETE FROM AmmunitionTypes WHERE AmmunitionID=%s"
    params = (ammunition_id,)
    execute_query(query, params)
    return jsonify({'message': 'Ammunition type deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)