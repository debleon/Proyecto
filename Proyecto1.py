import random

class Ataque:
    def __init__(self, nombre, danio):
        self.nombre = nombre
        self.danio = danio

class EstrategiaSeleccionAtaque:
    def seleccionar_ataque(self, pokemon):
        pass

class EstrategiaSeleccionAtaqueHumano(EstrategiaSeleccionAtaque):
    def seleccionar_ataque(self, pokemon):
        print(f"Ataques disponibles para {pokemon.nombre}:")
        for i, ataque in enumerate(pokemon.ataques):
            print(f"{i + 1}. {ataque.nombre} (Daño: {ataque.danio})")
        seleccion = int(input("Seleccione un ataque (1-4): "))
        return pokemon.ataques[seleccion - 1]

class EstrategiaSeleccionAtaqueMaquina(EstrategiaSeleccionAtaque):
    def seleccionar_ataque(self, pokemon):
        return random.choice(pokemon.ataques)

class ObservadorSaludPokemon:
    def __init__(self, pokemon):
        self.pokemon = pokemon
        self.pokemon.agregar_observador(self)

    def actualizar(self):
        if self.pokemon.salud <= 0:
            print(f"{self.pokemon.nombre} ha sido derrotado!")
        else:
            print(f"Salud de {self.pokemon.nombre}: {self.pokemon.salud}")

class Pokemon:
    def __init__(self, nombre, salud, ataques, estrategia_seleccion_ataque):
        self.nombre = nombre
        self.salud = salud
        self.ataques = ataques
        self.estrategia_seleccion_ataque = estrategia_seleccion_ataque
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def quitar_observador(self, observador):
        self.observadores.remove(observador)

    def recibir_ataque(self, ataque):
        self.salud -= ataque.danio
        if self.salud < 0:
            self.salud = 0
            self.notificar_observadores()

    def seleccionar_ataque(self):
        return self.estrategia_seleccion_ataque.seleccionar_ataque(self)

    def notificar_observadores(self):
        for observador in self.observadores:
            observador.actualizar()

def seleccionar_objetivo(equipo):
    pokemones_vivos = [pokemon for pokemon in equipo if pokemon.salud > 0]
    if pokemones_vivos:
        return random.choice(pokemones_vivos)
    else:
        return None

def turno_jugador(equipo_jugador, equipo_maquina):
    print("\nTurno del Jugador:")
    for pokemon in equipo_jugador:
        if pokemon.salud > 0:
            print(f"Salud de {pokemon.nombre}: {pokemon.salud}")
            print(f"Turno de {pokemon.nombre}")
            ataque = pokemon.seleccionar_ataque()
            objetivo = seleccionar_objetivo(equipo_maquina)
            if objetivo is not None:
                print(f"{pokemon.nombre} ha usado {ataque.nombre} contra {objetivo.nombre}.")
                objetivo.recibir_ataque(ataque)
            else:
                print("¡No hay objetivo válido para atacar!")

def turno_maquina(equipo_maquina, equipo_jugador):
    print("\nTurno de la Máquina:")
    for pokemon in equipo_maquina:
        if pokemon.salud > 0:
            print(f"Salud de {pokemon.nombre}: {pokemon.salud}")
            ataque = pokemon.seleccionar_ataque()
            objetivo = seleccionar_objetivo(equipo_jugador)
            if objetivo is not None:
                print(f"{pokemon.nombre} ha usado {ataque.nombre} contra {objetivo.nombre}.")
                objetivo.recibir_ataque(ataque)
            else:
                print("¡No hay objetivo válido para atacar!")

def seleccionar_modo_juego():
    while True:
        print("Selecciona el modo de juego:")
        print("1. Jugar contra otro jugador")
        print("2. Jugar contra la máquina")
        modo = input("Selecciona una opción: ")
        if modo == "1":
            return "jugador"
        elif modo == "2":
            return "maquina"
        else:
            print("Opción inválida. Inténtalo de nuevo.")

