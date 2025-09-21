import pygame
import random as rand
import sys
import math

# ==========================
# Configuración
# ==========================
VEL_SEGURA = 5
MAX_GEN = 200
ANCHO, ALTO = 1000, 600

# Colores
CIELO = (135, 206, 250)
TIERRA = (34, 139, 34)
PARACAIDAS = (220, 20, 60)
CUERDAS = (139, 69, 19)
PARACAIDISTA = (255, 140, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (220, 220, 220)
GRIS_OSCURO = (150, 150, 150)

# ==========================
# Inicialización Pygame
# ==========================
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación Aterrizaje Paracaidista - Algoritmo Genético")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
font_titulo = pygame.font.SysFont("Arial", 24, bold=True)

# ==========================
# Clases
# ==========================
class Paracaidas:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiempo = 0
        self.oscilacion_x = 0
        self.oscilacion_y = 0
        
    def actualizar(self, velocidad):
        self.tiempo += 0.15
        # Oscilación suave basada en velocidad
        self.oscilacion_x = math.sin(self.tiempo) * (velocidad * 0.5)
        self.oscilacion_y = math.cos(self.tiempo * 0.8) * 2
        
    def dibujar(self, pantalla, individuo):
        V, B, S = individuo
        centro_x = self.x + self.oscilacion_x
        centro_y = self.y + self.oscilacion_y
        
        # Tamaño del paracaídas basado en parámetros
        radio_paracaidas = 60 + (B * 3) + (S * 2)
        
        # Dibujar paracaídas (semicírculo con ondulación)
        puntos_paracaidas = []
        for i in range(20):
            angulo = math.pi * i / 19
            ondulacion = math.sin(self.tiempo + i * 0.5) * 3
            px = centro_x + (radio_paracaidas + ondulacion) * math.cos(angulo)
            py = centro_y - (radio_paracaidas + ondulacion) * math.sin(angulo) * 0.7
            puntos_paracaidas.append((px, py))
        
        # Rellenar paracaídas
        if len(puntos_paracaidas) > 2:
            pygame.draw.polygon(pantalla, PARACAIDAS, puntos_paracaidas)
            pygame.draw.polygon(pantalla, NEGRO, puntos_paracaidas, 2)
        
        # Líneas del paracaídas
        for i in range(0, len(puntos_paracaidas), 3):
            if i < len(puntos_paracaidas):
                pygame.draw.line(pantalla, NEGRO, 
                               (centro_x, centro_y), puntos_paracaidas[i], 1)
        
        # Cuerdas del paracaídas
        paracaidista_y = centro_y + 80
        cuerda_puntos = [
            (centro_x - radio_paracaidas * 0.6, centro_y),
            (centro_x + radio_paracaidas * 0.6, centro_y),
            (centro_x - radio_paracaidas * 0.3, centro_y),
            (centro_x + radio_paracaidas * 0.3, centro_y)
        ]
        
        for punto in cuerda_puntos:
            pygame.draw.line(pantalla, CUERDAS, punto, 
                           (centro_x, paracaidista_y), 2)
        
        # Paracaidista (más detallado)
        pygame.draw.circle(pantalla, PARACAIDISTA, 
                          (int(centro_x), int(paracaidista_y)), 15)
        # Casco
        pygame.draw.circle(pantalla, BLANCO, 
                          (int(centro_x), int(paracaidista_y - 5)), 8)

class Boton:
    def __init__(self, x, y, w, h, texto, color=GRIS_CLARO, color_hover=GRIS_OSCURO):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.clickeado = False

    def dibujar(self, pantalla):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        # Determinar color
        color_actual = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color
        
        # Dibujar botón con sombra
        pygame.draw.rect(pantalla, (100, 100, 100), 
                        (self.rect.x + 3, self.rect.y + 3, self.rect.w, self.rect.h))
        pygame.draw.rect(pantalla, color_actual, self.rect)
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
        
        # Texto centrado
        texto_surf = font.render(self.texto, True, NEGRO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        pantalla.blit(texto_surf, texto_rect)
        
        # Detectar click
        if self.rect.collidepoint(mouse_pos) and mouse_click[0] and not self.clickeado:
            self.clickeado = True
            return True
        elif not mouse_click[0]:
            self.clickeado = False
            
        return False

# ==========================
# Funciones del Algoritmo Genético
# ==========================
def crear_individuo():
    return [rand.randint(1, 20), rand.randint(1, 10), rand.randint(1, 15)]

def calcular_fitness(individuo):
    V, B, S = individuo
    penalizacion = abs(V - VEL_SEGURA)
    return max(0, 100 - (penalizacion * 10) + (B * 2) + (S * 3))

def mutar_individuo(individuo):
    hijo = individuo.copy()
    gen_mutacion = rand.randint(0, 2)
    
    if gen_mutacion == 0:
        hijo[0] = rand.randint(1, 20)  # Velocidad
    elif gen_mutacion == 1:
        hijo[1] = rand.randint(1, 10)  # Freno
    else:
        hijo[2] = rand.randint(1, 15)  # Seguridad
    
    return hijo

# ==========================
# Funciones de Interfaz
# ==========================
def dibujar_fondo():
    # Degradado de cielo
    for y in range(ALTO - 50):
        color_r = 135 + int((200 - 135) * y / (ALTO - 50))
        color_g = 206 + int((230 - 206) * y / (ALTO - 50))
        color_b = 250
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, y), (ANCHO, y))
    
    # Suelo con textura
    pygame.draw.rect(pantalla, TIERRA, (0, ALTO - 50, ANCHO, 50))
    for i in range(0, ANCHO, 20):
        pygame.draw.line(pantalla, (40, 150, 40), (i, ALTO - 50), (i, ALTO), 1)

