from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("F:\\flask test brrr\\security\\Your_Firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'Your_database_URL'
})

# Function to insert data into Firebase Realtime Database
def insert_into_firebase(AmmunitionID, Name, Caliber, Manufacturer, Quantity, ExpirationDate, StorageLocation):
    try:
        ref = db.reference('ammunition_management')
        ammunition_data = {
            'AmmunitionID': AmmunitionID,
            'Name': Name,
            'Caliber': Caliber,
            'Manufacturer': Manufacturer,
            'Quantity': Quantity,
            'ExpirationDate': ExpirationDate,
            'StorageLocation': StorageLocation
        }
        ref.child(AmmunitionID).set(ammunition_data)
        return "Ammunition inserted successfully!"
    except Exception as e:
        return f"Error inserting ammunition: {str(e)}"

# Function to update data in Firebase Realtime Database
def update_ammunition_firebase(AmmunitionID, attribute, new_value):
    try:
        ref = db.reference(f'ammunition_management/{AmmunitionID}')
        ref.update({attribute: new_value})
        return f"Ammunition {attribute} updated successfully!"
    except Exception as e:
        return f"Error updating ammunition: {str(e)}"

# Function to delete data from Firebase Realtime Database
def delete_ammunition_firebase(AmmunitionID):
    try:
        ref = db.reference(f'ammunition_management/{AmmunitionID}')
        ref.delete()
        return "Ammunition deleted successfully!"
    except Exception as e:
        return f"Error deleting ammunition: {str(e)}"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

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
        return insert_into_firebase(AmmunitionID, Name, Caliber, Manufacturer, Quantity, ExpirationDate, StorageLocation)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update_form.html')
    elif request.method == 'POST':
        AmmunitionID = request.form['AmmunitionID']
        attribute = request.form['attribute']
        new_value = request.form['new_value']
        return update_ammunition_firebase(AmmunitionID, attribute, new_value)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete_form.html')
    elif request.method == 'POST':
        AmmunitionID = request.form['AmmunitionID']
        return delete_ammunition_firebase(AmmunitionID)



if __name__ == '__main__':
    app.run(debug=True)
