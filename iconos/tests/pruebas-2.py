import requests

def obtener_pokemon_generacion_9():
    # URL base de la PokéAPI para la lista de Pokémon
    url = "https://pokeapi.co/api/v2/pokemon/"
    
    # Lista para almacenar los nombres de los Pokémon de la Gen 9
    pokemones = []
    
    # Obtener Pokémon desde el 905 hasta el 1010
    for i in range(905, 1025):  # Los Pokémon de la Generación 9 van del 905 al 1010
        response = requests.get(f"{url}{i}/")
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            data = response.json()
            nombre = data["name"]
            pokemones.append(f"{i} {nombre}")
        else:
            print(f"Error al obtener datos del Pokémon con ID {i}")
    
    return pokemones

def guardar_pokemon_gen_9_en_txt():
    # Obtener la lista de Pokémon de la Generación 9
    gen_9 = obtener_pokemon_generacion_9()
    
    # Guardar la lista en un archivo de texto
    with open("pokemon_generacion_9.txt", "w") as file:
        for pokemon in gen_9:
            file.write(pokemon + "\n")
    
    print("La lista de Pokémon de la Generación 9 ha sido guardada en 'pokemon_generacion_9.txt'.")

# Ejecutar la función para guardar los datos
guardar_pokemon_gen_9_en_txt()
