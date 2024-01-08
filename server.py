# .env
import os
from dotenv import load_dotenv
# flask
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# sqlite
from flask_sqlalchemy import SQLAlchemy
# login
from flask import flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
# hash password
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Define the User model


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), default='customer')  # 預設為 'customer'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        # 假設所有用戶都是活躍的
        return True

    @property
    def is_authenticated(self):
        # 假設用戶一旦建立就已經通過身份驗證
        return True

    @property
    def is_anonymous(self):
        # 默認情況下，普通用戶不應該是匿名的
        return False

    def get_id(self):
        # 返回用戶 ID，用於加載用戶實體
        return str(self.id)

# Define the Product model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Define the Cart model


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    product = db.relationship('Product', backref=db.backref('cart', lazy=True))

    def __repr__(self):
        return f'<Cart {self.product_id}x{self.quantity}>'

# Define the Order model


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.now())
    # 可以是 pending, confirmed, shipped, delivered
    status = db.Column(db.String(50), nullable=False, default='pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)
    rating = db.Column(db.Integer, default=0)

# Define the OrderItem model


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# Route for the home page


@app.route('/')
def home():
    products = Product.query.all()
    cart_items = Cart.query.all()  # 從購物車表中讀取所有項目
    total_price = sum(
        [item.quantity * item.product.price for item in cart_items])
    return render_template('index.html', products=products, cart_items=cart_items, total_price=total_price)


# Route to add a product to the cart


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        # 檢查購物車中是否已有該商品
        cart_item = Cart.query.filter_by(
            product_id=product.id, user_id=current_user.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            # 創建新的購物車項目
            new_cart_item = Cart(product_id=product.id,
                                 user_id=current_user.id)
            db.session.add(new_cart_item)
        db.session.commit()
    return jsonify({'success': True})

# Route to edit the quantity of a product in the cart


@app.route('/update_cart_item/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    # 從表單中獲取用戶輸入的數量
    cart_item = Cart.query.filter_by(
        id=item_id, user_id=current_user.id).first_or_404()
    if 'update' in request.form:
        cart_item.quantity = request.form.get('quantity', type=int)
        db.session.commit()
    elif 'add_one' in request.form:
        cart_item.quantity += 1
        db.session.commit()
    elif 'remove_one' in request.form:
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            db.session.delete(cart_item)
        db.session.commit()
    else:
        cart_item.quantity = 0
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('shop'))


# Route to remove a product from the cart


@app.route('/remove_cart_item/<int:item_id>', methods=['POST'])
@login_required
def remove_cart_item(item_id):
    cart_item = Cart.query.filter_by(
        id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('shop'))

# Route to view the cart


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    cart_data = [{
        'id': item.id,
        'name': item.product.name,
        'quantity': item.quantity,
        'price': str(item.product.price),
    } for item in cart_items]
    return jsonify(cart_items=cart_data, total_price=total_price)


# Route to view the admin page

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # 檢查用戶是否有權限訪問管理員頁面
    if current_user.role != 'admin':
        return redirect(url_for('dashboard')), 401
    if request.method == 'POST':
        if "add" in request.form:
            # 從表單中獲取新產品資料並添加到數據庫
            new_product = Product(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price']
            )
            db.session.add(new_product)
            db.session.commit()
        elif "edit" in request.form:
            # 從表單中獲取編輯的產品資料並更新
            product_id = request.form['edit']
            product = Product.query.get(product_id)
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = request.form['price']
            db.session.commit()
        elif "delete" in request.form:
            # 刪除指定的產品
            product_id = request.form['delete']
            product = Product.query.get(product_id)
            db.session.delete(product)
            db.session.commit()

    products = Product.query.all()
    return render_template('admin.html', products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 註冊邏輯
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 檢查用戶名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            # 創建新用戶對象
            new_user = User(username=username)
            new_user.set_password(password)  # 設置密碼
            db.session.add(new_user)
            db.session.commit()
            # 這裡可以重定向到登入頁面，或直接登入用戶
            return redirect(url_for('login'))
        else:
            error_message = 'Username already taken. Please choose a different username.'
            return render_template('register.html', error_message=error_message)

    return render_template('register.html')


# Route to view the login page

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # 使用 get_json() 替代 form
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True}), 200  # 返回 JSON 響應
        else:
            return jsonify({'success': False, 'error_message': 'Invalid username or password.'}), 401

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route to create the database (for first-time setup)


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin.html')
    elif current_user.role == 'customer':
        # 假設 Cart 是一個模型，存儲著用戶購物車內容
        user_cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        return render_template('user.html', cart_items=user_cart_items)
    else:
        return redirect(url_for('home'))


@app.route('/shop')
@login_required
def shop():
    products = Product.query.all()
    # 假設 Cart 是一個模型，存儲著用戶購物車內容
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('shop.html', products=products, cart_items=cart_items)


# Route to checkout


@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'error': 'Your cart is empty'}), 400

    # 創建訂單
    order = Order(customer_id=current_user.id)
    db.session.add(order)
    db.session.flush()  # 獲取訂單的 ID

    # 創建訂單項目
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id, product_id=item.product_id, quantity=item.quantity)
        db.session.add(order_item)
        db.session.delete(item)  # 清空購物車

    db.session.commit()

    return jsonify({'success': 'Your order has been placed', 'order_id': order.id})

# 客戶查看訂單狀態的路由


@app.route('/order_status', methods=['GET'])
@login_required
def order_status():
    orders = Order.query.filter_by(customer_id=current_user.id).all()
    order_list = [{'id': order.id, 'status': order.status,
                   'rating': order.rating} for order in orders]
    return jsonify(order_list)

# 客戶對訂單評價的路由


@app.route('/rating', methods=['GET'])
@login_required
def rating():
    return render_template('rating.html')

#


@app.route('/user_orders')
@login_required
def user_orders():
    # Replace 'Order' with your actual Order model and 'customer_id' with the actual foreign key to the User model.
    orders_query = Order.query.filter_by(customer_id=current_user.id).all()
    orders = [{'id': order.id, 'status': order.status,
               'rating': order.rating} for order in orders_query]
    return jsonify(orders)


@app.route('/rate_order/<int:order_id>', methods=['POST'])
@login_required
def rate_order(order_id):
    data = request.get_json()
    rating = data['rating']
    order = Order.query.get(order_id)
    if order and order.customer_id == current_user.id:
        order.rating = rating
        db.session.commit()
        return jsonify({'success': 'Rating submitted'}), 200
    else:
        return jsonify({'error': 'Order not found'}), 404


# 商家查看所有訂單的路由

@app.route('/orders', methods=['GET'])
@login_required
def orders():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    orders = Order.query.all()
    order_list = [{'id': order.id, 'status': order.status,
                   'rating': order.rating} for order in orders]
    return jsonify(order_list)


# 商家更新訂單狀態的路由


@app.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    new_status = data['status']
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
        return jsonify({'success': 'Order status updated'}), 200
    else:
        return jsonify({'error': 'Order not found'}), 404


# driver 的路由

@app.route('/driver')
def driver_page():
    # 返回 driver.html 的內容
    return render_template('driver.html')


@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Database created!'


if __name__ == '__main__':
    app.run(debug=True)
