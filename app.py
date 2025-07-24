from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os  # ✅ Added to read PORT from environment (Render requirement)

app = Flask(__name__)

# ✅ Changed secret key for production (you can set it as env variable on Render)
app.secret_key = os.environ.get('SECRET_KEY', 'my_secret_key')

# ✅ In-memory "database" — note: this data resets when the app restarts
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/welcome')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if username in users:
            return "User already exists!"
        users[username] = password
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect('/welcome')
        return "Invalid credentials!"
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect('/login')

@app.route('/logout')
def logout():
    username = session.get('username', 'Guest')
    session.clear()
    return render_template('logout.html', username=username)

# ✅ This is required by Render to work — uses environment PORT
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render uses dynamic port
    app.run(host='0.0.0.0', port=port)        # Listen on all IPs
