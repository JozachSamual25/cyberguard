from flask import Flask, render_template, request, redirect, session, jsonify, send_file
import sqlite3
import csv
from detector import detect_attack, reset_attempts

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- LOG FUNCTION ----------------
def log_event(username, action, severity="INFO"):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (username, action, severity) VALUES (?, ?, ?)",
        (username, action, severity)
    )
    conn.commit()
    conn.close()

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    u = request.form['username']
    p = request.form['password']

    # Check correct login FIRST
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    user = cur.fetchone()
    conn.close()

    if user:
        reset_attempts(u)  # reset brute force counter
        session['user'] = u
        log_event(u, "Login Success", "INFO")
        return redirect('/dashboard')

    # Then detect attack
    attack, severity = detect_attack(u, p)

    if attack:
        log_event(u, attack, severity)
        return "🚨 Attack Detected"

    log_event(u, "Login Failed", "WARNING")
    return "Invalid Login"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/api/logs')
def logs():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT username, action, severity, timestamp FROM logs ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/export')
def export():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs")
    rows = cur.fetchall()
    conn.close()

    with open("logs.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "User", "Action", "Severity", "Time"])
        writer.writerows(rows)

    return send_file("logs.csv", as_attachment=True)

@app.route('/attacker')
def attacker():
    return render_template('attacker.html')

if __name__ == '__main__':
    app.run(debug=True)