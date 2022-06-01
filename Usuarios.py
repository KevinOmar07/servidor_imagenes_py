from werkzeug.security import generate_password_hash, check_password_hash

import conexionBD

def signIn(data):
    user = data['data']['user']
    password = data['data']['password']
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
            print("Cierra conexion sing in")
            res[0].close()
    return estado

def signUp(data):
    user = data['data']['user']
    password = data['data']['password']    
    res = realizarConsulta("SELECT nombre FROM usuarios where nombre=%s;", user)

    conexion = res[0]

    if(len(res[1])==0):
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuarios(nombre, contrasena) VALUES (%s, %s);"                         
            cursor.execute(consulta, (user, generate_password_hash(password)))                    
            conexion.commit()
            mensaje = 'usuario creado'
    else:
        mensaje = "Usuario ya existe, tal vez es tu clon malvado"    
    conexion.close()

    return mensaje

def realizarConsulta(consulta, user):    
    conexion = conexionBD.DBConnection().conexion        
    with conexion.cursor() as cursor:        
        cursor.execute(consulta, (user))
        datosUser = cursor.fetchall()
        
    return [conexion, datosUser]
    