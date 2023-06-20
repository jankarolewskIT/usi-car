import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM cars"
    cur.execute(s)
    list_cars = cur.fetchall()
    return render_template('index.html', list_cars = list_cars)

@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        registration_number = request.form['registration_number']
        time_arrive = request.form['time_arrive']
        cur.execute("INSERT INTO cars (make, model, registration_number, time_arrive) VALUES (%s,%s,%s, %s)", (make, model, registration_number, time_arrive))
        conn.commit()
        flash('Dodano wpis')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM cars WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', car = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        registration_number = request.form['registration_number']
        time_arrive = request.form['time_arrive']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE cars
            SET make = %s,
                model = %s,
                registration_number = %s,
                time_arrive = %s
            WHERE id = %s
        """, (make, model, registration_number, time_arrive, id))
        flash('Zaktualizowano wpis')
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM cars WHERE id = {0}'.format(id))
    conn.commit()
    flash('Usunięto wpis')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
