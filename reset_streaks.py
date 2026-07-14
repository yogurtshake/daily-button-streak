from datetime import datetime, timedelta
import os
import shutil
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'database.txt')
ARCHIVE_DIR = os.path.join(BASE_DIR, 'archived')

def read_users():
    users = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    username, streak, last_date, highest_streak, total_clicks, total_days_clicked = parts
                    users[username] = {
                        'streak': int(streak),
                        'last_date': last_date,
                        'highest_streak': int(highest_streak),
                        'total_clicks': int(total_clicks),
                        'total_days_clicked': int(total_days_clicked)
                    }
    return users

def write_users(users):
    with open(DB_FILE, 'w') as f:
        for username, data in users.items():
            f.write(f"{username},{data['streak']},{data['last_date']},{data['highest_streak']},{data['total_clicks']},{data['total_days_clicked']}\n")

def archive_database(today):
    if not os.path.exists(DB_FILE):
        return
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive_file = os.path.join(ARCHIVE_DIR, f'database-{today}.txt')
    shutil.copy2(DB_FILE, archive_file)

def reset_streaks():
    today = datetime.now(ZoneInfo("America/New_York")).date()
    archive_database(today.strftime('%Y-%m-%d'))
    
    users = read_users()
    yesterday = today - timedelta(days=1)
    
    for username, data in users.items():
        last_date = datetime.strptime(data['last_date'], '%Y-%m-%d').date()
        if last_date != yesterday and last_date != today:
            users[username]['streak'] = 0
            
    write_users(users)

if __name__ == '__main__':
    reset_streaks()