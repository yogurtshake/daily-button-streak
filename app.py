from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import os

app = Flask(__name__)

DB_FILE = 'database.txt'

def read_users():
    users = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    username, streak, last_date = parts
                    users[username] = {'streak': int(streak), 'last_date': last_date}
    return users

def write_users(users):
    with open(DB_FILE, 'w') as f:
        for username, data in users.items():
            f.write(f"{username},{data['streak']},{data['last_date']}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/streak')
def get_streak():
    username = request.args.get('username')
    users = read_users()
    user = users.get(username)
    streak = user['streak'] if user else 0
    return jsonify({'streak': streak})

@app.route('/click', methods=['POST'])
def click():
    data = request.get_json()
    username = data.get('username')
    today = datetime.now().date()
    users = read_users()
    user = users.get(username)

    if user:
        last_date = datetime.strptime(user['last_date'], '%Y-%m-%d').date()
        if last_date == today:
            streak = user['streak']
        elif last_date == today - timedelta(days=1):
            streak = user['streak'] + 1
        else:
            streak = 1
    else:
        streak = 1

    users[username] = {'streak': streak, 'last_date': today.strftime('%Y-%m-%d')}
    write_users(users)
    return jsonify({'streak': streak})

@app.route('/rankings')
def rankings():
    users = read_users()
    sorted_users = sorted(users.items(), key=lambda x: (-x[1]['streak'], x[0]))
    return render_template('rankings.html', rankings=sorted_users)

if __name__ == '__main__':
    app.run(debug=True)