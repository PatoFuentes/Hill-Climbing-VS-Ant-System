import random
import time
import math

# Definir el problema del Viajante de Comercio (TSP)
nodos = 20
coordenadas = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(nodos)]

# Calcular la distancia euclidiana entre dos nodos
def distancia(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Matriz de distancias entre cada par de nodos
distancias = [[distancia(coordenadas[i], coordenadas[j]) for j in range(nodos)] for i in range(nodos)]

# 1. Algoritmo Hill Climbing (HC)
def hill_climbing():
    # Generar una solución inicial aleatoria
    solucion_actual = list(range(nodos))
    random.shuffle(solucion_actual)
    mejor_costo = calcular_costo(solucion_actual)
    
    # Iterar para encontrar una mejor solución
    for _ in range(1000):  # Límite de iteraciones
        vecinos = generar_vecinos(solucion_actual)
        for vecino in vecinos:
            costo_vecino = calcular_costo(vecino)
            if costo_vecino < mejor_costo:
                solucion_actual = vecino
                mejor_costo = costo_vecino
    
    return solucion_actual, mejor_costo

# Generar vecinos mediante intercambio de dos nodos
def generar_vecinos(solucion):
    vecinos = []
    for i in range(len(solucion)):
        for j in range(i + 1, len(solucion)):
            vecino = solucion[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

# Calcular el costo de una solución
def calcular_costo(solucion):
    costo = 0
    for i in range(len(solucion) - 1):
        costo += distancias[solucion[i]][solucion[i + 1]]
    costo += distancias[solucion[-1]][solucion[0]]  # Regresar al nodo inicial
    return costo

# 2. Algoritmo Ant System (AS)
def ant_system(iteraciones=100, num_hormigas=20, alfa=1, beta=5, evaporacion=0.5, q=100):
    feromonas = [[1 for _ in range(nodos)] for _ in range(nodos)]  # Inicializar feromonas
    mejor_solucion = None
    mejor_costo = float('inf')
    
    for _ in range(iteraciones):
        soluciones_hormigas = []
        costos_hormigas = []
        
        # Cada hormiga construye una solución
        for _ in range(num_hormigas):
            solucion = construir_solucion(feromonas, alfa, beta)
            costo = calcular_costo(solucion)
            soluciones_hormigas.append(solucion)
            costos_hormigas.append(costo)
            
            if costo < mejor_costo:
                mejor_solucion = solucion
                mejor_costo = costo
        
        # Actualizar feromonas
        for i in range(nodos):
            for j in range(nodos):
                feromonas[i][j] *= (1 - evaporacion)  # Evaporación
                for k in range(num_hormigas):
                    if j in soluciones_hormigas[k]:
                        feromonas[i][j] += q / costos_hormigas[k]
                        
    return mejor_solucion, mejor_costo

# Construir una solución probística basada en las feromonas
def construir_solucion(feromonas, alfa, beta):
    solucion = [random.randint(0, nodos - 1)]
    while len(solucion) < nodos:
        i = solucion[-1]
        probabilidades = []
        for j in range(nodos):
            if j not in solucion:
                tau = feromonas[i][j] ** alfa
                eta = (1.0 / distancias[i][j]) ** beta
                probabilidades.append(tau * eta)
            else:
                probabilidades.append(0)
        
        # Seleccionar el próximo nodo basado en las probabilidades
        total_probabilidad = sum(probabilidades)
        probabilidades = [p / total_probabilidad for p in probabilidades]
        siguiente_nodo = random.choices(range(nodos), probabilidades)[0]
        solucion.append(siguiente_nodo)
    
    return solucion

# Comparación de los dos algoritmos
def comparar_algoritmos():
    print("Iniciando Hill Climbing...")
    start_time = time.time()
    solucion_hc, costo_hc = hill_climbing()
    tiempo_hc = time.time() - start_time
    print(f"Hill Climbing - Costo: {costo_hc}, Tiempo: {tiempo_hc:.2f} segundos")
    
    print("\nIniciando Ant System...")
    start_time = time.time()
    solucion_as, costo_as = ant_system()
    tiempo_as = time.time() - start_time
    print(f"Ant System - Costo: {costo_as}, Tiempo: {tiempo_as:.2f} segundos")

# Ejecutar la comparación
comparar_algoritmos()
