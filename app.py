from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import os
import time
import threading
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

app = Flask(
    __name__,
    static_url_path='/daily-button-streak/static',
    static_folder='static'
)

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
    clicked_today = False
    if user:
        last_date = user['last_date']
        today = datetime.now().date().strftime('%Y-%m-%d')
        clicked_today = (last_date == today)
    return jsonify({'streak': streak, 'clicked_today': clicked_today})

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

def daily_streak_reset():
    while True:
        now = datetime.now(ZoneInfo("America/New_York"))
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = (next_midnight - now).total_seconds()
        
        time.sleep(seconds_until_midnight)
        
        users = read_users()
        today = datetime.now(ZoneInfo("America/New_York")).date()
        yesterday = today - timedelta(days=1)
        
        for username, data in users.items():
            last_date = datetime.strptime(data['last_date'], '%Y-%m-%d').date()
            if last_date != yesterday and last_date != today:
                users[username]['streak'] = 0
                
        write_users(users)

if __name__ == '__main__':
    threading.Thread(target=daily_streak_reset, daemon=True).start()
    app.run(debug=True, port=5002)