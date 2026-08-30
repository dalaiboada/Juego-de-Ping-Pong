from pygame import *

# --- ASSETS ---

# Imágenes

img_Players = "racket.png"
img_ball = "tenis_ball.png"
img_fondo = "Fondo.png"

 # fondo de juego

# Texto

font.init()
font1 = font.Font(None, 80)

P1_Win = font1.render('PLAYER 1 WIN', True, (255, 255, 255))
P2_Win = font1.render('PLAYER 2 WIN', True, (255, 255, 255))

font2 = font.Font(None, 35)

# Música y sonidos

#colores

bg_color = (47, 222, 184)

# --- AJUSTES VENTANA ---

ventana_ancho = 700
ventana_alto = 500
x = 0
display.set_caption("Ping Pong")
ventana = display.set_mode((ventana_ancho, ventana_alto))
Fondo = transform.scale(image.load(img_fondo), (ventana_ancho, ventana_alto))
""" ventana.fill(bg_color) """

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
        ventana.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < ventana_alto - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < ventana_alto - 80:
            self.rect.y += self.speed

# ELEMENTOS DEL JUEGO

# Personajes

P1 = Player(img_Players, 20 , ventana_alto - 300, 40, 100, 10)

P2 = Player(img_Players, ventana_ancho - 60, ventana_alto - 300, 40, 100, 10)

# CICLO PRINCIPAL DE JUEGO

finish = False
run = True 

while run:
    # EVENTOS
    for e in event.get():
        if e.type == QUIT:
            run = False       

    x_relativa = x % Fondo.get_rect().width
    ventana.blit(Fondo, (x_relativa - Fondo.get_rect().width, 0))
    if x_relativa < ventana_ancho:
        ventana.blit(Fondo,(x_relativa,0))
    x -= 5

    if not finish:
        # actualizar fondo

        """ ventana.blit(Fondo, (0, 0)) """
        """ ventana.fill(bg_color) """

		# Textos
  
        # Movimientos
        P1.update_r()
        P2.update_l()
        """ tenis_ball.update() """

        # Renderizado
        P1.reset()
        P2.reset()
        """ tenis_ball.reset() """

		# Colisiones

        display.update()
    # el ciclo se ejecuta cada 0.05 segundos
    time.delay(50)# comienza tu juego aquí!
