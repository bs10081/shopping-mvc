from flask import Flask, jsonify, request, send_from_directory, render_template
import os
import requests
import logging
from dotenv import load_dotenv
import requests
load_dotenv()  # 這會自動尋找並加載項目根目錄下的 .env 文件

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # 設置日誌級別為 DEBUG
# Environment variables
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')


# Environment variables for different Notion databases and API keys
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID_PRODUCTS = os.getenv('NOTION_DATABASE_ID_PRODUCTS')
NOTION_DATABASE_ID_CART = os.getenv('NOTION_DATABASE_ID_CART')
# Ensure environment variables are set
if not NOTION_API_KEY or not NOTION_DATABASE_ID_PRODUCTS:
    raise ValueError(
        "Please set the NOTION_API_KEY and NOTION_DATABASE_ID environment variables.")
# Headers for Notion API requests for the cart
HEADERS_CART = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json"
}

# Headers for Notion API
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/products', methods=['get'])
def get_products():
    try:
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID_PRODUCTS}/query"
        # Ensure this is a post request
        # 這很重要，回應要用 post 請求，，媽的，在這裡卡很久，GPT 是垃圾，我手動排錯的，幹
        response = requests.post(url, headers=HEADERS)
        if response.status_code == 200:
            products_data = response.json()
            products = parse_products(products_data)
            print(products)
            return jsonify(products)
        else:
            return jsonify({"error": "Unable to fetch products"}), response.status_code
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        response = jsonify(
            {"error": "Unable to fetch products", "details": str(e)})
        response.status_code = 500
        return response


def parse_products(notion_data):
    products = []
    for item in notion_data.get("results", []):
        try:
            properties = item.get("properties", {})
            product = {
                "id": item.get("id"),
                "name": next((text['plain_text'] for text in properties.get("Name", {}).get("rich_text", [])), ""),
                "description": next((text['plain_text'] for text in properties.get("Description", {}).get("rich_text", [])), ""),
                "category": [category.get("name", "") for category in properties.get("Category", {}).get("multi_select", [])],
                "stock": properties.get("Stock", {}).get("number", 0),
                # "image": next((file.get("name", "") for file in properties.get("Image", {}).get("url", [])), ""),
                "price": properties.get("Price", {}).get("number", 0.0),
                "notion_url": item.get("url", "")
            }
            products.append(product)
        except Exception as e:
            app.logger.error(f"Error parsing product: {str(e)}")
            # 錯誤處理，可以選擇記錄錯誤並繼續，或返回錯誤響應
    return products

# 以下是商家功能


@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.json
        print("Received data:", data)  # Debug: 輸出接收到的數據
        # Construct the request to add the product to the Notion database
        url = f"https://api.notion.com/v1/pages"
        notion_payload = {
            "parent": {"database_id": NOTION_DATABASE_ID_PRODUCTS},
            "properties": {
                "Name": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data["name"]
                            }
                        }
                    ]
                },
                "Description": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data["description"]
                            }
                        }
                    ]
                },
                "Category": {
                    "multi_select": [{"name": category} for category in data.get("category", [])]
                },
                "Stock": {
                    "number": data["stock"]
                },
                "Price": {
                    "number": data["price"]
                }
            }
        }
        print("Payload to Notion:", notion_payload)  # Debug: 輸出構造的 payload
        response = requests.post(url, json=notion_payload, headers=HEADERS)
        print("Notion response status code:",
              response.status_code)  # Debug: 輸出響應狀態碼
        print("Notion response body:", response.text)  # Debug: 輸出響應正文
        response = requests.post(url, json=notion_payload, headers=HEADERS)
        if response.status_code == 200:
            # If the Notion API call was successful
            return jsonify({"message": "Product added successfully"}), 201
        else:
            # If the Notion API call failed
            return jsonify({"error": "Failed to add product", "details": response.text}), 500

    except Exception as e:
        print("Error occurred:", e)  # Debug: 輸出錯誤信息
        return jsonify({"error": "An error occurred while adding the product"}), 500


# main
if __name__ == '__main__':
    app.debug = True
    app.run()

# Please ensure that there is a route handler for '/product/<product_id>' to fetch product details from Notion
