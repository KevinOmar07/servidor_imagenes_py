from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import threading

import Usuarios
import  Imagenes


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return 'Creado'


@app.route('/login', methods=['POST'])
def singin():
    if request.method == 'POST':        
        return Usuarios.signIn(json.loads( request.data ))


@app.route('/singup', methods=['POST'])
def signup():
    if request.method == 'POST':        
        return Usuarios.signUp( json.loads(request.data) )


@app.route('/set_image2',methods=['POST'])
def add_image2():
    if request.method == "POST":        
        hilo = threading.Thread(target=Imagenes.setImagenes, args=( request.files.getlist('files') , request.args.get('id') ,))
        hilo.start()
        hilo.join()
    return "Imagenes Guardadas"   


@app.route('/get_Images', methods=['GET'])
def get_iamge():
        return json.dumps(['imagenes', Imagenes.obtenerURL( request.args.get('id') )
])


if __name__ == '__main__':
    app.run(port = 3001, debug = True)
