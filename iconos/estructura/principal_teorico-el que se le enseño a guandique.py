import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
from PIL import Image, ImageTk
from funciones_objetos import Funciones, Pokemon
import pygame


pygame.mixer.init()
music_path = "sounds\\songs\\Pokémon_Center.mp3"  # Ruta de la musica a reproducirse durante el programa
pygame.mixer.music.load(music_path)  # Carga del archivo o reproducion
pygame.mixer.music.play(-1)  # Reproducir en bucle indefinidamente
original_volume = 0.1  # Volumen original de la música
pygame.mixer.music.set_volume(0)

"""
Este es para que funcione la musica mientras se ejecuta la pokedex
"""


"""
1-ESTRUCTURA DE LA PRINCIPAL ESTA ES LA PRINCPAL :
esta funcion mostrar_busqueda es la principal donde se buscaran los pokemons 

Funcionamiento: nota busca el codigo mientras lees.
ejemplo:

funcion_ejemplo()
explicacion esto aqui etc

"""

def mostrar_busqueda():

    # Función que elimina todos los widgets en la ventana
    limpiar_contenido()
    
    """
    llama primeramente la funcion limpiar_contenido esta se encarga que cada vez que 
    iniciemos en un apartado borrara todo lo que contenga la ventana asi no se sobreponen los 
    widgets
    """
    
    Pokemon.inicializar_objetos()
    Funciones.actualizar_dic()
    """
    ----Pokemon.inicializar_objetos()
    proveniente de la importacion from funciones_objetos import Funciones, Pokemon
    
    este viene 2 importaciones instancias_pokemon.py(originario)
    por modularidad en el archivo (funciones_objetos.py) se usa todo el contenido
    
    Este funciona para instanciar los objetos cada vez que se entra al apartado de busqueda
    esto es asi ya que a la hora de agregar pokemon vuelve a instanciar los objetos de nuevo
    si quieres saber como funciona internamente puedes ir al archivo (instancias_pokemon.py)
    para comprender el funcionamiento de instancias
    
    ----Funciones.actualizar_dic()
    proveniente de from funciones_objetos import Funciones, Pokemon
    
    Este llama la case Funcion que se encarga de obtencion de iformacion de los pokemons(objetos)
    tambien almacena un dicionario de objetos el cual debe de actualizarse el motivo de ello(si se agrega un
    pokemon los objetos seran todos menos el nuevo por lo que al inicializar otra vez los pokemons toma el nuevo
    a su vez el dic tomara sus contenidos de la instancia anterior no la nueva pero con llamar Funciones.actualizar_dic()
    tomara la nueva isntancias incluyendo como objeto el nuevo pokemon agregado)
    
    """
    
    
    """etuiquetas y entradas a mostrarse en la ventana"""    
    # Etiqueta de la página de búsqueda
    label_busqueda = tk.Label(contenido_frame, text="Página Principal: Búsqueda de Pokémon", font=("Arial", 14))
    label_busqueda.pack(pady=10)
    
    # Opciones de los tipos de Pokémon de la primera generación
    # se usara para la cajita desplegable de opciones o combobox
    opciones = [
        "normal", "fighting", "flying", "poison", "ground",
        "rock", "bug", "ghost", "fire", "water",
        "grass", "electric", "psychic", "ice", "dragon"
    ]
    
    # NOTA:
    # si una variable se pone (global var) significa que se usara tanto fuera como dentro de cualquier lugar
    # del codigo con fines de modificar/ actualizar su contenido 

    # Entrada para buscar Pokémon
    global entrada_busqueda
    entrada_busqueda = tk.Entry(contenido_frame)
    entrada_busqueda.pack()
    
    # Botón de búsqueda
    boton_buscar = tk.Button(contenido_frame, text="Buscar", command=buscar)
    boton_buscar.pack()
    
    # Combobox para seleccionar el tipo de Pokémon
    global combobox
    combobox = Combobox(contenido_frame, values=opciones, state="readonly")
    combobox.set("Selecciona un tipo")
    combobox.pack()
    
    # Listbox para mostrar los Pokémon encontrados
    # variable global su uso es que se modifica su contenido
    global lista
    lista = tk.Listbox(contenido_frame)
    lista.pack()
    
    global imagen_pokemon
    imagen_pokemon = tk.Label(contenido_frame)
    imagen_pokemon.pack()
    
    """Eventos en busqueda"""
    # Vincular el evento de cambio de selección en el Combobox con la función de actualización
    combobox.bind("<<ComboboxSelected>>", actualizar_lista)
    """
    lo que hace es simple si se elije un tipo de pokemon entonces en la listbox 
    o mejor dicho donde apareceran los pokemons por tipo apareceran esos pokemons
    
    """
    
    # Vincular el evento de selección del Listbox para mostrar los detalles del Pokémon
    lista.bind("<<ListboxSelect>>", selecion_tipo)
    """
    lo que hace es que por la selecion de un pokemon por tipo en la listbox
    ese pokemon selecionado aparezca en la barra de busqueda
    """
    """
    FUNCION EXPERIMENTAL NOSE SI LLEGARA AL FINAL
    si seleciona ese pokemon se muestra su imagen
    """

