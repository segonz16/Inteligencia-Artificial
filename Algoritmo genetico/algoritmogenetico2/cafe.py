import random as rd
import tkinter as tk

# =====================
# Algoritmo Genético
# =====================

def crear_cromosoma():
    cafe1 = rd.randint(0, 100)
    cafe2 = rd.randint(0, 100 - cafe1)
    cafe3 = 100 - cafe1 - cafe2
    return [cafe1, cafe2, cafe3]

def funcion_objetivo(cromosoma, destino):
    return -sum(abs(cromosoma[i] - destino[i]) for i in range(3))

def cruce(p1, p2):
    punto = rd.randint(1, 2)
    hijo = p1[:punto] + p2[punto:]
    if sum(hijo) != 100:  
        diff = 100 - sum(hijo)
        hijo[0] += diff  
    return hijo

def mutacion(cromosoma):
    i, j = rd.sample(range(3), 2)
    cambio = rd.randint(-5, 5)
    if 0 <= cromosoma[i] + cambio <= 100 and 0 <= cromosoma[j] - cambio <= 100:
        cromosoma[i] += cambio
        cromosoma[j] -= cambio
    return cromosoma

# =====================
# Interfaz gráfica
# =====================

def crear_poblacion():
    global poblacion, destino, historial
    try:
        destino = [int(e1.get()), int(e2.get()), int(e3.get())]
        if sum(destino) != 100:
            text_result.insert(tk.END, " La suma debe ser 100\n")
            return
    except:
        text_result.insert(tk.END, " Valores inválidos\n")
        return

    poblacion = [crear_cromosoma() for _ in range(10)]
    historial = []

    mejor = max(poblacion, key=lambda c: funcion_objetivo(c, destino))
    historial.append((0, mejor, funcion_objetivo(mejor, destino)))

    text_result.insert(tk.END, f"Generación 0: {mejor} | Fitness {funcion_objetivo(mejor, destino)}\n")

def iniciar_algoritmo():
    global poblacion, destino, historial
    generaciones = 50

    for gen in range(generaciones):
        poblacion.sort(key=lambda c: funcion_objetivo(c, destino), reverse=True)
        nueva_pob = poblacion[:2]

        while len(nueva_pob) < len(poblacion):
            p1, p2 = rd.sample(poblacion[:5], 2)
            hijo = cruce(p1, p2)
            if rd.random() < 0.3:
                hijo = mutacion(hijo)
            nueva_pob.append(hijo)

        poblacion = nueva_pob
        mejor = max(poblacion, key=lambda c: funcion_objetivo(c, destino))
        historial.append((gen+1, mejor, funcion_objetivo(mejor, destino)))

        text_result.insert(tk.END, f"Generación {gen+1}: {mejor} | Fitness {funcion_objetivo(mejor, destino)}\n")

        if mejor == destino:
            text_result.insert(tk.END, "¡Mezcla exacta encontrada!\n")
            break

def borrar_informacion():
    text_result.delete("1.0", tk.END)

root = tk.Tk()
root.title("Algoritmo Genético - Mezcla de Café")

tk.Label(root, text="Destino Café 1:").grid(row=0, column=0)
tk.Label(root, text="Destino Café 2:").grid(row=1, column=0)
tk.Label(root, text="Destino Café 3:").grid(row=2, column=0)

e1 = tk.Entry(root); e1.grid(row=0, column=1)
e2 = tk.Entry(root); e2.grid(row=1, column=1)
e3 = tk.Entry(root); e3.grid(row=2, column=1)

btn_crear = tk.Button(root, text="Crear Población", command=crear_poblacion)
btn_crear.grid(row=3, column=0, pady=5)

btn_iniciar = tk.Button(root, text="Iniciar Algoritmo", command=iniciar_algoritmo)
btn_iniciar.grid(row=3, column=1, pady=5)

btn_borrar = tk.Button(root, text="Borrar Información", command=borrar_informacion)
btn_borrar.grid(row=3, column=2, pady=5)

text_result = tk.Text(root, height=20, width=70)
text_result.grid(row=4, column=0, columnspan=3)

root.mainloop()
