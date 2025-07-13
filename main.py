import pygame
from random import randint

pygame.init()

# --- Window ---
width, height = 500, 700
scr = pygame.display.set_mode((width, height))
pygame.display.set_caption('Invert flappy')
bg1 = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (width, height))
bg2 = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (width, height))
speed = 3
bg1_x = 0
bg2_x = width

# --- Classes ---
class GameSprites(pygame.sprite.Sprite):
    def __init__(self, sprite_image, spritex, spritey, sizex, sizey, sprite_speed):
        super().__init__()
        self.original_image = pygame.image.load(sprite_image)
        self.speed = sprite_speed
        self.rect = pygame.Rect(spritex, spritey, sizex, sizey)
        self.img = pygame.transform.scale(self.original_image, (sizex, sizey))

    def resize(self, sizex, sizey):
        self.rect.width = sizex
        self.rect.height = sizey
        self.img = pygame.transform.scale(self.original_image, (sizex, sizey))

    def draw(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, img_normal_path, img_flap_path, x, y, w, h):
        super().__init__()
        self.img_normal = pygame.transform.scale(pygame.image.load(img_normal_path), (w, h))
        self.img_flap = pygame.transform.scale(pygame.image.load(img_flap_path), (w, h))
        self.img = self.img_normal
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 0
        self.gravity = 1
        self.flap_strength = -8
        self.max_velocity = 10

    def draw(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))

    def update(self, pipeA, pipeB):
        global score, add, over, game, score_idx
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game == 'play':
            self.velocity = self.flap_strength
            self.img = self.img_flap
        else:
            self.img = self.img_normal

        self.velocity += self.gravity
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity

        self.rect.y -= self.velocity

        if add:
            if self.rect.x > pipeA.rect.x or self.rect.x > pipeB.rect.x:
                score += 1
                scored.play()
                score_idx += 1
                add = False
        elif self.rect.x < pipeA.rect.x:
            add = True

        if (
            self.rect.bottom < 0
            or self.rect.colliderect(ground1)
            or self.rect.colliderect(ground2)
            or self.rect.colliderect(pipeA)
            or self.rect.colliderect(pipeB)
        ):
            die.play()
            over = True

# --- Ground ---
ground1 = GameSprites('assets/images/base.png', 0, height - 120, width + 2, 150, speed)
ground2 = GameSprites('assets/images/base.png', width, height - 120, width + 2, 150, speed)

# --- Pipes ---
gap = randint(180, 250)
def create_pipes():
    top_height = randint(100, height - gap - 150)
    bottom_y = top_height + gap
    bottom_height = height - bottom_y
    p1 = GameSprites('assets/images/pipe-down.png', width + 100, 0, 80, top_height, speed)
    p2 = GameSprites('assets/images/pipe-up.png', width + 100, bottom_y, 80, bottom_height, speed)
    return p1, p2

pipe1, pipe2 = create_pipes()

# --- Player ---
player = Player('assets/images/bird2.png', 'assets/images/bird1.png', width // 2 - 120, height // 2, 50, 50)

# --- Font ---
font0 = pygame.font.Font('assets/font/04B_19__.TTF', 85)
font1 = pygame.font.Font('assets/font/04B_19__.TTF', 50)
score = 0
score_idx = 0
start_txt = font1.render('SPACE', True, (255, 255, 255))
start_width = start_txt.get_width()

# --- Sound ---
die = pygame.mixer.Sound('assets/sound/die.ogg')
scored = pygame.mixer.Sound('assets/sound/point.ogg')

# --- Game values ---
run = True
clock = pygame.time.Clock()
FPS = 60
add = True
over = False
game = 'start'

# --- Main game ---
pygame.mouse.set_visible(False)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game == 'start':
                game = 'play'
            
    scr.blit(bg1, (bg1_x, 0))
    scr.blit(bg2, (bg2_x, 0))
    
    if score_idx == 5:
        score_idx = 0
        speed += 1
    
    if game == 'start':
        scr.blit(start_txt, (width // 2 - (start_width // 2), height - (height // 3)))

    if game == 'play':
        bg1_x -= speed / 2
        bg2_x -= speed / 2
        if bg1_x <= -width:
            bg1_x = width
        if bg2_x <= -width:
            bg2_x = width

    pipe1.draw()
    pipe2.draw()
    if game == 'play':
        pipe1.rect.x -= speed
        pipe2.rect.x -= speed

        if pipe1.rect.right <= 0:
            pipe1, pipe2 = create_pipes()

    ground1.draw()
    ground2.draw()
    if game == 'play':
        ground1.rect.x -= speed
        ground2.rect.x -= speed
        if ground1.rect.right <= 0:
            ground1.rect.x = ground2.rect.right
        if ground2.rect.right <= 0:
            ground2.rect.x = ground1.rect.right

    player.draw()
    if not over and game == 'play':
        player.update(pipe1, pipe2)

    score_txt = font0.render(f'{score}', True, (255, 70, 150))
    scr.blit(score_txt, (width // 2 - score_txt.get_width() // 2, 40))

    if over:
        over_txt = font0.render('Game Over', True, (255, 75, 40))
        scr.blit(over_txt, (width // 2 - over_txt.get_width() // 2, height // 2 - over_txt.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3500)
        run = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
