import requests

# Notion API 配置
NOTION_API_KEY = "secret_wrlnTaT6WQZuwhBIbLhPiOnJk79fAW4xD0imkNLP5vi"
NOTION_DATABASE_ID = "c38f74a7308d4ce48ddf43a0141263ba"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

# 新商品的數據
new_product_data = {
    "parent": {"database_id": NOTION_DATABASE_ID},
    "properties": {
        "ID": {
            "title": [
              {
                  "text": {
                      "content": "df5c1175-28c2-4852-97e7-a6927f850d93"
                  }
              }
            ]
        },
        "Name": {
            "rich_text": [
                {
                    "text": {
                        "content": "測試產品"
                    }
                }
            ]
        },
        "Description": {
            "rich_text": [
                {
                    "text": {
                        "content": "這是一個測試商品的描述。"
                    }
                }
            ]
        },
        "Price": {
            "number": 99.99
        },
        "Stock": {
            "number": 100
        },
        "Image": {
            "files": [
                {
                    "type": "external",
                    "name": "image.jpg",
                    "external": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        },
        "Category": {
            "multi_select": [
                {
                    "name": "電子產品"
                }
            ]
        }
    }
}


# 向 Notion API 發送請求來創建新頁面
create_page_url = "https://api.notion.com/v1/pages"
response = requests.post(
    create_page_url, headers=HEADERS, json=new_product_data)

# 檢查響應
if response.status_code == 200:
    print("新商品成功添加到 Notion 數據庫。")
else:
    print("添加商品失敗：", response.text)
