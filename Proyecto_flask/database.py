import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ejercicios_flask"
    )

    return conexion
conexion = conectar()

if conexion.is_connected():
    print("✅ Conexión exitosa a MySQL")

conexion.close()