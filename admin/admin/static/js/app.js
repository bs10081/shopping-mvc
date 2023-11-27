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
            <button onclick="editProduct('${product.id}')">修改</button>
            <button onclick="deleteProduct('${product.id}')">刪除</button>
            </div>`).join('');

    // 添加到商品列表區域
    productList.appendChild(productItem);
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

document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('productForm');

    form.onsubmit = function (event) {
        console.log('Form submission triggered');
        event.preventDefault(); // 阻止表單默認提交行為

        // 獲取表單內的數據
        var name = document.getElementById('name').value;
        var description = document.getElementById('description').value;
        var price = document.getElementById('price').value || 0;
        var stock = document.getElementById('stock').value || 0;
        // 構造要發送的數據
        var data = {
            name: name,
            description: description,
            price: Number(price),
            stock: Number(stock)
        };
        console.log('Sending data:', JSON.stringify(data));

        // 使用 fetch API 發送數據到後端
        fetch('/add_product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(function (response) {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        }).then(function (data) {
            if (data.message) {
                alert('商品添加成功！');
                // 可以在這裡清空表單或進行其他操作
            } else {
                alert('商品添加失敗：' + data.error);
            }
        }).catch(function (error) {
            console.error('There has been a problem with your fetch operation:', error);
            alert('發生錯誤：' + error.message);
        });
    };
});
