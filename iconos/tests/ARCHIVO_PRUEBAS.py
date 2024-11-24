import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox

from PIL import Image, ImageTk # Pillow su uso es para imagenes y gifs animados en la ventana
from funciones_objetos import Funciones, Pokemon # Modularidad funciones para busqueda de pokemon
import pygame # Su uso es unicamente para reproducir sonido

from api_generacion import * # importamos las funcionalidades de busqueda por la api
from io import BytesIO

from listas_pokemons import *

"""
Este es el archivo principal donde ocurre todo lo relacionado
con la interfaz grafica.


# se encarga de ser la busqueda principal (donde buscas los pokemons en la pokedex)
-mostrar_busqueda()
    --actualizar_lista() # se encarga de actualizar el contenido de la listbox y lo relacionado a ella como por ejemplo que aparezca cuando se seleciona un tipo 
                            (listbox es donde se muestra la lista de pokemons por x tipo)
    --selecion_tipo() # se encarga que el pokemon selecionado en la lista de pokemons por tipo se muestre en la barra de busqueda y aparezca su imagen previa.
    --buscar() # este es comando para el boton de busqueda tiene las validaciones de entrada y si se cumple con ello dara inicio a la ventana de informacion.
            --mostrar_ventana() # esta es una ventana que aparece gracias al boton de busqueda mencionado, aqui se muestra todo sobre x pokemon.

# Aqui es la busqueda de pokemon por generaciones (quitando de lado las de primer gen que fue principalmente)  
-mostrar_generaciones()
    --actualizar_lista_gen() # se encarga de actualizar el contenido de la listbox y lo relacionado a ella como por ejemplo que aparezca cuando se seleciona un tipo 
                            (listbox es donde se muestra la lista de pokemons de x region o generacion)
    --selecion_tipo_gen() # se encarga que el pokemon selecionado en la lista de pokemons por tipo se muestre en la barra de busqueda.
    --buscar_gen() # este es comando para el boton de busqueda tiene las validaciones de entrada y si se cumple con ello dara inicio a la ventana de informacion de x pokemon.
            --mostrar_ventana_gen() # esta es una ventana que aparece gracias al boton de busqueda mencionado, aqui se muestra todo sobre x pokemon.
            
--limpiar_contenido() # se encarga de eliminar todos los widgets mostrados en la ventana para no haber problemas a la hora de pasar de busqueda y agregar pokemon 
                        asi no se sobre pone el contenido de ellas.
"""


#---Reproducir musica al ejecutarse
pygame.mixer.init()
# Ruta de la musica a reproducirse durante el programa
music_path = "sounds\\songs\\Pokémon_Center.mp3"
pygame.mixer.music.load(music_path)  # Carga del archivo o reproducion
pygame.mixer.music.play(-1)  # Reproducir en bucle indefinidamente
original_volume = 0.1  # Volumen original de la música
pygame.mixer.music.set_volume(0.1)

# Encargada de la busqueda de pokemon
def mostrar_busqueda():
    
    # Función que elimina todos los widgets en la ventana
    limpiar_contenido()
    
    # Inicializar los objetos una vez se ejecute la pokedex
    Pokemon.inicializar_objetos()
    Funciones.actualizar_dic()

    # Asegúrate de que la ruta sea correcta
    fondo_imagen = Image.open("fondos\\Pantalla.png")
    # Redimensionar la imagen de fondo para que se ajuste al tamaño de la ventana
    fondo_imagen_redimensionada = fondo_imagen.resize((ventana.winfo_width(), ventana.winfo_height()))  
    # Variable que tendra la imagen.
    fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen_redimensionada)

    # Crear el label para la imagen de fondo y colocarla en el fondo
    global label_fondo
    label_fondo = tk.Label(contenido_frame, image=fondo_imagen_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo_imagen_tk  # Mantener la referencia de la imagen
    
    # Opciones de los tipos de Pokémon de la primera generación
    # se usara para la cajita desplegable de opciones o combobox
    opciones = [
        "normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison",
        "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
    ]

    # NOTA:
    # si una variable se pone (global var) significa que se usara tanto fuera como dentro de cualquier lugar
    # del codigo con fines de modificar/ actualizar su contenido

    # Entrada para buscar Pokémon
    global entrada_busqueda
    entrada_busqueda = tk.Entry(contenido_frame,width=24,font=("Pokemon Classic", 9))
    entrada_busqueda.place(x=1060, y=45, anchor="center")

    # Combobox para la busqueda por tipo
    global combobox
    combobox = Combobox(contenido_frame, values=opciones, state="readonly",font=("Pokemon Classic", 9))
    combobox.set("Busqueda por tipo")  # Texto inicial
    combobox.place(x=375, y=50, anchor="center")

    # Listbox para mostrar los Pokémon encontrados (es la lista que aparece x pokemon de n tipo)
    # variable global su uso es que se modifica su contenido
    global lista
    lista = tk.Listbox(contenido_frame, background="black", fg="white", font=("Pokemon Classic", 15))
    lista.place_forget() # se agrega pero queda sin uso para su aparicion si se seleciona un tipo(mas adelante se vera)
    
    # un scrollbar para visualizar los pokemons (esta va con la listbox)
    global scrollbar
    scrollbar = tk.Scrollbar(contenido_frame)
    scrollbar.place_forget() # se agrega pero queda sin uso para su aparicion si se seleciona un tipo(mas adelante se vera)
    
    # Vincular el Listbox con el Scrollbar
    lista.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista.yview)
    
    # Label para ver la vista previa del pokemon
    global imagen_pokemon
    imagen_pokemon = tk.Label(contenido_frame, background="black")
    imagen_pokemon.place(x=980, y=380, anchor="center")
    
    # Botón de búsqueda con imagen 
    imagen = Image.open("fondos\\lupa.png")# ruta de imagen 
    imagen_redimensionada = imagen.resize((41, 19))# Redimensionar la imagen
    # Convertir la imagen redimensionada en un formato que Tkinter pueda usar
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
    
    # Crear un botón con la imagen                                        # ojito comando buscar 
    boton_buscar = tk.Button(contenido_frame,image=imagen_tk, compound="left",command=buscar,width=41,height=19)
    boton_buscar.place(x=1250, y=45, anchor="center")
    # Es importante mantener una referencia de la imagen
    boton_buscar.image = imagen_tk # Esto mantiene la imagen en memoria
    
    """Eventos en busqueda"""
    # Vincular el evento de cambio de selección en el Combobox con la función de actualizar_lista
    combobox.bind("<<ComboboxSelected>>", actualizar_lista)

    # Vincular el evento de selección del Listbox para mostrar el nombre en el buscador e imagen previa
    lista.bind("<<ListboxSelect>>", selecion_tipo)