""" PARA USO PRICIPAL DE BUSQUEDA"""

# Función para actualizar la lista de Pokémon en base al tipo seleccionado
def actualizar_lista(event):
    
    """
    Esta funcion al ser llamada hace que en la list box segun el tipo de pokemon selecionado 
    en la combobox apareceran a elecion los pokemons de ese tipo
    """
    
    # Limpiar el Listbox antes de insertar los nuevos pokemon por su tipo
    lista.delete(0, tk.END)
    
    # Obtener el tipo seleccionado
    tipo_seleccionado = combobox.get()
    
    # SE MUESTRA EN LA TERMINAL
    print(f"Tipo seleccionado: {tipo_seleccionado}")  # Verifica que se recibe correctamente el tipo
    

    # Verifica que la función de búsqueda retorne una lista
    pokemon_tipo = Funciones.buscar_pokemon_tipo(str(tipo_seleccionado))
    """
    Al usar Funciones.buscar_pokemon_tipo(str(tipo_seleccionado)) retororna una lista con los nombres 
    de los pokemons segun su lista 
    """
    if pokemon_tipo:  # Si la lista no está vacía(imposible que no este vacia) pero ahi va el condicional
        # Insertar los nombres de los Pokémon en el Listbox
        for pokemon in pokemon_tipo:
            lista.insert(tk.END, pokemon)
        
""" Para uso principal BUSQUEDA"""
def selecion_tipo(event):
    
    """
    Esta funcion se encarga de que el pokemon selecionado en la listbox o mejor
    dicho despues de haber buscado un pokemon por su tipo y selecionarlo 
    ese nombre de pokemon aparezca en la barra de busqueda
    """
    
    # Obtener el índice del Pokémon seleccionado
    seleccionado = lista.curselection()    
    
    if seleccionado:
        
        # Obtener el nombre del Pokémon
        pokemon_seleccionado = lista.get(seleccionado[0])
        
        "asi buscamos in que nos joda ese apartado "
        resultado = ""
        for caracter in pokemon_seleccionado:
            if not caracter.isdigit() and not caracter.isspace(): # Verifica si el carácter es una letra
                resultado += caracter

        
        pokemon = Funciones.buscar_pokemon_nombre(resultado)
        
        entrada_busqueda.delete(0, tk.END)  # Limpiar la entrada de búsqueda
        entrada_busqueda.insert(0, resultado) # ahora tomara el nombre del pokemon
        
        """
        Opcional 
        ver imagen de pokemon antes de buscar dicha informacion
        """
        try:
            # Obtener la ruta del gif del Pokémon
            gif_ruta = pokemon.get_animacion()  # Asumiendo que este método devuelve la ruta del gif
            
            # Cargar el gif usando Pillow
            gif_imagen = Image.open(gif_ruta)
            gif_imagen = ImageTk.PhotoImage(gif_imagen)

            # Mostrar el gif en el label
            imagen_pokemon.config(image=gif_imagen)
            imagen_pokemon.image = gif_imagen  # Mantener una referencia al gif para evitar que se destruya
        except Exception as e:
            imagen_pokemon.config(text="No se pudo cargar la animación.")
            print(f"Error al cargar la animación: {e}")
        
        
