import pygame
import random

pygame.init()

# Definicion del tamaño de la ventana
ANCHO = 800
ALTO = 600

# Creacion de la ventana
pantalla = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Juego de Nave") #Titulo de la ventana

# Creamos la nave
nave = pygame.Rect(ANCHO // 2 -25, ALTO - 50, 30, 30) # Objeto rectangular en la posicion (ANCHO // - 25, ALTO - 50)(x,y) de tamaño 50x30

# Color de la nave
color_nave = (255, 255, 255) # Blanco

# Velocidad de la nave
velocidad_nave = 8

# Lista para almacenar los proyectiles
proyectiles = []

# Intervalo entre disparos en milisegundos
tiempo_entre_disparos = 200
ultimo_disparo = 0 # Almacena el tiempo del ultimo disparo

# Definimos las propiedades de los proyectiles
color_proyectil = (255, 0 ,0) # Rojo
velocidad_proyectil = 7

# Definimos los objetos enemigos
enemigos = []

# Definimos las propiedades de los enemigos
color_enemigos = (0, 0, 255) # Azul
velocidad_enemigos = 3

# Contador de puntos
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
    pantalla.fill((0, 0, 0))
    
    # Pintamos la nave en la pantalla
    pygame.draw.rect(pantalla, color_nave, nave)
    
    # Pintamos los proyectiles
    for proyectil in proyectiles:
        pygame.draw.rect(pantalla, color_proyectil, proyectil)
        
    # Pintamos los enemigos en la pantalla
    for enemigo in enemigos:
        pygame.draw.rect(pantalla, color_enemigos, enemigo["rect"])
        
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
            print("¡Colisión! Fin del juego")
            ejecutando = False
            break
        if  enemigo["rect"].y == ALTO - 40:
            print("¡Te alcanzaron! Fin del juego")
            ejecutando = False
            break
            
    
    # Actualizacion de la pantalla
    pygame.display.flip()
    
    # Establecer FPS (fotogramas por segundo)
    pygame.time.Clock().tick(60)

# Cerramos Pygame
pygame.quit()
            

