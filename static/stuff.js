let username = localStorage.getItem('username');

document.addEventListener('DOMContentLoaded', function() {
    function showMain() {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('main-content').style.display = 'block';
        document.getElementById('username-display').textContent = username;
        document.getElementById('main-username-input').value = username;

        fetch(`/streak?username=${encodeURIComponent(username)}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('streak-count').textContent = data.streak;
                if (data.clicked_today) {
                    document.getElementById('button-message').textContent = "Well done. Come back tomorrow.";
                } else {
                    document.getElementById('button-message').textContent = "You have not clicked today. Please click.";
                }
            });

        document.getElementById('streak-btn').onclick = function() {
            fetch('/click', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('streak-count').textContent = data.streak;
                document.getElementById('button-message').textContent = "Well done. Come back tomorrow.";
            });
        };

        document.getElementById('change-username-form').onsubmit = function(e) {
            e.preventDefault();
            const newUsername = document.getElementById('main-username-input').value.trim();
            if (newUsername && newUsername !== username) {
                localStorage.setItem('username', newUsername);
                username = newUsername;
                document.getElementById('username-display').textContent = username;
                fetch(`/streak?username=${encodeURIComponent(username)}`)
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('streak-count').textContent = data.streak;
                        if (data.clicked_today) {
                            document.getElementById('button-message').textContent = "Well done. Come back tomorrow.";
                        } else {
                            document.getElementById('button-message').textContent = "You have not clicked today. Please click.";
                        }
                    });
            }
        };
    }

    if (username) {
        showMain();
    } else {
        document.getElementById('login-real-form').onsubmit = function(e) {
            e.preventDefault();
            const input = document.getElementById('username-input').value.trim();
            if (input) {
                username = input;
                localStorage.setItem('username', username);
                showMain();
            }
        };
    }
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