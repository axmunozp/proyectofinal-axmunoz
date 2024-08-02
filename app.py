from flask import Flask, request, render_template, redirect, url_for, jsonify
from dotenv import load_dotenv
from flask_restful import Api
from db import db
import os
from models.user import Users
from flask_login import LoginManager, login_user
from resources.producto_resource import ProductosResource
from resources.ventas_resource import VentaResource
from resources.ingrediente_resource import IngredientesResource, AbastecerIngredienteResource, RenovarInventarioIngredienteResource


load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_database = os.getenv('DB_DATABASE')
secret_key = os.urandom(24)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}"
app.config["SECRET_KEY"] = secret_key
db.init_app(app)
api = Api(app)

login_manager = LoginManager()
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    user = Users.query.get(id)
    if user:
        return user
    return None

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)  
            return redirect(url_for('resultado', exito=True))
        else:
            return redirect(url_for('resultado', exito=False))
    return render_template("login.html")

@app.route('/resultado')
def resultado():
    exito_param = request.args.get('exito', 'false').lower()
    exito = exito_param == 'true'
    return render_template('resultado.html', exito=exito)

@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html'), 403


# Añadir recursos a la API
api.add_resource(ProductosResource, '/productos','/productos/<int:id>')
api.add_resource(VentaResource, '/vender/<int:id>') 
api.add_resource(IngredientesResource, '/ingredientes', '/ingredientes/<int:id>')
api.add_resource(AbastecerIngredienteResource, '/ingredientes/<int:id>/abastecer')
api.add_resource(RenovarInventarioIngredienteResource, '/ingredientes/<int:id>/renovar')

if __name__ == "__main__":
    app.run(debug=True)


