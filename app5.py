from flask import Flask, render_template, request, redirect

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
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        db.commit()
        return cursor
    finally:
        cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display_table', methods=['GET', 'POST'])
def display_table():
    if request.method == 'POST':
        table_name = request.form['table_name']
        cursor = execute_query(f"SELECT * FROM {table_name}")
        headers = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return render_template('display_table.html', headers=headers, rows=rows)
    return redirect('/')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        table_name = request.form['table_name']
        values = request.form.getlist('values')
        placeholders = ', '.join(['%s' for _ in range(len(values))])
        execute_query(f"INSERT INTO {table_name} VALUES ({placeholders})", tuple(values))
        return redirect('/')
    return render_template('insert.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        table_name = request.form['table_name']
        set_values = dict(request.form.items())
        del set_values['table_name']
        condition_column = set_values.pop('condition_column')
        condition_value = set_values.pop('condition_value')
        placeholders = ', '.join([f'{key}=%s' for key in set_values.keys()])
        execute_query(f"UPDATE {table_name} SET {placeholders} WHERE {condition_column}=%s",
                      tuple(set_values.values()) + (condition_value,))
        return redirect('/')
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        table_name = request.form['table_name']
        condition_column = request.form['condition_column']
        condition_value = request.form['condition_value']
        execute_query(f"DELETE FROM {table_name} WHERE {condition_column}=%s", (condition_value,))
        return redirect('/')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)