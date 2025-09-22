from datetime import datetime, timedelta
import os
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'database.txt')

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

def reset_streaks():
    users = read_users()
    today = datetime.now(ZoneInfo("America/New_York")).date()
    yesterday = today - timedelta(days=1)
    
    for username, data in users.items():
        last_date = datetime.strptime(data['last_date'], '%Y-%m-%d').date()
        if last_date != yesterday and last_date != today:
            users[username]['streak'] = 0
            
    write_users(users)

if __name__ == '__main__':
    reset_streaks()