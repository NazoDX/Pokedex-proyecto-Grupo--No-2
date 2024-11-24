def mostrar_ventana(objeto):
    # Crear la ventana secundaria
    ventana_info = tk.Toplevel(ventana)  # 'ventana' es la ventana principal
    ventana_info.title("Ventana de Información")  # Título de la nueva ventana
    ventana_info.geometry("1280x720")  # Definimos un tamaño fijo para la ventana
    ventana_info.state("zoomed")  # Maximiza la ventana
    ventana_info.config(bg='white')  # Fondo blanco en la ventana secundaria
    
    # Crear el lienzo (Canvas)
   
    # Ruta de la imagen de fondo
    fondo_path = "estructura\\ver.jpg"
    imagen_fondo = Image.open(fondo_path)
    
    width = ventana_info.winfo_width()
    height = ventana_info.winfo_height()
    
    canvas = tk.Canvas(ventana_info, width=width, height=height)
    canvas.pack(fill="both", expand=True)
            
            # Redimensionamos la imagen solo cuando sea necesario
    imagen_fondo_resized = imagen_fondo.resize((1362,695))  # Redimensionar según el tamaño de la ventana
    fondo = ImageTk.PhotoImage(imagen_fondo_resized)
            
            # Mostrar la imagen de fondo en el lienzo
    canvas.create_image(2, 2, image=fondo, anchor = "nw")
            # Mantener una referencia de la imagen para evitar que se elimine
    canvas.image = fondo



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

    # Crear el espacio para la animación del GIF en el lienzo
    etiqueta_animacion = canvas.create_image(345, 330, anchor="center")  # Ajusta la posición según necesites
    etiqueta_animacion.bind("<Button-1>", play_sound)
    # Inicializamos la animación en el tipo 'normal' por defecto
    current_gif = 'normal'  
    animacion_id = None  # Controlador de la animación

    # Función para actualizar los fotogramas de la animación
    def actualizar_frame(indice=0):
        nonlocal animacion_id  # Usamos la variable global animacion_id
        # Actualizamos el fotograma actual
        frame = frames[current_gif][indice]
        canvas.itemconfig(etiqueta_animacion, image=frame)  # Actualizamos la imagen en el lienzo

        # Si hay una animación en curso, la cancelamos
        if animacion_id is not None:
            ventana_info.after_cancel(animacion_id)
        
        # Programamos la actualización del siguiente fotograma
        animacion_id = ventana_info.after(durations[current_gif][indice], actualizar_frame, (indice + 1) % len(frames[current_gif]))

    # Llamamos a actualizar_frame para mostrar la animación por defecto (normal)
    actualizar_frame(0)

    # Función para cambiar el tipo de GIF (normal, shiny, femenino)
    def cambiar_gif(tipo):
        nonlocal current_gif  # Usamos la variable global current_gif
        if current_gif != tipo:
            current_gif = tipo  # Actualizamos el tipo de animación
            actualizar_frame(0)  # Reiniciamos la animación desde el primer fotograma

    # Botones para cambiar entre las animaciones
    boton_mostrar_normal = tk.Button(ventana_info, text="Mostrar Normal", command=lambda: cambiar_gif('normal'))
    boton_mostrar_normal.place(x=50, y=500)

    boton_mostrar_shiny = tk.Button(ventana_info, text="Mostrar Shiny", command=lambda: cambiar_gif('shiny'))
    boton_mostrar_shiny.place(x=200, y=500)

    # Si existe la animación femenina, agregamos un botón para mostrarla
    if gif_paths['femenino']:
        try:
            # Intentamos abrir el GIF femenino para verificar que existe
            Image.open(gif_paths['femenino'])
            boton_mostrar_femenino = tk.Button(ventana_info, text="Mostrar Femenino", command=lambda: cambiar_gif('femenino'))
            boton_mostrar_femenino.place(x=350, y=500)
        except Exception:
            pass  # Si no existe, no mostramos el botón

    # Evento para reproducir sonido al hacer clic sobre la animación
    def play_sound(event):
        pygame.mixer.music.set_volume(0.2)  # Reducimos el volumen del sonido temporalmente
        pokemon_sound.play()  # Reproducimos el sonido del Pokémon
        # Después de 500 ms, restauramos el volumen original
        ventana_info.after(500, lambda: pygame.mixer.music.set_volume(1.0))


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

    # Crear las etiquetas de información sobre el objeto
    for i, info in enumerate(etiquetas_info):
        tk.Label(ventana_info, text=info).place(x=50, y=50 + (i * 30))

    # Llamar a la función mostrando la ventana
    ventana_info.mainloop()
    
def mostrar_ventana(objeto):
    
    # Creamos una nueva ventana hija
    ventana_info = tk.Toplevel(ventana)  # 'ventana' es la ventana principal
    ventana_info.title("Ventana de Información")  # Título de la nueva ventana
    ventana_info.geometry("1280x720")  # Definimos un tamaño fijo para la ventana
    ventana_info.state("zoomed")  # Maximiza la ventana
    
    # intenta poner la imagen de fondo 
    try:
        # Ruta de la imagen de fondo
        fondo_path = "estructura\\ver.jpg"  
        imagen_fondo = Image.open(fondo_path)
        
        # Crear un Label para la imagen de fondo
        label_fondo = tk.Label(ventana_info)
        label_fondo.place(relwidth=1, relheight=1)  # Hace que ocupe toda la ventana
        
        # Inicializamos el fondo con la imagen redimensionada
        def ajustar_fondo(event=None):
            width = ventana_info.winfo_width()
            height = ventana_info.winfo_height()
            
            # Redimensionamos la imagen solo cuando sea necesario
            imagen_fondo_resized = imagen_fondo.resize((width, height))  # Redimensionar según el tamaño de la ventana
            fondo = ImageTk.PhotoImage(imagen_fondo_resized)
            
            # Actualizar el fondo
            label_fondo.config(image=fondo)
            label_fondo.image = fondo  # Mantener la referencia de la imagen
            
        # Llamar a ajustar_fondo cuando cambia el tamaño de la ventana
        ventana_info.bind("<Configure>", ajustar_fondo)
        
        # Iniciar la ventana y ajustar el fondo solo cuando sea necesario
        ventana_info.after(100, ajustar_fondo)  # Asegurar que se ajuste al principio
        
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        
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