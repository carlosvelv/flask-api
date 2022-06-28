#Importando librerias necesarias
import os
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#Creamos app
app = Flask(__name__)
api = Api(app) #Hacemos el wrap de nuestra app en una api

basedir = os.path.abspath(os.path.dirname(__file__))
### Base de datos ###
# Construimos el URL de la BDD de sqlite para SqlAlchemy 
sqlite_url = "sqlite:///" + os.path.join(basedir, "libros.db")
# Agregamos el URI de la bdd como parte de la aplicacion
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#A continuación creamos el modelo de la base de datos
class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    ventas = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Libro(Nombre={nombre}, autor={autor}, ventas={ventas}"

#Creamos la base de datos
db.create_all()


#Esto va a ayudar a validar lo que se pasa en el request.form, osea lo que nos envía  en los argumentos
book_args = reqparse.RequestParser()
#Definimos los argumentos que aceptaremos en el form, nombre tipo y ayuda por si no lo pone bien el usuario
book_args.add_argument("nombre", type=str, help='String que contiene el nombre del libro')
book_args.add_argument("autor", type=str,help='String que contiene el nombre del libro')
book_args.add_argument("ventas", type=int, help='int que contiene las ventas del libro')


# Esto ayudará a la hora de serializar la respuesta de la API
resource_fields = {
    'id' : fields.Integer,
    'nombre' : fields.String,
    'autor': fields.String,
    'ventas': fields.Integer
}


#Creando el recurso
class Libro(Resource):

    #Para el GET request de ese recurso
    @marshal_with(resource_fields) #Decorador para Serializar el resultado
    def get(self, book_id): #El id va a venir del get request
        #Realizamos el query a la BDD
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message='No existe libro con ese ID')
        return result

    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if result:
            abort(409, message='video id taken')
        libro = BookModel(id=book_id, nombre=args['nombre'], autor=args['autor'],
                          ventas=args['ventas'])
        db.session.add(libro)
        db.session.commit()
        return libro, 201

    def delete(self, book_id):

        #Confirmamos que exista el libro
        result = BookModel.query.filter_by(id=book_id)
        if not result:
            abort(404, message='No existe libro con ese ID')
        result.delete()
        db.session.commit()
        return '', 204

#Agregamos el recurso
api.add_resource(Libro,  '/libro/<int:book_id>')

if __name__ ==  '__main__':
    app.run(port=5001,debug=True)#Production debug False