""" PARA USO PRICIPAL DE BUSQUEDA"""
# Función para actualizar la lista de Pokémon en base al tipo seleccionado
def actualizar_lista(event):
    """
    Esta funcion al ser llamada hace que en la list box segun el tipo de pokemon selecionado 
    en la combobox apareceran a elecion los pokemons de ese tipo
    """

    # Limpiar el Listbox antes de insertar los nuevos pokemon por su tipo
    lista.delete(0, tk.END)
    
    # Poner la listbox para poder selecionarla
    lista.config(state="normal")

    # Obtener el tipo seleccionado
    tipo_seleccionado = combobox.get()

    # Se imprime la sleccion en la terminal
    # Verifica que se recibe correctamente el tipo
    print(f"Tipo seleccionado: {tipo_seleccionado}")

    tipo_seleccionado = tipo_seleccionado.lower()
    
    # Verifica que la función de búsqueda retorne una lista
    pokemon_tipo = Funciones.buscar_pokemon_tipo(tipo_seleccionado)
    # si se cumple:
    if pokemon_tipo: 
        lista.delete(0, tk.END) # nos aseguramos que se limpie la listbox
        lista.config(state="normal")# Si la lista no está vacía(imposible que no este vacia) pero ahi va el condicional
        
        for pokemon in pokemon_tipo:
            lista.insert(tk.END, pokemon)# Insertar los nombres de los Pokémon en el Listbox
            if pokemon_tipo:
                #Nota: aqui se podria modificar mas tarde
                # hace aparecer la lista de pokemones por tipo
                
                # Que ahora si aparezca en pantalla la listbox
                lista.place(x=280, y=350, anchor="center",)
                
                # Tambien el scrollbar para la busqueda por tipo
                scrollbar.place(x=520, y=350, anchor="center",height=345)
    else:
        # Si no hay ningun pokemon y no nos retorna una lista 
        
        # inserta que no hay pokemones mas que todo para el tipo dark
        lista.insert(tk.END, "No hay registrados")
        # desactiva temporalmente la selecion 
        lista.config(state="disabled")
        # y muestra la lista nula
        lista.place(x=280, y=350, anchor="center",)


""" Para uso principal BUSQUEDA"""
# Encargada de la selecion en la lisbox 
def selecion_tipo(event):

    # Obtener el índice del Pokémon seleccionado
    seleccionado = lista.curselection()
    
    # Solo si se ha selecionado
    if seleccionado:
        # Obtener el nombre del Pokémon
        pokemon_seleccionado = lista.get(seleccionado[0])
        
        # Creamos la variable resultado que sera un str vacio para obtener el nombre del pokemon
        resultado = ""
        
        # Hora como en la lisbox se muestra (25 pikachu)
        # nos encargamos de quitar los espacios y los numeros
        
        for caracter in pokemon_seleccionado:
            if not caracter.isdigit() and not caracter.isspace():
                resultado += caracter # ir concatenando cada letra

        entrada_busqueda.delete(0, tk.END)  # Limpiar la entrada de búsqueda
        
        entrada_busqueda.insert(0, resultado)  # ahora la busqueda tomara el nombre del pokemon
        
        # Ahora buscara el pokemon para mostrar su imagen
        resultado = resultado.lower()
        pokemon = Funciones.buscar_pokemon_nombre(resultado)
        
        try:
            # Obtener la ruta del gif del Pokémon
            # Asumiendo que este método devuelve la ruta del gif
            gif_ruta = pokemon.get_animacion()

            # Cargar el gif usando Pillow
            gif_imagen = Image.open(gif_ruta)
            gif_imagen = ImageTk.PhotoImage(gif_imagen)

            # Mostrar el gif en el label que se creo en mostrar_busqueda()
            imagen_pokemon.config(image=gif_imagen)
            # Mantener una referencia al gif para evitar que se destruya
            imagen_pokemon.image = gif_imagen
        except Exception as e:
            # en caso que no se pueda cargar su imagen.
            imagen_pokemon.config(text="No se pudo cargar la animación.")
            print(f"Error al cargar la animación: {e}")


