from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="webapp"
)

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE UserName=%s AND Password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return redirect(url_for('student_list'))
        else:
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
    return render_template('login.html')

# Student list page route
@app.route('/student_list')
def student_list():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM studentlist")
    students = cursor.fetchall()
    cursor.close()
    return render_template('student_list.html', students=students)
# Route to add a new student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['class']
        division = request.form['division']
        guardian = request.form['guardian']
        mobile_no = request.form['mobile_no']
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO studentlist (Name, Class, Division, Guardian, MobileNo) VALUES (%s, %s, %s, %s, %s)",
            (name, student_class, division, guardian, mobile_no)
        )
        db.commit()
        cursor.close()
        
        flash('New student added successfully!')
        return redirect(url_for('student_list'))
    
    return render_template('add_student.html')

@app.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM studentlist WHERE Id = %s", (id,))
        db.commit()
        cursor.close()
        return {"success": True}, 200
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False}, 500


# Edit student route
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['class']
        division = request.form['division']
        guardian = request.form['guardian']
        mobile_no = request.form['mobile_no']
        cursor.execute(
            "UPDATE studentlist SET Name=%s, Class=%s, Division=%s, Guardian=%s, MobileNo=%s WHERE Id=%s",
            (name, student_class, division, guardian, mobile_no, id)
        )
        db.commit()
        flash('Student updated successfully!')
        return redirect(url_for('student_list'))
    else:
        cursor.execute("SELECT * FROM studentlist WHERE Id=%s", (id,))
        student = cursor.fetchone()
        cursor.close()
        return render_template('edit_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
