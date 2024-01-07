document.addEventListener('DOMContentLoaded', fetchProducts);

let shoppingCart = [];

function fetchProducts() {
    fetch('/products')
        .then(response => response.json())
        .then(products => {
            productsList = products;
            displayProducts(products);
        })
        .catch(error => console.error('Error fetching products:', error));
}

function displayProducts(products) {
    const productListElement = document.getElementById('product-list');
    productListElement.innerHTML = products.map(product => `
        <div class="product-item">
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p>價格: ${product.price}</p>
            <p>庫存: ${product.stock}</p>
            <p>分類: ${product.category.join(', ')}</p>
            <button onclick="addToCart('${product.id}')">加入購物車</button>
            </div>`).join('');
}


// app.js - addToCart function updated
let productsList = [];  // This will hold the fetched products list

// This function fetches the list of products from the server
function fetchProductsList() {
    fetch('/products')
        .then(response => response.json())
        .then(products => {
            productsList = products;
            displayProducts(products);  // This is a hypothetical function to display products on the page
        })
        .catch(error => console.error('Error fetching products list:', error));
}


function addToCart(productId) {
    const existingItem = shoppingCart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        const product = productsList.find(p => p.id === productId);
        if (product) {
            shoppingCart.push({ ...product, quantity: 1 });
        } else {
            console.error('Product not found');
            return;
        }
    }
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartItemsElement = document.getElementById('cart-items');
    let totalPrice = 0;
    cartItemsElement.innerHTML = shoppingCart.map(item => {
        const itemTotalPrice = item.price * (item.quantity || 1);
        totalPrice += itemTotalPrice;
        return `
            <div class="cart-item">
                <span>${item.name}</span>
                <span>單價: ${item.price}</span>
                <span>數量: ${item.quantity || 1}</span>
                <span>小計: ${itemTotalPrice}</span>
                <button onclick="removeFromCart('${item.id}')">移除</button>
            </div>
        `;
    }).join('');
    // 更新總價
    const totalPriceElement = document.getElementById('total-price');
    totalPriceElement.textContent = `總價: ${totalPrice}`;
}

function removeFromCart(productId) {
    shoppingCart = shoppingCart.filter(item => item.id !== productId);
    updateCartDisplay();
}

// CSS function
window.addEventListener('scroll', function () {
    var shoppingCart = document.getElementById('shopping-cart');
    if (window.pageYOffset > shoppingCart.offsetTop) {
        shoppingCart.classList.add('sticky');
    } else {
        shoppingCart.classList.remove('sticky');
    }
});