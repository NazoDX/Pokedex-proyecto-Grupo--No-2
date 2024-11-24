# clase padre a heredar para el uso de agregar pokemon 
class Plantilla_Pokemon:
    def __init__(self,id, nombre, descripcion, tipo, peso, altura, habilidad, stats,animacion,animacion_femenino,shiny,grito, minis):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo
        self.peso = peso
        self.altura = altura
        self.habilidad = habilidad
        self.stats = stats
        self.animacion = animacion
        self.animacion_femenino = animacion_femenino
        self.shiny = shiny
        self.grito = grito
        self.minis = minis
        
        # faltara ponerle animacion femenina
        # falta ponerle las 3 evoluciones
        # falta ponerle animacion shiny

    # Getters generales
    def get_id(self):
        return self.id
    
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
    
    # Gif animado 
    def get_animacion(self):
        return self.animacion
    
    # Gif animado femenino
    def get_animacion_femenino(self):
        return self.animacion_femenino
    
    #Gif shiny 
    def get_shiny(self):
        return self.shiny
    
    # Sonido .wav
    def get_grito(self):
        return self.grito
    
    # Diccionario de rutas de la evolucion del pokemon
    def get_minis(self):
        return self.minis
    
    # Retorna la ruta de la imagen del pokemon 
    def get_minis_1(self):
        return self.get_minis()["mini_1"]
    
    # Retorna la ruta de la imagen del pokemon su evolucion
    def get_minis_2(self):
        return self.get_minis()["mini_2"]
    
    # Retorna la ruta de la imagen del pokemon su sigiente evolucion
    def get_minis_3(self):
        return self.get_minis()["mini_3"]

    # Getters específicos para cada estadística
    def get_ps(self):
        return self.stats.get("ps")

    def get_ataque(self):
        return self.stats.get("ataque")

    def get_defensa(self):
        return self.stats.get("defensa")

    def get_special_ataque(self):
        return self.stats.get("special-ataque")

    def get_defensa_especial(self):
        return self.stats.get("defensa_especial")

    def get_velocidad(self):
        return self.stats.get("velocidad")
    
    def __str__(self):
        return f"""
Id-{self.id}
Nombre: {self.nombre},
Descripción: {self.descripcion},
Tipo: {', '.join(self.tipo)},
Peso: {self.peso}g,
Altura: {self.altura}cm
Hablidad: {', '.join(self.habilidad)}
Stats:
    ps: {self.get_ps()}
    ataque: {self.get_ataque()}
    defensa: {self.get_defensa()}
    ataque-especial: {self.get_special_ataque()}
    defensa-especial: {self.get_defensa_especial()}
    velocidad: {self.get_velocidad()}
femenino: {self.animacion_femenino},
shiny: {self.shiny},
minis{self.minis}
ruta animacion: {self.animacion}
ruta sonido: {self.grito}"""

"""
COMO SE VE LA ESTRUCTURA EN TERMINAL 
"bulbasaur": {
        "descripcion": "Una rara semilla le fue plantada en el lomo al nacer.\nLa planta brota y crece con este Pokémon.",
        "tipo": [
            "grass",
            "poison"
        ],
        "peso": 69,
        "altura": 7,
        "habilidad": [
            "chlorophyll",
            "overgrow"
        ],
        "stats": {
            "ps": 45,
            "ataque": 49,
            "defensa": 49,
            "special-ataque": 65,
            "defensa_especial": 65,
            "velocidad": 45
        },
        "animacion": "gifs\\1.GIF",
        "femenino": null,
        "shiny": "gifs_shiny\\1.GIF",
        "minis": "minis{'mini_1': 'iconos\\151.PNG', 'mini_2': None, 'mini_3': None}",
        "grito": "sounds\\cries\\bulbasaur.wav"
    }

"""