""" Para uso principal (boton buscar o enviar)"""
# Función para buscar Pokémon por nombre o número
def buscar():
    
    """
    VALIDACIONES PERFECTAS
    """

    # Verifica que no se envie nada en blanco
    if entrada_busqueda.get() == "":
        messagebox.showerror("Error","Debe de llenar el campo")
    else:
        try:
            # intenta convertir a numero entero (numero pokemon) si es posible seguira
            busqueda = int(entrada_busqueda.get())
            print("Se ha ingresado un numero")
            # se lo dejo si queremos dejar el easter egg de missingno
            if busqueda >=0:
                pokemon = Funciones.buscar_pokemon_numero(busqueda)
                # hace aparecer la ventana con la informacion
                # si el objeto existe 
                if pokemon: # si no existe el pokemon 200 retornaria falso 
                    mostrar_ventana(pokemon)
                else:
                    messagebox.showerror("Error","Pokemon no registrado")
                # si se ha ingresado un numero negativo
            else:
                messagebox.showerror("Error","Ingrese un numero valido")
        
        except:
            # si no es numero lo que se envia 
            # es un nombre 
            busqueda = entrada_busqueda.get()
            busqueda.strip()
            
            # si el la busqueda es texto letras intentara buscar el pokemon
            if busqueda.isalpha():
                print("se ha ingresado texto")
                pokemon = Funciones.buscar_pokemon_nombre(busqueda)
                
                # el mismo caso si es verdad lo hara sino retorna none
                if pokemon:
                    # dar paso a la ejecucuion de la ventana con informacion
                    mostrar_ventana(pokemon)
                else:
                    messagebox.showerror("Error","Pokemon no registrado")
                # si en la busquda lo ingresado es diferente de letras
            else:
                messagebox.showerror("Error","Ingrese un nombre valido")
        
        
    """if pokemon:
        mostrar_ventana(pokemon)
    else:
        messagebox.showerror("Error","Pokemon no se ha registrado")
        """
#/////////////////////////////////////////////////////////////////////////////        

