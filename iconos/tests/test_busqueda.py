import tkinter as tk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import pygame

# Inicialización de la música
pygame.mixer.init()
music_path = "sounds\\songs\\Pokémon_Center.mp3"  # Ruta de la música a reproducirse durante el programa
pygame.mixer.music.load(music_path)  # Carga del archivo o reproducción
pygame.mixer.music.play(-1)  # Reproducir en bucle indefinidamente
pygame.mixer.music.set_volume(0.8)  # Volumen bajo

def limpiar_contenido():
    """Limpia todos los widgets, incluyendo la imagen de fondo."""
    for widget in contenido_frame.winfo_children():
        widget.destroy()

def mostrar_busqueda():
    limpiar_contenido()
    
    # Redimensionar la imagen de fondo para que se ajuste al tamaño de la ventana
    fondo_imagen = Image.open("estructura\\fondo principal.jpg")  # Asegúrate de que la ruta sea correcta
    fondo_imagen_redimensionada = fondo_imagen.resize((ventana.winfo_width(), ventana.winfo_height()))  # Redimensionar al tamaño de la ventana
    fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen_redimensionada)
    
    # Crear el label para la imagen de fondo y colocarla en el fondo
    global label_fondo
    label_fondo = tk.Label(contenido_frame, image=fondo_imagen_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo_imagen_tk  # Mantener la referencia de la imagen
    
    # Cargar el GIF con fondo transparente
    gif_image = Image.open("gifs\\25.gif")
    
    # Crear un objeto de imagen Tkinter para manejar la transparencia
    gif_frames = []
    for frame in range(gif_image.n_frames):
        gif_image.seek(frame)  # Cambiar al frame actual
        frame_image = gif_image.convert("RGBA")  # Asegurarse de que tenga un canal alfa (transparencia)
        gif_frames.append(ImageTk.PhotoImage(frame_image))
    
    # Crear un canvas donde se mostrará la imagen de fondo y el gif
    canvas = tk.Canvas(contenido_frame, width=ventana.winfo_width(), height=ventana.winfo_height())
    canvas.place(x=0, y=0, relwidth=1, relheight=1)  # Ubicación en todo el contenido_frame
    
    # Colocar el fondo en el canvas
    canvas.create_image(0, 0, anchor="nw", image=fondo_imagen_tk)

    # Crear el ID para mostrar el GIF en el canvas
    gif_id = canvas.create_image(400, 300, image=gif_frames[0])  # Posición inicial del GIF

    # Función para actualizar el GIF y animarlo
    def animate_gif(frame=0):
        next_frame = (frame + 1) % len(gif_frames)  # Ciclar entre los frames
        canvas.itemconfig(gif_id, image=gif_frames[next_frame])  # Actualizar el frame del GIF
        ventana.after(100, animate_gif, next_frame)  # Llamar nuevamente después de 100 ms

    # Llamar a la función de animación para comenzar
    animate_gif()

    # Etiqueta de la página de búsqueda
    label_busqueda = tk.Label(contenido_frame, text="Página Principal: Búsqueda de Pokémon", font=("Arial", 14))
    label_busqueda.pack(pady=10)
    
    # Opciones de los tipos de Pokémon
    opciones = [
        "normal", "fighting", "flying", "poison", "ground",
        "rock", "bug", "ghost", "fire", "water",
        "grass", "electric", "psychic", "ice", "dragon"
    ]
    
    # Entrada para buscar Pokémon
    global entrada_busqueda
    entrada_busqueda = tk.Entry(contenido_frame)
    entrada_busqueda.pack()
    
    # Botón de búsqueda
    boton_buscar = tk.Button(contenido_frame, text="Buscar")
    boton_buscar.pack()
    
    # Combobox para seleccionar el tipo de Pokémon
    global combobox
    combobox = Combobox(contenido_frame, values=opciones, state="readonly")
    combobox.set("Selecciona un tipo")
    combobox.pack()

    # Listbox para mostrar los Pokémon encontrados (inicialmente oculto)
    global lista
    lista = tk.Listbox(contenido_frame)
    lista.pack_forget()  # Ocultar el listbox por defecto
    
    # Función para mostrar el Listbox solo si se selecciona un tipo
    def mostrar_lista(event=None):
        if combobox.get() != "Selecciona un tipo":  # Si se seleccionó un tipo
            lista.pack()  # Mostrar el Listbox
        else:
            lista.pack_forget()  # Ocultar el Listbox si no se ha seleccionado un tipo

    # Asociar la función mostrar_lista al evento de selección del combobox
    combobox.bind("<<ComboboxSelected>>", mostrar_lista)

def agregar_pokemon():
    limpiar_contenido()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Pokedex")
ventana.geometry("1920x1080")
ventana.state("zoomed")

menu = tk.Menu(ventana)
ventana.config(menu=menu)

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
ventana.after(100, mostrar_busqueda)  # Usar after para asegurarse de que la ventana está completamente cargada

# Ejecuta la aplicación
ventana.mainloop()
