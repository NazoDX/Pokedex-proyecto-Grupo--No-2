import requests

"""
Este archivo se encarga de las funcionalidades de búsqueda de PokeAPI (por región y generación).
"""

# Definir la clase Api_pokemon (se cambió el nombre para evitar conflictos con otra clase llamada Pokemon)
class Api_pokemon:
    def __init__(self, numero, nombre, peso, altura, stats, tipo, habilidad, descripcion, imagen, shiny):
        # Inicializa los atributos del objeto Pokémon con los datos proporcionados
        self.numero = numero
        self.nombre = nombre
        self.peso = peso
        self.altura = altura
        self.stats = stats
        self.tipo = tipo
        self.habilidad = habilidad
        self.descripcion = descripcion
        self.imagen = imagen
        self.shiny = shiny

    def to_dict(self):
        # Convierte el objeto Pokémon a un diccionario
        return {
            "numero": self.numero,
            "nombre": self.nombre,
            "peso": self.peso,
            "altura": self.altura,
            "stats": self.stats,
            "tipo": self.tipo,
            "habilidad": self.habilidad,
            "descripcion": self.descripcion
        }
        
    # Métodos para obtener información del Pokémon
    def get_id(self):
        return self.numero
    
    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion

    def get_tipo(self):
        return self.tipo

    def get_peso(self):
        return self.peso

    def get_altura(self):
        return self.altura

    def get_habilidad(self):
        return self.habilidad
    
    # Método para obtener la imagen (GIF animado)
    def get_imagen(self):
        return self.imagen
    
    def get_shiny(self):
        return self.shiny

    # Getters específicos para cada estadística
    def get_ps(self):
        return self.stats.get("hp")

    def get_ataque(self):
        return self.stats.get("attack")

    def get_defensa(self):
        return self.stats.get("defense")

    def get_special_ataque(self):
        return self.stats.get("special-attack")

    def get_defensa_especial(self):
        return self.stats.get("special-defense")

    def get_velocidad(self):
        return self.stats.get("speed")  # Corrige el nombre de la estadística a "speed"
    

# Función para obtener la información del Pokémon como objeto usando su nombre
def obtener_pokemon_nombre(nombre_pokemon):
    """
    Función para obtener los datos del Pokémon a partir de su nombre.
    Esta función obtiene información de la API de Pokémon y organiza los datos.
    """
    # Construir la URL para obtener los datos generales del Pokémon usando su nombre
    url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}/'

    try:
        # Realizar una solicitud GET para obtener los datos generales del Pokémon
        respuesta_pokemon = requests.get(url_pokemon, timeout=10)
        respuesta_pokemon.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
        datos_pokemon = respuesta_pokemon.json()  # Convertir la respuesta JSON a un diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos del Pokémon {nombre_pokemon}: {e}")
        return None  # En caso de error, retornar None

    # Extraer el ID del Pokémon
    id_pokemon = datos_pokemon['id']
    print(f"ID obtenido para {nombre_pokemon}: {id_pokemon}")  # Depuración

    # Construir la URL para obtener los datos de la especie (descripción) usando el ID
    url_species = f'https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}/'

    try:
        # Realizar una solicitud GET para obtener los datos de la especie (descripción)
        respuesta_species = requests.get(url_species, timeout=10)
        respuesta_species.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
        datos_species = respuesta_species.json()  # Convertir la respuesta JSON a un diccionario

        # Buscar la descripción en español
        descripcion = next(
            (entry['flavor_text'] for entry in datos_species['flavor_text_entries'] if entry['language']['name'] == 'es'),
            "Sin descripción"
        ).replace("\n", " ").replace("\f", " ")  # Limpiar la descripción de caracteres no deseados
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la descripción del Pokémon con ID {id_pokemon}: {e}")
        descripcion = "Sin descripción"  # Si no se puede obtener la descripción, asignar un valor por defecto

    # Extraer más información relevante del Pokémon
    nombre = datos_pokemon['name']
    peso = datos_pokemon['weight']
    altura = datos_pokemon['height']
    tipo = [type_info['type']['name'] for type_info in datos_pokemon['types']]  # Obtener los tipos del Pokémon
    stats = {stat['stat']['name']: stat['base_stat'] for stat in datos_pokemon['stats']}  # Obtener estadísticas
    habilidad = [habilidad_info['ability']['name'] for habilidad_info in datos_pokemon['abilities']]  # Obtener habilidades
    imagen = datos_pokemon['sprites']['other']['official-artwork']['front_default']  # Obtener imagen normal
    shiny = datos_pokemon['sprites']['other']['official-artwork']['front_shiny']  # Obtener imagen shiny

    # Crear el objeto Pokémon con todos los datos obtenidos y retornarlo
    return Api_pokemon(id_pokemon, nombre, peso, altura, stats, tipo, habilidad, descripcion, imagen, shiny)


# Función para obtener la información del Pokémon como objeto usando su ID
def obtener_pokemon_numero(identificador):
    """
    Obtiene los datos del Pokémon a partir de su nombre o número de Pokédex.
    """
    # Construir las URLs para obtener datos del Pokémon y de su especie
    url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{str(identificador).lower()}/'
    url_species = f'https://pokeapi.co/api/v2/pokemon-species/{str(identificador).lower()}/'
    
    # Obtener datos generales del Pokémon
    respuesta_pokemon = requests.get(url_pokemon)
    if respuesta_pokemon.status_code != 200:
        print(f'Error al obtener el Pokémon {identificador}: {respuesta_pokemon.status_code}')
        return None  # Retorna None si hay un error en la solicitud

    datos_pokemon = respuesta_pokemon.json()  # Convierte la respuesta a JSON
    
    # Obtener datos de especies para la descripción
    respuesta_species = requests.get(url_species)
    if respuesta_species.status_code != 200:
        print(f'Error al obtener la descripción del Pokémon {identificador}: {respuesta_species.status_code}')
        descripcion = "Sin descripción"  # Asigna una descripción por defecto si hay un error
    else:
        datos_species = respuesta_species.json()
        # Busca la descripción en español
        descripcion = next(
            (entry['flavor_text'] for entry in datos_species['flavor_text_entries'] if entry['language']['name'] == 'es'),
            "Sin descripción"
        ).replace("\n", " ").replace("\f", " ")  # Limpia la descripción

    # Extraer información relevante del Pokémon
    id_pokemon = datos_pokemon['id']
    nombre = datos_pokemon['name']
    peso = datos_pokemon['weight']
    altura = datos_pokemon['height']
    tipo = [type_info['type']['name'] for type_info in datos_pokemon['types']]
    stats = {stat['stat']['name']: stat['base_stat'] for stat in datos_pokemon['stats']}
    habilidad = [habilidad_info['ability']['name'] for habilidad_info in datos_pokemon['abilities']]
    imagen = datos_pokemon['sprites']['other']['official-artwork']['front_default']
    shiny = datos_pokemon['sprites']['other']['official-artwork']['front_shiny']

    # Crear el objeto Pokémon y retornarlo
    return Api_pokemon(id_pokemon, nombre, peso, altura, stats, tipo, habilidad, descripcion, imagen, shiny)
