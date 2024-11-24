from clase_padre import Plantilla_Pokemon
import sqlite3

"""
Este archivo funciona para la instancia automatica 
de los pokemones.

Hereda de la clase padre Plantilla_pokemon tomando 
como atributo cada apartado de la tabla en la base de datos.

Convierte cada pokemon en la bd en un objeto. 
"""


# esta clase hereda de la plantilla para cada pokemon
class Pokemon(Plantilla_Pokemon):
    def __init__(self, id, nombre, descripcion, tipo, peso, altura, habilidad, stats, animacion, animacion_femenino, shiny, grito, minis):
        super().__init__(id, nombre, descripcion, tipo, peso, altura, habilidad, stats, animacion, animacion_femenino, shiny, grito, minis)
        
        
    # Lista para almacenar objetos en este caso pokemons
    pokemons_objetos = []
    
    
    # Metodo de clase usara la variable que almacena los pokemons
    @classmethod
    def inicializar_objetos(cls):
        
        # Conectar a la base de datos
        conexion = sqlite3.connect("estructura\\pokedex.db")
        
        # Crear un cursor para interactuar con la base de datos
        cursor = conexion.cursor()
        
        # Ejecutar una consulta para obtener todos los registros de la tabla pokemon
        cursor.execute("SELECT id, nombre, descripcion, tipo, peso, altura, habilidad, stats, animacion, femenino, shiny, minis, grito FROM pokemon")
        
        # Obtener los datos en la variable 
        pokemons_data = cursor.fetchall()
        
        # Limpiar la lista antes de agregar nuevos objetos para no tener problemas
        cls.pokemons_objetos.clear()

        # Crear un objeto para cada registro de la base de datos y añadirlo a la lista
        for data in pokemons_data:
            # Desempaquetar los datos de cada Pokémon para usarlos como atributos
            id, nombre, descripcion, tipo, peso, altura, habilidad, stats, animacion, animacion_femenino, shiny, minis, grito = data
            
            # Intentar cambiar en el str de las rutas minis(evoluciones) remplazar \ por \\ para evitar problemas
            try:
                ruta_minis = minis.replace("\\", "\\\\")
            except:
                pass
            
            # Como se obtiene un str remplazamos los [] por "", " por "", y " " por ""
            # Ya que una lista no se pudo guardar exactamente en la db de sqlite
            try:
                tipo_lista = tipo.replace("[", "").replace("]", "").replace("\"", "").replace(" ", "").split(',')
                habilidad_lista = habilidad.replace("[", "").replace("]", "").replace("\"", "").replace(" ", "").split(',')    
            except:
                pass
            
            
            # Crear el objeto Pokémon usando los datos obtenidos
            pokemon_objeto = Pokemon(
                id= id,
                nombre=nombre,
                descripcion=descripcion,
                tipo=tipo_lista, #lista que era un string separado por comas
                peso=peso,
                altura=altura,
                habilidad=habilidad_lista,  #lista que era un string separado por comas
                stats=eval(stats),  # Usar eval este sirve para convertir el string a un diccionario si es seguro
                # en este caso los stats son diccionario con contentenido 
                animacion=animacion, # Ruta .GIF
                animacion_femenino=animacion_femenino, # Ruta .GIF
                shiny=shiny, # Ruta .GIF
                minis=eval(ruta_minis),# Usar eval este sirve para convertir el string a un diccionario si es seguro
                # en este caso los minis es un diccionario con contentenido rutas
                grito=grito # ruta .wav
            )

            # Agregar el objeto a la lista de objetos Pokémon
            cls.pokemons_objetos.append(pokemon_objeto)
            print(f"{nombre.capitalize()} creado como objeto Pokémon")

        # Cerrar la conexión a la base de datos
        conexion.close()
        
    #Intanciar los objetos 
    # Pokemon.inicializar_objetos() imprime los pokemones que se acaban de crear como objetos 
        
        
    # Metodo de clase unicamente para verificar los pokemones instanciados muestra el metodo str de cada pokemon.
    @classmethod
    def mostrar_objetos(cls):
        for pokemon in cls.pokemons_objetos:
            print(pokemon)
    # Mostrar los objetos o pokemones ya instanciados 
    # Pokemon.mostrar_objetos (solo funciona si se han instanciado los objetos anteriormente.)
    
            


