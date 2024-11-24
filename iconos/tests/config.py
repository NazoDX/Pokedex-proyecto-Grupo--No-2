
"""
SOLO PARA PROBAR LA CONEXION CON BASE DE DATOS NO SE VINCULA CON NINGUN ARCHIVO
"""
import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect("pokedex.db")

# Crear un cursor para interactuar con la base de datos
cursor = conexion.cursor()

# Ejecutar una consulta para obtener todos los registros de la tabla pokemon
cursor.execute("SELECT * FROM pokemon") # una consulta por asi decirlo 
# Obtener los datos
pokemones = cursor.fetchall()

# Mostrar cada registro
for pokemon in pokemones:
    print(pokemon)

# Cerrar la conexión
conexion.close()
