document.addEventListener('DOMContentLoaded', function () {
    fetch('/order_status')
        .then(response => response.json())
        .then(data => {
            const ordersList = document.getElementById('orders-list');
            ordersList.innerHTML = '';
            data.forEach(order => {
                const li = document.createElement('li');
                li.textContent = `Order ID: ${order.id} - Status: ${order.status} - Rating: ${order.rating}`;
                ordersList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
});

document.addEventListener('DOMContentLoaded', function () {
    fetch('/user_orders') // 這是獲取當前用戶訂單的假設端點
        .then(response => response.json())
        .then(orders => {
            const orderList = document.getElementById('order-list');
            orders.forEach(order => {
                const li = document.createElement('li');
                li.textContent = `Order ID: ${order.id} `;
                const ratingSelect = createRatingSelect(order.id);
                li.appendChild(ratingSelect);
                orderList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
});

function createRatingSelect(orderId) {
    const select = document.createElement('select');
    select.id = `rating-${orderId}`;
    for (let i = 0; i <= 5; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        select.appendChild(option);
    }
    select.addEventListener('change', () => submitRating(orderId, select.value));
    return select;
}

function submitRating(orderId, rating) {
    fetch(`/rate_order/${orderId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rating: rating })
    })
        .then(response => response.json())
        .then(data => {
            alert('Thank you for your rating!');
            this.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