""" Para uso principal (boton buscar o enviar)"""
# Función para buscar Pokémon por nombre o número
def buscar():

    # Verifica que no se envie nada en blanco
    if entrada_busqueda.get() == "":
        messagebox.showerror("Error", "Debe de llenar el campo")
    else:
        try:
            # intenta convertir a numero entero (numero pokemon) si es posible seguira
            busqueda = int(entrada_busqueda.get())
            print("Se ha ingresado un numero")
            # se lo dejo si queremos dejar el easter egg de missingno
            if busqueda >= 0:
                pokemon = Funciones.buscar_pokemon_numero(busqueda)
                
                # si el objeto existe
                if pokemon:  # si no existe el pokemon 200 retornaria falso
                    print(pokemon)
                    mostrar_busqueda() # Resetea el frame empieza desde 0
                    mostrar_ventana(pokemon)# hace aparecer la ventana con la informacion
                    
                else:
                    messagebox.showerror("Error", "Pokemon no registrado")
                # si se ha ingresado un numero negativo
            else:
                messagebox.showerror("Error", "Ingrese un numero valido")

        except:
            # si no es numero lo que se envia
            # es un nombre
            busqueda = entrada_busqueda.get()
            busqueda = busqueda.lower()
            # este en casos especiales donde

            # si el la busqueda es texto letras intentara buscar el pokemon
            if busqueda.isalpha():
                print("se ha ingresado texto")
                pokemon = Funciones.buscar_pokemon_nombre(busqueda)
                
                # el mismo caso si es verdad lo hara sino retorna none
                if pokemon:
                    # dar paso a la ejecucuion de la ventana con informacion
                    print(pokemon)
                    # hacer desde 0 cada ves que se busca el pokemon
                    # mejor dicho si existe
                    mostrar_busqueda()
                    mostrar_ventana(pokemon)
                else:
                    messagebox.showerror("Error", "Pokemon no registrado")
                # si en la busquda lo ingresado es diferente de letras
            else:
                messagebox.showerror("Error", "Ingrese un nombre valido")


# /////////////////////////////////////////////////////////////////////////////

"""VENTANA PARA MOSTRAR POKEMON"""

