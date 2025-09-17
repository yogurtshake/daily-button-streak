document.addEventListener('DOMContentLoaded', function() {
    function showMain(username) {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('main-content').style.display = 'block';
        document.getElementById('username-display').textContent = username;

        fetch(`/streak?username=${encodeURIComponent(username)}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('streak-count').textContent = data.streak;
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
            });
        };
    }

    let username = localStorage.getItem('username');
    if (username) {
        showMain(username);
    } else {
        document.getElementById('login-btn').onclick = function() {
            const input = document.getElementById('username-input').value.trim();
            if (input) {
                username = input;
                localStorage.setItem('username', username);
                showMain(username);
            }
        };
        document.getElementById('username-input').addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('login-real-form').submit();
            }
        });
    }
});