from flask import Flask, render_template, request, redirect, url_for, session 
from database import User, Product
from os import environ


app = Flask(__name__)

app.secret_key = environ.get("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            user = User.create_user(username, password)
            session["user_id"] = user.id

            return redirect(url_for("products"))
    return render_template("register.html")

@app.route("/products")
def products():
    user =  User.get(session["user_id"])

    _products = user.products

    return render_template("products/index.html", products=_products)

@app.route("/products/create", methods=["GET","POST"])
def product_create():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")

        if name and price:
            user = User.get(session["user_id"])

            Product.create(name=name, price=price, user=user)
            return redirect(url_for("products"))
    return render_template("products/create.html")

@app.route("/products/update/<int:product_id>", methods=["GET","POST"])
def product_update(product_id: int):
    _product = Product.select().where(Product.id == product_id).first()

    if request.method == "POST":
        _product.name = request.form.get("name")
        _product.price = request.form.get("price")
        _product.save()
        return redirect(url_for("products"))

    return render_template("products/update.html", product=_product)

