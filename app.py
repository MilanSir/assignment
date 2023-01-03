import mysql.connector
from flask import Flask, request, redirect, url_for, render_template

import os
os.environ['FLASK_DEBUG'] = '1'


app = Flask(__name__)

# Connect to the database
conn = mysql.connector.connect(
    host='localhost', database='task', user='root', password='', port='3306')

# Create the "tasks" table if it doesn't exist
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTO_INCREMENT, description TEXT, status TEXT,last_date date)''')

# Close the connection to the database
cursor.close()
conn.close()

# Home page


@app.route('/')
def index():
    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Retrieve all tasks from the database
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return render_template('index.html', tasks=tasks)

# Add a new task


@app.route('/add', methods=['POST'])
def add():
    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Insert the new task into the database
    cursor.execute('INSERT INTO tasks (description, status, last_date) VALUES (%s, %s, %s)',
                   (request.form['description'], 'Not Started', request.form['last_date']))

    conn.commit()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

# Mark a task as complete


@app.route('/updateall/<id>', methods=['POST'])
def updateall(id):
    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()
    data = request.form

    # Insert the new task into the database
    cursor.execute(
        f"UPDATE tasks SET description = '{data['description']}', last_date = '{data['last_date']}' , status ='{data['status']}' WHERE id ={id} ")

    conn.commit()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/addtask')
def addtask():
    return render_template('add.html')


@app.route('/notcompleted')
def notcompleted():

    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Retrieve all tasks from the database
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Close the connection to the database
    cursor.close()
    conn.close()
    return render_template('notcompleted.html', tasks=tasks)


@app.route('/overdue')
def overdue():
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Retrieve all tasks from the database

    cursor.execute('SELECT * FROM tasks WHERE last_date < CURDATE()')
    tasks = cursor.fetchall()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return render_template('overdue.html', tasks=tasks)


@app.route('/completed')
def completed():
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Retrieve all tasks from the database
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return render_template('completed.html', tasks=tasks)


@app.route('/delete/<id>')
def delete(id):
    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Update the task status in the database
    cursor.execute(f"DELETE FROM tasks WHERE id={id}")

    conn.commit()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/update/<id>')
def update(id):
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Retrieve all tasks from the database
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return render_template('update.html', tasks=tasks, id=int(id))


@app.route('/complete/<id>',)
def complete(id):
    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost', database='task', user='root', password='', port='3306')
    cursor = conn.cursor()

    # Update the task status in the database
    cursor.execute('UPDATE tasks  WHERE id=%s', ('complete', id))
    conn.commit()

    # Close the connection to the database
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
