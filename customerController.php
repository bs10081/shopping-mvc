<?php
require('customerModel.php');

$act = $_REQUEST['act'];
switch ($act) {
	case "showProductList": // 顯示商品清單
		$products = getProductList();
		if ($products === false) {
            echo "Error fetching product list.";
        } else {
			echo json_encode($products);
		}
		return;

	case "addCart":	// 顧客將商品加入購物車
		$id = (int)$_REQUEST['id']; // 商品編號
		addCart($id);
		return;
	case "getDetail": // 顧客查看商品詳細資訊
		$id = (int)$_REQUEST['id']; // 前端傳來的商品編號
		$product=getDetail($id);
		echo json_encode($product);
		return;
	case "showCartList": // 顧客查看購物車
		$cart = getCartList();
		echo json_encode($cart);
		return;
	case "delCart": // 顧客刪除購物車商品
		$id = (int)$_REQUEST['id'];
		delCart($id);
		return;
	default:  
}
?>