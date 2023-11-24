<?php
session_start();
require_once('db_connection.php'); // 資料庫連線

// 處理 AJAX 請求
if (isset($_GET['action'])) {
    $action = $_GET['action'];

    switch ($action) {
        case 'get_products':
            echo json_encode(getProductList());
            break;
        case 'get_cart':
            echo json_encode(getCartContent());
            break;
    }
}

if (isset($_POST['action'])) {
    $action = $_POST['action'];

    switch ($action) {
        case 'add_to_cart':
            if (isset($_POST['product_id'])) {
                addToCart($_POST['product_id']);
            }
            break;
        case 'update_cart':
            if (isset($_POST['product_id']) && isset($_POST['quantity'])) {
                updateCart($_POST['product_id'], $_POST['quantity']);
            }
            break;
        case 'remove_from_cart':
            if (isset($_POST['product_id'])) {
                removeFromCart($_POST['product_id']);
            }
            break;
    }
}

// 取得商品列表
function getProductList() {
    // 從資料庫取得商品列表並回傳 JSON 格式
    // 範例：[{ "id": 1, "name": "商品1", "price": 10 }, { "id": 2, "name": "商品2", "price": 15 }]
    // 注意：實際應用中需從資料庫中讀取商品資訊
    return $products;
}

// 取得購物車內容
function getCartContent() {
    // 從 session 取得購物車內容並回傳 JSON 格式
    // 範例：[{ "product_id": 1, "name": "商品1", "quantity": 2 }, { "product_id": 2, "name": "商品2", "quantity": 1 }]
    // 注意：實際應用中需從資料庫中讀取商品資訊
    return $cart;
}

// 新增商品到購物車
function addToCart($product_id) {
    // 處理將商品新增到購物車的邏輯
    // 更新 session 中的購物車內容
}

// 修改購物車中的商品數量
function updateCart($product_id, $quantity) {
    // 處理更新購物車中商品數量的邏輯
    // 更新 session 中的購物車內容
}

// 從購物車刪除商品
function removeFromCart($product_id) {
    // 處理將商品從購物車中移除的邏輯