"""VENTANA PARA MOSTRAR POKEMON"""
def mostrar_ventana(objeto):
    
    # Creamos una nueva ventana hija
    ventana_info = tk.Toplevel(ventana)  # 'ventana' es la ventana principal
    ventana_info.title("Ventana de Información")  # Título de la nueva ventana
    ventana_info.geometry("1280x720")  # Definimos un tamaño fijo para la ventana
    ventana_info.state("zoomed")  # Maximiza la ventana

    # Inicializamos pygame para la reproducción de sonidos
    pygame.mixer.init()
    sound_path = objeto.get_grito()  # Ruta del sonido asociado al objeto
    pokemon_sound = pygame.mixer.Sound(sound_path)  # Cargamos el sonido

    # Cargamos los GIFs asociados a diferentes tipos del objeto
    gif_paths = {
        'normal': objeto.get_animacion(),  # Animación estándar
        'shiny': objeto.get_shiny(),  # Animación shiny (si existe)
        'femenino': objeto.get_animacion_femenino()  # Animación femenina (si existe)
    }

    # Diccionarios para almacenar los fotogramas y las duraciones de los GIFs
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
                frame = ImageTk.PhotoImage(gif.copy())  # Convertimos cada fotograma a un formato adecuado
                frames[tipo].append(frame)  # Añadimos el fotograma a la lista
                durations[tipo].append(gif.info.get('duration', 100))  # Añadimos la duración de cada fotograma
                gif.seek(gif.tell() + 1)  # Avanzamos al siguiente fotograma
        except EOFError:
            pass  # Fin del GIF
        except Exception:
            pass  # Si ocurre otro error, no hacemos nada

    # Llamamos a la función para cargar todos los GIFs (normal, shiny, femenino)
    cargar_gif('normal')
    cargar_gif('shiny')
    cargar_gif('femenino')

    # Función para mostrar la información del objeto en la ventana secundaria
    def mostrar_informacion():
        # Etiquetas con la información del objeto (Pokémon)
        etiquetas_info = [
            f"Nombre: {objeto.get_nombre()}",
            f"Descripción: {objeto.get_descripcion()}",
            f"Tipo 1: {objeto.get_tipo()[0]}",
            f"Tipo 2: {objeto.get_tipo()[1] if len(objeto.get_tipo()) > 1 else 'N/A'}",
            f"Peso: {objeto.get_peso()} kg",
            f"Altura: {objeto.get_altura()} m",
            f"Habilidad: {objeto.get_habilidad()}",
            f"PS: {objeto.get_ps()}",
            f"Ataque: {objeto.get_ataque()}",
            f"Defensa: {objeto.get_defensa()}",
            f"Ataque Especial: {objeto.get_special_ataque()}",
            f"Defensa Especial: {objeto.get_defensa_especial()}",
            f"Mini: {objeto.get_mini()}",
            f"Velocidad: {objeto.get_velocidad()}"
        ]
        # Creamos una etiqueta por cada línea de información y la agregamos a la ventana
        for info in etiquetas_info:
            tk.Label(ventana_info, text=info).pack()
            
    # Mostramos la información del objeto en la ventana 
    mostrar_informacion()

    # Función para reproducir el sonido del Pokémon cuando se hace clic
    def play_sound(event):
        pygame.mixer.music.set_volume(0.2)  # Reducimos el volumen del sonido temporalmente
        pokemon_sound.play()  # Reproducimos el sonido del Pokémon
        # Después de 500 ms, restauramos el volumen original
        ventana_info.after(500, lambda: pygame.mixer.music.set_volume(1.0))

    # Configuramos la etiqueta para mostrar el GIF de la animación
    etiqueta_animacion = tk.Label(ventana_info)
    etiqueta_animacion.pack()

    # Inicializamos la animación en el tipo 'normal'
    current_gif = 'normal'  
    animacion_id = None  # Controlador de la animación

    # Función para actualizar los fotogramas de la animación
    def actualizar_frame(indice=0):
        nonlocal animacion_id  # Usamos la variable global animacion_id

        # Actualizamos el fotograma actual
        frame = frames[current_gif][indice]
        etiqueta_animacion.config(image=frame)  # Actualizamos la imagen en la etiqueta

        # Si hay una animación en curso, la cancelamos
        if animacion_id is not None:
            ventana_info.after_cancel(animacion_id)
        
        # Programamos la actualización del siguiente fotograma
        animacion_id = ventana_info.after(durations[current_gif][indice], actualizar_frame, (indice + 1) % len(frames[current_gif]))

    # Función para cambiar el tipo de GIF (normal, shiny, femenino)
    def cambiar_gif(tipo):
        nonlocal current_gif  # Usamos la variable global current_gif
        if current_gif != tipo:
            current_gif = tipo  # Actualizamos el tipo de animación
            actualizar_frame(0)  # Reiniciamos la animación desde el primer fotograma

    # Botones para cambiar entre las animaciones
    boton_mostrar_normal = tk.Button(ventana_info, text="Mostrar Normal", command=lambda: cambiar_gif('normal'))
    boton_mostrar_normal.pack()

    boton_mostrar_shiny = tk.Button(ventana_info, text="Mostrar Shiny", command=lambda: cambiar_gif('shiny'))
    boton_mostrar_shiny.pack()

    # Si existe la animación femenina, agregamos un botón para mostrarla
    if gif_paths['femenino']:
        try:
            # Intentamos abrir el GIF femenino para verificar que existe
            Image.open(gif_paths['femenino'])
            boton_mostrar_femenino = tk.Button(ventana_info, text="Mostrar Femenino", command=lambda: cambiar_gif('femenino'))
            boton_mostrar_femenino.pack()
        except Exception:
            pass  # Si hay un error (por ejemplo, el GIF no existe), no hacemos nada

    # Reproducimos el sonido al hacer clic en la etiqueta de la animación
    etiqueta_animacion.bind("<Button-1>", play_sound)

    # Iniciamos la animación en el primer fotograma
    actualizar_frame(0)

    # Iniciamos el bucle principal de la ventana secundaria
    ventana_info.mainloop()
#/////////////////////////////////////////////////////////////////////////////

