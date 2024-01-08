function updateOrderStatus(orderId, newStatus) {
    fetch(`/update_order_status/${orderId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Order status updated');
                loadOrders();
            }
        })
        .catch(error => console.error('Error:', error));
}

// 獲取訂單列表並添加到頁面
function loadOrders() {
    // 假設有一個從伺服器獲取訂單的 endpoint '/get_orders'
    fetch('/orders')
        .then(response => response.json())
        .then(orders => {
            const orderListDiv = document.getElementById('order-list');
            // 清空現有列表
            orderListDiv.innerHTML = '';
            // 填入訂單資訊和操作按鈕
            orders.forEach(order => {
                const orderDiv = document.createElement('div');
                orderDiv.innerHTML = `
                    <div>Order ID: ${order.id}</div>
                    <div>Order Status: ${order.status}</div>
                    <div>Order Rating: ${order.rating}</div>
                    <button onclick="updateOrderStatus(${order.id}, 'shipped')">Mark as shipped</button>
                    
                    <button onclick="updateOrderStatus(${order.id}, 'cancelled')">Cancel order</button>
                `;
                // <button onclick="updateOrderStatus(${order.id}, 'delivered')">Mark as delivered</button>
                orderListDiv.appendChild(orderDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', loadOrders);
