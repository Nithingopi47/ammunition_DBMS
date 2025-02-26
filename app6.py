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

# Display table
def display_table(table_name):
    query = f"SELECT * FROM {table_name}"
    result = execute_query(query)
    headers = [desc[0] for desc in result.description]
    rows = [dict(zip(headers, row)) for row in result.fetchall()]
    return headers, rows

# Insert into table
def insert_into_table(table_name, values):
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    execute_query(query, values)

# Update table
def update_table(table_name, set_values, condition):
    set_clause = ', '.join([f"{key}=%s" for key in set_values.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition[0]}=%s"
    values = list(set_values.values())
    values.append(condition[1])
    execute_query(query, values)

# Delete from table
def delete_from_table(table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition[0]}=%s"
    execute_query(query, (condition[1],))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        table_name = request.form['table_name']
        headers, rows = display_table(table_name)
        return render_template('table.html', table_name=table_name, headers=headers, rows=rows)
    else:
        return render_template('table.html')

@app.route('/insert', methods=['POST'])
def insert():
    table_name = request.form['table_name']
    values = [request.form[key] for key in request.form if key != 'table_name']
    insert_into_table(table_name, values)
    return table()

@app.route('/update', methods=['POST'])
def update():
    table_name = request.form['table_name']
    set_values = {key: request.form[key] for key in request.form if key != 'table_name' and key != 'condition_column' and key != 'condition_value'}
    condition = (request.form['condition_column'], request.form['condition_value'])
    update_table(table_name, set_values, condition)
    return table()

@app.route('/delete', methods=['POST'])
def delete():
    table_name = request.form['table_name']
    condition = (request.form['condition_column'], request.form['condition_value'])
    delete_from_table(table_name, condition)
    return table()

if __name__ == '__main__':
    app.run(debug=True)