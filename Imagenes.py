import platform, asyncio, os
from flask import Flask
from os import remove
from fileinput import filename
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Flask

import conexionBD
import CloudDinary

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "servidor_imagenes_py\images"

cloudinary = CloudDinary.cloudinary

async def add_img_bd(files, idUser):    
    conexion = conexionBD.DBConnection().conexion
    try:        
        with conexion.cursor() as cursor:                        
            consulta = "INSERT INTO imagenes(nombreImage, ruta, idUser) VALUES (%s, %s, %s);"            
            for file in files:  
                filename = str(datetime.today().strftime('%Y %H_%M_%S_')) + secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                res = cloudinary.uploader.upload("servidor_imagenes_py\images/" + filename)
                cursor.execute(consulta, (filename, res['url'], idUser))                
                remove("servidor_imagenes_py\images/" + filename)                                
            conexion.commit()
    finally:        
        conexion.close()
    return "guardado"


async def add_img_recibe(files, idU):    
    await add_img_bd(files, idU)    
    return "ok img complet"


def setImagenes(files, idU):    
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(add_img_recibe(files, idU))
    return "ok aync complet"


def obtenerURL(id):
    imagenes = []    
    conexion = conexionBD.DBConnection().conexion
    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT nombreImage, ruta FROM imagenes where idUser=%s;"
            cursor.execute(consulta, (id))
            datosUser = cursor.fetchall()
            for img in datosUser:
                imagenes.append(img[1])
    finally:
            conexion.close()
    return imagenes
    