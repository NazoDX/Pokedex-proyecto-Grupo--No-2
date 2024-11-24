import os
import random
import pygame

def reproducir_sonido_aleatorio():
    # Ruta a la carpeta "sounds/cries" en la raíz del proyecto
    carpeta = os.path.join("sounds", "cries")

    # Obtener una lista de archivos .wav
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.wav')]
    if not archivos:
        print("No hay archivos .wav en la carpeta.")
        return

    # Seleccionar un archivo aleatorio
    archivo_aleatorio = random.choice(archivos)
    ruta_archivo = os.path.join(carpeta, archivo_aleatorio)

    # Iniciar pygame mixer y reproducir el sonido
    pygame.mixer.init()
    pygame.mixer.music.load(ruta_archivo)
    pygame.mixer.music.play()

    print(f"Reproduciendo: {archivo_aleatorio}")

    # Esperar a que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Ejecutar la función
reproducir_sonido_aleatorio()
reproducir_sonido_aleatorio()
