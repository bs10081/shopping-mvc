<?php
require('dbconfig.php');

function showProductList() { // 顧客查看商品列表
	global $db;
	$sql = "select pID, name, price, stock from product;";
	$stmt = mysqli_prepare($db,$sql);
	mysqli_stmt_execute($stmt);
	$result = mysqli_stmt_get_result($stmt);
	$rows = array();
	while($r = mysqli_fetch_assoc($result)) {
		$rows[]=$r;
	}
	return $rows;
}
function addCart($pID) {
    global $db;

    // 獲取商品庫存數量
    $sqlStock = "select stock from product where pID=?";
    $stmtStock = mysqli_prepare($db, $sqlStock);
    mysqli_stmt_bind_param($stmtStock, "i", $pID);
    mysqli_stmt_execute($stmtStock);
    mysqli_stmt_bind_result($stmtStock, $stock);
    mysqli_stmt_fetch($stmtStock);
    mysqli_stmt_close($stmtStock);

    if ($stock > 0) {
        // 檢查購物車是否已包含此商品
        $sql1 = "select count(*) from cart where pID=?";
        $stmt1 = mysqli_prepare($db, $sql1);
        mysqli_stmt_bind_param($stmt1, "i", $pID);
        mysqli_stmt_execute($stmt1);
        mysqli_stmt_bind_result($stmt1, $count);
        mysqli_stmt_fetch($stmt1);
        mysqli_stmt_close($stmt1);

        if ($count > 0) {
            // 購物車裡已經有此商品，檢查總數是否小於庫存數量
            $sqlCart = "select amount from cart where pID=?";
            $stmtCart = mysqli_prepare($db, $sqlCart);
            mysqli_stmt_bind_param($stmtCart, "i", $pID);
            mysqli_stmt_execute($stmtCart);
            mysqli_stmt_bind_result($stmtCart, $cartAmount);
            mysqli_stmt_fetch($stmtCart);
            mysqli_stmt_close($stmtCart);

            if ($cartAmount < $stock) {
                // 購物車中商品總數小於庫存數量，數量+1
                $sql2 = "update cart set amount = amount + 1 where pID=?";
                $stmt2 = mysqli_prepare($db, $sql2);
                mysqli_stmt_bind_param($stmt2, "i", $pID);
                mysqli_stmt_execute($stmt2);
                mysqli_stmt_close($stmt2);
            } else {
                // 購物車中商品總數已達到庫存數量，不執行任何操作
            }
        } else {
            // 購物車裡沒有此商品，新增一筆資料
            $sql3 = "insert into cart (pID, amount) values (?, 1)";
            $stmt3 = mysqli_prepare($db, $sql3);
            mysqli_stmt_bind_param($stmt3, "i", $pID);
            mysqli_stmt_execute($stmt3);
            mysqli_stmt_close($stmt3);
        }

        // 結帳後庫存-1
        $sql4 = "update product set stock = stock - 1 where pID=?";
        $stmt4 = mysqli_prepare($db, $sql4);
        mysqli_stmt_bind_param($stmt4, "i", $pID);
        mysqli_stmt_execute($stmt4);
        mysqli_stmt_close($stmt4);

        return true; // 表示成功加入購物車
    } else {
        echo "Out of stock!";
        return false; // 表示庫存不足，無法加入購物車
    }
}


function getDetail($pID) { // 顧客查看商品資訊
	global $db;
	$sql = "select name, price, stock, content from product where pID=?";
	$stmt = mysqli_prepare($db,$sql);
	mysqli_stmt_bind_param($stmt,"i",$pID);
	mysqli_stmt_execute($stmt);
	$result = mysqli_stmt_get_result($stmt);
	$rows = array();
	while($r = mysqli_fetch_assoc($result)) {
		$rows[] = $r;
	}
	return $rows;
}

function showCartList() { // 顧客查看購物車
	global $db;
	$sql = "select product.pID, product.name, product.price, cart.amount, cart.total from product inner join cart on product.pID = cart.pID";
	$stmt = mysqli_prepare($db,$sql);
	mysqli_stmt_execute($stmt);
	$result = mysqli_stmt_get_result($stmt);
	$rows = array();
	while($r = mysqli_fetch_assoc($result)) {
		$rows[] = $r;
	}
	return $rows;
}

function delCart($pID) { // 顧客刪除購物車內容
	global $db;
	$sql = "delete from cart where pID=?;";
	$stmt = mysqli_prepare($db,$sql);
	mysqli_stmt_bind_param($stmt,"i",$pID);
	mysqli_stmt_execute($stmt);
	return True;
}
?>