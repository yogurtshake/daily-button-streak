const BASE_PATH = window.location.pathname.split('/')[1] === 'daily-button-streak' ? '/daily-button-streak' : '';
let username = localStorage.getItem('username');

document.addEventListener('DOMContentLoaded', function() {
    function showMain() {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('main-content').style.display = 'block';
        document.getElementById('rankings-section').style.display = 'none';
        document.getElementById('username-display').textContent = username;
        document.getElementById('main-username-input').value = username;

        fetch(`${BASE_PATH}/streak?username=${encodeURIComponent(username)}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('streak-count').textContent = data.streak;
                if (data.clicked_today) {
                    document.getElementById('button-message').textContent = "Well done. Come back tomorrow.";
                    document.getElementById('button-message').style.color = "#ff9800";
                } else {
                    document.getElementById('button-message').textContent = "You have not clicked today. Please click.";
                    document.getElementById('button-message').style.color = "#ff0000";
                }
            });

        document.getElementById('streak-btn').onclick = function() {
            fetch(`${BASE_PATH}/click`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('streak-count').textContent = data.streak;
                document.getElementById('button-message').textContent = "Well done. Come back tomorrow.";
                document.getElementById('button-message').style.color = "#ff9800";
            });
        };

        document.getElementById('change-username-form').onsubmit = function(e) {
            e.preventDefault();
            const newUsername = document.getElementById('main-username-input').value.trim();
            if (newUsername && newUsername !== username) {
                localStorage.setItem('username', newUsername);
                username = newUsername;
                document.getElementById('username-display').textContent = username;
                fetch(`${BASE_PATH}/streak?username=${encodeURIComponent(username)}`)
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('streak-count').textContent = data.streak;
                        if (data.clicked_today) {
                            document.getElementById('button-message').textContent = "Well done. Come back tomorrow.";
                            document.getElementById('button-message').style.color = "#ff9800";
                        } else {
                            document.getElementById('button-message').textContent = "You have not clicked today. Please click.";
                            document.getElementById('button-message').style.color = "#ff0000";
                        }
                    });
            }
        };
    }

    function showRankings() {
        document.getElementById('main-content').style.display = 'none';
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('rankings-section').style.display = 'block';

        fetch(`${BASE_PATH}/rankings-data`)
            .then(res => res.json())
            .then(data => {
                const table = document.querySelector('.rankings-table');
                table.querySelectorAll('tr:not(:first-child)').forEach(tr => tr.remove());

                data.rankings.forEach((row, idx) => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${idx+1}</td><td>${row[0]}</td><td>${row[1].streak}</td>`;
                    table.appendChild(tr);
                });
            });
    }

    document.getElementById('nav-main').onclick = function(e) {
        e.preventDefault();
        showMain();
        document.getElementById('nav-main').classList.add('hidden');
        document.getElementById('nav-rankings').classList.remove('hidden');
    };
    document.getElementById('nav-rankings').onclick = function(e) {
        e.preventDefault();
        showRankings();
        document.getElementById('nav-main').classList.remove('hidden');
        document.getElementById('nav-rankings').classList.add('hidden');
    };

    if (username) {
        showMain();
        document.getElementById('nav-rankings').classList.remove('hidden');
    } else {
        document.getElementById('login-real-form').onsubmit = function(e) {
            e.preventDefault();
            const input = document.getElementById('username-input').value.trim();
            if (input) {
                username = input;
                localStorage.setItem('username', username);
                showMain();
            }

            document.getElementById('nav-rankings').classList.remove('hidden');
        };
    }

    document.getElementById('info-btn').onclick = function() {
        document.getElementById('info-popup').style.display = 'flex';
    };
    document.getElementById('close-info-popup').onclick = function() {
        document.getElementById('info-popup').style.display = 'none';
    };
    document.getElementById('info-popup').onclick = function(e) {
        if (e.target === this) this.style.display = 'none';
    };
});

function updateTimer() {
    const now = new Date();
    const options = { timeZone: "America/New_York", hour12: false };
    const parts = new Intl.DateTimeFormat('en-US', {
        ...options,
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    }).formatToParts(now);

    const getPart = (type) => parts.find(p => p.type === type).value;
    const year = getPart('year');
    const month = getPart('month');
    const day = getPart('day');
    const hour = getPart('hour');
    const minute = getPart('minute');
    const second = getPart('second');

    const estNow = new Date(`${year}-${month}-${day}T${hour}:${minute}:${second}-05:00`);

    const estMidnight = new Date(estNow);
    estMidnight.setHours(24, 0, 0, 0);

    const diff = estMidnight - estNow;

    if (diff > 0) {
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);
        document.getElementById('timer').textContent =
            `${hours.toString().padStart(2, '0')}:` +
            `${minutes.toString().padStart(2, '0')}:` +
            `${seconds.toString().padStart(2, '0')}`;
    } else {
        document.getElementById('timer').textContent = "00:00:00";
    }
}

setInterval(updateTimer, 1000);
updateTimer();