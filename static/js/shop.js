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
            alert('Product added to cart!');
            // 這裡可以添加用於更新購物車顯示的代碼
            loadCart();
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// 加載購物車內容
function loadCart() {
    fetch('/cart')
        .then(response => response.json())
        .then(data => {
            updateCartDisplay(data.cart_items);
            updateTotalPrice(data.total_price);
        })
        .catch(error => console.error('Error:', error));
}

// 更新購物車顯示
function updateCartDisplay(cartItems) {
    const cartElement = document.getElementById('cart');
    cartElement.innerHTML = ''; // 清空當前購物車內容

    cartItems.forEach(item => {
        // 為每個購物車項目創建 DOM 元素
        const itemElement = document.createElement('div');
        itemElement.innerHTML = `
        <span>${item.product.name} - Quantity: ${item.quantity}</span>
        <button onclick="changeQuantity(${item.id}, ${item.quantity - 1})">-</button>
        <button onclick="changeQuantity(${item.id}, ${item.quantity + 1})">+</button>
        <button onclick="removeCartItem(${item.id})">Delete</button>
      `;
        cartElement.appendChild(itemElement);
    });
}
