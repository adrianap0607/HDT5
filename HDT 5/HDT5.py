import simpy
import random
import numpy as np
import csv

# Parámetros de la simulación
NUM_PROCESSES = [25, 50, 100, 150, 200]
ARRIVAL_INTERVAL = 10
CPU_SPEED = 1
INSTRUCTIONS_PER_CYCLE = 3
MEMORY_SIZE = 100
NEW_RANDOM_SEED = 20  # Nuevo valor para el random seed

# Variables para almacenar los tiempos de cada simulación
average_times = []
standard_deviations = []

# Función para simular un proceso
def process(env, name, memory, cpu, times):
    arrival_time = env.now
    memory_request = random.randint(1, 10)
    instructions_to_execute = random.randint(1, 10)

    with memory.get(memory_request) as req:
        yield req

        while instructions_to_execute > 0:
            with cpu.request() as req1:
                yield req1
                instructions_executed = min(CPU_SPEED * INSTRUCTIONS_PER_CYCLE, instructions_to_execute)
                instructions_to_execute -= instructions_executed
                yield env.timeout(instructions_executed)

        finish_time = env.now
        total_time = finish_time - arrival_time
        times.append(total_time)

# Función para ejecutar una simulación con una cantidad específica de procesos
def run_simulation(num_processes):
    env = simpy.Environment()
    memory = simpy.Container(env, init=MEMORY_SIZE, capacity=MEMORY_SIZE)
    cpu = simpy.Resource(env, capacity=2)
    times = []

    env.process(generate_processes(env, num_processes, memory, cpu, times))
    env.run()

    return times

# Generador de procesos
def generate_processes(env, num_processes, memory, cpu, times):
    for j in range(num_processes):
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_INTERVAL))
        env.process(process(env, f'Process-{j+1}', memory, cpu, times))

# Fijar la nueva semilla aleatoria
random.seed(NEW_RANDOM_SEED)

# Ejecuta la simulación para cada cantidad de procesos
for num in NUM_PROCESSES:
    times = run_simulation(num)
    avg_time = np.mean(times)
    std_deviation = np.std(times)
    average_times.append(avg_time)
    standard_deviations.append(std_deviation)

    print(f"Para {num} procesos:")
    print(f"Tiempo promedio: {avg_time}")
    print(f"Desviación estándar: {std_deviation}")
    print()

# Escribir los resultados en un archivo CSV
with open('simulacion_resultados.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Cantidad de Procesos', 'Tiempo Promedio'])
    for i, num in enumerate(NUM_PROCESSES):
        writer.writerow([num, average_times[i]])

print("---------------------------------------------------------------")
# Imprimir los resultados finales
print("Resultados finales:")
for i, num in enumerate(NUM_PROCESSES):
    print(f"Para {num} procesos:")
    print(f"Tiempo promedio: {average_times[i]}")
    print(f"Desviación estándar: {standard_deviations[i]}")
    print()
print("---------------------------------------------------------------")