"""
Prototipo
"""
def agregar_pokemon():
    
    """
    EN PROSESO
    """
            
    limpiar_contenido()
    # Etiquetas y campos de entrada para la información del Pokémon
    label_nombre = tk.Label(contenido_frame, text="Nombre del Pokémon:")
    label_nombre.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(contenido_frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    label_descripcion = tk.Label(contenido_frame, text="Descripción:")
    label_descripcion.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_descripcion = tk.Entry(contenido_frame)
    entry_descripcion.grid(row=1, column=1, padx=10, pady=5)

    label_peso = tk.Label(contenido_frame, text="Peso (kg):")
    label_peso.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_peso = tk.Entry(contenido_frame)
    entry_peso.grid(row=2, column=1, padx=10, pady=5)

    label_altura = tk.Label(contenido_frame, text="Altura (cm):")
    label_altura.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_altura = tk.Entry(contenido_frame)
    entry_altura.grid(row=3, column=1, padx=10, pady=5)

    # Habilidades
    label_habilidad1 = tk.Label(contenido_frame, text="Habilidad 1:")
    label_habilidad1.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_habilidad1 = tk.Entry(contenido_frame)
    entry_habilidad1.grid(row=4, column=1, padx=10, pady=5)

    label_habilidad2 = tk.Label(contenido_frame, text="Habilidad 2:")
    label_habilidad2.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_habilidad2 = tk.Entry(contenido_frame)
    entry_habilidad2.grid(row=5, column=1, padx=10, pady=5)

    # Tipo primario
    label_tipo1 = tk.Label(contenido_frame, text="Seleccione el tipo primario:")
    label_tipo1.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    var_tipo_pokemon = tk.IntVar()
    tipos = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon"]

    for idx, tipo in enumerate(tipos):
        tk.Radiobutton(contenido_frame, text=tipo, variable=var_tipo_pokemon, value=idx+1).grid(row=7, column=idx, padx=5, sticky="w")

    # Tipo secundario
    label_tipo2 = tk.Label(contenido_frame, text="Seleccione el tipo secundario (Opcional):")
    label_tipo2.grid(row=8, column=0, padx=10, pady=5, sticky="w")

    var_tipo2_pokemon = tk.IntVar()

    for idx, tipo in enumerate(tipos):
        tk.Radiobutton(contenido_frame, text=tipo, variable=var_tipo2_pokemon, value=idx+1).grid(row=9, column=idx, padx=5, sticky="w")

    # Botón para guardar Pokémon                                         # lamda nos ayuda a llamar una funcion con argumentos
    boton_guardar = tk.Button(contenido_frame, text="Guardar Pokémon",command= lambda: enviar(entry_nombre.get(),entry_descripcion.get(),entry_peso.get(),entry_altura.get(),entry_habilidad1.get(),entry_habilidad2.get(),var_tipo_pokemon.get(),var_tipo2_pokemon.get()))
    boton_guardar.grid(row=20, column=0, columnspan=2, pady=10, padx=10) 


def enviar(nombre,desc,peso,alt,hab1,hab2,tipo1,tipo2):
    """
    Necesita validaciones 
    nota su quieres mejorar la estrcutura andele 
    """
    pass
"""
LIMPIAR CONTENIDO DEL FRAME ES AUTOMATICO POR CADA APARTADO
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
ventana.title("Pokedex")
ventana.geometry("1920x1080")
ventana.state("zoomed")

# Menú principal
menu = tk.Menu(ventana)
ventana.config(menu=menu)

# Menú de opciones
menu_opciones = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Opciones", menu=menu_opciones)

# Opciones del menú
menu_opciones.add_command(label="Página de Búsqueda", command=mostrar_busqueda)
menu_opciones.add_command(label="Cómo Funciona")
menu_opciones.add_command(label="Agregar Pokémon ",command= agregar_pokemon)

# Frame para mostrar el contenido de cada sección
contenido_frame = tk.Frame(ventana)
contenido_frame.pack(fill="both", expand=True)

# Mostrar la página de búsqueda al inicio por defecto
mostrar_busqueda()

# Ejecuta la aplicación
ventana.mainloop()