def main():
    print("¡Bienvenido a la Batalla Pokémon!")

    # Seleccionar el modo de juego
    modo = seleccionar_modo_juego()

    # Crear equipo del jugador 1
    equipo_jugador_1 = []
    pokemones_disponibles = pokemones.copy()  # Copiar la lista de pokemones disponibles
    print("Jugador 1, selecciona tu equipo de Pokémon:")
    for _ in range(3):
        print("Elige un Pokémon para tu equipo:")
        for i, pokemon in enumerate(pokemones_disponibles):
            print(f"{i + 1}. {pokemon['nombre']}")
        seleccion = int(input("Selecciona un Pokémon: "))

        # Validar que la selección esté dentro del rango y no se haya seleccionado antes
        while seleccion <= 0 or seleccion > len(pokemones_disponibles):
            print("Selección inválida. Inténtalo de nuevo.")
            seleccion = int(input("Selecciona un Pokémon: "))
        
        pokemon_elegido = pokemones_disponibles.pop(seleccion - 1)  # Eliminar el Pokémon seleccionado de los disponibles
        equipo_jugador_1.append(Pokemon(pokemon_elegido["nombre"], pokemon_elegido["salud"], pokemon_elegido["ataques"], EstrategiaSeleccionAtaqueHumano()))

    if modo == "jugador":
        # Crear equipo del jugador 2
        equipo_jugador_2 = []
        print("Jugador 2, selecciona tu equipo de Pokémon:")
        for _ in range(3):
            print("Elige un Pokémon para tu equipo:")
            for i, pokemon in enumerate(pokemones_disponibles):
                print(f"{i + 1}. {pokemon['nombre']}")
            seleccion = int(input("Selecciona un Pokémon: "))

            # Validar que la selección esté dentro del rango y no se haya seleccionado antes
            while seleccion <= 0 or seleccion > len(pokemones_disponibles):
                print("Selección inválida. Inténtalo de nuevo.")
                seleccion = int(input("Selecciona un Pokémon: "))
            
            pokemon_elegido = pokemones_disponibles.pop(seleccion - 1)  # Eliminar el Pokémon seleccionado de los disponibles
            equipo_jugador_2.append(Pokemon(pokemon_elegido["nombre"], pokemon_elegido["salud"], pokemon_elegido["ataques"], EstrategiaSeleccionAtaqueHumano()))

        # Añadir observadores de salud
        for pokemon in equipo_jugador_1 + equipo_jugador_2:
            ObservadorSaludPokemon(pokemon)

        print("¡Comienza la batalla Pokémon entre Jugador 1 y Jugador 2!")
        jugar(equipo_jugador_1, equipo_jugador_2)

    elif modo == "maquina":
        # Crear equipo de la máquina
        equipo_maquina = []
        print("El equipo de la máquina ha sido seleccionado aleatoriamente.")
        for _ in range(3):
            pokemon_aleatorio = random.choice(pokemones)
            equipo_maquina.append(Pokemon(pokemon_aleatorio["nombre"], pokemon_aleatorio["salud"], pokemon_aleatorio["ataques"], EstrategiaSeleccionAtaqueMaquina()))

        # Añadir observadores de salud
        for pokemon in equipo_jugador_1 + equipo_maquina:
            ObservadorSaludPokemon(pokemon)

        print("¡Comienza la batalla Pokémon entre Jugador 1 y la Máquina!")
        jugar(equipo_jugador_1, equipo_maquina)

# Lista de pokémones con sus ataques
pokemones = [
    {"nombre": "Pikachu", "salud": 100, "ataques": [Ataque("Impactrueno", 30), Ataque("Rayo", 25), Ataque("Ataque Rápido", 20), Ataque("Placaje", 15)]},
    {"nombre": "Caterpie", "salud": 80, "ataques": [Ataque("Placaje", 20), Ataque("Tacleada", 15), Ataque("Supersónico", 10), Ataque("Drenadoras", 5)]},
    {"nombre": "Pidgeotto", "salud": 120, "ataques": [Ataque("Picotazo", 25), Ataque("Remolino", 15), Ataque("Tornado", 35), Ataque("Ataque Rápido", 5)]},
    {"nombre": "Bulbasaur", "salud": 110, "ataques": [Ataque("Látigo Cepa", 20), Ataque("Drenadoras", 5), Ataque("Placaje", 15), Ataque("Somnífero", 30)]},
    {"nombre": "Charmander", "salud": 100, "ataques": [Ataque("Lanzallamas", 30), Ataque("Gruñido", 5), Ataque("Arañaso", 10), Ataque("Ascuas", 20)]},
    {"nombre": "Squirtle", "salud": 100, "ataques": [Ataque("Pistola Agua", 10), Ataque("Burbuja", 5), Ataque("Ataque Rápido", 20), Ataque("Placaje", 15)]},
    {"nombre": "Krabby", "salud": 90, "ataques": [Ataque("Burbuja", 5), Ataque("Rayo Burbuja", 10), Ataque("Placaje", 15), Ataque("Tajo Cruzado", 30)]},
    {"nombre": "Raticate", "salud": 110, "ataques": [Ataque("Hipercolmillo", 30), Ataque("Ataque Rápido", 15), Ataque("Placaje", 10), Ataque("Golpe Cabeza", 20)]},
    {"nombre": "Muk", "salud": 120, "ataques": [Ataque("Lodo", 10), Ataque("Bomba Lodo", 20), Ataque("Ataque Ácido", 30), Ataque("Infortunio", 5)]},
    {"nombre": "Kingler", "salud": 100, "ataques": [Ataque("Hidropulso", 30), Ataque("Rayo Burbuja", 20), Ataque("Rayo", 10), Ataque("Placaje", 15)]},
]

def jugar(equipo_jugador_1, equipo_jugador_2):
    # Iniciar batalla
    turno_actual = 1
    while any(pokemon.salud > 0 for pokemon in equipo_jugador_1) and any(pokemon.salud > 0 for pokemon in equipo_jugador_2):
        print(f"\nTurno {turno_actual}:")

        # Turno del Jugador 1
        print("\nTurno del Jugador 1:")
        turno_jugador(equipo_jugador_1, equipo_jugador_2)
        
        # Verificar si el jugador 2 sigue en la batalla
        if not any(pokemon.salud > 0 for pokemon in equipo_jugador_2):
            break

        # Turno del Jugador 2
        print("\nTurno del Jugador 2:")
        turno_jugador(equipo_jugador_2, equipo_jugador_1)
        
        # Incrementar el número de turno
        turno_actual += 1

    # Determinar el ganador
    if all(pokemon.salud <= 0 for pokemon in equipo_jugador_1):
        print("¡El Jugador 2 ha ganado la batalla!")
    elif all(pokemon.salud <= 0 for pokemon in equipo_jugador_2):
        print("¡El Jugador 1 ha ganado la batalla!")
    else:
        print("¡La batalla ha terminado en empate!")


if __name__ == "__main__":
    main()
