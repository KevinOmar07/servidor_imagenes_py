import re
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

host = "bxwuncwod1yxvwwned5s-mysql.services.clever-cloud.com"
DB = "bxwuncwod1yxvwwned5s"
userDB = "ujo5pftfpvqiwoqw"
passDB = "OTNfrdZFDJEVuHqeGajm"

def signIn(user, password):
    try:
        res = realizarConsulta("SELECT nombre, contrasena, idUser FROM usuarios where nombre=%s;", user)              
        if (len(res[1]) > 0):
            if(check_password_hash( res[1][0][1],password)):
                estado = {"status": 'Inicio correcto', "id": res[1][0][2]}
            else:
                estado = {"status": 'Error de inicio', "id": ""}    
        else :
            estado = {"status": 'Error de inicio', "id": ""}           
    finally:
            res[0].close()             

    return estado

def signUp(user, password):
    print("Sign Up")
    res = realizarConsulta("SELECT nombre FROM usuarios where nombre=%s;", user)

    if(len(res[1])==0):
        with res[0].cursor() as cursor:
            consulta = "INSERT INTO usuarios(nombre, contrasena) VALUES (%s, %s);"                         
            cursor.execute(consulta, (user, generate_password_hash(password)))                    
            res[0].commit()
            mensaje = 'usuario creado'
    else:
        mensaje = "Usuario ya existe, tal vez es tu clon malvado"
    res[0].close()

    return mensaje

def realizarConsulta(consulta, user):
    conexion = pymysql.connect( host=host, user= userDB, passwd=passDB, db=DB )
        
    with conexion.cursor() as cursor:
        cursor.execute(consulta, (user))
        datosUser = cursor.fetchall()
    
    return [conexion, datosUser]
    