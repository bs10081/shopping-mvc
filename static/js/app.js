
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
});

function fetchProducts() {
    fetch('/products')
        .then(response => response.json())
        .then(products => displayProducts(products))
        .catch(error => console.error('Error fetching products:', error));
}

function displayProducts(products) {
    const productListElement = document.getElementById('product-list');
    productListElement.innerHTML = products.map(product => `
        <div class="product-item">
            <img src="${product.image}" alt="${product.name}" class="product-image" />
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p>價格: ${product.price}</p>
            <p>庫存: ${product.stock}</p>
            <p>分類: ${product.category.join(', ')}</p>
            <button onclick="addToCart('${product.id}')">加入購物車</button>
        </div>
    `).join('');
}

function addToCart(productId) {
    // 假設購物車是一個簡單的陣列
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push(productId);
    localStorage.setItem('cart', JSON.stringify(cart));

    updateCartView();
}

function updateCartView() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartElement = document.getElementById('cart');
    cartElement.innerHTML = `購物車: ${cart.length} 項商品`;
}

// 您可能還需要其他功能，例如顯示購物車詳細內容、從購物車中刪除商品等。
