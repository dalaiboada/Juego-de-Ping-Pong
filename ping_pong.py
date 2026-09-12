import pygame, sys

pygame.init()

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        if self.image is None:
            self.image = self.text
            
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# --- AJUSTES VENTANA ---
ventana_ancho = 1280
ventana_alto = 720
pygame.display.set_caption("Ping Pong")
SCREEN = pygame.display.set_mode((ventana_ancho, ventana_alto))

BG = pygame.image.load("Background.png")
BG = pygame.transform.scale(BG, (ventana_ancho, ventana_alto))

def get_font(size):
    return pygame.font.Font("font.ttf", size)

# --- ASSETS ---
img_Players = "racket.png"
img_ball = "tenis_ball.png"
img_fondo = "Fondo.png"

font1 = pygame.font.Font(None, 80)
font2 = pygame.font.Font(None, 35)

P1_Win = font1.render('PLAYER 1 WIN', True, (0, 0, 0))
P2_Win = font1.render('PLAYER 2 WIN', True, (0, 0, 0))

bg_color = (47, 222, 184)
color_texto = (0, 0, 0)

Fondo_Juego = pygame.transform.scale(pygame.image.load(img_fondo), (ventana_ancho, ventana_alto))

# --- CLASES Y ESTRUCTURAS ---
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < ventana_alto - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < ventana_alto - 80:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y, 0)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self): 
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y <= 0 or self.rect.y >= ventana_alto - self.rect.height:
            self.speed_y *= -1

    def reset_position(self):
        self.rect.x = ventana_ancho // 2 - 20
        self.rect.y = ventana_alto // 2 - 20
        self.speed_x *= -1

# --- ELEMENTOS DEL JUEGO ---
def play():
    P1 = Player(img_Players, 40 , ventana_alto - 420, 60, 180, 10)
    P2 = Player(img_Players, ventana_ancho - 100, ventana_alto - 420, 60, 180, 10)
    tenis_ball = Ball(img_ball, ventana_ancho // 2 - 20, ventana_alto // 2 - 20, 50, 50, 7, 7)

    score_p1 = 0
    score_p2 = 9
    rebotes = 0
    max_puntos = 10

    x = 0
    clock = pygame.time.Clock()
    finish = False
    playing = True  # CORREGIDO: Se definió 'playing' antes del ciclo
    winner_text = None

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (finish and event.key == pygame.K_m):
                    playing = False

        if not finish:
            x -= 5

            # Movimientos
            P1.update_r()
            P2.update_l()
            tenis_ball.update()

            # Colisiones con las raquetas
            if pygame.sprite.collide_rect(P1, tenis_ball):
                tenis_ball.rect.left = P1.rect.right
                tenis_ball.speed_x *= -1
                rebotes += 1

            if pygame.sprite.collide_rect(P2, tenis_ball):
                tenis_ball.rect.right = P2.rect.left
                tenis_ball.speed_x *= -1
                rebotes += 1

            # Condición de victoria
            if tenis_ball.rect.x < 0:
                score_p2 += 1
                rebotes = 0
                tenis_ball.reset_position()
                if score_p2 >= max_puntos:
                    finish = True
                    winner_text = P2_Win

            if tenis_ball.rect.x > ventana_ancho - tenis_ball.rect.width:
                score_p1 += 1
                rebotes = 0
                tenis_ball.reset_position()
                if score_p1 >= max_puntos:
                    finish = True
                    winner_text = P1_Win

        # Renderizado
        x_relativa = x % Fondo_Juego.get_rect().width
        SCREEN.blit(Fondo_Juego, (x_relativa - Fondo_Juego.get_rect().width, 0))
        if x_relativa < ventana_ancho:
            SCREEN.blit(Fondo_Juego, (x_relativa, 0))

        P1.reset()
        P2.reset()
        tenis_ball.reset()

        texto_marcador = font2.render(f"P1: {score_p1}  |  P2: {score_p2}", True, color_texto)
        texto_rebotes = font2.render(f"Pases: {rebotes}", True, color_texto)

        SCREEN.blit(texto_marcador, (ventana_ancho // 2 - 80, 20))
        SCREEN.blit(texto_rebotes, (ventana_ancho // 2 - 50, 50))

        if finish and winner_text:
            SCREEN.blit(winner_text, (ventana_ancho // 2 - 200, ventana_alto // 2 - 50))
            msg_salida = font2.render("Presiona ESC para volver al menú", True, color_texto)
            SCREEN.blit(msg_salida, (ventana_ancho // 2 - 220, ventana_alto // 2 + 30))

        pygame.display.update()  # CORREGIDO: Se añadió 'pygame.'
        clock.tick(60)

def Practice_mode():
    while True:
        Practice_mode_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        Practice_mode_TEXT = get_font(45).render("This is the   Practice mode screen.", True, "Black")
        Practice_mode_RECT =   Practice_mode_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(  Practice_mode_TEXT,   Practice_mode_RECT)

        Practice_mode_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        Practice_mode_BACK.changeColor(  Practice_mode_MOUSE_POS)
        Practice_mode_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if   Practice_mode_BACK.checkForInput(  Practice_mode_MOUSE_POS):
                    return

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Ping Pong", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="Multiplayer", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        Practice_mode_BUTTON = Button(image=None, pos=(640, 400), 
                            text_input="  Practice mode", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON,   Practice_mode_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if   Practice_mode_BUTTON.checkForInput(MENU_MOUSE_POS):
                      Practice_mode()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
