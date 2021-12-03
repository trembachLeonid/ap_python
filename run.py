from flask import Flask, Response
from waitress import serve
from user import user
from family import family
from login import login
from history import history
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/family_budget_db'
app.config['JWT_SECRET_KEY'] = 'love'
jwt = JWTManager(app)
app.register_blueprint(user)
app.register_blueprint(family)
app.register_blueprint(login)
app.register_blueprint(history)

serve(app, host='0.0.0.0', port=5000)