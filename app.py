from flask import Flask, request, jsonify, render_template, Response
from datetime import datetime, timedelta
import os
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

app = Flask(__name__, static_url_path='/daily-button-streak/static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'database.txt')

def read_users():
    users = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    username, streak, last_date, highest_streak = parts
                    users[username] = {
                        'streak': int(streak),
                        'last_date': last_date,
                        'highest_streak': int(highest_streak)
                    }
                elif len(parts) == 3:
                    username, streak, last_date = parts
                    users[username] = {
                        'streak': int(streak),
                        'last_date': last_date,
                        'highest_streak': int(streak)
                    }
    return users

def write_users(users):
    with open(DB_FILE, 'w') as f:
        for username, data in users.items():
            f.write(f"{username},{data['streak']},{data['last_date']},{data['highest_streak']}\n")


@app.route('/daily-button-streak/static/manifest.json')
@app.route('/static/manifest.json')
def manifest():
    manifest_path = os.path.join(BASE_DIR, 'static', 'manifest.json')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest_content = f.read()
    return Response(manifest_content, mimetype='application/json')

@app.route('/')
@app.route('/daily-button-streak')
def index():
    return render_template('index.html')

@app.route('/streak')
@app.route('/daily-button-streak/streak')
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
@app.route('/daily-button-streak/click', methods=['POST'])
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
        highest_streak = max(streak, user.get('highest_streak', streak))
    else:
        streak = 1
        highest_streak = 1

    users[username] = {
        'streak': streak,
        'last_date': today.strftime('%Y-%m-%d'),
        'highest_streak': highest_streak
    }
    write_users(users)
    return jsonify({'streak': streak, 'highest_streak': highest_streak})

@app.route('/rankings-data')
@app.route('/daily-button-streak/rankings-data')
def rankings_data():
    users = read_users()
    filtered_users = {u: d for u, d in users.items() if d['streak'] > 0}
    sorted_users = sorted(filtered_users.items(), key=lambda x: (-x[1]['streak'], x[0]))
    
    today = datetime.now().date().strftime('%Y-%m-%d')
    rankings = []
    for username, data in sorted_users:
        clicked_today = "yes" if data['last_date'] == today else "no"
        rankings.append((username, {
            'streak': data['streak'],
            'clicked_today': clicked_today,
            'highest_streak': data.get('highest_streak', data['streak'])
        }))
        
    return jsonify(rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True, port=5002)