def dibujar_info(individuo, fitness, generacion, historico):
    V, B, S = individuo
    
    # Panel de información principal
    panel_rect = pygame.Rect(10, 10, 500, 80)
    panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
    panel_surface.set_alpha(180)
    panel_surface.fill((255, 255, 255))
    pantalla.blit(panel_surface, (panel_rect.x, panel_rect.y))
    pygame.draw.rect(pantalla, NEGRO, panel_rect, 2)
    
    # Texto principal
    texto_gen = font_titulo.render(f"Generación: {generacion}", True, NEGRO)
    pantalla.blit(texto_gen, (20, 20))
    
    texto_params = font.render(f"Velocidad: {V}  |  Freno: {B}  |  Seguridad: {S}", True, NEGRO)
    pantalla.blit(texto_params, (20, 45))
    
    texto_fitness = font.render(f"Fitness: {fitness}", True, NEGRO)
    pantalla.blit(texto_fitness, (20, 65))
    
    # Panel histórico
    if historico:
        panel_hist = pygame.Rect(ANCHO - 250, 10, 240, 180)
        hist_surface = pygame.Surface((panel_hist.width, panel_hist.height))
        hist_surface.set_alpha(180)
        hist_surface.fill((255, 255, 255))
        pantalla.blit(hist_surface, (panel_hist.x, panel_hist.y))
        pygame.draw.rect(pantalla, NEGRO, panel_hist, 2)
        
        pantalla.blit(font_titulo.render("Histórico", True, NEGRO), (ANCHO - 240, 20))
        
        for i, entrada in enumerate(historico[-5:]):
            color_fitness = (0, 150, 0) if entrada['fit'] >= 90 else (150, 0, 0)
            texto = font.render(f"Gen {entrada['gen']}: {entrada['fit']}", True, color_fitness)
            pantalla.blit(texto, (ANCHO - 240, 50 + i * 25))