def mostrar_ventana(objeto):
    
    
    # Objetiendo el nombre del pokemon para su nombre en ventana
    nombre = objeto.get_nombre()
    nombre = nombre.capitalize()
    
    # Crear la ventana secundaria
    ventana_info = tk.Toplevel(ventana)  # 'ventana' es la ventana principal
    ventana_info.title(nombre)  # Título de la nueva ventana pokemon elejido
    
    # Definimos un tamaño fijo para la ventana
    ventana_info.geometry("1362x695")
    ventana_info.resizable(False, False) # Bloquea el minimizar pantallla.
    
    # Crear el lienzo (Canvas)
    # Ruta de la imagen de fondo
    fondo_path = "Pantalla.png"
    imagen_fondo = Image.open(fondo_path)
    
    # Tomamos en 2 variables el ancho y alto de la ventana
    width = ventana_info.winfo_width()
    height = ventana_info.winfo_height()
    
    # Crear el lienzo (Canvas) se ha decidido usarlo para sobreponer imagenes (el fondo con el gif del pokemon)
    canvas = tk.Canvas(ventana_info, width=width, height=height)
    canvas.pack(fill="both", expand=True)
    
    
    # Redimensionamos la imagen solo cuando sea necesario
    # Redimensionar según el tamaño de la ventana
    imagen_fondo_resized = imagen_fondo.resize((1362, 695))
    fondo = ImageTk.PhotoImage(imagen_fondo_resized)
    
    # Mostrar la imagen de fondo en el lienzo
    canvas.create_image(2, 2, image=fondo, anchor="nw")
    
    # Mantener una referencia de la imagen para evitar que se elimine
    canvas.image = fondo
    
    # Inicializamos pygame para la reproducción de sonido del pokemon
    pygame.mixer.init()
    sound_path = objeto.get_grito()  # Ruta del sonido asociado al pokemon
    pokemon_sound = pygame.mixer.Sound(sound_path)  # Cargamos el sonido
    
    
    # Cargamos los GIFs asociados a diferentes tipos de pokemon
    gif_paths = {
        'normal': objeto.get_animacion(),  # Animación normal
        'shiny': objeto.get_shiny(),  # Animación shiny 
        'femenino': objeto.get_animacion_femenino()  # Animación femenina (si existe)
    }

    # Diccionarios para almacenar los fotogramas y las duraciones de los GIFs del pokemon
    frames = {'normal': [], 'shiny': [], 'femenino': []}
    durations = {'normal': [], 'shiny': [], 'femenino': []}
    
    # Función para cargar un GIF específico y separar sus fotogramas
    def cargar_gif(tipo):
        gif_path = gif_paths[tipo]  # Obtiene la ruta del GIF según el tipo
        frames[tipo].clear()  # Limpiamos los fotogramas anteriores
        durations[tipo].clear()  # Limpiamos las duraciones anteriores

        try:
            # Abrimos el GIF
            gif = Image.open(gif_path)
            # Iteramos por todos los fotogramas del GIF
            while True:
                # Convertimos cada fotograma a un formato adecuado
                frame = ImageTk.PhotoImage(gif.copy())
                frames[tipo].append(frame)  # Añadimos el fotograma a la lista
                # Añadimos la duración de cada fotograma
                durations[tipo].append(gif.info.get('duration', 100))
                gif.seek(gif.tell() + 1)  # Avanzamos al siguiente fotograma
        except EOFError:
            pass  # Fin del GIF
        except Exception:
            pass  # Si ocurre otro error, no hacemos nada

    # Llamamos a la función para cargar todos los GIFs (normal, shiny, femenino)
    cargar_gif('normal')
    cargar_gif('shiny')
    cargar_gif('femenino')

    # Crear el espacio para la animación del GIF en el lienzo de canvas
    etiqueta_animacion = canvas.create_image(348, 330)  # Ajusta la posición que es dentro de la pokebola

    # Inicializamos la animación en el tipo 'normal' por defecto
    gif_por_defecto = 'normal'
    animacion_id = None  # Controlador de la animación

    # Función para actualizar los fotogramas de la animación
    def actualizar_frame(indice=0):
        nonlocal animacion_id  # Usamos la variable global animacion_id
        # Actualizamos el fotograma actual
        frame = frames[gif_por_defecto][indice]
        # Actualizamos la imagen en el lienzo
        canvas.itemconfig(etiqueta_animacion, image=frame)

        # Si hay una animación en curso, la cancelamos
        if animacion_id is not None:
            ventana_info.after_cancel(animacion_id)

        # Programamos la actualización del siguiente fotograma
        animacion_id = ventana_info.after(
            durations[gif_por_defecto][indice], actualizar_frame, (indice + 1) % len(frames[gif_por_defecto]))

    # Llamamos a actualizar_frame para mostrar la animación por defecto (normal)
    actualizar_frame(0)

    # Función para cambiar el tipo de GIF (normal, shiny, femenino)
    def cambiar_gif(tipo):
        nonlocal gif_por_defecto  # Usamos la variable global gif_por_defecto
        if gif_por_defecto != tipo:
            gif_por_defecto = tipo  # Actualizamos el tipo de animación
            # Reiniciamos la animación desde el primer fotograma
            actualizar_frame(0)

    # Botones para cambiar entre las animaciones
    boton_mostrar_normal = tk.Button(
        ventana_info, text="Mostrar Normal", command=lambda: cambiar_gif('normal'))
    boton_mostrar_normal.place(x=50, y=500)

    boton_mostrar_shiny = tk.Button(
        ventana_info, text="Mostrar Shiny", command=lambda: cambiar_gif('shiny'))
    boton_mostrar_shiny.place(x=200, y=500)

    # Si existe la animación femenina, agregamos un botón para mostrarla
    if gif_paths['femenino']:
        try:
            # Intentamos abrir el GIF femenino para verificar que existe
            Image.open(gif_paths['femenino'])
            boton_mostrar_femenino = tk.Button(
                ventana_info, text="Mostrar Femenino", command=lambda: cambiar_gif('femenino'))
            boton_mostrar_femenino.place(x=350, y=500)
        except Exception:
            pass  # Si no existe, no mostramos el botón en pantalla.

    # Evento para reproducir sonido al hacer clic sobre la animación
    def play_sound(event):
        # Reducimos el volumen del sonido temporalmente
        pygame.mixer.music.set_volume(0.8)
        pokemon_sound.play()  # Reproducimos el sonido del Pokémon
        # Después de 500 ms, restauramos el volumen origina

    # Etiquetas con la información del objeto (Pokémon)
    # mostrar nombre del pokemon
    etiqueta_nombre = tk.Label(ventana_info,text=nombre, background="#908cac",fg="black",font=("Pokemon Classic",18))
    etiqueta_nombre.place(x= 800,y=115, anchor="center")
    
    # Texto desccrpcion en pantalla
    etiqueta_des = tk.Label(ventana_info,text="Descripcion", background="#908cac",fg="black",font=("Pokemon Classic",14))
    etiqueta_des.place(x= 840,y=275, anchor="center")
    
    # descripcion del pokemon
    etiqueta_descripcion = tk.Text(ventana_info, height=10, width=22, wrap=tk.WORD,font=("Pokemon Classic",8),background="#14131b",fg="white",bd=0, highlightthickness=0)  # Ajusta el tamaño según lo que necesites
    etiqueta_descripcion.place(x= 860,y=420, anchor="center")
    etiqueta_descripcion.insert(tk.END, objeto.get_descripcion())
    etiqueta_descripcion.config(state=tk.DISABLED)
    
    # Tipo de pokemon 
    tipos = objeto.get_tipo()
    tipo = ", ".join(tipos) # convierte en str lo que esta en la lista tipos
    # Mostrando en consola 
    print(tipo)
    # Agregando a la ventana el tipo de pokemon
    etiqueta_tipo = tk.Label(ventana_info,text=f"Tipo: {tipo}", background="Black",fg="White",font=("Pokemon Classic",12))
    etiqueta_tipo.place(x= 680,y=170, anchor="nw")
    
    # Habilidades del pokemon 
    habilidades = objeto.get_habilidad()
    
    hab = ", ".join(habilidades)
    hab = hab.replace(",","\n") # por cada , lo remplaza por \n asi se vea mejor en la interfaz
    print(hab)
    
    # Texto habilidad en la ventana 
    etiqueta_habilidades_texto = tk.Label(ventana_info,text=f"habilidad:",background="#14131b",fg="White",font=("Pokemon Classic",12))
    etiqueta_habilidades_texto.place(x=1080,y=460, anchor="nw")
    
    # Hablilidades propias del pokemon
    etiqueta_habilidades = tk.Label(ventana_info,text=f"{hab}",background="#14131b",fg="White",font=("Pokemon Classic",10),anchor="w", justify="left")
    etiqueta_habilidades.place(x=1080,y=500, anchor="nw")
    
    # Altura y peso 
    etiqueta_altura_peso = tk.Label(ventana_info,text=f"Altura: {objeto.get_altura()} m\nPeso: {objeto.get_peso()} kg",background="#14131b",fg="White",font=("Pokemon Classic",10),anchor="w", justify="left")
    etiqueta_altura_peso.place(x=1080,y=618, anchor="nw")
    
    # Texto de statas en pantalla
    etiqueta_stats_texto= tk.Label(ventana_info,text=f"Stats",background="#908cac",fg="Black",font=("Pokemon Classic",18))
    etiqueta_stats_texto.place(x=1100,y=110, anchor="nw")
    
    # Stats del pokemon
    etuiqueta_stats = tk.Label(ventana_info,text=f"Ps: {objeto.get_ps()}\nAtaque:{objeto.get_ataque()}\nDefensa: {objeto.get_defensa()}\nAtk. Especial: {objeto.get_special_ataque()}\nDef. Especial: {objeto.get_defensa_especial()}\nVelocidad: {objeto.get_velocidad()}",background="#1e1e1e",fg="White",font=("Pokemon Classic",10),anchor="w", justify="left")
    etuiqueta_stats.place(x=1090,y=240, anchor="nw")
    # Aqui anchor="w", justify="left" sirve para  justificar el texto dentro del label
    
    """
    colores usados para la ventana
    
    #14131b gris oscuro mas oscuro

    #18141c gris oscuro
    
    ##1e1e1e gris 
    
    #908cac gris opaco
    """

    # Aqui son las imagenes pequeñas
    if objeto.get_minis_1():
        try:
            # Obtener la ruta de la imagen
            
            ruta = objeto.get_minis_1()
            print(f"Ruta de la imagen: {ruta}")  # Verificar la ruta
            
            # Cargar y redimensionar la imagen con Pillow
            imagen_original = Image.open(ruta).convert("RGBA")  # Asegurar el formato con transparencia
            imagen_redimensionada = imagen_original.resize((100, 100))  # Ajusta el tamaño
            
            # Convertir a formato compatible con Tkinter
            imagen_1 = ImageTk.PhotoImage(imagen_redimensionada)
            # Usaremos en canvas para sobreponer la imagen
            canvas.create_image(655, 610, image=imagen_1, anchor='center')
            # Mantener una referencia de la imagen para evitar que se elimine
            canvas.image = fondo
            
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            
    # Si la mini imagen de su evolucion existe
    if objeto.get_minis_2():
        try:
            # Obtener la ruta de la imagen
            ruta = objeto.get_minis_2()
            print(f"Ruta de la imagen: {ruta}")  # Verificar la ruta
            
            # Cargar y redimensionar la imagen con Pillow
            imagen_original = Image.open(ruta).convert("RGBA")  # Asegurar el formato con transparencia
            imagen_redimensionada = imagen_original.resize((100, 100))  # Ajusta el tamaño
            
            # Convertir a formato compatible con Tkinter
            imagen_2 = ImageTk.PhotoImage(imagen_redimensionada)
            
            # Usamos canvas para sobreponerla en la imagen de fondo
            canvas.create_image(815, 610, image=imagen_2, anchor='center')
            # Mantener una referencia de la imagen para evitar que se elimine
            canvas.image = fondo
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            
    # si la mini imagen de la evolucion existe 
    if objeto.get_minis_3():
        try:
            # Obtener la ruta de la imagen
            ruta = objeto.get_minis_3()
            print(f"Ruta de la imagen: {ruta}")  # Verificar la ruta
            
            # Cargar y redimensionar la imagen con Pillow
            imagen_original = Image.open(ruta).convert("RGBA")  # Asegurar el formato con transparencia
            imagen_redimensionada = imagen_original.resize((100, 100))  # Ajusta el tamaño
            
            # Convertir a formato compatible con Tkinter
            imagen_3 = ImageTk.PhotoImage(imagen_redimensionada)
            
            # Uaremos canvas para sobreponer la imagen con el fondo
            canvas.create_image(970, 610, image=imagen_3, anchor='center')
            # Mantener una referencia de la imagen para evitar que se elimine
            canvas.image = fondo
            
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")


    # reporducir el audio del pokemon a la hora de hacer click en el
    canvas.tag_bind(etiqueta_animacion, "<Button-1>", play_sound)
    
    # Llamar a la función mostrando la ventana
    ventana_info.mainloop()
