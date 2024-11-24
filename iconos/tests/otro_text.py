import tkinter as tk

def mostrar_informacion():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Mostrar Información")
    
    # Crear un frame para contener el Text y el Scrollbar
    frame = tk.Frame(ventana)
    frame.pack(pady=20)

    # Crear un widget Text (cuadro de texto) en el frame
    text_box = tk.Text(frame, height=10, width=40, wrap=tk.WORD)  # Ajusta el tamaño según lo que necesites
    text_box.pack(side=tk.LEFT)

    # Crear una barra de desplazamiento
    scrollbar = tk.Scrollbar(frame, command=text_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configurar el Text para que use la barra de desplazamiento
    text_box.config(yscrollcommand=scrollbar.set)

    # Información a mostrar en el Text box
    informacion = """Este es una prueba 
    para ver cómo se muestra un párrafo largo dentro de un cuadro de texto en una ventana de Tkinter. 
Me gusta cómo queda la interfaz gráfica, pero la cantidad de texto es demasiado grande para una sola línea, por lo que es necesario que se ajuste de manera que se pueda leer bien.
Por ejemplo, este es un texto largo donde se está probando si todo el texto se ajusta bien sin que se corte o quede fuera de la vista del usuario. Es importante que el texto se vea de manera legible sin que se corte. 
Aquí hay algo más de texto para probar cómo se comporta cuando hay mucho más contenido.
    """
    
    # Insertar la información en el Text box
    text_box.insert(tk.END, informacion)

    # Evitar que el usuario edite el contenido
    text_box.config(state=tk.DISABLED)

    ventana.mainloop()

# Llamar la función para mostrar la ventana
mostrar_informacion()
