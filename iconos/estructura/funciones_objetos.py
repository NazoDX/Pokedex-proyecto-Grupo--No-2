from instancias_pokemon import *

"""
Este archivo se encarga de las busquedas de x pokemon

metodos:
-busqueda por numero y nombre,
-tambien los pokemones de x tipo

este archivo funciona en conjunto con las intancias_pokemon

por lo que con modularidad puedes llamar unicamente este archivo.
"""


class Funciones:
    
    # Almacenamos en una variable los objetos para más comodidad
    datos_pokemon = Pokemon.pokemons_objetos
    
    # Metodo de clase especifico para actualizar la lista de pokemon(objetos)
    # Esto es mejor logico cuando se agrega un pokemon asi lo incluye.
    @classmethod
    def actualizar_dic(cls):
        # Actualiza la lista de Pokémon desde los objetos de la clase Pokemon
        cls.datos_pokemon = []
        cls.datos_pokemon = Pokemon.pokemons_objetos
        
    #Metodo de clase busqueda de pokemon por nombre
    @classmethod
    def buscar_pokemon_nombre(cls, nombre):
        
        # ahora la lista contiene los objetos pokemon
        """
        Busca un Pokémon por su nombre.
        
        Argumento:
        - nombre: str, el nombre del Pokémon a buscar.
        
        Retorna:
        - El objeto Pokémon si se encuentra, sino retona None si no se encuentra.
        """

        for pokemon in cls.datos_pokemon:
            # Verificar si el nombre del Pokémon coincide con el argumento
            if nombre == pokemon.get_nombre():
                print(f"Se encontró el Pokémon: {pokemon.get_nombre()}")
                return pokemon
        
        # Si no se encuentra el Pokémon, imprimir mensaje y retorna None
        print("No se encuentra el Pokémon")
        return None
    
    # Metodo de clase busqueda de pokemon por ID o numero.
    @classmethod
    def buscar_pokemon_numero(cls, numero):  
        """
        Busca un Pokémon por su número (ID).
        
        Argumento:
        - numero: int, el número ID del Pokémon a buscar.
        
        Retorna:
        - El objeto Pokémon si se encuentra, sino retona None si no se encuentra.
        """

        # Recorrer la lista y buscar por ID
        for pokemon in cls.datos_pokemon:
            if numero == pokemon.get_id():
                print(f"Se encontró el Pokémon: {pokemon.get_nombre()}")
                return pokemon
            
        # Si no encontro el pokemon imrpime y retorna None
        print("No se encuentra el Pokémon")
        return None
    
    # Metodo de clase busqueda de pokemons por x tipo.
    @classmethod
    def buscar_pokemon_tipo(cls, tipo):
        """ 
        Busca Pokémon por tipo y devuelve una lista de coincidencias.
        
        Argumento:
        - tipo: str, x tipo del Pokémon a buscar (por ejemplo, "grass").
        
        Retorna:
        - Una lista de nombres de Pokémon que coinciden con el tipo.
        """   
        # Almacena los pokemones de x tipo     
        lista_tipos = []
        
        # Recorrer el diccionario de objetos
        for pokemon in cls.datos_pokemon:
            # Por cada pokemon tomar el tipo
            tipos = pokemon.get_tipo()
            # Recorre la lista [] que contiene los nombres de los tipos.
            for contenido in tipos:
                if contenido == tipo:
                    nombre = pokemon.get_nombre()
                    nombre = nombre.capitalize()
                    # Si se cumple lo agregara a la lista e imprimira el pokemon con informacion veridica
                    lista_tipos.append(f"{pokemon.get_id()} {nombre}")
                    print(f"{pokemon.get_id()} {pokemon.get_nombre()} Tipo: {pokemon.get_tipo()}")
                    
        # Retorna la lista con los nombres de los pokemons de x tipo
        return lista_tipos
    

# USO
# primero que nada inicializar los objetos
#
# Pokemon.inicializar_objetos()
# Pokemon.mostrar_objetos() "opcional"

# ahora podemos hacer la busqueda recuerda numero int y nombre si o si str
#
#poke2 = Funciones.buscar_pokemon_numero(1)
#poke1 = Funciones.buscar_pokemon_nombre("muk")

# Pokemones de cierto tipo

#print(Funciones.buscar_pokemon_tipo("poison")) 
#print(Funciones.buscar_pokemon_tipo("fire"))

# se pueden almacenar todo ello en una variable por su puesto ya que retornda dato.