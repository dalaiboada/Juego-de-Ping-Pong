from pygame import *

# --- ASSETS ---

# Imágenes
 # fondo de juego

# Texto

# Música y sonidos

#colores

bg_color = (47, 222, 184)

# --- AJUSTES VENTANA ---

ventana_ancho = 700
ventana_alto = 500

display.set_caption("Ping Pong")
ventana = display.set_mode((ventana_ancho, ventana_alto))
ventana.fill(bg_color)

# --- CLASES Y ESTRUCTURAS ---

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        key = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.x -= self.speed
        if keys[K_DOWN] and self.rect.y < ventana_alto - 80:
            self.rect.x += self.speed

    def update_l(self):
        key = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.x -= self.speed
        if keys[K_s] and self.rect.y < ventana_alto - 80:
            self.rect.x += self.speed
# ELEMENTOS DEL JUEGO

# Personajes


# CICLO PRINCIPAL DE JUEGO

finish = False
run = True 

while run:
    # EVENTOS
    for e in event.get():
        if e.type == QUIT:
            run = False       

    if not finish:
        # actualizar fondo

		# Textos
  
        # Movimientos
        """ racket.update()
        tenis_ball.update() """

        # Renderizado
        """ racket.reset()
        tenis_ball.reset() """

		# Colisiones

        display.update()
    # el ciclo se ejecuta cada 0.05 segundos
    time.delay(50)# comienza tu juego aquí!
