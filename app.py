from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
import mariadb
import sys

app = Flask(__name__)
app.secret_key = 'many random bytes'

# MariaDB Configuration
db_config = {
    'host': 'localhost',
    'user': 'swapnil-intern',
    'password': 'swapnil-intern',
    'database': 'crud'
}

try:
    conn = mariadb.connect(**db_config)
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

@app.route('/')
def Index():
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur.execute("INSERT INTO students (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur.execute("DELETE FROM students WHERE id=?", (id_data,))
    conn.commit()
    return redirect(url_for('Index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur.execute("""
        UPDATE students SET name=?, email=?, phone=?
        WHERE id=?
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