def mostrar_resultado(mensaje, individuo, fitness, generacion, historico):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(100)
    overlay.fill(NEGRO)
    pantalla.blit(overlay, (0, 0))
    
    # Panel de resultado
    panel_w, panel_h = 400, 200
    panel_x = (ANCHO - panel_w) // 2
    panel_y = (ALTO - panel_h) // 2
    
    pygame.draw.rect(pantalla, BLANCO, (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(pantalla, NEGRO, (panel_x, panel_y, panel_w, panel_h), 3)
    
    # Mensaje principal
    color_mensaje = (0, 150, 0) if "EXITOSO" in mensaje else (150, 0, 0)
    texto_mensaje = font_titulo.render(mensaje, True, color_mensaje)
    texto_rect = texto_mensaje.get_rect(center=(ANCHO // 2, panel_y + 50))
    pantalla.blit(texto_mensaje, texto_rect)
    
    # Detalles
    V, B, S = individuo
    detalle = f"Gen {generacion} | V={V}, B={B}, S={S} | Fitness={fitness}"
    texto_detalle = font.render(detalle, True, NEGRO)
    detalle_rect = texto_detalle.get_rect(center=(ANCHO // 2, panel_y + 100))
    pantalla.blit(texto_detalle, detalle_rect)

# ==========================
# Simulación Principal
# ==========================
def ejecutar_simulacion(individuo, fitness, generacion, historico):
    V, B, S = individuo
    paracaidas = Paracaidas(ANCHO // 2, 80)
    velocidad_caida = V
    tiempo_simulacion = 0
    
    while paracaidas.y < ALTO - 120:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
        
        # Actualizar física
        tiempo_simulacion += 1
        paracaidas.y += velocidad_caida * 0.8
        paracaidas.actualizar(velocidad_caida)
        
        # Dibujar escena
        dibujar_fondo()
        paracaidas.dibujar(pantalla, individuo)
        dibujar_info(individuo, fitness, generacion, historico)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Determinar resultado
    mensaje = "ATERRIZAJE EXITOSO" if fitness >= 90 else "ATERRIZAJE FALLIDO"
    
    if mensaje == "ATERRIZAJE EXITOSO":
        return manejar_resultado_exitoso(mensaje, individuo, fitness, generacion, historico, paracaidas)
    
    return "continuar"

def manejar_resultado_exitoso(mensaje, individuo, fitness, generacion, historico, paracaidas):
    boton_reiniciar = Boton(150, 450, 200, 50, "🔄 Reiniciar Simulación")
    boton_nueva = Boton(450, 450, 200, 50, "🆕 Nueva Población")
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
        
        # Dibujar escena final
        dibujar_fondo()
        paracaidas.dibujar(pantalla, individuo)
        dibujar_info(individuo, fitness, generacion, historico)
        mostrar_resultado(mensaje, individuo, fitness, generacion, historico)
        
        # Manejar botones
        if boton_reiniciar.dibujar(pantalla):
            return "reiniciar"
        if boton_nueva.dibujar(pantalla):
            return "nueva"
        
        pygame.display.flip()
        clock.tick(60)

# ==========================
# Programa Principal
# ==========================
def main():
    mejor_individuo = None
    mejor_fitness = 0
    generacion_actual = 0
    historico = []
    
    boton_poblacion = Boton(100, 450, 250, 60, "Generar Población Inicial")
    boton_simulacion = Boton(450, 450, 250, 60, "Iniciar Simulación")
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        
        # Dibujar interfaz principal
        dibujar_fondo()
        
        # Título
        titulo = font_titulo.render("Simulación Aterrizaje Paracaidista - Algoritmo Genético", True, NEGRO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, 50))
        pantalla.blit(titulo, titulo_rect)
        
        # Manejar botones
        if boton_poblacion.dibujar(pantalla):
            mejor_individuo = crear_individuo()
            mejor_fitness = calcular_fitness(mejor_individuo)
            generacion_actual = 0
            historico.clear()
        
        if boton_simulacion.dibujar(pantalla) and mejor_individuo:
            # Ejecutar evolución
            for gen in range(1, MAX_GEN + 1):
                # Crear y evaluar nuevo individuo
                nuevo_individuo = mutar_individuo(mejor_individuo)
                nuevo_fitness = calcular_fitness(nuevo_individuo)
                
                # Selección
                if nuevo_fitness > mejor_fitness:
                    mejor_individuo = nuevo_individuo
                    mejor_fitness = nuevo_fitness
                
                generacion_actual = gen
                historico.append({"gen": gen, "fit": mejor_fitness})
                
                # Ejecutar simulación visual
                resultado = ejecutar_simulacion(mejor_individuo, mejor_fitness, gen, historico)
                
                if resultado == "salir":
                    ejecutando = False
                    break
                elif resultado == "reiniciar":
                    historico.clear()
                    break
                elif resultado == "nueva":
                    mejor_individuo = None
                    historico.clear()
                    break
                
                # Terminar si se alcanza fitness óptimo
                if mejor_fitness >= 100:
                    break
        
        # Mostrar información actual
        if mejor_individuo:
            info_texto = f"Gen {generacion_actual} | V={mejor_individuo[0]}, B={mejor_individuo[1]}, S={mejor_individuo[2]} | Fitness={mejor_fitness}"
            info_surf = font.render(info_texto, True, NEGRO)
            info_rect = info_surf.get_rect(center=(ANCHO // 2, 150))
            pantalla.blit(info_surf, info_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()