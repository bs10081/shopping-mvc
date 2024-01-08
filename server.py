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
    return redirect(url_for('shop'))  # 改為跳轉到 shop.html
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
    return redirect(url_for('shop'))


# Route to remove a product from the cart


@app.route('/remove_cart_item/<int:item_id>', methods=['POST'])
@login_required
def remove_cart_item(item_id):
    cart_item = Cart.query.filter_by(
        id=item_id, user_id=current_user.id).first_or_404()
    # 完全刪除商品項目
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('shop'))

# Route to view the cart


@app.route('/cart')
def view_cart():
    cart_items = Cart.query.all()
    total_price = sum(
        [item.product.price * item.quantity for item in cart_items])
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


# Route to view the admin page

@app.route('/admin', methods=['GET', 'POST'])
def admin():
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


@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Database created!'


if __name__ == '__main__':
    app.run(debug=True)
