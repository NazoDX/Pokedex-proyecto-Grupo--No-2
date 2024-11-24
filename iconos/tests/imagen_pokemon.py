"""import requests
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
from io import BytesIO

def obtener_imagen_pokemon(pokemon_nombre):
    # Crear la URL usando el nombre del Pokémon
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_nombre.lower()}/'
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        # Obtener la URL de la imagen
        imagen_url = datos['sprites']['other']['official-artwork']['front_default']
        return imagen_url
    else:
        print(f'Error al obtener el Pokémon con nombre "{pokemon_nombre}": {respuesta.status_code}')
        return None

def mostrar_imagen(pokemon_nombre):
    # Obtener la URL de la imagen del Pokémon
    imagen_url = obtener_imagen_pokemon(pokemon_nombre)
    if not imagen_url:
        return

    # Descargar la imagen desde la URL
    respuesta_imagen = requests.get(imagen_url)
    if respuesta_imagen.status_code == 200:
        imagen_datos = Image.open(BytesIO(respuesta_imagen.content))

        # Redimensionar la imagen para que se ajuste a la ventana
        imagen_datos = imagen_datos.resize((300, 300))

        # Convertir la imagen a un formato compatible con Tkinter
        imagen_tk = ImageTk.PhotoImage(imagen_datos)

        # Mostrar la imagen en la ventana
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk  # Mantener referencia para evitar que se elimine
    else:
        print(f"Error al descargar la imagen del Pokémon: {respuesta_imagen.status_code}")

# Crear ventana principal
ventana = Tk()
ventana.title("Pokémon Viewer")

# Etiqueta para mostrar la imagen
etiqueta_imagen = Label(ventana)
etiqueta_imagen.pack(pady=10)

# Botón para buscar Pokémon
boton_buscar = Button(ventana, text="Buscar Pikachu", command=lambda: mostrar_imagen("pikachu"))
boton_buscar.pack(pady=20)

# Iniciar la ventana
ventana.mainloop()"""

import requests
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
from io import BytesIO

def obtener_imagen_pokemon(pokemon_nombre, shiny=False):
    # Crear la URL usando el nombre del Pokémon
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_nombre.lower()}/'
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        # Verificar si la imagen shiny está disponible
        if shiny:
            imagen_url = datos['sprites']['other']['official-artwork']['front_shiny']
        else:
            imagen_url = datos['sprites']['other'].get('official-artwork', {}).get('front_default', None)

        if imagen_url:
            return imagen_url
        else:
            print(f'Imagen { "shiny" if shiny else "normal"} no disponible para {pokemon_nombre}.')
            return None
    else:
        print(f'Error al obtener el Pokémon con nombre "{pokemon_nombre}": {respuesta.status_code}')
        return None

def mostrar_imagen(pokemon_nombre, shiny=False):
    # Obtener la URL de la imagen del Pokémon
    imagen_url = obtener_imagen_pokemon(pokemon_nombre, shiny)
    if not imagen_url:
        return

    # Descargar la imagen desde la URL
    respuesta_imagen = requests.get(imagen_url)
    if respuesta_imagen.status_code == 200:
        imagen_datos = Image.open(BytesIO(respuesta_imagen.content))

        # Redimensionar la imagen para que se ajuste a la ventana
        imagen_datos = imagen_datos.resize((300, 300))

        # Convertir la imagen a un formato compatible con Tkinter
        imagen_tk = ImageTk.PhotoImage(imagen_datos)

        # Mostrar la imagen en la ventana
        etiqueta_imagen.config(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk  # Mantener referencia para evitar que se elimine
    else:
        print(f"Error al descargar la imagen del Pokémon: {respuesta_imagen.status_code}")

# Crear ventana principal
ventana = Tk()
ventana.title("Pokémon Viewer")

# Etiqueta para mostrar la imagen
etiqueta_imagen = Label(ventana)
etiqueta_imagen.pack(pady=10)

# Botón para buscar Pokémon normal
boton_buscar_normal = Button(ventana, text="Buscar Pikachu Normal", command=lambda: mostrar_imagen("pikachu", shiny=False))
boton_buscar_normal.pack(pady=5)

# Botón para buscar Pokémon shiny
boton_buscar_shiny = Button(ventana, text="Buscar Pikachu Shiny", command=lambda: mostrar_imagen("pikachu", shiny=True))
boton_buscar_shiny.pack(pady=5)

# Iniciar la ventana
ventana.mainloop()
