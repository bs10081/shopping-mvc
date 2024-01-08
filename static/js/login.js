document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('login-form').addEventListener('submit', login);
});

function login(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    var data = {
        'username': username,
        'password': password
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/dashboard'; // 登入成功，跳轉到 dashboard
            } else {
                alert('Login failed: ' + data.message); // 登入失敗，顯示錯誤訊息
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
