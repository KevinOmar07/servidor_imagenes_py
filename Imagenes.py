import platform, asyncio, pymysql, os, cloudinary
from os import remove
import cloudinary.uploader
import cloudinary.api
from fileinput import filename
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./images"


host = "bxwuncwod1yxvwwned5s-mysql.services.clever-cloud.com"
DB = "bxwuncwod1yxvwwned5s"
userDB = "ujo5pftfpvqiwoqw"
passDB = "OTNfrdZFDJEVuHqeGajm"


async def add_img_bd(files, idUser):
    conexion = pymysql.connect(host=host, user=userDB, passwd=passDB, db=DB)
    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO imagenes(nombreImage, ruta, idUser) VALUES (%s, %s, %s);"
            for file in files:
                filename = str(datetime.today().strftime('%Y %H_%M_%S_')) + secure_filename(
                    file.filename)  # filename guarda el nombre de la imagen
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                res = cloudinary.uploader.upload("./images/" + filename)
                cursor.execute(consulta, (filename, res['url'], idUser))
                remove("./images/" + filename)
            conexion.commit()
    finally:
        print("Proceso terminado")
        conexion.close()
    return "guardado"


async def add_img_recibe(files, idU):
    print("Inicia el await")
    await add_img_bd(files, idU)
    print("Entra a await")
    return "ok img complet"


def setImagenes(files, idU):
    print("Entra en asyncio, run")
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(add_img_recibe(files, idU))
    return "ok aync complet"


def obtenerURL(id):
    imagenes = []
    conexion = pymysql.connect(host=host, user=userDB, passwd=passDB, db=DB)
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