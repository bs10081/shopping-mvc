<?php
// 假設這是你的商家資料庫連線
$servername = "your_servername";
$username = "your_username";
$password = "your_password";
$dbname = "your_dbname";

// 創建連線
$conn = new mysqli($servername, $username, $password, $dbname);

// 檢查連線
if ($conn->connect_error) {
    die("連線失敗: " . $conn->connect_error);
}

// 新增商家
if (isset($_POST['add'])) {
    $name = $_POST['name'];
    $address = $_POST['address'];

    $sql = "INSERT INTO businesses (name, address) VALUES ('$name', '$address')";

    if ($conn->query($sql) === TRUE) {
        echo "新增成功";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

// 刪除商家
if (isset($_POST['delete'])) {
    $business_id = $_POST['business_id'];

    $sql = "DELETE FROM businesses WHERE id = $business_id";

    if ($conn->query($sql) === TRUE) {
        echo "刪除成功";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

// 修改商家
if (isset($_POST['update'])) {
    $business_id = $_POST['business_id'];
    $new_name = $_POST['new_name'];
    $new_address = $_POST['new_address'];

    $sql = "UPDATE businesses SET name='$new_name', address='$new_address' WHERE id = $business_id";

    if ($conn->query($sql) === TRUE) {
        echo "修改成功";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

// 關閉連線
$conn->close();
?>

