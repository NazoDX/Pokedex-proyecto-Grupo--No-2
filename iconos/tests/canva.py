import tkinter as tk
from PIL import Image, ImageTk

def ajustar_imagen(event=None):
    """Redimensiona la imagen al tamaño de la ventana manteniendo el aspecto 16:9."""
    canvas_width = ventana.winfo_width()
    canvas_height = ventana.winfo_height()

    # Calcula el nuevo tamaño de la imagen manteniendo la relación 16:9
    if canvas_width / canvas_height > 16 / 9:
        # La ventana es más ancha, ajustar por altura
        new_height = canvas_height
        new_width = int(new_height * 16 / 9)
    else:
        # La ventana es más alta, ajustar por ancho
        new_width = canvas_width
        new_height = int(new_width * 9 / 16)

    # Redimensionar la imagen
    imagen_resized = imagen_original.resize((new_width, new_height), Image.ANTIALIAS)
    imagen_tk = ImageTk.PhotoImage(imagen_resized)

    # Actualizar la imagen en el canvas
    canvas.itemconfig(canvas_imagen, image=imagen_tk)
    canvas.image = imagen_tk  # Mantener referencia a la imagen para evitar que se recolecte por el GC

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1280x720")
ventana.title("Imagen centrada 16:9")

# Crear canvas para mostrar la imagen
canvas = tk.Canvas(ventana, bg="black")
canvas.pack(fill="both", expand=True)

# Cargar la imagen original
ruta_imagen = "1.png"  # Cambia a la ruta de tu imagen
imagen_original = Image.open(ruta_imagen)

# Redimensionar la imagen inicial para ajustarla a la ventana
imagen_resized = imagen_original.resize((ventana.winfo_width(), ventana.winfo_height()))
imagen_tk = ImageTk.PhotoImage(imagen_resized)

# Ejemplo de ubicación y anclaje de la imagen:
# Cambiar (ventana.winfo_width() // 2, ventana.winfo_height() // 2) por las coordenadas deseadas
canvas_imagen = canvas.create_image(ventana.winfo_width() // 2, ventana.winfo_height() // 2, 
                                    image=imagen_tk, anchor="center")

# Cambiar a otro anclaje si deseas que la imagen esté en otra posición:
# - "nw" (noroeste): esquina superior izquierda
# - "ne" (noreste): esquina superior derecha
# - "sw" (suroeste): esquina inferior izquierda
# - "se" (suroeste): esquina inferior derecha

# Ajusta el anclaje y las coordenadas como desees
# canvas_imagen = canvas.create_image(100, 100, image=imagen_tk, anchor="nw")  # Esquina superior izquierda
# canvas_imagen = canvas.create_image(ventana.winfo_width() - 50, ventana.winfo_height() - 50, image=imagen_tk, anchor="se")  # Esquina inferior derecha

# Vincular el evento de cambio de tamaño para ajustar la imagen
ventana.bind("<Configure>", ajustar_imagen)

# Ejecutar la ventana
ventana.mainloop()
