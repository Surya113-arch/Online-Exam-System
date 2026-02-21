import webbrowser
webbrowser.open("http://127.0.0.1:5000")
from flask import session 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)

# Student table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

@app.route('/')
def home():
    return render_template('login.html')

# Question table
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))
    answer = db.Column(db.String(100))

# Add Questions
@app.route('/add_question', methods=['POST'])
def add_question():

    question = request.form['question']
    a = request.form['a']
    b = request.form['b']
    c = request.form['c']
    d = request.form['d']
    correct = request.form['correct']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO questions(question,a,b,c,d,correct) VALUES(?,?,?,?,?,?)",
                (question,a,b,c,d,correct))

    conn.commit()
    conn.close()

    return "Question Added Successfully!"

# Exam Page
@app.route('/exam', methods=['GET','POST'])
def exam():
    if 'user' not in session:
        return redirect(url_for('home'))

    questions = Question.query.all()

    if request.method == 'POST':
        score = 0
        total = len(questions)

        for q in questions:
            selected = request.form.get(str(q.id))
            if selected == q.answer:
                score += 1

        session['score'] = score
        session['total'] = total

        return redirect(url_for('result'))

    return render_template('exam.html', questions=questions)

# Result Page
@app.route('/result')
def result():
    if 'score' in session:
        score = session['score']
        total = session['total']
        return render_template('result.html', score=score, total=total)
    else:
        return redirect(url_for('dashboard'))

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('register.html')

# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid username or password"

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    else:
        return redirect(url_for('home'))

#start exam
@app.route('/start_exam')
def start_exam():
    return render_template('exam.html')
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    conn.close()

    return render_template('exam.html', questions=questions)

#submit exam
@app.route('/submit_exam', methods=['POST'])
def submit_exam():

    score = 0

    if request.form.get('q1') == 'a':
        score += 1

    if request.form.get('q2') == 'b':
        score += 1

    return "Your Score is: " + str(score) + "/2"

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

#admin
@app.route('/admin')
def admin():
    if request.method == 'POST':
        q = request.form['question']
        op1 = request.form['op1']
        op2 = request.form['op2']
        op3 = request.form['op3']
        ans = request.form['answer']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO questions(question,option1,option2,option3,answer) VALUES(?,?,?,?,?)",
                    (q,op1,op2,op3,ans))

        conn.commit()
        conn.close()

        return "Question Added Successfully!"

    return render_template('admin.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)