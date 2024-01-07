import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        cart_item = Cart.query.filter_by(product_id=product.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            new_cart_item = Cart(product_id=product.id)
            db.session.add(new_cart_item)
        db.session.commit()
    return redirect(url_for('home'))
# Route to edit the quantity of a product in the cart


@app.route('/update_cart_item/<int:item_id>', methods=['POST'])
def update_cart_item(item_id):
    cart_item = Cart.query.get_or_404(item_id)
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
    return redirect(url_for('home'))


# Route to remove a product from the cart


@app.route('/remove_cart_item/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart_item = Cart.query.get_or_404(item_id)
    # 完全刪除商品項目
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('home'))

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


# Route to create the database (for first-time setup)


@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Database created!'


if __name__ == '__main__':
    app.run(debug=True)
