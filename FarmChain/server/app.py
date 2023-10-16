from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmchain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Enable CORS for the entire app
CORS(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    farmer = db.Column(db.String(255), nullable=False)

# Product schema for serialization/deserialization
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# User model (assuming you have a User model with fields like 'username' and 'password')
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# User schema for serialization/deserialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Create the database tables
db.create_all()

# User registration endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message='Username already exists'), 400
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Create a new user
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message='User registered successfully'), 201

# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify(message='Invalid credentials'), 401

# Get all products endpoint
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products)), 200

# Create a new product endpoint (requires authentication)
@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    farmer = data.get('farmer')
    
    new_product = Product(name=name, price=price, farmer=farmer)
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify(message='Product created successfully'), 201

# Custom error handling for 404 (Not Found) and 500 (Internal Server Error)
@app.errorhandler(404)
def not_found(error):
    return jsonify(message='Not Found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(message='Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
