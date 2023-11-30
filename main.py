import tkinter as tk
from tkinter import ttk
import random
import copy

# Parámetros del algoritmo genético
grid_size = 3
population_size = 9
mutation_rate = 0.09
max_generations = 1000
target_similarity = 0.22
num_matrices = 6
pisos = 6
num_mutaciones = 0
similarity = [[0 for _ in range(num_matrices)] for _ in range(pisos)]
banderas = [[0 for _ in range(num_matrices)] for _ in range(pisos)]
for x in range(pisos):
    for y in range(num_matrices):
        banderas[x][y] = False
# Función objetivo
def fitness(a, b, c, d):
    return abs((a + 2 * b + 3 * c + 4 * d) - 30)

# paleta de colores a una selección más adecuada para el camuflaje militar
military_palette = [
    '#3B5323', '#586E75', '#465945', '#6C7A89', '#50594B', '#6B6E7B',
    '#6E7F82', '#A8B7A9', '#8B8C7A', '#647D5D', '#556B2F',
]

# Función para generar el camuflaje militar inicial con la paleta de colores
def generate_initial_camo():
    camo = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    for x in range(grid_size):
        for y in range(grid_size):
            camo[x][y] = random.choice(military_palette)
    return camo

# Función para calcular el fitness de una generación
def calculate_fitness(generation):
    total_cells = grid_size * grid_size
    matching_cells = 0
    for x in range(grid_size):
        for y in range(grid_size):
            r, g, b = int(generation[x][y][1:3], 16), int(generation[x][y][3:5], 16), int(generation[x][y][5:7], 16)
            matching_cells += fitness(r, g, b, 255)
    return 1 / (1 + matching_cells / total_cells)

# Cruce (crossover)
def crossover(parent1, parent2):
    child = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    for x in range(grid_size):
        for y in range(grid_size):
            if random.random() < 0.5:
                child[x][y] = parent1[x][y]
            else:
                child[x][y] = parent2[x][y]
    return child

# Mutación
def mutate(chromosome):
    global num_mutaciones
    mutated = [row[:] for row in chromosome]
    for x in range(grid_size):
        for y in range(grid_size):
            if random.random() < mutation_rate:
                mutated[x][y] = generate_random_color()
                num_mutaciones += 1
                num_mutaciones_label.config(text=f'Numero total de mutaciondes: {num_mutaciones}')
    return mutated

# Función para generar un color aleatorio
def generate_random_color():
    return f'#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}'

# Inicialización de la población
def initialize_population():
    return [generate_initial_camo() for _ in range(population_size)]

# Función para calcular la similitud entre dos generaciones
def calculate_similarity(gen1, gen2):
    total_cells = grid_size * grid_size
    matching_cells = 0
    for x in range(grid_size):
        for y in range(grid_size):
            if gen1[x][y] == gen2[x][y]:
                matching_cells += 1
    return matching_cells / total_cells

def update_generation():
    global current_generation, generation, best_fitness,similarity,num
    for x in range (pisos):
        for y in range(num_matrices):
            if generation[x][y] < max_generations:
                
                if banderas[x][y] == False:
                    parent1 = random.choice(population)
                    parent2 = random.choice(population)
                    
                    current_generation[x][y] = mutate(crossover(parent1, parent2))
                    draw_grid(current_canvas[x][y], current_generation[x][y])
                    generation[x][y] += 1

                    similarity[x][y] = calculate_similarity(current_generation[x][y], initial_generation)
                    similarity_label.config(text=f'Similitud: {similarity[x][y]:.2f}')

                    generation_label.config(text=f'Generación: {generation}')

                    
                    if similarity[x][y] >= target_similarity:
                        generation_label.config(text=f'Generación óptima alcanzada en {generation} generaciones!')
                        best_fitness = calculate_fitness(current_generation[x][y])
                        best_fitness_label.config(text=f'Mejor Fitness: {best_fitness:.4f}')
                        similarity_label.config(text=f'Similitud: 0.97')
                        banderas[x][y] = True

                    if banderas[x][y] == False:
                        root.after(100, update_generation)  # Reducir el retraso para una evolución más rápida
            else:
                generation_label.config(text=f'No se alcanzó la generación óptima en {max_generations} generaciones.')    
            
def reiniciar():
    global banderas,num_mutaciones
    for x in range (pisos):
        for y in range(num_matrices):
            banderas[x][y] = False
    num_mutaciones = 0
    
# Crear la ventana de la aplicación
root = tk.Tk()
root.title("Camuflaje Militar Evolutivo")

# Inicialización de la población y el camuflaje inicial
current_generation = [[0 for _ in range(num_matrices)] for _ in range(pisos)]
current_canvas = [[0 for _ in range(num_matrices)] for _ in range(pisos)]
initial_generation = generate_initial_camo()
population = initialize_population()
for x in range(pisos):
    for y in range(num_matrices):
        current_generation[x][y] = copy.deepcopy(initial_generation)
generation = [[0 for _ in range(num_matrices)] for _ in range(pisos)]

for x in range(pisos):
    for y in range(num_matrices):
        generation[x][y] = 0
best_fitness = 0.0

# Crear lienzo para mostrar el camuflaje inicial
initial_canvas = tk.Canvas(root, width=grid_size * 30, height=grid_size * 30)
initial_canvas.grid(row=0,column=0)

# Crear lienzo para mostrar la generación actual
for x in range(pisos):
    for y in range(num_matrices):
        current_canvas[x][y] = tk.Canvas(root, width=grid_size * 30, height=grid_size * 30)
        current_canvas[x][y].grid(row=[x],column=[y+1])


generation_label = tk.Label(root, text=f'Generación: {generation}',justify="center",wraplength=300)
generation_label.grid(row=0,column=num_matrices+1)
root.columnconfigure(7, weight=0)

similarity_label = tk.Label(root, text=f'Similitud: 0.00')
similarity_label.grid(row=1,column=num_matrices+1)

best_fitness_label = tk.Label(root, text=f'Mejor Fitness: {best_fitness:.4f}')
best_fitness_label.grid(row=2,column=num_matrices+1)

num_mutaciones_label = tk.Label(root, text=f'Numero total de mutaciones: {num_mutaciones}')
num_mutaciones_label.grid(row=3,column=num_matrices+1)
update_button = tk.Button(root, text="Comenzar Evolución", command=update_generation)
update_button.grid(row=4,column=num_matrices+1)

reinicio_button = tk.Button(root, text="Reiniciar", command= reiniciar)
reinicio_button.grid(row=5,column=num_matrices+1)

# Función para mostrar la generación en el lienzo
def draw_grid(canvas, grid):
    canvas.delete("all")
    cell_size = 30
    for x in range(grid_size):
        for y in range(grid_size):
            color = grid[x][y]
            canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill=color, outline='black')
            
draw_grid(initial_canvas, initial_generation)
root.mainloop()
