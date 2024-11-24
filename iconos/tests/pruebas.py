import tkinter as tk  # Importa tkinter para la interfaz gráfica
from PIL import Image, ImageTk  # Importa PIL para manejar el GIF

def mostrar_gif():
    """
    Esta función actualiza el fotograma del GIF animado en un bucle.
    """
    global frame_index  # Índice del fotograma actual
    frame = frames[frame_index]  # Selecciona el fotograma actual
    etiqueta_gif.config(image=frame)  # Actualiza la imagen en la etiqueta

    # Avanza al siguiente fotograma, reiniciando si llega al final de la animación
    frame_index = (frame_index + 1) % len(frames)
    
    # Programa la actualización del próximo fotograma
    ventana.after(durations[frame_index], mostrar_gif)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("GIF Animado")  # Título de la ventana
ventana.geometry("500x500")  # Tamaño de la ventana

# Cargar el GIF animado y sus fotogramas
gif_path = "1.png"  # Ruta del archivo GIF animado
gif = Image.open(gif_path)  # Abre el archivo GIF

# Extraer los fotogramas y duraciones del GIF
frames = []
durations = []
try:
    while True:
        # Convierte el fotograma actual para que sea compatible con tkinter y lo almacena en frames
        frame = ImageTk.PhotoImage(gif.copy())
        frames.append(frame)
        
        # Obtiene la duración del fotograma actual (en milisegundos)
        durations.append(gif.info.get('duration', 100))
        
        # Avanza al siguiente fotograma del GIF
        gif.seek(gif.tell() + 1)
except EOFError:
    pass  # Termina cuando alcanza el último fotograma

# Configura el índice inicial del fotograma
frame_index = 0

# Crear una etiqueta para mostrar el GIF animado
etiqueta_gif = tk.Label(ventana)
etiqueta_gif.pack(expand=True)  # Centra la etiqueta en la ventana

# Inicia la animación del GIF
mostrar_gif()

# Ejecuta la ventana principal
ventana.mainloop()
