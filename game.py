import pygame
import random

pygame.init()

# Definicion del tamaño de la ventana
ANCHO = 800
ALTO = 600
BLANCO = (255, 255, 255) # Color blanco
AZUL = (0, 0, 255) # Color azul
ROJO = (255, 0, 0) # Color rojo
NEGRO = (0, 0, 0) # Color negro


# Creacion de la ventana
pantalla = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Juego de Nave") #Titulo de la ventana

# Creamos la nave
nave = pygame.Rect(ANCHO // 2 -25, ALTO - 50, 30, 30) # Objeto rectangular en la posicion (ANCHO // - 25, ALTO - 50)(x,y) de tamaño 50x30

# Color de la nave
color_nave = BLANCO

# Velocidad de la nave
velocidad_nave = 8

# Lista para almacenar los proyectiles
proyectiles = []

# Intervalo entre disparos en milisegundos
tiempo_entre_disparos = 200
ultimo_disparo = 0 # Almacena el tiempo del ultimo disparo

# Definimos las propiedades de los proyectiles
color_proyectil = ROJO
velocidad_proyectil = 7

# Definimos los objetos enemigos
enemigos = []

# Definimos las propiedades de los enemigos
color_enemigos = AZUL
velocidad_enemigos = 3

# Contador de puntos
fuente = pygame.font.Font(None, 36)
puntos = 0

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        # Comprobacion para saber si cerrar la ventana
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    # Obtencion de las teclas presionadas
    teclas = pygame.key.get_pressed()
    
    # Movimiento de la nave
    if teclas[pygame.K_LEFT] and nave.left > 0:
        nave.x -= velocidad_nave
    if teclas[pygame.K_RIGHT] and nave.right < ANCHO:
        nave.x += velocidad_nave
    
    # Disparo de los proyectiles
    tiempo_actual = pygame.time.get_ticks() # Tiempo actual en milisegundos
    if teclas[pygame.K_SPACE]:
        if tiempo_actual - ultimo_disparo > tiempo_entre_disparos:
            proyectil = pygame.Rect(nave.centerx - 3, nave.top - 10, 5, 10)
            proyectiles.append(proyectil)
            ultimo_disparo = tiempo_actual      
            
    # Mover los proyectiles
    for proyectil in proyectiles[:]:
        proyectil.y -= velocidad_proyectil
        if proyectil.bottom < 0:
            proyectiles.remove(proyectil)     
            
    # Generamos enemigos de forma aleatoria
    if random.randint(0, 150) < 1:
        enemigo = {"rect": pygame.Rect(random.randint(0, ANCHO - 30), 0, 30, 30), "vidas": 2}  
        enemigos.append(enemigo)
        
    # Movemos los enemigos
    for enemigo in enemigos[:]:
        enemigo["rect"].y += velocidad_enemigos
        if enemigo["rect"].top > ALTO:
            enemigos.remove(enemigo)
    
    # Fondo de la pantalla en negro
    pantalla.fill(NEGRO)
    
    # Pintamos la nave en la pantalla
    pygame.draw.rect(pantalla, color_nave, nave)
    
    # Pintamos los proyectiles
    for proyectil in proyectiles:
        pygame.draw.rect(pantalla, color_proyectil, proyectil)
        
    # Pintamos los enemigos en la pantalla
    for enemigo in enemigos:
        pygame.draw.rect(pantalla, color_enemigos, enemigo["rect"])
        
    # Pintamos la puntuación en la pantalla
    texto_puntuacion = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))
        
    # Comprobamos si los proyectiles "Matan" a los enemigos
    for proyectil in proyectiles[:]:
        for enemigo in enemigos[:]:
            if proyectil.colliderect(enemigo["rect"]):
                enemigo["vidas"] -= 1
                proyectiles.remove(proyectil)
                if enemigo["vidas"] <= 0:
                    enemigos.remove(enemigo)
                    puntos += 1
                    
        
    # Verificamos colisiones entre proyectiles y enemigos
    for enemigo in enemigos[:]:
        if nave.colliderect(enemigo["rect"]):
            print(f"¡Colisión! Fin del juego. Has obtenido {puntos} puntos")
            ejecutando = False
            break
        if  enemigo["rect"].top >= ALTO - 20:
            print(f"¡Te alcanzaron! Fin del juego. Has obtenido {puntos} puntos")
            ejecutando = False
            break
            
    
    # Actualizacion de la pantalla
    pygame.display.flip()
    
    # Establecer FPS (fotogramas por segundo)
    pygame.time.Clock().tick(60)

# Cerramos Pygame
pygame.quit()
            