# /////////////////////////////////////////////////////////////////////////////


"//////////////////////////////////////////////////////////////////////////////////"
"""
Busqueda por generacion/region
cabe a aclarar que tiene una estructura similiar al aterior
"""
def mostrar_generacion():
    
    # Función que elimina todos los widgets en la ventana
    limpiar_contenido()
    
    # Inicializar los objetos una vez se ejecute la pokedex
    # Asegúrate de que la ruta sea correcta
    fondo_imagen = Image.open("fondos\\Pantalla.png")
    # Redimensionar la imagen de fondo para que se ajuste al tamaño de la ventana
    fondo_imagen_redimensionada = fondo_imagen.resize((ventana.winfo_width(), ventana.winfo_height()))  
    # Variable que tendra la imagen.
    fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen_redimensionada)

    # Crear el label para la imagen de fondo y colocarla en el fondo
    global label_fondo
    label_fondo = tk.Label(contenido_frame, image=fondo_imagen_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo_imagen_tk  # Mantener la referencia de la imagen
    
    # datos de las generaciones 
    # se usara para la cajita desplegable de opciones o combobox
    generaciones_pokemon = [
    "Primera Generación",
    "Segunda Generación",
    "Tercera Generación",
    "Cuarta Generación",
    "Quinta Generación",
    "Sexta Generación",
    "Séptima Generación",
    "Octava Generación",
    "Novena Generación"
]
    # NOTA:
    # si una variable se pone (global var) significa que se usara tanto fuera como dentro de cualquier lugar
    # del codigo con fines de modificar/ actualizar su contenido
    # se les agrego var_gen para identificar

    # Entrada para buscar Pokémon
    global entrada_busqueda_gen
    entrada_busqueda_gen = tk.Entry(contenido_frame,width=24,font=("Pokemon Classic", 9))
    entrada_busqueda_gen.place(x=1060, y=45, anchor="center")

    # Combobox para la busqueda por tipo
    global combobox_gen
    combobox_gen= Combobox(contenido_frame, values=generaciones_pokemon, state="readonly",font=("Pokemon Classic", 9))
    combobox_gen.set("Busqueda por generacion")  # Texto inicial
    combobox_gen.place(x=375, y=50, anchor="center")

    # Listbox para mostrar los Pokémon encontrados (es la lista que aparece x pokemon de n tipo)
    # variable global su uso es que se modifica su contenido
    global lista_gen
    lista_gen= tk.Listbox(contenido_frame, background="black", fg="white", font=("Pokemon Classic", 15))
    lista_gen.place_forget() # se agrega pero queda sin uso para su aparicion si se seleciona un tipo(mas adelante se vera)
    
    # un scrollbar para visualizar los pokemons (esta va con la listbox)
    global scrollbar_gen
    scrollbar_gen= tk.Scrollbar(contenido_frame)
    scrollbar_gen.place_forget() # se agrega pero queda sin uso para su aparicion si se seleciona un tipo(mas adelante se vera)
    
    # Vincular el Listbox con el Scrollbar
    lista_gen.config(yscrollcommand=scrollbar_gen.set)
    scrollbar_gen.config(command=lista_gen.yview)
    
    # Label para ver la vista previa del pokemon
    global imagen_pokemon_gen 
    imagen_pokemon_gen = tk.Label(contenido_frame, background="black")
    imagen_pokemon_gen.place(x=980, y=380, anchor="center")
    
    # Botón de búsqueda con imagen 
    imagen = Image.open("fondos\\lupa.png")# ruta de imagen 
    imagen_redimensionada = imagen.resize((41, 19))# Redimensionar la imagen
    # Convertir la imagen redimensionada en un formato que Tkinter pueda usar
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
    
    # Crear un botón con la imagen                                        # ojito comando buscar 
    boton_buscar = tk.Button(contenido_frame,image=imagen_tk, compound="left",command=buscar_gen,width=41,height=19)
    boton_buscar.place(x=1250, y=45, anchor="center")
    # Es importante mantener una referencia de la imagen
    boton_buscar.image = imagen_tk # Esto mantiene la imagen en memoria
    
    """Eventos en busqueda"""
    # Vincular el evento de cambio de selección en el Combobox con la función de actualizar_lista
    combobox_gen.bind("<<ComboboxSelected>>",actualizar_lista_gen)

    # Vincular el evento de selección del Listbox para mostrar el nombre en el buscador e imagen previa
    lista_gen.bind("<<ListboxSelect>>",selecion_tipo_gen)


def actualizar_lista_gen(event):
    
    """
    Esta funcion al ser llamada hace que en la list box segun la generacion seleiconada 
    aparecede pokemon selecionado en la listbox apareceran a elecion los pokemons de ese tipo
    """

    # Limpiar el Listbox antes de insertar los nuevos pokemon por su tipo
    lista_gen.delete(0, tk.END)
    
    # lista que es la que se usa para el combobox ojito se usa para verificar lo selecionado
    generaciones_pokemon = [
    "Primera Generación",
    "Segunda Generación",
    "Tercera Generación",
    "Cuarta Generación",
    "Quinta Generación",
    "Sexta Generación",
    "Séptima Generación",
    "Octava Generación",
    "Novena Generación"
]
    # Obtener el la generacion seleccionada
    tipo_seleccionado = combobox_gen.get()

    # Se imprime la sleccion en la terminal
    # Verifica que se recibe correctamente la generacion
    print(f"Tipo seleccionado: {tipo_seleccionado}")
    
    # Estas son condicionales dependiendo la elecion de generacion/region
    # cabe aclarar que estas  variables de gen_1 a gen_2
    # fueron importadas al inicio del archivo listas_pokemon.py 
    # from listas_pokemons import *
    
    # si la selecion es generacion 1 en el combobox insertara a todos los pokemons de la primera gen
    if tipo_seleccionado == generaciones_pokemon[0]:
        for i in gen_1: # revisar el archivo que les dije
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox ya que se habia dejado para mientras 
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda, igual solo estaba para mientras 
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
        
    if tipo_seleccionado == generaciones_pokemon[1]:
        # RECORDAR ESTE gen_2 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_2:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda por tipo
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    if tipo_seleccionado == generaciones_pokemon[2]:
        # RECORDAR ESTE gen_3 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_3:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    if tipo_seleccionado == generaciones_pokemon[3]:
        # RECORDAR ESTE gen_4 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_4:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda 
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    if tipo_seleccionado == generaciones_pokemon[4]:
        # RECORDAR ESTE gen_5 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_5:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda 
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    
    if tipo_seleccionado == generaciones_pokemon[5]:
        # RECORDAR ESTE gen_2 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_6:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda por tipo
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    
    if tipo_seleccionado == generaciones_pokemon[6]:
        # RECORDAR ESTE gen_2 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_7:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda por tipo
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    if tipo_seleccionado == generaciones_pokemon[7]:
        # RECORDAR ESTE gen_2 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_8:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda por tipo
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    if tipo_seleccionado == generaciones_pokemon[8]:
        # RECORDAR ESTE gen_2 es una lista  que esta  en
        # listas_pokemon.py se usa modularidad
        for i in gen_9:
            lista_gen.insert(tk.END,i)
        # Que ahora si aparezca en pantalla la listbox
        lista_gen.place(x=280, y=350, anchor="center",)
                
        # Tambien el scrollbar para la busqueda por tipo
        scrollbar_gen.place(x=520, y=350, anchor="center",height=345)
    
    


""" Para uso principal BUSQUEDA"""
# Encargada de la selección en la listbox
def selecion_tipo_gen(event):
    # Obtener el índice del Pokémon seleccionado en la listbox
    seleccionado = lista_gen.curselection()
    
    # Solo si se ha seleccionado un Pokémon
    if seleccionado:
        # Obtener el nombre del Pokémon seleccionado
        pokemon_seleccionado = lista_gen.get(seleccionado[0])
        
        # Creamos la variable resultado que será un string vacío para obtener el nombre del Pokémon
        resultado = ""
        
        # En la listbox se muestra algo como "25 Pikachu"
        # Nos encargamos de quitar los espacios y los números
        for caracter in pokemon_seleccionado:
            # Concatenamos solo los caracteres que no son dígitos ni espacios
            if not caracter.isdigit() and not caracter.isspace(): 
                resultado += caracter  # Ir concatenando cada letra
                
        print(resultado)  # Imprime el nombre del Pokémon sin números ni espacios
        entrada_busqueda_gen.delete(0, tk.END)  # Limpiar la entrada de búsqueda
        entrada_busqueda_gen.insert(0, resultado)  # Ahora la barra de búsqueda tomará el nombre del Pokémon
    
        # por optimizacion de codigo no se mostrara la imagen como el gif 

""" Para uso principal (boton buscar o enviar)"""
# Función para buscar Pokémon por nombre o número
def buscar_gen():
    # Verifica que no se envíe nada en blanco
    if entrada_busqueda_gen.get() == "":
        messagebox.showerror("Error", "Debe de llenar el campo")  # Muestra un mensaje de error si el campo está vacío
    else:
        try:
            # Intenta convertir la entrada a un número entero (número del Pokémon)
            busqueda = int(entrada_busqueda_gen.get())
            print("Se ha ingresado un número")
            
            # Se permite el número 0 y positivos, se deja el easter egg de MissingNo
            if busqueda >= 0:
                pokemon = obtener_pokemon_numero(busqueda)  # Busca el Pokémon por su número
                
                # Si el objeto existe
                if pokemon:  # Si no existe el Pokémon, 'obtener_pokemon_numero' retornaría None
                    print(pokemon) # creacion del objeto
                    mostrar_generacion()  # Resetea el frame, empieza desde 0
                    mostrar_ventana_gen(pokemon)  # Muestra la ventana con la información del Pokémon
                else:
                    messagebox.showerror("Error", "Pokémon no registrado")  # Muestra un mensaje de error si no se encuentra el Pokémon
            else:
                messagebox.showerror("Error", "Ingrese un número válido")  # Mensaje de error para números negativos

        except:
            # Si no se puede convertir a número, se asume que es un nombre
            busqueda = entrada_busqueda_gen.get()  # Obtiene el texto de búsqueda
            busqueda = busqueda.lower()  # Convierte a minúsculas para hacer la búsqueda insensible a mayúsculas
            
            # Verifica si la búsqueda es texto (letras) o contiene caracteres especiales
            if busqueda.isalpha() or "-" in busqueda or "50" in busqueda:
                print("Se ha ingresado texto")
                pokemon = obtener_pokemon_nombre(busqueda)  # Busca el Pokémon por su nombre
                
                # Verifica si el Pokémon fue encontrado
                if pokemon:
                    print(pokemon)  # Imprime el objeto Pokémon encontrado
                    mostrar_generacion()  # Resetea la la busqeda
                    mostrar_ventana_gen(pokemon)  # Muestra la ventana con la información del Pokémon
                else:
                    messagebox.showerror("Error", "Pokémon no registrado")  # Mensaje de error si no se encuentra el Pokémon
            else:
                messagebox.showerror("Error", "Ingrese un nombre válido")  # Mensaje de error para entradas no válidas
                
                
def mostrar_ventana_gen(objeto):
    # Obtener el nombre del Pokémon para usarlo como título en la ventana
    nombre = objeto.get_nombre()
    nombre = nombre.capitalize()  # Capitaliza la primera letra del nombre
    
    # Crear la ventana secundaria
    ventana_info = tk.Toplevel(ventana)  # 'ventana' es la ventana principal
    ventana_info.title(nombre)  # Establece el título de la nueva ventana con el nombre del Pokémon
    
    # Definir un tamaño fijo para la ventana
    ventana_info.geometry("1362x695")  # Establece el tamaño de la ventana
    ventana_info.resizable(False, False)  # Bloquea la opción de redimensionar la ventana
    
    """
    Crear el fondo con lienzo
    """
    # Crear el lienzo (Canvas)
    canvas = tk.Canvas(ventana_info, width=1362, height=695)
    canvas.pack(fill="both", expand=True)  # Permite que el lienzo se expanda para llenar la ventana
    
    # Ruta de la imagen de fondo
    fondo_path = "Pantalla3.png"
    imagen_fondo = Image.open(fondo_path)  # Abre la imagen de fondo
    
    # Redimensionar la imagen del fondo según el tamaño de la ventana
    imagen_fondo_resized = imagen_fondo.resize((1362, 695))
    fondo = ImageTk.PhotoImage(imagen_fondo_resized)  # Convierte la imagen redimensionada a un formato que Tkinter puede usar
    
    # Mostrar la imagen de fondo en el lienzo (canvas)
    canvas.create_image(2, 2, image=fondo, anchor="nw")  # Coloca la imagen en la esquina superior izquierda
    canvas.image = fondo  # Mantiene una referencia a la imagen para evitar que se elimine de la memoria
    
    """
    Recibir la imagen del Pokémon para usarla en el lienzo canvas
    """
    # Obtener la URL de la imagen del Pokémon
    imagen_pokemon_url = objeto.get_imagen()
    print(imagen_pokemon_url)  # Imprime la URL en la terminal para verificar que se obtiene correctamente
    
    # Intentar descargar la imagen del Pokémon
    try:
        response = requests.get(imagen_pokemon_url)  # Realiza una solicitud GET a la URL de la imagen
        if response.status_code == 200:  # Verifica que la solicitud fue exitosa
            imagen_datos = Image.open(BytesIO(response.content))  # Abre la imagen desde los datos descargados
            imagen_1 = ImageTk.PhotoImage(imagen_datos)  # Convierte la imagen a un formato que Tkinter puede usar

            # Mostrar la imagen del Pokémon en el lienzo (canvas)
            canvas.create_image(348, 330, image=imagen_1, anchor='center')  # Coloca la imagen en el lienzo
            canvas.image = imagen_1  # Mantiene una referencia a la imagen para evitar que se elimine de la memoria
        else:
            # En caso de que no se pueda cargar la imagen
            print(f"Error al cargar la imagen del Pokémon. Código de estado: {response.status_code}")
    except Exception as e:
        # En caso de que no se pudo descargar la imagen
        print(f"Error al intentar descargar la imagen: {e}")
        
    """
    Etiquetas con la información del objeto (Pokémon)
    """
    
    # Mostrar el nombre del Pokémon en pantalla
    etiqueta_nombre = tk.Label(ventana_info, text=nombre, background="#908cac", fg="black", font=("Pokemon Classic", 18))
    etiqueta_nombre.place(x=800, y=115, anchor="center")  # Coloca la etiqueta en la ventana
    
    # Texto de descripción
    etiqueta_des = tk.Label(ventana_info, text="Descripción", background="#908cac", fg="black", font=("Pokemon Classic", 14))
    etiqueta_des.place(x=840, y=275, anchor="center")  # Coloca la etiqueta de descripción
    
    # Mostrar en pantalla la descripción del Pokémon
    etiqueta_descripcion = tk.Text(ventana_info, height=10, width=22, wrap=tk.WORD, font=("Pokemon Classic", 8), background="#14131b", fg="white", bd=0, highlightthickness=0)
    etiqueta_descripcion.place(x=860, y=420, anchor="center")  # Coloca el cuadro de texto en la ventana
    etiqueta_descripcion.insert(tk.END, objeto.get_descripcion())  # Inserta la descripción del pokemon
    etiqueta_descripcion.config(state=tk.DISABLED)  # Desactiva la edición del texto para que no se pueda modificar
    
    # Obtener y mostrar los tipos del Pokémon
    tipos = objeto.get_tipo()  # Obtiene los tipos del Pokémon(una lista)
    tipo = ", ".join(tipos)  # Une los tipos en una cadena separada por comas
    etiqueta_tipo = tk.Label(ventana_info, text=f"Tipo: {tipo}", background="Black", fg="White", font=("Pokemon Classic", 12))
    etiqueta_tipo.place(x=680, y=170, anchor="nw")  # Coloca la etiqueta de tipos en la ventana
    
    # Obtener y mostrar las habilidades del Pokémon
    habilidades = objeto.get_habilidad()  # Obtiene las habilidades del Pokémon(una lista)
    hab = ", ".join(habilidades).replace(",", "\n")  # Une las habilidades y reemplaza comas por saltos de línea
    etiqueta_habilidades_texto = tk.Label(ventana_info, text=f"Habilidad:", background="#14131b", fg="White", font=("Pokemon Classic", 12))
    etiqueta_habilidades_texto.place(x=1080, y=460, anchor="nw")  # Coloca la etiqueta de habilidades en la ventana
    
    etiqueta_habilidades = tk.Label(ventana_info, text=f"{hab}", background="#14131b", fg="White", font=("Pokemon Classic", 10), anchor="w", justify="left")
    etiqueta_habilidades.place(x=1080, y=500, anchor="nw")  # Coloca la lista de habilidades en la ventana
    
    # Mostrar altura y peso del Pokémon
    etiqueta_altura_peso = tk.Label(ventana_info, text=f"Altura: {objeto.get_altura()} m\nPeso: {objeto.get_peso()} kg", background="#14131b", fg="White", font=("Pokemon Classic", 10), anchor="w", justify="left")
    etiqueta_altura_peso.place(x=1080, y=618, anchor="nw")  # Coloca la etiqueta de altura y peso en la ventana
    
    # Título para la sección de estadísticas
    etiqueta_stats_texto = tk.Label(ventana_info, text=f"Stats", background="#908cac", fg="Black", font=("Pokemon Classic", 18))
    etiqueta_stats_texto.place(x=1100, y=110, anchor="nw")  # Coloca el título de estadísticas en la ventana
    
    # Mostrar las estadísticas del Pokémon
    etuiqueta_stats = tk.Label(ventana_info, text=f"Ps: {objeto.get_ps()}\nAtaque: {objeto.get_ataque()}\nDefensa: {objeto.get_defensa()}\nAtk. Especial: {objeto.get_special_ataque()}\nDef. Especial: {objeto.get_defensa_especial()}\nVelocidad: {objeto.get_velocidad()}", background="#1e1e1e", fg="White", font=("Pokemon Classic", 10), anchor="w", justify="left")
    etuiqueta_stats.place(x=1090, y=240, anchor="nw")  # Coloca la etiqueta de estadísticas en la ventana
    
    # Llamar a la función mostrando la ventana
    ventana_info.mainloop()

"""
Limpiar el contenido del frame contenido_frame

este si o si dentro de la ventana principal debe de ejecutarse 
para no tener problemas de sobreponerse widgets
"""

# Función para limpiar el contenido del frame
def limpiar_contenido():
    for widget in contenido_frame.winfo_children():
        widget.destroy()


"""
Configuracion de la ventana
"""

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Pokedex-Primera generacion")
ventana.geometry("1362x695")
ventana.state("zoomed")

# Menú principal
menu = tk.Menu(ventana)
ventana.config(menu=menu)
ventana.resizable(False, False) # Bloquea el minimizar pantallla.


# Menú de opciones
menu_opciones = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Opciones", menu=menu_opciones)

# Opciones del menú
menu_opciones.add_command(label="Primera-gen", command=mostrar_busqueda)
menu_opciones.add_command(label="regiones/generaciones", command=mostrar_generacion)

# Frame para mostrar el contenido de cada sección
contenido_frame = tk.Frame(ventana)
contenido_frame.pack(fill="both", expand=True)

# Mostrar la página de búsqueda al inicio por defecto
ventana.after(100, mostrar_busqueda)

# Ejecuta la aplicación
ventana.mainloop()