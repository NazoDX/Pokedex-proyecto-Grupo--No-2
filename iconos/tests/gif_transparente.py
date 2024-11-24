import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("GIF transparente sobre imagen de fondo")
root.geometry("800x600")  # Tamaño de la ventana

# Cargar la imagen de fondo
background_image = Image.open("estructura\\fondo principal.jpg")
background_image = background_image.resize((800, 600))  # Ajustar el tamaño de la imagen de fondo
background_tk = ImageTk.PhotoImage(background_image)

# Crear un canvas donde se mostrará la imagen de fondo
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Colocar la imagen de fondo en el canvas
canvas.create_image(0, 0, anchor="nw", image=background_tk)

# Cargar el GIF con fondo transparente
gif_image = Image.open("gifs\\25.gif")

# Crear un objeto de imagen Tkinter para manejar la transparencia
gif_frames = []
for frame in range(gif_image.n_frames):
    gif_image.seek(frame)  # Cambiar al frame actual
    frame_image = gif_image.convert("RGBA")  # Asegurarse de que tenga un canal alfa (transparencia)
    gif_frames.append(ImageTk.PhotoImage(frame_image))

# Crear el ID para mostrar el GIF en el canvas
gif_id = canvas.create_image(400, 300, image=gif_frames[0])  # Posición inicial del GIF

# Función para actualizar el GIF y animarlo
def animate_gif(frame=0):
    next_frame = (frame + 1) % len(gif_frames)  # Ciclar entre los frames
    canvas.itemconfig(gif_id, image=gif_frames[next_frame])  # Actualizar el frame del GIF
    root.after(100, animate_gif, next_frame)  # Llamar nuevamente después de 100 ms

# Llamar a la función de animación para comenzar
animate_gif()

# Ejecutar el bucle principal de Tkinter
root.mainloop()
