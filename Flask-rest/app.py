from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)
ma = Marshmallow(app)

# product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(50))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "qty")


# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# create product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


# get products
@app.route("/product")
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# get single product
@app.route("/product/<id>")
def get_single_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# update the product
@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    product.name = request.json["name"]
    product.description = request.json["description"]
    product.price = request.json["price"]
    product.qty = request.json["qty"]

    db.session.commit()

    return product_schema.jsonify(product)


# run
if __name__ == "__main__":
    app.run(debug=True)
