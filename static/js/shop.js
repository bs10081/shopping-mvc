function addToCart(productId) {
    fetch('/add_to_cart/' + productId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            location.reload();
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

function loadCart() {
    fetch('/cart')
        .then(response => response.json())
        .then(data => {
            updateCartDisplay(data.cart_items);
            document.getElementById('total-price').textContent = data.total_price.toFixed(2);
        })
        .catch(error => console.error('Error:', error));
}

function updateCartDisplay(cartItems) {
    const cartElement = document.getElementById('cart');
    cartElement.innerHTML = cartItems.map(item => `
        <div class="cart-item">
            <span>${item.name} - Quantity: ${item.quantity}</span>
            <span>Price: ${item.price}</span>
            <button onclick="changeQuantity(${item.id}, ${item.quantity - 1})">-</button>
            <button onclick="changeQuantity(${item.id}, ${item.quantity + 1})">+</button>
            <button onclick="removeCartItem(${item.id})">Delete</button>
        </div>
    `).join('');
}

